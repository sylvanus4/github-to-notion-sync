# Ship Pipeline Steps

## Table of Contents

1. [Review Agent Prompts](#review-agent-prompts)
2. [Domain-Commit Mapping](#domain-commit-mapping)
3. [PR Template](#pr-template)
4. [Pipeline Flags](#pipeline-flags)

## Review Agent Prompts

The ship pipeline reuses the same 4 agents as `/simplify`. Refer to the simplify skill's agent prompts at `.cursor/skills/simplify/references/agent-prompts.md`.

Each agent receives the full list of changed files and returns:

```
CATEGORY: [agent category]
FINDINGS:
- severity: [Critical|High|Medium|Low]
  file: [path]
  line: [number or range]
  issue: [description]
  fix: [suggested change]
```

## Domain-Commit Mapping

Files are grouped into domains for split commits. Follow the domain-commit skill's mapping at `.cursor/skills/domain-commit/references/hooks-and-domains.md`.

Default domain grouping:

| Domain | Patterns |
|--------|----------|
| backend | `api/`, `routes/`, `services/`, `middleware/`, `*.py`, `*.go`, `*.rs` |
| frontend | `components/`, `pages/`, `views/`, `*.tsx`, `*.jsx`, `*.vue`, `*.css` |
| config | `*.json`, `*.yaml`, `*.yml`, `*.toml`, `*.env*`, `Dockerfile`, `docker-compose*` |
| docs | `*.md`, `docs/`, `README*`, `CHANGELOG*` |
| tests | `tests/`, `__tests__/`, `*.test.*`, `*.spec.*` |
| db | `migrations/`, `schemas/`, `*.sql`, `models/` |
| infra | `.github/`, `helm/`, `k8s/`, `terraform/` |

Commit type mapping:

| Domain | Default Type |
|--------|-------------|
| backend | `feat` or `fix` (based on diff) |
| frontend | `feat` or `fix` |
| config | `chore` |
| docs | `docs` |
| tests | `test` |
| db | `feat` |
| infra | `chore` |

## PR Template

```markdown
## Summary
{2-3 bullet points from review findings and changes}

## Changes
{domain-grouped file list}

### Backend
- `path/to/file.py` — {brief description}

### Frontend
- `path/to/component.tsx` — {brief description}

## Review Results
- Findings: {N} total ({breakdown by severity})
- Fixed: {N} | Skipped: {N}
- Lint: PASS

## Test Plan
- [ ] Verify {key behavior 1}
- [ ] Verify {key behavior 2}
```

## Pipeline Flags

| Flag | Effect |
|------|--------|
| (none) | Full pipeline: review → fix → verify → commit → PR |
| `--dry-run` | Review only: show findings, no changes |
| `--no-pr` | Skip PR creation: review → fix → verify → commit |
| `--no-fix` | Skip auto-fix: review → verify → commit → PR |
| `--base BRANCH` | Set PR base branch (default: `main`) |

Flag combinations:
- `--dry-run` overrides all other flags (review only)
- `--no-pr --no-fix` = review + verify + commit (minimal pipeline)
