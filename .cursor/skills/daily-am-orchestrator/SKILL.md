---
name: daily-am-orchestrator
description: >-
  Morning Pipeline orchestrator: 8 phases covering pre-flight, git sync, Google
  Workspace, email intelligence, market intelligence, news/content, AI research,
  and dev intelligence — with a consolidated Slack briefing. Runs at 7:00 AM
  daily. Use when the user runs /daily-am, asks to "run morning pipeline",
  "morning automation", "아침 파이프라인", "모닝 오케스트레이터", "daily-am", "daily
  morning", or wants to run the full morning automation. Do NOT use for partial
  morning routines (use morning-ship), individual skills (invoke them directly),
  or evening pipeline (use daily-pm-orchestrator).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "orchestration"
---
# Daily AM Orchestrator — Morning Pipeline (7:00 AM)

Orchestrate 8 phases of morning automation across 15+ skills with parallel execution where possible, consolidated Slack briefing, and robust error handling.

## Configuration

- **Slack channel**: `#효정-할일` (Channel ID: `C0AA8NT4T8T`)
- **Stock Slack**: `#h-report` (Channel ID: `C0AKHQWJBLZ`)
- **Research Slack**: `#deep-research-trending` (Channel ID: `C0AN34G4QHK`)
- **Design doc**: `docs/daily-automation-guide.md`
- **Pipeline state**: `outputs/pipeline-state/YYYY-MM-DD-am.json`

## Usage

```
/daily-am                         # full morning pipeline
/daily-am --skip-phase 4          # skip Market Intelligence
/daily-am --only-phase 2,3        # run only Google + Email phases
/daily-am --skip-market           # skip market (auto on weekends)
/daily-am --skip-email            # skip email intelligence
/daily-am --skip-research         # skip AI research
/daily-am --no-slack              # suppress Slack notifications
/daily-am --dry-run               # preview plan without execution
```

## Workflow

### Initialization

1. Record start time: `pipeline_start = now()`
2. Initialize results tracker:
   ```python
   results = {
     "date": "YYYY-MM-DD",
     "pipeline": "am",
     "phases": {},
     "start_time": pipeline_start,
     "end_time": None,
     "status": "running"
   }
   ```
3. Determine if today is a trading day (skip market on weekends/KRX holidays)
4. Determine if it's Friday (for any Friday-specific behavior)
5. Parse flags (`--skip-phase`, `--only-phase`, `--skip-market`, etc.)

---

### Phase 0: Pre-flight (setup-doctor)

**Duration**: ~1 min | **Dependencies**: None | **Critical**: YES

Read and follow the `setup-doctor` skill (`.cursor/skills/setup-doctor/SKILL.md`) with scope limited to daily pipeline prerequisites.

**Checks**:
| Check | Command / Method | Fail Action |
|---|---|---|
| PostgreSQL | `pg_isready` or connect test | ABORT pipeline |
| `gws` CLI auth | `gws auth status` | WARN, skip Google phases |
| `TWITTER_COOKIE` | Check `.env` | WARN, skip Twitter |
| Slack MCP | Test `slack_send_message` | WARN, skip Slack posts |
| Notion MCP | Test search | WARN, skip Notion uploads |

**On critical failure** (PostgreSQL down): Post alert to `#효정-할일` and abort.

```python
results["phases"]["phase0"] = {"status": "pass|fail", "checks": {...}, "duration_s": N}
```

---

### Phase 1: Git Sync (sod-ship)

**Duration**: ~2-5 min | **Dependencies**: Phase 0 | **Critical**: YES

Read and follow the `sod-ship` skill (`.cursor/skills/sod-ship/SKILL.md`).

1. Commit dirty working directories across all 5 managed projects
2. Push unpushed commits
3. Pull remote changes (ai-platform-webui via `git pull origin tmp`)
4. Update Slack Canvas with sync status

```python
results["phases"]["phase1"] = {
  "status": "pass|partial|fail",
  "projects": {"name": {"pulled": N, "pushed": N, "conflicts": bool}},
  "duration_s": N
}
```

**On failure**: Log per-project errors, continue (non-critical phases can still run).

---

### Phase 2: Google Workspace (google-daily)

**Duration**: ~3-5 min | **Dependencies**: Phase 1 | **Sequential after Phase 1**

Read and follow the `google-daily` skill (`.cursor/skills/google-daily/SKILL.md`).

This orchestrates:
1. `calendar-daily-briefing` — Today's events with priority classification
2. `gmail-daily-triage` — Spam removal, notification labeling, classification
3. Drive upload of generated documents
4. Slack notification with threaded replies
5. MEMORY.md sync

**Skip if** `--skip-phase 2` is set or `gws` auth failed in Phase 0.

```python
results["phases"]["phase2"] = {
  "status": "pass|partial|fail",
  "calendar": {"events": N, "high_priority": N, "focus_slots": [...]},
  "gmail": {"spam": N, "notifications": N, "reply_needed": N, "colleague": N},
  "duration_s": N
}
```

---

### Phase 3: Email Intelligence

**Duration**: ~5-8 min | **Dependencies**: Phase 2 (needs triage output) | **Sequential after Phase 2**

**Skip if** `--skip-email` or `--skip-phase 3` is set.

Run 4 email intelligence sub-skills sequentially:

#### 3a. email-auto-reply

Read and follow `email-auto-reply` skill (`.cursor/skills/email-auto-reply/SKILL.md`).

- Read reply-needed emails from Phase 2 output
- Retrieve context from Cognee knowledge graph and recall memory
- Generate 2-3 draft reply options per email
- Post drafts to Slack `#효정-할일` for async human approval

#### 3b. email-research-dispatcher

Read and follow `email-research-dispatcher` skill (`.cursor/skills/email-research-dispatcher/SKILL.md`).

- Extract research-worthy topics from emails
- Run `parallel-web-search` per topic
- Synthesize findings and post to appropriate Slack channels

#### 3c. proactive-meeting-scheduler

Read and follow `proactive-meeting-scheduler` skill (`.cursor/skills/proactive-meeting-scheduler/SKILL.md`).

- Detect implicit meeting requests ("let's discuss", "can we sync")
- Extract context and generate agendas
- Find available calendar slots via `gws-calendar`
- Propose meetings via Slack for approval

#### 3d. feedback-meeting-scheduler

Read and follow `feedback-meeting-scheduler` skill (`.cursor/skills/feedback-meeting-scheduler/SKILL.md`).

- Detect stale PR reviews, conflicting comments, blocked items
- Propose 1:1 feedback meetings with relevant parties

```python
results["phases"]["phase3"] = {
  "status": "pass|partial|fail",
  "auto_reply": {"emails_drafted": N},
  "research": {"topics_found": N, "posted": N},
  "meetings_proposed": N,
  "feedback_meetings": N,
  "duration_s": N
}
```

---

### Phase 4: Market Intelligence (today)

**Duration**: ~10-20 min | **Dependencies**: Phase 1 only | **PARALLEL with Phase 2-3**

**Skip if** `--skip-market` or `--skip-phase 4` is set, or not a trading day.

Read and follow the `today` skill (`.cursor/skills/today/SKILL.md`).

Full pipeline:
1. DB/CSV freshness check
2. Yahoo Finance data sync (`weekly-stock-update`)
3. Fundamental data collection (quarterly financials)
4. Hot stock discovery (NASDAQ/KOSPI/KOSDAQ 100)
5. Multi-factor screening (P/E, RSI, volume, MA, FCF yield)
6. Turtle + Bollinger + Oscillator analysis (SMA 20/55/200, RSI, MACD, Stochastic, ADX)
7. Optional: `alphaear-news` + `alphaear-sentiment`
8. .docx report generation
9. Slack posting to `#h-report` with stock thread to `#h-daily-stock-check`

```python
results["phases"]["phase4"] = {
  "status": "pass|partial|fail|skipped",
  "stocks_analyzed": N,
  "buy_signals": [...],
  "sell_signals": [...],
  "report_path": "...",
  "duration_s": N
}
```

---

### Phase 5: News & Content Intelligence

**Duration**: ~10-15 min | **Dependencies**: Phase 1 only | **PARALLEL with Phase 2-4**

**Skip if** `--skip-phase 5` is set.

Run two sub-skills. These can run sequentially within this phase:

#### 5a. bespin-news-digest

Read and follow `bespin-news-digest` skill (`.cursor/skills/bespin-news-digest/SKILL.md`).

- Fetch latest Bespin Global news email from Gmail
- Extract all article URLs
- Per-article: Jina extraction + WebSearch + AI GPU Cloud classification
- Post 3-message Slack thread per article to `#press`
- Generate DOCX → Google Drive

#### 5b. twitter-timeline-to-slack

Read and follow `twitter-timeline-to-slack` skill (`.cursor/skills/twitter-timeline-to-slack/SKILL.md`).

- Fetch latest tweets from `hjguyhan` profile
- Store locally with deduplication
- Classify each tweet by topic
- Run full x-to-slack pipeline per tweet (sequentially, with rate limiting)
- Post to appropriate Slack channel based on classification

**Skip twitter if** `TWITTER_COOKIE` not set (detected in Phase 0).

```python
results["phases"]["phase5"] = {
  "status": "pass|partial|fail",
  "bespin": {"articles_processed": N},
  "twitter": {"tweets_processed": N, "channels_posted": [...]},
  "duration_s": N
}
```

---

### Phase 6: AI Research Intelligence

**Duration**: ~5-10 min | **Dependencies**: Phase 1 only | **PARALLEL with Phase 2-5**

**Skip if** `--skip-research` or `--skip-phase 6` is set.

Run two sub-skills:

#### 6a. hf-trending-intelligence

Read and follow `hf-trending-intelligence` skill (`.cursor/skills/hf-trending-intelligence/SKILL.md`).

- Cross-reference HF daily papers, trending models, new datasets, community activity
- Score emerging trends before they go mainstream
- Post intelligence report to `#deep-research-trending` + Notion

#### 6b. paper-auto-classifier

Read and follow `paper-auto-classifier` skill (`.cursor/skills/paper-auto-classifier/SKILL.md`).

- Poll arXiv RSS feeds for tracked categories
- Fetch HF daily papers
- Score relevance against tracked research topics
- Route: Tier A (relevance >= 8) → queue for full `paper-review`
- Route: Tier B (relevance 5-7) → quick summary to `#deep-research-trending`
- Discard: Tier C (relevance < 5)

```python
results["phases"]["phase6"] = {
  "status": "pass|partial|fail",
  "hf_trending": {"trends_detected": N, "report_posted": bool},
  "papers": {"discovered": N, "tier_a": N, "tier_b": N, "discarded": N},
  "duration_s": N
}
```

---

### Phase 7: Dev Intelligence

**Duration**: ~3-5 min | **Dependencies**: Phase 1 only | **PARALLEL with Phase 2-6**

**Skip if** `--skip-phase 7` is set.

Run two sub-skills:

#### 7a. github-sprint-digest

Read and follow `github-sprint-digest` skill (`.cursor/skills/github-sprint-digest/SKILL.md`).

- Fetch overnight GitHub activity (issues, PRs, reviews, comments) per user
- Aggregate across 5 managed projects
- Generate Korean summary
- Post to Notion sub-pages + Slack

#### 7b. standup-digest

Read and follow `standup-digest` skill (`.cursor/skills/standup-digest/SKILL.md`).

- Aggregate GitHub commits/PRs/issues + Slack messages + Calendar events
- Generate per-team-member did/doing/blocked summaries
- Post to Slack

```python
results["phases"]["phase7"] = {
  "status": "pass|partial|fail",
  "github": {"commits": N, "prs": N, "issues": N, "blockers": N},
  "standup": {"members_reported": N},
  "duration_s": N
}
```

---

### Phase 8: Consolidated Morning Briefing

**Duration**: ~1 min | **Dependencies**: ALL phases complete | **Sequential (final)**

**Skip if** `--no-slack` is set.

Post a master summary to `#효정-할일` using `slack_send_message` MCP tool.

**Main message** (Slack mrkdwn):

```
*☀️ Morning Pipeline 완료* (YYYY-MM-DD, Nm Ns)

*Git Sync*: N/5 프로젝트 동기화, 총 M커밋 수신
*Calendar*: N개 이벤트 (HIGH N건), 집중 슬롯 N개
*Gmail*: N건 정리, 답장 필요 N건
*Market*: N개 종목 분석 — BUY N / SELL N / HOLD N
*News*: 기사 N건 (베스핀 N, 트위터 N)
*Research*: 논문 N건 (Tier A: N, Tier B: N)
*Dev*: N commits, N PRs, N blockers

{[INCOMPLETE] sections if any phase failed}
```

**Thread replies** for each phase with detailed results.

Save pipeline state to `outputs/pipeline-state/YYYY-MM-DD-am.json`.

---

## Parallelism Execution Strategy

After Phase 1 (Git Sync) completes, launch the following as parallel subagents:

| Batch | Phases | Max Concurrent |
|---|---|---|
| Sequential | Phase 0 → Phase 1 → Phase 2 → Phase 3 | 1 (dependency chain) |
| Parallel A | Phase 4 (Market Intelligence) | 1 |
| Parallel B | Phase 5 (News & Content) | 1 |
| Parallel C | Phase 6 (AI Research) | 1 |
| Parallel D | Phase 7 (Dev Intelligence) | 1 |
| Final | Phase 8 (Briefing) — waits for ALL | 1 |

Total max concurrent subagents: 4 (Phases 4, 5, 6, 7 running in parallel).

Phase 2 → Phase 3 runs sequentially as a chain, concurrent with Phases 4-7.

---

## Weekend/Holiday Behavior

| Phase | Weekend/Holiday |
|---|---|
| Phase 0 (Pre-flight) | Run (reduced checks — skip PostgreSQL trading check) |
| Phase 1 (Git Sync) | Run normally |
| Phase 2 (Google) | Run normally |
| Phase 3 (Email Intel) | Run normally |
| Phase 4 (Market) | **SKIP** (pykrx returns errors, Yahoo KRX data absent) |
| Phase 5 (News) | Run normally |
| Phase 6 (Research) | Run normally |
| Phase 7 (Dev) | Run normally (reduced activity expected) |

Detection: Use Python `datetime.today().weekday()` (5=Sat, 6=Sun) or `is_trading_day()`.

---

## Error Handling

| Failure Type | Action |
|---|---|
| Phase 0 critical (PostgreSQL) | ABORT entire pipeline, alert Slack |
| Phase 0 warning (gws auth) | Skip dependent phases, continue others |
| Phase-level timeout (>30 min) | Kill phase, mark `[TIMEOUT]`, continue |
| Individual skill failure | Log error, mark `[INCOMPLETE]` in briefing |
| Slack MCP unavailable | Log all results to file, skip Slack posts |
| All phases fail | Post minimal alert: "Morning pipeline failed — check logs" |

Each phase catches its own errors and never propagates failures to other parallel phases.

---

## Examples

### Example 1: Full weekday pipeline

```
/daily-am
```

Runs all 8 phases. Market analysis runs in parallel with email, news, research, and dev intelligence. Consolidated briefing posted at end.

### Example 2: Skip market (weekend)

```
/daily-am --skip-market
```

Automatically applied on weekends. Phases 0-3, 5-8 run normally.

### Example 3: Only email and Google

```
/daily-am --only-phase 2,3
```

Runs Phase 0 (pre-flight), Phase 1 (git sync), Phase 2 (Google), Phase 3 (Email), Phase 8 (briefing).

### Example 4: Dry run

```
/daily-am --dry-run
```

Prints execution plan with phase ordering, parallelism, and estimated durations. No actual execution.

### Example 5: No Slack

```
/daily-am --no-slack
```

Full pipeline but results only shown in chat, not posted to Slack.

## Safety Rules

- Never force-push or hard-reset any git repository
- Never send emails automatically — only generate drafts for human approval
- Never delete calendar events
- Never accept meeting proposals automatically — propose for human approval
- Never commit to production branches without human confirmation
- Pipeline state is always persisted for debugging
- Individual phase failures never cascade to other phases
