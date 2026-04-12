---
name: engineering-harness
version: 1.0.0
description: >
  Engineering & Coding domain harness orchestrator — Fan-out/Fan-in + Evaluator-
  Optimizer pattern. Runs 4 parallel domain-expert review agents (Frontend, Backend/
  DB, Security, Test Coverage), then sequentially applies dependency audit, performance
  profiling, CI quality gate, and domain-split commits with an Evaluator-Optimizer
  loop that re-reviews until the quality bar is met. Wraps 12+ existing review and
  shipping skills into a single end-to-end code-health pipeline. Use when the user
  asks to "run engineering pipeline", "engineering harness", "full code health",
  "엔지니어링 하네스", "코드 건강 파이프라인", "engineering-harness", or wants end-
  to-end code review through shipping. Do NOT use for individual review operations
  (invoke deep-review, simplify, or test-suite directly). Do NOT use for release
  lifecycle (use release-commander directly).
tags: [harness, engineering, orchestrator, fan-out, evaluator-optimizer, code-review, ci]
triggers:
  - "engineering harness"
  - "engineering pipeline"
  - "full code health"
  - "run engineering harness"
  - "code health pipeline"
  - "engineering-harness"
  - "엔지니어링 하네스"
  - "코드 건강 파이프라인"
  - "엔지니어링 파이프라인"
  - "코드 건강 점검"
  - "코드 종합 리뷰"
do_not_use:
  - "For individual review operations (invoke deep-review, simplify, or test-suite directly)"
  - "For release lifecycle (use release-commander)"
  - "For marketing campaigns (use marketing-harness)"
  - "For PM product management (use pm-harness)"
composes:
  - deep-review
  - test-suite
  - security-expert
  - dependency-auditor
  - performance-profiler
  - ci-quality-gate
  - domain-commit
  - ship
  - simplify
  - frontend-expert
  - backend-expert
  - db-expert
---

# Engineering Harness Orchestrator

Fan-out/Fan-in pattern for parallel multi-domain code review, followed by sequential quality enforcement with an Evaluator-Optimizer loop for iterative improvement.

## When to Use

- End-to-end code health assessment before release
- Multi-domain parallel code review (Frontend + Backend/DB + Security + Test)
- Quality enforcement pipeline including dependency audit, performance profiling, and CI gates
- Any "run the engineering pipeline" or "코드 건강 파이프라인" request

## Architecture

```
User Request (mode + scope selection)
       │
       ▼
┌──────────────────────────────────────────┐
│              SCOPE ANALYSIS              │
│  diff | today | full → file list         │
└──────────────────┬───────────────────────┘
                   │
     ┌─────────────┼─────────────┬──────────────┐
     ▼             ▼             ▼              ▼
┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  ← Fan-out (parallel)
│ FRONTEND│ │BACKEND/DB│ │ SECURITY │ │  TEST    │
│ Review  │ │ Review   │ │ Review   │ │ COVERAGE │
│ Phase 1a│ │ Phase 1b │ │ Phase 1c │ │ Phase 1d │
└────┬────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
     └───────────┼───────────┼──────────────┘
                 ▼
       ┌──────────────────┐
       │     FAN-IN       │  ← Merge + Deduplicate findings
       │  CONSOLIDATION   │
       └────────┬─────────┘
                ▼
       ┌──────────────────┐
       │   AUTO-FIX       │  ← Phase 2: Apply fixes by priority
       │   Phase 2        │
       └────────┬─────────┘
                ▼
       ┌──────────────────┐
       │  DEPENDENCY      │  ← Phase 3: CVE scan + patch
       │  AUDIT Phase 3   │
       └────────┬─────────┘
                ▼
       ┌──────────────────┐
       │  PERFORMANCE     │  ← Phase 4: Profiling + SLO check
       │  PROFILE Phase 4 │
       └────────┬─────────┘
                ▼
       ┌──────────────────┐
       │   CI GATE        │  ← Phase 5: Full CI pipeline
       │   Phase 5        │
       └────────┬─────────┘
                │
         ┌──────┴──────┐
         │ All pass?   │
         └──────┬──────┘
           YES ↓      NO → Phase 2 (max 2 iterations)
       ┌──────────────────┐
       │   COMMIT + SHIP  │  ← Phase 6: Domain-split commit + PR
       │   Phase 6        │
       └──────────────────┘
```

## Modes

| Mode | Phases | Use Case |
|------|--------|----------|
| `review` | 1→Fan-in | Multi-domain parallel code review only (no fixes) |
| `fix` | 1→Fan-in→2 | Review + auto-fix |
| `quality` | 1→Fan-in→2→3→4→5 | Full quality enforcement (no commit) |
| `ship` | 1→Fan-in→2→3→4→5→6 | End-to-end: review through PR creation |
| `ci-only` | 5 only | Run CI quality gate only |
| `security-only` | 1c only | Security review only |
| `perf-only` | 4 only | Performance profiling only |
| `full` | 1→Fan-in→2→3→4→5→6 | Same as `ship` |

Default mode: `quality`

## Scoping

The harness supports three scoping modes, consistent with the underlying review skills:

| Scope | Description |
|-------|-------------|
| `diff` | Changed files (uncommitted + staged) |
| `today` | Files modified today |
| `full` | Entire project |

Default scope: `diff`

## Pipeline

### Phase 1: Multi-Domain Fan-out Review

Four parallel review agents analyze the scoped files simultaneously.

#### Phase 1a: Frontend Review

**Skills**: `frontend-expert`, `deep-review` (FE agent)
**Focus**: React component architecture, Vite build, Core Web Vitals, FSD compliance
**Output**: `outputs/engineering-harness/{date}/phase1a-frontend.md`

#### Phase 1b: Backend/DB Review

**Skills**: `backend-expert`, `db-expert`, `deep-review` (BE/DB agent)
**Focus**: Go/Fiber patterns, PostgreSQL schemas, migrations, query plans, API design
**Output**: `outputs/engineering-harness/{date}/phase1b-backend.md`

#### Phase 1c: Security Review

**Skill**: `security-expert`
**Focus**: STRIDE threat model, OWASP Top 10, secret detection, LLM security, PII handling
**Output**: `outputs/engineering-harness/{date}/phase1c-security.md`

#### Phase 1d: Test Coverage Review

**Skill**: `test-suite`
**Focus**: Coverage gaps, test quality, missing edge cases, untested failure modes
**Output**: `outputs/engineering-harness/{date}/phase1d-test-coverage.md`

### Fan-in: Consolidation

Merge all four review outputs, deduplicate overlapping findings, and produce a unified severity-ranked report.

**Output**: `outputs/engineering-harness/{date}/fan-in-consolidated.md`

### Phase 2: Auto-Fix (Generator)

Apply fixes for consolidated findings in priority order: Critical → High → Medium.

**Skill**: `simplify` (fix mode)
**Input**: Consolidated findings from Fan-in
**Output**: `outputs/engineering-harness/{date}/phase2-fixes.md`
**Constraint**: 8/10 confidence gate — only apply fixes the agent is confident about.

### Phase 3: Dependency Audit

Scan for CVEs, classify severity, apply safe patch updates.

**Skill**: `dependency-auditor`
**Input**: Scoped file list (package.json, go.mod, requirements.txt)
**Output**: `outputs/engineering-harness/{date}/phase3-dependency.md`

### Phase 4: Performance Profile

Measure API latency (p50/p95/p99), Core Web Vitals, PostgreSQL slow queries, bundle size.

**Skill**: `performance-profiler`
**Input**: Scoped endpoints + pages
**Output**: `outputs/engineering-harness/{date}/phase4-performance.md`

### Phase 5: CI Quality Gate (Evaluator)

Run the full CI pipeline locally: secret scan, Python lint/test, Go lint/test, frontend lint/test/build, schema check.

**Skill**: `ci-quality-gate`
**Input**: Current working tree (post-fixes)
**Output**: `outputs/engineering-harness/{date}/phase5-ci-gate.md`

**Evaluator-Optimizer Loop**: If CI fails, loop back to Phase 2 (auto-fix) with the specific failure details. Maximum 2 iterations.

### Phase 6: Commit + Ship

Domain-split commits and PR creation.

**Skills**: `domain-commit`, `ship`
**Input**: All fixes applied and CI passing
**Output**: Git commits + PR URL

## Evaluator-Optimizer Loop

The Engineering harness implements an Evaluator-Optimizer loop between Phase 2 (Generator) and Phase 5 (Evaluator):

```
┌──────────────────┐
│ Phase 2: Fix     │◄─── Failure details from Phase 5
│ (Generator)      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Phase 5: CI Gate │───► Pass? → Phase 6
│ (Evaluator)      │───► Fail? → Back to Phase 2 (max 2 iterations)
└──────────────────┘
```

**Stopping criteria**:
- CI gate passes (all checks green)
- Maximum 2 fix-evaluate iterations reached
- No improvement between iterations (same failures persist)

## Skill Routing Table

| User Intent | Routed Skill | Phase |
|-------------|-------------|-------|
| "Review frontend code" | `frontend-expert` + `deep-review` | 1a |
| "Review backend/API" | `backend-expert` + `db-expert` | 1b |
| "Security audit" | `security-expert` | 1c |
| "Check test coverage" | `test-suite` | 1d |
| "Auto-fix findings" | `simplify` | 2 |
| "Scan for CVEs" | `dependency-auditor` | 3 |
| "Profile performance" | `performance-profiler` | 4 |
| "Run CI locally" | `ci-quality-gate` | 5 |
| "Commit and ship" | `domain-commit` + `ship` | 6 |

## Error Handling

| Error | Recovery |
|-------|----------|
| Fan-out agent fails | Other agents continue. Failed agent output marked as UNAVAILABLE. |
| Auto-fix breaks tests | Revert fix, exclude from this iteration, log in findings. |
| CI gate fails after 2 iterations | Produce failure report with remaining issues for manual resolution. |
| Dependency audit finds Critical CVE | Halt pipeline. Report CVE with remediation guidance. |
| Performance profiler timeout | Skip Phase 4, continue with warning in consolidated report. |

## Output Artifacts

| Phase | Stage Name | Output File | Skip Flag |
|-------|-----------|-------------|-----------|
| 1a | Frontend Review | `outputs/engineering-harness/{date}/phase1a-frontend.md` | `skip-frontend` |
| 1b | Backend/DB Review | `outputs/engineering-harness/{date}/phase1b-backend.md` | `skip-backend` |
| 1c | Security Review | `outputs/engineering-harness/{date}/phase1c-security.md` | `skip-security` |
| 1d | Test Coverage | `outputs/engineering-harness/{date}/phase1d-test-coverage.md` | `skip-tests` |
| — | Consolidated | `outputs/engineering-harness/{date}/fan-in-consolidated.md` | — |
| 2 | Auto-Fix | `outputs/engineering-harness/{date}/phase2-fixes.md` | `skip-fix` |
| 3 | Dependency Audit | `outputs/engineering-harness/{date}/phase3-dependency.md` | `skip-deps` |
| 4 | Performance | `outputs/engineering-harness/{date}/phase4-performance.md` | `skip-perf` |
| 5 | CI Gate | `outputs/engineering-harness/{date}/phase5-ci-gate.md` | `skip-ci` |
| 6 | Ship | Git commits + PR URL | `skip-ship` |

## Workspace Convention

- Intermediate files: `_workspace/engineering-harness/`
- Final deliverables: `outputs/engineering-harness/{date}/`
- CI gate logs: `_workspace/engineering-harness/ci-logs/`

## Constraints

- Fan-out agents must not share mutable state; each operates on its own file read context
- Auto-fix confidence gate: only apply fixes with ≥8/10 confidence
- Evaluator-Optimizer loop: maximum 2 iterations to prevent infinite fix cycles
- Critical CVEs in Phase 3 halt the pipeline (no silent pass-through)
- Phase 6 (commit/ship) only runs if Phase 5 passes
- Domain-split commits ensure bisect-friendly git history
