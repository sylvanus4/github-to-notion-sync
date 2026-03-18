---
description: Weekly executive business summary: pipeline changes, closed deals, risk items, next week's priorities as a one-pager.
argument-hint: "[--week YYYY-MM-DD]"
---

# /ceo-brief

Generates a weekly executive business summary: pipeline delta metrics, closed deals with values, risk items, and next week's priorities. Outputs a one-pager DOCX, posts to Slack, and uploads to Google Drive.

## What This Command Does

Queries the Notion pipeline database for this week's changes, computes pipeline delta metrics, lists closed deals with values, identifies risk items, generates an executive one-pager, creates a DOCX, posts to Slack, and uploads to Google Drive.

## Required Input

- **Week** (optional) — `--week YYYY-MM-DD` to specify the week; defaults to current week.

## Execution Steps

1. **Query Notion pipeline DB for this week's changes** — Fetch pipeline data via Notion MCP.
2. **Compute pipeline delta metrics** — Compare to prior week: new deals, moved stages, value changes.
3. **List closed deals with values** — Extract won deals and amounts.
4. **Identify risk items** — Flag at-risk deals, blockers, and escalations.
5. **Generate executive one-pager** — Use agency-executive-summary-generator and kwp-product-management-stakeholder-comms.
6. **Create .docx** — Produce one-pager via anthropic-docx.
7. **Post to Slack + upload to Drive** — Post summary to `#효정-할일`, upload DOCX to gws-drive.

## Output

- Executive one-pager DOCX
- Slack post with summary
- Google Drive file

## Skills Used

- agency-executive-summary-generator: Executive summary format
- kwp-product-management-stakeholder-comms: Stakeholder-tailored comms
- visual-explainer: Metrics visualization (optional)
- anthropic-docx: DOCX generation
- gws-drive: Drive upload

## Example Usage

```
/ceo-brief
/ceo-brief --week 2026-03-11
```
