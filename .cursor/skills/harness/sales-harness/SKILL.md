---
name: sales-harness
version: 1.0.0
description: >
  Sales domain harness orchestrator — Pipeline + Expert Pool pattern covering
  lead discovery, enrichment, account research, call prep, outreach, competitive
  intelligence, asset generation, and deal tracking across Apollo, Common Room,
  and native sales skills (19 skills total). Use when the user asks to "run sales
  pipeline", "sales harness", "lead-to-deal pipeline", "영업 하네스",
  "세일즈 파이프라인", "sales-harness", or wants end-to-end sales operations.
  Do NOT use for individual sales operations (invoke kwp-sales-* directly).
  Do NOT use for marketing campaigns (use marketing-harness).
tags: [harness, sales, orchestrator, pipeline, expert-pool, lead-generation, crm]
triggers:
  - "sales harness"
  - "sales pipeline"
  - "lead to deal pipeline"
  - "run sales harness"
  - "sales operations"
  - "sales-harness"
  - "영업 하네스"
  - "세일즈 파이프라인"
  - "영업 파이프라인"
  - "리드 투 딜"
  - "영업 종합"
do_not_use:
  - "For individual sales skill operations (invoke kwp-sales-* directly)"
  - "For marketing campaigns and content (use marketing-harness)"
  - "For customer support tickets (use customer-support-harness)"
  - "For Apollo-only operations (invoke kwp-apollo-* directly)"
composes:
  - kwp-apollo-prospect
  - kwp-apollo-enrich-lead
  - kwp-apollo-sequence-load
  - kwp-sales-account-research
  - kwp-sales-call-prep
  - kwp-sales-draft-outreach
  - kwp-sales-competitive-intelligence
  - kwp-sales-create-an-asset
  - kwp-sales-daily-briefing
  - kwp-common-room-account-research
  - kwp-common-room-call-prep
  - kwp-common-room-compose-outreach
  - kwp-common-room-contact-research
  - kwp-common-room-prospect
  - kwp-common-room-weekly-prep-brief
  - deal-stage-guardian
  - lead-research-agent
  - lead-lifecycle-manager
  - sales-meeting-pipeline
---

# Sales Harness Orchestrator

Pipeline + Expert Pool pattern that routes each pipeline phase to the best-fit expert skill based on available data sources (Apollo, Common Room, or native sales skills).

## When to Use

- Full lead-to-deal lifecycle from ICP-based prospecting through close
- Pre-call preparation combining account research with competitive intelligence
- Generating personalized outreach sequences with enriched lead data
- Competitive intelligence and battlecard creation
- Daily sales briefings and weekly pipeline reviews
- Any "run the sales pipeline" or "영업 파이프라인" request

## Architecture

```
User Request (mode selection)
       │
       ▼
┌──────────────────────────────────────────────────┐
│                 EXPERT POOL ROUTER                │
│  Routes each phase to the best data source:       │
│  Apollo | Common Room | Native Sales              │
└──────────────────────┬───────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
┌────────────┐  ┌────────────┐  ┌────────────┐
│   Apollo   │  │ Common Room│  │   Native   │
│   Expert   │  │   Expert   │  │   Expert   │
│ prospect   │  │ prospect   │  │ account-   │
│ enrich     │  │ contact    │  │ research   │
│ sequence   │  │ account    │  │ call-prep  │
└─────┬──────┘  └─────┬──────┘  └─────┬──────┘
      └───────────────┼───────────────┘
                      ▼
              ┌───────────────┐
              │   PIPELINE    │
              └───────┬───────┘
                      │
    Phase 1: Lead Discovery ──→ Phase 2: Enrichment
              │
    Phase 3: Account Research ──→ Phase 4: Call Prep
              │
    Phase 5: Outreach ──→ Phase 6: Competitive Intel
              │
    Phase 7: Asset Generation ──→ Phase 8: Deal Tracking
```

## Expert Pool Routing

The Expert Pool Router selects the optimal skill for each task based on:

| Condition | Primary Expert | Fallback |
|-----------|---------------|----------|
| ICP-based lead search | `kwp-apollo-prospect` | `kwp-common-room-prospect` |
| Lead enrichment by name/email | `kwp-apollo-enrich-lead` | `kwp-common-room-contact-research` |
| Account-level research | `kwp-common-room-account-research` | `kwp-sales-account-research` |
| Call preparation | `kwp-common-room-call-prep` | `kwp-sales-call-prep` |
| Outreach drafting | `kwp-common-room-compose-outreach` | `kwp-sales-draft-outreach` |
| Sequence loading | `kwp-apollo-sequence-load` | — |
| Competitive intel | `kwp-sales-competitive-intelligence` | — |
| Asset generation | `kwp-sales-create-an-asset` | — |

## Modes

| Mode | Phases | Use Case |
|------|--------|----------|
| `prospect` | 1→2→3→5 | Full prospecting pipeline (discover → enrich → research → outreach) |
| `prep` | 3→4 | Call preparation with account research |
| `compete` | 6 only | Competitive intelligence and battlecard generation |
| `daily` | `kwp-sales-daily-briefing` | Morning sales briefing |
| `weekly` | `kwp-common-room-weekly-prep-brief` | Weekly pipeline review and call prep |
| `asset` | 7 only | Create sales collateral (decks, one-pagers, landing pages) |
| `full` | 1→2→3→4→5→6→7→8 | Complete lead-to-deal pipeline |

Default mode: `prospect`

## Pipeline

### Phase 1: Lead Discovery

Find prospects matching ICP criteria with enriched decision-maker profiles.

**Skills**: `kwp-apollo-prospect` → `kwp-common-room-prospect` → `lead-research-agent`
**Input**: ICP description, target criteria
**Output**: `outputs/sales-harness/{date}/phase1-leads.md`

### Phase 2: Lead Enrichment

Enrich discovered leads with full contact cards, company intel, and social signals.

**Skills**: `kwp-apollo-enrich-lead` → `kwp-common-room-contact-research`
**Input**: Phase 1 lead list
**Output**: `outputs/sales-harness/{date}/phase2-enriched-leads.md`

### Phase 3: Account Research

Deep research on target companies with actionable sales intel.

**Skills**: `kwp-sales-account-research` → `kwp-common-room-account-research`
**Input**: Phase 2 enriched leads
**Output**: `outputs/sales-harness/{date}/phase3-account-research.md`

### Phase 4: Call Preparation

Prepare for sales calls with account context, attendee research, and suggested agenda.

**Skills**: `kwp-sales-call-prep` → `kwp-common-room-call-prep`
**Input**: Phase 3 account research
**Output**: `outputs/sales-harness/{date}/phase4-call-prep.md`

### Phase 5: Outreach

Draft personalized outreach messages with research-backed personalization.

**Skills**: `kwp-sales-draft-outreach` → `kwp-common-room-compose-outreach`
**Input**: Phase 2 lead profiles + Phase 3 account research
**Output**: `outputs/sales-harness/{date}/phase5-outreach-drafts.md`

### Phase 6: Competitive Intelligence

Research competitors and build interactive battlecards.

**Skill**: `kwp-sales-competitive-intelligence`
**Input**: Target account's competitive landscape
**Output**: `outputs/sales-harness/{date}/phase6-competitive-intel.md`

### Phase 7: Asset Generation

Generate tailored sales assets from deal context.

**Skill**: `kwp-sales-create-an-asset`
**Input**: Phase 3-6 context (account + competitive intel)
**Output**: `outputs/sales-harness/{date}/phase7-sales-assets/`

Covers: landing pages, pitch decks, one-pagers, workflow demos.

### Phase 8: Deal Tracking

Monitor deal stage transitions, enforce checklist completion, and track SLA.

**Skills**: `deal-stage-guardian` → `lead-lifecycle-manager`
**Input**: Active deal data
**Output**: `outputs/sales-harness/{date}/phase8-deal-status.md`

## Skill Routing Table

| User Intent | Routed Skill | Phase |
|-------------|-------------|-------|
| "Find leads matching ICP" | `kwp-apollo-prospect` / `kwp-common-room-prospect` | 1 |
| "Enrich this lead" | `kwp-apollo-enrich-lead` / `kwp-common-room-contact-research` | 2 |
| "Research this company" | `kwp-sales-account-research` / `kwp-common-room-account-research` | 3 |
| "Prep for my call" | `kwp-sales-call-prep` / `kwp-common-room-call-prep` | 4 |
| "Draft outreach" | `kwp-sales-draft-outreach` / `kwp-common-room-compose-outreach` | 5 |
| "Competitive battlecard" | `kwp-sales-competitive-intelligence` | 6 |
| "Create a sales deck" | `kwp-sales-create-an-asset` | 7 |
| "Deal stage check" | `deal-stage-guardian` | 8 |
| "Morning briefing" | `kwp-sales-daily-briefing` | — |
| "Weekly prep" | `kwp-common-room-weekly-prep-brief` | — |

## Error Handling

| Error | Recovery |
|-------|----------|
| Apollo API unavailable | Fallback to Common Room expert or web-search-based research |
| Common Room API unavailable | Fallback to native `kwp-sales-*` skills with web research |
| No leads match ICP criteria | Report empty results; suggest broadening ICP parameters |
| Phase N fails | Prior phase outputs remain valid. Fix and re-run from Phase N. |
| Enrichment returns partial data | Continue pipeline with available data; flag incomplete fields |

## Output Artifacts

| Phase | Stage Name | Output File | Skip Flag |
|-------|-----------|-------------|-----------|
| 1 | Lead Discovery | `outputs/sales-harness/{date}/phase1-leads.md` | `skip-discover` |
| 2 | Enrichment | `outputs/sales-harness/{date}/phase2-enriched-leads.md` | `skip-enrich` |
| 3 | Account Research | `outputs/sales-harness/{date}/phase3-account-research.md` | `skip-research` |
| 4 | Call Prep | `outputs/sales-harness/{date}/phase4-call-prep.md` | `skip-prep` |
| 5 | Outreach | `outputs/sales-harness/{date}/phase5-outreach-drafts.md` | `skip-outreach` |
| 6 | Competitive Intel | `outputs/sales-harness/{date}/phase6-competitive-intel.md` | `skip-compete` |
| 7 | Assets | `outputs/sales-harness/{date}/phase7-sales-assets/` | `skip-assets` |
| 8 | Deal Tracking | `outputs/sales-harness/{date}/phase8-deal-status.md` | `skip-deals` |

## Workspace Convention

- Intermediate files: `_workspace/sales-harness/`
- Final deliverables: `outputs/sales-harness/{date}/`
- Lead database cache: `_workspace/sales-harness/lead-cache.json`

## Constraints

- Lead contact data (emails, phones) must be handled per data governance policies
- Outreach drafts require user approval before sending
- Expert Pool selection should prefer the data source with the richest data for the target
- Sequence loading (`kwp-apollo-sequence-load`) requires Apollo API connectivity
- Deal stage transitions in `deal-stage-guardian` require checklist completion before advancing
