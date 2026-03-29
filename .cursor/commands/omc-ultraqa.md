## UltraQA

Autonomous QA cycling: test → diagnose → fix → repeat until the quality goal is met (max 5 cycles). Supports tests, build, lint, typecheck, and custom goals.

### Usage

```
[goal type] [custom command]
```

### Goal Types

| Goal | Description |
|------|-------------|
| `tests` | All test suites pass (default) |
| `build` | Build succeeds with exit 0 |
| `lint` | No lint errors |
| `typecheck` | No type errors |
| `custom <cmd>` | Custom command succeeds |

### Execution

Read and follow the `omc-ultraqa` skill (`.cursor/skills/omc-ultraqa/SKILL.md`) for the full workflow.

### Examples

```bash
# Fix all failing tests
/omc-ultraqa tests

# Fix the build
/omc-ultraqa build

# Fix all lint errors
/omc-ultraqa lint

# Fix type errors
/omc-ultraqa typecheck

# Custom goal
/omc-ultraqa custom "npm run e2e -- --reporter=list"
```
