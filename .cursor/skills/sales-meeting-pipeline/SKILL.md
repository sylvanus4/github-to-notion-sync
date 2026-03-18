---
description: Post-meeting pipeline: digests meeting, extracts commitments and next steps, drafts follow-up email, updates CRM status in Notion, creates internal brief, and posts to team channel. Use when "post meeting", "미팅 후 처리", "meeting follow-up pipeline". Do NOT use for meeting prep (use kwp-sales-call-prep), email only (use gws-gmail). Korean triggers: "미팅 후 처리", "미팅 팔로업", "영업 미팅 파이프라인".
---

# Sales Meeting Pipeline

## Overview
Post-meeting automation that digests sales call content, extracts commitments and next steps, drafts follow-up email, updates CRM status in Notion, creates an internal brief for the team, and posts a summary to the sales channel.

## Autonomy Level
**L2** — Human-in-loop for email send and CRM update approval; automation handles digest and draft.

## Pipeline Architecture
Sequential: meeting-digest → extract commitments → gws-gmail (follow-up) → Notion CRM update → internal brief → Slack post.

### Mermaid Diagram
```mermaid
flowchart LR
    A[Meeting Content] --> B[meeting-digest]
    B --> C[Extract Commitments]
    C --> D[gws-gmail Draft]
    D --> E[Notion CRM Update]
    E --> F[Internal Brief]
    F --> G[Slack Post]
```

## Trigger Conditions
- Post-sales-meeting workflow
- "post meeting", "미팅 후 처리", "meeting follow-up pipeline"
- `/sales-meeting-pipeline` with meeting URL or transcript

## Skill Chain
| Step | Skill | Purpose |
|------|-------|---------|
| 1 | meeting-digest | Summarize meeting, extract action items |
| 2 | kwp-sales-call-prep | Context for follow-up (used inversely for post-call) |
| 3 | gws-gmail | Draft and optionally send follow-up email |
| 4 | kwp-sales-draft-outreach | Polish follow-up message |
| 5 | md-to-notion | Update deal/contact record in Notion CRM |

## Output Channels
- **Gmail**: Follow-up email draft or sent
- **Notion**: Updated CRM record (deal stage, next steps, notes)
- **Slack**: Internal brief to team channel

## Configuration
- `NOTION_CRM_DB_ID`: Deals/contacts database
- `SLACK_SALES_CHANNEL_ID`: Team channel for briefs
- Meeting source: Notion page, transcript file, or calendar event

## Example Invocation
```
"Run post-meeting pipeline for [meeting URL]"
"미팅 후 처리해줘"
"Sales meeting follow-up: [transcript]"
```
