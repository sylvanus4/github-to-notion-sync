# Weekly Digest

Weekly summary for planning: this week's calendar, email backlog, important threads, and action items.

## When to Use

User says: "weekly digest", "weekly summary", "what's my week", "Monday morning summary", "plan my week", "주간 요약", "이번 주 뭐 있어", "한 주 정리"

## Workflow

### Step 1: Fetch This Week's Calendar

```bash
gwcli calendar events --days 7 --format json
```

Parse and organize events by day:
- Count total meetings per day
- Identify meeting-heavy days vs. focus days
- Flag any conflicts or back-to-back meetings
- Note recurring vs. one-off meetings

### Step 2: Fetch Unread Email Backlog

```bash
gwcli gmail list --unread --limit 50 --format json
```

Categorize by:
- Sender frequency (who's emailing you most)
- Age (how long unread)
- Thread depth (ongoing conversations vs. new)

### Step 3: Find Important/Starred Emails

```bash
gwcli gmail search "is:important" --format json
```

```bash
gwcli gmail search "is:starred" --format json
```

These are emails the system or user has flagged as important. Read the top 3:

```bash
gwcli gmail read <message-id> --format json
```

### Step 4: Identify Action Items from Recent Threads

Search for emails with action-oriented language:

```bash
gwcli gmail search "subject:(action OR todo OR deadline OR review OR approve) newer_than:7d" --format json
```

### Step 5: Produce the Weekly Digest

Output a structured weekly overview in Korean:

```markdown
# 주간 다이제스트 -- {week range, e.g., 3/10 ~ 3/14}

## 주간 캘린더 요약

| 요일 | 미팅 수 | 주요 일정 |
|------|---------|-----------|
| 월 (3/10) | 3건 | 팀 스탠드업, 클라이언트 미팅, 1:1 |
| 화 (3/11) | 1건 | 주간 리뷰 |
| 수 (3/12) | 0건 | **포커스 데이** |
| 목 (3/13) | 2건 | 전략 회의, 외부 미팅 |
| 금 (3/14) | 1건 | 팀 회고 |

**총 미팅**: {total}건 | **포커스 가능 시간**: ~{hours}시간

{일정 충돌 경고: 있으면 표시}

## 이메일 현황

- **미확인 메일**: {unread_count}건
- **중요 표시**: {important_count}건
- **별표 표시**: {starred_count}건
- **가장 오래된 미확인**: {oldest unread date and subject}

### 주요 발신자 (미확인 기준)
| 발신자 | 미확인 수 | 최근 제목 |
|--------|-----------|-----------|
| boss@company.com | 5건 | Re: Q2 계획 |
| client@ext.com | 3건 | 프로젝트 업데이트 |

## 액션 아이템

### 긴급 (이번 주 내 처리)
1. {subject} from {sender} -- {deadline if mentioned}
2. {subject} from {sender}

### 보류 중 (팔로업 필요)
- {thread subject} -- 마지막 응답: {date}
- {thread subject} -- {days}일 전 요청, 응답 없음

## 이번 주 추천 우선순위
1. **월요일**: {가장 긴급한 이메일 처리} + {미팅 준비}
2. **수요일 (포커스)**: {딥워크 항목}
3. **금요일**: {주간 마무리 + 다음 주 준비}
```

## Error Handling

| Issue | Resolution |
|-------|------------|
| No calendar events this week | Report "No meetings this week -- full focus week" |
| Very large unread count (>100) | Limit to 50 most recent, report total |
| No important/starred emails | Skip that section, note "No flagged emails" |
| gwcli timeout | Retry once after 5 seconds |
