#!/usr/bin/env python3
"""
Static scanner for common iOS AI/privacy review signals.

This scanner is intentionally conservative. It highlights files and patterns
that require human review; it does not prove compliance.
"""
from __future__ import annotations

import argparse
import json
import os
import plistlib
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

TEXT_EXTENSIONS = {
    ".swift", ".m", ".mm", ".h", ".plist", ".strings", ".json", ".md",
    ".yml", ".yaml", ".xcprivacy", ".entitlements"
}

SKIP_DIRS = {
    ".git", ".build", "DerivedData", "build", "Pods", ".swiftpm",
    "node_modules", "Carthage", ".idea", ".vscode"
}

PATTERNS = [
    ("external_ai_provider", "medium", re.compile(r"\b(OpenAI|Anthropic|Claude|Gemini|Mistral|Groq|Cohere|Perplexity|ChatGPT)\b", re.I)),
    ("ai_language", "low", re.compile(r"\b(ai|agent|agentic|llm|prompt|model|completion|chat completions?)\b", re.I)),
    ("possible_api_key", "high", re.compile(r"\b(sk-[A-Za-z0-9_-]{12,}|api[_-]?key|secret|bearer token|authorization:)\b", re.I)),
    ("external_network_call", "medium", re.compile(r"\b(URLSession|http://|https://|Alamofire|Network\.framework)\b", re.I)),
    ("upload_or_send", "medium", re.compile(r"\b(upload|send|share|export|post|put|delete|archive|sync|forward|email)\b", re.I)),
    ("sensitive_data", "medium", re.compile(r"\b(camera|photo|image|ocr|vision|speech|transcript|location|contact|address|phone|email|journal|diary|receipt|business card|customer|client)\b", re.I)),
    ("background_processing", "medium", re.compile(r"\b(BGTask|background|silent|daemon|timer|schedule)\b", re.I)),
    ("privacy_settings", "info", re.compile(r"\b(Settings|Privacy|Consent|Toggle|external ai|AI Suggestions|Allow external)\b", re.I)),
]

REQUIRED_PRIVACY_HINTS = [
    "PrivacyInfo.xcprivacy",
]

@dataclass
class Finding:
    severity: str
    kind: str
    file: str
    line: int
    excerpt: str


def iter_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix in TEXT_EXTENSIONS or filename in {"Info.plist", "PrivacyInfo.xcprivacy"}:
                yield path


def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-16")
        except Exception:
            return ""
    except Exception:
        return ""


def scan_text(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_files(root):
        text = safe_read(path)
        if not text:
            continue
        rel = str(path.relative_to(root))
        for idx, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped:
                continue
            for kind, severity, pattern in PATTERNS:
                if pattern.search(stripped):
                    findings.append(Finding(
                        severity=severity,
                        kind=kind,
                        file=rel,
                        line=idx,
                        excerpt=stripped[:240],
                    ))
    return findings


def inspect_plists(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in root.rglob("Info.plist"):
        try:
            with path.open("rb") as f:
                plist = plistlib.load(f)
        except Exception:
            continue
        rel = str(path.relative_to(root))
        permission_keys = [
            "NSCameraUsageDescription",
            "NSPhotoLibraryUsageDescription",
            "NSPhotoLibraryAddUsageDescription",
            "NSSpeechRecognitionUsageDescription",
            "NSMicrophoneUsageDescription",
            "NSLocationWhenInUseUsageDescription",
            "NSContactsUsageDescription",
        ]
        for key in permission_keys:
            if key in plist:
                value = str(plist.get(key, ""))
                if re.search(r"prompt|agent|pipeline|internal|llm", value, re.I):
                    severity = "medium"
                else:
                    severity = "info"
                findings.append(Finding(severity, "permission_string", rel, 0, f"{key}: {value}"))
    return findings


def project_hints(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    found_privacy = any(p.name == "PrivacyInfo.xcprivacy" for p in root.rglob("PrivacyInfo.xcprivacy"))
    if not found_privacy:
        findings.append(Finding("medium", "missing_privacy_manifest", ".", 0, "PrivacyInfo.xcprivacy not found"))

    settings_files = [p for p in root.rglob("*Settings*.swift") if all(part not in SKIP_DIRS for part in p.parts)]
    if not settings_files:
        findings.append(Finding("low", "missing_settings_surface", ".", 0, "No *Settings*.swift file found; verify AI/privacy controls exist elsewhere."))
    return findings


def summarize(findings: list[Finding]) -> dict[str, int]:
    counts = {"high": 0, "medium": 0, "low": 0, "info": 0}
    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan an iOS project for AI/privacy review signals.")
    parser.add_argument("path", help="Path to an iOS project or repository root")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--max-findings", type=int, default=200, help="Maximum findings to print")
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"path does not exist: {root}")

    findings = scan_text(root) + inspect_plists(root) + project_hints(root)
    findings.sort(key=lambda f: {"high": 0, "medium": 1, "low": 2, "info": 3}.get(f.severity, 9))
    result = {
        "root": str(root),
        "summary": summarize(findings),
        "findings": [asdict(f) for f in findings[: args.max_findings]],
        "truncated": len(findings) > args.max_findings,
        "note": "Findings are review signals, not proof of a violation. Apply the skill review workflow before approving AI features.",
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Scan root: {root}")
        print("Summary:", result["summary"])
        for finding in result["findings"]:
            print(f"[{finding['severity']}] {finding['kind']} {finding['file']}:{finding['line']} - {finding['excerpt']}")
        if result["truncated"]:
            print("... findings truncated; increase --max-findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
