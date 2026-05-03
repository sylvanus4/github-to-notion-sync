---
name: playwright-runner
description: >-
  Run ad-hoc Playwright browser automation scripts with a universal Node.js
  executor. Detects local dev servers, writes scripts to /tmp, and provides
  helper utilities for common browser tasks (screenshots, form filling,
  responsive testing, link validation, login flows). Use when running quick
  browser tests, ad-hoc page automation, taking screenshots, testing
  responsive design, checking broken links, or automating form interactions.
  Do NOT use for project E2E test suites (use e2e-testing). Do NOT use for
  Python-based browser testing (use anthropic-webapp-testing). Do NOT use for
  CLI-based browser automation (use agent-browser). Korean triggers: "테스트",
  "설계", "체크", "자동화".
---

# Playwright Runner — Ad-hoc Browser Automation

General-purpose browser automation via a universal Node.js executor. Write custom Playwright scripts, execute them from the skill directory, and get results in real-time with a visible browser window.

## Setup (First Time)

```bash
cd .cursor/skills/playwright-runner && npm run setup
```

This installs Playwright and Chromium. Only needed once.

## Critical Workflow

Follow these steps in order for every automation task:

### Step 1: Detect Dev Servers (for localhost testing)

```bash
cd .cursor/skills/playwright-runner && node -e "require('./lib/helpers').detectDevServers().then(s => console.log(JSON.stringify(s)))"
```

- 1 server found: Use it automatically
- Multiple found: Ask the user which one to test
- None found: Ask for a URL or offer to help start a dev server

### Step 2: Write Script to /tmp

Always write test files to `/tmp/playwright-test-*.js`. Never write to the skill directory or the user's project.

```javascript
// /tmp/playwright-test-page.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001';

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto(TARGET_URL);
  console.log('Page loaded:', await page.title());

  await page.screenshot({ path: '/tmp/screenshot.png', fullPage: true });
  console.log('Screenshot saved to /tmp/screenshot.png');

  await browser.close();
})();
```

### Step 3: Execute from Skill Directory

```bash
cd .cursor/skills/playwright-runner && node run.js /tmp/playwright-test-page.js
```

The executor handles module resolution, auto-installs Playwright if missing, and cleans up temp files.

## Execution Modes

The `run.js` executor supports three input modes:

```bash
# File path
cd .cursor/skills/playwright-runner && node run.js /tmp/playwright-test-page.js

# Inline code (auto-wrapped with browser setup)
cd .cursor/skills/playwright-runner && node run.js "const browser = await chromium.launch({headless: false}); const page = await browser.newPage(); await page.goto('https://example.com'); console.log(await page.title()); await browser.close();"

# Stdin
cat /tmp/playwright-test-page.js | cd .cursor/skills/playwright-runner && node run.js
```

For inline code, the executor auto-injects `chromium`, `firefox`, `webkit`, `devices`, and `helpers`.

## Common Patterns

### Test a Page Across Viewports

```javascript
// /tmp/playwright-test-responsive.js
const { chromium } = require('playwright');
const TARGET_URL = process.env.TEST_URL || 'http://localhost:3000';

const viewports = [
  { name: 'Mobile', width: 375, height: 667 },
  { name: 'Tablet', width: 768, height: 1024 },
  { name: 'Desktop', width: 1280, height: 720 },
  { name: 'Wide', width: 1920, height: 1080 }
];

(async () => {
  const browser = await chromium.launch({ headless: false });

  for (const vp of viewports) {
    const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    const page = await context.newPage();
    await page.goto(TARGET_URL);
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: `/tmp/screenshot-${vp.name}.png`, fullPage: true });
    console.log(`${vp.name} (${vp.width}x${vp.height}): OK`);
    await context.close();
  }

  await browser.close();
})();
```

### Test Login Flow

```javascript
// /tmp/playwright-test-login.js
const { chromium } = require('playwright');
const TARGET_URL = process.env.TEST_URL || 'http://localhost:3000/login';

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  const page = await browser.newPage();
  await page.goto(TARGET_URL);

  await page.fill('input[name="email"], input[type="email"], #email', 'test@example.com');
  await page.fill('input[name="password"], input[type="password"], #password', 'password123');
  await page.click('button[type="submit"]');

  await page.waitForNavigation({ waitUntil: 'networkidle' }).catch(() => {});
  console.log('After login:', page.url());
  console.log('Title:', await page.title());

  await page.screenshot({ path: '/tmp/login-result.png' });
  await browser.close();
})();
```

### Fill and Submit a Form

```javascript
// /tmp/playwright-test-form.js
const { chromium } = require('playwright');
const TARGET_URL = process.env.TEST_URL || 'http://localhost:3000/form';

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const page = await browser.newPage();
  await page.goto(TARGET_URL);

  await page.fill('#name', 'Test User');
  await page.fill('#email', 'test@example.com');
  await page.selectOption('#role', 'developer');
  await page.check('#terms');
  await page.click('button[type="submit"]');

  await page.waitForSelector('.success-message, .confirmation', { timeout: 10000 });
  const message = await page.textContent('.success-message, .confirmation');
  console.log('Result:', message);

  await browser.close();
})();
```

### Check for Broken Links

```javascript
// /tmp/playwright-test-links.js
const { chromium } = require('playwright');
const TARGET_URL = process.env.TEST_URL || 'http://localhost:3000';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto(TARGET_URL);
  await page.waitForLoadState('networkidle');

  const links = await page.$$eval('a[href]', anchors =>
    anchors.map(a => ({ text: a.textContent?.trim(), href: a.href }))
      .filter(l => l.href.startsWith('http'))
  );

  console.log(`Found ${links.length} links to check\n`);
  let broken = 0;

  for (const link of links) {
    try {
      const response = await page.goto(link.href, { timeout: 10000, waitUntil: 'domcontentloaded' });
      const status = response?.status() || 0;
      if (status >= 400) {
        console.log(`BROKEN [${status}]: ${link.text} -> ${link.href}`);
        broken++;
      }
    } catch (e) {
      console.log(`ERROR: ${link.text} -> ${link.href} (${e.message})`);
      broken++;
    }
  }

  console.log(`\nResult: ${broken} broken out of ${links.length} links`);
  await browser.close();
})();
```

### Take Screenshot with Error Handling

```javascript
// /tmp/playwright-test-screenshot.js
const { chromium } = require('playwright');
const TARGET_URL = process.env.TEST_URL || 'https://example.com';

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  try {
    await page.goto(TARGET_URL, { waitUntil: 'networkidle', timeout: 30000 });
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const path = `/tmp/screenshot-${timestamp}.png`;
    await page.screenshot({ path, fullPage: true });
    console.log(`Screenshot saved: ${path}`);
  } catch (error) {
    console.error('Navigation failed:', error.message);
    const path = `/tmp/error-screenshot-${Date.now()}.png`;
    await page.screenshot({ path });
    console.log(`Error screenshot saved: ${path}`);
  }

  await browser.close();
})();
```

## Available Helpers

The `lib/helpers.js` module provides utility functions usable via `require('./lib/helpers')` from inline execution:

| Function | Purpose |
|----------|---------|
| `detectDevServers(customPorts?)` | Detect servers on common ports (3000, 3001, 5173, 8080, etc.) |
| `launchBrowser(type?, options?)` | Launch browser with standard configuration |
| `createPage(context, options?)` | Create page with viewport and user agent |
| `createContext(browser, options?)` | Create context with environment headers |
| `waitForPageReady(page, options?)` | Smart wait for page load |
| `safeClick(page, selector, options?)` | Click with retry logic |
| `safeType(page, selector, text, options?)` | Type with optional clear |
| `extractTexts(page, selector)` | Extract text from elements |
| `takeScreenshot(page, name, options?)` | Screenshot with timestamp |
| `authenticate(page, credentials, selectors?)` | Login with credentials |
| `scrollPage(page, direction, distance?)` | Scroll up/down/top/bottom |
| `extractTableData(page, tableSelector)` | Extract table data as objects |
| `handleCookieBanner(page, timeout?)` | Dismiss common cookie banners |
| `retryWithBackoff(fn, retries?, delay?)` | Retry with exponential backoff |
| `getExtraHeadersFromEnv()` | Parse headers from env vars |

## Custom HTTP Headers

Set custom headers via environment variables:

```bash
# Single header
PW_HEADER_NAME=Authorization PW_HEADER_VALUE="Bearer token123" node run.js /tmp/test.js

# Multiple headers (JSON)
PW_EXTRA_HEADERS='{"Authorization":"Bearer tok","X-Custom":"val"}' node run.js /tmp/test.js
```

## Defaults

- `headless: false` — visible browser for debugging
- `slowMo: 100ms` — slow enough to observe
- Default timeout: 30 seconds
- Screenshots saved to `/tmp/`

## Detailed Reference

For full Playwright API reference (selectors, assertions, network interception, mobile emulation, debugging), see [references/api-reference.md](references/api-reference.md).

## Examples

### Example 1: Standard usage
**User says:** "playwright runner" or request matching the skill triggers
**Actions:** Execute the skill workflow as specified. Verify output quality.
**Result:** Task completed with expected output format.

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Unexpected input format | Validate input before processing; ask user for clarification |
| External service unavailable | Retry with exponential backoff; report failure if persistent |
| Output quality below threshold | Review inputs, adjust parameters, and re-run the workflow |
