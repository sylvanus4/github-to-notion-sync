---
name: agent-browser
description: >-
  Headless browser automation via the agent-browser CLI (v0.16.3). Navigates pages,
  fills forms, clicks elements, takes screenshots, extracts data, diffs page states,
  records video, profiles performance, and manages sessions -- all from the terminal.
  Use when the user asks to "automate a browser task", "test a web page", "scrape data",
  "take a screenshot of a site", "fill out a form", "login to a website", "compare two pages",
  "visual diff", "record browser session", "profile page performance", "native mode browser",
  "stream browser", "iOS mobile testing", "auth vault", "cloud browser", or any task
  requiring programmatic browser interaction via CLI.
  Do NOT use for interactive MCP-based browser sessions (use cursor-ide-browser MCP instead),
  Playwright test suites (use webapp-testing skill), or general web fetching without browser
  rendering (use WebFetch).
metadata:
  author: thaki
  version: 2.0.0
  upstream: vercel-labs/agent-browser@0.16.3
---

# Agent Browser — CLI Browser Automation for AI Agents

Automate headless Chromium via the `agent-browser` CLI. Uses a snapshot-ref interaction pattern: navigate to a page, snapshot the accessibility tree to get element refs (`@e1`, `@e2`), then interact using those refs.

## Prerequisites

```bash
which agent-browser || npm install -g agent-browser
agent-browser install  # downloads Chromium (first time only)
```

## Core Workflow

Every browser automation follows this loop:

```
1. Navigate  →  agent-browser open <url>
2. Snapshot  →  agent-browser snapshot -i
3. Interact  →  agent-browser click @e1 / fill @e2 "text"
4. Re-snapshot after page changes
```

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output: @e1 input "Email", @e2 input "Password", @e3 button "Submit"

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # fresh refs after navigation
```

## Command Chaining

Chain commands with `&&` when you don't need intermediate output:

```bash
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser snapshot -i
agent-browser fill @e1 "user@example.com" && agent-browser fill @e2 "pass" && agent-browser click @e3
```

Run commands separately when you need to parse output first (e.g., snapshot to discover refs before interacting).

## Essential Commands

```bash
# Navigation
agent-browser open <url>              # Navigate (aliases: goto, navigate)
agent-browser close                   # Close browser

# Snapshot
agent-browser snapshot -i             # Interactive elements with refs (recommended)
agent-browser snapshot -i -C          # Include cursor-interactive elements (divs with onclick)
agent-browser snapshot -s "#selector" # Scope to CSS selector

# Interaction (use @refs from snapshot)
agent-browser click @e1               # Click element
agent-browser click @e1 --new-tab     # Click and open in new tab
agent-browser fill @e2 "text"         # Clear and type text
agent-browser type @e2 "text"         # Type without clearing
agent-browser select @e1 "option"     # Select dropdown
agent-browser check @e1               # Check checkbox
agent-browser press Enter             # Press key
agent-browser keyboard type "text"    # Type at current focus (no selector)
agent-browser scroll down 500         # Scroll page
agent-browser scroll down 500 --selector "div.content"  # Scroll container

# Get information
agent-browser get text @e1            # Element text
agent-browser get url                 # Current URL
agent-browser get title               # Page title

# Wait
agent-browser wait @e1                # Wait for element
agent-browser wait --load networkidle # Wait for network idle
agent-browser wait --url "**/page"    # Wait for URL pattern
agent-browser wait --fn "window.ready === true"  # Wait for JS condition
agent-browser wait 2000               # Wait milliseconds

# Downloads
agent-browser download @e1 ./file.pdf          # Click to trigger download
agent-browser wait --download ./output.zip     # Wait for download
agent-browser --download-path ./downloads open <url>

# Capture
agent-browser screenshot              # Screenshot to temp dir
agent-browser screenshot --full       # Full page screenshot
agent-browser screenshot --annotate   # Annotated with numbered labels
agent-browser pdf output.pdf          # Save as PDF

# Diff (compare page states)
agent-browser diff snapshot                          # Current vs last
agent-browser diff snapshot --baseline before.txt    # Current vs saved file
agent-browser diff screenshot --baseline before.png  # Visual pixel diff
agent-browser diff url <url1> <url2>                 # Compare two pages
agent-browser diff url <url1> <url2> --screenshot    # Also visual diff
```

For the full command reference, see [references/commands.md](references/commands.md).

## Ref Lifecycle

**CRITICAL**: Refs (`@e1`, `@e2`) are invalidated when the DOM changes. Always re-snapshot after:
- Clicking links or buttons that navigate
- Form submissions
- Dynamic content loading (dropdowns, modals, AJAX)

```bash
agent-browser click @e5              # triggers navigation
agent-browser wait --load networkidle
agent-browser snapshot -i            # MUST re-snapshot for fresh refs
agent-browser click @e1              # now use new refs
```

## Annotated Screenshots (Vision Mode)

Use `--annotate` for visual element identification. Each label `[N]` maps to `@eN` and caches refs:

```bash
agent-browser screenshot --annotate
# [1] @e1 button "Submit"
# [2] @e2 link "Home"
agent-browser click @e2  # click using ref from annotated screenshot
```

Use when: unlabeled icons, canvas/chart elements, visual layout verification, or spatial reasoning needed.

## Authentication

### Auth Vault (Recommended)

Store credentials encrypted locally so the LLM never sees passwords:

```bash
echo "$PASSWORD" | agent-browser auth save github \
  --url https://github.com/login --username "$USERNAME" --password-stdin

agent-browser auth login github
agent-browser auth list / auth show <name> / auth delete <name>
```

### State Persistence

```bash
# Login once and save
agent-browser state save auth.json
# Restore in future sessions
agent-browser state load auth.json

# Auto-save/restore with session name
agent-browser --session-name myapp open https://app.example.com
# Encrypt state at rest
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)
```

For detailed auth patterns (OAuth, 2FA, HTTP Basic), see [references/authentication.md](references/authentication.md).

## Sessions

Isolate parallel browser instances with named sessions:

```bash
agent-browser --session site1 open https://site-a.com
agent-browser --session site2 open https://site-b.com
agent-browser session list
agent-browser --session site1 close
```

For persistent profiles, session state management, and concurrent scraping, see [references/session-management.md](references/session-management.md).

## JavaScript Evaluation

Use `--stdin` for complex expressions to avoid shell quoting issues:

```bash
agent-browser eval 'document.title'

# Complex JS: use heredoc (recommended)
agent-browser eval --stdin <<'EVALEOF'
JSON.stringify(Array.from(document.querySelectorAll("a")).map(a => a.href))
EVALEOF

# Alternative: base64 encoding
agent-browser eval -b "$(echo -n 'expression' | base64)"
```

## Security

All security features are opt-in. See [references/security-and-config.md](references/security-and-config.md) for full details.

```bash
export AGENT_BROWSER_CONTENT_BOUNDARIES=1     # LLM-safe output markers
export AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com"  # Domain allowlist
export AGENT_BROWSER_ACTION_POLICY=./policy.json  # Gate destructive actions
export AGENT_BROWSER_MAX_OUTPUT=50000          # Prevent context flooding
```

## Diffing (Verify Changes)

```bash
agent-browser snapshot -i          # baseline
agent-browser click @e2            # action
agent-browser diff snapshot        # see what changed (+ additions, - removals)

# Visual regression
agent-browser screenshot baseline.png
agent-browser diff screenshot --baseline baseline.png

# Compare staging vs production
agent-browser diff url https://staging.example.com https://prod.example.com --screenshot
```

## Video Recording

```bash
agent-browser record start ./demo.webm
# ... actions ...
agent-browser record stop
agent-browser record restart ./take2.webm  # stop current + start new
```

For detailed recording workflows, see [references/video-recording.md](references/video-recording.md).

## Profiling

```bash
agent-browser profiler start
# ... actions to profile ...
agent-browser profiler stop ./trace.json
# View in chrome://tracing or https://ui.perfetto.dev/
```

For categories and analysis, see [references/profiling.md](references/profiling.md).

## Native Mode (Experimental)

Pure Rust daemon communicating with Chrome directly via CDP -- no Node.js/Playwright dependency:

```bash
agent-browser --native open example.com
# Or persist: export AGENT_BROWSER_NATIVE=1
```

Supports Chromium and Safari (via WebDriver). Use `agent-browser close` before switching between native and default mode.

## Browser Engine Selection

```bash
agent-browser --engine lightpanda open example.com  # 10x faster, 10x less memory
# Or: export AGENT_BROWSER_ENGINE=lightpanda
```

Engines: `chrome` (default), `lightpanda` (headless-only, no extensions/profiles).

## iOS Simulator (Mobile Safari)

Requires macOS + Xcode + Appium (`npm install -g appium && appium driver install xcuitest`).

```bash
agent-browser device list
agent-browser -p ios --device "iPhone 16 Pro" open https://example.com
agent-browser -p ios snapshot -i
agent-browser -p ios tap @e1
agent-browser -p ios swipe up
agent-browser -p ios screenshot mobile.png
agent-browser -p ios close
```

## Cloud Browser Providers

```bash
# Browserbase
export BROWSERBASE_API_KEY="key" && export BROWSERBASE_PROJECT_ID="id"  # pragma: allowlist secret
agent-browser -p browserbase open https://example.com

# Browser Use
export BROWSER_USE_API_KEY="key"  # pragma: allowlist secret
agent-browser -p browseruse open https://example.com

# Kernel (stealth mode, persistent profiles)
export KERNEL_API_KEY="key"  # pragma: allowlist secret
agent-browser -p kernel open https://example.com
```

## Configuration

Create `agent-browser.json` in project root for persistent settings:

```json
{"headed": true, "proxy": "http://localhost:8080", "profile": "./browser-data"}
```

Priority: `~/.agent-browser/config.json` < `./agent-browser.json` < env vars < CLI flags.

## Timeouts

Default timeout is 25 seconds. Override with `AGENT_BROWSER_DEFAULT_TIMEOUT=45000`. Prefer explicit waits over increasing the global timeout.

## Examples

### Example 1: Screenshot and Data Extraction

```bash
agent-browser open https://example.com && agent-browser wait --load networkidle
agent-browser screenshot --full --annotate page.png
agent-browser eval --stdin <<'EOF'
JSON.stringify(Array.from(document.querySelectorAll("h2")).map(h => h.textContent))
EOF
agent-browser close
```

### Example 2: Form Filling with Auth Vault

```bash
echo "$PASS" | agent-browser auth save myapp --url https://app.com/login --username user --password-stdin
agent-browser auth login myapp
agent-browser wait --url "**/dashboard"
agent-browser screenshot dashboard.png
agent-browser close
```

### Example 3: Visual Diff Between Environments

```bash
agent-browser diff url https://staging.app.com https://prod.app.com --screenshot --selector "#main"
agent-browser close
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `command not found` | CLI not installed | `npm install -g agent-browser && agent-browser install` |
| `EAGAIN` / timeout | Page too slow (25s default) | Add `wait --load networkidle` after `open` |
| `Element not found @eN` | Stale ref after DOM change | Re-run `snapshot -i` for fresh refs |
| Daemon connection error | Stale daemon | `agent-browser close` then retry |
| Screenshot blank | Page not loaded | `wait --load networkidle` before screenshot |

## Deep-Dive References

| Reference | When to Read |
|-----------|-------------|
| [references/commands.md](references/commands.md) | Full command list (find, mouse, network, cookies, frames, debug) |
| [references/authentication.md](references/authentication.md) | OAuth, 2FA, cookie auth, token refresh |
| [references/session-management.md](references/session-management.md) | Parallel sessions, state persistence, concurrent scraping |
| [references/snapshot-refs.md](references/snapshot-refs.md) | Ref lifecycle, invalidation rules, troubleshooting |
| [references/video-recording.md](references/video-recording.md) | Recording workflows for debugging and documentation |
| [references/profiling.md](references/profiling.md) | Chrome DevTools profiling for performance analysis |
| [references/proxy-support.md](references/proxy-support.md) | Proxy configuration, geo-testing, rotating proxies |
| [references/security-and-config.md](references/security-and-config.md) | Domain allowlists, action policies, config files, env vars |

## Ready-to-Use Templates

| Template | Description |
|----------|-------------|
| [templates/form-automation.sh](templates/form-automation.sh) | Form filling with validation |
| [templates/authenticated-session.sh](templates/authenticated-session.sh) | Login once, reuse state |
| [templates/capture-workflow.sh](templates/capture-workflow.sh) | Content extraction with screenshots |
