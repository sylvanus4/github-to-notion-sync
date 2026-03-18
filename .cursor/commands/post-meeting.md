---
description: Post-meeting pipeline — processes meeting notes, generates follow-up email, updates CRM, creates internal brief.
argument-hint: "<notion-meeting-url or --file path or --raw text>"
---

# /post-meeting

Post-meeting pipeline that processes meeting content, extracts commitments and next steps, drafts follow-up email, updates Notion CRM record, creates a one-page internal brief, and posts to the team Slack channel.

## What This Command Does

Accepts a Notion meeting page URL, file path, or raw transcript. Runs meeting-digest to analyze content, extracts commitments and next steps, drafts a follow-up email, updates the Notion CRM record for the account, creates a one-page internal brief, and posts the brief to the team Slack channel.

## Required Input

- **Meeting content** — Notion meeting page URL, `--file <path>`, or `--raw "text"`.

## Execution Steps

1. **Accept Notion meeting page URL or paste transcript** — Parse input source.
2. **Run meeting-digest** — Analyze meeting content and extract structured summary + action items.
3. **Extract commitments and next steps** — Parse action items for customer commitments and follow-ups.
4. **Draft follow-up email** — Use kwp-sales-draft-outreach or gws-gmail to compose follow-up.
5. **Update Notion CRM record** — Create or update CRM page with meeting outcomes.
6. **Create one-page internal brief** — Generate concise brief for internal distribution.
7. **Post brief to team Slack channel** — Post to `#효정-할일` or specified sales channel.

## Output

- Meeting digest (Notion)
- Follow-up email draft
- Updated Notion CRM record
- One-page internal brief
- Slack post with brief summary

## Skills Used

- meeting-digest: Meeting analysis and action items
- kwp-sales-call-prep: Call context and prep
- gws-gmail: Email drafting
- kwp-sales-draft-outreach: Follow-up message composition
- md-to-notion: CRM and brief publishing

## Example Usage

```
/post-meeting https://notion.so/thakicloud/Customer-X-Discovery-abc123
/post-meeting --file output/meetings/raw/customer-call.md
/post-meeting --raw "Meeting with Acme Corp. Discussed pricing..."
```
