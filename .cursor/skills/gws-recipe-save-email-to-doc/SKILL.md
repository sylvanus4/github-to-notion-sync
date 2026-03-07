---
name: gws-recipe-save-email-to-doc
description: >-
  Save a Gmail message body into a Google Doc for archival or reference.
  Use when the user asks to archive an email to Docs, save email content
  as a document, or create a Doc from an email. Do NOT use for email
  forwarding (use gws-gmail) or saving attachments to Drive (use gws-drive).
metadata:
  author: googleworkspace/cli (adapted)
  version: 1.0.0
---

# Recipe: Save Gmail Message to Google Docs

> **Required skills**: `gws-gmail`, `gws-docs`

Save a Gmail message body into a Google Doc for archival or reference.

## Steps

1. **Find the message** by searching:

```bash
gws gmail users messages list \
  --params '{"userId": "me", "q": "subject:important from:boss@company.com"}' \
  --format table
```

2. **Get message content** and extract the body:

```bash
gws gmail users messages get \
  --params '{"userId": "me", "id": "MSG_ID"}'
```

Extract the email body from the JSON response:
- Plain text: `payload.parts[]` where `mimeType` is `text/plain`, then base64-decode `body.data`
- Simple messages: `payload.body.data` (base64-encoded)
- Extract `From`, `Subject`, `Date` from `payload.headers[]`

3. **Create a new document**:

```bash
gws docs documents create \
  --json '{"title": "Saved Email - Important Update"}'
```

4. **Write the extracted email body** to the document:

```bash
gws docs +write --document DOC_ID \
  --text 'From: boss@company.com
Subject: Important Update
Date: 2026-03-05

[Decoded email body text here]'
```

> **Write command** -- the document creation and write steps modify Google Docs.

## Tips

- For emails with HTML content, extract the `text/plain` part or strip HTML tags before writing
- `+write` appends plain text; it does not render markdown or HTML formatting
- Add the original message link in the doc for reference
