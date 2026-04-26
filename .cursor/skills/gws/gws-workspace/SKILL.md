---
name: gws-workspace
description: >-
  Install, authenticate, and configure the Google Workspace CLI (gws) for
  controlling Gmail, Drive, Calendar, Sheets, Docs, and Chat from the terminal.
  Use when the user asks to set up gws, configure Google Workspace CLI,
  authenticate with Google, or start the gws MCP server. Do NOT use for
  service-specific operations (use gws-gmail, gws-drive, gws-calendar,
  gws-sheets, gws-docs, or gws-chat instead). Korean triggers: "구글 워크스페이스", "gws 설정".
metadata:
  author: "googleworkspace/cli (adapted)"
  version: "1.0.0"
  category: "integration"
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

### Manual OAuth2 Bypass (REQUIRED — default method)

The `gws` CLI's built-in encrypted credential store (`credentials.enc`) fails on macOS due to Keychain integration issues. **Always use the manual OAuth2 bypass** which stores plain-text credentials at `~/.config/gws/credentials.json`.

**Setup (already configured in `~/.zshrc`):**

```bash
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE="/Users/hanhyojung/.config/gws/credentials.json"
```

**Authenticate or re-authenticate:**

```bash
python3 ~/.config/gws/oauth2_manual.py
```

This script opens a browser for Google OAuth2 consent, captures the authorization code via a local HTTP server, exchanges it for tokens with full scopes (Drive, Gmail, Calendar, Sheets, Docs, Chat), and writes `credentials.json` with `0o600` permissions.

**After authentication, clean stale caches:**

```bash
rm -f ~/.config/gws/token_cache.json ~/.config/gws/credentials.enc
```

**Verify:**

```bash
gws drive files list 2>&1 | head -3
gws gmail +triage --max 1 2>&1 | head -3
gws calendar +agenda --today 2>&1 | head -3
```

> **Note**: `warning: failed to decrypt token cache` may appear — this is non-blocking. The `credentials.json` bypass ensures all commands work.

### Service Account (CI / headless)

```bash
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/service-account.json
export GOOGLE_WORKSPACE_CLI_IMPERSONATED_USER=admin@example.com
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

## Examples

### Example 1: Basic operation

**User says:** "Set up gws"

**Actions:**
1. Verify `gws` CLI is authenticated (`gws drive files list 2>&1 | head -3`)
2. Execute the appropriate `gws` command with required parameters
3. Confirm the result and report back

### Example 2: Troubleshooting

**User says:** "The command failed with an authentication error"

**Actions:**
1. Check auth status: `gws drive files list 2>&1 | head -3` (real API call, not `gws auth status`)
2. Re-authenticate if expired: `python ~/.config/gws/oauth2_manual.py && rm ~/.config/gws/token_cache.json credentials.enc 2>/dev/null`
3. Retry the original command
