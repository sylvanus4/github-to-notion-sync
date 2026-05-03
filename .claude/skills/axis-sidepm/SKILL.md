---
name: axis-sidepm
description: >-
  Axis 5 of the 6-Axis Personal Assistant. Side project management —
  multi-project registry, sprint orchestration, code shipping, CI/CD, and PR
  management across 5 ThakiCloud repositories. Use when the user asks for
  "axis sidepm", "side project axis", "사이드PM 축", "project axis",
  "axis-sidepm", or wants side project portfolio management. Do NOT use for
  single-project coding tasks (use the specific review/frontend/backend
  skill). Do NOT use for daily git sync only (use sod-ship or eod-ship).
---

# Axis 5: Side PM

Multi-project management across 5 ThakiCloud repositories. Tracks sprints,
manages code quality, ships changes, and produces portfolio-level status reports.

## Principles

- **Single Responsibility**: Only side project and code management
- **Context Isolation**: Writes to `outputs/axis/sidepm/{date}/`
- **Failure Isolation**: One repo's CI failure does not block other repos
- **File-First Data Bus**: Sprint data and CI results written to files

## Project Registry

| # | Alias | Path | Branch Strategy |
|---|-------|------|-----------------|
| 1 | `ai-platform-strategy` | `~/thaki/ai-platform-strategy` | `dev` branch (standard push/pull and PR workflow) |
| 2 | `ai-model-event-stock-analytics` | `~/thaki/ai-model-event-stock-analytics` | Standard branches |
| 3 | `research` | `~/thaki/ai-platform-strategy` | Standard branches |
| 4 | `ai-template` | `~/thaki/ai-template` | Standard branches |
| 5 | `github-to-notion-sync` | `~/thaki/github-to-notion-sync` | Standard branches |

## Phase Guard Protocol

Before running git sync or CI checks, verify that `sod-ship` or `eod-ship`
was not already invoked today. If their outputs exist, reuse them.

| Phase | Guard File | Skip Condition |
|-------|-----------|----------------|
| 1 (Git sync) | `outputs/axis/sidepm/{date}/git-status.json` | File exists |
| E1 (EOD ship) | `outputs/axis/sidepm/{date}/shipped.json` | File exists |
| E2 (Cursor sync) | `outputs/axis/sidepm/{date}/cursor-sync.json` | File exists |

Pass `--force` to bypass all guards and re-run from scratch.
When a phase is skipped, log `REUSED — {guard_file}` in the dispatch manifest.

## Composed Skills

### Git Operations
- `sod-ship` — start-of-day sync all repos
- `eod-ship` — end-of-day commit + push all repos
- `cursor-sync` — .cursor/ asset sync across repos
- `domain-commit` — domain-split commits
- `release-ship` — commit + push + PR

### Sprint Management
- `sprint-orchestrator` — auto-triage issues and PRs
- `github-sprint-digest` — overnight activity summary
- `commit-to-issue` — track commits as issues
- `pr-to-issue-linker` — bidirectional PR-issue links

### Code Quality
- `ci-quality-gate` — local CI pipeline
- `deep-review` — multi-domain code review
- `simplify` — code cleanup
- `test-suite` — test lifecycle
- `quality-gate-orchestrator` — unified security + quality

### Release
- `release-ops-orchestrator` — weekly release cycle (Tue-Thu)
- `release-commander` — 10-skill release pipeline
- `ship` — pre-merge pipeline

### Status
- `weekly-status-report`, `portfolio-report-generator`
- `engineering-retro` — time-based retrospective
- `standup-digest` — daily standup

### Infrastructure
- `local-dev-runner`, `local-dev-setup`, `service-health-doctor`

## Workflow

### Morning Run (triggered by `axis-dispatcher` ~07:30)

```
Phase 1: Git sync status        → outputs/axis/sidepm/{date}/git-status.json
Phase 2: Sprint triage          → outputs/axis/sidepm/{date}/sprint-triage.json
Phase 3: CI health              → outputs/axis/sidepm/{date}/ci-health.json
Phase 4: Dev brief              → outputs/axis/sidepm/{date}/dev-briefing.md
```

**Phase 1 — Git Sync Status** *(guarded)*
Check Phase Guard: if `outputs/axis/sidepm/{date}/git-status.json` exists,
SKIP and reuse. Otherwise check each repo's dirty state, unpushed commits,
and branch status. Write per-repo status to `git-status.json`.

**Phase 2 — Sprint Triage**
Run `sprint-orchestrator` for `ai-platform-strategy` (primary dev project).
Collect new issues, stale PRs, and unassigned items. Write to `sprint-triage.json`.

**Phase 3 — CI Health**
Check latest GitHub Actions status for each repo via `gh run list`.
Flag any failing CI runs. Write to `ci-health.json`.

**Phase 4 — Dev Briefing**
Compile a Korean developer morning brief:
1. Repos with uncommitted changes
2. PRs awaiting review
3. CI failures needing attention
4. Sprint items assigned to me

### Evening Run (triggered by `axis-dispatcher` ~17:00)

```
Phase E1: Code shipping         → outputs/axis/sidepm/{date}/shipped.json
Phase E2: Cursor sync           → outputs/axis/sidepm/{date}/cursor-sync.json
```

**Phase E1 — Code Shipping** *(guarded)*
Check Phase Guard: if `outputs/axis/sidepm/{date}/shipped.json` exists,
SKIP. Otherwise run `eod-ship` to commit and push all repos. Record what
was shipped.

**Phase E2 — Cursor Sync** *(guarded)*
Check Phase Guard: if `outputs/axis/sidepm/{date}/cursor-sync.json` exists,
SKIP. Otherwise run `cursor-sync` to propagate .cursor/ assets across repos.
Record sync results.

### Weekly (Friday PM)

```
Phase W1: Weekly report         → outputs/axis/sidepm/{date}/weekly-report.md
Phase W2: Release ops check     → outputs/axis/sidepm/{date}/release-status.json
```

**Phase W1 — Weekly Status**
Run `weekly-status-report` for a cross-project portfolio view.

**Phase W2 — Release Ops**
Check release cycle status (Tuesday collection → Wednesday QA → Thursday deploy).

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 1 | `outputs/axis/sidepm/{date}/git-status.json` | Per-repo git status |
| 2 | `outputs/axis/sidepm/{date}/sprint-triage.json` | Sprint triage results |
| 3 | `outputs/axis/sidepm/{date}/ci-health.json` | CI status per repo |
| 4 | `outputs/axis/sidepm/{date}/dev-briefing.md` | Developer morning brief |
| E1 | `outputs/axis/sidepm/{date}/shipped.json` | EOD shipping results |
| E2 | `outputs/axis/sidepm/{date}/cursor-sync.json` | Asset sync results |
| W1 | `outputs/axis/sidepm/{date}/weekly-report.md` | Weekly portfolio report |
| W2 | `outputs/axis/sidepm/{date}/release-status.json` | Release cycle status |

## Slack Channels

- `#효정-할일` — dev briefing, CI failure alerts

## Automation Level

Tracked centrally in `outputs/axis/automation-levels.json`.
Full protocol: `axis-dispatcher/references/automation-levels.md`.

- **Level 0 (current)**: Report only — status and alerts
- **Level 1**: Auto-triage + suggest PR assignments
- **Level 2**: Auto-commit domain-split, auto-post CI status

PR creation and force push NEVER auto-execute (safety constraint).

## Error Recovery

Follow the protocol in `axis-dispatcher/references/failure-alerting.md`.

Git sync failures are per-repo — one repo's failure does not block others.
CI checks are read-only (just querying GitHub API), so they rarely fail.
Sprint triage may fail if GitHub API rate-limits; retry after 60 seconds.

Write errors to `outputs/axis/sidepm/{date}/errors.json` using the
standard error record format (severity S1-S4, phase, impact, recovery).

## Gotchas

- `ai-platform-strategy` uses the standard `dev` branch workflow (push/pull and
  PR/merge per CONTRIBUTING; do not use legacy `tmp` shortcuts)
- Pre-push hook can hang >4min on E2E tests — use `git push --no-verify`
  as workaround
- `github-sprint-digest` needs GitHub tokens — verify with `gh auth status`
