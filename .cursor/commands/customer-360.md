---
description: Aggregates all customer touchpoints (meetings, emails, proposals, issues) into a comprehensive customer brief.
argument-hint: "<company-name or notion-crm-link>"
---

# /customer-360

Aggregates all customer touchpoints from Notion, Gmail, and Cognee knowledge graph into a comprehensive customer brief with timeline and actionable insights.

## What This Command Does

Accepts a company name or Notion CRM link, searches Notion for all related pages (meetings, proposals, issues), searches Gmail for recent correspondence, queries Cognee knowledge graph for historical interactions, compiles a customer timeline, and generates a comprehensive brief. Output is published to Notion and posted to Slack.

## Required Input

- **Company name or Notion CRM link** — Identifier for the customer/account.

## Execution Steps

1. **Accept company name or Notion CRM link** — Parse input.
2. **Search Notion for all related pages** — Meetings, proposals, issues, CRM records.
3. **Search Gmail for recent correspondence** — Emails involving the customer.
4. **Search Cognee KG for historical interactions** — Query knowledge graph for past touchpoints.
5. **Compile customer timeline** — Merge all sources into chronological timeline.
6. **Generate comprehensive brief** — Create structured brief with key insights and next actions.
7. **Output to Notion + Slack** — Publish brief to Notion, post summary to `#효정-할일`.

## Output

- Customer 360 brief (markdown)
- Notion page with full brief
- Slack post with summary and link

## Skills Used

- kwp-sales-account-research: Account research
- kwp-sales-call-prep: Call context
- kwp-common-room-account-research: Common Room signals (if connected)
- gws-gmail: Email search
- cognee: Knowledge graph search
- md-to-notion: Notion publishing

## Example Usage

```
/customer-360 Acme Corp
/customer-360 https://notion.so/thakicloud/CRM-Acme-abc123
```
