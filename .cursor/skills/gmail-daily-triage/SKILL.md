---
name: gmail-daily-triage
description: >-
  Triage yesterday's Gmail inbox: delete spam, move low-priority notifications
  (Notion, RunPod, GitHub, calendar accepts) to a label, summarize unanswered
  emails with action items into a .docx, compile bespin_news links into a news
  digest .docx via Playwright, open company colleague attachments, and create
  Gmail filters for recurring patterns. Use when the user asks to "triage
  email", "clean up inbox", "yesterday's emails", "메일 정리", "이메일 트리아지",
  "어제 메일 정리", "gmail triage", or "inbox cleanup". Do NOT use for sending
  emails (use gws-gmail), reading a single email, or calendar management
  (use gws-calendar).
metadata:
  author: thaki
  version: 1.0.0
---

# Gmail Daily Triage

Automated daily inbox cleanup that classifies yesterday's emails, trashes spam, files low-priority notifications, summarizes actionable emails, and creates Gmail filters.

> **Prerequisites**: `gws` CLI installed and authenticated. See `gws-workspace` skill.

## Sub-Skill Index

| Phase | Description | Reference |
|-------|-------------|-----------|
| Sender Rules | Classification patterns for known senders | [references/sender-rules.md](references/sender-rules.md) |
| Filter Templates | Gmail filter JSON templates | [references/filter-templates.md](references/filter-templates.md) |

## Workflow

### Phase 0: Setup Labels

Ensure the "Low Priority" label exists. If not, create it.

```bash
gws gmail users labels list --params '{"userId": "me"}'
```

If "Low Priority" is missing:

```bash
gws gmail users labels create \
  --params '{"userId": "me"}' \
  --json '{"name": "Low Priority", "labelListVisibility": "labelShow", "messageListVisibility": "show"}'
```

Save the label ID for later use.

### Phase 1: Fetch Yesterday's Emails

Calculate yesterday's date boundaries and fetch all messages.

```bash
gws gmail users messages list \
  --params '{"userId": "me", "q": "after:YYYY/MM/DD before:YYYY/MM/DD", "maxResults": 100}'
```

For each message ID, fetch full message (metadata-only format may omit headers):

```bash
gws gmail users messages get \
  --params '{"userId": "me", "id": "MSG_ID"}'
```

Extract From, Subject, Date, To, Cc from `payload.headers`, and labels from `labelIds`.

### Phase 2: Classify and Act

Read [references/sender-rules.md](references/sender-rules.md) for classification patterns.

For each email, classify and apply the corresponding action:

#### Category A -- Spam (Trash)

Classify by sender pattern only. **Never open or render spam email bodies.**

```bash
gws gmail users messages trash \
  --params '{"userId": "me", "id": "MSG_ID"}'
```

#### Category B -- Low Priority Notifications

Move to "Low Priority" label and remove from INBOX.
Includes: Notion team, RunPod, GitHub notifications, Google Calendar accepts/declines.

```bash
gws gmail users messages modify \
  --params '{"userId": "me", "id": "MSG_ID"}' \
  --json '{"addLabelIds": ["LOW_PRIORITY_LABEL_ID"], "removeLabelIds": ["INBOX"]}'
```

#### Category C -- bespin_news@bespinglobal.com

1. Fetch full message body: `gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID"}'`
2. Extract all URLs from the HTML body (filter out unsubscribe/tracking links)
3. For each article URL, use `cursor-ide-browser` MCP tools to fetch content:

```
browser_navigate → URL
browser_snapshot → extract article text
```

If browser tools are unavailable, fall back to `WebFetch` tool.

4. Summarize each article in 2-3 sentences (Korean)
5. Generate an "AI/GPU Cloud Insights" analysis section covering:
   - Market trends relevant to AI infrastructure
   - Competitor moves (cloud providers, GPU vendors)
   - Technology shifts (new models, hardware, frameworks)
   - Customer pain points and opportunities for ThakiCloud
6. Compile into `/tmp/bespin-news-YYYY-MM-DD.docx` using `anthropic-docx` skill:
   - Title: "Bespin News Digest - YYYY-MM-DD"
   - Per-article section: title, source URL, 2-3 sentence summary
   - Final section: "AI/GPU Cloud 핵심 인사이트" with 3-5 actionable bullet points

**Output**: article summaries (for Slack thread), docx path, insight bullets

#### Category D -- Company Colleague Emails

Detect by known company domains: `@thakicloud.co.kr`, `@bespinglobal.com`.
Triggers for ALL colleague emails regardless of attachments.

1. Fetch full message body:

```bash
gws gmail users messages get \
  --params '{"userId": "me", "id": "MSG_ID"}'
```

2. Summarize email content in 2-3 sentences (Korean)
3. Draft a reply:
   - `@thakicloud.co.kr` senders: team-casual tone
   - `@bespinglobal.com` senders: formal business tone
4. If attachments exist, download and summarize:

```bash
gws gmail users messages attachments get \
  --params '{"userId": "me", "messageId": "MSG_ID", "id": "ATTACHMENT_ID"}'
```

**Output per email**: sender, subject, summary, draft_reply, attachment_summary (if any)

#### Category E -- Needs Reply (Unanswered)

Identify emails where:
- User is in TO or CC
- Thread has no reply from user (check thread for sent messages)
- Not a notification or automated email

For each:
- Summarize the email in 2-3 sentences
- List action items
- Draft a suggested reply template

Compile into `reply-needed-YYYY-MM-DD.docx` using `anthropic-docx` skill:
- Title: "Reply Needed - YYYY-MM-DD"
- Per-email sections: sender, subject, summary, action items, draft reply

#### Category F -- Calendar Accepts/Declines

These are subcategorized under Category B (Low Priority) but explicitly handled:
- Detect by sender containing `calendar-notification@google.com` or snippet containing "수락", "거절", "accepted", "declined"
- Move to Low Priority label

### Phase 3: Generate Gmail Filters

Based on the day's triage patterns, create Gmail filters for automation.
Read [references/filter-templates.md](references/filter-templates.md) for templates.

```bash
gws gmail users settings filters create \
  --params '{"userId": "me"}' \
  --json '{"criteria": {...}, "action": {...}}'
```

Only create filters for patterns that appeared 2+ times during triage.
List existing filters first to avoid duplicates:

```bash
gws gmail users settings filters list --params '{"userId": "me"}'
```

### Phase 4: Report

Present a Korean summary:

```
## 메일 정리 완료 (YYYY-MM-DD)

### 처리 현황
- 스팸 삭제: N건
- 중요하지 않은 알림 이동: N건
- 답장 필요: N건
- Bespin 뉴스 정리: N개 기사

### 생성된 문서
- /tmp/reply-needed-YYYY-MM-DD.docx
- /tmp/bespin-news-YYYY-MM-DD.docx

### 새로 생성된 Gmail 필터
- [필터 설명]: [적용 기준]
```

## Examples

### Example 1: Standard daily triage

User: "어제 메일 정리해줘"

Actions:
1. Check/create "Low Priority" label
2. Fetch 12 messages from yesterday
3. Classify: 2 spam, 4 calendar notifications, 1 bespin_news, 3 company emails, 2 need reply
4. Trash 2 spam, move 4 to Low Priority, extract 39 news links from bespin_news, summarize 2 reply-needed
5. Generate bespin-news-2026-03-09.docx and reply-needed-2026-03-09.docx
6. Create 2 new Gmail filters

### Example 2: No actionable emails

User: "gmail triage"

Actions:
1. Fetch 3 messages from yesterday
2. All are calendar notifications -> move to Low Priority
3. Report: "답장 필요한 메일이 없습니다. 모든 알림이 정리되었습니다."

## Security Rules

- **Never permanently delete** emails -- use trash (reversible)
- **Never open spam bodies** -- classify by sender and subject metadata only
- **Never send replies** without explicit user confirmation
- Confirm before creating Gmail filters
- Company email domains are trusted: `@thakicloud.co.kr`, `@bespinglobal.com`

## Error Handling

| Situation | Action |
|-----------|--------|
| gws auth expired | Prompt: `gws auth login -s gmail` |
| No emails yesterday | Report "받은편지함이 비어 있습니다" |
| Playwright URL timeout | Skip article, note in digest as "[접속 불가]" |
| Attachment download fails | Note in summary, continue with remaining |
| Label creation fails | Use existing similar label or report error |
| Filter already exists | Skip creation, note in report |
| Filter creation 403 (insufficient scopes) | Prompt: `gws auth login -s gmail,gmail.settings.basic` -- filter creation requires the `gmail.settings.basic` scope beyond the standard `gmail.modify` scope |
