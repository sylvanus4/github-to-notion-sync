# Domain Rules Reference

## Domain Categorization

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
