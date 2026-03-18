---
description: Reads Notion backlog DB, runs multi-framework scoring (RICE, ICE, MoSCoW), outputs ranked recommendations with confidence intervals.
argument-hint: "[--db <notion-db-id>]"
---

# /backlog-triage

Reads the Notion backlog database, applies RICE, ICE, and MoSCoW scoring frameworks, and produces a ranked recommendation report with confidence intervals and visual charts.

## What This Command Does

Queries the Notion backlog database for items, extracts scoring dimensions (impact, effort, confidence, reach, etc.), calculates RICE and ICE scores, applies MoSCoW classification, and generates a ranked list with confidence intervals. Output includes a recommendation report and visual chart posted to Slack.

## Required Input

- **Notion backlog database** — Either the default backlog DB or one specified via `--db <notion-db-id>`.

## Execution Steps

1. **Query Notion backlog DB** — Fetch backlog items via Notion MCP database-query.
2. **Extract scoring dimensions** — Parse each item for impact, effort, confidence, reach, strategic fit.
3. **Calculate RICE scores** — Compute (Reach × Impact × Confidence) / Effort for each item.
4. **Calculate ICE scores** — Compute Impact × Confidence × Ease for each item.
5. **Generate ranked list with confidence intervals** — Combine frameworks, apply MoSCoW (Must/Should/Could/Won't), add confidence intervals.
6. **Produce recommendation report** — Create structured markdown report with rankings and rationale.
7. **Post to Slack with visual chart** — Post summary to `#효정-할일` with visual-explainer chart of top items.

## Output

- Ranked backlog report (markdown)
- Visual chart (HTML or image)
- Slack post with summary and chart

## Skills Used

- kwp-product-management-roadmap-management: RICE, MoSCoW, prioritization frameworks
- pm-execution: Sprint planning, prioritization logic
- kwp-data-statistical-analysis: Confidence intervals, scoring
- visual-explainer: Chart generation for Slack

## Example Usage

```
/backlog-triage
/backlog-triage --db abc123def456
```
