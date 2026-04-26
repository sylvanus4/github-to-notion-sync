# Google Workspace CLI — Agent Context

## Rules of Engagement

- **Schema Discovery**: If unsure about JSON payload structure, run `gws schema <service>.<resource>.<method>` first.
- **Context Window Protection**: Workspace APIs return massive JSON. ALWAYS use `--fields` when listing or getting resources: `--params '{"fields": "id,name"}'`
- **Dry-Run Safety**: Always use `--dry-run` for mutating operations (create, update, delete) before actual execution.
- **Confirm Writes**: Always confirm with the user before executing write/delete commands.

## Architecture

`gws` is a Rust CLI that dynamically generates its command surface at runtime by parsing Google Discovery Service JSON documents. It does NOT use static API crates.

### Two-Phase Parsing

1. Read `argv[1]` to identify the service (e.g., `drive`)
2. Fetch the Discovery Document (cached 24h)
3. Build a `clap::Command` tree from the document
4. Re-parse remaining arguments
5. Authenticate, build HTTP request, execute

All output (success, errors, metadata) is structured JSON.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GOOGLE_WORKSPACE_CLI_TOKEN` | Pre-obtained OAuth2 access token (highest priority) |
| `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` | Path to OAuth credentials JSON |
| `GOOGLE_WORKSPACE_CLI_ACCOUNT` | Default account email for multi-account |

Variables can also live in a `.env` file.

## Auth Precedence

| Priority | Source |
|----------|--------|
| 1 | Access token (`GOOGLE_WORKSPACE_CLI_TOKEN`) |
| 2 | Credentials file (`GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE`) |
| 3 | Per-account encrypted credentials (`gws auth login`) | **Unreliable — DO NOT USE** (Keychain failures) |
| 4 | Plaintext credentials (`~/.config/gws/credentials.json`) |

Account resolution: `--account` flag > env var > default in `accounts.json`.

## Usage Patterns

### Reading Data

```bash
gws drive files list --params '{"q": "name contains \"Report\"", "pageSize": 10}' --fields "files(id,name,mimeType)"
gws gmail users messages get --params '{"userId": "me", "id": "MSG_123"}'
```

### Writing Data

```bash
gws gmail users messages send --params '{"userId": "me"}' --json '{"raw": "BASE64..."}'
gws sheets spreadsheets create --json '{"properties": {"title": "Q4 Budget"}}'
```

### Pagination

```bash
gws admin users list --params '{"domain": "example.com"}' --page-all
```

### Schema Introspection

```bash
gws schema drive.files.list
gws schema sheets.spreadsheets.create
```
