---
name: customer-support-harness
description: >-
  Customer Support domain harness orchestrator — Pipeline + Supervisor pattern
  for ticket lifecycle from triage through resolution to knowledge capture.
  Auto-escalates P1 tickets. Use when the user asks to "run support pipeline",
  "customer support harness", "ticket lifecycle", "고객 지원 하네스", "CS 파이프라인",
  "customer-support-harness", or wants end-to-end support operations. Do NOT
  use for individual support operations (invoke kwp-customer-support-*
  directly). Do NOT use for sales outreach (use sales-harness).
---

# Customer Support Harness Orchestrator

Pipeline + Supervisor pattern for the full ticket lifecycle. The Supervisor layer monitors ticket priority and auto-routes P1 tickets to immediate escalation.

## When to Use

- Processing a customer ticket from initial receipt through resolution and KB update
- Batch triage of incoming support tickets
- Building escalation packages for engineering or product teams
- Analyzing resolved tickets to update the knowledge base
- Any "handle this support ticket end-to-end" request

## Architecture

```
Incoming Ticket
       │
       ▼
┌──────────────┐
│ Phase 1      │ ← Triage: categorize, prioritize (P1-P4), route
│ TRIAGE       │   kwp-customer-support-ticket-triage
└──────┬───────┘
       │
       ├─── P1 ──→ FAST PATH: Skip to Phase 5 (Escalation)
       │
       ▼ (P2-P4)
┌──────────────┐
│ Phase 2      │ ← Research: search docs, KB, account context
│ RESEARCH     │   kwp-customer-support-customer-research
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 3      │ ← Response: draft reply adapted to channel/urgency
│ RESPOND      │   kwp-customer-support-response-drafting
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 4      │ ← Knowledge: update KB from resolved ticket
│ KB UPDATE    │   kwp-customer-support-knowledge-management
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 5      │ ← Escalation (if needed): package for engineering
│ ESCALATE     │   kwp-customer-support-escalation
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 6      │ ← Optional: batch feedback analysis
│ FEEDBACK     │   customer-feedback-processor
└──────────────┘
```

## Supervisor Logic

The Supervisor layer inspects triage output and applies routing rules:

| Priority | Route | Rationale |
|----------|-------|-----------|
| **P1** (critical outage) | Fast-path to Phase 5 (Escalation) | Immediate engineering involvement required |
| **P2** (major impact) | Full pipeline (Phase 2→3→4) + Phase 5 | Research and respond, but also escalate |
| **P3** (moderate) | Full pipeline (Phase 2→3→4) | Standard support flow |
| **P4** (low) | Phase 2→3, skip Phase 4 if FAQ | May use canned response |

## Modes

| Mode | Phases | Use Case |
|------|--------|----------|
| `triage` | 1 only | Triage and route incoming tickets |
| `respond` | 2→3 | Research context and draft a response |
| `escalate` | 1→5 | Triage and build escalation package |
| `kb` | 4 only | Create KB article from a resolved ticket |
| `feedback` | 6 only | Batch process customer feedback |
| `full` | 1→2→3→4→(5) | Complete lifecycle (escalation if needed) |

Default mode: `full`

## Pipeline

### Phase 1: Ticket Triage

Categorize the issue, assign priority (P1-P4), and recommend routing.

**Skill**: `kwp-customer-support-ticket-triage`
**Input**: Ticket content (email, chat, form submission)
**Output**: `outputs/customer-support-harness/{date}/phase1-triage.md`

Output includes: issue category, priority level, recommended team, severity assessment.

### Phase 2: Customer Research

Search documentation, knowledge bases, and connected sources for relevant context.

**Skill**: `kwp-customer-support-customer-research`
**Input**: Phase 1 triage result + ticket content
**Output**: `outputs/customer-support-harness/{date}/phase2-research.md`

Output includes: relevant KB articles, account context, confidence-scored answer, prior ticket history.

### Phase 3: Response Drafting

Draft a professional, empathetic response adapted to the situation, urgency, and channel.

**Skill**: `kwp-customer-support-response-drafting`
**Input**: Phase 2 research findings
**Output**: `outputs/customer-support-harness/{date}/phase3-response-draft.md`

Output includes: response text, tone notes, suggested follow-up actions.

### Phase 4: Knowledge Management

Write or update KB articles from the resolved support interaction.

**Skill**: `kwp-customer-support-knowledge-management`
**Input**: Phase 1-3 outputs (full resolution context)
**Output**: `outputs/customer-support-harness/{date}/phase4-kb-update.md`

Covers: how-to guides, troubleshooting docs, FAQ entries from resolved tickets.

### Phase 5: Escalation (Conditional)

Structure and package the escalation for engineering, product, or leadership.

**Skill**: `kwp-customer-support-escalation`
**Input**: Triage result + research findings + business impact
**Output**: `outputs/customer-support-harness/{date}/phase5-escalation.md`

Output includes: reproduction steps, business impact statement, customer context, recommended severity.

### Phase 6: Feedback Analysis (Optional)

Batch process customer feedback from multiple channels.

**Skill**: `customer-feedback-processor`
**Input**: Feedback data from app stores, surveys, support tickets, NPS
**Output**: `outputs/customer-support-harness/{date}/phase6-feedback-report.md`

## Skill Routing Table

| User Intent | Routed Skill | Phase |
|-------------|-------------|-------|
| "Triage this ticket" | `kwp-customer-support-ticket-triage` | 1 |
| "Research customer issue" | `kwp-customer-support-customer-research` | 2 |
| "Draft a response" | `kwp-customer-support-response-drafting` | 3 |
| "Update the KB" | `kwp-customer-support-knowledge-management` | 4 |
| "Escalate to engineering" | `kwp-customer-support-escalation` | 5 |
| "Analyze customer feedback" | `customer-feedback-processor` | 6 |

## Error Handling

| Error | Recovery |
|-------|----------|
| Phase N fails | Prior phase outputs remain valid. Fix and re-run from Phase N. |
| P1 ticket detected | Supervisor fast-paths to Phase 5; Phases 2-4 skipped |
| KB search returns no results | Proceed with response drafting using general knowledge; flag KB gap |
| Response draft rejected by user | Loop back to Phase 3 with feedback for redraft |

## Output Artifacts

| Phase | Stage Name | Output File | Skip Flag |
|-------|-----------|-------------|-----------|
| 1 | Triage | `outputs/customer-support-harness/{date}/phase1-triage.md` | `skip-triage` |
| 2 | Research | `outputs/customer-support-harness/{date}/phase2-research.md` | `skip-research` |
| 3 | Response | `outputs/customer-support-harness/{date}/phase3-response-draft.md` | `skip-respond` |
| 4 | KB Update | `outputs/customer-support-harness/{date}/phase4-kb-update.md` | `skip-kb` |
| 5 | Escalation | `outputs/customer-support-harness/{date}/phase5-escalation.md` | `skip-escalate` |
| 6 | Feedback | `outputs/customer-support-harness/{date}/phase6-feedback-report.md` | `skip-feedback` |

## Workspace Convention

- Intermediate files: `_workspace/customer-support-harness/`
- Final deliverables: `outputs/customer-support-harness/{date}/`

## Constraints

- P1 tickets MUST be escalated — the Supervisor never downgrades a P1
- Every resolved ticket should trigger a KB update consideration (Phase 4)
- Response drafts require user approval before sending to customers
- Escalation packages must include reproduction steps and business impact
- PII in ticket content must be handled per data governance policies
