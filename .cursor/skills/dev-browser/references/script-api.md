# dev-browser Script API Reference

Scripts run in a QuickJS WASM sandbox. Top-level `await` is supported. All output is captured via `console.log()`.

## Browser Globals

These are available at the top level of every script.

### `browser.getPage(name: string): Promise<Page>`

Returns an existing named page or creates a new one. Pages persist across script invocations within the same dev-browser session.

```javascript
const page = await browser.getPage("main");
```

### `browser.newPage(name?: string): Promise<Page>`

Creates a new page. If `name` is provided, the page is stored and can be retrieved later with `getPage`.

```javascript
const page = await browser.newPage("detail");
```

### `browser.listPages(): Promise<object>`

Returns an object describing currently open pages. **Known limitation**: may return `{}` in `--headless` mode even when named pages exist. Prefer `browser.getPage(name)` to retrieve pages by name.

```javascript
const pages = await browser.listPages();
console.log("Open pages:", JSON.stringify(pages));
```

### `browser.closePage(name: string): Promise<void>`

Closes a named page and removes it from the persistent page store.

```javascript
await browser.closePage("detail");
```

---

## Page Object (Playwright API)

The page returned by `browser.getPage()` / `browser.newPage()` exposes the full Playwright `Page` API. Key methods:

### Navigation

```javascript
await page.goto("https://example.com");
await page.goto("https://example.com", { waitUntil: "networkidle" });
await page.goBack();
await page.goForward();
await page.reload();
```

### Selectors & Interaction

```javascript
await page.click("button.submit");
await page.dblclick("#item");
await page.fill("#email", "user@example.com");
await page.type("#search", "query", { delay: 50 });
await page.press("#input", "Enter");
await page.check("#agree");
await page.uncheck("#newsletter");
await page.selectOption("select#country", "US");
await page.hover(".menu-item");
await page.focus("#input");
```

### Waiting

```javascript
await page.waitForSelector(".loaded");
await page.waitForSelector(".loaded", { state: "visible", timeout: 10000 });
await page.waitForLoadState("networkidle");
await page.waitForLoadState("domcontentloaded");
await page.waitForURL("**/dashboard");
await page.waitForTimeout(2000);
```

### Querying

```javascript
const title = await page.title();
const url = await page.url();
const html = await page.content();
const text = await page.textContent(".heading");
const value = await page.inputValue("#email");
const visible = await page.isVisible(".modal");
const count = await page.locator(".item").count();
```

### Evaluate (Run JS in Browser Context)

```javascript
const result = await page.evaluate(() => {
  return document.querySelectorAll("a").length;
});
console.log("Link count:", result);

const data = await page.evaluate((selector) => {
  return Array.from(document.querySelectorAll(selector))
    .map(el => el.textContent);
}, ".product-name");
console.log(JSON.stringify(data));
```

### Screenshots

```javascript
const buffer = await page.screenshot();
const fullPage = await page.screenshot({ fullPage: true });
const element = await page.screenshot({ selector: "#chart" });
```

Prefer the helper `saveScreenshot()` for writing to disk from the sandbox.

### AI Snapshot

```javascript
const snapshot = await page.snapshotForAI();
console.log(snapshot);
```

Returns an accessibility-tree-based text representation of the page, optimized for LLM consumption. Similar to Playwright's `page.accessibility.snapshot()` but formatted for AI agents.

---

## File I/O Helpers

These functions bridge the WASM sandbox and the host filesystem.

### `saveScreenshot(buf: Buffer, path: string): Promise<void>`

Saves a screenshot buffer (from `page.screenshot()`) to the specified path on the host filesystem. Files are written to `~/.dev-browser/tmp/` by default.

```javascript
const buf = await page.screenshot();
await saveScreenshot(buf, "screenshot.png");
```

### `writeFile(path: string, content: string): Promise<void>`

Writes text content to a file on the host filesystem.

```javascript
const data = await page.evaluate(() => JSON.stringify(window.__DATA__));
await writeFile("output/data.json", data);
```

### `readFile(path: string): Promise<string>`

Reads text content from a file on the host filesystem.

```javascript
const config = await readFile("config.json");
const parsed = JSON.parse(config);
```

---

## Console Output

All `console.log()` calls in the script are captured and returned to the calling agent as the command's stdout. This is the primary way to return data from scripts.

```javascript
console.log("Status: OK");
console.log(JSON.stringify({ key: "value" }));
```

---

## Sandbox Constraints

| Capability | Available? |
|-----------|-----------|
| Playwright Page API | Yes (full) |
| `console.log` output | Yes |
| `saveScreenshot`, `writeFile`, `readFile` | Yes (host FS bridge) |
| Direct `fs` / `path` Node modules | No (sandboxed) |
| `fetch` / `http` from script | No (use `page.goto` + `page.evaluate`) |
| `require` / `import` Node modules | No (QuickJS WASM) |
| `process.env` | No (sandboxed) |
| Top-level `await` | Yes |
| ES modules syntax | Limited (QuickJS) |

To access web APIs, use `page.evaluate()` to run code in the browser context where `fetch` is available:

```javascript
const apiData = await page.evaluate(async () => {
  const res = await fetch("/api/data");
  return await res.json();
});
console.log(JSON.stringify(apiData));
```
