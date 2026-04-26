---
name: gws-sheets
description: >-
  Manage Google Sheets via the gws CLI -- read cell ranges, append rows, and
  create spreadsheets. Use when the user asks to read spreadsheet data, write to
  sheets, append rows, or create new spreadsheets. Do NOT use for Google Docs
  (use gws-docs), Drive file management (use gws-drive), or CSV files on disk
  (handle locally). Korean triggers: "구글 시트", "스프레드시트".
metadata:
  author: "googleworkspace/cli (adapted)"
  version: "1.0.0"
  category: "integration"
---
# Google Sheets

> **Prerequisites**: `gws` CLI installed + `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` env var set. See `gws-workspace` skill for the manual OAuth2 bypass setup.

```bash
gws sheets <resource> <method> [flags]
```

## Quick Commands

### Read Values

```bash
gws sheets +read --spreadsheet <ID> --range <RANGE>
```

| Flag | Required | Description |
|------|----------|-------------|
| `--spreadsheet` | Yes | Spreadsheet ID |
| `--range` | Yes | Range (e.g. `'Sheet1!A1:D10'`) |

Read-only -- never modifies the spreadsheet.

### Append Rows

```bash
gws sheets +append --spreadsheet <ID> --values 'Alice,100,true'
gws sheets +append --spreadsheet <ID> --json-values '[["a","b"],["c","d"]]'
```

| Flag | Required | Description |
|------|----------|-------------|
| `--spreadsheet` | Yes | Spreadsheet ID |
| `--values` | One of | Comma-separated values (single row) |
| `--json-values` | One of | JSON array of rows (bulk insert) |

> **Write command** -- confirm with the user before executing.

## Shell Escaping

Sheets ranges use `!` which bash interprets as history expansion. Always wrap in **single quotes**:

```bash
gws sheets spreadsheets values get \
  --params '{"spreadsheetId": "ID", "range": "Sheet1!A1:C10"}'
```

## Raw API Resources

### spreadsheets

- `batchUpdate`, `create`, `get`, `getByDataFilter`
- `developerMetadata` -- get, search
- `sheets` -- copyTo
- `values` -- append, batchClear, batchGet, batchGetByDataFilter, batchUpdate, batchUpdateByDataFilter, clear, get, update

## Discovering Commands

```bash
gws sheets --help
gws schema sheets.spreadsheets.create
gws schema sheets.spreadsheets.values.get
gws schema sheets.spreadsheets.values.append
```

## Common Patterns

```bash
# Create a spreadsheet
gws sheets spreadsheets create --json '{"properties": {"title": "Q1 Budget"}}'

# Read a range
gws sheets spreadsheets values get \
  --params '{"spreadsheetId": "ID", "range": "Sheet1!A1:D10"}'

# Append rows
gws sheets spreadsheets values append \
  --params '{"spreadsheetId": "ID", "range": "Sheet1!A1", "valueInputOption": "USER_ENTERED"}' \
  --json '{"values": [["Name", "Score"], ["Alice", 95]]}'

# Batch get multiple ranges
gws sheets spreadsheets values batchGet \
  --params '{"spreadsheetId": "ID", "ranges": "Sheet1!A1:B5,Sheet1!D1:E5"}'

# Clear a range
gws sheets spreadsheets values clear \
  --params '{"spreadsheetId": "ID", "range": "Sheet1!A1:D10"}' --dry-run
```

## Examples

### Example 1: Basic operation

**User says:** "Read spreadsheet data"

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
