## Google Drive Operations

Upload, download, search, and manage files in Google Drive via the gws CLI.

### Usage

```
/gws-files [action] [args]
```

Actions:
- `upload <path> [--parent FOLDER_ID]` -- upload a file
- `list [query]` -- list or search files
- `share <file_id> <email>` -- share a file with a user
- `audit` -- audit externally shared files

### Examples

```
/gws-files upload ./report.pdf
/gws-files list "name contains 'Budget'"
/gws-files share FILE_ID alice@company.com
/gws-files audit
```

### Execution

Read and follow the `gws-drive` skill (`.cursor/skills/gws-drive/SKILL.md`) for full CLI reference, raw API resources, and common patterns. For external sharing audit, see the `gws-recipe-audit-sharing` skill.
