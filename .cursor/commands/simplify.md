## Simplify

Run 4 parallel code review agents (Refactor, Quality, Tech Debt, Performance) on code, aggregate findings, and auto-fix issues by priority. Supports 3 scoping modes.

### Usage

```
# Scoping modes
/simplify                          # diff mode (default) — uncommitted changes
/simplify diff                     # explicit diff mode
/simplify today                    # today mode — all files changed today
/simplify full                     # full mode — entire project scan
/simplify project                  # alias for full mode

# Focus (combinable with any mode)
/simplify focus on performance     # diff + prioritize performance
/simplify today focus on security  # today + prioritize security

# Directory scope
/simplify src/api/                 # scan specific directory only
```

### Workflow

1. **Scope files** — Resolve target files by mode (diff / today / full / directory)
2. **Parallel review** — 4 Task sub-agents analyze code simultaneously
3. **Aggregate** — Merge and deduplicate findings by severity
4. **Auto-fix** — Apply fixes from Critical to Low priority
5. **Verify** — Lint check all modified files, fix regressions
6. **Report** — Present structured summary with applied/skipped fixes

### Execution

Read and follow the `simplify` skill (`.cursor/skills/simplify/SKILL.md`) for sub-agent prompts, output format, and error handling.

### Examples

Post-implementation cleanup (diff):
```
/simplify
```

End-of-day review (today):
```
/simplify today
```

Project health check (full):
```
/simplify full
```

Focused review with mode:
```
/simplify today focus on memory efficiency
```
