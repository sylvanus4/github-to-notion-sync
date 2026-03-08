# Playwright API Quick Reference

Condensed reference for the most-used Playwright patterns. Full docs at https://playwright.dev/docs/api/class-playwright.

## Selectors (Priority Order)

```javascript
// 1. data-testid (most stable)
page.locator('[data-testid="submit-btn"]')

// 2. Role-based (accessible)
page.getByRole('button', { name: 'Submit' })
page.getByRole('link', { name: 'Home' })
page.getByRole('textbox', { name: 'Email' })

// 3. Text-based
page.getByText('Welcome')
page.getByLabel('Email address')
page.getByPlaceholder('Enter email')

// 4. CSS selector (last resort)
page.locator('.submit-button')
page.locator('#main-content')
```

## Navigation

```javascript
await page.goto('https://example.com');
await page.goto(url, { waitUntil: 'networkidle' });
await page.goBack();
await page.goForward();
await page.reload();
```

## Form Interactions

```javascript
// Text input
await page.fill('#email', 'test@example.com');
await page.type('#search', 'query', { delay: 100 });

// Select dropdown
await page.selectOption('#country', 'US');
await page.selectOption('#color', { label: 'Blue' });

// Checkbox / radio
await page.check('#agree');
await page.uncheck('#newsletter');

// File upload
await page.setInputFiles('#upload', 'path/to/file.pdf');
await page.setInputFiles('#upload', ['file1.jpg', 'file2.jpg']);
```

## Mouse and Keyboard

```javascript
await page.click('#button');
await page.dblclick('#item');
await page.hover('#menu');
await page.press('#input', 'Enter');
await page.keyboard.type('Hello');
await page.keyboard.press('Control+A');
```

## Waiting

```javascript
await page.waitForSelector('.loaded');
await page.waitForLoadState('networkidle');
await page.waitForURL('**/dashboard');
await page.waitForTimeout(2000);
await page.waitForResponse(resp => resp.url().includes('/api/data'));
await page.waitForFunction(() => document.querySelector('.count')?.textContent === '5');
```

## Assertions

```javascript
const { expect } = require('@playwright/test');

await expect(page.locator('.title')).toBeVisible();
await expect(page.locator('.title')).toHaveText('Welcome');
await expect(page.locator('.title')).toContainText('Welc');
await expect(page.locator('#input')).toHaveValue('hello');
await expect(page.locator('.item')).toHaveCount(3);
await expect(page).toHaveURL(/dashboard/);
await expect(page).toHaveTitle('My App');
```

## Screenshots

```javascript
await page.screenshot({ path: '/tmp/page.png' });
await page.screenshot({ path: '/tmp/full.png', fullPage: true });
await page.locator('.card').screenshot({ path: '/tmp/card.png' });
```

## Network Interception

```javascript
// Mock API response
await page.route('**/api/users', route => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([{ id: 1, name: 'Test' }])
  });
});

// Block images
await page.route('**/*.{png,jpg,jpeg}', route => route.abort());

// Modify request
await page.route('**/api/*', route => {
  const headers = { ...route.request().headers(), 'X-Custom': 'value' };
  route.continue({ headers });
});
```

## Mobile Emulation

```javascript
const { devices } = require('playwright');

const iPhone = devices['iPhone 13'];
const context = await browser.newContext({ ...iPhone });

// Common devices: 'iPhone 13', 'iPad Pro 11', 'Pixel 5', 'Galaxy S9+'
```

## Multiple Pages / Tabs

```javascript
const [newPage] = await Promise.all([
  context.waitForEvent('page'),
  page.click('a[target="_blank"]')
]);
await newPage.waitForLoadState();
```

## Debugging

```javascript
// Pause and open inspector
await page.pause();

// Slow down execution
const browser = await chromium.launch({ slowMo: 500 });

// Trace recording
const context = await browser.newContext();
await context.tracing.start({ screenshots: true, snapshots: true });
// ... actions ...
await context.tracing.stop({ path: '/tmp/trace.zip' });
// View: npx playwright show-trace /tmp/trace.zip
```

## Console and Errors

```javascript
page.on('console', msg => console.log('PAGE:', msg.text()));
page.on('pageerror', error => console.log('ERROR:', error.message));
page.on('request', req => console.log('>>>', req.method(), req.url()));
page.on('response', res => console.log('<<<', res.status(), res.url()));
```
