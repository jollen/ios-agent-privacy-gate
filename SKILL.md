---
name: ios-agent-privacy-gate
description: security and privacy review workflow for ios apps that add ai, llm, agentic ai, prompt/context export, ocr-to-ai, ai drafts, ai classification, ai summaries, external model calls, or automation features. use this skill when reviewing or modifying swift/swiftui projects, release metadata, app store metadata, infoplist permission strings, privacyinfo.xcprivacy, settings screens, or roadmap items involving ai agents, local-first ai, external ai providers, data redaction, user consent, or agent action boundaries.
---

# iOS Agent Privacy Gate

Use this skill to keep Agentic AI features safe, private, reviewable, and App Store friendly in iOS projects.

The core principle is: **security and privacy first; AI output is a draft unless the user explicitly confirms an action.**

## Required Review Workflow

For every iOS AI or agentic feature, complete these gates in order.

### 1. Feature boundary

Identify the exact AI feature and write a one-paragraph summary:

- What user problem it solves.
- What inputs it needs.
- What output it creates.
- Whether it changes app data or only proposes a draft.
- Whether any data leaves the device.

Do not approve broad features such as "AI assistant" without narrowing the boundary.

### 2. Data boundary

Classify every input using `references/data-boundary.md`.

Default rule: **data stays on device unless there is a specific, user-visible reason to send it out.**

Flag these as sensitive by default:

- Photos, OCR text, speech transcripts, journal entries, business-card data, reports, files, contact data, location, precise timestamps, customer names, company names, addresses, phone numbers, emails, IDs, financial amounts, medical content, legal content, credentials, API keys, and internal prompts.

Require redaction before external AI whenever possible.

### 3. Agent action boundary

Classify the action using `references/agent-action-boundary.md`.

Allow by default:

- Summarize, classify, tag, score for sorting, suggest next steps, draft text, generate checklist suggestions.

Require explicit user confirmation:

- Save, overwrite, delete, archive, send, share, upload, schedule, purchase, invite, message, email, export, sync, or modify source-of-truth data.

Block unless specifically redesigned:

- Silent background uploads, automatic external side effects, hidden data sharing, destructive AI decisions, AI-only source-of-truth changes, or external AI use without Settings disclosure.

### 4. Local-first alternative

Before adding external AI, check whether the feature can be completed with:

- iOS SDK frameworks such as Vision, Speech, NaturalLanguage, CoreLocation, PDFKit, App Intents, or SwiftData.
- A rules-first classifier.
- A deterministic template.
- On-device model inference.

If local-first is sufficient, recommend it. External AI should be optional and additive.

### 5. UX and settings disclosure

Require a visible Settings area for AI/privacy controls when external AI or context export exists.

The UI should state:

- Whether external AI is off or on.
- What categories of data may be used.
- Whether raw content is sent or redacted.
- That AI suggestions are drafts.
- That the user can disable external AI.

Avoid UI labels such as "prompt", "system prompt", "agent pipeline", or internal engineering language in user-facing production copy.

### 6. App Store and release copy review

Review the following if present:

- `Info.plist`
- `PrivacyInfo.xcprivacy`
- `app metadata files or release metadata files`
- privacy policy and terms pages
- App Store review notes
- onboarding and Settings copy

Use `references/app-store-review.md` and `references/release-copy-rules.md`.

### 7. Repository scan

When a project folder is available, run:

```bash
python3 scripts/scan_ios_ai_privacy.py /path/to/ios/project --json
```

Use the scan as a checklist accelerator, not as a substitute for human review. Investigate all high and medium findings.

## Output Format

Return this review format unless the user requested an implementation patch:

```markdown
# iOS Agent Privacy Gate Review

## AI Feature Summary
...

## Data Boundary Review
- Pass / Needs Work / Blocked: ...
- Sensitive data involved: ...
- External transfer: ...
- Redaction required: ...

## Agent Action Boundary Review
- Allowed draft actions: ...
- Actions requiring confirmation: ...
- Blocked actions: ...

## Local-first Review
...

## Required UI / Settings Changes
...

## App Store / Privacy Manifest Review
...

## Required Code or Product Changes
...

## Verdict
Pass / Needs Work / Blocked
```

For implementation tasks, include the same review in the completion report and state which files were changed.

## Implementation Rules

When modifying iOS code:

- Prefer local-first and rules-first behavior.
- Store AI settings with a clear model such as `AgentPrivacySettings`, `AIPrivacySettings`, or project-specific equivalent.
- Gate all context export behind explicit settings.
- Make external AI output draft-only.
- Never add silent upload, background sync, or external calls without user-visible controls.
- Keep non-AI app functionality usable when external AI is disabled.

## Resources

- `references/data-boundary.md`: classify iOS app data and decide what may leave device.
- `references/agent-action-boundary.md`: decide what AI/agents may do automatically, with confirmation, or never.
- `references/app-store-review.md`: App Store privacy and review checklist for AI features.
- `references/release-copy-rules.md`: production copy rules for AI/privacy features.
- `scripts/scan_ios_ai_privacy.py`: static scanner for common iOS AI/privacy risks.
