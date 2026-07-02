# iOS Agent Privacy Gate

`ios-agent-privacy-gate` is a reusable ChatGPT Skill for reviewing iOS apps that introduce AI, LLM, or Agentic AI features. Its purpose is to keep AI-assisted features local-first, privacy-aware, user-confirmed, and App Store review friendly.

## What this Skill is for

Use this Skill when an iOS project adds or changes features such as:

- AI summaries, classifications, labels, or recommendations
- Agentic AI workflows or multi-step AI actions
- OCR, speech, photo, file, or note content sent to an AI model
- Prompt/context export from the app
- External AI providers such as OpenAI, Claude, Gemini, or custom LLM endpoints
- AI-generated drafts, checklists, reports, replies, or follow-up suggestions
- Settings, privacy policy, App Store metadata, or release copy related to AI

The core idea is simple:

> Security and privacy come first. AI output is a draft unless the user explicitly confirms an action.

## Main review gates

The Skill reviews AI features through these gates:

1. **Feature boundary** — define the exact AI feature, input, output, and side effects.
2. **Data boundary** — classify what data is used, whether it leaves the device, and whether redaction is required.
3. **Agent action boundary** — decide what AI may suggest, what requires confirmation, and what must be blocked.
4. **Local-first alternative** — prefer iOS SDK, deterministic rules, or on-device processing before external AI.
5. **UX and Settings disclosure** — make AI usage visible and controllable by the user.
6. **App Store and release copy review** — align `Info.plist`, `PrivacyInfo.xcprivacy`, App Store metadata, review notes, privacy copy, and terms.
7. **Repository scan** — use the bundled script to accelerate static inspection.

## Bundled script

The Skill includes:

```bash
scripts/scan_ios_ai_privacy.py
```

Example usage:

```bash
python3 scripts/scan_ios_ai_privacy.py /path/to/ios/project --json
```

The script scans for common AI/privacy indicators such as external AI references, prompt/context terminology, possible sensitive data categories, permission files, settings screens, and action verbs that may imply side effects. The scan is a checklist accelerator, not a replacement for human product/security review.

## Recommended output

A typical review should produce:

- AI Feature Summary
- Data Boundary Review
- Agent Action Boundary Review
- Local-first Alternative Review
- UX and Settings Requirements
- App Store / PrivacyInfo / Release Copy Review
- Required Changes
- Final Decision: Pass, Needs Work, or Blocked

## Design principles

- Default to local-first.
- Default deny external transfer unless explicitly justified.
- Redact before sending content to external AI.
- Treat external AI output as a draft.
- Require user confirmation for save, delete, send, share, upload, sync, purchase, schedule, or source-of-truth changes.
- Keep the app usable when external AI is disabled.
- Avoid engineering terms such as “prompt” or “agent pipeline” in production UI copy.

## Intended relationship with iOS production workflows

This Skill is designed to complement, not replace, a general iOS production pipeline. Use the production pipeline for app structure, roadmap, build checks, UI, performance, packaging, and release readiness. Use this Skill specifically when AI, LLM, privacy, context export, agent actions, or external model calls enter the product design.
