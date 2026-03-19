---
name: morning
description: >-
  Morning routine orchestrator that runs google-daily (calendar briefing, Gmail
  triage, Drive upload, Slack notification) then today (stock data sync,
  screening, analysis, report) in sequence. Posts a consolidated morning
  briefing to Slack.
  Use when the user asks to "start my morning", "morning routine", "morning",
  "아침 루틴", "아침", "모닝", "하루 시작", "start the day", "/morning".
  Do NOT use for google-daily only (use google-daily), today pipeline only
  (use today), or end-of-day shipping (use eod-ship).
metadata:
  author: thaki
  version: 1.0.0
  category: execution
---

# Morning — Daily Morning Routine Orchestrator

Runs Google Workspace automation and the stock analysis pipeline as a
single morning sequence. Google Daily handles personal productivity
(calendar, email, documents); Today handles market data and analysis.

## Prerequisites

- `gws` CLI installed and authenticated (`gws auth login -s drive,gmail,calendar`)
- PostgreSQL running with migrated schema
- Stock CSV files in `data/latest/` (seed via `stock-csv-downloader` if empty)
- Slack MCP server (`plugin-slack-slack`) connected
- Node.js with `docx` package installed (`cd outputs && npm install`)

## Pipeline Overview

```
Phase 1: Google Daily   (calendar → gmail → drive → slack → memory)
Phase 2: Today Pipeline  (data sync → fundamentals → discovery → screening → analysis → report)
Phase 3: Morning Briefing (consolidated Slack summary to #효정-할일)
```

Estimated time: 15–25 minutes total (Google Daily ~5min, Today ~10–20min).

## Phase 1: Google Daily

Read and execute `.cursor/skills/google-daily/SKILL.md`.

Skip this phase if `--skip-google` is set.

The Google Daily skill runs 5 sub-phases:
1. Calendar briefing (today's schedule)
2. Gmail triage (spam removal, notification labeling, colleague email summaries)
3. Drive upload (generated documents)
4. Slack notification (main summary + threaded replies to `#효정-할일`)
5. Memory sync (append daily entry to `MEMORY.md`)

**Capture output** from Google Daily for Phase 3:
- `calendar_summary`: event count, key meetings, focus time slots
- `email_summary`: triage counts (spam, notifications, colleague, news, reply-needed)
- `documents_created`: list of generated docx files with Drive links

### Error Handling

If Google Daily fails at any sub-phase, log the error and continue to
Phase 2. The morning briefing (Phase 3) will note which sub-phases
completed successfully.

## Phase 1.5: Google Daily Completion Gate

Before proceeding to the Today pipeline, verify:
- [ ] Calendar briefing generated (non-empty event list or "no events today")
- [ ] Gmail triage completed (counts reported: spam, notifications, colleague, reply-needed)
- [ ] No Google API authentication failures that halted the entire Phase 1

If Google Daily fails entirely (auth error, CLI not found), proceed to Phase 2 independently and note the failure in the Phase 3 briefing. Partial failures (e.g., calendar OK but Gmail failed) are acceptable — continue and report which sub-phases succeeded.

## Phase 2: Today Pipeline

Read and execute `.cursor/skills/today/SKILL.md`.

Skip this phase if `--skip-today` is set.

Pass through any Today-specific flags from the morning command:
- `--skip-sync` → skip data sync
- `--skip-fundamentals` → skip fundamental data collection
- `--skip-discover` → skip hot stock discovery
- `--skip-screener` → skip multi-factor screening
- `--skip-news` → skip market news context
- `--skip-sentiment` → skip sentiment scoring
- `--skip-docx` → skip .docx report generation
- `--skip-quality-gate` → skip report quality evaluation
- `--dry-run` → skip Slack posting in Today pipeline

**Capture output** from Today for Phase 3:
- `stock_count`: number of stocks analyzed
- `signal_summary`: BUY/NEUTRAL/SELL counts
- `top_movers`: top BUY and SELL stocks
- `hot_stocks`: discovered untracked stocks
- `report_path`: path to generated .docx report

### Error Handling

If Today fails at any phase, log the error and proceed to Phase 3.
Report partial results in the morning briefing.

## Phase 3: Morning Briefing

Post a consolidated morning summary to `#효정-할일` (`C0AA8NT4T8T`).

Skip if `--skip-briefing` is set or `--dry-run` is set.

**Note**: Google Daily already posts its own detailed thread to
`#효정-할일`. The Today pipeline optionally posts to `#h-report`.
This Phase 3 briefing is a short consolidated summary linking both.

Use `slack_send_message` MCP tool (server: `plugin-slack-slack`):

```
slack_send_message(
  channel_id="C0AA8NT4T8T",
  message="*☀️ 모닝 루틴 완료* (YYYY-MM-DD)\n\n*Google Daily*\n- 캘린더: N건 일정 (면접 N, 미팅 N)\n- 메일: N건 정리 (스팸 N, 알림 N, 팀원 N, 뉴스 N)\n- 답장 필요: N건\n- 문서: N건 생성 → Drive 업로드\n\n*주식 분석*\n- N개 종목 분석 완료\n- 매수 N | 중립 N | 매도 N\n- 핫 종목: {discovered tickers}\n- 보고서: `{report_path}`\n\n_상세: Google Daily → 위 쓰레드 / 주식 보고서 → #h-report_"
)
```

### Slack mrkdwn Rules

- `*bold*` (single asterisk, never `**`)
- `_italic_` (underscore)
- `<url|text>` (links)
- No `## headers`
- Write all content in Korean

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--skip-google` | Skip Phase 1 (Google Daily) | Google Daily enabled |
| `--skip-today` | Skip Phase 2 (Today pipeline) | Today enabled |
| `--skip-briefing` | Skip Phase 3 (consolidated Slack briefing) | Briefing enabled |
| `--dry-run` | Run all phases but skip all Slack posting | Slack enabled |
| `--skip-sync` | Pass to Today: skip data sync | Sync enabled |
| `--skip-fundamentals` | Pass to Today: skip fundamental data | Fundamentals enabled |
| `--skip-discover` | Pass to Today: skip hot stock discovery | Discovery enabled |
| `--skip-screener` | Pass to Today: skip multi-factor screening | Screener enabled |
| `--skip-news` | Pass to Today: skip market news | News enabled |
| `--skip-sentiment` | Pass to Today: skip sentiment scoring | Sentiment enabled |
| `--skip-docx` | Pass to Today: skip .docx report | DOCX enabled |
| `--skip-quality-gate` | Pass to Today: skip report quality eval | Quality gate enabled |

## Examples

### Full morning routine

```
/morning
```

Runs Google Daily (calendar + gmail + drive + slack + memory), then Today
(sync + fundamentals + discovery + screening + analysis + report + slack),
then posts a consolidated morning briefing to `#효정-할일`.

### Google Daily only

```
/morning --skip-today
```

Runs only Google Daily. Useful when markets are closed (weekends/holidays).

### Today pipeline only

```
/morning --skip-google
```

Runs only the stock analysis pipeline. Useful when email was already triaged.

### Lightweight morning (no heavy analysis)

```
/morning --skip-screener --skip-news --skip-sentiment --skip-docx
```

Quick data sync + basic technical analysis without screening, news, or report.

### Dry run (preview, no Slack)

```
/morning --dry-run
```

Runs everything but skips all Slack posting across both pipelines.

## Skills Composed

| Skill | Phase | Purpose |
|-------|-------|---------|
| google-daily | 1 | Calendar, Gmail, Drive, Slack, Memory |
| calendar-daily-briefing | 1.1 | Today's schedule |
| gmail-daily-triage | 1.2 | Email triage and summaries |
| gws-drive | 1.3 | Document upload |
| today | 2 | Stock data pipeline |
| weekly-stock-update | 2.2 | Yahoo Finance data sync |
| daily-stock-check | 2.4 | Technical analysis |
| alphaear-news | 2.4.5 | Market news context |
| alphaear-sentiment | 2.4.5 | Sentiment scoring |
| anthropic-docx | 2.5 | Report generation |
| Slack MCP | 1, 2, 3 | Channel posting |

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| gws auth expired | Run `gws auth login -s drive,gmail,calendar` |
| PostgreSQL not running | `docker compose up -d db` |
| No CSV data | Run `stock-csv-downloader` first |
| Slack channel not found | Verify `C0AA8NT4T8T` with `slack_search_channels` |
| Google Daily partial failure | Check gws CLI auth; pipeline continues to Today |
| Today partial failure | Check DB connection; briefing reports partial results |
| Weekend/holiday: no market data | Use `--skip-today` or `--skip-sync` |

## Related Skills

- **google-daily** — Google Workspace automation (Phase 1)
- **today** — Stock data sync and analysis (Phase 2)
- **eod-ship** — End-of-day multi-project shipping (opposite bookend)
- **ai-chief-of-staff** — Alternative morning briefing (Gmail/Calendar/Drive only)
