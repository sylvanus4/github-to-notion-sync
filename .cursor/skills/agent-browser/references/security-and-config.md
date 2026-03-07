# Agent Browser — Security and Configuration

## Table of Contents

- [Security Features](#security-features) (Content Boundaries, Domain Allowlist, Action Policy, Confirmation, Output Limits, Auth Vault)
- [Configuration File](#configuration-file)
- [Environment Variables](#environment-variables)
- [Global CLI Options](#global-cli-options)

## Security Features

All security features are opt-in. Default behavior imposes no restrictions.

### Content Boundaries

Wrap page output in delimiters so LLMs distinguish tool output from untrusted page content:

```bash
export AGENT_BROWSER_CONTENT_BOUNDARIES=1
agent-browser snapshot
# --- AGENT_BROWSER_PAGE_CONTENT nonce=<hex> origin=https://example.com ---
# [accessibility tree]
# --- END_AGENT_BROWSER_PAGE_CONTENT nonce=<hex> ---
```

### Domain Allowlist

Restrict navigation to trusted domains. Wildcards like `*.example.com` also match the bare domain. Sub-resource requests, WebSocket, and EventSource connections to non-allowed domains are blocked.

```bash
export AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com,*.cdn.example.com"
agent-browser open https://example.com        # OK
agent-browser open https://malicious.com       # Blocked
```

### Action Policy

Gate destructive actions with a policy file:

```bash
export AGENT_BROWSER_ACTION_POLICY=./policy.json
```

Example `policy.json`:

```json
{"default": "deny", "allow": ["navigate", "snapshot", "click", "scroll", "wait", "get"]}
```

### Action Confirmation

Require explicit approval for sensitive categories:

```bash
export AGENT_BROWSER_CONFIRM_ACTIONS="eval,download"
```

### Output Length Limits

Prevent context flooding from large pages:

```bash
export AGENT_BROWSER_MAX_OUTPUT=50000
```

### Auth Vault Encryption

Credentials stored via `auth save` are always encrypted. A key is auto-generated at `~/.agent-browser/.encryption-key` if `AGENT_BROWSER_ENCRYPTION_KEY` is not set.

## Configuration File

Create `agent-browser.json` in the project root for persistent defaults.

Priority (lowest to highest):
1. `~/.agent-browser/config.json` (user-level)
2. `./agent-browser.json` (project-level)
3. `AGENT_BROWSER_*` environment variables
4. CLI flags

Example `agent-browser.json`:

```json
{
  "headed": true,
  "proxy": "http://localhost:8080",
  "profile": "./browser-data",
  "userAgent": "my-agent/1.0",
  "ignoreHttpsErrors": true
}
```

All CLI options map to camelCase keys (e.g., `--executable-path` becomes `"executablePath"`).

Use `--config <path>` or `AGENT_BROWSER_CONFIG` to load a custom config file.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AGENT_BROWSER_DEFAULT_TIMEOUT` | Playwright timeout in ms (default: 25000) |
| `AGENT_BROWSER_SESSION` | Named session for isolation |
| `AGENT_BROWSER_SESSION_NAME` | Auto-save/restore state persistence name |
| `AGENT_BROWSER_PROFILE` | Persistent browser profile directory |
| `AGENT_BROWSER_STATE` | Load storage state from JSON file |
| `AGENT_BROWSER_ENCRYPTION_KEY` | 64-char hex key for AES-256-GCM encryption |
| `AGENT_BROWSER_STATE_EXPIRE_DAYS` | Auto-delete states older than N days (default: 30) |
| `AGENT_BROWSER_CONTENT_BOUNDARIES` | Wrap output in boundary markers |
| `AGENT_BROWSER_MAX_OUTPUT` | Max characters for page output |
| `AGENT_BROWSER_ALLOWED_DOMAINS` | Comma-separated allowed domain patterns |
| `AGENT_BROWSER_ACTION_POLICY` | Path to action policy JSON file |
| `AGENT_BROWSER_CONFIRM_ACTIONS` | Action categories requiring confirmation |
| `AGENT_BROWSER_EXECUTABLE_PATH` | Custom browser executable path |
| `AGENT_BROWSER_EXTENSIONS` | Browser extensions to load |
| `AGENT_BROWSER_ARGS` | Browser launch args |
| `AGENT_BROWSER_USER_AGENT` | Custom User-Agent string |
| `AGENT_BROWSER_PROXY` | Proxy server URL |
| `AGENT_BROWSER_PROXY_BYPASS` | Hosts to bypass proxy |
| `AGENT_BROWSER_COLOR_SCHEME` | Color scheme (dark/light/no-preference) |
| `AGENT_BROWSER_DOWNLOAD_PATH` | Default download directory |
| `AGENT_BROWSER_ANNOTATE` | Default to annotated screenshots |
| `AGENT_BROWSER_AUTO_CONNECT` | Auto-discover running Chrome |
| `AGENT_BROWSER_CONFIG` | Custom config file path |
| `AGENT_BROWSER_STREAM_PORT` | WebSocket streaming port for live preview |
| `AGENT_BROWSER_PROVIDER` | Cloud provider (browserbase/browseruse/kernel/ios) |
| `AGENT_BROWSER_IOS_DEVICE` | iOS device name for simulator |

## Global CLI Options

| Option | Description |
|--------|-------------|
| `--session <name>` | Isolated session |
| `--session-name <name>` | Auto-save/restore state |
| `--profile <path>` | Persistent browser profile |
| `--state <file>` | Load storage state |
| `--headers <json>` | HTTP headers scoped to URL's origin |
| `--executable-path <path>` | Custom browser |
| `--extension <path>` | Load extension (repeatable) |
| `--args <args>` | Browser launch args |
| `--user-agent <ua>` | Custom User-Agent |
| `--proxy <url>` | Proxy server |
| `--ignore-https-errors` | Ignore HTTPS cert errors |
| `--allow-file-access` | Allow file:// URLs |
| `-p, --provider <name>` | Cloud browser provider |
| `--device <name>` | iOS device name |
| `--json` | JSON output |
| `--full, -f` | Full page screenshot |
| `--annotate` | Annotated screenshot |
| `--headed` | Show browser window |
| `--cdp <port/url>` | Connect via CDP |
| `--auto-connect` | Auto-discover Chrome |
| `--color-scheme <scheme>` | Color scheme |
| `--download-path <path>` | Download directory |
| `--config <path>` | Custom config file |
| `--debug` | Debug output |
