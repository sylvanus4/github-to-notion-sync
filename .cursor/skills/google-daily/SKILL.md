---
name: google-daily
description: >-
  Google Workspace 데일리 자동화: 캘린더 브리핑, Gmail 정리, Drive 업로드, Slack 알림(쓰레드 포함), 메모리
  동기화를 순차 실행. /google, "google daily", "구글 데일리" 등으로 호출. 개별 작업은 해당 스킬 사용.
  Do NOT use for individual Google Workspace operations (use the specific gws-* skill).
metadata:
  author: "thaki"
  version: "3.0.0"
  category: "execution"
---
# Google Daily Automation

Google Workspace 일일 작업을 순차 파이프라인으로 실행하는 마스터 오케스트레이터.

> **Prerequisites**: `gws` CLI 설치 및 인증 (`gws auth login -s drive,gmail,calendar`). See `gws-workspace` skill.

## Pipeline

```
Calendar → Gmail Triage → Drive Upload → Slack Notify (+ threads) → Memory Sync
```

## Slack Configuration

| Key | Value |
|-----|-------|
| Channel | `#효정-할일` |
| Channel ID | `C0AA8NT4T8T` |
| Decision (Personal) | `#효정-의사결정` |
| Decision (Personal) ID | `C0ANBST3KDE` |
| Decision (Team) | `#7층-리더방` |
| Decision (Team) ID | `C0A6Q7007N2` |

All Slack messages go to `#효정-할일`. Decision items go to their respective channels. Never use DM.

## Phase 1 -- Calendar Briefing

`.cursor/skills/calendar-daily-briefing/SKILL.md` 실행.

```bash
gws calendar +agenda --today
```

1. 이벤트 분류: 면접(HIGH), 외부미팅(HIGH), 팀미팅(MEDIUM), 집중시간(LOW)
2. 한국어 브리핑 생성 + 준비 알림
3. 집중 가능 시간대 계산 (09:00-18:00 기준, 30분 이상 공백)

## Phase 2 -- Gmail Triage

`.cursor/skills/gmail-daily-triage/SKILL.md` 실행.

1. "Low Priority" 라벨 확인/생성
2. 어제 메일 조회: `gws gmail +triage --max 50 --query "after:YYYY/MM/DD before:YYYY/MM/DD" --labels --format json`
3. 분류 및 처리:

| Category | Sender Pattern | Action |
|----------|---------------|--------|
| Spam | 광고, 마케팅 | `messages trash` |
| Notification | Notion, RunPod, GitHub, NotebookLM, Calendar | `messages modify` → Low Priority |
| News | bespin_news@bespinglobal.com | 링크 추출 → 기사 요약 → docx 생성 → AI/GPU Cloud 인사이트 |
| Colleague | @thakicloud.co.kr, @bespinglobal.com | 요약 + 답변 초안 작성 (첨부 있으면 첨부도 요약) |
| Reply Needed | 직접 수신 + 미답장 | 요약 + 액션아이템 → docx 생성 |

4. 생성 문서: `/tmp/reply-needed-YYYY-MM-DD.docx`, `/tmp/bespin-news-YYYY-MM-DD.docx`

**Collect structured output** from Phase 2 for use in Phase 4:
- `colleague_emails[]`: list of {sender, subject, summary, draft_reply, attachment_summary}
- `news_articles[]`: list of {title, url, summary}
- `news_insights[]`: 3-5 AI/GPU Cloud insight bullets
- `triage_counts`: {spam, notifications, colleague, news, reply_needed}

## Phase 3 -- Drive Upload

생성된 문서가 있을 때만 실행. 없으면 건너뛰기.

```bash
gws drive files create \
  --json '{"name": "Google Daily - YYYY-MM-DD", "mimeType": "application/vnd.google-apps.folder"}'

gws drive +upload /tmp/bespin-news-YYYY-MM-DD.docx --parent FOLDER_ID
gws drive +upload /tmp/reply-needed-YYYY-MM-DD.docx --parent FOLDER_ID
```

Save Drive folder URL and file links for Phase 4.

## Phase 3.5 -- Pre-Notification Quality Gate

Before posting to Slack, verify:
- [ ] Calendar summary exists and covers today's date (or Phase 1 explicitly failed with error logged)
- [ ] Gmail triage result includes counts (spam, notifications, colleague, news, reply-needed)
- [ ] Drive uploads (if any) completed without error; file links are captured
- [ ] `colleague_emails[]` and `news_articles[]` arrays are populated (empty is OK if no such emails exist)

If calendar or Gmail failed, post a partial briefing clearly marking missing sections with `[미완료]`. Do NOT silently omit sections.

## Phase 4 -- Slack Notify (threaded)

Three-step posting pattern using `slack_send_message` MCP tool.

### Step 1: Main Summary

Post the daily summary to `#효정-할일` (`C0AA8NT4T8T`). **Capture `message_ts` from the response** for thread replies.

```json
{
  "channel_id": "C0AA8NT4T8T",
  "message": "*Google 데일리 자동화 완료* (YYYY-MM-DD)\n\n*오늘의 일정*\n- 회의 N건, 면접 N건\n- 집중 가능: HH:MM~HH:MM\n\n*메일 정리*\n- 알림 정리: N건 → Low Priority\n- 팀원 메일: N건 (쓰레드 확인)\n- 뉴스: N건 (쓰레드 확인)\n- 답장 필요: N건\n\n*생성된 문서*\n- <DRIVE_LINK|bespin-news.docx>\n- <DRIVE_LINK|reply-needed.docx>\n\n*주의사항*\n- HIGH 우선순위 일정 알림"
}
```

### Step 2: Colleague Email Threads

For EACH colleague email, post a thread reply using `thread_ts`:

```json
{
  "channel_id": "C0AA8NT4T8T",
  "thread_ts": "MAIN_MESSAGE_TS",
  "message": "*[팀원 메일] {sender_name}* - {subject}\n\n*요약*\n{2-3 sentence summary}\n\n*답변 초안*\n> {draft reply text}\n\n{attachment_summary if any}"
}
```

Reply tone rules:
- `@thakicloud.co.kr` senders: team-casual tone
- `@bespinglobal.com` senders: formal business tone

### Step 3: Bespin News Thread (articles)

If bespin_news email exists, post a thread reply with article summaries:

```json
{
  "channel_id": "C0AA8NT4T8T",
  "thread_ts": "MAIN_MESSAGE_TS",
  "message": "*[뉴스 다이제스트]* Bespin News ({article_count}건)\n\n{for each article:\n*{title}*\n{2-sentence summary}\n<{url}|원문 보기>\n}\n\n문서: <DRIVE_LINK|bespin-news-YYYY-MM-DD.docx>"
}
```

### Step 4: Bespin News Insights Thread

Post a SEPARATE thread reply with AI/GPU Cloud insights analysis:

```json
{
  "channel_id": "C0AA8NT4T8T",
  "thread_ts": "MAIN_MESSAGE_TS",
  "message": "*[AI/GPU Cloud 핵심 인사이트]*\n_ThakiCloud 관점에서의 시사점_\n\n{3-5 numbered insight bullets, each 1-2 sentences}\n\nEach insight must cover one of:\n- Market trends (시장 트렌드)\n- Competitor moves (경쟁사 동향)\n- Technology shifts (기술 변화)\n- Customer pain points (고객 페인포인트)\n- Opportunities for ThakiCloud (사업 기회)"
}
```

Insight format example:
```
*1.* AI 에이전트 시장 폭발적 성장 → ThakiCloud 에이전트 플랫폼 포지셔닝 필요
*2.* AI 보안 취약점 실제 피해 발생 → 엔터프라이즈 배포 시 guardrails 필수
*3.* GPU 연산 수요 지속 증가 → 배치 처리 최적화 인프라 경쟁력 핵심
```

### Slack mrkdwn Rules

- `*bold*` (single asterisk only, never `**`)
- `_italic_` (underscore)
- `<url|text>` (links)
- No `## headers` -- use `*bold text*` on its own line
- `> quote` for draft replies

## Phase 4.5 -- Decision Extraction

Skip if `skip-decisions` flag is set. After posting the main summary and threads to `#효정-할일`, scan the collected data for decision-worthy items using the `decision-router` skill rules.

**Step 4.5a — Scan colleague emails:**

Review `colleague_emails[]` for decision keywords: 승인, 결정, 예산, 아키텍처, 채용, 제안, 검토 요청, approve, budget, architecture, hire, proposal, review.

- Emails requesting approval, budget, or architectural decisions → scope: **team**, post to `#7층-리더방` (`C0A6Q7007N2`)
- Emails with explicit questions requiring a personal response → scope: **personal**, post to `#효정-의사결정` (`C0ANBST3KDE`)

**Step 4.5b — Scan reply-needed emails:**

Review `reply_needed[]` for items that require a decision (respond/ignore/delegate). Post to `#효정-의사결정` as personal decisions with MEDIUM urgency.

**Step 4.5c — Scan calendar conflicts:**

If Phase 1 found overlapping events or HIGH-priority meetings requiring prep decisions, post to `#효정-의사결정` as personal decisions with HIGH urgency.

**Step 4.5d — Format and post:**

For each detected decision item, format using the DECISION template from `decision-router`:

```
*[DECISION]* {urgency_badge} | 출처: google-daily

*{Decision Title}*

*배경*
{1-3 sentence context}

*판단 필요 사항*
{What needs to be decided}

*옵션*
A. {option A} — {brief pro/con}
B. {option B} — {brief pro/con}
C. 보류 / 추가 조사 필요

*추천*
{recommended option with rationale}

*긴급도*: {HIGH / MEDIUM / LOW}
*원본*: <{slack_thread_link}|Google Daily {date}>
```

Post each decision as a separate message (not threaded) to the appropriate channel. Include decision posts in the Phase 5 Memory Sync entry.

## Phase 5 -- Memory Sync

Append a daily entry to `MEMORY.md` at the project root following the protocol in `.cursor/rules/self-improvement.mdc`.

```markdown
## [task] Google Daily (YYYY-MM-DD)

- Calendar: N events, {key meetings}
- Gmail: N emails triaged (spam: N, notifications: N, colleague: N, news: N, reply-needed: N)
- Colleague emails: {sender names and topics}
- News themes: {top 2-3 themes from Bespin digest}
- Action items: {any pending replies or follow-ups}
- Slack: summary + N threads posted to #효정-할일
```

This accumulates context so future sessions can reference past daily patterns, recurring senders, and action item history.

## Error Recovery

| Phase | Failure | Action |
|-------|---------|--------|
| Calendar | API error | 에러 보고, Phase 2 계속 |
| Gmail | API error | 부분 결과 보고, Phase 3 계속 |
| Gmail | Browser/fetch timeout | 해당 기사 건너뛰기, "[접속 불가]" 표시 |
| Drive | Upload 실패 | 로컬 경로 안내 |
| Slack | Main message 실패 | 에러 보고, 사용자에게 직접 요약 표시 |
| Slack | Thread reply 실패 | 에러 보고, 계속 진행 |
| Memory | MEMORY.md 쓰기 실패 | 에러 보고, 요약은 정상 완료 |
| Any | Auth expired | `gws auth login -s drive,gmail,calendar` 안내 |

## Security Rules

- 메일 자동 발송 금지 (답변 초안은 Slack 쓰레드에만 게시)
- 캘린더 이벤트 삭제 금지
- Gmail 필터 생성 전 사용자 확인
- credentials/secrets 포함 파일 업로드 금지
- 스팸 본문 열기 금지 (발신자/제목만으로 분류)

## Examples

### Example 1: Standard usage
**User says:** "google daily" or request matching the skill triggers
**Actions:** Execute the skill workflow as specified. Verify output quality.
**Result:** Task completed with expected output format.
