---
name: qa-dogfood
description: >-
  Exploratory browser QA that navigates a running app like a real user, finds
  bugs through unscripted exploration, scores application health with weighted
  metrics, and optionally generates regression tests or applies fixes.
  Supports quick/standard/exhaustive tiers and diff-aware mode. Use when the
  user asks for "QA dogfood", "exploratory QA", "dogfooding", "find bugs",
  "app health check", "QA 탐색", "버그 찾기", "앱 건강 점검", "탐색 QA",
  "qa-dogfood", or wants human-like bug discovery through unscripted
  navigation. Do NOT use for writing Playwright test suites (use e2e-testing),
  CLI browser automation (use agent-browser), or pre-merge code review (use
  deep-review).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# QA Dogfood — Exploratory Browser Quality Assurance

Navigate the running application like a real user to discover bugs through unscripted exploration. Unlike `e2e-testing` (which writes deterministic test suites), this skill explores organically and scores overall application health.

## Usage

```
/qa-dogfood http://localhost:3000                  # standard exploration
/qa-dogfood --tier quick                           # 3-minute quick sweep
/qa-dogfood --tier exhaustive                      # deep 15-minute exploration
/qa-dogfood --diff                                 # focus on areas changed in git diff
/qa-dogfood --fix                                  # auto-fix found bugs (default: report-only)
/qa-dogfood --pages /dashboard,/settings           # scope to specific pages
```

## Exploration Tiers

| Tier | Duration | Depth | Use Case |
|------|----------|-------|----------|
| `quick` | ~3 min | Happy paths only, 1 page per route | Post-commit sanity check |
| `standard` (default) | ~8 min | Happy paths + common edge cases, form validation, error states | Pre-PR QA |
| `exhaustive` | ~15 min | All paths + boundary conditions, race conditions, responsive, accessibility | Pre-release |

## Health Score

Application health is scored on a 0-100 weighted scale:

| Component | Weight | Criteria |
|-----------|--------|----------|
| Functionality | 35% | Do features work as expected? |
| Console errors | 20% | Zero console errors = full score |
| Visual consistency | 15% | Layout breaks, overlapping elements, z-index issues |
| Performance | 15% | Page load time, animation smoothness |
| Accessibility | 10% | Keyboard navigation, focus management, contrast |
| Error handling | 5% | Graceful error states, fallback UI |

Health Grade:
- **A (90-100)**: Ship-ready
- **B (75-89)**: Minor issues, acceptable for staging
- **C (60-74)**: Notable issues, fix before shipping
- **D (40-59)**: Significant problems
- **F (0-39)**: Critical failures, do not ship

## WTF-Likelihood Self-Calibration

For each discovered bug, estimate "how likely is a real user to hit this?":

| Level | Description | Priority |
|-------|-------------|----------|
| **Certain** | Happy path, every user hits it | P0 - Fix immediately |
| **Likely** | Common user flow, most users encounter | P1 - Fix before shipping |
| **Possible** | Edge case, power users or specific conditions | P2 - Fix soon |
| **Unlikely** | Rare conditions, specific timing/input | P3 - Track and fix later |

## Workflow

### Step 1: Gather Context

1. Check if target URL is accessible
2. If `--diff` mode: read `git diff HEAD --name-only` to identify changed areas
3. Map changed files to URL routes (e.g., `src/pages/dashboard/` → `/dashboard`)
4. Determine exploration scope

### Step 2: Explore Application

Use browser MCP tools to navigate and interact:

1. **Start at root** or first `--pages` URL
2. **Take snapshot** of initial state
3. **Navigate systematically**:
   - Click navigation links
   - Fill and submit forms (with valid and invalid data)
   - Trigger loading states (slow network)
   - Check empty states (no data scenarios)
   - Test error states (invalid URLs, expired sessions)
4. **For each page/interaction**:
   - Take screenshot
   - Check console for errors
   - Verify interactive elements respond
   - Check responsive behavior (if exhaustive tier)

### Step 3: Classify Findings

For each discovered issue:

```
BUG:
  page: [URL]
  description: [what happened]
  expected: [what should happen]
  wtf_likelihood: [Certain|Likely|Possible|Unlikely]
  category: [functionality|visual|performance|accessibility|error-handling]
  screenshot: [reference]
  fix_complexity: [trivial|moderate|complex]
```

### Step 4: Calculate Health Score

Sum weighted scores from each component based on findings.

### Step 5: Fix Mode (if `--fix`)

For bugs with `fix_complexity: trivial`:
1. Identify the source file from the page URL
2. Read the file and locate the issue
3. Apply fix via StrReplace
4. Re-navigate to the page to verify fix
5. If fix doesn't resolve: revert and report as unfixed

### Step 6: Report

```
QA Dogfood Report
=================
Target: [URL]
Tier: [quick|standard|exhaustive]
Mode: [report-only|fix]
Diff-aware: [yes — focused on N changed routes | no]

Health Score: [N]/100 (Grade: [A-F])
  Functionality:     [N]/35
  Console errors:    [N]/20
  Visual:            [N]/15
  Performance:       [N]/15
  Accessibility:     [N]/10
  Error handling:    [N]/5

Bugs Found: [N]
  P0 (Certain):  [N]
  P1 (Likely):   [N]
  P2 (Possible): [N]
  P3 (Unlikely): [N]

Top Issues:
  1. [page] — [description] (P[X], [category])
  2. [page] — [description] (P[X], [category])
  3. [page] — [description] (P[X], [category])

Fixed (if --fix): [N] / [N] trivial bugs
Unfixed: [N] (require manual attention)

Pages Explored: [N]
  [list of URLs visited with status]
```

## Diff-Aware Mode

When `--diff` is set:
1. Run `git diff HEAD --name-only` to get changed files
2. Map file paths to URL routes using project structure:
   - `src/pages/<name>/` → `/<name>`
   - `src/features/<domain>/` → pages that use this feature
   - `src/entities/<domain>/` → all pages using this entity
3. Prioritize exploration of changed routes
4. Still do a quick sweep of other routes for integration regressions

## Examples

### Example 1: Quick post-commit check

User runs `/qa-dogfood http://localhost:3000 --tier quick` after a commit.

Actions:
1. Navigate root, dashboard, settings (3 pages)
2. Happy path only: page loads, no console errors, links work
3. Health score: 95/100 (Grade A) — 1 minor console warning
4. Report in ~3 minutes

### Example 2: Pre-release exhaustive QA

User runs `/qa-dogfood http://localhost:3000 --tier exhaustive --fix`.

Actions:
1. Deep exploration: 12 pages, forms with invalid data, error states
2. Find 3 bugs: 1 P1 (broken form validation), 1 P2 (z-index overlap), 1 P3 (missing alt text)
3. Auto-fix P3 (trivial: add alt text)
4. Health score: 72/100 (Grade C) — fix P1 before shipping
5. Report with detailed findings

### Example 3: Diff-aware mode

User runs `/qa-dogfood http://localhost:3000 --diff` after modifying dashboard components.

Actions:
1. Git diff shows 4 files in `src/pages/dashboard/`
2. Focus exploration on `/dashboard` and related routes
3. Quick sweep of other pages for integration issues
4. Find 1 P1 bug in dashboard (new feature broken)
5. Report focused on changed areas

## Error Handling

| Scenario | Action |
|----------|--------|
| Target URL unreachable | Report error, suggest checking if dev server is running |
| Login required | Report as blocker, suggest providing auth credentials |
| Browser crash during exploration | Restart browser, continue from last visited page |
| No routes mapped from diff | Fall back to standard (non-diff) exploration |
