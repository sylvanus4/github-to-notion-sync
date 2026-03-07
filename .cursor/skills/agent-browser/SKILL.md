---
name: agent-browser
description: >-
  Headless browser automation via the agent-browser CLI. Navigates pages,
  fills forms, clicks elements, takes screenshots, extracts data, diffs
  page states, and manages sessions -- all from the terminal. Use when the
  user asks to "automate a browser task", "test a web page", "scrape data",
  "take a screenshot of a site", "fill out a form", "login to a website",
  "compare two pages", or any task requiring programmatic browser interaction
  via CLI. Do NOT use for interactive MCP-based browser sessions (use
  cursor-ide-browser MCP instead), Playwright test suites (use webapp-testing
  skill), or general web fetching without browser rendering (use WebFetch).
metadata:
  author: thaki
  version: 1.0.0
---

# Agent Browser — CLI Browser Automation for AI Agents

Automate headless Chromium via the `agent-browser` CLI. Uses a snapshot-ref interaction pattern: navigate to a page, snapshot the accessibility tree to get element refs (`@e1`, `@e2`), then interact using those refs.

## Prerequisites

**CRITICAL**: The CLI must be installed before use. Check and install if needed:

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

## Essential Commands

| Category | Command | Purpose |
|----------|---------|---------|
| Navigate | `open <url>` | Go to URL |
| Navigate | `back` / `forward` / `reload` | History navigation |
| Snapshot | `snapshot -i` | Interactive elements with refs |
| Snapshot | `snapshot -i -C` | Include cursor-interactive elements |
| Snapshot | `snapshot -s "#sel"` | Scope to CSS selector |
| Click | `click @e1` | Click element |
| Input | `fill @e2 "text"` | Clear and type |
| Input | `type @e2 "text"` | Append text |
| Input | `select @e1 "option"` | Select dropdown |
| Input | `check @e1` / `uncheck @e1` | Checkbox |
| Key | `press Enter` | Press key |
| Scroll | `scroll down 500` | Scroll page |
| Get | `get text @e1` | Element text |
| Get | `get url` / `get title` | Page info |
| Wait | `wait @e1` | Wait for element |
| Wait | `wait --load networkidle` | Wait for network idle |
| Wait | `wait --url "**/page"` | Wait for URL pattern |
| Wait | `wait 2000` | Wait milliseconds |
| Capture | `screenshot` | Screenshot to temp dir |
| Capture | `screenshot --full` | Full page screenshot |
| Capture | `screenshot --annotate` | Annotated with labels |
| Capture | `pdf output.pdf` | Save as PDF |
| Diff | `diff snapshot` | Compare current vs last |
| Diff | `diff screenshot --baseline b.png` | Visual pixel diff |
| Session | `close` | Close browser |

All commands are prefixed with `agent-browser`. For the full command reference, see [references/commands.md](references/commands.md).

## Command Chaining

Chain commands with `&&` when you don't need intermediate output:

```bash
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser snapshot -i
```

Run commands separately when you need to parse output first (e.g., snapshot to discover refs before interacting).

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

## Annotated Screenshots

Use `--annotate` for visual element identification. Each label `[N]` maps to `@eN`:

```bash
agent-browser screenshot --annotate
# [1] @e1 button "Submit"
# [2] @e2 link "Home"
# [3] @e3 textbox "Email"
agent-browser click @e2  # click using ref from annotated screenshot
```

Use when: unlabeled icons, canvas/chart elements, or visual layout verification needed.

## Sessions

Isolate parallel browser instances with named sessions:

```bash
agent-browser --session site1 open https://site-a.com
agent-browser --session site2 open https://site-b.com
agent-browser session list
```

Always close sessions when done: `agent-browser close`

## Diffing (Verify Changes)

Compare page states after actions:

```bash
agent-browser snapshot -i          # baseline
agent-browser click @e2            # action
agent-browser diff snapshot        # see what changed (+ additions, - removals)
```

Visual regression:

```bash
agent-browser screenshot baseline.png
# ... changes ...
agent-browser diff screenshot --baseline baseline.png
```

## JavaScript Evaluation

Use `--stdin` for complex expressions to avoid shell quoting issues:

```bash
# Simple
agent-browser eval 'document.title'

# Complex (recommended: heredoc)
agent-browser eval --stdin <<'EVALEOF'
JSON.stringify(Array.from(document.querySelectorAll("a")).map(a => a.href))
EVALEOF
```

## Examples

### Example 1: Basic Page Interaction

User says: "Open example.com and click the Learn More link"

Actions:
1. `agent-browser open https://example.com`
2. `agent-browser snapshot -i` -- find the link ref
3. `agent-browser click @e4` -- click "Learn more"
4. `agent-browser snapshot -i` -- verify navigation

Result: Navigated to the linked page, confirmed via snapshot

### Example 2: Form Submission with Authentication

User says: "Login to my-app.com and take a screenshot of the dashboard"

Actions:
1. `agent-browser open https://my-app.com/login`
2. `agent-browser snapshot -i` -- find email, password, submit refs
3. `agent-browser fill @e1 "$EMAIL" && agent-browser fill @e2 "$PASSWORD" && agent-browser click @e3`
4. `agent-browser wait --url "**/dashboard"`
5. `agent-browser screenshot dashboard.png`
6. `agent-browser state save auth.json` -- save for reuse

Result: Screenshot saved, auth state persisted for future sessions

### Example 3: Data Extraction

User says: "Extract all product names from the catalog page"

Actions:
1. `agent-browser open https://shop.example.com/catalog`
2. `agent-browser wait --load networkidle`
3. `agent-browser eval --stdin <<'EOF'`
   `JSON.stringify(Array.from(document.querySelectorAll(".product-name")).map(el => el.textContent))`
   `EOF`
4. Parse JSON output

Result: JSON array of product names returned

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `command not found: agent-browser` | CLI not installed | `npm install -g agent-browser && agent-browser install` |
| `EAGAIN` / timeout | Page too slow, default 25s exceeded | Add `agent-browser wait --load networkidle` after `open` |
| `Element not found` with `@eN` | Stale ref after DOM change | Re-run `agent-browser snapshot -i` for fresh refs |
| Daemon connection error | Stale daemon process | `agent-browser close` then retry |
| `No browser installed` | Chromium not downloaded | `agent-browser install` |
| Screenshot blank/empty | Page not loaded yet | `agent-browser wait --load networkidle` before screenshot |
| JS eval returns `undefined` | Expression has no return value | Ensure expression returns a value; use `JSON.stringify()` for objects |

## Timeouts

Default Playwright timeout is 25 seconds. Override with:

```bash
export AGENT_BROWSER_DEFAULT_TIMEOUT=45000  # milliseconds
```

For slow pages, prefer explicit waits over increasing the global timeout.

## Deep-Dive References

| Reference | When to Read |
|-----------|--------------|
| [references/commands.md](references/commands.md) | Need the full command list (find, mouse, network, cookies, frames, debug) |
| [references/common-patterns.md](references/common-patterns.md) | Auth vault, session persistence, iOS simulator, CDP, parallel sessions |
| [references/security-and-config.md](references/security-and-config.md) | Domain allowlists, action policies, config files, environment variables |
