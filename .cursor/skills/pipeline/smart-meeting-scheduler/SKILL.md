---
name: smart-meeting-scheduler
description: >-
  Find conflict-free calendar slots, invite attendees, and create an agenda from
  email or Slack context. Handles the full lifecycle from "we need to meet" to a
  calendar event with agenda and pre-read materials. Use when the user asks to
  "schedule a meeting", "find a time to meet", "book a meeting", "미팅 잡아줘",
  "회의 예약", "캘린더에서 빈 시간 찾아줘", "smart-meeting-scheduler", or when
  an email thread implies a meeting is needed. Do NOT use for viewing today's
  schedule (use calendar-daily-briefing), managing existing events (use
  gws-calendar directly), or full daily Google Workspace automation (use
  google-daily).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "comms-automation"
---
# smart-meeting-scheduler

Find conflict-free calendar slots, invite attendees, and create an agenda from email or Slack context.

## Workflow

1. **Detect meeting need** — Parse email thread or Slack message to identify required attendees, topic, urgency, and preferred duration
2. **Availability check** — Query `gws-calendar` for each attendee's free/busy slots over the next 5 business days
3. **Slot selection** — Find optimal slot (minimizes scheduling distance, respects timezone preferences, avoids early morning/late evening)
4. **Agenda generation** — Generate a structured agenda from the conversation context; attach relevant documents from `gws-drive` if referenced
5. **Send invite** — Create calendar event via `gws-calendar` with agenda in description and document links

## Composed Skills

- `gws-calendar` — Free/busy queries and event creation
- `gws-gmail` — Email thread parsing for meeting context
- `gws-drive` — Document attachment lookup

## Error Handling

| Error | Action |
|-------|--------|
| No common free slots found in 5-day window | Expand search to 10 business days; if still none, report top-3 least-conflict options |
| Attendee email not recognized by Calendar API | Ask user to confirm the attendee's Google-compatible email address |
| gws-calendar auth failure | Prompt user to re-authenticate via `gws auth login` |
| Ambiguous attendee name (multiple matches) | Present candidates and ask user to select |
| Meeting duration not specified | Default to 30 minutes; confirm with user before creating |

## Examples

```
User: "김팀장, 박과장이랑 다음 주에 30분 미팅 잡아줘. 주제는 Q3 로드맵 리뷰"
→ Checks 3 people's calendars, finds optimal slot, creates event with Q3 roadmap review agenda

User: "이 메일 스레드 기반으로 미팅 잡아줘"
→ Parses email participants and topic, finds time, sends invite
```
