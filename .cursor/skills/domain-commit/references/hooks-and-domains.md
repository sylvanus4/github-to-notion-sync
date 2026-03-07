# Domain Mapping and Pre-commit Hooks

## Domain-to-Path Mapping

Group files by directory prefix into commit batches:

| Domain | Path patterns | Commit type |
|--------|--------------|-------------|
| Project config | `.env*`, `.gitignore`, `docker-compose*`, `.github/`, `Makefile`, `.cursor/` | `[chore]` |
| Agent skills | `.agents/` | `[chore]` |
| Database | `db/` | `[enhance]` |
| Documentation | `docs/` | `[docs]` |
| Shared libs | `shared/` | `[enhance]` |
| Backend services | `services/` | `[enhance]` |
| Frontend | `frontend/` | `[enhance]` |
| Client libs | `libs/` | `[enhance]` |
| Scripts | `scripts/` | `[chore]` |
| Infrastructure | `infra/` | `[enhance]` |
| README files | `**/README.md` (new only) | `[docs]` |

Skip empty domains. Combine small domains if fewer than 3 files.

## Pre-commit Hooks

| Hook | Scope | Config |
|------|-------|--------|
| trailing-whitespace, end-of-file-fixer | all files | built-in |
| check-yaml, check-json, check-toml | all files | built-in |
| ruff lint | `services/`, `shared/`, `db/`, `libs/` | `pyproject.toml` |
| black format | `services/`, `shared/`, `db/`, `libs/` | `pyproject.toml` |
| eslint | `frontend/**/*.{ts,tsx,js,jsx}` | `frontend/.eslintrc` |
| golangci-lint | `services/call-manager/**/*.go` | inline |
| gitleaks | all files | built-in |
| commit-msg-format | commit message | `scripts/check-commit-msg.py` |

## Hook Failure Remediation

| Hook | Fix |
|------|-----|
| ruff | Fix code or add `# noqa: RULE` for false positives (TC001/TC002/TC003, B008, RUF012, SIM105 are project-wide ignores in `pyproject.toml`) |
| black | Auto-fixed by hook; just re-add and commit again |
| eslint | Fix TypeScript/React issues |
| golangci-lint | Fix Go errcheck/staticcheck issues |
| commit-msg-format | Shorten summary to 50 chars |
| gitleaks | Remove secrets from staged files |
