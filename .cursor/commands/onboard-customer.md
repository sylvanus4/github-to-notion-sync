---
description: Generates complete customer onboarding package: checklist, welcome docs, success criteria, CSM assignment.
argument-hint: "<customer-name> [--contract <details>]"
---

# /onboard-customer

Generates a complete customer onboarding package: onboarding checklist from template, welcome documentation, success criteria template, Notion onboarding tracker, CSM assignment, and Drive-shared package.

## What This Command Does

Accepts customer name and contract details, generates an onboarding checklist from template, creates a welcome documentation package, defines success criteria template, creates a Notion onboarding tracker, assigns CSM and notifies, and shares the package via Google Drive.

## Required Input

- **Customer name** — Name of the new customer.
- **Contract details** (optional) — Key contract terms, start date, tier.

## Execution Steps

1. **Accept customer name and contract details** — Parse input.
2. **Generate onboarding checklist from template** — Use onboarding-accelerator patterns or pm-execution for checklist structure.
3. **Create welcome documentation package** — Generate welcome letter, getting-started guide via anthropic-docx.
4. **Define success criteria template** — Create success criteria checklist for the customer tier.
5. **Create Notion onboarding tracker** — Publish tracker via md-to-notion.
6. **Assign CSM and notify** — Update tracker with CSM, post assignment to Slack.
7. **Share package via Drive** — Upload docs to gws-drive and share with customer.

## Output

- Onboarding checklist
- Welcome documentation package (DOCX)
- Success criteria template
- Notion onboarding tracker
- Slack notification for CSM
- Google Drive shared folder

## Skills Used

- onboarding-accelerator: Checklist and structure (adapted for customer onboarding)
- anthropic-docx: Welcome docs and templates
- gws-drive: Drive upload and sharing
- md-to-notion: Notion tracker

## Example Usage

```
/onboard-customer Acme Corp
/onboard-customer NewCo --contract "Enterprise, 12-month, starts 2026-04-01"
```
