---
name: expect-qa
description: >-
  AI agent-driven browser QA testing via the expect-cli tool. Scans git
  changes (unstaged, branch, or all), generates an adversarial test plan,
  and executes it against a live browser with session recording and replay.
  Works with Claude Code, Codex CLI, and Cursor agents. Use when the user
  asks to "test my changes in a browser", "browser QA", "expect test",
  "adversarial browser test", "run expect", "QA my changes", "test in a
  real browser", "validate UI changes", "expect-qa", "expect-cli",
  "run browser tests on my diff", "verify my code works", "end-to-end
  agent test", "does my code actually work", "test the UI", "break the app",
  "try to find bugs", "QA before merging", "verify in browser",
  "test this PR in a browser", "smoke test my changes", or any request
  for AI-driven browser validation of code changes.
  Do NOT use for writing Playwright E2E test suites with assertions and
  reporters (use e2e-testing). Do NOT use for interactive browser
  exploration with snapshot refs (use agent-browser or cursor-ide-browser
  MCP). Do NOT use for scripted multi-step browser automation without
  QA intent (use dev-browser). Do NOT use for simple URL content fetching
  (use WebFetch or defuddle). Do NOT use for exploratory QA on a running
  app without specific code changes to validate (use qa-dogfood). Do NOT
  use for Playwright-based web app testing in Python (use
  anthropic-webapp-testing).
  Korean triggers: "브라우저 QA", "변경사항 테스트", "expect 테스트",
  "에이전트 QA", "실제 브라우저 테스트", "코드 검증", "코드 동작 확인",
  "UI 변경 검증", "PR 브라우저 테스트", "머지 전 QA", "버그 찾기 테스트".
metadata:
  author: "thaki"
  version: "1.0.0"
  upstream: "millionco/expect"
  category: "testing"
  license: "FSL-1.1-MIT"
---

# expect-qa — AI Agent Browser QA Testing

Let AI agents test your code changes in a real browser. Scans git diffs, generates an adversarial test plan, and runs it against a live Playwright browser with rrweb session recording.

## Prerequisites

```bash
which expect-cli || npm install -g expect-cli@latest
npx playwright install chromium
expect-cli init -y
```

| Requirement | Check | Install |
|-------------|-------|---------|
| expect-cli | `expect-cli --version` | `npm install -g expect-cli@latest` |
| AI agent | `which cursor \|\| which claude \|\| which codex` | At least one must be available |
| Chromium | `npx playwright install chromium` | Auto-downloads on first run |
| Dev server | App running at `EXPECT_BASE_URL` | Default: `http://localhost:3000` |

## Core Workflow

```
1. Agent detects code changes (git diff)
2. AI generates an adversarial test plan
3. Agent executes the plan in a real browser
4. Results: pass/fail + session replay video
5. Fix failures → re-run until all pass
```

### Quick Start

```bash
# Interactive TUI — reviews plan before execution
expect-cli

# Headless — skip plan review, run immediately
expect-cli -m "test the login flow" -y

# Test all branch changes
expect-cli --target branch -y

# Test only unstaged changes
expect-cli --target unstaged -y
```

## CLI Reference

```
Usage: expect-cli [options] [command]

Options:
  -m, --message <instruction>   natural language instruction for what to test
  -f, --flow <slug>             reuse a saved flow by slug
  -y, --yes                     skip plan review, run immediately
  -a, --agent <provider>        agent provider: claude or codex
  -t, --target <target>         what to test: unstaged, branch, or changes (default: changes)
  --headed                      show browser window (visible mode)
  --no-cookies                  skip system browser cookie extraction
  --ci                          CI mode (headless, no cookies, auto-yes, 30min timeout)
  --timeout <ms>                execution timeout in milliseconds
  --replay-host <url>           replay viewer host (default: https://expect.dev)
  --verbose                     enable verbose logging
  -v, --version                 print version
  -h, --help                    display help

Commands:
  init                          install globally and set up agent skill
  add github-action             add GitHub Actions workflow for CI
  add skill                     install expect skill for your agent
  audit                         run workspace lint/type/format audit
```

## Key Principles

### Adversarial Testing Mindset

The `-m` instruction should describe what to **break**, not what to verify:

```bash
# GOOD — adversarial, tries to find bugs
expect-cli -m "try to submit the form with invalid data, empty fields, and XSS payloads" -y

# BAD — just a checklist
expect-cli -m "verify the form has a submit button and fields" -y
```

### Agent-Driven Execution

When running inside an AI agent (Claude Code, Codex, Cursor), always use `-y` to skip interactive plan review:

```bash
expect-cli -m "break the checkout flow with edge cases" -y
```

The agent environment is auto-detected via `CURSOR_AGENT`, `CLAUDECODE`, `CODEX_CI`, or `CI` env vars.

### Custom Base URL

If your app runs on a non-default port:

```bash
EXPECT_BASE_URL=http://localhost:5173 expect-cli -m "test navigation" -y
```

## Examples

### Example 1: Test UI Changes After a Feature Branch

```bash
# Test all changes on current branch vs main
expect-cli --target branch -m "verify the new dashboard widgets render correctly and handle empty data states" -y
```

### Example 2: Quick Validation of Unstaged Work

```bash
# Test only files you just edited
expect-cli --target unstaged -m "test the form validation handles all edge cases" -y
```

### Example 3: CI Integration

```bash
# In GitHub Actions or CI pipeline
expect-cli --ci -m "comprehensive QA of all user-facing changes"
```

Or add a workflow automatically:

```bash
expect-cli add github-action -y
```

### Example 4: Reuse a Saved Flow

```bash
# Run a previously saved test flow
expect-cli -f "login-flow" -y
```

### Example 5: Visible Browser for Debugging

```bash
# Watch the browser as tests execute
expect-cli --headed -m "test the drag-and-drop feature" -y
```

## Session Replay

Every test run generates an rrweb recording viewable at `https://expect.dev`. The replay URL is printed after execution completes. Use `--replay-host` to point to a self-hosted viewer.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `No agent detected` | No Claude Code, Codex, or Cursor found | Install one: `npm i -g @anthropic-ai/claude-code` or ensure Cursor agent mode |
| `expect-cli: command not found` | CLI not installed | `npm install -g expect-cli@latest` |
| `No changes detected` | Clean git working tree | Make changes or use `--target branch` |
| `Browser launch failed` | Missing Chromium | `npx playwright install chromium` |
| `Timeout exceeded` | Test took too long | Increase `--timeout <ms>` or simplify the test scope |
| `EXPECT_BASE_URL unreachable` | App not running | Start your dev server before running expect |

## When to Use: Decision Matrix

| Need | Tool | Why |
|------|------|-----|
| AI-driven QA of code changes | **expect-qa** | Scans diffs, adversarial test plan, session recording |
| Exploratory QA on a running app | qa-dogfood | Unscripted navigation, health scoring |
| Playwright E2E test suites | e2e-testing | Test framework with assertions and reporters |
| Python Playwright web testing | anthropic-webapp-testing | Python-based, browser screenshots, logs |
| Scripted browser automation | dev-browser | Sandboxed JS scripts, persistent pages |
| Interactive browser exploration | agent-browser / cursor-ide-browser | Step-by-step with snapshot refs |
| Simple URL content fetch | defuddle / WebFetch | No browser needed |

## Integration with Project Pipelines

### With deep-review (code review + QA)

After `deep-review` identifies UI changes, run expect to validate them in a real browser:

```bash
# After code review
expect-cli --target branch -m "verify all flagged UI changes work correctly" -y
```

### With ship (pre-merge validation)

Add expect as a pre-merge QA step:

```bash
# Review + QA + commit + PR
expect-cli --target branch -y && echo "QA passed"
```

### With today pipeline

For daily pipeline validation, use `--ci` mode to auto-test the latest changes.

## References

| Reference | When to Read |
|-----------|-------------|
| [references/cli-patterns.md](references/cli-patterns.md) | Advanced CLI usage patterns, CI integration, flow reuse |
| [references/agent-integration.md](references/agent-integration.md) | Agent provider setup, environment detection, skill installation |
