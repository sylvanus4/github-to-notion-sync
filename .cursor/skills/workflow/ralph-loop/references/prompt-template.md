# PROMPT.md Template

Copy this template to `.agent/PROMPT.md` and customize for your project.

```markdown
## Overview

You are implementing the project described in @.agent/prd/SUMMARY.md

## Required Setup

Run `npm run dev` (as background process) in `src` directory.
App will be running at http://localhost:3000

## Before Starting

Check @.agent/STEERING.md for critical work.
Complete items in sequence, remove when done.
Only proceed to implement tasks if no critical work pending.

## Task Flow

Tasks are listed in @.agent/tasks.json

1. Pick highest-priority task with `passes: false` in `tasks.json`
2. Read full spec: `.agent/tasks/TASK-${ID}.json`
3. Check existing dir structure in @.agent/STRUCTURE.md
4. Implement step by step according to spec and write unit test
5. **UI tasks only:** do a Playwright smoke test
   - Check console for errors
   - Write minimal e2e test (happy path only)
   - Skip e2e if unit test already covers functionality
   - Save UI screenshot to `.agent/screenshots/TASK-${ID}-{index}.png`
6. Run `eslint --fix`, `prettier --write` for affected files
7. Run `tsc` and unit tests project-wide
8. All tests must pass
9. When tests pass, set `passes: true` in `tasks.json` for completed task
10. Log entry → `.agent/logs/LOG.md`
11. Update `.agent/STRUCTURE.md` if dirs changed
12. Commit changes (Conventional Commit format)

## Rules

- **CRITICAL**: Only work on **ONE task per invocation**. After committing, output `<promise>TASK-{ID}:DONE</promise>` and **STOP**
- Kill all background processes before outputting promise tag
- No git init/remote changes. **No git push**
- Check last 5 tasks in `.agent/logs/LOG.md` for context
- **CRITICAL**: When **ALL** tasks pass → output `<promise>COMPLETE</promise>` and **nothing else**

## When Stuck

- Blocked: `<promise>BLOCKED:brief description</promise>`
- Decision needed: `<promise>DECIDE:question (Option A vs B)</promise>`
```

## Customization Guide

| Section | What to change |
|---------|---------------|
| Required Setup | Replace with your project's dev server command and port |
| Task Flow step 5 | Remove if no UI tasks; adjust for your test runner |
| Task Flow step 6 | Replace with your project's linter/formatter commands |
| Task Flow step 7 | Replace `tsc` with your type-checker; adjust test runner |
| Rules | Add project-specific constraints (e.g., "never modify shared types") |

## Key Design Decisions

- **One task per iteration** prevents context bloat and keeps commits atomic
- **STEERING.md checked first** allows human intervention without stopping the loop
- **Tests must pass** before marking complete ensures quality gate
- **Promise tags** give the shell script structured signals to control the loop
- **No git push** prevents accidental deployment of incomplete work
