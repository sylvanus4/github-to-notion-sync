---
name: email-auto-reply
description: >-
  Knowledge-based email draft generation with human approval gate. Reads
  incoming emails, retrieves relevant context from Cognee knowledge graph and
  recall memory, generates 2-3 draft reply options per email, and presents them
  for human approval before sending. Use when the user asks to "auto-reply to
  emails", "draft email responses", "answer my emails", "이메일 자동 답변",
  "메일 답장 초안", "email auto-reply", or wants AI-generated reply drafts with
  approval workflow. Do NOT use for sending emails without approval (use
  gws-gmail directly), email triage without replies (use gmail-daily-triage), or
  calendar-related email actions (use smart-meeting-scheduler).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "comms-automation"
---
# email-auto-reply

Knowledge-based email draft generation with human approval gate.

## Workflow

1. **Triage** — Fetch unread emails via `gws-gmail`, classify by urgency (P1-P4) and intent (reply-needed, FYI, action-required)
2. **Context retrieval** — For reply-needed emails: query `cognee` knowledge graph for sender history, related projects, prior decisions; query `recall` for recent session context
3. **Draft generation** — Generate 2-3 reply drafts per email with varying tone/detail level (concise, detailed, diplomatic)
4. **Human gate** — Present drafts to user via Slack thread or terminal; user selects one, edits if needed, approves
5. **Send** — Send approved reply via `gws-gmail`; index the exchange in Cognee for future context

## Composed Skills

- `gws-gmail` — Email read/send operations
- `recall` — Cross-session context retrieval
- `cognee` — Knowledge graph search for sender/topic context
- `gmail-daily-triage` — Email classification patterns

## Error Handling

| Error | Action |
|-------|--------|
| No unread reply-needed emails found | Report "No emails requiring replies" and exit gracefully |
| Cognee unavailable or empty | Proceed with recall-only context; note reduced context quality in draft headers |
| gws-gmail auth failure | Prompt user to re-authenticate via `gws auth login` |
| User rejects all drafts for an email | Skip that email, log as "deferred", move to next |
| Send failure after approval | Retry once; if still failing, save draft in Gmail drafts folder and notify user |

## Examples

```
User: "오늘 답장 필요한 메일 처리해줘"
→ Fetches reply-needed emails, generates 2-3 drafts per email, presents for approval

User: "email auto-reply"
→ Runs full pipeline: triage → context → drafts → approval → send
```
