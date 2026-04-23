---
name: sales-deal-prep
version: 1.0.0
description: >
  Generate ThakiCloud-customized meeting briefings with company context,
  deal status, expected security/sovereignty questions, talking points,
  and red flags. Wraps kwp-sales-call-prep with ThakiCloud-specific
  enrichment: expected on-prem/sovereignty questions from sales-security-qa,
  previous RFP analysis context from sales-rfp-interpreter, and segment-
  aware talking points. Auto-delivers 30 minutes before meetings.
  Use when the user asks to "prepare for meeting", "deal prep",
  "meeting briefing", "call prep", "미팅 준비", "딜 준비",
  "브리핑 생성", "sales-deal-prep", "미팅 브리핑", or has
  an upcoming customer meeting requiring preparation.
  Do NOT use for general calendar briefing (use calendar-daily-briefing).
  Do NOT use for non-sales meeting prep (use kwp-sales-call-prep directly).
  Do NOT use for proposal drafting (use sales-proposal-architect).
  Do NOT use for partner deal tracking (use sales-partner-orchestrator).
tags: [sales, deal-prep, meeting, briefing, call-prep, thakicloud]
triggers:
  - "prepare for meeting"
  - "deal prep"
  - "meeting briefing"
  - "call prep"
  - "meeting preparation"
  - "sales-deal-prep"
  - "미팅 준비"
  - "딜 준비"
  - "브리핑 생성"
  - "미팅 브리핑"
  - "고객 미팅 준비"
  - "콜 준비"
do_not_use:
  - "General calendar briefing without sales context (use calendar-daily-briefing)"
  - "Non-ThakiCloud meeting prep (use kwp-sales-call-prep directly)"
  - "Proposal drafting (use sales-proposal-architect)"
  - "Partner deal orchestration (use sales-partner-orchestrator)"
  - "Post-meeting analysis (use meeting-digest)"
composes:
  - kwp-sales-call-prep
  - kwp-sales-account-research
  - kwp-common-room-call-prep
  - sales-security-qa
metadata:
  author: "thaki"
  category: "sales-agents/deal-prep"
  autonomy: "L3"
---

# Sales Deal Preparation Agent

Generate ThakiCloud-specific 1-page meeting briefings that combine company intelligence, deal context, expected security questions, and segment-aware talking points — auto-delivered 30 minutes before each meeting.

## When to Use

- Upcoming customer meeting (detected from calendar or user request)
- Sales needs context on a customer before a call
- Deal review preparation requiring consolidated context
- Follow-up meeting needing history from previous interactions

## Briefing Template

```markdown
# 📋 Meeting Briefing: [Customer Name]
**Date**: [meeting date/time] | **Attendees**: [list]

## 🏢 Company Snapshot
- Industry / Size / Funding stage
- Tech stack signals (from public data)
- Recent news / press releases (last 30 days)

## 📊 Deal Context
- Current stage: [stage from CRM or previous interactions]
- Days in stage: [N days]
- Previous interactions summary
- Open requirements / pending items

## 🔐 Expected Security Questions
[Auto-generated from sales-security-qa based on customer segment]
- Q1: [likely question] → Quick answer + evidence
- Q2: [likely question] → Quick answer + evidence
- Q3: [likely question] → Quick answer + evidence

## 🎯 Talking Points
1. [Segment-specific value message #1]
2. [Segment-specific value message #2]
3. [Segment-specific value message #3]

## 🔴 Red Flags
- [Risk or concern to be aware of]
- [Competitive threat or objection expected]

## ✅ Recommended Next Actions
- [What to propose at end of meeting]
- [Follow-up commitment to offer]
```

## Pipeline

```
Calendar Event / User Request
       │
       ▼
┌──────────────────────────────────────────┐
│  Phase 1: Context Assembly (parallel)     │
│  ┌────────────┐  ┌────────────────────┐  │
│  │ kwp-sales- │  │ kwp-sales-account- │  │
│  │ call-prep  │  │ research           │  │
│  └─────┬──────┘  └────────┬───────────┘  │
│        │                  │              │
│  ┌─────┴──────┐  ┌───────┴────────────┐ │
│  │ kwp-common │  │ Previous RFP/      │ │
│  │ room-call  │  │ proposal outputs   │ │
│  │ -prep      │  │ (if available)     │ │
│  └────────────┘  └────────────────────┘  │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│  Phase 2: ThakiCloud Enrichment           │
│  - Detect customer segment                │
│  - Generate expected security questions   │
│    via sales-security-qa patterns         │
│  - Select segment-specific talking points │
│  - Identify red flags from deal history   │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│  Phase 3: Briefing Assembly               │
│  - Merge all context into 1-page format   │
│  - Prioritize most actionable items       │
│  - Post to Slack / email                  │
└──────────────────────────────────────────┘
```

## Execution Instructions

### Step 1 — Trigger Detection

1. If invoked with a calendar event: extract customer name from event title, attendees from participant list, meeting type from event description. If the event title lacks a company name, infer from attendee email domains (e.g., `@samsung.com` → Samsung).
2. If invoked with a company name: treat as manual prep request.
3. Check `outputs/sales-rfp/` and `outputs/sales-proposals/` for previous analysis on this customer.
4. For first-touch meetings (no prior data): explicitly note "first interaction — no deal history" in the Deal Context section rather than leaving it blank or generating placeholder content.

### Step 2 — Parallel Context Assembly

Launch in parallel:
1. `kwp-sales-call-prep`: Core call preparation with account context and suggested agenda.
2. `kwp-sales-account-research`: Deep company research — news, tech stack, funding, leadership.
3. `kwp-common-room-call-prep` (if Common Room is configured): Signal enrichment from community data.
4. Read previous `sales-rfp-interpreter` and `sales-proposal-architect` outputs for this customer if they exist.

### Step 3 — ThakiCloud Enrichment

1. **Segment Detection**: Infer customer segment from company size, industry, and previous requirement patterns.
2. **Expected Security Questions**: Based on the detected segment, generate the top 3-5 security questions this customer is likely to ask, using patterns from `sales-security-qa` and the security-sovereignty KB.
3. **Talking Points**: Select 3 segment-appropriate talking points from the segment templates in `sales-proposal-architect`.
4. **Red Flags**: Identify risks from deal history — stalled stages, competitive mentions, unresolved requirements, pricing concerns.

### Step 4 — Assemble and Deliver

1. Merge all inputs into the 1-page briefing template.
2. Cap the briefing at approximately 500 words — brevity is critical for pre-meeting consumption.
3. If fewer than 2 of 4 context sources returned data, add a prominent "⚠ Low Confidence" banner at the top of the briefing.
4. Persist to `outputs/sales-deal-prep/{date}/{customer-slug}/`.
5. Deliver via Slack DM or channel (preferred) or email. If Slack delivery fails, fall back to persisting on disk and notifying the user — never let delivery failure block the entire pipeline.

## Constraints

- Briefing must not exceed ~500 words — brevity is critical for pre-meeting consumption
- Do not include confidential internal assessments (e.g., "this deal is unlikely to close") in the briefing — keep factual
- Expected security questions must be drawn from the security-sovereignty KB patterns, not fabricated
- Red flags must cite specific evidence (e.g., "no email response for 14 days") not vague concerns
- Do not suggest specific pricing or discount levels in talking points

## Gotchas

- Calendar event titles often lack the company name — the skill may need to extract it from attendee email domains or ask the user
- `kwp-common-room-call-prep` requires Common Room to be configured; skip gracefully if unavailable rather than failing the entire briefing
- Previous RFP/proposal outputs may not exist for new customers — the enrichment phase must handle empty lookups without generating placeholder content
- Segment detection from company research can be wrong for conglomerates with multiple business units — verify when the customer has both startup and enterprise divisions
- Slack delivery failures (channel not found, token expired) should not block briefing persistence to disk

## Verification

Before delivering the briefing:
1. Company name and meeting date are correctly populated (not placeholder text)
2. At least 2 of 4 context sources returned data (call-prep, account-research, common-room, previous outputs)
3. Expected security questions reference real KB content, not generic templates
4. Briefing total word count is under 600 words

## Autonomy Level: L3

- **Auto**: Context assembly, enrichment, briefing generation, Slack/email delivery
- **Human Review**: Optional — briefings are informational, not customer-facing
- **Never Auto**: Making commitments on behalf of sales, sending briefings to customers

## Integration Points

- **Upstream**: Calendar events, previous outputs from `sales-rfp-interpreter` and `sales-proposal-architect`
- **Downstream**: Post-meeting notes feed back into deal context for future briefings
- **Harness**: Invoked standalone in `meeting-prep` mode of `sales-agent-harness`
