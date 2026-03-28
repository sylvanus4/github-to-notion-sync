# dev-browser Connect Mode

Connect mode attaches to a running Chrome instance with remote debugging enabled, allowing automation of pages that are already logged in, have specific state, or require manual interaction first.

## Launching Chrome with Remote Debugging

### macOS

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222
```

### macOS (with specific profile)

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/chrome-debug-profile"
```

### Linux

```bash
google-chrome --remote-debugging-port=9222
```

### Verify Chrome is Ready

```bash
curl -s http://localhost:9222/json/version | jq .Browser
```

---

## Basic Connect Workflow

```bash
# 1. Launch Chrome with debugging port
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &

# 2. Manually navigate to a page and log in (if needed)

# 3. Connect and automate
dev-browser --connect <<'SCRIPT'
const page = await browser.getPage("main");
const url = await page.url();
console.log("Connected to:", url);
const snapshot = await page.snapshotForAI();
console.log(snapshot);
SCRIPT
```

---

## Use Cases

### Automating Logged-In Sessions

When a site requires OAuth, 2FA, or complex auth that's easier done manually:

1. Launch Chrome with `--remote-debugging-port=9222`
2. Log in manually in the browser
3. Use `--connect` to automate the authenticated session

```bash
dev-browser --connect <<'SCRIPT'
const page = await browser.getPage("main");
await page.goto("https://app.example.com/dashboard");
await page.waitForLoadState("networkidle");
const data = await page.evaluate(() =>
  JSON.stringify(window.__DASHBOARD_DATA__)
);
await writeFile("dashboard-data.json", data);
console.log("Data extracted");
SCRIPT
```

### Debugging Page State

Inspect the current state of any tab in the running Chrome:

```bash
dev-browser --connect <<'SCRIPT'
const page = await browser.getPage("main");
console.log("URL:", await page.url());
console.log("Title:", await page.title());
const snapshot = await page.snapshotForAI();
console.log(snapshot);
SCRIPT
```

### Inspecting DevTools-Inaccessible Content

Extract data from pages that are hard to inspect manually:

```bash
dev-browser --connect <<'SCRIPT'
const page = await browser.getPage("main");
const cookies = await page.context().cookies();
console.log(JSON.stringify(cookies, null, 2));
SCRIPT
```

---

## Auto-Connect Pattern

For scripts that should work in both modes, check connectivity first:

```bash
# Try connect first, fall back to headless
dev-browser --connect <<'SCRIPT'
const page = await browser.getPage("main");
console.log("Connected to existing Chrome");
SCRIPT

# If connect fails (no Chrome running), use headless
if [ $? -ne 0 ]; then
  dev-browser --headless <<'SCRIPT'
  const page = await browser.getPage("main");
  await page.goto("https://example.com");
  console.log("Launched headless Chromium");
SCRIPT
fi
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `Could not connect` | Chrome not running or wrong port | Launch Chrome with `--remote-debugging-port=9222` |
| `Connection refused` | Port mismatch or firewall | Verify with `curl http://localhost:9222/json/version` |
| Connected but wrong page | Multiple tabs open | Use `browser.listPages()` to identify pages, or navigate with `page.goto()` |
| Auth state not visible | Chrome launched without profile | Add `--user-data-dir` to persist login state |
| Port already in use | Another Chrome instance using 9222 | Kill existing Chrome or use a different port |
