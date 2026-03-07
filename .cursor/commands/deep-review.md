## Deep Review

Run 4 parallel domain-expert agents (Frontend, Backend/DB, Security, Test Coverage) to review code from multiple engineering perspectives and auto-fix findings.

### Usage

```
# Scoping modes
/deep-review                          # diff mode — review uncommitted changes
/deep-review today                    # today mode — all files changed today
/deep-review full                     # full mode — entire project
/deep-review project                  # alias for full mode

# Focus (combinable with any mode)
/deep-review focus on security        # prioritize security findings
/deep-review today focus on testing   # today + prioritize test coverage

# Directory scope
/deep-review src/api/                 # scan specific directory only
```

### Workflow

1. **Scope files** — Resolve target files by mode (diff / today / full / directory)
2. **Classify** — Sort files by domain (frontend, backend, DB, test)
3. **Parallel review** — 4 domain-expert agents analyze simultaneously
4. **Aggregate** — Merge and deduplicate findings by severity
5. **Auto-fix** — Apply fixes from Critical to Low priority
6. **Verify** — Lint check all modified files, fix regressions
7. **Report** — Domain-breakdown summary with applied/skipped fixes

### Execution

Read and follow the `deep-review` skill (`.cursor/skills/deep-review/SKILL.md`) for agent prompts, output format, and error handling.

### Examples

Full-stack review after feature work:
```
/deep-review
```

Security-focused daily review:
```
/deep-review today focus on security
```

Project-wide audit:
```
/deep-review full
```
