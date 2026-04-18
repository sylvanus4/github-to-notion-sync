## Setup Pre-Commit

Set up Husky pre-commit hooks with lint-staged, Prettier, ESLint, type checking, and test runners.

### Usage

```
/setup-pre-commit
/setup-pre-commit --with-commitlint
/setup-pre-commit --monorepo
```

### Workflow

1. **Audit** — Check for existing hooks, linters, formatters, and package manager
2. **Install** — Add Husky, lint-staged, Prettier, and ESLint as dev dependencies
3. **Configure** — Set up lint-staged rules for JS/TS/CSS/JSON files
4. **Hook** — Create pre-commit (lint-staged), pre-push (typecheck + tests), and optionally commit-msg (conventional commits)
5. **Verify** — Test with intentional lint errors to confirm hooks block bad commits

### Execution

Read and follow the `setup-pre-commit` skill (`.cursor/skills/standalone/setup-pre-commit/SKILL.md`) for the full 6-phase setup workflow.

### Examples

Basic setup for a TypeScript project:
```
/setup-pre-commit
```

With conventional commit enforcement:
```
/setup-pre-commit --with-commitlint
```
