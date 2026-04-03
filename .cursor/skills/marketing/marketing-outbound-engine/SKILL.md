---
name: marketing-outbound-engine
version: 1.0.0
description: Cold outbound sequence optimization with ICP definition, infrastructure audit, expert panel scoring, competitive monitoring, and capacity planning for Instantly campaigns.
---

# Marketing Outbound Engine

Cold outbound automation system. Audits infrastructure, defines ICP profiles, designs email sequences with expert panel scoring (90-point threshold), monitors competitors, and plans send capacity.

## Triggers

Use when the user asks to:

- "cold outbound", "outbound automation", "lead pipeline", "outbound optimizer"
- "Instantly audit", "cold email sequence", "competitive monitor"
- "콜드 아웃바운드", "아웃바운드 자동화", "리드 파이프라인"

## Do NOT Use

- For personalized outreach message drafting → use `kwp-sales-draft-outreach`
- For Apollo sequence management → use `kwp-apollo-sequence-load`
- For Common Room outreach composition → use `kwp-common-room-compose-outreach`
- For lead enrichment → use `kwp-apollo-enrich-lead`

## Prerequisites

- Python 3.10+
- `pip install requests python-dotenv`
- Optional: Instantly API key (for infrastructure audit mode)

## Execution Steps

### Step 1: Infrastructure Audit

Run `scripts/instantly-audit.py` (if API key available) to assess domain health, warmup status, and sending limits.

### Step 2: ICP Definition

Use `references/icp-template.md` to define ideal customer profile with firmographic and technographic criteria.

### Step 3: Sequence Design

Build email sequences following `references/copy-rules.md` and `references/instantly-rules.md`.

### Step 4: Expert Panel Scoring

Assemble panel per `references/expert-panel.md` and score sequences to 90-point threshold.

### Step 5: Competitive Monitoring

Run `scripts/competitive-monitor.py` to track competitor messaging and positioning changes.

### Step 6: Lead Pipeline

Run `scripts/lead-pipeline.py` to manage lead flow and `scripts/cross-signal-detector.py` for multi-channel signal aggregation.

### Step 7: Send Execution

Run `scripts/cold-outbound-sender.py` with human review gate — never auto-push without approval.

## Examples

### Example 1: Audit outbound infrastructure

User: "Audit our Instantly setup before launching a new campaign"

1. Run `scripts/instantly-audit.py --api-key $INSTANTLY_API_KEY`

Result: Domain health report with warmup status, sending limits, and deliverability scores.

### Example 2: Design a cold outbound sequence

User: "Create a cold email sequence for SaaS CTOs"

1. Define ICP using `references/icp-template.md`
2. Write sequence following `references/copy-rules.md`
3. Score with expert panel (90-point threshold)

Result: 5-email sequence with expert scores and improvement suggestions.

## Error Handling

| Error | Action |
|-------|--------|
| Instantly API unreachable | Check API key validity; fall back to manual infrastructure checklist |
| Expert panel score below 90 | Iterate on copy with specific feedback; max 3 revision rounds |
| No competitive data found | Expand competitor list or use manual research |
| Human review gate timeout | Never auto-send; re-queue for review |

## Output

- Infrastructure audit report
- ICP definition document
- Scored email sequences
- Competitive monitoring alerts
- Capacity planning spreadsheet
