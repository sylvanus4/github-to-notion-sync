---
name: calendar-daily-briefing
description: >-
  Fetch today's Google Calendar events and produce a concise Korean briefing
  with preparation alerts for meetings and interviews. Use when the user asks
  for "today's schedule", "calendar briefing", "오늘 일정", "캘린더 브리핑",
  "daily briefing", "오늘 미팅", "일정 요약", or "what's on my calendar".
  Do NOT use for creating events (use gws-calendar), email triage
  (use gmail-daily-triage), or weekly digests (use ai-chief-of-staff).
metadata:
  author: thaki
  version: 1.0.0
---

# Calendar Daily Briefing

Fetch today's calendar events, classify them, and produce a concise Korean briefing highlighting meetings and interviews that need preparation.

> **Prerequisites**: `gws` CLI installed and authenticated. See `gws-workspace` skill.

## Workflow

### Step 1: Fetch Today's Events

```bash
gws calendar +agenda --today
```

If JSON output is needed for parsing:

```bash
gws calendar events list \
  --params '{"calendarId": "primary", "timeMin": "YYYY-MM-DDT00:00:00+09:00", "timeMax": "YYYY-MM-DDT23:59:59+09:00", "singleEvents": true, "orderBy": "startTime"}' \
  --format json
```

Replace `YYYY-MM-DD` with today's date.

### Step 2: Classify Events

For each event, classify into one of these categories:

| Category | Detection | Priority | Action |
|----------|-----------|----------|--------|
| **Interview** | Title/description contains: "면접", "interview", "채용", "candidate", "지원자" | HIGH | Alert: prepare questions, review resume |
| **External Meeting** | Has attendees from non-company domains | HIGH | Alert: prepare agenda, review context |
| **Team Meeting** | Title contains: "스크럼", "scrum", "데일리", "daily", "스프린트", "sprint", "회의", "meeting" | MEDIUM | Note: check agenda/action items |
| **1:1** | Exactly 2 attendees (including self) | MEDIUM | Note: prepare talking points |
| **Focus Time** | Title contains: "집중", "focus", "deep work", "리팩토링" | LOW | Note: block protected |
| **All-day Event** | No specific start/end time | INFO | Note only |
| **Personal** | Calendar is not primary or title contains personal keywords | INFO | Note only |

### Step 3: Generate Briefing

Output a structured Korean briefing:

```markdown
## 오늘의 일정 브리핑 (YYYY-MM-DD, 요일)

### 준비 필요 (HIGH)
| 시간 | 일정 | 장소 | 참석자 | 준비사항 |
|------|------|------|--------|----------|
| HH:MM-HH:MM | 일정명 | 장소 | N명 | 준비 내용 |

### 미팅 (MEDIUM)
| 시간 | 일정 | 장소 | 참석자 |
|------|------|------|--------|
| HH:MM-HH:MM | 일정명 | 장소 | N명 |

### 기타
| 시간 | 일정 | 비고 |
|------|------|------|
| HH:MM-HH:MM | 일정명 | 메모 |

### 집중 가능 시간
- HH:MM ~ HH:MM (N시간)
- HH:MM ~ HH:MM (N시간)

### 요약
- 총 N개 일정 (면접 N, 미팅 N, 기타 N)
- 첫 일정: HH:MM
- 마지막 일정: HH:MM
```

### Step 4: Preparation Alerts

For HIGH priority events, provide specific preparation guidance:

**Interviews**:
- "면접 준비: 지원자 이력서 확인, 질문 리스트 준비"
- "예상 소요 시간: N분"

**External Meetings**:
- "외부 미팅: 참석자 [이름] 확인, 안건 준비"
- "장소: [위치] 이동 시간 고려"

**Meetings with linked documents**:
- If event description contains Drive links, note: "관련 문서 확인 필요"

## Free Time Calculation

Calculate gaps between events (minimum 30 minutes) as focus time blocks.
Business hours: 09:00 - 18:00 KST.
Exclude lunch (12:00-13:00) from focus time unless no event overlaps.

## Examples

### Example 1: Busy day with interview

User: "오늘 일정 요약해줘"

Result:
```
## 오늘의 일정 브리핑 (2026-03-10, 화)

### 준비 필요 (HIGH)
| 시간 | 일정 | 장소 | 참석자 | 준비사항 |
|------|------|------|--------|----------|
| 14:00-15:00 | ML엔지니어 면접 | D회의실 | 3명 | 지원자 이력서 확인, 기술 질문 준비 |

### 미팅 (MEDIUM)
| 시간 | 일정 | 장소 | 참석자 |
|------|------|------|--------|
| 10:30-11:00 | Research 데일리 스크럼 | D회의실 | 4명 |
| 13:00-13:15 | 기획 스프린트 | D회의실 | 5명 |

### 집중 가능 시간
- 09:00 ~ 10:30 (1.5시간)
- 15:00 ~ 18:00 (3시간)
```

### Example 2: Empty calendar

User: "what's on my calendar"

Result: "오늘은 일정이 없습니다. 집중 업무에 활용하세요!"

## Error Handling

| Situation | Action |
|-----------|--------|
| gws auth expired | Prompt: `gws auth login -s calendar` |
| No events today | Report "오늘은 일정이 없습니다. 집중 업무에 활용하세요!" |
| Multiple calendars | Aggregate all calendars, note which calendar each event belongs to |
| All-day events only | Report them but note "시간별 일정 없음" |
