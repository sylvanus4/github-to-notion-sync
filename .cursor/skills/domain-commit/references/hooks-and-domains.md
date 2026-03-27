# Domain Mapping and Pre-commit Hooks

## Domain-to-Path Mapping

Group files by directory prefix into commit batches:

| Domain | Path patterns | Commit type |
|--------|--------------|-------------|
| Project config | `.env*`, `.gitignore`, `docker-compose*`, `.github/`, `Makefile`, `.editorconfig`, `*.toml`, `*.yaml` (root) | `[chore]` |
| Cursor config | `.cursor/` | `[chore]` |
| AI Platform Backend | `ai-platform/backend/` | `[enhance]` |
| AI Platform Frontend | `ai-platform/frontend/` | `[enhance]` |
| AI Platform Console | `ai-platform/console-api/` | `[enhance]` |
| MCP Agents | `agents/` | `[enhance]` |
| Web Apps | `apps/` | `[enhance]` |
| Server | `server/` | `[enhance]` |
| Packages | `packages/` | `[enhance]` |
| Documentation | `docs/` | `[docs]` |
| Generated output | `output/` | `[docs]` |
| Pipeline outputs | `outputs/` | `[docs]` |
| Helm charts | `helm/` | `[chore]` |
| Scripts | `scripts/` | `[chore]` |
| Specs | `specs/` | `[docs]` |
| Tests | `tests/` | `[test]` |
| Tasks | `tasks/` | `[chore]` |
| README files | `**/README.md` (new only) | `[docs]` |
| **Catch-all** | any other path not matched above | `[chore]` |

### Critical: Catch-all Rule

Files that do not match any domain above MUST still be committed.
Assign them to the closest matching domain or use `[chore]` as fallback.
**Never silently skip untracked files.** If `git status` shows untracked
content files (`.md`, `.ts`, `.tsx`, `.go`, `.py`, `.yaml`, `.json`),
they must be staged and committed.

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
