# App Store Review Reference for iOS AI Features

Use this checklist when an iOS project adds AI, LLM, or agentic workflow features.

## Files to Inspect

- `Info.plist`
- `PrivacyInfo.xcprivacy`
- localized `InfoPlist.strings`
- Settings or Privacy screen Swift files
- onboarding copy
- privacy policy and terms
- `app metadata files or release metadata files`
- App Store review notes

## Permission Strings

Permission copy should explain the direct user benefit, not internal implementation.

Good:

- Camera: "Take photos for field observations and reports."
- Speech: "Transcribe your spoken notes into observation drafts."
- Location: "Attach an optional site location to observations."

Avoid:

- "Needed for AI."
- "Used by prompt pipeline."
- "Required for agent processing."

## Privacy Manifest Review

Check whether the app or SDKs collect or transmit:

- User content.
- Photos or videos.
- Audio.
- Location.
- Contacts.
- Identifiers.
- Diagnostics.
- Usage data.

If external AI receives user content, confirm that the privacy manifest and policy are consistent with actual behavior.

## Metadata and Review Notes

App Store copy should say AI assists, not decides.

Preferred language:

- "AI can help organize selected content into drafts."
- "Suggestions should be reviewed before use."
- "External AI features can be disabled in Settings."

Avoid:

- "Fully automatic professional judgement."
- "Guaranteed detection."
- "No user review needed."
- "AI replaces professional inspection, legal, medical, financial, or safety advice."

## Review Risk Signals

Flag the feature if:

- It sends photos, OCR text, or transcripts externally without clear disclosure.
- It has no Settings control.
- It can take external actions without confirmation.
- It claims authoritative diagnosis or compliance decisions.
- It hides AI provider or data transfer behavior.
- It fails when external AI is unavailable.
