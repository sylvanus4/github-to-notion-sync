---
name: e2e-testing
description: Write, run, and debug Playwright E2E tests for the frontend application. Use for creating E2E tests, running tests, debugging failures, or browser-based testing scenarios.
disable-model-invocation: true
---

# E2E Testing

Playwright-based E2E test writing, execution, and debugging.

## Project Context

- **Test dir**: `frontend/e2e/`
- **Config**: `frontend/playwright.config.ts`
- **Base URL**: `http://localhost:5173`
- **Framework**: Playwright
- **Browser**: Chromium only
- **Runner**: `pnpm test:e2e` or `make test-e2e`

## Test File Conventions

- One test file per feature/page: `e2e/<feature>.spec.ts`
- Page Object Model in `e2e/pages/`
- Fixtures in `e2e/fixtures/`
- Global setup for auth in `e2e/global-setup.ts`

## Writing Tests

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test('should do expected behavior', async ({ page }) => {
    await page.goto('/path');
    await expect(page.getByRole('heading')).toContainText('Expected');
  });
});
```

## Key Patterns

- Use `data-testid` attributes for stable selectors
- Use `page.waitForResponse()` for API-dependent assertions
- Use `test.step()` for logical grouping
- Mock external APIs via `page.route()` when needed
- Take screenshots on failure: `await page.screenshot()`

## Running Tests

```bash
cd frontend
pnpm test:e2e                    # all tests
pnpm test:e2e -- --grep "login"  # filter by name
pnpm test:e2e -- --debug          # step-through debug
```

## Debugging Failures

1. Check if dev server is running
2. Verify test data/seed state
3. Use `--debug` flag for step-through
4. Check `test-results/` for screenshots and traces
5. Verify selector stability (prefer role/testid over CSS)

Do NOT use for: test strategy planning or unit test generation (use qa-test-expert).
