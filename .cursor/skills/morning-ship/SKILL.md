---
name: morning-ship
description: >-
  Start-of-day pipeline: git pull all 5 managed repos (ai-platform-webui via
  tmp branch), run Google Workspace briefing (calendar + Gmail triage), run the
  daily stock analysis pipeline, and post a consolidated morning briefing to
  Slack. Use when the user runs /morning-ship, asks to "start my day", "morning
  ship", "아침 시작", "출근 파이프라인", "morning pull all", or "pull and brief". Do NOT
  use for pulling a single repo (use git directly), running Google daily only
  (use google-daily), running the stock pipeline only (use today), or end-of-day
  shipping (use eod-ship).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# Morning Ship — Start-of-Day Multi-Project Pipeline

Pull latest changes from all managed repos, run Google Workspace briefing, kick off the daily stock pipeline, and post a consolidated morning briefing to Slack.

## Configuration

- **Managed projects**: See [eod-ship project-registry.md](../eod-ship/references/project-registry.md)
- **Slack channel**: `#효정-할일` (Channel ID: `C0AA8NT4T8T`)
- **Upstream skills**: `calendar-daily-briefing`, `gmail-daily-triage`, `today`

## Usage

```
/morning-ship                        # full pipeline (pull + google + stock + Slack)
/morning-ship --skip-pull            # skip git pull, start from Google daily
/morning-ship --skip-google          # skip calendar briefing and Gmail triage
/morning-ship --skip-stock           # skip daily stock pipeline
/morning-ship --targets research     # pull specific projects only (comma-separated)
/morning-ship --no-slack             # skip Slack notification
/morning-ship --dry-run              # preview only (no git pull, no triage, no pipeline)
```

Arguments can be combined freely. Defaults: pull all, run Google daily, run stock pipeline, post to Slack.

## Workflow

### Phase 1: Git Sync (Pull All Managed Projects)

**Skip if** `--skip-pull` or `--dry-run` flag is set.

**If `--targets` is set**, only pull the specified projects. Otherwise pull all 5.

Read project paths from [eod-ship project-registry.md](../eod-ship/references/project-registry.md).

**Path resolution**: Each project has two possible paths (`Path (회사)` and `Path (집)`). For each project, try `Path (회사)` first; if that directory does not exist, try `Path (집)`. Use the first path that exists. If neither exists, warn and skip the project.

For each project in order:

```bash
cd PROJECT_PATH    # resolved path from above
git fetch origin
```

1. Check if directory exists. If not, warn and skip.
2. Verify the working directory is clean (`git status --short`). If dirty, warn about uncommitted changes and skip pull for that project.
3. Pull based on mode:

| Mode | Pull Command | Notes |
|------|-------------|-------|
| `full` | `git pull` | Standard pull from default remote tracking branch |
| `tmp-only` | `git pull origin tmp` | ai-platform-webui only; always pulls from remote `tmp` |

4. Capture per-project result: `{project, branch, status, commits_pulled, conflicts}`
5. `cd` back to original directory before processing next project.

**Execution order** (from [eod-ship project-registry.md](../eod-ship/references/project-registry.md)):

1. `github-to-notion-sync` — `git pull`
2. `ai-template` — `git pull`
3. `ai-model-event-stock-analytics` — `git pull`
4. `research` — `git pull`
5. `ai-platform-webui` — `git pull origin tmp`

If a project directory does not exist, warn and skip it. Continue with remaining projects.

### Phase 2: Google Daily (Calendar + Gmail)

**Skip if** `--skip-google` or `--dry-run` flag is set.

Run two sub-skills sequentially:

#### Step 2a: Calendar Briefing

Follow the `calendar-daily-briefing` skill (`.cursor/skills/calendar-daily-briefing/SKILL.md`).

1. Fetch today's events via `gws calendar +agenda --today`
2. Classify events by priority: Interview(HIGH), External Meeting(HIGH), Team Meeting(MEDIUM), Focus Time(LOW)
3. Generate a Korean briefing with preparation alerts
4. Calculate focus-available time slots (09:00-18:00, gaps >= 30 min)
5. Capture output: `{events[], focus_slots[], high_priority_count, briefing_text}`

#### Step 2b: Gmail Triage

Follow the `gmail-daily-triage` skill (`.cursor/skills/gmail-daily-triage/SKILL.md`).

1. Ensure "Low Priority" label exists
2. Fetch yesterday's emails
3. Classify and process: Spam(trash), Notifications(Low Priority), News(docx), Colleague(summary+draft), Reply Needed(docx)
4. Generate documents: `/tmp/reply-needed-YYYY-MM-DD.docx`, `/tmp/bespin-news-YYYY-MM-DD.docx`
5. Capture output: `{triage_counts, colleague_emails[], news_articles[], news_insights[]}`

### Phase 3: Daily Stock Pipeline

**Skip if** `--skip-stock` or `--dry-run` flag is set.

Run the `today` skill (`.cursor/skills/today/SKILL.md`) with `--skip-slack` flag (Slack posting is handled in Phase 4 as a consolidated message).

1. Data Freshness Check (DB vs CSV)
2. Data Sync (CSV import + Yahoo Finance backfill)
3. Fundamental Data Sync (yfinance)
4. Hot Stock Discovery (NASDAQ 100 / KOSPI 100 / KOSDAQ 100)
5. Multi-Factor Screening
6. Turtle + Bollinger + Oscillator analysis
7. Report generation (.docx)
8. Capture output: `{stocks_analyzed, signals[], report_path, screener_results}`

### Phase 4: Slack Notification

**Skip if** `--no-slack` or `--dry-run` flag is set.

Post a consolidated morning briefing to `#효정-할일` using the `slack_send_message` MCP tool.

#### Step 1: Main Summary

```json
{
  "channel_id": "C0AA8NT4T8T",
  "message": "<Slack mrkdwn message>"
}
```

**Capture `message_ts` from the response** for thread replies.

**Message template** (Slack mrkdwn):

```
*☀️ 모닝 브리핑* (YYYY-MM-DD)

*Git 동기화*
- N/5 프로젝트 pull 완료, 총 M개 커밋 수신

*오늘의 일정*
- 회의 N건 (HIGH N건)
- 집중 가능: HH:MM~HH:MM

*메일 정리*
- 스팸 N건 삭제, 알림 N건 정리
- 답장 필요 N건 (쓰레드 확인)

*주식 분석*
- N개 종목 분석 완료
- 매수 시그널: TICKER1, TICKER2
- 리포트: <REPORT_LINK|daily-report.docx>

*합계*
- N개 프로젝트 동기화, 일정 N건, 메일 N건 처리, N개 종목 분석
```

#### Step 2: Git Sync Details (Thread)

Post a thread reply with per-project pull results:

```json
{
  "channel_id": "C0AA8NT4T8T",
  "thread_ts": "MAIN_MESSAGE_TS",
  "message": "*[Git 동기화 상세]*\n\n- github-to-notion-sync: N개 커밋 수신 (branch)\n- ai-template: 변경사항 없음\n- ai-model-event-stock-analytics: N개 커밋 수신\n- research: N개 커밋 수신\n- ai-platform-webui: N개 커밋 수신 (tmp)"
}
```

#### Step 3: Calendar + Gmail Thread

Post a thread reply with calendar briefing and Gmail triage details:

```json
{
  "channel_id": "C0AA8NT4T8T",
  "thread_ts": "MAIN_MESSAGE_TS",
  "message": "*[일정 & 메일 상세]*\n\n*일정*\n{calendar briefing text}\n\n*메일 처리 결과*\n- 스팸 삭제: N건\n- 알림 정리: N건\n- 팀원 메일: N건\n- 뉴스: N건\n- 답장 필요: N건"
}
```

#### Step 4: Stock Analysis Thread (if run)

Post a thread reply with stock pipeline summary:

```json
{
  "channel_id": "C0AA8NT4T8T",
  "thread_ts": "MAIN_MESSAGE_TS",
  "message": "*[주식 분석 요약]*\n\n*시그널*\n{buy/sell/neutral signals per ticker}\n\n*스크리너 결과*\n- 통과 종목: N개\n- 주요 종목: TICKER1 (이유), TICKER2 (이유)\n\n리포트: <REPORT_LINK|daily-report-YYYY-MM-DD.docx>"
}
```

#### Slack mrkdwn Rules

- `*bold*` (single asterisk only, never `**`)
- `_italic_` (underscore)
- `<url|text>` (links)
- No `## headers` — use `*bold text*` on its own line
- `> quote` for draft replies
- Write all message text in Korean
- Omit sections with no data
- Keep each message under 5000 chars

### Phase 5: Report

Display the same consolidated summary in the chat as a formatted report (in Korean).

```
모닝 브리핑
================
날짜: YYYY-MM-DD

Git 동기화:
  github-to-notion-sync:          3개 커밋 수신 (main)
  ai-template:                    변경사항 없음
  ai-model-event-stock-analytics: 2개 커밋 수신 (dev)
  research:                       1개 커밋 수신 (main)
  ai-platform-webui:              4개 커밋 수신 (tmp)

오늘의 일정:
  09:00 팀 미팅 (MEDIUM)
  11:00 외부 미팅 - 고객사 A (HIGH)
  14:00 면접 - 백엔드 개발자 (HIGH)
  집중 가능: 10:00~11:00, 15:00~18:00

메일 정리:
  스팸 삭제: 5건
  알림 정리: 12건 → Low Priority
  팀원 메일: 3건
  뉴스: 1건 (Bespin News)
  답장 필요: 2건

주식 분석:
  분석 종목: 15개
  매수 시그널: AAPL, MSFT
  매도 시그널: 없음
  리포트: outputs/daily-report-YYYY-MM-DD.docx

슬랙: #효정-할일 채널에 게시 완료

합계: 5/5 프로젝트 동기화, 일정 3건, 메일 23건 처리, 15개 종목 분석
```

## Examples

### Example 1: Full morning pipeline

User runs `/morning-ship` at the start of the day.

1. Git pull: 5/5 projects synced, 10 commits received total
2. Calendar: 3 meetings (2 HIGH), focus slots 10:00-11:00 and 15:00-18:00
3. Gmail: 5 spam deleted, 12 notifications archived, 3 colleague emails, 2 reply needed
4. Stock: 15 tickers analyzed, AAPL buy signal
5. Slack: summary + 3 threads posted to #효정-할일
6. Report displayed in chat

### Example 2: Pull only

User runs `/morning-ship --skip-google --skip-stock` to just sync repos.

1. Git pull: 5/5 projects synced
2. Calendar: skipped
3. Gmail: skipped
4. Stock: skipped
5. Slack: git sync summary only
6. Report: git sync results only

### Example 3: Skip pull, run briefing

User runs `/morning-ship --skip-pull` because repos were already synced.

1. Git pull: skipped
2. Calendar + Gmail: full triage
3. Stock: full pipeline
4. Slack + Report

### Example 4: Specific projects only

User runs `/morning-ship --targets ai-platform-webui,research`.

1. Git pull: only `ai-platform-webui` (tmp) and `research` pulled
2. Calendar + Gmail: full triage
3. Stock: full pipeline
4. Slack + Report

### Example 5: Dry run

User runs `/morning-ship --dry-run` to preview.

1. For each project: show current branch, remote status, pending changes
2. Calendar/Gmail/Stock: skipped (dry-run)
3. Slack: skipped (dry-run)
4. Report: preview summary only

## Error Handling

| Scenario | Action |
|----------|--------|
| Project directory does not exist | Warn and skip; continue with remaining projects |
| Uncommitted changes in project | Warn about dirty state; skip pull for that project; continue with others |
| Merge conflict on pull | Report conflict details; skip that project; continue with others |
| Pull rejected (diverged history) | Report error with remediation suggestion; continue with others |
| `gws` CLI not authenticated | Report error; suggest `gws auth login -s drive,gmail,calendar`; continue to stock pipeline |
| Calendar API error | Report error; continue to Gmail triage |
| Gmail API error | Report partial results; continue to stock pipeline |
| Stock pipeline failure | Report error; continue to Slack/Report |
| Slack message fails | Report error; still display report in chat |
| No changes in any project | Report "all projects up to date" |

## Safety Rules

- **Never force pull** (`--force`) or hard reset (`--hard`) in any project
- **Never switch branches** automatically — pull into the current branch only
- **Never auto-resolve** merge conflicts — report and skip
- **ai-platform-webui**: Always `git pull origin tmp`, never pull from other branches
- **Never delete** uncommitted changes — warn and skip pull for dirty repos
- **Never send** emails automatically (Gmail triage generates drafts only)
- **Never delete** calendar events
- **Always return** to original working directory after processing each project
- **Always post** Slack message as the authenticated user, never impersonate
