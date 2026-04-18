## Auto Commit

Read staged diff and generate conventional commit messages with type, scope, and body. Splits changes into domain-specific commits.

### Usage

```
/auto-commit                           # commit all staged changes
/auto-commit --dry-run                 # preview commit messages without committing
/auto-commit --single                  # single commit instead of domain-split
```

### Workflow

1. **Read diff** — Analyze staged changes via `git diff --cached`
2. **Classify** — Group changes by domain (frontend, backend, infra, docs, etc.)
3. **Generate messages** — Create conventional commit messages (feat/fix/refactor/docs/chore)
4. **Commit** — Run pre-commit hooks and create domain-split commits
5. **Report** — List of created commits with messages

### Execution

Read and follow the `domain-commit` skill (`.cursor/skills/review/domain-commit/SKILL.md`) for pre-commit hook execution, domain classification, and conventional commit format.

### Examples

Auto-commit all staged changes:
```
/auto-commit
```

Preview commit messages:
```
/auto-commit --dry-run
```
