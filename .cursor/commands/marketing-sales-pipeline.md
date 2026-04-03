---
description: "Visitor-to-pipeline automation — RB2B identification, intent routing, deal resurrection, trigger prospecting, ICP learning"
argument-hint: "[ingest|suppress|route|resurrect|prospect|icp] [context]"
---

# Marketing Sales Pipeline

Read and follow the skill at `.cursor/skills/marketing/marketing-sales-pipeline/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Run the requested sales pipeline operation:

| Command | Script | Purpose |
|---------|--------|---------|
| `ingest` | `scripts/rb2b_webhook_ingest.py` | Receive RB2B visitor webhooks |
| `suppress` | `scripts/rb2b_suppression_pipeline.py` | Filter existing customers/competitors |
| `route` | `scripts/rb2b_instantly_router.py` | Score intent and route to campaigns |
| `resurrect` | `scripts/deal_resurrector.py` | Scan CRM for stalled deal re-engagement |
| `prospect` | `scripts/trigger_prospector.py` | Monitor hiring/funding/tech signals |
| `icp` | `scripts/icp_learning_analyzer.py` | Refine ideal customer profiles |

If no specific command given, provide an overview of available operations and current prerequisites status.
