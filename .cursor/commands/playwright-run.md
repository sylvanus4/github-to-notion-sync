## Playwright Run

Run ad-hoc Playwright browser automation scripts with a universal Node.js executor. Detects local dev servers, writes scripts to /tmp, and supports visible-browser debugging.

### Usage

```
/playwright-run <url>                # Quick test a URL (navigate, screenshot, report)
/playwright-run --screenshot <url>   # Take full-page screenshot
/playwright-run --responsive <url>   # Test across mobile/tablet/desktop viewports
/playwright-run --links <url>        # Check for broken links
/playwright-run --form <url>         # Test form interactions
/playwright-run --login <url>        # Test login flow
/playwright-run --setup              # Install Playwright and Chromium (first time)
```

### Workflow

1. **Setup** (first time) — `cd .cursor/skills/playwright-runner && npm run setup`
2. **Detect servers** — Auto-detect local dev servers on common ports
3. **Write script** — Create test script at `/tmp/playwright-test-*.js`
4. **Execute** — Run via `cd .cursor/skills/playwright-runner && node run.js /tmp/playwright-test-*.js`
5. **Report** — Display results, save screenshots to `/tmp/`

### Execution

Read and follow the `playwright-runner` skill (`.cursor/skills/review/playwright-runner/SKILL.md`) for common patterns, helper functions, and API reference.

### Examples

Quick test a local dev server:

```
/playwright-run http://localhost:3000
```

Take responsive screenshots:

```
/playwright-run --responsive https://example.com
```

Check for broken links:

```
/playwright-run --links https://docs.example.com
```
