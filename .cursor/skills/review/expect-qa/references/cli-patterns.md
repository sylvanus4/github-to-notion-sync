# expect-cli: Advanced CLI Patterns

## CI/CD Integration

### GitHub Actions

```bash
# Auto-generate workflow file
expect-cli add github-action -y
```

This creates `.github/workflows/expect.yml` that runs on every push/PR.

### Manual CI Setup

```yaml
# .github/workflows/qa.yml
name: Expect QA
on: [push, pull_request]
jobs:
  qa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm start &  # start dev server
      - run: npx expect-cli --ci -m "comprehensive QA"
        env:
          EXPECT_BASE_URL: http://localhost:3000
```

Key: `--ci` flag automatically sets `--yes`, `--no-cookies`, headless mode, and a 30-minute timeout.

## Flow Management

### Save and Reuse Flows

Flows are test plans that can be saved and replayed:

```bash
# First run generates a flow
expect-cli -m "test checkout flow"
# Save the generated plan as a slug
# Then reuse it:
expect-cli -f "checkout-flow" -y
```

### Target Modes

| Flag | Git Scope | When |
|------|-----------|------|
| `--target changes` (default) | All modified/new files | General QA |
| `--target unstaged` | Only unstaged files | Quick validation during dev |
| `--target branch` | Branch diff vs main/master | Pre-merge validation |

## Agent Provider Selection

```bash
# Auto-detect (default)
expect-cli -y

# Force Claude Code
expect-cli -a claude -y

# Force Codex
expect-cli -a codex -y
```

Auto-detection order:
1. Check `which cursor` → Cursor agent
2. Check `which claude` → Claude Code agent
3. Check `which codex` → Codex CLI agent

## Timeout Configuration

```bash
# Default: 5 minutes
expect-cli -y

# Extended for complex flows
expect-cli --timeout 600000 -m "full checkout with payment" -y

# CI mode default: 30 minutes
expect-cli --ci -m "comprehensive QA"
```

## Verbose Debugging

```bash
# Full Playwright and agent logs
expect-cli --verbose --headed -m "test login" -y
```

Combines `--verbose` (agent logs) + `--headed` (visible browser) for maximum observability.

## Cookie Handling

By default, expect-cli extracts cookies from your system browser for authenticated flows:

```bash
# Skip cookie extraction (fresh session)
expect-cli --no-cookies -m "test as unauthenticated user" -y
```

## Self-Hosted Replay

```bash
# Point to a self-hosted replay viewer
expect-cli --replay-host https://replay.internal.company.com -m "test" -y
```

## Workspace Audit

```bash
# Run lint, type-check, and format audit
expect-cli audit
```

This runs project-level quality checks before browser testing.
