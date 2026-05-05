---
name: rr-cs-support
version: 1.0.0
description: >-
  Role Replacement Case Study: Customer Support Lead — Pipeline + Supervisor pattern
  for the full ticket lifecycle from triage through resolution, knowledge capture, and
  batch feedback analysis with RICE-scored executive reports. Thin harness composing
  customer-support-harness, customer-feedback-processor, and 5 kwp-customer-support-*
  skills into a unified CS-lead role pipeline with MemKraft-powered ticket history,
  proactive trend detection, SLA tracking, and automated Slack escalation routing.
tags: [role-replacement, harness, customer-support, feedback, RICE, ticket-lifecycle]
triggers:
  - rr-cs-support
  - CS support replacement
  - customer support automation
  - CS lead replacement
  - support ticket lifecycle
  - feedback to action pipeline
  - 고객 지원 대체
  - CS 역할 자동화
  - CS 리드 대체
  - 티켓 라이프사이클 자동화
  - 피드백 액션 파이프라인
do_not_use:
  - Individual support operations without lifecycle context (invoke kwp-customer-support-* directly)
  - Sales outreach or lead management (use sales-harness)
  - General feedback mining without CS context (use feedback-miner)
  - Internal engineering incidents (use incident-to-improvement)
  - Product feature spec writing (use pm-execution)
  - Marketing content from feedback (use content-repurposing-engine)
composes:
  - customer-support-harness
  - customer-feedback-processor
  - kwp-customer-support-ticket-triage
  - kwp-customer-support-response-drafting
  - kwp-customer-support-customer-research
  - kwp-customer-support-escalation
  - kwp-customer-support-knowledge-management
  - feedback-miner
  - evaluation-engine
  - anthropic-docx
  - visual-explainer
  - memkraft
  - ai-context-router
  - decision-router
  - sentence-polisher
  - kb-ingest
---

# Role Replacement: Customer Support Lead

A human CS lead handles ticket triage, response drafting, escalation packaging,
knowledge base maintenance, SLA monitoring, trend detection across ticket streams,
and periodic feedback analysis for the product team. This thin harness replicates
the full CS lead role by orchestrating existing pipeline and individual CS skills
with MemKraft-powered ticket history, proactive pattern detection, and automated
executive feedback reporting.

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    rr-cs-support (Orchestrator)                   │
│                                                                  │
│  Phase 0: MemKraft Context Pre-load                              │
│  ┌────────────────┐                                              │
│  │ ai-context-     │ ← Load: prior ticket patterns, known issues,│
│  │ router          │   escalation history, customer entity map    │
│  └──────┬─────────┘                                              │
│         ▼                                                        │
│  Phase 1: Ticket Lifecycle Pipeline                              │
│  ┌────────────────────────────────────────────────────────┐      │
│  │ customer-support-harness (Pipeline + Supervisor)        │      │
│  │                                                        │      │
│  │  1a. Triage     ← kwp-cs-ticket-triage                │      │
│  │      │                                                 │      │
│  │      ├─── P1 ──→ 1e. Escalation (fast path)           │      │
│  │      │                                                 │      │
│  │      ▼ (P2-P4)                                         │      │
│  │  1b. Research   ← kwp-cs-customer-research             │      │
│  │      │            + MemKraft ticket history lookup      │      │
│  │      ▼                                                 │      │
│  │  1c. Response   ← kwp-cs-response-drafting             │      │
│  │      │            + sentence-polisher                   │      │
│  │      ▼                                                 │      │
│  │  1d. KB Update  ← kwp-cs-knowledge-management          │      │
│  │      │            + kb-ingest (to project KB)           │      │
│  │      ▼                                                 │      │
│  │  1e. Escalation ← kwp-cs-escalation (conditional)      │      │
│  └────────────────────────────────────────────────────────┘      │
│         ▼                                                        │
│  Phase 2: Pattern Detection & Trend Alert                        │
│  ┌────────────────┐                                              │
│  │ Trend Detector  │ ← Scan Phase 1 outputs + MemKraft history   │
│  │ (inline logic)  │   for: recurring issues (3+), SLA breaches, │
│  │                 │   escalation spikes, new failure patterns    │
│  └──────┬─────────┘                                              │
│         ▼                                                        │
│  Phase 3: Batch Feedback Processing (weekly/on-demand)           │
│  ┌────────────────────────────────────────────────────────┐      │
│  │ customer-feedback-processor                             │      │
│  │  3a. Ingest    ← Multi-channel (app reviews, surveys,  │      │
│  │                   tickets, NPS, Slack)                   │      │
│  │  3b. Classify  ← Topic + sentiment + urgency            │      │
│  │  3c. Score     ← RICE framework via evaluation-engine   │      │
│  │  3d. Synthesize← Theme clustering + trend detection     │      │
│  │  3e. Report    ← anthropic-docx + visual-explainer      │      │
│  │  3f. Deliver   ← Notion + Slack                         │      │
│  └────────────────────────────────────────────────────────┘      │
│         ▼                                                        │
│  Phase 4: Decision Routing & Escalation                          │
│  ┌────────────────┐                                              │
│  │ decision-router │ ← Route CRITICAL findings:                  │
│  │                 │   Product gaps → #효정-의사결정               │
│  │                 │   Escalation → #7층-리더방                   │
│  └──────┬─────────┘                                              │
│         ▼                                                        │
│  Phase 5: MemKraft Write-back & Session Close                    │
│  ┌────────────────┐                                              │
│  │ memkraft-ingest │ ← Persist: new ticket patterns,             │
│  │                 │   customer entity updates, trend shifts,     │
│  │                 │   escalation outcomes, KB gap signals        │
│  └────────────────┘                                              │
└──────────────────────────────────────────────────────────────────┘
```

## Prerequisites

| Dependency | Purpose | Check Command |
|---|---|---|
| Slack posting | Post triage results, escalations, feedback summaries | Verify `python3 scripts/slack_post_message.py` + `SLACK_USER_TOKEN` |
| Notion MCP | Publish KB articles and feedback reports | Verify `notion_create_page` tool available |
| `anthropic-docx` deps | Generate executive feedback reports | `python -c "import docx"` |
| `python-docx` | DOCX generation for feedback reports | `pip show python-docx` |
| MemKraft store | `memory/memkraft/` directory exists | `ls memory/memkraft/` |
| KB topics dir | `knowledge-bases/` directory exists | `ls knowledge-bases/` |

## Pipeline Output Protocol

All outputs persist to `outputs/rr-cs-support/{YYYY-MM-DD}/`.

| Phase | Stage Name | Output File | Format |
|---|---|---|---|
| 0 | MemKraft Context | `phase-0-memkraft-context.json` | JSON |
| 1a | Triage | `phase-1a-triage.md` | Markdown |
| 1b | Research | `phase-1b-research.md` | Markdown |
| 1c | Response Draft | `phase-1c-response-draft.md` | Markdown |
| 1d | KB Update | `phase-1d-kb-update.md` | Markdown |
| 1e | Escalation | `phase-1e-escalation.md` | Markdown |
| 2 | Trend Alert | `phase-2-trend-alert.json` | JSON |
| 3 | Feedback Report | `phase-3-feedback-report.docx` | DOCX |
| 3 | Feedback Dashboard | `phase-3-feedback-dashboard.html` | HTML |
| 3 | RICE Scores | `phase-3-rice-scores.tsv` | TSV |
| 4 | Decision Items | `phase-4-decision-items.json` | JSON |
| 5 | MemKraft Delta | `phase-5-memkraft-delta.json` | JSON |
| — | Manifest | `manifest.json` | JSON |

## Execution Steps

### Phase 0: MemKraft Context Pre-load

Query `ai-context-router` for relevant prior context before processing any ticket:

```
Query topics:
  - "recent customer support tickets and patterns"
  - "known issues and active bugs"
  - "escalation history for this customer" (if customer identified)
  - "SLA breach patterns"
  - "product areas with recurring complaints"

Expected return:
  - Prior ticket patterns (recurring issues, resolution templates)
  - Customer entity data (tier, history, sentiment trajectory)
  - Active known issues list
  - SLA performance baseline
```

Save context to `phase-0-memkraft-context.json`. This context enriches every
subsequent phase — triage gets faster resolution suggestions, research gets
customer history, response drafting gets tone guidance from prior interactions.

### Phase 1: Ticket Lifecycle Pipeline

Delegate to `customer-support-harness` in `full` mode. The harness manages the
Pipeline + Supervisor pattern internally:

**Phase 1a — Triage** (`kwp-customer-support-ticket-triage`):
- Categorize by root cause (Bug / How-to / Feature Request / Billing / Account / Integration / Security / Data / Performance)
- Assign priority P1-P4 with mood detection (frustrated / anxious / neutral / positive)
- Calculate urgency score (1-5) and SLA deadline
- **MemKraft enhancement**: Cross-reference triage output against MemKraft's `known_issues` list — if the issue matches a known pattern, annotate with the prior resolution and estimated fix time

**Supervisor gate**: P1 tickets fast-path to Phase 1e (Escalation). P2 tickets run full pipeline + Phase 1e.

**Phase 1b — Research** (`kwp-customer-support-customer-research`):
- Search documentation, knowledge bases, and connected sources
- **MemKraft enhancement**: Retrieve this customer's prior ticket history from MemKraft entity store. Include prior mood trajectory, resolution satisfaction, and recurring themes. Flag if the customer has escalated before.
- Produce confidence-scored answer with source citations

**Phase 1c — Response Drafting** (`kwp-customer-support-response-drafting`):
- Draft empathetic response adapted to channel, urgency, and mood
- Apply `sentence-polisher` for Korean text quality
- **MemKraft enhancement**: If MemKraft contains a prior successful response template for this issue type, use it as the base draft and adapt for the current customer

**Phase 1d — KB Update** (`kwp-customer-support-knowledge-management`):
- Determine if the resolved ticket reveals a KB gap
- Write or update KB article following the structure standards (how-to / troubleshooting / FAQ / known issue)
- **Project KB integration**: Ingest the new KB article into the project's LLM Knowledge Base via `kb-ingest` with topic `customer-support`
- Verify searchability with keyword check

**Phase 1e — Escalation** (`kwp-customer-support-escalation`, conditional):
- Package escalation brief with reproduction steps, business impact, and customer context
- Quantify impact across 6 dimensions: Breadth, Depth, Duration, Revenue, Reputation, Contractual
- Route to correct tier: L1→L2, L2→Engineering, L2→Product, Any→Security, Any→Leadership
- Post escalation to Slack with structured format

### Phase 2: Pattern Detection & Trend Alert

After Phase 1 completes, scan today's ticket outputs + MemKraft historical data
for emerging patterns. This is the proactive intelligence a CS lead provides:

```
Trend Detection Rules:
  1. RECURRING ISSUE: Same root cause appears in 3+ tickets within 7 days
     → Alert: "Potential systematic issue — consider engineering escalation"
  2. SLA BREACH PATTERN: 2+ SLA breaches in same product area within 14 days
     → Alert: "SLA health degrading in {area} — review staffing/process"
  3. ESCALATION SPIKE: Escalation rate exceeds 20% of triaged tickets
     → Alert: "Escalation rate abnormal — check for product regression"
  4. SENTIMENT SHIFT: Customer satisfaction trending negative (3+ frustrated in a row)
     → Alert: "Sentiment degradation detected — proactive outreach recommended"
  5. NEW FAILURE MODE: Ticket describes a symptom not matching any known pattern
     → Alert: "Novel issue detected — potential undiscovered bug"
```

Save alerts to `phase-2-trend-alert.json`. Post critical alerts to Slack immediately.

### Phase 3: Batch Feedback Processing

Run weekly or on-demand. Delegates entirely to `customer-feedback-processor`:

1. **Ingest**: Collect feedback from app store reviews, surveys, support ticket exports, NPS comments, social media, Slack feedback channels
2. **Classify**: Topic cluster + sentiment + urgency + feature area + customer tier
3. **Score**: RICE framework (Reach × Impact × Confidence / Effort) via `evaluation-engine`
4. **Synthesize**: Top 5 themes with representative quotes, trend indicators, and RICE scores
5. **Report**: Executive `.docx` via `anthropic-docx` + visual dashboard via `visual-explainer`
6. **Deliver**: Push themes to Notion, post summary to Slack

**MemKraft enhancement for feedback processing**:
- Before scoring, query MemKraft for historical RICE scores of the same themes
- Detect score trajectory: themes with increasing RICE scores across weeks get a "Growing" trend tag
- Include "last week's top 5 vs this week's top 5" comparison in the executive report

### Phase 4: Decision Routing

Invoke `decision-router` for items requiring human decisions:

| Signal Type | Route | Channel |
|---|---|---|
| Product gap from feedback (RICE > 500) | Personal decision | #효정-의사결정 |
| Escalation requiring leadership attention | Team/CTO decision | #7층-리더방 |
| SLA policy change recommendation | Team decision | #7층-리더방 |
| New known issue announcement | Informational | #h-report |

### Phase 5: MemKraft Write-back & Session Close

Persist today's learnings to MemKraft:

```json
{
  "ticket_patterns": [
    {
      "pattern_id": "recurring-auth-timeout",
      "frequency": 5,
      "resolution": "Clear session cache + re-auth",
      "first_seen": "2026-04-08",
      "last_seen": "2026-04-15"
    }
  ],
  "customer_entities": [
    {
      "customer_id": "acme-corp",
      "tier": "enterprise",
      "sentiment_trajectory": "improving",
      "last_interaction": "2026-04-15",
      "open_tickets": 1
    }
  ],
  "kb_gaps_identified": ["OAuth PKCE flow troubleshooting", "Rate limit error codes"],
  "trend_alerts_fired": 2,
  "escalation_count": 1,
  "feedback_themes_updated": true,
  "sla_performance": {
    "p1_met": true,
    "p2_met": true,
    "p3_breached": 1
  }
}
```

Write consolidated Slack summary to #효정-할일:
- Main message: Today's ticket count, resolution rate, SLA performance, escalations
- Thread 1: Trend alerts and pattern detections
- Thread 2: KB articles created/updated
- Thread 3: Feedback report highlights (if Phase 3 ran)

## Memory Configuration

### HOT (Session-Critical)
- Current ticket content and customer details
- Active triage priority and SLA countdown
- Escalation state and routing decisions
- Today's trend detection results

### WARM (Cross-Session via MemKraft)
- Customer entity map (tier, history, sentiment trajectory)
- Recurring issue patterns with resolution templates
- SLA performance baselines by product area
- RICE score trajectories for feedback themes
- Escalation outcome history (which escalations led to fixes)
- Successful response templates by issue category

### Knowledge (Persistent KB)
- Project LLM Knowledge Base topic: `customer-support`
- KB article index with searchability scores
- Known issues registry with status tracking
- Product area taxonomy and routing rules

## Slack Configuration

| Content | Channel | Format |
|---|---|---|
| Daily CS summary | #효정-할일 | 3-message thread |
| P1 escalation alert | #7층-리더방 | Immediate, structured |
| Product gap decisions | #효정-의사결정 | Decision-router format |
| Weekly feedback report | #h-report | Summary + Drive link |
| Trend alerts (critical) | #효정-할일 | Inline with daily summary |

## Error Recovery

| Failure | Recovery Strategy |
|---|---|
| Phase 0 (MemKraft) fails | Proceed without history — log degraded mode. All phases still functional. |
| Phase 1a (Triage) fails | Cannot proceed with ticket lifecycle. Retry with raw ticket text. |
| Phase 1b (Research) fails | Skip to Phase 1c with limited context. Flag "low-confidence" on response. |
| Phase 1c (Response) fails | Return research results only. Human drafts response manually. |
| Phase 1d (KB Update) fails | Log KB gap for next session. Ticket resolution still valid. |
| Phase 1e (Escalation) fails | Post raw escalation to Slack manually. Never silently drop a P1. |
| Phase 2 (Trend) fails | Non-critical. Log and continue to Phase 3. |
| Phase 3 (Feedback) fails at any sub-phase | Prior sub-phases remain valid. Retry from failed sub-phase. |
| Phase 4 (Decision) fails | Decisions queue to `_workspace/pending-decisions.json` for next run. |
| Phase 5 (MemKraft write) fails | Retry once. If persistent, save delta to `_workspace/memkraft-pending.json`. |
| Slack MCP unavailable | Write all messages to `_workspace/slack-queue/`. Retry when available. |
| Notion MCP unavailable | Save KB articles locally. Retry upload next session. |

## Security & Compliance Rules

1. **PII Handling**: Strip customer names, emails, account IDs, and payment info from all outputs, KB articles, feedback reports, and Slack messages. Use anonymized identifiers.
2. **Response Approval Gate**: AI-drafted customer responses are NEVER sent automatically. All responses require human review and approval before sending.
3. **Escalation Integrity**: P1 tickets MUST be escalated. The system never downgrades a P1 or suppresses an escalation.
4. **Data Retention**: Ticket content in `_workspace/` is ephemeral. Only anonymized patterns and KB articles persist.
5. **Feedback Anonymization**: Customer quotes in feedback reports must be anonymized. Remove names, companies, and identifying details.

## Honest Reporting

- Report outcomes faithfully — never claim all phases passed when any failed
- Never suppress errors, partial results, or skipped phases
- Surface unexpected findings even if they complicate the narrative
- If a phase produces no actionable output, say so explicitly

## Coordinator Synthesis

- Do not reconstruct phase outputs from chat context — always read from persisted files
- Each phase dispatch includes a purpose statement explaining the expected transformation
- File paths and line numbers must be specific, not inferred
- Never delegate with vague instructions like "analyze this" — provide concrete specs

## Subagent Contract

Every subagent dispatch MUST include:
1. **Purpose statement** — one sentence explaining why this subagent exists
2. **Absolute file paths** — all input/output paths as absolute paths
3. **Return contract** — subagent must return JSON: `{"status": "ok|error", "file": "<output_path>", "summary": "<1-line>"}`
4. Load-bearing outputs must be written to disk, not passed via chat context

## Operational Runbook

### Daily Ticket Processing
```bash
# 1. Process incoming tickets (run per ticket or batch)
# Invoke rr-cs-support with ticket content
# System runs Phases 0→1→2→4→5

# 2. Check outputs
ls outputs/rr-cs-support/$(date +%Y-%m-%d)/
cat outputs/rr-cs-support/$(date +%Y-%m-%d)/manifest.json

# 3. Review and approve response drafts
cat outputs/rr-cs-support/$(date +%Y-%m-%d)/phase-1c-response-draft.md
```

### Weekly Feedback Analysis
```bash
# Run batch feedback processing (Phase 3)
# Invoke rr-cs-support with mode: feedback
# Provide: feedback sources (CSV paths, URLs, channel names)

# Review executive report
open outputs/rr-cs-support/$(date +%Y-%m-%d)/phase-3-feedback-report.docx
open outputs/rr-cs-support/$(date +%Y-%m-%d)/phase-3-feedback-dashboard.html
```

### SLA Health Check
```bash
# Query MemKraft for SLA performance baseline
# Compare today's SLA metrics against 30-day average
# Trigger alerts if breach rate exceeds 10%
```

## Comparison: Human CS Lead vs. rr-cs-support

| Dimension | Human CS Lead | rr-cs-support |
|---|---|---|
| Ticket triage speed | 5-15 min per ticket | < 30 sec per ticket |
| Pattern detection | Relies on memory and experience | Systematic scan across all tickets + MemKraft history |
| SLA tracking | Manual spreadsheet or dashboard | Automated with breach prediction |
| KB article creation | Post-resolution, often deferred | Immediate, integrated into resolution flow |
| Feedback analysis | Monthly, manual categorization | Weekly, RICE-scored with trend tracking |
| Escalation quality | Varies by experience | Consistent 6-dimension impact assessment |
| Cross-ticket correlation | Limited by human memory | Full MemKraft entity + pattern correlation |
| Customer history recall | Depends on CRM lookup | Automatic MemKraft entity retrieval |
| Shift handoff | Verbal or written notes | Persistent MemKraft state — zero handoff loss |
| Still requires human | — | Response approval, complex judgment calls, empathy in sensitive cases |

## Examples

### Example 1: Daily ticket batch processing

User says: "Process today's support tickets"

Actions:
1. Phase 0: Load MemKraft context (known issues, customer entities, SLA baseline)
2. Phase 1: Run customer-support-harness in `full` mode for each ticket
   - Triage with mood + urgency scoring, cross-reference known issues
   - Research with customer history from MemKraft
   - Draft response with sentence polishing
   - Update KB if resolution reveals a gap
   - Escalate P1/P2 tickets with structured packages
3. Phase 2: Scan all triaged tickets for recurring patterns and SLA health
4. Phase 4: Route decisions (product gaps, escalations)
5. Phase 5: Write-back to MemKraft, post daily summary to Slack

### Example 2: Weekly feedback report

User says: "고객 피드백 분석 보고서 생성해줘"

Actions:
1. Phase 0: Load prior RICE score trajectories from MemKraft
2. Phase 3: Run customer-feedback-processor
   - Ingest from App Store, NPS survey, Zendesk export, Slack #feedback
   - Classify by topic + sentiment, score with RICE
   - Compare this week's top 5 themes vs last week's (from MemKraft)
   - Generate Korean executive .docx + visual HTML dashboard
3. Phase 4: Route high-RICE product gaps to #효정-의사결정
4. Phase 5: Update MemKraft with new RICE baselines

### Example 3: P1 critical escalation

User says: "Production is down for enterprise customer Acme Corp"

Actions:
1. Phase 0: MemKraft lookup — Acme Corp is enterprise tier, $200K ARR, prior escalation history
2. Phase 1a: Triage → P1 Critical, mood: anxious, urgency: 5/5
3. Phase 1e: Supervisor fast-paths to Escalation
   - Package: reproduction steps, customer context from MemKraft, business impact ($200K ARR at risk)
   - Post immediately to #7층-리더방 and Slack engineering channel
4. Phase 2: Flag as potential systematic issue if 2+ other tickets share symptoms
5. Phase 5: Update Acme Corp entity in MemKraft with escalation record
