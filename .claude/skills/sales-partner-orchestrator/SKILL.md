---
name: sales-partner-orchestrator
description: >-
  Track and orchestrate MSP/partner co-proposal deals by extracting action
  items from partner emails, meeting notes, and Slack threads. Identifies
  blockers, ownership gaps, and follow-up lapses across multi-party deals
  (ThakiCloud + MSP partner + end customer). Produces structured action item
  lists, partner deal health cards, and blocker escalation suggestions. Use
  when the user asks to "track partner deal", "partner orchestration",
  "co-proposal tracking", "partner follow-up", "파트너 딜 관리", "파트너십 오케스트레이션", "공동
  제안 추적", "sales-partner-orchestrator", "채널 딜 관리", or needs to manage a
  multi-party partner deal. Do NOT use for direct sales deal tracking without
  partner involvement (use deal-stage-guardian). Do NOT use for lead
  prospecting (use kwp-apollo-prospect). Do NOT use for meeting analysis
  without partner context (use meeting-digest). Do NOT use for proposal
  drafting (use sales-proposal-architect).
---

# Sales Partnership / Channel Deal Orchestrator

Structure and track multi-party partner deals by extracting commitments from unstructured communications, detecting follow-up lapses, and maintaining a shared action item registry across ThakiCloud, MSP partners, and end customers.

## When to Use

- Managing a co-proposal with an MSP partner (e.g., Bespin Global, Megazone)
- Tracking action items across multiple parties after a joint meeting
- Detecting stalled partner deals or follow-up lapses
- Preparing status updates for partner deal reviews
- Onboarding a new partner deal into the tracking system

## Multi-Party Deal Model

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  ThakiCloud  │◄──►│  MSP Partner │◄──►│ End Customer │
│              │    │              │    │              │
│  - Platform  │    │  - Services  │    │  - Budget    │
│  - Support   │    │  - Delivery  │    │  - Timeline  │
│  - License   │    │  - Ops       │    │  - Decision  │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────┴───────┐
                    │  Shared      │
                    │  Action Items│
                    │  + Blockers  │
                    └──────────────┘
```

## Pipeline

```
Partner Communications (email / meeting notes / Slack)
       │
       ▼
┌─────────────────────────────┐
│  Phase 1: Communication      │
│  Ingestion                   │
│  gws-gmail for emails        │
│  meeting-digest for meetings │
│  Slack MCP for threads       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 2: Commitment         │
│  Extraction                  │
│  Parse action items with     │
│  owner + deadline + party    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 3: Blocker            │
│  Detection                   │
│  Identify stalled items,     │
│  missing responses, gaps     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 4: Health Assessment  │
│  Score deal health,          │
│  generate partner deal card  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 5: Status Publishing  │
│  md-to-notion for tracking   │
│  Slack notification for      │
│  urgent blockers             │
└─────────────────────────────┘
```

## Action Item Schema

```json
{
  "deal_id": "PARTNER-DEAL-001",
  "deal_name": "Customer X — MSP Partner Y — ThakiCloud",
  "parties": {
    "thakicloud": {"contact": "name", "role": "platform provider"},
    "partner": {"name": "MSP name", "contact": "name", "role": "service delivery"},
    "customer": {"name": "company", "contact": "name", "role": "buyer"}
  },
  "action_items": [
    {
      "id": "AI-001",
      "description": "action description",
      "owner_party": "thakicloud | partner | customer",
      "owner_name": "specific person",
      "source": "email | meeting | slack",
      "source_date": "ISO-8601",
      "deadline": "ISO-8601 or null",
      "status": "open | in-progress | blocked | done | overdue",
      "blocker": "description of what's blocking, if any",
      "days_since_created": 0,
      "follow_up_needed": true
    }
  ],
  "blockers": [
    {
      "id": "BLK-001",
      "description": "blocker description",
      "blocking_party": "thakicloud | partner | customer",
      "blocked_items": ["AI-001", "AI-003"],
      "suggested_escalation": "escalation approach",
      "severity": "critical | high | medium"
    }
  ],
  "deal_health": {
    "score": 75,
    "grade": "B",
    "trend": "improving | stable | declining",
    "risk_factors": ["list of concerns"],
    "positive_signals": ["list of good signs"]
  },
  "next_meeting_suggestion": {
    "proposed_agenda": ["agenda items"],
    "proposed_date_range": "suggested timeframe",
    "key_questions_to_resolve": ["questions"]
  }
}
```

## Execution Instructions

### Step 1 — Ingest Communications

1. For email threads: use `gws-gmail` to fetch recent partner-related emails (search by partner name or deal label).
2. For meeting transcripts: use `meeting-digest` to extract structured meeting notes.
3. For Slack threads: use Slack MCP to read relevant channel threads.
4. Identify the three parties (ThakiCloud, partner, customer) and their representatives.

### Step 2 — Extract Commitments

1. Parse each communication for action items — statements containing commitments, requests, or deliverables. For bilingual communications (Korean + English mixed), extract from both languages and unify duplicates.
2. Apply a confidence threshold: firm commitments ("I will send by Friday" / "금요일까지 보내드리겠습니다") are high-confidence action items. Vague intent ("I'll look into it" / "확인해보겠습니다") should be flagged as `tentative` and require human confirmation before being tracked as real action items.
3. For each action item, identify:
   - **Owner party**: Who committed or was asked (ThakiCloud / partner / customer). If ambiguous ("we" or "우리"), flag for human assignment.
   - **Owner name**: Specific person responsible
   - **Deadline**: Explicit or inferred deadline. If no deadline is stated, set to `null` and flag for human assignment — do not infer arbitrary deadlines.
   - **Source**: Which communication the commitment came from
4. Deduplicate across sources — the same action item may appear in email and meeting notes. Match by semantic similarity, not exact text.

### Step 3 — Detect Blockers

1. Flag action items with no response after 48 hours as potential blockers.
2. Identify circular dependencies (A waits for B, B waits for A).
3. Detect items where the owner party has gone silent.
4. For each blocker, suggest an escalation approach (direct follow-up email, escalate to partner manager, schedule sync call).

### Step 4 — Assess Deal Health

1. Score deal health 0-100 based on:
   - Action item completion rate (weight: 30%)
   - Communication recency — days since last meaningful exchange (weight: 25%)
   - Blocker severity and count (weight: 25%)
   - Forward momentum — are new items being created and completed? (weight: 20%)
2. Assign grade: A (80+), B (60-79), C (40-59), D (<40).
3. Determine trend by comparing to previous health assessment if available.

### Step 5 — Publish Status

1. Generate a deal health card in markdown format.
2. Publish to Notion via `md-to-notion` for persistent tracking.
3. Post blocker alerts to Slack if any critical blockers exist.
4. Persist full output to `outputs/sales-partner/{date}/{deal-slug}/`.

## Constraints

- Never auto-send messages to partners or customers — all external communications require human approval
- Action items must have an identified owner party; unattributable items should be flagged for human assignment
- Deal health scores must follow the documented formula (completion 30%, recency 25%, blockers 25%, momentum 20%) — no ad-hoc weighting
- Blocker escalation suggestions are advisory only — do not execute escalation without human approval
- Limit action item extraction to the most recent 30 days of communications unless explicitly asked for a wider window

## Gotchas

- Partner emails often CC multiple ThakiCloud contacts — deduplicate action items that appear in both individual and group email threads
- Meeting notes from joint meetings may attribute action items ambiguously ("we will do X") — flag these for human clarification rather than guessing the owner party
- MSP partner naming conventions vary (e.g., "Bespin Global" vs "Bespin" vs "BG") — normalize partner names to prevent duplicate deal tracking
- Slack threads may contain informal commitments ("I'll look into it") that are not genuine action items — apply a higher bar for Slack-sourced items than email-sourced ones
- Deal health trends require at least 2 assessment snapshots to calculate — first assessment should show "trend: new" rather than fabricating a direction

## Verification

Before publishing the deal status:
1. Every action item has an owner_party and source attribution
2. Blocker items reference specific blocked action item IDs
3. Deal health score calculation matches the documented weights
4. No external-facing content is included in the Notion/Slack output without human review flag
5. Partner names are normalized consistently across all action items

## Autonomy Level: L2

- **Auto**: Communication ingestion, commitment extraction, blocker detection, health scoring, internal status publishing
- **Human Review Required**: Escalation decisions, partner-facing communications, deal health assessments shared externally
- **Never Auto**: Sending messages to partners or customers, committing resources or timelines

## Integration Points

- **Upstream**: Partner emails, meeting notes, Slack threads
- **Downstream**: Deal health feeds into `sales-deal-prep` for meeting context, and into overall pipeline reporting
- **Harness**: Invoked standalone in `partner-deal` mode of `sales-agent-harness`
