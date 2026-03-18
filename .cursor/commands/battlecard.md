---
description: Generates competitive battlecard from web research with win/loss analysis and talking points.
argument-hint: "<competitor-name>"
---

# /battlecard

Generates a competitive battlecard from deep web research, including win/loss analysis, comparison matrix, and interactive HTML sections. Publishes to Notion and posts to Slack.

## What This Command Does

Accepts a competitor name, runs parallel-deep-research and kwp-sales-competitive-intelligence analysis, generates a comparison matrix, creates an interactive HTML battlecard with clickable sections, publishes to Notion, and posts a summary to Slack.

## Required Input

- **Competitor name** — Name of the competitor to analyze.

## Execution Steps

1. **Accept competitor name** — Parse input.
2. **Run parallel-deep-research on competitor** — Deep research on positioning, features, pricing, recent news.
3. **Run kwp-sales-competitive-intelligence analysis** — Build battlecard structure with win/loss angles.
4. **Generate comparison matrix** — Feature/positioning/pricing vs. our product.
5. **Create HTML battlecard with interactive sections** — Use kwp-sales-create-an-asset and visual-explainer for interactive HTML.
6. **Publish to Notion** — Upload battlecard content via md-to-notion.
7. **Post to Slack** — Post summary to `#효정-할일` with link to battlecard.

## Output

- Interactive HTML battlecard
- Comparison matrix
- Notion page with battlecard content
- Slack post with summary

## Skills Used

- parallel-deep-research: Competitor research
- kwp-sales-competitive-intelligence: Battlecard structure and win/loss
- kwp-sales-create-an-asset: Asset generation
- kwp-marketing-content-creation: Talking points and copy
- visual-explainer: Interactive HTML sections
- md-to-notion: Notion publishing

## Example Usage

```
/battlecard AWS
/battlecard CompetitorX
```
