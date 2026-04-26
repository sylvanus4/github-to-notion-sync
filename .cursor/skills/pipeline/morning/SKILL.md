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

- `gws` CLI installed and authenticated (`GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` 환경변수 설정 필수; `gws drive files list`로 검증)
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

Read and execute `.cursor/skills/pipeline/google-daily/SKILL.md`.

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

Read and execute `.cursor/skills/pipeline/today/SKILL.md`.

Skip this phase if `--skip-today` is set.

Pass through any Today-specific flags from the morning command:
- `--skip-sync` → skip data sync
- `--skip-fundamentals` → skip fundamental data collection
- `--skip-discover` → skip hot stock discovery
- `--skip-screener` → skip multi-factor screening
- `--skip-tradingview` → skip TradingView extended stages (live prices, backtests, sentiment, multi-timeframe)
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

Use `slack_send_message` from MCP server `plugin-slack-slack` in **two steps** (parent + thread).

#### Step A — Parent message (channel summary)

Post the high-level header and **signal summary** first. Capture the returned message `ts` for Step B.

```
slack_send_message(
  channel_id="C0AA8NT4T8T",
  message="*☀️ 모닝 루틴 완료* (YYYY-MM-DD)\n\n*Google Daily*\n- 캘린더: N건 일정 (면접 N, 미팅 N)\n- 메일: N건 정리 (스팸 N, 알림 N, 팀원 N, 뉴스 N)\n- 답장 필요: N건\n- 문서: N건 생성 → Drive 업로드\n\n*주식 분석 (요약)*\n- N개 종목 분석 완료\n- 매수 N | 중립 N | 매도 N\n- 핫 종목: {discovered tickers}\n- 보고서: `{report_path}`\n\n_스레드에 세부 종목·단계 상태를 정리합니다._"
)
```

#### Step B — Thread reply (detail + disclaimer)

Post **details** in a thread on Step A using `thread_ts` from Step A’s response. Include:

- Google Daily: which sub-phases completed vs failed (calendar, gmail, drive, slack, memory)
- Today: top BUY / top SELL tickers (names or symbols), and pointer to `#h-report` if posted there
- **Disclaimer** (required, last line of thread body):

`_본 브리핑은 정보 제공 목적이며 특정 금융상품 매수·매도를 권유하지 않습니다._`

```
slack_send_message(
  channel_id="C0AA8NT4T8T",
  thread_ts="<ts_from_step_A>",
  message="*세부 내역*\n\n*Google Daily 상태*\n- …\n\n*주식 시그널 상세*\n- 매수 후보: …\n- 매도 후보: …\n\n_본 브리핑은 정보 제공 목적이며 특정 금융상품 매수·매도를 권유하지 않습니다._"
)
```

#### Phase 3 — Error recovery (Slack MCP)

If `slack_send_message` fails: **retry once** after a short backoff (2–3s). If it still fails, log the error, record `morning_briefing=failed` in session notes (and append a one-line entry to `MEMORY.md` if that file is updated this run), and **stop Phase 3** without failing the entire morning run—Phases 1–2 outputs remain valid.

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
| `--dry-run` | Suppress Slack in Today + Google Daily; skip Phase 3 briefing | Slack enabled |
| `--skip-sync` | Pass to Today: skip data sync | Sync enabled |
| `--skip-fundamentals` | Pass to Today: skip fundamental data | Fundamentals enabled |
| `--skip-discover` | Pass to Today: skip hot stock discovery | Discovery enabled |
| `--skip-screener` | Pass to Today: skip multi-factor screening | Screener enabled |
| `--skip-tradingview` | Pass to Today: skip TradingView extended stages (live, backtest, sentiment, MTF) | TV enabled |
| `--skip-news` | Pass to Today: skip market news | News enabled |
| `--skip-sentiment` | Pass to Today: skip sentiment scoring | Sentiment enabled |
| `--skip-docx` | Pass to Today: skip .docx report | DOCX enabled |
| `--skip-quality-gate` | Pass to Today: skip report quality eval | Quality gate enabled |

### CLI propagation and defaults

- Forward **`--dry-run`** to **Today** so its Slack steps are skipped per `today` skill.
- **Google Daily** has no documented `--dry-run` flag: when `--dry-run` is set, still run Calendar, Gmail, Drive, and memory steps, but **do not** post Slack messages for Google Daily phases (treat as a manual dry-run branch).
- **`--skip-briefing`**: skip Phase 3 only; Phases 1–2 still run unless combined with `--skip-google` / `--skip-today`.
- **Combined flags** apply left-to-right semantics: all stated skips are honored; there is no implicit override between `--dry-run` and `--skip-briefing` (both suppress Phase 3 posting).

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

Runs Google Daily and Today workflows with **Slack disabled** (Today: pass `--dry-run`; Google Daily: skip Slack posts only). Phase 3 briefing is **not** posted.

### Skip consolidated briefing only

```
/morning --skip-briefing
```

Runs Phases 1–2; omits Phase 3 parent + thread (Google Daily / Today may still post to their own channels per those skills unless you combine with `--dry-run`).

### Per-flag reference (each flag appears in an example)

| Test input / intent | Example command |
|---------------------|-----------------|
| Full default pipeline | `/morning` |
| Skip stock pipeline | `/morning --skip-today` |
| Skip Google | `/morning --skip-google` |
| Lightweight Today | `/morning --skip-screener --skip-news --skip-sentiment --skip-docx` |
| Dry run | `/morning --dry-run` |
| Skip data sync only | `/morning --skip-sync` |
| Skip fundamentals only | `/morning --skip-fundamentals` |
| Skip hot-stock discovery | `/morning --skip-discover` |
| Skip quality gate only | `/morning --skip-quality-gate` |
| Skip Phase 3 only | `/morning --skip-briefing` |

### End-to-end walkthrough (all phases, default flags)

Use this as the canonical “full run” narrative when the user says e.g. “아침 루틴 시작해줘” with no skips:

1. **Phase 1 — Google Daily**: Open `.cursor/skills/pipeline/google-daily/SKILL.md` and execute Calendar → Gmail triage → Drive upload → Slack (unless `--dry-run`) → memory sync. Capture `calendar_summary`, `email_summary`, `documents_created`.
2. **Phase 1.5 — Gate**: Verify calendar + triage produced structured output or an explicit “no events / no mail” outcome; if Google auth or CLI is missing, log and continue to Phase 2.
3. **Phase 2 — Today**: Open `.cursor/skills/pipeline/today/SKILL.md` and run the full pipeline (sync, fundamentals, discovery, screener, news, sentiment, analysis, optional quality gate, docx, Slack to `#h-report` when enabled). Forward any Today flags from the user line. Capture `stock_count`, `signal_summary`, `top_movers`, `hot_stocks`, `report_path`.
4. **Phase 3 — Morning briefing**: Unless `--skip-briefing` or `--dry-run`, post Step A parent message to `#효정-할일`, then Step B thread with details + disclaimer. On Slack failure, follow Phase 3 error recovery above.

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
| gws auth expired | Run `python ~/.config/gws/oauth2_manual.py && rm ~/.config/gws/token_cache.json credentials.enc 2>/dev/null` |
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
