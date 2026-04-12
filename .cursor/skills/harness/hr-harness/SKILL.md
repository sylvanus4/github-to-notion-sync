---
name: hr-harness
version: 1.0.0
description: >
  Human Resources domain harness orchestrator — Fan-out/Fan-in pattern for
  parallel candidate processing, org planning, compensation benchmarking,
  people analytics, and employee handbook Q&A. Use when the user asks to "run
  HR pipeline", "HR harness", "hiring pipeline", "HR 하네스", "인사 파이프라인",
  "hr-harness", or wants end-to-end HR operations. Do NOT use for individual
  HR operations (invoke kwp-human-resources-* directly). Do NOT use for
  interview scheduling (use smart-meeting-scheduler).
tags: [harness, hr, human-resources, orchestrator, fan-out, recruiting]
triggers:
  - "HR harness"
  - "HR pipeline"
  - "hiring pipeline"
  - "run HR harness"
  - "human resources pipeline"
  - "hr-harness"
  - "HR 하네스"
  - "인사 파이프라인"
  - "인사 하네스"
  - "채용 파이프라인"
  - "HR 종합"
do_not_use:
  - "For individual HR skill operations (invoke kwp-human-resources-* directly)"
  - "For interview scheduling without HR pipeline context (use smart-meeting-scheduler)"
  - "For compensation only (use kwp-human-resources-compensation-benchmarking directly)"
  - "For legal employment matters (use legal-harness)"
composes:
  - kwp-human-resources-recruiting-pipeline
  - kwp-human-resources-interview-prep
  - kwp-human-resources-org-planning
  - kwp-human-resources-compensation-benchmarking
  - kwp-human-resources-people-analytics
  - kwp-human-resources-employee-handbook
---

# HR Harness Orchestrator

Fan-out/Fan-in pattern that enables parallel execution of independent HR workstreams (recruiting, org design, compensation, analytics) and aggregates results into a unified HR operations report.

## When to Use

- Running the full hiring lifecycle from pipeline management through interview prep
- Parallel execution of org planning + compensation benchmarking + people analytics
- Comprehensive HR operations review combining multiple workstreams
- Any "run the HR pipeline" or "인사 파이프라인" request

## Architecture

```
User Request (mode selection)
       │
       ▼
┌──────────────────────────────┐
│         INTAKE               │
│  Parse intent → select mode  │
└──────────┬───────────────────┘
           │
     ┌─────┼─────────────────┐
     │     │                 │
     ▼     ▼                 ▼
┌────────┐ ┌────────┐ ┌──────────┐    ← Fan-out (parallel)
│RECRUIT │ │  ORG   │ │ANALYTICS │
│Pipeline│ │PLANNING│ │  People  │
│ Phase 1│ │Phase 3 │ │ Phase 5  │
└───┬────┘ └───┬────┘ └────┬─────┘
    │          │            │
    ▼          ▼            │
┌────────┐ ┌────────┐      │
│INTERVW │ │  COMP  │      │
│  Prep  │ │BENCHMK │      │
│Phase 2 │ │Phase 4 │      │
└───┬────┘ └───┬────┘      │
    │          │            │
    └──────────┼────────────┘
               ▼
       ┌───────────────┐
       │   FAN-IN      │    ← Aggregate all workstream results
       │  SYNTHESIZE   │
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │   HANDBOOK    │    ← Phase 6: Policy Q&A and reference
       │   Phase 6     │
       └───────────────┘
```

## Modes

| Mode | Phases | Use Case |
|------|--------|----------|
| `hire` | 1→2 | Recruiting pipeline + interview preparation |
| `plan` | 3→4 | Org design + compensation benchmarking |
| `analyze` | 5 only | People analytics (attrition, engagement, diversity) |
| `handbook` | 6 only | Employee handbook Q&A |
| `full` | Fan-out(1,3,5) → Fan-in(2,4) → 6 | Complete HR pipeline |

Default mode: `full`

## Pipeline

### Phase 1: Recruiting Pipeline (Fan-out Branch A)

Track and manage recruiting pipeline stages.

**Skill**: `kwp-human-resources-recruiting-pipeline`
**Input**: Open positions, candidate data
**Output**: `outputs/hr-harness/{date}/phase1-recruiting-pipeline.md`

Covers: sourcing, screening, interviewing, offers, pipeline status.

### Phase 2: Interview Prep (Sequential after Phase 1)

Create structured interview plans with competency-based questions and scorecards.

**Skill**: `kwp-human-resources-interview-prep`
**Input**: Phase 1 candidate profiles
**Output**: `outputs/hr-harness/{date}/phase2-interview-prep.md`

Covers: competency questions, behavioral interview guides, scorecards, evaluation criteria.

### Phase 3: Org Planning (Fan-out Branch B)

Headcount planning, org design, and team structure optimization.

**Skill**: `kwp-human-resources-org-planning`
**Input**: Current org data, growth plans
**Output**: `outputs/hr-harness/{date}/phase3-org-planning.md`

Covers: headcount plan, reporting structure, team size, reorg scenarios.

### Phase 4: Compensation Benchmarking (Sequential after Phase 3)

Benchmark compensation against market data.

**Skill**: `kwp-human-resources-compensation-benchmarking`
**Input**: Phase 3 org plan + market data
**Output**: `outputs/hr-harness/{date}/phase4-compensation.md`

Covers: market rate analysis, salary range recommendations, offer competitiveness.

### Phase 5: People Analytics (Fan-out Branch C)

Analyze workforce data for attrition, engagement, and diversity trends.

**Skill**: `kwp-human-resources-people-analytics`
**Input**: Workforce data (attrition, engagement, diversity metrics)
**Output**: `outputs/hr-harness/{date}/phase5-people-analytics.md`

Covers: attrition rate, turnover analysis, engagement data, retention risk, diversity metrics.

### Phase 6: Employee Handbook (Post-aggregation)

Answer policy and procedure questions from the employee handbook.

**Skill**: `kwp-human-resources-employee-handbook`
**Input**: Aggregated context from all prior phases
**Output**: `outputs/hr-harness/{date}/phase6-handbook-qa.md`

Covers: PTO policy, benefits, expense policy, remote work policy, procedures.

## Fan-out/Fan-in Strategy

### Fan-out (Parallel Execution)

In `full` mode, three independent workstreams run concurrently:
- **Branch A**: Recruiting Pipeline (Phase 1)
- **Branch B**: Org Planning (Phase 3)
- **Branch C**: People Analytics (Phase 5)

These branches have no data dependencies and can execute as parallel subagents.

### Fan-in (Aggregation)

After parallel branches complete:
1. Sequential follow-ups: Phase 2 (after Phase 1) and Phase 4 (after Phase 3)
2. Synthesis: merge all branch outputs into a unified HR operations summary
3. Cross-reference: identify connections (e.g., attrition data informing hiring priorities)

## Skill Routing Table

| User Intent | Routed Skill | Phase |
|-------------|-------------|-------|
| "Manage recruiting pipeline" | `kwp-human-resources-recruiting-pipeline` | 1 |
| "Prepare interview questions" | `kwp-human-resources-interview-prep` | 2 |
| "Plan org structure" | `kwp-human-resources-org-planning` | 3 |
| "Benchmark compensation" | `kwp-human-resources-compensation-benchmarking` | 4 |
| "Analyze workforce data" | `kwp-human-resources-people-analytics` | 5 |
| "Policy question" | `kwp-human-resources-employee-handbook` | 6 |

## Error Handling

| Error | Recovery |
|-------|----------|
| Fan-out branch fails | Other branches continue. Failed branch output marked as INCOMPLETE in synthesis. |
| Missing workforce data for analytics | Skip Phase 5 with WARNING; include data gap in summary. |
| Compensation market data unavailable | Phase 4 produces best-effort analysis with available data; flags data sources needed. |
| Phase N fails | Re-run only the failed phase; parallel branch outputs are isolated. |

## Output Artifacts

| Phase | Stage Name | Output File | Skip Flag |
|-------|-----------|-------------|-----------|
| 1 | Recruiting Pipeline | `outputs/hr-harness/{date}/phase1-recruiting-pipeline.md` | `skip-recruit` |
| 2 | Interview Prep | `outputs/hr-harness/{date}/phase2-interview-prep.md` | `skip-interview` |
| 3 | Org Planning | `outputs/hr-harness/{date}/phase3-org-planning.md` | `skip-org` |
| 4 | Compensation | `outputs/hr-harness/{date}/phase4-compensation.md` | `skip-comp` |
| 5 | People Analytics | `outputs/hr-harness/{date}/phase5-people-analytics.md` | `skip-analytics` |
| 6 | Handbook Q&A | `outputs/hr-harness/{date}/phase6-handbook-qa.md` | `skip-handbook` |
| — | Synthesis | `outputs/hr-harness/{date}/hr-operations-summary.md` | — |

## Workspace Convention

- Intermediate files: `_workspace/hr-harness/`
- Final deliverables: `outputs/hr-harness/{date}/`

## Constraints

- Candidate PII must be handled per data governance policies — no logging to Slack
- Compensation data is confidential — output files must be marked CONFIDENTIAL
- Fan-out branches must not share mutable state; communication only through files
- Interview scorecards must use standardized evaluation criteria (no ad-hoc scales)
