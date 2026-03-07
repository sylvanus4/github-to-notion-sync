# Morning Sweep

Daily morning briefing that combines email triage, today's calendar, and task classification into a single actionable report.

## When to Use

User says: "morning sweep", "start my day", "morning briefing", "daily briefing", "what needs my attention", "아침 브리핑", "오늘 뭐해야해"

## Workflow

### Step 1: Fetch Today's Calendar

```bash
gwcli calendar events --days 1 --format json
```

Parse the JSON response and extract:
- Event summary (title)
- Start/end times
- Attendees (names and emails)
- Location (if any)
- Meeting links (Google Meet, Zoom, etc.)

Sort events chronologically. Flag any conflicts (overlapping times).

### Step 2: Fetch Unread Emails

```bash
gwcli gmail list --unread --limit 20 --format json
```

For each email, extract:
- Message ID
- From (sender name and email)
- Subject
- Date received
- Snippet (preview text)

### Step 3: Read Important Emails

For emails that appear urgent or from key contacts, read the full content:

```bash
gwcli gmail read <message-id> --format json
```

Indicators of importance:
- From a known contact or manager
- Subject contains: "urgent", "action required", "deadline", "ASAP", "review"
- Received in the last 12 hours
- Part of an ongoing thread

Read up to 5 important emails in full. Summarize the rest from snippets.

### Step 4: Classify Items

Apply the 4-category framework to all items (emails + calendar events):

**Green (Dispatch)** -- Agent can handle fully:
- Simple acknowledgment emails ("Thanks", "Got it")
- Calendar RSVP responses
- Newsletter/notification emails (archive)
- FYI-only emails with no action needed

**Yellow (Prep)** -- 80% ready, human reviews:
- Emails requiring a substantive reply (draft the reply)
- Meeting invites needing acceptance/decline decision (summarize context)
- Follow-up emails where prior context is needed (gather the context)

**Red (Yours)** -- Requires human judgment:
- Strategic decisions, pricing, sensitive communications
- Emails from executives or key clients
- Calendar conflicts requiring prioritization
- Anything involving money, contracts, or personnel

**Gray (Skip)** -- Not actionable today:
- Newsletters to read later
- Low-priority FYIs
- Events more than 24 hours away
- Threads where you're CC'd but not required to act

### Step 5: Produce the Briefing

Output a structured markdown briefing in Korean:

```markdown
# 모닝 브리핑 -- {today's date}

## 오늘의 일정 ({count}건)
| 시간 | 일정 | 참석자 | 장소/링크 |
|------|------|--------|-----------|
| 09:00-10:00 | 팀 스탠드업 | 홍길동 외 3명 | Google Meet |
| ... | ... | ... | ... |

{일정 충돌이 있으면 여기에 경고}

## 이메일 트리아지 ({unread_count}건 미확인)

### 🟢 Dispatch (에이전트 처리 가능)
- [Subject] from Sender -- {1줄 요약 및 제안 액션}

### 🟡 Prep (검토 후 처리)
- [Subject] from Sender -- {요약 + 초안/옵션 준비됨}

### 🔴 Yours (직접 판단 필요)
- [Subject] from Sender -- {왜 중요한지 + 컨텍스트}

### ⚪ Skip (오늘 보류)
- {count}건 뉴스레터/알림 -- 나중에 확인

## 추천 액션
1. {가장 긴급한 Red 항목}
2. {두 번째 우선순위}
3. {Yellow 항목 중 가장 중요한 것}
```

## Error Handling

| Issue | Resolution |
|-------|------------|
| gwcli returns empty email list | Report "Inbox zero" -- no unread emails |
| gwcli returns empty calendar | Report "No meetings today -- focus day" |
| gwcli auth error | Tell user to re-authenticate: `gwcli profiles add work --client <path>` |
| Too many unread emails (>50) | Limit to 20 most recent, note total count |
