# Meeting Prep

Prepare comprehensive context for the next upcoming meeting: attendees, recent email threads, related Drive documents, and suggested talking points.

## When to Use

User says: "prep my meeting", "meeting prep", "prepare for my next meeting", "what do I need for the meeting", "미팅 준비", "다음 미팅 준비해줘"

## Workflow

### Step 1: Find the Next Meeting

```bash
gwcli calendar events --days 1 --format json
```

Parse the JSON response and select the next upcoming event (closest start time in the future). Extract:
- Event ID
- Summary (title)
- Start/end time
- Description (may contain agenda or links)
- Attendees (list of emails and names)
- Location or conferencing link
- Organizer

If no events today, expand to 3 days:

```bash
gwcli calendar events --days 3 --format json
```

If the user specifies a particular meeting, search for it:

```bash
gwcli calendar search "MEETING_TITLE" --format json
```

### Step 2: Research Attendees via Email

For each attendee (up to 5), search recent email threads:

```bash
gwcli gmail search "from:attendee@company.com" --format json
```

For the most relevant thread (most recent or most active), read the full message:

```bash
gwcli gmail read <message-id> --format json
```

Extract:
- Last topic discussed
- Any pending action items
- Tone and relationship context

### Step 3: Find Related Documents

Search Drive for documents related to the meeting topic:

```bash
gwcli drive search "name contains 'MEETING_KEYWORD'" --format json
```

Use keywords from:
- The meeting title
- The meeting description
- Recent email subjects with attendees

If documents are found, note their names, last modified dates, and IDs for reference.

### Step 4: Produce the Prep Document

Output a structured meeting prep in Korean:

```markdown
# 미팅 준비 -- {meeting title}

## 기본 정보
- **일시**: {start} ~ {end}
- **장소/링크**: {location or Meet/Zoom link}
- **주최자**: {organizer name}

## 참석자 ({count}명)
| 이름 | 이메일 | 최근 소통 내용 |
|------|--------|----------------|
| 홍길동 | hong@co.com | 지난주 프로젝트 진행 상황 논의 |
| 김철수 | kim@co.com | 예산 승인 요청 메일 (3/5) |

## 안건/맥락
{meeting description에서 추출한 안건}

{description이 없으면:}
참석자와의 최근 이메일 내용을 기반으로 추정되는 주제:
- {topic 1 from email threads}
- {topic 2 from email threads}

## 관련 문서
- [{doc name}](https://drive.google.com/file/d/{id}) -- 최종 수정: {date}
- {없으면: "관련 문서 없음"}

## 제안 토킹 포인트
1. {참석자 이메일에서 파악한 핵심 이슈}
2. {이전 미팅 후속 조치 확인}
3. {agenda 항목에 대한 준비 사항}

## 사전 확인 필요 사항
- [ ] {확인이 필요한 데이터나 수치}
- [ ] {준비해야 할 자료}
```

## Error Handling

| Issue | Resolution |
|-------|------------|
| No upcoming meetings | Report "No meetings scheduled in the next 3 days" |
| No email history with attendee | Note "No recent email history" for that attendee |
| No Drive documents found | Note "No related documents found" and skip section |
| External attendee (no email history) | Note as "External contact -- no internal email history" |
