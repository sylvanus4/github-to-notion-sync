---
name: ralph-loop
description: >-
  Set up and run the Ralph Loop — a continuous AI agent loop that completes
  tasks one-by-one from a structured task list, persisting state in text files
  and git commits so each iteration starts with a fresh context window. Use when
  the user asks to "run ralph loop", "set up ralph loop", "continuous agent
  loop", "long-running agent", "AFK coding", "batch task execution", or wants to
  run an AI agent autonomously for many iterations without context window
  limits. Do NOT use for single-task execution (just run the task directly),
  interactive pair-programming sessions (use normal agent mode), or tasks
  requiring pixel-perfect design review (Ralph Loop excels at functional code,
  not visual polish). Korean triggers: "리뷰", "설계", "커밋".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# Ralph Loop

Run an AI coding agent in a continuous loop, completing a structured task list one task per iteration. Each iteration gets a fresh context window; state is persisted in `.agent/` text files and git commits.

Named after Ralph Wiggum from The Simpsons. Originated from [PageAI-Pro/ralph-loop](https://github.com/PageAI-Pro/ralph-loop).

## Prerequisites

- **Docker Desktop** with AI sandbox support (`docker sandbox run`)
- **Claude Code** CLI (or alternative: Codex, Gemini CLI, Copilot CLI, Kiro)
- **Git** initialized repository
- **Test infrastructure**: Playwright (E2E) + Vitest/Jest (unit) recommended

## Workflow

### Step 1: Bootstrap Project

Verify the project has test infrastructure. If missing, scaffold it:

```bash
# Check for existing test setup
ls package.json vitest.config.* playwright.config.* 2>/dev/null

# If missing, install
npm install -D vitest @testing-library/react playwright @playwright/test
npx playwright install chromium
```

### Step 2: Install Ralph Loop

```bash
npx @pageai/ralph-loop
```

This creates the `.agent/` directory. Verify the structure:

```bash
ls -la .agent/
# Expected: PROMPT.md, STEERING.md, tasks.json, tasks/, logs/, history/, skills/, prd/
```

For the full directory layout, see [references/task-format.md](references/task-format.md).

### Step 3: Generate PRD & Tasks

Option A — Use the built-in `prd-creator` skill:

```bash
cd .agent && npx @pageai/ralph-loop prd
```

Option B — Manually create the PRD and task list:

1. Write `.agent/prd/PRD.md` with full requirements
2. Write `.agent/prd/SUMMARY.md` with a concise project overview
3. Populate `.agent/tasks.json` with task entries
4. Create individual `.agent/tasks/TASK-{ID}.json` spec files

For task file format and schema, see [references/task-format.md](references/task-format.md).

### Step 4: Docker Sandbox Setup

```bash
# Set platform for Playwright compatibility
export DOCKER_DEFAULT_PLATFORM=linux/amd64

# Authenticate (answer Yes to bypass permissions)
docker sandbox run claude .
```

### Step 5: Run the Loop

```bash
# Small test run (2 iterations)
./ralph.sh -n 2

# Production run
./ralph.sh -n 30

# Single iteration (debugging)
./ralph.sh --once
```

The script runs this cycle per iteration:

1. Read `.agent/STEERING.md` — handle critical work first
2. Read `.agent/tasks.json` — pick highest-priority task with `passes: false`
3. Read `.agent/tasks/TASK-{ID}.json` — full spec for selected task
4. Implement the task + write tests
5. Run linting + type-check + all tests
6. Mark task `passes: true` in `tasks.json`
7. Log to `.agent/logs/LOG.md`
8. Commit changes (Conventional Commit format)
9. Output promise tag → script handles next iteration or exit

### Step 6: Monitor & Steer

While the loop runs:

- **Check progress**: `cat .agent/logs/LOG.md`
- **Check task status**: `cat .agent/tasks.json | jq '.[] | select(.passes == false)'`
- **Redirect the agent**: Edit `.agent/STEERING.md` to add critical work items (the agent reads this file at the start of each iteration)
- **Review history**: `ls .agent/history/`

For steering patterns, see [references/steering-patterns.md](references/steering-patterns.md).

## Promise Tags

The agent communicates with the loop script via promise tags:

| Tag | Meaning | Exit Code |
|-----|---------|-----------|
| `<promise>TASK-{ID}:DONE</promise>` | Task completed, continue loop | — |
| `<promise>COMPLETE</promise>` | All tasks done | 0 |
| `<promise>BLOCKED:description</promise>` | Needs human help | 2 |
| `<promise>DECIDE:question</promise>` | Needs human decision | 3 |

Exit code 1 = max iterations reached.

## PROMPT.md

The main loop prompt is `.agent/PROMPT.md`. It controls agent behavior each iteration. For the recommended template, see [references/prompt-template.md](references/prompt-template.md).

Key rules enforced by PROMPT.md:
- One task per iteration (prevents context bloat)
- STEERING.md checked before tasks (allows mid-run intervention)
- Tests must pass before marking task complete
- No `git push` (safety)
- Conventional Commit messages

## Strengths & Limitations

**Ralph Loop excels at:**
- Rapid prototyping / MVP builds
- E2E and unit test generation
- Framework migrations (React class → hooks, Vue 2 → 3)
- Large-scale refactoring and boilerplate generation
- Repetitive multi-file changes

**Not ideal for:**
- Pixel-perfect design / UX polish
- Novel architecture from scratch (needs human guidance)
- Security-critical code (requires human review)

## Examples

### Example 1: MVP Build from PRD

User says: "Ralph Loop 세팅해서 이 PRD 기반으로 MVP 빌드해줘"

Actions:
1. `npx @pageai/ralph-loop` to scaffold `.agent/`
2. Write PRD in `.agent/prd/PRD.md`, generate tasks with `prd-creator`
3. `./ralph.sh -n 50` — let it run AFK
4. Review `.agent/logs/LOG.md` in the morning

Result: Working MVP with tests, committed incrementally via one commit per task.

### Example 2: Framework Migration

User says: "React 클래스 컴포넌트 40개를 hooks로 마이그레이션하고 싶어"

Actions:
1. Create one `TASK-{ID}.json` per component migration
2. Set PROMPT.md to enforce test verification after each migration
3. `./ralph.sh -n 45` — one component per iteration

Result: 40 components migrated with passing tests, each in its own atomic commit.

### Example 3: Test Suite Generation

User says: "레거시 코드에 유닛 테스트 전부 만들어줘"

Actions:
1. Generate tasks: one per module/file that needs tests
2. Include coverage thresholds in each task spec
3. `./ralph.sh -n 30`

Result: Comprehensive test suite built incrementally, each file tested and committed separately.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Docker auth fails | Run `docker sandbox run claude .` manually first, answer "Yes" to permissions |
| Playwright SIGILL in sandbox | Add to STEERING.md: `npm install --ignore-scripts` then reinstall Playwright |
| Agent stuck in loop | Edit STEERING.md with explicit instructions to unblock |
| BLOCKED promise tag | Read the description, resolve the blocker, restart with `./ralph.sh --once` |
| Node version mismatch | Pin Node version in STEERING.md or `.nvmrc` |
| Tests fail repeatedly | Check `.agent/history/` for the failing iteration, add fix to STEERING.md |
| Context too large | Reduce PROMPT.md size; move details to task specs |

## Alternative CLIs

Replace `claude` in the Docker command with your preferred CLI:

| CLI | Command |
|-----|---------|
| Claude Code | `docker sandbox run claude .` |
| Codex | `docker sandbox run codex .` |
| Gemini CLI | `docker sandbox run gemini .` |
| Copilot CLI | `docker sandbox run copilot .` |

## References

- [Prompt Template](references/prompt-template.md) — PROMPT.md template
- [Steering Patterns](references/steering-patterns.md) — STEERING.md usage patterns
- [Task Format](references/task-format.md) — tasks.json and TASK-{ID}.json schemas
