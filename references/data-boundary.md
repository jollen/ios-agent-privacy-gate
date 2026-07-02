# Data Boundary Reference

Use this reference to decide what data an iOS AI feature may process locally, redact, or send externally.

## Default Rule

Data should stay on device unless the feature cannot work without external processing and the user can understand and control that transfer.

## Data Classes

### Public or low sensitivity

May be used for local or external AI when the app explains the feature:

- App-defined category names.
- Non-identifying template labels.
- Generic UI copy.
- User-selected non-personal preferences.

Still avoid sending unnecessary data.

### Personal or customer-identifying

Redact before external AI unless raw data is strictly required:

- Names.
- Phone numbers.
- Email addresses.
- Addresses.
- Company names tied to a person or customer.
- Customer/project/site names.
- Location names or precise coordinates.
- Calendar event details.
- Contact records.
- Device identifiers.

### Sensitive by default

Do not send externally unless the product explicitly depends on it, the privacy policy covers it, and the user has a clear control:

- Photos and videos.
- OCR text from documents, signs, receipts, business cards, equipment labels, or field reports.
- Speech transcripts.
- Journal or mental-health content.
- Medical, legal, financial, housing, employment, or identity-related information.
- Children or school-related records.
- Authentication secrets, API keys, tokens, passwords, private keys.
- Internal prompts, system instructions, hidden scoring rules, or proprietary logic.

### Blocked from external AI in normal product flows

- API keys, credentials, tokens, private keys.
- Raw address books or contact databases.
- Hidden internal prompts that reveal security-sensitive implementation.
- Data the user did not intentionally select for the AI feature.
- Background-collected content with no visible user action.

## Redaction Checklist

Before external AI, consider removing or generalizing:

- Person names -> `[person]`.
- Customer/company names -> `[customer]` or `[company]`.
- Emails -> `[email]`.
- Phone numbers -> `[phone]`.
- Addresses -> `[address]`.
- Coordinates -> coarse area or `[location]`.
- Exact dates/times -> relative or coarse time.
- Amounts -> ranges if possible.
- Photos -> derived labels or local OCR summary instead of raw image.

## Approval Questions

Ask and answer:

1. What exact fields are sent out?
2. Why are they needed?
3. Can the feature work with derived labels instead of raw content?
4. Can the app redact identifiers first?
5. Is the transfer visible in Settings or onboarding?
6. Can the user disable it?
7. Does the app still work when disabled?
