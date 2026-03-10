---
name: google-daily
description: >-
  Master Google Workspace daily automation: calendar briefing, Gmail triage
  (spam cleanup, notification filing, news digest, reply-needed summary),
  and Drive upload of generated documents. Chains calendar-daily-briefing,
  gmail-daily-triage, and gws-drive skills sequentially. Use when the user
  runs /google, asks for "google daily", "구글 일일 자동화", "google 자동화",
  "daily google", "구글 데일리", or wants all Google Workspace daily tasks
  done in one flow. Do NOT use for individual tasks (use the specific skill).
metadata:
  author: thaki
  version: 1.0.0
---

# Google Daily Automation

Master orchestrator that chains all Google Workspace daily tasks into a single sequential pipeline.

> **Prerequisites**: `gws` CLI installed and authenticated with gmail, calendar, drive scopes. See `gws-workspace` skill.

## Pipeline Overview

```
Phase 1: Calendar Briefing  →  Phase 2: Gmail Triage  →  Phase 3: Drive Upload  →  Phase 4: Summary
```

Sequential pattern: each phase depends on the previous.

## Execution

### Phase 1 -- Calendar Briefing

Read and execute the `calendar-daily-briefing` skill at `.cursor/skills/calendar-daily-briefing/SKILL.md`.

1. Fetch today's events via `gws calendar +agenda --today`
2. Classify events (interviews, meetings, focus time)
3. Present the Korean briefing with preparation alerts
4. Note any HIGH priority items that need attention

**Output**: Korean schedule briefing displayed to user.

### Phase 2 -- Gmail Triage

Read and execute the `gmail-daily-triage` skill at `.cursor/skills/gmail-daily-triage/SKILL.md`.

1. Ensure "Low Priority" label exists
2. Fetch yesterday's emails
3. Classify each email using sender rules
4. Execute actions (trash spam, label notifications, extract news, summarize replies)
5. Generate `.docx` documents:
   - `/tmp/reply-needed-YYYY-MM-DD.docx` -- unanswered emails with action items
   - `/tmp/bespin-news-YYYY-MM-DD.docx` -- news digest (if bespin_news emails exist)
6. Create Gmail filters for recurring patterns
7. Present the triage report

**Output**: Triage summary + generated .docx files.

### Phase 3 -- Drive Upload

Upload all generated documents to Google Drive.

1. Create a dated folder:

```bash
gws drive files create \
  --json '{"name": "Google Daily - YYYY-MM-DD", "mimeType": "application/vnd.google-apps.folder"}'
```

2. Extract the folder ID from the response.

3. Upload each generated file:

```bash
gws drive +upload /tmp/reply-needed-YYYY-MM-DD.docx --parent FOLDER_ID
gws drive +upload /tmp/bespin-news-YYYY-MM-DD.docx --parent FOLDER_ID
```

4. Upload any other `.docx` or `.pptx` files generated during the session.

**Output**: Drive folder URL with uploaded files.

### Phase 4 -- Summary

Present a unified Korean daily briefing:

```markdown
# Google 데일리 자동화 완료 (YYYY-MM-DD)

## 1. 오늘의 일정
[Calendar briefing summary from Phase 1]

## 2. 메일 정리 결과
- 스팸 삭제: N건
- 알림 정리: N건
- 답장 필요: N건
- 뉴스 정리: N건 (N개 기사)

## 3. 생성된 문서
| 문서 | Drive 위치 |
|------|-----------|
| reply-needed-YYYY-MM-DD.docx | [Drive link] |
| bespin-news-YYYY-MM-DD.docx | [Drive link] |

## 4. Gmail 필터
- 새로 생성: N건
- 기존 유지: N건

## 5. 주의사항
[Any HIGH priority items from calendar or urgent emails]
```

## Examples

### Example 1: Full daily run

User: "/google"

Result:
1. Calendar: 5 events today, 1 interview (HIGH), 2 team meetings
2. Gmail: 9 emails yesterday -- 0 spam, 4 notifications moved, 1 news digest, 2 need reply
3. Drive: 2 documents uploaded to "Google Daily - 2026-03-09" folder
4. Summary presented in Korean with action items

### Example 2: Light day

User: "구글 데일리"

Result:
1. Calendar: 1 all-day event, no time-specific meetings
2. Gmail: 3 emails yesterday -- all calendar notifications, moved to Low Priority
3. Drive: No documents to upload (no news or reply-needed emails)
4. Summary: "오늘은 가볍습니다. 집중 업무에 활용하세요!"

## Subagent Strategy

Use sequential execution (Phase 2 depends on Phase 1 for context, Phase 3 depends on Phase 2 for files):

1. Run calendar briefing inline (fast, read-only)
2. Run Gmail triage as a Task subagent (slower, many API calls)
3. Run Drive upload inline (fast, few API calls)

## Error Recovery

| Phase | Failure | Action |
|-------|---------|--------|
| Phase 1 | Calendar API error | Report error, continue to Phase 2 |
| Phase 2 | Gmail API error | Report partial results, continue to Phase 3 |
| Phase 2 | Playwright timeout | Skip that article, note in digest |
| Phase 2 | docx generation fails | Report error, continue |
| Phase 3 | Drive upload fails | Save files locally, report paths |
| Any | Auth expired | Prompt: `gws auth login -s drive,gmail,calendar` |

## Security Rules

- All security rules from `gmail-daily-triage` apply
- Never auto-send emails
- Never delete calendar events
- Confirm before creating Gmail filters
- Never upload files containing credentials or secrets
