# Domain Rules Reference

## Domain Categorization

| Domain | Path patterns | Commit type |
|--------|--------------|-------------|
| Project config | `.env*`, `.gitignore`, `docker-compose*`, `.github/`, `Makefile`, `.cursor/` | `chore:` |
| Agent skills | `.agents/` | `chore:` |
| Database | `db/` | `feat:` |
| Documentation | `docs/` | `docs:` |
| Shared libs | `shared/` | `feat:` |
| Backend services | `services/` | `feat:` |
| Frontend | `frontend/` | `feat:` |
| Client libs | `libs/` | `feat:` |
| Scripts | `scripts/` | `chore:` |
| Infrastructure | `infra/` | `feat:` |
| README files | `**/README.md` (new only) | `docs:` |

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
| conventional-pre-commit | commit message | `conventional-pre-commit v3.0.0` (Conventional Commits) |
