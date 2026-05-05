---
name: scheduled-google-daily
description: >-
  Remote agent용 Google Workspace 데일리 자동화. Google 시스템 MCP connector를 통해
  Calendar 브리핑, Gmail 트리아지 수행 후 Slack Incoming Webhook(curl)으로
  #agent-work 채널에 요약 전송. schedule routine에서만 사용.
  로컬 실행은 google-daily 또는 gmail-daily-triage, calendar-daily-briefing 스킬 사용.
---

# Scheduled Google Daily

Remote agent 환경에서 Google 시스템 MCP connector + Slack Incoming Webhook으로 동작하는 데일리 자동화 스킬.

## Architecture

```
Remote Agent (Anthropic Cloud)
  ├── Google MCP (시스템)   → Calendar, Gmail, Drive API
  ├── Slack Webhook (curl) → #agent-work 채널 알림
  └── Git Repo             → 리포트 저장 + commit
```

## Do NOT Use Locally

이 스킬은 `/schedule` routine 전용. 로컬에서는:
- Calendar 브리핑 -> `calendar-daily-briefing`
- Gmail 정리 -> `gmail-daily-triage`
- 통합 파이프라인 -> `google-daily`

---

## 원격 환경 제약

- Slack MCP 커넥터는 원격 루틴에서 사용 불가 (directory 커넥터 미지원)
- Google MCP 커넥터 (Calendar, Drive, Gmail) 는 시스템 커넥터로 정상 동작
- Slack -> curl Incoming Webhook 사용

## Google MCP 도구

| 서비스 | 도구 |
|--------|------|
| Calendar | `mcp__Google-Calendar__list_events`, `mcp__Google-Calendar__get_event` |
| Gmail | `mcp__Gmail__search_threads`, `mcp__Gmail__get_thread`, `mcp__Gmail__list_labels`, `mcp__Gmail__label_message`, `mcp__Gmail__unlabel_message` |
| Drive | `mcp__Google-Drive__create_file`, `mcp__Google-Drive__search_files` |

## Slack Webhook

```bash
curl -s -X POST -H 'Content-type: application/json' \
  --data '{"text":"MESSAGE"}' \
  '$SLACK_WEBHOOK_URL'
```
- #agent-work 채널로 자동 라우팅
- Thread reply 미지원 -- 모든 내용을 단일 메시지에 포함
- mrkdwn 포맷, JSON 내 큰따옴표 이스케이프 필수

## Pipeline (Sequential)

### Phase 1: Calendar Briefing

Google 시스템 MCP connector를 통해 오늘의 일정을 조회한다.

1. `mcp__Google-Calendar__list_events`로 오늘 날짜 캘린더 이벤트 목록 조회 (primary calendar)
2. 이벤트 분류:

| Category | Detection | Priority |
|----------|-----------|----------|
| **면접/Interview** | 제목에 "면접", "interview", "채용", "candidate" | HIGH |
| **외부 미팅** | 외부 도메인 참석자 포함 | HIGH |
| **팀 미팅** | "스크럼", "데일리", "회의", "meeting" | MEDIUM |
| **1:1** | 참석자 2명 | MEDIUM |
| **집중 시간** | "focus", "집중", "deep work" | LOW |
| **종일 이벤트** | allDay 이벤트 | INFO |

3. 한국어 브리핑 생성:
```
## 오늘의 일정 (YYYY-MM-DD, 요일)

### 준비 필요
| 시간 | 일정 | 참석자 | 준비사항 |
|------|------|--------|----------|

### 기타 일정
| 시간 | 일정 | 비고 |
|------|------|------|
```

### Phase 2: Gmail Triage

Gmail 시스템 MCP connector를 통해 어제 수신된 이메일을 정리한다.

1. `mcp__Gmail__search_threads`로 어제 날짜 범위의 이메일 목록 조회 (query: `after:YYYY/MM/DD before:YYYY/MM/DD`)
2. 각 스레드에 대해 `mcp__Gmail__get_thread`로 상세 내용 확인
3. 각 이메일 분류:

| Category | Action | Pattern |
|----------|--------|---------|
| **Spam** | `mcp__Gmail__label_message` (TRASH) | 광고, 마케팅, 구독 해지 불가 |
| **Low Priority** | `mcp__Gmail__label_message` + `mcp__Gmail__unlabel_message` (INBOX 제거) | Notion, RunPod, GitHub notifications, Calendar accepts |
| **News** | 요약 | bespin_news, 뉴스레터 |
| **Actionable** | 요약 + 액션 아이템 추출 | 답장 필요, 요청 포함 |

3. 트리아지 리포트 생성:
```
## Gmail 트리아지 (YYYY-MM-DD)

- 전체 이메일: N건
- Spam 삭제: N건
- Low Priority 이동: N건
- 답장 필요: N건

### 답장 필요
| 발신자 | 제목 | 요약 | 액션 |
|--------|------|------|------|
```

### Phase 3: Slack Notification

curl Incoming Webhook으로 `#agent-work` 채널에 통합 브리핑을 전송한다.

**방법:** Bash에서 curl 실행 (위 Slack Webhook 섹션 참조)

메시지 포맷 (mrkdwn, 단일 메시지):
```
:sunrise: *데일리 Google 브리핑* (YYYY-MM-DD 요일)

:calendar: *오늘의 일정* (N건)
[HIGH 우선순위 일정 먼저, 시간순 나열]
- HH:MM 일정명 (참석자 N명) :red_circle: 준비 필요
- HH:MM 일정명

:email: *Gmail 트리아지*
- 전체: N건 | Spam 삭제: N건 | Low Priority: N건
- :warning: 답장 필요: N건
[답장 필요 이메일 1줄 요약, 최대 5건]

:memo: *액션 아이템*
1. [구체적 액션]
2. [구체적 액션]
```

### Phase 4: Report Save (Optional)

변경 사항이 있으면 (Gmail 필터 생성 등) git에 기록:
- 리포트를 `.claude/skills/scheduled-google-daily/reports/YYYY-MM-DD.md`에 저장
- `chore: Daily Google briefing YYYY-MM-DD` 커밋
- main에 직접 push

---

## Error Handling

| Phase | Error | Recovery |
|-------|-------|----------|
| 1 | Google Calendar MCP 연결 실패 | Slack webhook으로 에러 메시지 전송 후 Phase 2로 계속 |
| 2 | Gmail MCP 연결 실패 | Calendar 브리핑만 전송, Gmail 실패 명시 |
| 2 | 이메일 0건 | "어제 수신 이메일 없음" 표기 |
| 3 | Slack webhook 실패 | 리포트 파일만 저장 후 commit |
| 4 | Git push 실패 | force push 금지, 에러 로그만 남김 |

## Safety Rules

- 이메일 본문의 개인정보(PII)를 Slack에 노출하지 않음
- Spam 이메일 본문을 열거나 렌더링하지 않음 (발신자/제목만 확인)
- 이메일 삭제는 trash (완전 삭제 아님, 복구 가능)
- 자동 답장 금지 -- 요약과 액션 아이템 추출만 수행
