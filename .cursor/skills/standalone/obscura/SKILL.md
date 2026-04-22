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
  version: "1.0"
  upstream: https://github.com/h4ckf0r0day/obscura
  category: standalone/browser
---

# Obscura — Lightweight Headless Browser for AI Agents

Rust-built headless browser optimized for AI agent automation and web scraping.
30MB memory footprint, built-in anti-detection, V8 JS engine, CDP-compatible.

## Prerequisites

### Installation (macOS Apple Silicon)

```bash
# Download the latest release
curl -LO https://github.com/h4ckf0r0day/obscura/releases/latest/download/obscura-aarch64-apple-darwin.tar.gz

# Extract and install
tar xzf obscura-aarch64-apple-darwin.tar.gz
chmod +x obscura
sudo mv obscura /usr/local/bin/

# Verify
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
Bulk scraping? ─────yes──▶ obscura scrape -i urls.txt --parallel 10
```

### Mode 1: fetch — Single Page Extraction

Fetch a single URL, optionally execute JavaScript, and return HTML or extracted text.

```bash
# Basic HTML fetch
obscura fetch https://example.com

# With stealth mode
obscura fetch https://example.com --stealth

# Execute JS and capture result
obscura fetch https://example.com --stealth --eval "document.title"

# Wait for JS rendering before capture
obscura fetch https://spa-app.com --stealth --wait 3000

# Save output to file
obscura fetch https://example.com --stealth -o output.html
```

### Mode 2: serve — CDP Server

Start a Chrome DevTools Protocol server that Puppeteer or Playwright can connect to.
Uses ~30MB memory vs Chrome's ~200MB+.

```bash
# Start CDP server (default port 9222)
obscura serve --port 9222 --stealth

# Background mode for pipeline use
obscura serve --port 9222 --stealth &
OBSCURA_PID=$!

# ... run Puppeteer/Playwright scripts ...

kill $OBSCURA_PID
```

### Mode 3: scrape — Parallel Bulk Scraping

Scrape multiple URLs concurrently from a file or stdin.

```bash
# From a URL file (one URL per line)
obscura scrape -i urls.txt --parallel 10 --stealth -o results/

# With JS wait for SPA content
obscura scrape -i urls.txt --parallel 5 --stealth --wait 2000 -o results/

# Pipe URLs from another command
cat urls.txt | obscura scrape --parallel 8 --stealth -o results/
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

## CLI Reference

### `obscura serve`

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | `9222` | CDP server listen port |
| `--host` | `127.0.0.1` | Bind address |
| `--stealth` | off | Enable anti-detection |

### `obscura fetch`

| Flag | Default | Description |
|------|---------|-------------|
| `--stealth` | off | Enable anti-detection |
| `--wait` | `0` | Wait ms after page load for JS rendering |
| `--eval` | — | JavaScript expression to evaluate and return |
| `-o` | stdout | Output file path |
| `--timeout` | `30000` | Navigation timeout in ms |

### `obscura scrape`

| Flag | Default | Description |
|------|---------|-------------|
| `-i` | stdin | Input file with URLs (one per line) |
| `--parallel` | `1` | Concurrent scraping workers |
| `--stealth` | off | Enable anti-detection |
| `--wait` | `0` | Wait ms per page for JS rendering |
| `-o` | stdout | Output directory for results |
| `--timeout` | `30000` | Per-page navigation timeout in ms |

## When to Use: Decision Matrix

| Scenario | Best Skill | Why |
|----------|-----------|-----|
| Stealth scraping (single or bulk) | **obscura** | Built-in anti-detection + low memory + parallel CLI |
| Lightweight CDP backend for Puppeteer/Playwright | **obscura** | 1/7 Chrome memory, instant startup |
| Single page with JS execution needed | **obscura** | Fast load (85ms) + `--eval` flag |
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
| Page loads but content empty | SPA needs JS render time | Add `--wait 3000` (or higher) |
| `Navigation timeout` | Slow target or network issue | Increase `--timeout 60000` |
| Bot detection despite `--stealth` | Advanced anti-bot (Cloudflare, DataDome) | Switch to `scrapling` for Turnstile; add `--wait` for timing-based detection |
| Garbled output encoding | Non-UTF8 page | Pipe through `iconv` or handle in post-processing |
| High memory with many `--parallel` workers | Too many concurrent pages | Reduce `--parallel` count (start with 5) |

## Examples

### Example 1: Single Page Stealth Fetch

Extract the title and first paragraph from a news article:

```bash
obscura fetch "https://techcrunch.com/latest/" \
  --stealth \
  --wait 2000 \
  --eval "JSON.stringify({
    title: document.querySelector('h1')?.textContent,
    lead: document.querySelector('p')?.textContent
  })"
```

### Example 2: CDP Server for Puppeteer Pipeline

Run Obscura as a background CDP server and connect Puppeteer for a multi-page workflow:

```bash
# Terminal 1: Start CDP server
obscura serve --port 9222 --stealth

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

Scrape 100 product pages with 10 concurrent workers:

```bash
# Prepare URL list
cat > urls.txt <<EOF
https://shop.example.com/product/1
https://shop.example.com/product/2
https://shop.example.com/product/3
EOF

# Run parallel scrape with stealth
obscura scrape -i urls.txt --parallel 10 --stealth --wait 1000 -o ./scraped/

# Results saved as individual HTML files in ./scraped/
ls ./scraped/
```
