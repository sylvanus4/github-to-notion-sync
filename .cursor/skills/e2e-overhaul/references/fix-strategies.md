# Fix Strategies — Subagent Delegation Guide

## Subagent Configuration

All subagents use: `subagent_type: generalPurpose`, `model: fast`

## Subagent A: Frontend Bug Fixes

**Scope**: Actual bugs in `frontend/src/` that cause test failures.

**Common patterns**:

1. **useParams mismatch**: Route defines `:id` but component destructures `{ runId }`.
   - Fix: Match the destructured name to the route parameter name.
   - Files: Check `App.tsx` routes vs component `useParams` calls.

2. **Missing imports**: Component references undefined variable.
   - Fix: Add the missing import.

3. **Broken hooks**: `useQuery` with `enabled: false` due to undefined dependency.
   - Fix: Ensure the dependency resolves correctly.

4. **Dual rendering**: `MainLayout` renders `<Outlet/>` twice (desktop + mobile sidebar).
   - Impact: `.first()` may select the wrong (hidden) instance.
   - Fix: Tests must scope to the visible container, not the component itself.

**Prompt template**:
```
You are fixing frontend component bugs that cause E2E test failures.

Bug list:
[paste categorized bugs]

For each bug:
1. Read the failing test to understand expected behavior
2. Read the frontend component to find the root cause
3. Fix the component (not the test) when the component is genuinely broken
4. Verify the fix doesn't break other functionality

Report: file changed, what was wrong, what you fixed
```

## Subagent B: Selector & Mock Fixes

**Scope**: Test files in `e2e/tests/` and `e2e/pages/`

**Selector fix patterns**:

| Problem | Fix |
|---------|-----|
| `getByText('exact')` not found | Use regex: `getByText(/partial/i)` |
| Multiple matches | Add `.first()` or scope to parent |
| Role mismatch | Check actual element role in browser |
| data-testid missing | Add to component or use alternative selector |
| Finds hidden mobile element | Scope to `visibleContent(page)` |

**Mock fix patterns**:

| Problem | Fix |
|---------|-----|
| Route not intercepted | Check URL pattern; use `**` glob for path prefix |
| Wrong response shape | Match actual API response structure |
| Missing mock | Create fixture file in `e2e/fixtures/` |
| Mock overrides real data | Ensure `page.route()` runs before navigation |

**Prompt template**:
```
You are fixing E2E test selectors and API mocks.

Failures:
[paste selector/mock failures]

Rules:
- Use viewport-aware helpers from e2e/helpers/viewport.ts
- Mock fixtures go in e2e/fixtures/
- Use glob patterns for API routes: **/api/v1/endpoint**
- All locators must handle dual-rendering (MainLayout renders Outlet twice)

Report: file changed, old selector → new selector, mock added/fixed
```

## Subagent C: Mobile Fixes

**Scope**: All `e2e/tests/*.spec.ts` that fail on `mobile` project

**Fix decision tree**:

```
Test fails on mobile?
  ├── Test clicks sidebar nav link?
  │   └── Add: test.skip(testInfo.project.name === 'mobile', 'Sidebar nav not visible on mobile')
  ├── Test uses desktop-scoped locator (.lg:flex)?
  │   └── Replace with: visibleContent(page) from helpers/viewport.ts
  ├── Test checks element only visible on desktop?
  │   └── Add mobile skip OR create mobile-specific assertion
  └── Test times out finding element?
      └── Scope locator to visible container first
```

**Prompt template**:
```
You are fixing mobile viewport test failures.

Mobile project: iPhone 13 (390x844)
Failures: [paste mobile failures]

Rules:
- Import { visibleContent, isMobile } from '../helpers/viewport'
- Sidebar navigation tests: skip on mobile
- All content locators: scope to visibleContent(page)
- Never target .lg:flex or .hidden.lg:block on mobile
```

## Subagent D: Timeout & Logic Fixes

**Scope**: Tests that time out or have wrong assertions

**Timeout fixes**:

- Add `await page.waitForLoadState('networkidle').catch(() => {})` after navigation
- Replace `waitForTimeout(N)` with explicit condition waits
- Increase specific test timeouts for slow pages: `test.setTimeout(30000)`
- Ensure API mocks are set up BEFORE `page.goto()`

**Logic fixes**:

- Update expected values to match actual API response
- Fix assertion targets (wrong element, wrong attribute)
- Handle i18n: use regex patterns for text that may be English or Korean

## Iteration Protocol

After all 4 subagents complete:

1. Run `cd e2e && npx playwright test --retries=0 --reporter=list`
2. If failures remain:
   - Classify remaining failures (new categories may emerge)
   - Launch targeted fix subagent(s) for remaining issues
   - Max 2 additional iterations
3. If 0 failures: proceed to Phase 5
