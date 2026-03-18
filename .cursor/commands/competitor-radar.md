---
description: Deep researches competitors + multi-perspective analysis, produces DOCX report and distributes to Notion + Slack.
argument-hint: "[competitor1, competitor2, ...] or --watchlist"
---

# /competitor-radar

Runs deep research on a competitor list, dispatches CSO and PM perspectives for multi-angle analysis, generates a comparison matrix and DOCX report, and distributes to Notion and Slack.

## What This Command Does

Accepts a list of competitors (or uses a default watchlist), runs parallel-deep-research per competitor, invokes role-cso and role-pm for strategic and product perspectives, builds a comparison matrix, creates a comprehensive DOCX report, publishes to Notion, and posts a summary to Slack.

## Required Input

- **Competitor list** — Comma-separated competitor names, or `--watchlist` to use the default competitive watchlist.

## Execution Steps

1. **Accept competitor list or use default watchlist** — Parse input or load default competitors.
2. **Run parallel-deep-research per competitor** — Deep research each competitor's positioning, features, pricing, and market presence.
3. **Run role-dispatcher with CSO + PM perspectives** — Invoke role-cso and role-pm for strategic and product analysis.
4. **Generate comparison matrix** — Build feature/positioning/pricing comparison table.
5. **Create DOCX report** — Produce comprehensive report via anthropic-docx.
6. **Publish to Notion** — Upload report content via md-to-notion.
7. **Post summary to Slack** — Post main summary to `#효정-할일` with thread for key findings.

## Output

- Competitor analysis DOCX
- Notion page(s) with report content
- Slack post with summary and links

## Skills Used

- parallel-deep-research: Per-competitor deep research
- kwp-marketing-competitive-analysis: Competitive positioning
- kwp-product-management-competitive-analysis: Feature comparison
- role-cso: Strategic perspective
- role-pm: Product perspective
- anthropic-docx: DOCX generation
- md-to-notion: Notion publishing
- md-to-slack-canvas: Slack Canvas distribution (optional)

## Example Usage

```
/competitor-radar AWS, GCP, Azure
/competitor-radar --watchlist
/competitor-radar CompetitorA, CompetitorB, CompetitorC
```
