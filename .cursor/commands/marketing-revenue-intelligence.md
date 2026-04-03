---
description: "Revenue intelligence — Gong call insights, content-to-revenue attribution, automated client reports"
argument-hint: "[gong|attribution|report] [client name or transcript]"
---

# Marketing Revenue Intelligence

Read and follow the skill at `.cursor/skills/marketing/marketing-revenue-intelligence/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Run the requested revenue intelligence operation:

| Command | Script | Purpose |
|---------|--------|---------|
| `gong` | `scripts/gong_insight_pipeline.py` | Call insight extraction (--file or --gong) |
| `attribution` | `scripts/revenue_attribution.py` | Multi-touch attribution (--report, --gaps, --cpa) |
| `report` | `scripts/client_report_generator.py` | Client performance report (--client, --format) |

Requires: `GONG_ACCESS_KEY`, `GONG_ACCESS_KEY_SECRET`, `HUBSPOT_API_KEY`. Optional: `GA4_PROPERTY_ID`, `AHREFS_TOKEN`.
