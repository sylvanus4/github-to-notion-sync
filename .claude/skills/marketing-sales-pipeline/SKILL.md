---
name: marketing-sales-pipeline
description: >-
  Visitor-to-pipeline automation combining RB2B visitor identification,
  intent-based routing, deal resurrection, trigger prospecting, ICP learning,
  and suppression management.
disable-model-invocation: true
---

# Marketing Sales Pipeline

End-to-end visitor-to-pipeline automation. Identifies anonymous website visitors via RB2B, scores intent, routes to campaigns, resurrects dead deals, discovers trigger events, and continuously refines ICP definitions.

## Triggers

Use when the user asks to:
- "sales pipeline automation", "deal resurrector", "ICP learning", "RB2B routing"
- "trigger prospecting", "visitor identification", "intent scoring"
- "영업 파이프라인 자동화", "딜 부활", "ICP 학습", "방문자 식별"
- "suppression pipeline", "webhook ingest", "deal resurrection"

## Do NOT Use

- For CRM outreach message drafting → use `kwp-sales-draft-outreach`
- For Apollo lead enrichment and sequencing → use `kwp-apollo-*` skills
- For Common Room contact/account research → use `kwp-common-room-*` skills
- For general account research → use `kwp-sales-account-research`
- For sales call preparation → use `kwp-sales-call-prep`

## Prerequisites

- Python 3.10+
- `pip install requests python-dotenv`
- Environment variables: `HUBSPOT_API_KEY`, `INSTANTLY_API_KEY`, `BRAVE_API_KEY`
- Optional: `DATABASE_URL` (for ICP learning persistence)

## Execution Steps

### Step 1: Webhook Ingestion
Run `scripts/rb2b_webhook_ingest.py --serve` to receive RB2B visitor identification webhooks.

### Step 2: Suppression Pipeline
Run `scripts/rb2b_suppression_pipeline.py` to filter out existing customers, competitors, and blacklisted domains.

### Step 3: Intent Routing
Run `scripts/rb2b_instantly_router.py --serve` to score visitor intent and route to appropriate Instantly campaigns.

### Step 4: Deal Resurrection
Run `scripts/deal_resurrector.py` to scan CRM for stalled deals matching re-engagement criteria.

### Step 5: Trigger Prospecting
Run `scripts/trigger_prospector.py` to monitor hiring signals, funding events, and tech stack changes via Brave Search API.

### Step 6: ICP Learning
Run `scripts/icp_learning_analyzer.py` to analyze closed-won patterns and continuously refine ideal customer profiles.

## Output

- Routed leads in Instantly campaigns
- Resurrected deal queue with re-engagement briefs
- Trigger event alerts
- Updated ICP model with confidence scores

## Examples

### Example 1: Full visitor-to-pipeline flow

User: "Set up RB2B visitor identification and route to Instantly campaigns"

1. Start webhook listener: `scripts/rb2b_webhook_ingest.py --serve`
2. Filter known contacts: `scripts/rb2b_suppression_pipeline.py`
3. Score and route: `scripts/rb2b_instantly_router.py --serve`

Result: Anonymous visitors identified, filtered, scored, and routed to appropriate campaigns.

### Example 2: Resurrect stalled deals

User: "Find dead deals we can re-engage"

1. Run `scripts/deal_resurrector.py --days-stale 90`

Result: List of re-engagement candidates with recommended outreach briefs.

## Error Handling

| Error | Action |
|-------|--------|
| HUBSPOT_API_KEY not set | Required for deal resurrection and ICP learning; set in `.env` |
| INSTANTLY_API_KEY not set | Required for campaign routing; set in `.env` |
| Webhook server port conflict | Default port 8080; override with `--port <N>` |
| No stalled deals found | Adjust `--days-stale` threshold or check CRM filters |

## Composed Skills

- `kwp-apollo-enrich-lead` for lead enrichment
- `kwp-sales-competitive-intelligence` for competitive context
