---
name: gws-workspace
description: >-
  Install, authenticate, and configure the Google Workspace CLI (gws) for
  controlling Gmail, Drive, Calendar, Sheets, Docs, and Chat from the terminal.
  Use when the user asks to set up gws, configure Google Workspace CLI,
  authenticate with Google, or start the gws MCP server. Do NOT use for
  service-specific operations (use gws-gmail, gws-drive, gws-calendar,
  gws-sheets, gws-docs, or gws-chat instead).
metadata:
  author: googleworkspace/cli (adapted)
  version: 1.0.0
---

# Google Workspace CLI — Setup & Reference

One CLI for all of Google Workspace. Built for humans and AI agents.

> For full CLI context and agent rules, see [references/context.md](references/context.md).
> For a quick command cheatsheet, see [references/cli-cheatsheet.md](references/cli-cheatsheet.md).

## Installation

```bash
npm install -g @googleworkspace/cli
```

Verify: `gws --version`

Pre-built binaries also available on [GitHub Releases](https://github.com/googleworkspace/cli/releases).

## Authentication

### Interactive (recommended)

```bash
gws auth setup      # one-time: creates GCP project, enables APIs, logs in (requires gcloud)
gws auth login      # subsequent logins with scope selection
```

For unverified apps (testing mode), select individual service scopes:

```bash
gws auth login --scopes drive,gmail,calendar
```

### Multiple Accounts

```bash
gws auth login --account work@corp.com
gws auth login --account personal@gmail.com
gws auth list
gws auth default work@corp.com
gws --account personal@gmail.com drive files list
```

### Headless / CI

```bash
gws auth export --unmasked > credentials.json
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/credentials.json
```

### Service Account

```bash
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/service-account.json
export GOOGLE_WORKSPACE_CLI_IMPERSONATED_USER=admin@example.com  # for domain-wide delegation
```

### Pre-obtained Token

```bash
export GOOGLE_WORKSPACE_CLI_TOKEN=$(gcloud auth print-access-token)
```

## MCP Server

Start an MCP server over stdio for AI agent integration:

```bash
gws mcp -s drive,gmail,calendar   # expose specific services
gws mcp -s all                    # expose all services
```

MCP client configuration (Claude Desktop, Cursor, VS Code):

```json
{
  "mcpServers": {
    "gws": {
      "command": "gws",
      "args": ["mcp", "-s", "drive,gmail,calendar"]
    }
  }
}
```

Keep the service list to what you need — each service adds 10-80 tools.

## Core Syntax

```bash
gws <service> <resource> [sub-resource] <method> [flags]
```

## Global Flags

| Flag | Description |
|------|-------------|
| `--format <fmt>` | Output: `json` (default), `table`, `yaml`, `csv` |
| `--dry-run` | Validate without calling the API |
| `--sanitize <tmpl>` | Screen responses through Model Armor |
| `--fields <mask>` | Limit response fields (critical for context efficiency) |

## Method Flags

| Flag | Description |
|------|-------------|
| `--params '{"key": "val"}'` | URL/query parameters |
| `--json '{"key": "val"}'` | Request body |
| `--upload <path>` | Upload file (multipart) |
| `-o, --output <path>` | Save binary responses to file |
| `--page-all` | Auto-paginate (NDJSON output) |
| `--page-limit <N>` | Max pages (default: 10) |

## Security Rules

- **Never** output secrets (API keys, tokens) directly
- **Always** confirm with user before write/delete commands
- Prefer `--dry-run` for destructive operations
- Use `--fields` to minimize response size and protect context window
- Use `--sanitize` for PII/content safety screening

## Schema Discovery

When unsure about JSON payload structure:

```bash
gws schema <service>.<resource>.<method>
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Access blocked" / 403 | Add yourself as test user in OAuth consent screen |
| "Google hasn't verified this app" | Click Advanced → Go to app (safe for personal use) |
| Too many scopes error | Use `--scopes drive,gmail,calendar` instead of all |
| `gcloud` not found | Use manual OAuth setup or install gcloud CLI |
| API not enabled (403 accessNotConfigured) | Click the enable_url in the error, wait 10s, retry |
