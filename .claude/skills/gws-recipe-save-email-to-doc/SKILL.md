---
name: gws-recipe-save-email-to-doc
description: >-
  Save a Gmail message body into a Google Doc for archival or reference. Use
  when the user asks to archive an email to Docs, save email content as a
  document, or create a Doc from an email. Do NOT use for email forwarding
  (use gws-gmail) or saving attachments to Drive (use gws-drive). Korean
  triggers: "이메일 보관", "메일 문서화".
disable-model-invocation: true
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

## Examples

### Example 1: Basic operation

**User says:** "Archive an email to Docs"

**Actions:**
1. Verify `gws` CLI is authenticated (`gws gmail +triage --max 1 2>&1 | head -3`)
2. Execute the appropriate `gws` command with required parameters
3. Confirm the result and report back

### Example 2: Troubleshooting

**User says:** "The command failed with an authentication error"

**Actions:**
1. Verify `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` is set: `echo $GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE`
2. Re-authenticate: `python3 ~/.config/gws/oauth2_manual.py`
3. Clean stale caches: `rm -f ~/.config/gws/token_cache.json ~/.config/gws/credentials.enc`
4. Retry the original command
## Error Handling

| Issue | Resolution |
|-------|-----------|
| Authentication error | Run `python3 ~/.config/gws/oauth2_manual.py` and clean caches (`rm -f ~/.config/gws/token_cache.json ~/.config/gws/credentials.enc`) |
| API rate limit | Wait and retry. For bulk operations, add delays between requests |
| Resource not found | Verify the resource ID/name and check permissions |
