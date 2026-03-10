---
name: gws-drive
description: >-
  Manage Google Drive via the gws CLI -- upload, download, search, and share
  files and folders. Use when the user asks to upload files, list Drive
  contents, manage permissions, search Drive, or organize folders. Do NOT use
  for Sheets data (use gws-sheets), Docs content (use gws-docs), or email
  attachments (use gws-gmail).
metadata:
  author: googleworkspace/cli (adapted)
  version: 1.0.0
---

# Google Drive

> **Prerequisites**: `gws` must be installed and authenticated. See `gws-workspace` skill.

```bash
gws drive <resource> <method> [flags]
```

## Quick Commands

### Upload a File

```bash
gws drive +upload <file>
gws drive +upload ./report.pdf --parent FOLDER_ID
gws drive +upload ./data.csv --name 'Sales Data.csv'
```

| Flag | Required | Description |
|------|----------|-------------|
| `<file>` | Yes | Path to file |
| `--parent` | No | Parent folder ID |
| `--name` | No | Target filename (defaults to source name) |

MIME type is detected automatically.

> **Write command** -- confirm with the user before executing.

## Raw API Resources

### files

- `copy`, `create`, `delete`, `emptyTrash`, `export`, `generateIds`, `get`, `list`, `update`
- `download` -- download file content (use `-o` flag)

### permissions

- `create`, `delete`, `get`, `list`, `update`

### comments / replies

- CRUD on file comments and replies

### changes / channels

- `list` changes, `watch` for changes, `stop` watch channels

### drives (shared drives)

- `create`, `delete`, `get`, `hide`, `list`, `unhide`, `update`

### revisions

- `delete`, `get`, `list`, `update`

## Discovering Commands

```bash
gws drive --help
gws schema drive.files.list
gws schema drive.files.create
```

## Common Patterns

**Note**: `--fields` is NOT a standalone flag. Pass `fields` inside `--params` JSON.

```bash
# List files (use fields inside params to protect context window)
gws drive files list \
  --params '{"pageSize": 10, "fields": "files(id,name,mimeType,modifiedTime)"}'

# Search by name
gws drive files list \
  --params '{"q": "name contains '\''Report'\''", "pageSize": 10, "fields": "files(id,name)"}'

# Search by type
gws drive files list \
  --params '{"q": "mimeType = '\''application/pdf'\''", "fields": "files(id,name)"}'

# Download a file
gws drive files get --params '{"fileId": "FILE_ID"}' -o ./download.pdf

# Copy a file (template use)
gws drive files copy \
  --params '{"fileId": "TEMPLATE_ID"}' \
  --json '{"name": "My Copy"}'

# Share with a user
gws drive permissions create \
  --params '{"fileId": "FILE_ID"}' \
  --json '{"role": "writer", "type": "user", "emailAddress": "user@co.com"}'

# List permissions
gws drive permissions list --params '{"fileId": "FILE_ID"}'

# List externally shared files
gws drive files list \
  --params '{"q": "visibility = '\''anyoneWithLink'\''", "fields": "files(id,name,owners)"}'

# Create a folder
gws drive files create \
  --json '{"name": "Project Docs", "mimeType": "application/vnd.google-apps.folder"}'

# Paginate all files
gws drive files list --params '{"pageSize": 100}' --page-all | jq -r '.files[].name'
```
