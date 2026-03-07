## Ralph Loop

Run an AI coding agent in a continuous loop, completing tasks one-by-one with fresh context each iteration. State persists in `.agent/` text files and git commits.

### Usage

```
/ralph-loop                # guided setup + loop execution
/ralph-loop init           # scaffold .agent/ directory only
/ralph-loop run -n 10      # run 10 iterations
/ralph-loop steer          # edit STEERING.md to redirect agent mid-run
/ralph-loop status         # check LOG.md + tasks.json progress
```

### What it does

1. **Init**: Runs `npx @pageai/ralph-loop` to scaffold the `.agent/` directory (PROMPT.md, tasks.json, tasks/, logs/, history/)
2. **PRD → Tasks**: Converts product requirements into structured `tasks.json` + individual `TASK-{ID}.json` specs
3. **Docker setup**: Authenticates with `docker sandbox run claude .` for sandboxed execution
4. **Loop execution**: Runs `./ralph.sh -n N` — each iteration picks one task, implements it, runs tests, commits, and moves on
5. **Steering**: Edits `.agent/STEERING.md` to redirect the agent mid-run (bug fixes, priority changes, architecture corrections)
6. **Status**: Shows progress from `.agent/logs/LOG.md` and remaining tasks from `tasks.json`

### Skill Reference

This command uses the **ralph-loop** skill at `.cursor/skills/ralph-loop/SKILL.md`.
Read and follow the skill instructions before proceeding.

### Examples

```bash
# Full guided setup from scratch
/ralph-loop

# Quick start: scaffold and run 5 iterations
/ralph-loop init
./ralph.sh -n 5

# Check what's been completed
/ralph-loop status

# Bug found mid-run — redirect the agent
/ralph-loop steer
```

### Notes

- Requires Docker Desktop with AI sandbox support
- Does NOT push to upstream (safety constraint)
- One task per iteration — prevents context window exhaustion
- Works with Claude Code, Codex, Gemini CLI, Copilot CLI
- Best for: MVPs, migrations, refactoring, test generation
- Not ideal for: pixel-perfect design, novel architecture, security-critical code
