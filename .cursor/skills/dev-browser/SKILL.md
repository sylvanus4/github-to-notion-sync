---
name: dev-browser
description: >-
  Sandboxed browser automation via heredoc JavaScript scripts running in QuickJS
  WASM with full Playwright Page API access and persistent named pages. Use when
  the user asks to "run browser script", "sandboxed browser", "dev-browser",
  "persistent page", "connect to chrome", "browser script", "automate with
  dev-browser", "multi-step browser workflow", "page.snapshotForAI", "headless
  script", or any task requiring scripted multi-step browser automation with
  sandbox isolation. Do NOT use for step-by-step interactive browser exploration
  with snapshot refs (use agent-browser). Do NOT use for interactive MCP-based
  browser sessions (use cursor-ide-browser MCP). Do NOT use for simple URL
  content fetching without browser rendering (use WebFetch or defuddle). Do NOT
  use for Playwright E2E test suites (use e2e-testing). Korean triggers:
  "브라우저 스크립트", "샌드박스 브라우저", "dev-browser", "크롬 연결",
  "영구 페이지".
metadata:
  author: "thaki"
  version: "1.0.0"
  upstream: "SawyerHood/dev-browser"
  category: "execution"
---

# dev-browser — Sandboxed Browser Automation via JS Scripts

Automate browsers by writing JavaScript scripts that run in a QuickJS WASM sandbox with full Playwright `Page` API access. Scripts are piped to the `dev-browser` CLI via heredoc or stdin.

## Prerequisites

```bash
which dev-browser || npm install -g dev-browser
dev-browser install  # downloads Chromium (first time only)
```

## Core Concepts

- **Sandboxed execution**: Scripts run in QuickJS WASM — no host filesystem or network access from script code
- **Persistent named pages**: Pages survive across script invocations; reuse them by name
- **Full Playwright Page API**: `page.goto()`, `page.click()`, `page.fill()`, `page.waitForSelector()`, etc.
- **AI-friendly snapshots**: `page.snapshotForAI()` returns an accessibility-tree snapshot optimized for LLM consumption
- **Two modes**: `--headless` (launch fresh Chromium) and `--connect` (attach to running Chrome)

## Core Workflow

Every dev-browser automation follows this pattern:

```
1. Write a JS script using the sandbox API
2. Pipe it to dev-browser via heredoc
3. Read console.log output and saved files
```

```bash
dev-browser --headless <<'SCRIPT'
const page = await browser.getPage("main");
await page.goto("https://example.com");
const title = await page.title();
console.log("Title:", title);
const snapshot = await page.snapshotForAI();
console.log(snapshot);
SCRIPT
```

## Modes

### Headless Mode (default for automation)

Launches a fresh Chromium instance. Best for automated pipelines, CI, and scripted tasks.

```bash
dev-browser --headless <<'SCRIPT'
const page = await browser.getPage("main");
await page.goto("https://example.com");
const buf = await page.screenshot();
await saveScreenshot(buf, "example.png");
SCRIPT
```

### Connect Mode (attach to running Chrome)

Attaches to an already-running Chrome with remote debugging enabled. Best for debugging, inspecting logged-in sessions, and working with pages that require manual auth.

```bash
# First: launch Chrome with remote debugging
# macOS:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# Then: connect and automate
dev-browser --connect <<'SCRIPT'
const page = await browser.getPage("main");
const url = await page.url();
console.log("Current page:", url);
SCRIPT
```

For detailed connection patterns, see [references/connect-mode.md](references/connect-mode.md).

## Script API Quick Reference

### Browser Globals

| API | Description |
|-----|-------------|
| `browser.getPage(name)` | Get or create a persistent named page |
| `browser.newPage(name?)` | Create a new page (optionally named) |
| `browser.listPages()` | List open named pages (may return `{}` in headless mode — see note below) |
| `browser.closePage(name)` | Close a named page |

**Note**: `browser.listPages()` may return an empty object in `--headless` mode. Named page persistence via `getPage(name)` works reliably — prefer `getPage` to retrieve pages by name rather than listing.

### Page Methods (Playwright API)

| Method | Description |
|--------|-------------|
| `page.goto(url)` | Navigate to URL |
| `page.click(selector)` | Click an element |
| `page.fill(selector, text)` | Fill an input field |
| `page.type(selector, text)` | Type text character by character |
| `page.waitForSelector(sel)` | Wait for element to appear |
| `page.waitForLoadState(state)` | Wait for `load`, `domcontentloaded`, or `networkidle` |
| `page.title()` | Get page title |
| `page.url()` | Get current URL |
| `page.content()` | Get full page HTML |
| `page.evaluate(fn)` | Run JS in the browser context |
| `page.snapshotForAI()` | Get AI-friendly accessibility tree snapshot |
| `page.screenshot(opts)` | Take screenshot (returns buffer) |

### File I/O (Sandbox)

| Function | Description |
|----------|-------------|
| `saveScreenshot(buf, path)` | Save a screenshot buffer to disk (use with `page.screenshot()`) |
| `writeFile(path, content)` | Write text content to a file |
| `readFile(path)` | Read text content from a file |
| `console.log(...)` | Print output (captured by the agent) |

For the full API reference, see [references/script-api.md](references/script-api.md).

## Persistent Pages

Pages are identified by name and persist across script invocations within the same `dev-browser` session:

```bash
# Script 1: Navigate and name the page
dev-browser --headless <<'SCRIPT'
const page = await browser.getPage("dashboard");
await page.goto("https://app.example.com/login");
await page.fill("#email", "user@example.com");
await page.fill("#password", "pass123");
await page.click("button[type=submit]");
await page.waitForLoadState("networkidle");
console.log("Logged in:", await page.url());
SCRIPT

# Script 2: Reuse the same page (still logged in)
dev-browser --headless <<'SCRIPT'
const page = await browser.getPage("dashboard");
await page.goto("https://app.example.com/settings");
const snapshot = await page.snapshotForAI();
console.log(snapshot);
SCRIPT
```

## Examples

### Example 1: Screenshot and Data Extraction

```bash
dev-browser --headless <<'SCRIPT'
const page = await browser.getPage("main");
await page.goto("https://news.ycombinator.com");
await page.waitForLoadState("networkidle");
const buf = await page.screenshot();
await saveScreenshot(buf, "hackernews.png");

const titles = await page.evaluate(() =>
  Array.from(document.querySelectorAll(".titleline > a")).map(a => a.textContent)
);
console.log(JSON.stringify(titles, null, 2));
SCRIPT
```

### Example 2: Form Automation

```bash
dev-browser --headless <<'SCRIPT'
const page = await browser.getPage("form");
await page.goto("https://example.com/contact");
await page.fill("#name", "Jane Doe");
await page.fill("#email", "jane@example.com");
await page.fill("#message", "Hello from dev-browser!");
await page.click("button[type=submit]");
await page.waitForLoadState("networkidle");
console.log("Form submitted. URL:", await page.url());
SCRIPT
```

### Example 3: Multi-Page Workflow

```bash
dev-browser --headless <<'SCRIPT'
const search = await browser.getPage("search");
const detail = await browser.newPage("detail");

await search.goto("https://example.com/products");
const firstLink = await search.evaluate(() =>
  document.querySelector(".product-link")?.href
);

if (firstLink) {
  await detail.goto(firstLink);
  const snapshot = await detail.snapshotForAI();
  console.log("Product detail snapshot:");
  console.log(snapshot);
}

const pages = await browser.listPages();
console.log("Open pages:", pages);
SCRIPT
```

### Example 4: AI-Friendly Snapshot for Agent Loops

```bash
dev-browser --headless <<'SCRIPT'
const page = await browser.getPage("agent");
await page.goto("https://example.com/dashboard");
await page.waitForLoadState("networkidle");
const snapshot = await page.snapshotForAI();
console.log(snapshot);
SCRIPT
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `command not found: dev-browser` | CLI not installed | `npm install -g dev-browser && dev-browser install` |
| `No browser found` | Chromium not downloaded | `dev-browser install` |
| `Could not connect` (connect mode) | Chrome not running with `--remote-debugging-port` | Launch Chrome with `--remote-debugging-port=9222` |
| `page.goto: net::ERR_NAME_NOT_RESOLVED` | Invalid URL or no network | Check URL spelling and network connectivity |
| `Timeout exceeded` | Element not found or page too slow | Add `waitForLoadState("networkidle")` or increase timeout |
| `page.click: Element not found` | Selector doesn't match | Use `page.snapshotForAI()` to inspect current page state |
| Script hangs | Unresolved promise or infinite loop | Ensure all `await` calls resolve; add timeouts |

## When to Use: Decision Matrix

| Need | Tool | Why |
|------|------|-----|
| Multi-step scripted browser workflow | **dev-browser** | Full JS scripts, Playwright API, persistent pages |
| Step-by-step interactive exploration | agent-browser | Snapshot-ref pattern, one command at a time |
| Interactive browser in Cursor IDE | cursor-ide-browser MCP | Built-in browser panel with refs |
| Extract clean text from a URL | defuddle / WebFetch | No browser rendering needed |
| Playwright E2E test suite | e2e-testing | Test framework with assertions and reporters |
| Connect to existing Chrome session | **dev-browser** `--connect` | Attach to running Chrome with debugging port |
| Sandboxed script execution | **dev-browser** | QuickJS WASM — no host access from scripts |

## References

| Reference | When to Read |
|-----------|-------------|
| [references/script-api.md](references/script-api.md) | Full sandbox API — browser globals, page methods, file I/O |
| [references/connect-mode.md](references/connect-mode.md) | Chrome remote debugging connection patterns |
