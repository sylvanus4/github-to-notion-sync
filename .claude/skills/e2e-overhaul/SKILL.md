---
name: e2e-overhaul
description: >-
  End-to-end Playwright test overhaul pipeline: run full suite across 3
  browsers (chromium/firefox/mobile), triage failures by category
  (selector/mock/timeout/logic), fix frontend bugs and test issues with
  parallel subagents, extend coverage for uncovered pages, browser-verify all
  tabs with screenshots, and produce a final pass/fail report. Composes
  e2e-testing, diagnose, qa-test-expert, and browser-use. Use when the user
  asks to "overhaul E2E tests", "fix all E2E failures", "comprehensive E2E",
  "E2E 전체 점검", "E2E 오버홀", "테스트 전체 수정", "E2E 100% 통과", "all tabs browser test",
  or wants to go from many failing tests to 100% pass rate with full coverage.
  Do NOT use for writing a single test file (use e2e-testing). Do NOT use for
  test strategy planning only (use qa-test-expert). Do NOT use for running
  tests without fixing (use e2e-test command). Do NOT use for unit or
  integration tests (use test-suite). Korean triggers: "E2E 전체 점검", "E2E 오버홀",
  "테스트 전체 수정", "E2E 100% 통과".
---

# E2E Overhaul — Comprehensive Test Fix & Extend Pipeline

One command to go from "many E2E tests failing" to "100% pass rate with full page coverage and browser verification."

## Usage

```
/e2e-overhaul                     # full 7-phase pipeline
/e2e-overhaul --skip-browser      # skip browser verification phase
/e2e-overhaul --skip-extend       # skip coverage extension (fix only)
/e2e-overhaul --chromium-only     # run only chromium (faster)
/e2e-overhaul --dry-run           # triage only, no fixes
```

## Prerequisites

Before running, ensure:

1. **OrbStack/Docker** running (for PostgreSQL/Redis)
2. **Database** initialized: `make db-up && make db-migrate`
3. **Backend** running on port 4567: `cd backend && source .venv/bin/activate && uvicorn app.main:app --port 4567`
4. **Frontend** running on port 4501: `cd frontend && npm run dev`

## Workflow

### Phase 1: Configuration Audit

Validate test infrastructure matches the project.

1. Read `e2e/playwright.config.ts` — verify:
   - `baseURL` matches frontend port (4501)
   - `webServer` backend port matches actual backend (4567)
   - Health check URL is correct (`/health` not `/api/v1/health`)
   - All 3 projects configured: chromium, firefox, mobile
2. Read `.cursor/rules/testing-conventions.mdc` — verify port consistency
3. Fix any mismatches immediately

### Phase 2: Environment Verification

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:4501   # frontend
curl -s -o /dev/null -w "%{http_code}" http://localhost:4567/health  # backend
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "(postgres|redis)"
```

If services are down, start them or inform the user with exact commands.

### Phase 3: Full Run & Triage

1. Run full suite with retries disabled for fast failure reporting:

```bash
cd e2e && npx playwright test --retries=0 --reporter=list 2>&1 | tee /tmp/e2e-overhaul-run.log
```

2. Parse results and categorize every failure into one of:

| Category | Description | Example |
|----------|-------------|---------|
| **Selector** | Locator doesn't match actual DOM | `getByRole('heading')` finds wrong element |
| **Mock** | Missing or incorrect API mock | Route not intercepted, wrong response shape |
| **Timeout** | Element never appears or API never responds | `waitForSelector` exceeds timeout |
| **Logic** | Assertion error, wrong expected value | `expect(text).toBe('X')` but got 'Y' |
| **Frontend Bug** | Actual bug in frontend code | `useParams` mismatch, broken component |
| **Mobile** | Works on desktop, fails on mobile viewport | Hidden sidebar elements clicked on mobile |
| **Environment** | Service not running, port mismatch | Connection refused, wrong URL |

3. Priority rank: Frontend Bug > Environment > Logic > Selector > Mock > Mobile > Timeout

If `--dry-run`, present triage report and stop.

### Phase 4: Parallel Fix (up to 4 subagents)

Launch parallel subagents grouped by failure category. For the subagent delegation strategy, see [references/fix-strategies.md](references/fix-strategies.md).

**Subagent A — Frontend Bugs**: Fix actual frontend component bugs (useParams, missing imports, broken hooks). These block everything else.

**Subagent B — Selector & Mock Fixes**: Update test selectors to match actual DOM. Add missing API mocks. Fix route patterns (glob vs regex).

**Subagent C — Mobile Fixes**: Create viewport-aware helpers (`visibleContent()`, `visibleMain()`). Add `test.skip` for desktop-only tests on mobile. Scope locators to visible containers.

**Subagent D — Timeout & Logic Fixes**: Adjust timeouts, add `waitForLoadState`, fix assertion values, handle race conditions.

After all subagents complete, run the full suite again to verify:

```bash
cd e2e && npx playwright test --retries=0
```

If failures remain, iterate (max 2 rounds).

### Phase 5: Coverage Extension (skip if `--skip-extend`)

1. Read `frontend/src/components/layout/Sidebar.tsx` to enumerate all navigation tabs
2. List all existing `e2e/tests/*.spec.ts` files
3. For each tab WITHOUT a dedicated spec file:
   a. Create a Page Object Model in `e2e/pages/{page}.page.ts`
   b. Create a spec file in `e2e/tests/{page}.spec.ts` with 6-8 test cases
   c. Include API mocks, i18n-aware selectors, mobile-compatible locators
4. Extend `e2e/tests/navigation.spec.ts` to cover all sidebar tabs
5. Run only the new specs to verify they pass

### Phase 6: Browser Verification (skip if `--skip-browser`)

Use the browser-use subagent to manually verify all tabs:

1. Navigate to each page URL
2. Wait for content to load
3. Take a screenshot (save to `e2e/screenshots/`)
4. Check browser console for JavaScript errors
5. Verify the page is not blank

Produce a verification table:

```
| Tab | URL | Status | Console Errors | Notes |
|-----|-----|--------|----------------|-------|
```

### Phase 7: Final Run & Report

1. Run the complete suite across all 3 browsers with HTML report:

```bash
cd e2e && npx playwright test --reporter=html,list --retries=0
```

2. Generate the final report:

```
E2E Overhaul Report
====================
Initial state:  [N] passed, [N] failed, [N] skipped
Final state:    [N] passed, [N] failed, [N] skipped

Fixes applied:
  Frontend bugs:  [N] (list)
  Test fixes:     [N] (selectors, mocks, timeouts)
  Mobile fixes:   [N] (viewport helpers, skips)

Coverage added:
  New spec files: [list]
  New POMs:       [list]
  Navigation:     [N] tabs covered

Browser verification: [N]/[N] tabs OK

Files changed:  [list]
```

3. Update `MEMORY.md` with session record
4. Update `tasks/todo.md` with completion entry

## Key Patterns

### Viewport-Aware Locators

The `MainLayout` renders `<Outlet/>` twice (desktop + mobile). Use the project helper:

```typescript
import { visibleContent } from '../helpers/viewport';
const content = visibleContent(page);
const heading = content.getByRole('heading', { name: /Title/i });
```

### Mobile Test Skipping

Sidebar navigation tests cannot work on mobile (sidebar is hidden):

```typescript
test('TC-NAV-001: Sidebar nav', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name === 'mobile', 'Sidebar nav not visible on mobile');
  // ...
});
```

### API Mock Pattern

```typescript
await page.route('**/api/v1/endpoint**', async (route) => {
  await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(mockData) });
});
```

## Composed Skills

| Skill | Role in Pipeline |
|-------|-----------------|
| e2e-testing | Test patterns, selectors, debugging strategies |
| diagnose | Root cause analysis for complex failures |
| qa-test-expert | Test strategy, coverage gap analysis |
| browser-use (subagent) | Tab-by-tab browser verification |

## Examples

### Example 1: Full overhaul from 52 failures to 0

User says: "E2E 전체 점검해줘" or "/e2e-overhaul"

Actions:
1. Config audit: found backend port mismatch (8000→4567), fixed
2. Full run: 52 failures across 12 specs
3. Triage: 5 frontend bugs, 20 selector issues, 15 mock issues, 12 mobile issues
4. 4 parallel subagents fix all categories
5. Re-run: 11 remaining → second round fixes dual-rendering + useParams bug
6. Coverage: added 2 new spec files, extended navigation to all 17 tabs
7. Browser: 18/18 tabs verified with screenshots
8. Final: 546 passed, 18 skipped, 0 failed

### Example 2: Fix-only mode

User says: "/e2e-overhaul --skip-extend --skip-browser"

Actions:
1. Config + env verification
2. Run suite, triage failures
3. Fix all failures in parallel
4. Final run confirms 0 failures
5. Report (no coverage extension, no browser screenshots)

## Error Handling

| Scenario | Action |
|----------|--------|
| No test files found | Check `e2e/tests/` path; inform user |
| Services not running | Provide exact start commands; wait for user |
| Fix introduces new failures | Revert the fix, try alternative approach |
| Circular breakage (fix A breaks B) | Isolate units, apply Must-NOT-Have guardrails per bugfix-loop rule |
| Subagent timeout | Re-launch once; continue with partial results |
| >100 failures | Focus on environment/config first; likely systemic issue |
| Browser verification tab blank | Check if page requires auth or specific data |

## Troubleshooting

- **"No tests found" error**: Ensure you run from `e2e/` directory, not project root
- **All mobile tests fail**: Check if `MainLayout` has dual `<Outlet/>`; use `visibleContent()` helper
- **API mocks not intercepting**: Use glob patterns (`**`) not regex; check URL matches actual requests
- **Bollinger Bands tests slow**: These wait for real API data; consider adding specific mocks


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
