## Ship

End-to-end pre-merge pipeline: parallel code review, auto-fix, domain-split commits, and PR creation in one command.

### Usage

```
/ship                           # full pipeline: review → fix → commit → PR
/ship --no-pr                   # review → fix → commit (skip PR)
/ship --dry-run                 # review only, preview findings
/ship --base dev                # specify PR base branch
/ship --no-fix                  # skip auto-fix step
```

### Workflow

1. **Detect changes** — `git diff` to identify changed files
2. **Parallel review** — 4 agents (Refactor, Quality, Tech Debt, Performance) analyze simultaneously
3. **Auto-fix** — Apply fixes by severity (skip with `--no-fix`)
4. **Verify** — Lint check all modified files
5. **Domain-commit** — Split changes into domain-specific commits
6. **Create PR** — Push branch and open PR with review summary (skip with `--no-pr`)
7. **Report** — PR URL, commit list, review results

### Execution

Read and follow the `ship` skill (`.cursor/skills/ship/SKILL.md`) for pipeline steps, PR template, and error handling.

### Examples

Ship a feature end-to-end:
```
/ship
```

Preview what review would find:
```
/ship --dry-run
```

Commit without PR:
```
/ship --no-pr
```

Ship to a specific base branch:
```
/ship --base dev
```
