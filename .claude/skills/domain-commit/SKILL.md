---
name: domain-commit
description: Run pre-commit hooks, fix lint errors, and create domain-split git commits from uncommitted changes.
disable-model-invocation: true
---

Create clean, domain-split commits from current uncommitted changes.

## Process

1. **Analyze changes**: Run `git status` and `git diff` to classify changes by domain
2. **Domain classification**: Group files into domains (frontend, backend, infra, docs, config, test)
3. **Pre-commit hooks**: Run hooks and fix lint errors automatically
4. **Split commits**: Create one commit per domain with Conventional Commits format
5. **Verify**: Run `git log --oneline -10` to confirm

## Commit Format

```
<type>: <Summary in English, ≤50 chars>

- Detail in Korean or English
- Wrap at 72 chars
```

Types: feat, fix, docs, chore, refactor, style, test, perf, ci, build, revert

## Rules

- Never use `enhance` type (pre-commit hook rejects it)
- No trailing period in summary
- Imperative mood in summary
- Do not push — only commit locally
