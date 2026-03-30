# Security and Configuration

All security features are opt-in. Default behavior imposes no restrictions.

**Related**: [commands.md](commands.md) for full command reference, [SKILL.md](../SKILL.md) for quick start.

## Security Features

### Content Boundaries (Recommended for AI Agents)

Wrap page output in delimiters so LLMs distinguish tool output from untrusted content:

```bash
export AGENT_BROWSER_CONTENT_BOUNDARIES=1
agent-browser snapshot
# --- AGENT_BROWSER_PAGE_CONTENT nonce=<hex> origin=https://example.com ---
# [accessibility tree]
# --- END_AGENT_BROWSER_PAGE_CONTENT nonce=<hex> ---
```

### Domain Allowlist

Restrict navigation to trusted domains. Wildcards like `*.example.com` also match the bare domain. Sub-resource requests, WebSocket, and EventSource connections to non-allowed domains are blocked. Include CDN domains your target pages depend on:

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

Auth vault operations (`auth login`, etc.) bypass action policy but domain allowlist still applies.

### Action Confirmation

Require explicit approval for sensitive categories:

```bash
export AGENT_BROWSER_CONFIRM_ACTIONS="eval,download"
export AGENT_BROWSER_CONFIRM_INTERACTIVE=1  # Interactive prompts (auto-denies if stdin not TTY)
```

### Output Length Limits

Prevent context flooding from large pages:

```bash
export AGENT_BROWSER_MAX_OUTPUT=50000
```

### Auth Vault Encryption

Credentials stored via `auth save` are always encrypted. A key is auto-generated at `~/.agent-browser/.encryption-key` if `AGENT_BROWSER_ENCRYPTION_KEY` is not set.

### Session State Encryption

Encrypt saved session data at rest with AES-256-GCM:

```bash
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)
agent-browser --session-name secure open https://app.example.com
```

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
  "ignoreHttpsErrors": true,
  "native": false,
  "colorScheme": "dark",
  "downloadPath": "./downloads"
}
```

All CLI options map to camelCase keys (e.g., `--executable-path` becomes `"executablePath"`). Boolean flags accept `true`/`false` values. Extensions from user and project configs are merged, not replaced.

Use `--config <path>` or `AGENT_BROWSER_CONFIG` to load a custom config file (exits with error if missing/invalid).

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
| `AGENT_BROWSER_CONFIRM_INTERACTIVE` | Enable interactive confirmation prompts |
| `AGENT_BROWSER_EXECUTABLE_PATH` | Custom browser executable path |
| `AGENT_BROWSER_EXTENSIONS` | Browser extensions to load |
| `AGENT_BROWSER_ARGS` | Browser launch args |
| `AGENT_BROWSER_USER_AGENT` | Custom User-Agent string |
| `AGENT_BROWSER_PROXY` | Proxy server URL |
| `AGENT_BROWSER_PROXY_BYPASS` | Hosts to bypass proxy |
| `AGENT_BROWSER_COLOR_SCHEME` | Color scheme (dark/light/no-preference) |
| `AGENT_BROWSER_DOWNLOAD_PATH` | Default download directory |
| `AGENT_BROWSER_ANNOTATE` | Default to annotated screenshots |
| `AGENT_BROWSER_HEADED` | Show browser window |
| `AGENT_BROWSER_AUTO_CONNECT` | Auto-discover running Chrome |
| `AGENT_BROWSER_NATIVE` | Use native Rust daemon |
| `AGENT_BROWSER_ENGINE` | Browser engine (chrome/lightpanda) |
| `AGENT_BROWSER_CONFIG` | Custom config file path |
| `AGENT_BROWSER_STREAM_PORT` | WebSocket streaming port for live preview |
| `AGENT_BROWSER_PROVIDER` | Cloud provider (browserbase/browseruse/kernel/ios) |
| `AGENT_BROWSER_IOS_DEVICE` | iOS device name for simulator |
| `AGENT_BROWSER_IOS_UDID` | iOS device UDID (alternative to name) |
| `KERNEL_API_KEY` | Kernel cloud browser API key |
| `KERNEL_HEADLESS` | Kernel headless mode (default: false) |
| `KERNEL_STEALTH` | Kernel stealth mode (default: true) |
| `KERNEL_TIMEOUT_SECONDS` | Kernel session timeout (default: 300) |
| `KERNEL_PROFILE_NAME` | Kernel persistent profile name |
| `BROWSERBASE_API_KEY` | Browserbase API key |
| `BROWSERBASE_PROJECT_ID` | Browserbase project ID |
| `BROWSER_USE_API_KEY` | Browser Use API key |

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
| `--proxy-bypass <hosts>` | Bypass proxy |
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
| `--native` | Experimental Rust daemon |
| `--engine <name>` | Browser engine (chrome/lightpanda) |
| `--debug` | Debug output |
