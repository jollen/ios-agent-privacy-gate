# Agent Action Boundary Reference

Use this reference to define what an AI or agentic workflow may do.

## Principle

AI can help prepare decisions. The user owns final decisions that affect data, people, money, communication, or external systems.

## Allowed Automatically

These are usually safe when performed locally or on already-approved input:

- Generate a title.
- Summarize text.
- Classify or tag an item.
- Rank items for display.
- Suggest next steps.
- Generate a draft checklist.
- Generate draft report text.
- Detect duplicate candidates without merging.
- Highlight missing fields.

## Requires User Confirmation

Require an explicit user action before:

- Saving AI-generated content into source-of-truth data.
- Overwriting user text.
- Merging records.
- Deleting or archiving records.
- Sending email or messages.
- Sharing files or reports.
- Exporting documents.
- Uploading content to cloud or third-party services.
- Scheduling reminders or calendar events.
- Creating tasks in external systems.
- Purchasing, subscribing, or charging.
- Inviting collaborators.
- Changing privacy settings.

## Blocked Unless Redesigned

Do not implement these as default product behavior:

- Silent external AI calls with raw user content.
- Background upload of photos, OCR text, contacts, location, journals, or reports.
- AI-only destructive actions.
- AI decisions that cannot be reviewed or reverted.
- Hidden agent chains that call external services without disclosure.
- External AI as a required dependency for core non-AI workflows.
- Security or privacy settings changed by AI.

## Draft-only Rule

External AI output should be treated as draft or suggestion. Use labels such as:

- Suggested title.
- Draft summary.
- Suggested category.
- Suggested next step.

Avoid product language implying guaranteed correctness.

## Confirmation UX Requirements

A confirmation screen should show:

- What will happen.
- Which data will be changed or sent.
- Where it will be sent, if external.
- A cancel option.
- A clear user action, such as Save, Export, Share, or Send.
