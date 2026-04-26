---
name: obscura
description: >-
  Lightweight Rust-based headless browser (30MB memory, 70MB binary) with built-in
  anti-detection stealth mode, V8 JS engine, and Chrome DevTools Protocol (CDP)
  compatibility for AI agent automation and web scraping. Three CLI modes: fetch
  (single page), serve (CDP server for Puppeteer/Playwright), scrape (parallel
  bulk scraping). Use when the user asks to "use obscura", "lightweight headless
  browser", "stealth scraping", "anti-detection browser", "lightweight CDP server",
  "parallel scraping CLI", "drop-in Chrome replacement", "low-memory browser",
  "Obscura fetch", "Obscura serve", "Obscura scrape", "경량 브라우저", "스텔스
  스크래핑", "안티디텍션", "Obscura", "경량 CDP", "경량 헤드리스", "병렬 스크래핑",
  "DOM to markdown", "LP.getMarkdown", "request interception",
  or needs a single-binary headless browser with built-in stealth for scraping or
  as a lightweight CDP backend. Do NOT use for interactive browser automation with
  snapshot-ref patterns (use agent-browser). Do NOT use for sandboxed JS script
  execution via QuickJS WASM (use dev-browser). Do NOT use for Cloudflare Turnstile
  bypass in Python (use scrapling). Do NOT use for simple URL-to-markdown extraction
  without JS rendering (use defuddle or WebFetch). Do NOT use for terminal visual
  browsing (use carbonyl-browser). Do NOT use for Playwright E2E test suites (use
  e2e-testing). Do NOT use for MCP-based interactive browser sessions (use
  cursor-ide-browser MCP).
metadata:
  author: ThakiCloud
  version: "2.0"
  upstream: https://github.com/h4ckf0r0day/obscura
  upstream_version: "0.1.1"
  category: standalone/browser
---

# Obscura — Lightweight Headless Browser for AI Agents

Rust-built headless browser optimized for AI agent automation and web scraping.
30MB memory footprint, built-in anti-detection, V8 JS engine, CDP-compatible.

## Prerequisites

### Installation (macOS Apple Silicon)

```bash
curl -LO https://github.com/h4ckf0r0day/obscura/releases/latest/download/obscura-aarch64-macos.tar.gz
tar xzf obscura-aarch64-macos.tar.gz
chmod +x obscura
sudo mv obscura /usr/local/bin/

obscura --version
```

For other platforms, check the [releases page](https://github.com/h4ckf0r0day/obscura/releases)
for the appropriate binary (`x86_64-unknown-linux-gnu`, `x86_64-pc-windows-msvc`, etc.).

### Health Check

```bash
# Quick fetch test
obscura fetch https://httpbin.org/headers --stealth

# CDP server test
obscura serve --port 9222 &
curl -s http://127.0.0.1:9222/json/version | head -5
kill %1
```

## Core Workflow

Obscura provides three CLI modes. Choose based on task:

```
Single page needed? ──yes──▶ obscura fetch <url>
                     │
                     no
                     │
CDP backend needed? ──yes──▶ obscura serve --port 9222
(Puppeteer/Playwright)       └─▶ connect via ws://127.0.0.1:9222
                     │
                     no
                     │
Bulk scraping? ─────yes──▶ obscura scrape url1 url2 ... --concurrency 10
```

### Mode 1: fetch — Single Page Extraction

Fetch a single URL, optionally execute JavaScript, and return HTML, text, or links.

```bash
# Basic HTML fetch (default --dump html)
obscura fetch https://example.com

# Extract text only (strips HTML tags)
obscura fetch https://example.com --dump text

# Extract links only
obscura fetch https://example.com --dump links

# With stealth mode
obscura fetch https://example.com --stealth

# Execute JS and capture result
obscura fetch https://example.com --stealth --eval "document.title"

# Wait for a CSS selector to appear (timeout in seconds)
obscura fetch https://spa-app.com --stealth --selector ".content-loaded" --wait 10

# Control navigation wait strategy
obscura fetch https://spa-app.com --wait-until networkidle0

# Quiet mode — suppress status output, print only result
obscura fetch https://example.com --quiet --eval "document.title"

# Save output to file (shell redirect — no -o flag)
obscura fetch https://example.com --dump text > output.txt
```

### Mode 2: serve — CDP Server

Start a Chrome DevTools Protocol server that Puppeteer or Playwright can connect to.
Uses ~30MB memory vs Chrome's ~200MB+.

```bash
# Start CDP server (default port 9222)
obscura serve --port 9222 --stealth

# With proxy and custom user-agent
obscura serve --port 9222 --stealth --proxy socks5://127.0.0.1:1080 --user-agent "MyBot/1.0"

# Multi-worker mode with load balancer
obscura serve --port 9222 --stealth --workers 4

# Background mode for pipeline use
obscura serve --port 9222 --stealth &
OBSCURA_PID=$!

# ... run Puppeteer/Playwright scripts ...

kill $OBSCURA_PID
```

### Mode 3: scrape — Parallel Bulk Scraping

Scrape multiple URLs concurrently. URLs are positional arguments.

```bash
# Scrape multiple URLs with 10 concurrent workers
obscura scrape https://example.com/1 https://example.com/2 --concurrency 10

# With JS evaluation and JSON output
obscura scrape https://example.com/a https://example.com/b \
  --eval "document.title" --concurrency 5 --format json

# TSV output format
obscura scrape https://example.com/1 https://example.com/2 --format tsv

# Custom timeout (seconds, default 60)
obscura scrape https://example.com/1 --timeout 120

# Pipe URLs from another command via xargs
cat urls.txt | xargs obscura scrape --concurrency 8
```

## Stealth Mode

The `--stealth` flag activates built-in anti-detection:

| Feature | Description |
|---------|-------------|
| Fingerprint randomization | Randomizes canvas, WebGL, audio fingerprints per session |
| Tracker blocking | Blocks 3,520 known trackers (EasyList + EasyPrivacy) |
| WebDriver flag | Sets `navigator.webdriver = undefined` |
| User-Agent rotation | Rotates realistic UA strings |
| Plugin/language spoofing | Mimics real browser plugin and language configurations |

**Always use `--stealth` for scraping tasks** unless targeting a trusted internal site
where stealth overhead is unnecessary.

## CLI Reference

### Global Flags

| Flag | Default | Description |
|------|---------|-------------|
| `-v, --verbose` | off | Enable verbose logging |
| `--port` | `9222` | CDP server listen port (top-level) |
| `--proxy` | — | SOCKS5 or HTTP proxy URL |
| `--obey-robots` | off | Respect robots.txt rules |
| `--user-agent` | — | Custom User-Agent string |

### `obscura fetch <URL>`

| Flag | Default | Description |
|------|---------|-------------|
| `--dump` | `html` | Output format: `html`, `text`, or `links` |
| `--selector` | — | CSS selector to wait for before capture |
| `--wait` | `5` | Wait seconds (used with `--selector`) |
| `--wait-until` | `load` | Navigation event: `load`, `domcontentloaded`, `networkidle0` |
| `--user-agent` | — | Custom User-Agent string |
| `--stealth` | off | Enable anti-detection |
| `-e, --eval` | — | JavaScript expression to evaluate and return |
| `-q, --quiet` | off | Suppress status output |

### `obscura serve`

| Flag | Default | Description |
|------|---------|-------------|
| `-p, --port` | `9222` | CDP server listen port |
| `--proxy` | — | SOCKS5 or HTTP proxy URL |
| `--user-agent` | — | Custom User-Agent string |
| `--stealth` | off | Enable anti-detection |
| `--workers` | `1` | Number of concurrent worker browsers |

### `obscura scrape <URLs...>`

| Flag | Default | Description |
|------|---------|-------------|
| `-e, --eval` | — | JavaScript expression to evaluate per page |
| `--concurrency` | `10` | Number of concurrent scraping workers |
| `--format` | `json` | Output format: `json` or `tsv` |
| `--timeout` | `60` | Per-page timeout in seconds (min: 1) |

## CDP API Reference

When running `obscura serve`, a full CDP WebSocket server is available. Obscura implements
10 CDP domains with 68+ methods. Connect via `ws://127.0.0.1:9222`.

### Supported Domains and Methods

#### `Target` — Browser target management

| Method | Description |
|--------|-------------|
| `Target.setDiscoverTargets` | Enable/disable target discovery events |
| `Target.getTargets` | List all available targets |
| `Target.createTarget` | Create a new page/tab |
| `Target.attachToTarget` | Attach a session to a target |
| `Target.closeTarget` | Close a target |
| `Target.setAutoAttach` | Auto-attach to new targets |
| `Target.getBrowserContexts` | List browser contexts |
| `Target.createBrowserContext` | Create an incognito context |
| `Target.disposeBrowserContext` | Destroy a browser context |
| `Target.getTargetInfo` | Get metadata about a target |

#### `Browser` — Browser-level controls

| Method | Description |
|--------|-------------|
| `Browser.getVersion` | Get browser version info |
| `Browser.close` | Close the browser |
| `Browser.getWindowForTarget` | Get window ID for a target |
| `Browser.setDownloadBehavior` | Configure download handling |
| `Browser.getWindowBounds` | Get window size/position |
| `Browser.setWindowBounds` | Set window size/position |

#### `Page` — Page navigation and lifecycle

| Method | Description |
|--------|-------------|
| `Page.enable` | Enable page domain events |
| `Page.navigate` | Navigate to URL |
| `Page.getFrameTree` | Get frame hierarchy |
| `Page.createIsolatedWorld` | Create isolated JS context |
| `Page.setLifecycleEventsEnabled` | Enable lifecycle event reporting |
| `Page.addScriptToEvaluateOnNewDocument` | Inject JS on every new document |
| `Page.removeScriptToEvaluateOnNewDocument` | Remove injected script |
| `Page.setInterceptFileChooserDialog` | Intercept file upload dialogs |
| `Page.getNavigationHistory` | Get navigation history entries |

#### `DOM` — Document Object Model

| Method | Description |
|--------|-------------|
| `DOM.enable` | Enable DOM domain events |
| `DOM.getDocument` | Get the root DOM node |
| `DOM.querySelector` | Find first matching element |
| `DOM.querySelectorAll` | Find all matching elements |
| `DOM.getOuterHTML` | Get element outer HTML |
| `DOM.describeNode` | Get detailed node description |
| `DOM.resolveNode` | Resolve DOM node to JS object |
| `DOM.setAttributeValue` | Set element attribute |
| `DOM.removeNode` | Remove a DOM node |
| `DOM.getBoxModel` | Get element box model (position/size) |

#### `Runtime` — JavaScript execution

| Method | Description |
|--------|-------------|
| `Runtime.enable` | Enable runtime domain events |
| `Runtime.evaluate` | Execute JS expression |
| `Runtime.callFunctionOn` | Call function on a remote object |
| `Runtime.getProperties` | Get object properties |
| `Runtime.releaseObject` | Release a remote object reference |
| `Runtime.releaseObjectGroup` | Release a group of remote objects |
| `Runtime.addBinding` | Expose a JS binding to pages |
| `Runtime.runIfWaitingForDebugger` | Resume execution if paused |
| `Runtime.getExceptionDetails` | Get exception details |
| `Runtime.discardConsoleEntries` | Clear console entries |

#### `Network` — Network monitoring and control

| Method | Description |
|--------|-------------|
| `Network.enable` | Enable network events |
| `Network.setExtraHTTPHeaders` | Add custom headers to all requests |
| `Network.setUserAgentOverride` | Override User-Agent |
| `Network.getCookies` | Get cookies for current page |
| `Network.setCookies` | Set cookies |
| `Network.clearBrowserCookies` | Clear all cookies |
| `Network.setCacheDisabled` | Disable/enable cache |
| `Network.setRequestInterception` | Legacy request interception (prefer `Fetch` domain) |

#### `Fetch` — Request interception (recommended)

| Method | Description |
|--------|-------------|
| `Fetch.enable` | Enable request interception with URL pattern filters |
| `Fetch.continueRequest` | Continue an intercepted request (optionally modify URL/headers) |
| `Fetch.fulfillRequest` | Fulfill request with custom response body |
| `Fetch.failRequest` | Fail request with a network error reason |
| `Fetch.getResponseBody` | Get the body of an intercepted response |

#### `Input` — Keyboard, mouse, and touch events

| Method | Description |
|--------|-------------|
| `Input.dispatchMouseEvent` | Simulate mouse click/move/scroll |
| `Input.dispatchKeyEvent` | Simulate key press/release |
| `Input.dispatchTouchEvent` | Simulate touch events |
| `Input.setIgnoreInputEvents` | Ignore input events on the page |

#### `Storage` — Browser storage

| Method | Description |
|--------|-------------|
| `Storage.getCookies` | Get cookies (via Storage domain) |
| `Storage.setCookies` | Set cookies (via Storage domain) |
| `Storage.deleteCookies` | Delete specific cookies |

#### `LP` — Obscura custom domain

| Method | Description |
|--------|-------------|
| `LP.getMarkdown` | Convert current page DOM to clean Markdown |

## Request Interception

Use the `Fetch` domain to intercept, modify, or block HTTP requests in flight.

### Block image loading (speed up scraping)

```javascript
// 1. Enable interception for image requests
await cdp.send("Fetch.enable", {
  patterns: [{ urlPattern: "*", requestStage: "Request" }]
});

// 2. Handle intercepted requests
cdp.on("Fetch.requestPaused", async (event) => {
  const url = event.request.url;
  if (/\.(png|jpg|gif|svg|webp)$/i.test(url)) {
    await cdp.send("Fetch.failRequest", {
      requestId: event.requestId,
      errorReason: "BlockedByClient"
    });
  } else {
    await cdp.send("Fetch.continueRequest", {
      requestId: event.requestId
    });
  }
});
```

### Inject custom headers

```javascript
await cdp.send("Fetch.enable", {
  patterns: [{ urlPattern: "*", requestStage: "Request" }]
});

cdp.on("Fetch.requestPaused", async (event) => {
  const headers = event.request.headers;
  headers["X-Custom-Auth"] = "Bearer token123";
  await cdp.send("Fetch.continueRequest", {
    requestId: event.requestId,
    headers: Object.entries(headers).map(([n, v]) => ({ name: n, value: v }))
  });
});
```

### Return mock response

```javascript
await cdp.send("Fetch.enable", {
  patterns: [{ urlPattern: "*/api/data*", requestStage: "Request" }]
});

cdp.on("Fetch.requestPaused", async (event) => {
  await cdp.send("Fetch.fulfillRequest", {
    requestId: event.requestId,
    responseCode: 200,
    responseHeaders: [{ name: "Content-Type", value: "application/json" }],
    body: btoa(JSON.stringify({ mock: true, items: [] }))
  });
});
```

## DOM-to-Markdown Extraction (LP.getMarkdown)

Obscura provides a custom CDP method `LP.getMarkdown` that converts the current page's
DOM into clean Markdown — ideal for feeding web content directly to LLMs.

```javascript
// Navigate to a page first
await cdp.send("Page.navigate", { url: "https://example.com/article" });

// Wait for content to load
await new Promise(r => setTimeout(r, 3000));

// Extract Markdown
const result = await cdp.send("LP.getMarkdown");
console.log(result.markdown);
```

### LP.getMarkdown vs defuddle

| Feature | LP.getMarkdown | defuddle |
|---------|---------------|----------|
| JS rendering | Yes (V8 engine) | No (server-side extraction) |
| SPA support | Full | Limited |
| Binary dependency | Requires Obscura running | API call only |
| Memory usage | ~30MB (Obscura process) | Zero (remote service) |
| Anti-detection | Built-in stealth | None |
| Output format | Markdown | Markdown with YAML frontmatter |

**Use LP.getMarkdown** when the page requires JavaScript rendering (SPAs, dynamic content)
or when you already have an Obscura CDP session open.

**Use defuddle** when JS rendering is unnecessary and you want zero local overhead.

## Puppeteer / Playwright Integration

Obscura's CDP server is a drop-in replacement for headless Chrome.

### Puppeteer (Node.js)

```javascript
const puppeteer = require("puppeteer-core");

// Start: obscura serve --port 9222 --stealth
const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://127.0.0.1:9222",
});

const page = await browser.newPage();
await page.goto("https://example.com", { waitUntil: "networkidle2" });
const title = await page.title();
console.log(title);

await browser.close();
```

### Playwright (Python)

```python
from playwright.sync_api import sync_playwright

# Start: obscura serve --port 9222 --stealth
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.title())
    browser.close()
```

## When to Use: Decision Matrix

| Scenario | Best Skill | Why |
|----------|-----------|-----|
| Stealth scraping (single or bulk) | **obscura** | Built-in anti-detection + low memory + parallel CLI |
| Lightweight CDP backend for Puppeteer/Playwright | **obscura** | 1/7 Chrome memory, instant startup |
| Single page with JS execution needed | **obscura** | Fast load (85ms) + `--eval` flag |
| DOM-to-Markdown with JS rendering | **obscura** | `LP.getMarkdown` CDP method for LLM-ready content |
| Request interception / mocking | **obscura** | `Fetch` domain for live HTTP interception |
| Interactive automation (click, type, snapshot-ref) | agent-browser | Rich interaction API with element refs |
| Sandboxed JS script automation | dev-browser | QuickJS WASM isolation + persistent pages |
| Cloudflare Turnstile / advanced anti-bot (Python) | scrapling | Dedicated Turnstile solver + TLS fingerprinting |
| Clean markdown from URL (no JS needed) | defuddle | Simpler, no binary dependency |
| Terminal visual browsing | carbonyl-browser | Unicode/ANSI rendering in terminal |
| E2E test suites with assertions | e2e-testing | Playwright test runner with reporters |
| MCP interactive browser sessions | cursor-ide-browser | Snapshot YAML + ref-based interaction |

### Quick Decision

```
Need stealth + low memory?          → obscura
Need DOM-to-Markdown (JS pages)?   → obscura (LP.getMarkdown)
Need request interception?         → obscura (Fetch domain)
Need interactive element clicking?  → agent-browser
Need Python anti-bot framework?     → scrapling
Need just the text, no JS?          → defuddle
Need CDP backend, not Chrome?       → obscura serve
Need bulk parallel scraping?        → obscura scrape
```

## Error Handling

| Symptom | Cause | Fix |
|---------|-------|-----|
| `command not found: obscura` | Not installed or not in PATH | Re-run installation; verify `which obscura` |
| `Connection refused` on port 9222 | CDP server not running | Start with `obscura serve --port 9222` first |
| Page loads but content empty | SPA needs JS render time | Add `--wait-until networkidle0` or `--selector ".content"` |
| Per-page timeout in scrape | Slow target or network issue | Increase `--timeout 120` (seconds) |
| Bot detection despite `--stealth` | Advanced anti-bot (Cloudflare, DataDome) | Switch to `scrapling` for Turnstile; use `--wait-until networkidle0` for timing-based detection |
| Garbled output encoding | Non-UTF8 page | Pipe through `iconv` or handle in post-processing |
| High memory with many concurrent workers | Too many concurrent pages | Reduce `--concurrency` count (start with 5) |

## Examples

### Example 1: Single Page Stealth Fetch

Extract text content from a news article with stealth and wait for full render:

```bash
obscura fetch "https://techcrunch.com/latest/" \
  --stealth \
  --wait-until networkidle0 \
  --dump text
```

Extract structured data with JS evaluation:

```bash
obscura fetch "https://techcrunch.com/latest/" \
  --stealth \
  --wait-until networkidle0 \
  --eval "JSON.stringify({
    title: document.querySelector('h1')?.textContent,
    lead: document.querySelector('p')?.textContent
  })"
```

### Example 2: CDP Server for Puppeteer Pipeline

Run Obscura as a background CDP server and connect Puppeteer for a multi-page workflow:

```bash
# Terminal 1: Start CDP server with proxy
obscura serve --port 9222 --stealth --proxy socks5://127.0.0.1:1080

# Terminal 2: Run Puppeteer script
node <<'SCRIPT'
const puppeteer = require("puppeteer-core");
(async () => {
  const browser = await puppeteer.connect({
    browserWSEndpoint: "ws://127.0.0.1:9222"
  });
  const page = await browser.newPage();

  await page.goto("https://example.com/login");
  await page.type("#email", "user@example.com");
  await page.type("#password", "pass");
  await page.click("#submit");
  await page.waitForNavigation();

  const data = await page.evaluate(() => document.body.innerText);
  console.log(data);
  await browser.close();
})();
SCRIPT
```

### Example 3: Parallel Bulk Scraping

Scrape product pages with 10 concurrent workers:

```bash
obscura scrape \
  https://shop.example.com/product/1 \
  https://shop.example.com/product/2 \
  https://shop.example.com/product/3 \
  --concurrency 10 \
  --eval "document.title" \
  --format json \
  --timeout 30
```

Or pipe URLs from a file:

```bash
cat urls.txt | xargs obscura scrape --concurrency 8 --format json
```

### Example 4: DOM-to-Markdown for LLM Ingestion

Use `LP.getMarkdown` via CDP to extract clean Markdown from a JS-rendered page:

```javascript
const puppeteer = require("puppeteer-core");

// Start: obscura serve --port 9222 --stealth
const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://127.0.0.1:9222"
});
const page = await browser.newPage();
await page.goto("https://docs.example.com/guide", { waitUntil: "networkidle0" });

const cdp = await page.target().createCDPSession();
const { markdown } = await cdp.send("LP.getMarkdown");
console.log(markdown);

await browser.close();
```

### Example 5: Request Interception — Block Ads and Trackers

```javascript
const puppeteer = require("puppeteer-core");

const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://127.0.0.1:9222"
});
const page = await browser.newPage();
const cdp = await page.target().createCDPSession();

await cdp.send("Fetch.enable", {
  patterns: [{ urlPattern: "*", requestStage: "Request" }]
});

cdp.on("Fetch.requestPaused", async (event) => {
  const url = event.request.url;
  const blocked = /(ads|tracker|analytics|doubleclick|googlesyndication)/i.test(url);
  if (blocked) {
    await cdp.send("Fetch.failRequest", {
      requestId: event.requestId,
      errorReason: "BlockedByClient"
    });
  } else {
    await cdp.send("Fetch.continueRequest", { requestId: event.requestId });
  }
});

await page.goto("https://example.com", { waitUntil: "networkidle0" });
console.log(await page.title());
await browser.close();
```
