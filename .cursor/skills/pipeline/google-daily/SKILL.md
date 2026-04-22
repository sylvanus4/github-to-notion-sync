---
name: google-daily
description: >-
  Google Workspace 데일리 자동화: 캘린더 브리핑, Gmail 정리, Drive 업로드, Slack 알림(쓰레드 포함), 메모리
  동기화를 순차 실행. /google, "google daily", "구글 데일리" 등으로 호출. 개별 작업은 해당 스킬 사용.
  Do NOT use for individual Google Workspace operations (use the specific gws-* skill).
metadata:
  author: "thaki"
  version: "3.1.0"
  category: "execution"
---
# Google Daily Automation

Google Workspace 일일 작업을 순차 파이프라인으로 실행하는 마스터 오케스트레이터.

> **Prerequisites**: `gws` CLI 설치 및 인증 (`gws auth login -s drive,gmail,calendar`). See `gws-workspace` skill.

## Pipeline

```
Calendar → Gmail Triage → Drive Upload → Slack Notify (+ threads) → Memory Sync → Orphan Cleanup
```

All intermediate and final aggregation steps persist to `outputs/google-daily/{date}/` (see Pipeline Output Protocol).

## Slack Configuration

| Key | Value |
|-----|-------|
| Channel | `#효정-할일` |
| Channel ID | `C0AA8NT4T8T` |
| Decision (Personal) | `#효정-의사결정` |
| Decision (Personal) ID | `C0ANBST3KDE` |
| Decision (Team) | `#ai-리더방` |
| Decision (Team) ID | `C0A6Q7007N2` |

All Slack messages go to `#효정-할일`. Decision items go to their respective channels. Never use DM.

## Pipeline Output Protocol (File-First)

### Initialization (before Phase 1)

1. Resolve run date `YYYY-MM-DD` (KST unless specified).
2. Create output directory: `outputs/google-daily/{date}/` (mkdir -p).
3. Write initial `outputs/google-daily/{date}/manifest.json` with:
   - `pipeline`: `"google-daily"`
   - `date`: `{date}`
   - `started_at`: ISO-8601 timestamp
   - `completed_at`: `null`
   - `phases`: `[]` (populated as phases complete)
   - `flags`: `{}` (e.g. `skip_decisions` when CLI/skill flag `skip-decisions` is set)
   - `overall_status`: `"running"`
   - `warnings`: `[]`
4. Set `MANIFEST_PATH=outputs/google-daily/{date}/manifest.json` for all subsequent updates.

### Per-phase files and manifest

- **Output directory**: `outputs/google-daily/{date}/`
- **Phase files**: `phase-{N}-{label}.json` — one JSON file per phase (see Output Artifacts table below).
- **Manifest**: `manifest.json` in the same directory tracks all phases and overall status.

**Subagent Return Contract:** Any subagent delegated to a phase returns **only**:

```json
{ "status": "ok|failed|skipped", "file": "outputs/google-daily/{date}/phase-N-label.json", "summary": "one-line outcome" }
```

The orchestrator persists full phase payloads to `file`; subagents must not rely on the parent retaining large blobs in context.

**Final aggregation rule:** Phases that produce user-facing summaries (Slack main post, threads, MEMORY.md, orphan-cleanup note) **read inputs exclusively** from `manifest.json` and the phase `phase-*.json` files under `outputs/google-daily/{date}/`. Do **not** compose Slack or MEMORY content from in-context conversation memory or undumped subagent transcripts.

### manifest.json schema

| Field | Type | Description |
|-------|------|-------------|
| `pipeline` | string | Always `"google-daily"`. |
| `date` | string | Run date `YYYY-MM-DD`. |
| `started_at` | string | ISO-8601 when run started. |
| `completed_at` | string \| null | ISO-8601 when run finished; `null` while running. |
| `phases` | array | Ordered phase records (see below). |
| `flags` | object | Pipeline flags (e.g. `skip_decisions: true`). |
| `overall_status` | string | `running`, `ok`, `partial`, or `failed`. |
| `warnings` | array of string | Non-fatal issues (e.g. partial Slack). |

Each element of `phases`:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | e.g. `"1"`, `"2"`, `"3-5"`. |
| `label` | string | Short phase name. |
| `status` | string | `ok`, `failed`, `skipped`. |
| `output_file` | string | Path to `phase-*.json` for this phase. |
| `started_at` | string | ISO-8601. |
| `elapsed_ms` | number | Wall time for the phase. |
| `summary` | string | One-line outcome. |

On successful completion, set `completed_at`, set `overall_status` from worst phase (`failed` > `partial` > `ok`), and append any warnings.

### Output Artifacts

| Phase | Label | Output file | Notes |
|-------|-------|-------------|-------|
| 1 | calendar | `outputs/google-daily/{date}/phase-1-calendar.json` | Agenda, briefing text, focus windows |
| 2 | gmail | `outputs/google-daily/{date}/phase-2-gmail.json` | Triage counts, colleague_emails, news arrays, paths to docx |
| 3 | drive | `outputs/google-daily/{date}/phase-3-drive.json` | Folder URL, uploaded file links or skip reason |
| 3.5 | quality-gate | `outputs/google-daily/{date}/phase-3-5-quality-gate.json` | Gate checklist result, partial_ok flag |
| 4 | slack | `outputs/google-daily/{date}/phase-4-slack.json` | `main_message_ts`, thread metadata, post counts |
| 4.5 | decisions | `outputs/google-daily/{date}/phase-4-5-decisions.json` | Decision posts emitted or skipped |
| 5 | memory | `outputs/google-daily/{date}/phase-5-memory.json` | MEMORY.md entry text or path written |
| 6 | orphan-cleanup | `outputs/google-daily/{date}/phase-6-orphan-cleanup.json` | Script JSON summary, one-line user message |

## Phase 1 -- Calendar Briefing

`.cursor/skills/pipeline/calendar-daily-briefing/SKILL.md` 실행.

```bash
gws calendar +agenda --today
```

1. 이벤트 분류: 면접(HIGH), 외부미팅(HIGH), 팀미팅(MEDIUM), 집중시간(LOW)
2. 한국어 브리핑 생성 + 준비 알림
3. 집중 가능 시간대 계산 (09:00-18:00 기준, 30분 이상 공백)

**Persist & manifest:** Write full Phase 1 result (raw agenda summary, classified events, Korean briefing text, focus windows, errors if any) to `outputs/google-daily/{date}/phase-1-calendar.json`. Update `manifest.json`: append phase record `id: "1"`, `label: calendar`, `output_file`, `status`, `started_at`, `elapsed_ms`, `summary`. If a subagent runs this phase, it returns only `{ status, file, summary }`; the orchestrator writes the JSON file and updates the manifest.

## Phase 2 -- Gmail Triage

`.cursor/skills/pipeline/gmail-daily-triage/SKILL.md` 실행.

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

**Collect structured output** and persist to `phase-2-gmail.json` (downstream phases read this file, not context):
- `colleague_emails[]`: list of {sender, subject, summary, draft_reply, attachment_summary}
- `news_articles[]`: list of {title, url, summary}
- `news_insights[]`: 3-5 AI/GPU Cloud insight bullets
- `triage_counts`: {spam, notifications, colleague, news, reply_needed}
- `reply_needed[]`: items for decision scanning (align with docx content)
- `docx_paths`: paths to generated docx files

**Persist & manifest:** Write the complete structured object to `outputs/google-daily/{date}/phase-2-gmail.json`. Update `manifest.json` with phase `id: "2"`, `label: gmail`, and the slim subagent contract if delegated. Phase 4 and 4.5 load colleague/news/reply data **only** from this file (and manifest), not from chat memory.

## Phase 3 -- Drive Upload

생성된 문서가 있을 때만 실행. 없으면 건너뛰기.

```bash
gws drive files create \
  --json '{"name": "Google Daily - YYYY-MM-DD", "mimeType": "application/vnd.google-apps.folder"}'

gws drive +upload /tmp/bespin-news-YYYY-MM-DD.docx --parent FOLDER_ID
gws drive +upload /tmp/reply-needed-YYYY-MM-DD.docx --parent FOLDER_ID
```

Save Drive folder URL and file links to `outputs/google-daily/{date}/phase-3-drive.json` (not only in context).

**Persist & manifest:** Write `{ folder_url, file_links[], skipped: boolean, skip_reason?, errors? }` to `outputs/google-daily/{date}/phase-3-drive.json`. Update `manifest.json` with `id: "3"`, `label: drive`. If no uploads, set `skipped: true` and still write the file.

## Phase 3.5 -- Pre-Notification Quality Gate

Before posting to Slack, verify:
- [ ] Calendar summary exists and covers today's date (or Phase 1 explicitly failed with error logged)
- [ ] Gmail triage result includes counts (spam, notifications, colleague, news, reply-needed)
- [ ] Drive uploads (if any) completed without error; file links are captured
- [ ] `colleague_emails[]` and `news_articles[]` arrays are populated (empty is OK if no such emails exist)

If calendar or Gmail failed, post a partial briefing clearly marking missing sections with `[미완료]`. Do NOT silently omit sections.

**Validation inputs:** Read `phase-1-calendar.json`, `phase-2-gmail.json`, and `phase-3-drive.json` from disk; do not rely on unstored context.

**Persist & manifest:** Write gate result `{ checks_passed: boolean, partial_ok: boolean, notes[], failed_checks[] }` to `outputs/google-daily/{date}/phase-3-5-quality-gate.json`. Update `manifest.json` with `id: "3-5"`, `label: quality-gate`.

## Phase 4 -- Slack Notify (threaded)

**Input source (mandatory):** Build every Slack message body **only** from:
- `outputs/google-daily/{date}/manifest.json`
- `outputs/google-daily/{date}/phase-1-calendar.json`
- `outputs/google-daily/{date}/phase-2-gmail.json`
- `outputs/google-daily/{date}/phase-3-drive.json`
- `outputs/google-daily/{date}/phase-3-5-quality-gate.json`

Re-read these files immediately before posting. Do **not** substitute recalled chat context, subagent narrative, or unstored variables for counts, links, or text.

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

**Persist & manifest:** After all Slack steps (main + threads), write `outputs/google-daily/{date}/phase-4-slack.json` with `{ main_message_ts, thread_posts[], partial_failure?, channel_id }`. Update `manifest.json` with `id: "4"`, `label: slack`, `summary` including thread count. Subagents return only `{ status, file, summary }`; the orchestrator persists the full JSON.

## Phase 4.5 -- Decision Extraction

Skip if `skip-decisions` flag is set (record in `manifest.json` under `flags.skip_decisions`). After posting the main summary and threads to `#효정-할일`, scan for decision-worthy items using the `decision-router` skill rules.

**Input source (mandatory):** Load `colleague_emails[]`, `reply_needed[]`, and calendar overlap/HIGH-prep signals **only** from `phase-2-gmail.json` and `phase-1-calendar.json` on disk (plus `manifest.json` for flags). Do not use in-context memory.

**Step 4.5a — Scan colleague emails:**

Review `colleague_emails[]` (from `phase-2-gmail.json`) for decision keywords: 승인, 결정, 예산, 아키텍처, 채용, 제안, 검토 요청, approve, budget, architecture, hire, proposal, review.

- Emails requesting approval, budget, or architectural decisions → scope: **team**, post to `#ai-리더방` (`C0A6Q7007N2`)
- Emails with explicit questions requiring a personal response → scope: **personal**, post to `#효정-의사결정` (`C0ANBST3KDE`)

**Step 4.5b — Scan reply-needed emails:**

Review `reply_needed[]` (from `phase-2-gmail.json`) for items that require a decision (respond/ignore/delegate). Post to `#효정-의사결정` as personal decisions with MEDIUM urgency.

**Step 4.5c — Scan calendar conflicts:**

If `phase-1-calendar.json` indicates overlapping events or HIGH-priority meetings requiring prep decisions, post to `#효정-의사결정` as personal decisions with HIGH urgency.

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

**Persist & manifest:** Write `{ decisions_posted[], skipped_reason?, channel_posts[] }` to `outputs/google-daily/{date}/phase-4-5-decisions.json`. Update `manifest.json` with `id: "4-5"`, `label: decisions`.

## Phase 5 -- Memory Sync

**Input source (mandatory):** Compose the MEMORY.md entry **only** from `manifest.json` and the phase files `phase-1-calendar.json` through `phase-4-5-decisions.json` under `outputs/google-daily/{date}/`. Do not reconstruct from conversation memory.

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

Populate each bullet from the on-disk JSON fields (counts and summaries from `phase-1-calendar.json`, `phase-2-gmail.json`, `phase-4-slack.json`, `phase-4-5-decisions.json` as applicable).

This accumulates context so future sessions can reference past daily patterns, recurring senders, and action item history.

**Persist & manifest:** Write `{ memory_entry_markdown, memory_md_path: "MEMORY.md", appended: boolean }` to `outputs/google-daily/{date}/phase-5-memory.json`. Update `manifest.json` with `id: "5"`, `label: memory`.

## Phase 6 -- Slack Orphan Cleanup

Run `slack-orphan-cleaner` to delete orphaned thread replies (deleted parent, remaining replies) across #press, #deep-research, #ai-coding-radar, #idea. This phase is non-blocking — failures are logged but do not fail the pipeline.

```bash
set -a && source .env && set +a
python backend/scripts/cleanup_orphaned_threads.py --execute --json
```

Parse the JSON output and include a one-line summary in the Phase 4 Slack thread (if `main_message_ts` is available) or post a brief message to `#효정-할일`:
`Orphan cleanup: {deleted} deleted, {failed} failed across {N} channels`

**Input source:** Read `main_message_ts` from `outputs/google-daily/{date}/phase-4-slack.json` only (not from chat memory).

**Persist & manifest:** Write `{ script_output, deleted, failed, channels, summary_line }` to `outputs/google-daily/{date}/phase-6-orphan-cleanup.json`. Update `manifest.json` with `id: "6"`, `label: orphan-cleanup`. Set `manifest.completed_at`, `overall_status`, and `warnings` from all phase outcomes.

## Error Recovery

Resume from the **last successful `phase-*.json`** under `outputs/google-daily/{date}/` and the current `manifest.json`. Do not re-run completed phases unless their output files are missing or invalid.

| Phase | Failure | Action |
|-------|---------|--------|
| Calendar | API error | 에러 보고, Phase 2 계속 |
| Gmail | API error | 부분 결과 보고, Phase 3 계속 |
| Gmail | Browser/fetch timeout | 해당 기사 건너뛰기, "[접속 불가]" 표시 |
| Drive | Upload 실패 | 로컬 경로 안내 |
| Slack | Main message 실패 | 에러 보고, 사용자에게 직접 요약 표시 |
| Slack | Thread reply 실패 | 에러 보고, 계속 진행 |
| Memory | MEMORY.md 쓰기 실패 | 에러 보고, 요약은 정상 완료 |
| Orphan Cleanup | Script error | 에러 로그, 파이프라인 계속 |
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

## Coordinator Synthesis

When delegating to subagents:

- **Never use lazy delegation.** Provide specific inputs (file paths, data, context) to every subagent — not "based on your findings, do X."
- **Purpose statement required:** Every subagent prompt must include why the task matters and how its output is used downstream.
- **Continue vs Spawn decision:**
  - Continue (resume) when worker context overlaps with the next task or fixing a previous failure
  - Spawn fresh when verifying another worker's output or when previous approach was fundamentally wrong
- Use `model: "fast"` for exploration/read-only subagents; default model for generation/analysis

## Honest Reporting

- Report phase outcomes faithfully: if a phase fails, say so with the error output
- Never claim "pipeline complete" when phases were skipped or failed
- Never suppress failing phases to manufacture a green summary
- When a phase succeeds, state it plainly without unnecessary hedging
- The Slack summary must accurately reflect what happened — not what was hoped

## Subagent Contract

Subagent prompts must include:
- Always use absolute file paths (subagent cwd may differ)
- Return `{ status, file, summary }` for orchestrator context efficiency
- Include code snippets only when exact text is load-bearing
- Do not recap files merely read — summarize findings
- Final response: concise report of what was done, key findings, files changed
- Do not use emojis
