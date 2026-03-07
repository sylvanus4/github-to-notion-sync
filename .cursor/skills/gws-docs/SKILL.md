---
name: gws-docs
description: >-
  Manage Google Docs via the gws CLI -- create documents, append text, and
  read content. Use when the user asks to create a Google Doc, write to a
  document, or read document content. Do NOT use for Google Sheets (use
  gws-sheets), Drive file management (use gws-drive), or local markdown
  files (handle locally).
metadata:
  author: googleworkspace/cli (adapted)
  version: 1.0.0
---

# Google Docs

> **Prerequisites**: `gws` must be installed and authenticated. See `gws-workspace` skill.

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
