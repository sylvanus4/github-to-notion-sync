---
name: gws-docs
description: >-
  Manage Google Docs via the gws CLI -- create documents, append text, and read
  content. Use when the user asks to create a Google Doc, write to a document,
  or read document content. Do NOT use for Google Sheets (use gws-sheets), Drive
  file management (use gws-drive), or local markdown files (handle locally).
  Korean triggers: "구글 문서", "문서 작성".
metadata:
  author: "googleworkspace/cli (adapted)"
  version: "1.0.0"
  category: "integration"
---
# Google Docs

> **Prerequisites**: `gws` CLI installed + `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` env var set. See `gws-workspace` skill for the manual OAuth2 bypass setup.

```bash
gws docs <resource> <method> [flags]
```

## Quick Commands

### Append Text

```bash
gws docs +write --document <ID> --text <TEXT>
```

| Flag | Required | Description |
|------|----------|-------------|
| `--document` | Yes | Document ID |
| `--text` | Yes | Plain text to append |

Text is inserted at the end of the document body. For rich formatting, use the raw `batchUpdate` API.

> **Write command** -- confirm with the user before executing.

## Raw API Resources

### documents

- `batchUpdate` -- apply structured updates (insert text, formatting, tables)
- `create` -- create a blank document with a title
- `get` -- get the latest version of a document

## Discovering Commands

```bash
gws docs --help
gws schema docs.documents.create
gws schema docs.documents.get
gws schema docs.documents.batchUpdate
```

## Common Patterns

```bash
# Create a new document
gws docs documents create --json '{"title": "Meeting Notes - March 2026"}'

# Get document content
gws docs documents get --params '{"documentId": "DOC_ID"}'

# Append text
gws docs +write --document DOC_ID --text 'Action items from today meeting...'

# Batch update (insert text at index)
gws docs documents batchUpdate \
  --params '{"documentId": "DOC_ID"}' \
  --json '{"requests": [{"insertText": {"location": {"index": 1}, "text": "Hello World\n"}}]}'
```

## Examples

### Example 1: Basic operation

**User says:** "Create a Google Doc"

**Actions:**
1. Verify `gws` CLI is authenticated (try a simple read command)
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
