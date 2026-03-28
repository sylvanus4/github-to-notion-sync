# expect-cli: Agent Integration Guide

## Supported Agents

| Agent | Detection | Env Var |
|-------|-----------|---------|
| Cursor | `which cursor` | `CURSOR_AGENT` |
| Claude Code | `which claude` | `CLAUDECODE` |
| Codex CLI | `which codex` | `CODEX_CI` |

## Installing as an Agent Skill

### Claude Code / Cursor

```bash
expect-cli add skill
```

This installs a `.agents/skills/expect/SKILL.md` file that teaches the agent how to use expect-cli for adversarial testing.

### Codex

For Codex, the skill is installed in the same `.agents/` directory structure.

## Agent Environment Detection

expect-cli auto-detects agent environments by checking:

1. **Environment variables**: `CURSOR_AGENT`, `CLAUDECODE`, `CODEX_CI`, `CI`
2. **Binary presence**: `which cursor`, `which claude`, `which codex`
3. **TTY availability**: Non-interactive terminals trigger headless mode

When running inside an agent, the tool automatically:
- Skips the interactive TUI (equivalent to `-y`)
- Runs in headless mode
- Uses appropriate timeouts

## Writing Effective Test Instructions

### Adversarial Pattern (Recommended)

The `-m` message should tell the agent to act as a hostile user trying to break the app:

```bash
# Try to break authentication
expect-cli -m "attempt to access protected pages without logging in, try SQL injection in login fields, test session timeout handling" -y

# Test form validation exhaustively
expect-cli -m "submit forms with: empty fields, fields exceeding max length, special characters, script tags, very long strings, unicode characters" -y

# Test error recovery
expect-cli -m "trigger network errors, test what happens when API calls fail, verify error messages are helpful" -y
```

### Scope-Aware Testing

Tell the agent what code changed so it focuses on relevant areas:

```bash
# Combine with target for focused testing
expect-cli --target unstaged -m "focus on the components I just modified, test edge cases in the new validation logic" -y
```

## Browser Configuration

### Custom Base URL

```bash
# React dev server
EXPECT_BASE_URL=http://localhost:3000 expect-cli -y

# Next.js
EXPECT_BASE_URL=http://localhost:3000 expect-cli -y

# Vite
EXPECT_BASE_URL=http://localhost:5173 expect-cli -y

# Custom backend
EXPECT_BASE_URL=http://localhost:8080 expect-cli -y
```

### Playwright Browser Setup

expect-cli uses Playwright's Chromium. If not installed:

```bash
npx playwright install chromium
```

## Session Recording (rrweb)

Every test execution generates an rrweb session recording:

1. **During execution**: Browser interactions are recorded
2. **After completion**: Recording is uploaded to the replay host
3. **Replay URL**: Printed to stdout for review

The recording captures:
- DOM mutations
- Mouse/keyboard events
- Network requests
- Console logs
- Screenshot states

## Architecture Overview

```
expect-cli
├── Scans git changes (configurable target)
├── Sends diff + instruction to AI agent
├── Agent generates adversarial test plan
├── Reviews plan (or auto-approves with -y)
├── Launches Playwright browser
├── Agent executes test plan in browser
│   ├── Uses @expect/browser API
│   │   ├── createPage() — new browser context
│   │   ├── snapshot() — AI-friendly page state
│   │   └── act() — agent-driven interaction
│   └── Records session via rrweb
└── Reports results + replay URL
```

## Troubleshooting

### Agent Not Detected

```bash
# Verify agent is available
which cursor && echo "Cursor found"
which claude && echo "Claude Code found"
which codex && echo "Codex found"

# Force a specific agent
expect-cli -a claude -y
```

### Headless Mode Issues

```bash
# Run with visible browser for debugging
expect-cli --headed --verbose -m "test the failing flow" -y
```

### Permission Errors

```bash
# If global install fails
sudo npm install -g expect-cli@latest

# Or use npx without install
npx expect-cli -m "test" -y
```
