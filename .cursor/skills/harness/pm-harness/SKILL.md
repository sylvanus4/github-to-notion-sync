---
name: pm-harness
version: 1.0.0
description: >
  Product Management domain harness orchestrator — Composite pattern combining
  parallel research fan-out with sequential strategy and execution phases.
  Covers discovery, market research, strategy, PRD lifecycle, sprint planning,
  metrics, and GTM launch across 14 PM skills. Use when the user asks to "run PM
  pipeline", "PM harness", "product management pipeline", "PM 하네스",
  "프로덕트 파이프라인", "pm-harness", or wants end-to-end product management
  operations. Do NOT use for individual PM operations (invoke pm-* or
  kwp-product-management-* directly). Do NOT use for PRD lifecycle only
  (use prd-lifecycle-orchestrator directly).
tags: [harness, pm, product-management, orchestrator, composite, discovery, gtm]
triggers:
  - "PM harness"
  - "PM pipeline"
  - "product management pipeline"
  - "run PM harness"
  - "product operations"
  - "pm-harness"
  - "PM 하네스"
  - "프로덕트 파이프라인"
  - "PM 파이프라인"
  - "제품 관리 파이프라인"
  - "PM 종합"
do_not_use:
  - "For individual PM skill operations (invoke pm-* directly)"
  - "For PRD lifecycle only (use prd-lifecycle-orchestrator)"
  - "For marketing campaigns (use marketing-harness)"
  - "For data analytics dashboards (use data-analyst-orchestrator)"
composes:
  - pm-product-discovery
  - pm-market-research
  - pm-product-strategy
  - pm-execution
  - pm-data-analytics
  - pm-go-to-market
  - pm-marketing-growth
  - kwp-product-management-feature-spec
  - kwp-product-management-competitive-analysis
  - kwp-product-management-metrics-tracking
  - kwp-product-management-roadmap-management
  - kwp-product-management-stakeholder-comms
  - kwp-product-management-user-research-synthesis
  - prd-lifecycle-orchestrator
  - hypothesis-pm
---

# PM Harness Orchestrator

Composite pattern: parallel fan-out for Discovery + Market Research, then sequential Strategy → PRD → Sprint → GTM phases. Wraps the existing `prd-lifecycle-orchestrator` for PRD mode.

## When to Use

- Full product lifecycle from initial discovery through GTM launch
- Parallel market research and product discovery before strategy formulation
- PRD creation with integrated research, quality gates, and stakeholder review
- Sprint planning with OKR alignment and prioritization frameworks
- Go-to-market launch preparation with ICP, battlecards, and growth loops
- Any "run the PM pipeline" or "프로덕트 파이프라인" request

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
     ┌─────┴─────┐
     │           │
     ▼           ▼               ← Fan-out (parallel)
┌──────────┐ ┌──────────┐
│DISCOVERY │ │ MARKET   │
│ Phase 1  │ │ RESEARCH │
│pm-product│ │ Phase 2  │
│-discovery│ │pm-market-│
│          │ │ research │
└────┬─────┘ └────┬─────┘
     └──────┬─────┘
            ▼                    ← Fan-in
     ┌──────────────┐
     │  STRATEGY    │           ← Sequential
     │  Phase 3     │
     │pm-product-   │
     │  strategy    │
     └──────┬───────┘
            ▼
     ┌──────────────┐
     │  PRD         │           ← Delegates to prd-lifecycle-orchestrator
     │  Phase 4     │
     │pm-execution  │
     └──────┬───────┘
            ▼
     ┌──────────────┐
     │  SPRINT      │           ← Sequential
     │  Phase 5     │
     │pm-execution  │
     │ + metrics    │
     └──────┬───────┘
            ▼
     ┌──────────────┐
     │  GTM LAUNCH  │           ← Sequential
     │  Phase 6     │
     │pm-go-to-     │
     │  market      │
     └──────────────┘
```

## Modes

| Mode | Phases | Use Case |
|------|--------|----------|
| `discover` | 1 ∥ 2 (parallel) | Product discovery + market research |
| `strategy` | 3 only | Strategy frameworks (Lean Canvas, SWOT, Porter) |
| `prd` | Delegates to `prd-lifecycle-orchestrator` | Full PRD lifecycle with quality gate |
| `sprint` | 5 only | Sprint planning + OKR + prioritization |
| `gtm` | 6 only | Go-to-market launch preparation |
| `full` | Fan-out(1∥2) → 3 → 4 → 5 → 6 | Complete product lifecycle |

Default mode: `full`

## Pipeline

### Phase 1: Product Discovery (Fan-out Branch A)

Ideation, assumption testing, Opportunity Solution Trees, and experiment design.

**Skill**: `pm-product-discovery`
**Input**: Product area, user problems, initial hypotheses
**Output**: `outputs/pm-harness/{date}/phase1-discovery.md`

Sub-skills: brainstorm ideas, identify assumptions, OST, interview scripts, feature prioritization, experiment design.

### Phase 2: Market Research (Fan-out Branch B)

User personas, market segmentation, competitive analysis, and market sizing.

**Skills**: `pm-market-research`, `kwp-product-management-competitive-analysis`, `kwp-product-management-user-research-synthesis`
**Input**: Target market, user data
**Output**: `outputs/pm-harness/{date}/phase2-market-research.md`

Sub-skills: personas, segmentation, customer journey, TAM/SAM/SOM, competitive analysis, sentiment analysis.

### Phase 2.5: Assumption Validation (Optional)

When Phase 1 or 2 reveals risky assumptions (unvalidated market size, untested user behaviors, pricing hypotheses), invoke `hypothesis-pm` for structured Observe → Hypothesize → Experiment → Conclude validation before committing to strategy. Triggered automatically when:

- Phase 1 discovery surfaces 3+ high-risk assumptions without validation evidence
- Phase 2 market research contains conflicting data points
- User explicitly requests assumption testing

**Skill**: `hypothesis-pm`
**Input**: Phase 1-2 outputs + identified assumptions
**Output**: `outputs/pm-harness/{date}/phase2.5-assumption-validation.md`
**Skip Flag**: `skip-hypothesis`

### Phase 3: Strategy (Sequential after fan-in)

Product strategy, business model, and strategic frameworks.

**Skills**: `pm-product-strategy`, `pm-marketing-growth`
**Input**: Phase 1 discovery + Phase 2 research (merged)
**Output**: `outputs/pm-harness/{date}/phase3-strategy.md`

Sub-skills: Lean Canvas, SWOT, PESTLE, Porter's Five Forces, Ansoff Matrix, pricing strategy, value proposition.

### Phase 4: PRD Lifecycle (Delegates to prd-lifecycle-orchestrator)

Research-backed PRD generation with quality gate, cascade sync, and stakeholder review.

**Skill**: `prd-lifecycle-orchestrator` (wraps `pm-execution`, `kwp-product-management-feature-spec`)
**Input**: Phase 3 strategy + Phase 1-2 research
**Output**: `outputs/pm-harness/{date}/phase4-prd.md`

Delegation: this phase fully delegates to the existing `prd-lifecycle-orchestrator` for its internal pipeline (prd-research-factory → doc-quality-gate → prd-cascade-sync → doc-review-orchestrator).

### Phase 5: Sprint Planning

OKRs, roadmaps, sprint planning, prioritization, and metrics tracking.

**Skills**: `pm-execution`, `kwp-product-management-metrics-tracking`, `kwp-product-management-roadmap-management`
**Input**: Phase 4 PRD
**Output**: `outputs/pm-harness/{date}/phase5-sprint-plan.md`

Sub-skills: OKR definition, sprint planning, RICE/MoSCoW/ICE prioritization, roadmap, retrospective, metrics dashboard.

### Phase 6: GTM Launch

Go-to-market strategy, ICP, beachhead, battlecards, and growth loops.

**Skills**: `pm-go-to-market`, `kwp-product-management-stakeholder-comms`
**Input**: Phase 4 PRD + Phase 3 strategy
**Output**: `outputs/pm-harness/{date}/phase6-gtm.md`

Sub-skills: GTM strategy, ideal customer profile, beachhead segment, growth loops, GTM motions, battlecards.

## Skill Routing Table

| User Intent | Routed Skill | Phase |
|-------------|-------------|-------|
| "Brainstorm product ideas" | `pm-product-discovery` | 1 |
| "Build user personas" | `pm-market-research` | 2 |
| "Competitive analysis" | `kwp-product-management-competitive-analysis` | 2 |
| "Create Lean Canvas" | `pm-product-strategy` | 3 |
| "Write a PRD" | `prd-lifecycle-orchestrator` | 4 |
| "Feature spec" | `kwp-product-management-feature-spec` | 4 |
| "Sprint plan" | `pm-execution` | 5 |
| "Set OKRs" | `pm-execution` | 5 |
| "Track metrics" | `kwp-product-management-metrics-tracking` | 5 |
| "Plan roadmap" | `kwp-product-management-roadmap-management` | 5 |
| "GTM strategy" | `pm-go-to-market` | 6 |
| "Positioning" | `pm-marketing-growth` | 6 |
| "Stakeholder update" | `kwp-product-management-stakeholder-comms` | — |
| "Data analytics" | `pm-data-analytics` | — |

## Error Handling

| Error | Recovery |
|-------|----------|
| Fan-out branch fails | Other branch continues. Failed branch output marked as INCOMPLETE in strategy phase. |
| PRD lifecycle fails | Check `prd-lifecycle-orchestrator` output for specific failure. Re-run Phase 4 only. |
| Missing market data for sizing | Proceed with available data; flag gaps in strategy output. |
| Phase N fails | Prior phase outputs remain valid. Fix and re-run from Phase N. |

## Output Artifacts

| Phase | Stage Name | Output File | Skip Flag |
|-------|-----------|-------------|-----------|
| 1 | Discovery | `outputs/pm-harness/{date}/phase1-discovery.md` | `skip-discover` |
| 2 | Market Research | `outputs/pm-harness/{date}/phase2-market-research.md` | `skip-research` |
| 3 | Strategy | `outputs/pm-harness/{date}/phase3-strategy.md` | `skip-strategy` |
| 4 | PRD | `outputs/pm-harness/{date}/phase4-prd.md` | `skip-prd` |
| 5 | Sprint Plan | `outputs/pm-harness/{date}/phase5-sprint-plan.md` | `skip-sprint` |
| 6 | GTM Launch | `outputs/pm-harness/{date}/phase6-gtm.md` | `skip-gtm` |

## Workspace Convention

- Intermediate files: `_workspace/pm-harness/`
- Final deliverables: `outputs/pm-harness/{date}/`

## Constraints

- Fan-out branches must not share mutable state; communication only through files
- PRD mode delegates entirely to `prd-lifecycle-orchestrator` — do not duplicate its internal logic
- Strategy phase requires merged discovery + research inputs before execution
- Stakeholder comms (`kwp-product-management-stakeholder-comms`) can be invoked at any phase for status updates
- Data analytics (`pm-data-analytics`) is a cross-cutting utility, not bound to a specific phase
