---
name: sales-agent-harness
description: >-
  Unified orchestrator for ThakiCloud's 5 sales automation agents. Supports 4
  execution modes: rfp-flow (RFP → security Q&A → proposal pipeline),
  meeting-prep (deal preparation), partner-deal (partner orchestration), and
  full (all 5 agents in optimal order). Extends the existing sales-harness
  with ThakiCloud-specific agents while preserving access to the 19 skills in
  the base sales-harness. Use when the user asks to "run sales pipeline",
  "sales agent harness", "rfp to proposal", "full sales flow", "영업 에이전트 하네스",
  "RFP 파이프라인", "영업 자동화 파이프라인", "sales-agent-harness", "세일즈 에이전트 실행", or wants
  to orchestrate multiple sales automation agents in a coordinated workflow.
  Do NOT use for individual agent operations (invoke the specific sales-*
  skill directly). Do NOT use for the base sales-harness lead-to-deal pipeline
  (use sales-harness). Do NOT use for non-ThakiCloud sales operations.
disable-model-invocation: true
---

# Sales Agent Harness — ThakiCloud Unified Sales Orchestrator

Coordinate all 5 ThakiCloud sales automation agents into cohesive workflows that mirror real deal lifecycles.

## Modes

### Mode 1: `rfp-flow` — RFP-to-Proposal Pipeline

The primary deal-winning pipeline. Takes a customer document and produces a review-ready proposal.

```
┌─────────────────────────────────────────────────────┐
│                    rfp-flow mode                     │
│                                                       │
│  ┌────────────────┐                                   │
│  │ Customer Doc   │                                   │
│  │ (RFP/email/    │                                   │
│  │  transcript)   │                                   │
│  └───────┬────────┘                                   │
│          │                                            │
│          ▼                                            │
│  ┌────────────────────────┐                           │
│  │ Phase 1                │                           │
│  │ sales-rfp-interpreter  │                           │
│  │                        │                           │
│  │ → Requirements table   │                           │
│  │ → Missing questions    │                           │
│  │ → Risk flags           │                           │
│  └───────┬────────────────┘                           │
│          │                                            │
│          ├── risk flags ──────────┐                   │
│          │                        ▼                   │
│          │               ┌────────────────────┐       │
│          │               │ Phase 2            │       │
│          │               │ sales-security-qa  │       │
│          │               │                    │       │
│          │               │ → Answer drafts    │       │
│          │               │ → Escalation flags │       │
│          │               └────────┬───────────┘       │
│          │                        │                   │
│          ├────────────────────────┤                   │
│          │                        │                   │
│          ▼                        ▼                   │
│  ┌────────────────────────────────────────┐           │
│  │ Phase 3                                │           │
│  │ sales-proposal-architect               │           │
│  │                                        │           │
│  │ → Proposal outline + section drafts    │           │
│  │ → Architecture options                 │           │
│  │ → Competitive positioning              │           │
│  │ → Next actions                         │           │
│  └────────────────────────────────────────┘           │
│                                                       │
│  Output: Review-ready proposal package                │
└─────────────────────────────────────────────────────┘
```

**Execution Steps:**

1. Accept customer document (RFP PDF/DOCX, email, or meeting transcript).
2. Launch `sales-rfp-interpreter` — wait for completion.
3. Review risk flags: if security/sovereignty flags exist, launch `sales-security-qa` with those flags as input. If no security flags, skip to Phase 3.
4. Launch `sales-proposal-architect` with requirements table + security Q&A outputs.
5. Present the complete proposal package for human review.
6. Persist all intermediate and final outputs to `outputs/sales-rfp-flow/{date}/{customer-slug}/`.

### Mode 2: `meeting-prep` — Daily Deal Preparation

Standalone mode for daily meeting briefing generation.

```
┌─────────────────────────────────────┐
│          meeting-prep mode           │
│                                       │
│  Calendar Event / Company Name        │
│          │                            │
│          ▼                            │
│  ┌────────────────┐                   │
│  │ sales-deal-prep│                   │
│  │                │                   │
│  │ → 1-page       │                   │
│  │   briefing     │                   │
│  │ → Slack/email  │                   │
│  │   delivery     │                   │
│  └────────────────┘                   │
│                                       │
│  Output: Briefing delivered            │
└─────────────────────────────────────┘
```

**Execution Steps:**

1. Accept calendar event or company name.
2. Launch `sales-deal-prep` directly.
3. Briefing auto-delivers to Slack/email (L3 autonomy).

### Mode 3: `partner-deal` — Partner Orchestration

Standalone mode for managing multi-party partner deals.

```
┌────────────────────────────────────────┐
│          partner-deal mode              │
│                                          │
│  Partner Emails / Meeting Notes / Slack  │
│          │                               │
│          ▼                               │
│  ┌──────────────────────────┐            │
│  │ sales-partner-            │            │
│  │ orchestrator              │            │
│  │                           │            │
│  │ → Action items            │            │
│  │ → Blockers                │            │
│  │ → Deal health card        │            │
│  │ → Notion + Slack          │            │
│  └──────────────────────────┘            │
│                                          │
│  Output: Partner deal status published   │
└────────────────────────────────────────┘
```

**Execution Steps:**

1. Accept partner name or deal identifier.
2. Launch `sales-partner-orchestrator` directly.
3. Deal status published to Notion and Slack.

### Mode 4: `full` — Complete Pipeline

Runs all 5 agents in optimal order for comprehensive deal management.

```
┌──────────────────────────────────────────────────────┐
│                      full mode                        │
│                                                        │
│  ┌──────────────────────────────────────────────┐      │
│  │ Phase 1-3: rfp-flow                          │      │
│  │ (rfp-interpreter → security-qa → proposal)   │      │
│  └──────────────────────┬───────────────────────┘      │
│                         │                              │
│            ┌────────────┴────────────┐                 │
│            ▼                         ▼                 │
│  ┌─────────────────┐      ┌──────────────────────┐    │
│  │ Phase 4          │      │ Phase 5              │    │
│  │ sales-deal-prep  │      │ sales-partner-       │    │
│  │ (if meeting      │      │ orchestrator         │    │
│  │  upcoming)       │      │ (if partner deal)    │    │
│  └─────────────────┘      └──────────────────────┘    │
│                                                        │
│  Output: Full deal package                             │
└──────────────────────────────────────────────────────┘
```

**Execution Steps:**

1. Run `rfp-flow` pipeline (Phases 1-3).
2. In parallel after Phase 3 completes:
   - If upcoming meetings exist for this customer: launch `sales-deal-prep`.
   - If this is a partner deal: launch `sales-partner-orchestrator`.
3. Aggregate all outputs into a consolidated deal package.
4. Persist to `outputs/sales-full-flow/{date}/{customer-slug}/`.

## Mode Selection Logic

```
User Input
    │
    ├─ Has RFP/customer document? ──────────── → rfp-flow
    │
    ├─ Has upcoming meeting + company name? ── → meeting-prep
    │
    ├─ Has partner deal context? ────────────── → partner-deal
    │
    ├─ Has RFP + meeting + partner? ────────── → full
    │
    └─ Ambiguous ──────────────────────────── → Ask user to specify mode
```

## Error Handling

- **Phase failure**: If any phase fails, log the error and continue to the next phase with available data. Do not block the entire pipeline.
- **KB unavailable**: If the security-sovereignty KB is not bootstrapped, `sales-security-qa` uses web search and general knowledge as fallback (with lower confidence scores).
- **Missing inputs**: If downstream skills receive incomplete upstream outputs, they operate on what is available and flag gaps in their output.

## Output Structure

```
outputs/
  sales-rfp-flow/{date}/{customer-slug}/
    01-rfp-interpretation.json
    01-rfp-interpretation.md
    02-security-qa.json
    02-security-qa.md
    03-proposal-draft.docx
    03-proposal-outline.md
    pipeline-summary.md
  sales-deal-prep/{date}/{customer-slug}/
    briefing.md
  sales-partner/{date}/{deal-slug}/
    action-items.json
    deal-health.md
  sales-full-flow/{date}/{customer-slug}/
    [all of the above consolidated]
```

## Relationship to Existing sales-harness

This harness **extends** (does not replace) the existing `sales-harness`:

- `sales-harness`: Lead discovery → enrichment → account research → call prep → outreach → competitive intel → asset generation → deal tracking (19 skills)
- `sales-agent-harness`: RFP interpretation → security Q&A → proposal architecture → deal preparation → partner orchestration (5 ThakiCloud-specific skills)

Use `sales-harness` for **lead-to-qualified-opportunity** workflows.
Use `sales-agent-harness` for **opportunity-to-proposal** workflows.
