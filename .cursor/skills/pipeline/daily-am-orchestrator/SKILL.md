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
  version: "1.2.0"
  category: "orchestration"
---
# Daily AM Orchestrator — Morning Pipeline (7:00 AM)

Orchestrate 9 phases of morning automation across 15+ skills with parallel execution where possible, consolidated Slack briefing, and robust error handling. Includes a personal AI briefing (Phase 0.2) via MemKraft + LLM Wiki.

## Configuration

- **Slack channel**: `#효정-할일` (Channel ID: `C0AA8NT4T8T`)
- **Stock Slack**: `#h-report` (Channel ID: `C0AKHQWJBLZ`)
- **Research Slack**: `#deep-research-trending` (Channel ID: `C0AN34G4QHK`)
- **Design doc**: `docs/daily-automation-guide.md`
- **Pipeline state (canonical)**: `outputs/daily-am/{date}/manifest.json` per Pipeline Output Protocol; optional compact snapshot: `outputs/pipeline-state/YYYY-MM-DD-am.json`

## Pipeline Output Protocol (File-First)

This orchestrator uses **file-first persistence** so parallel phases, resumability, and Phase 8 stay context-lean.

- **Output directory**: `outputs/daily-am/{date}/` where `{date}` is `YYYY-MM-DD` (project root).
- **Per-phase files**: Each phase writes exactly one JSON file: `outputs/daily-am/{date}/phase-{N}-{label}.json` (e.g. `phase-0-preflight.json`, `phase-4-market-intelligence.json`).
- **Manifest**: `outputs/daily-am/{date}/manifest.json` tracks the full run: pipeline name, date, start/end timestamps, every phase entry (status, output filename, timing, one-line summary), flags, overall status, warnings.
- **Subagent return contract**: Subagents and parallel phase runners return **only** `{ "status": "...", "file": "<path to phase JSON>", "summary": "<one line>" }` to the orchestrator. Large payloads live in the file, not in chat context.
- **Phase 8 rule**: The consolidated Slack briefing **must** assemble content by **reading** `manifest.json` and each `phase-*.json` under that `{date}` — **not** from conversation memory, prior inline summaries, or unstored subagent prose.

### manifest.json schema

```json
{
  "pipeline": "daily-am",
  "date": "YYYY-MM-DD",
  "started_at": "ISO timestamp",
  "completed_at": null,
  "phases": [
    {
      "id": "phase-{N}",
      "label": "{label}",
      "status": "completed|skipped|failed",
      "output_file": "phase-{N}-{label}.json",
      "started_at": "ISO timestamp",
      "elapsed_ms": 5200,
      "summary": "one-line summary"
    }
  ],
  "flags": [],
  "overall_status": "completed|completed_with_warnings|failed",
  "warnings": []
}
```

On completion, set `completed_at`, `overall_status`, and append the Phase 8 entry. Optionally write a compact duplicate to `outputs/pipeline-state/YYYY-MM-DD-am.json` for tools that expect the legacy path.

### Output artifacts (phase JSON files)

| Phase | Label | Output file |
| --- | --- | --- |
| 0 | preflight | `phase-0-preflight.json` |
| 0.2 | ai-brief | `phase-0.2-ai-brief.json` |
| 1 | git-sync | `phase-1-git-sync.json` |
| 2 | google-workspace | `phase-2-google-workspace.json` |
| 3 | email-intelligence | `phase-3-email-intelligence.json` |
| 4 | market-intelligence | `phase-4-market-intelligence.json` |
| 5 | news-content | `phase-5-news-content.json` |
| 6 | ai-research | `phase-6-ai-research.json` |
| 7 | dev-intelligence | `phase-7-dev-intelligence.json` |
| 8 | consolidated-briefing | `phase-8-consolidated-briefing.json` |

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

1. Record start time: `pipeline_start = now()`; set `out_dir = outputs/daily-am/{date}/` and create `out_dir` if missing.
2. Initialize `manifest.json` at `out_dir/manifest.json` with `pipeline: "daily-am"`, `date`, `started_at` (ISO), `completed_at: null`, `phases: []`, `flags` (parsed CLI flags), `overall_status: "running"`, `warnings: []`.
3. Initialize in-memory results tracker (for writing phase files only — Phase 8 does not trust this for Slack text):
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
4. Determine if today is a trading day (skip market on weekends/KRX holidays)
5. Determine if it's Friday (for any Friday-specific behavior)
6. Parse flags (`--skip-phase`, `--only-phase`, `--skip-market`, etc.) and merge into `manifest.json` → `flags`

---

### Phase 0: Pre-flight (setup-doctor)

**Duration**: ~1 min | **Dependencies**: None | **Critical**: YES

Read and follow the `setup-doctor` skill (`.cursor/skills/automation/setup-doctor/SKILL.md`) with scope limited to daily pipeline prerequisites.

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

**Persist & manifest**:
1. Write full phase payload to `outputs/daily-am/{date}/phase-0-preflight.json` (include `results["phases"]["phase0"]` and any check details).
2. Update `manifest.json`: append phase entry `id: phase-0`, `label: preflight`, `status` mapped to `completed|failed`, `output_file: phase-0-preflight.json`, `started_at`, `elapsed_ms`, `summary` (one line).
3. Subagent/orchestrator return to parent: `{ "status", "file": ".../phase-0-preflight.json", "summary" }` only.

---

### Phase 0.2: Personal AI Briefing (ai-brief)

**Duration**: ~30s | **Dependencies**: Phase 0 | **Critical**: NO

Invoke the `ai-brief` skill (`.cursor/skills/standalone/ai-brief/SKILL.md`) to generate a personal morning briefing from MemKraft + LLM Wiki context.

**Steps**:

1. **MemKraft hot-tier scan**: Load HOT entries from `memory/` — recent context, unresolved issues, active preferences
2. **LLM Wiki scan**: Query `_wiki-registry.json` for any recently-updated company/team articles relevant to today's schedule
3. **Assemble briefing** via `ai-context-router`:
   - Unresolved items from yesterday (`[UNRESOLVED]` provenance)
   - Active preferences affecting today's work (`[PREFERENCE]`)
   - Recent context carry-forward (`[RECENT]`)
   - Any overnight wiki updates (`[COMPANY]` / `[TEAM]`)
4. **Output**: Structured markdown with provenance tags, included in Phase 8 Slack briefing

**Graceful degradation**: If MemKraft files are missing or empty, skip personal sections and produce a minimal briefing with wiki-only context.

**Persist & manifest**: Write `outputs/daily-am/{date}/phase-0.2-ai-brief.json`. Update `manifest.json`.

---

### Phase 0.5: Paperclip Morning Check (Optional)

**Duration**: ~30s | **Dependencies**: Phase 0 | **Critical**: NO

Check Paperclip agent orchestrator health and run morning governance tasks. Skip if Paperclip is unavailable (graceful degradation).

**Step 0.5a — Health check:**

```
Tool: paperclip_dashboard
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

If the call fails (connection refused, timeout), log "Paperclip unavailable — skipping agent orchestration" and skip the rest of Phase 0.5.

**Step 0.5b — Heartbeat all registered agents:**

```
Tool: paperclip_list_agents
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

For each agent with `status != "terminated"`:

```
Tool: paperclip_heartbeat
Input: { "agentId": "<agent-id>", "status": "morning pipeline started" }
```

**Step 0.5c — Check pending approvals:**

```
Tool: paperclip_list_approvals
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

If pending approvals exist, include a summary line in the Phase 8 briefing:
`*Paperclip*: N건 승인 대기 중 — dashboard: http://127.0.0.1:3100`

**Step 0.5d — Budget check:**

```
Tool: paperclip_get_budget
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

If budget >= 80% spent, add a warning to `manifest.json` → `warnings[]` and prefer `model: "fast"` for all subagents in this pipeline run.

**Persist & manifest**: Write `outputs/daily-am/{date}/phase-0.5-paperclip.json`. Update `manifest.json`.

---

### Phase 1: Git Sync (sod-ship)

**Duration**: ~2-5 min | **Dependencies**: Phase 0 | **Critical**: YES

Read and follow the `sod-ship` skill (`.cursor/skills/pipeline/sod-ship/SKILL.md`).

1. Commit dirty working directories across all 5 managed projects
2. Push unpushed commits
3. Pull remote changes (same rules as `sod-ship`; `ai-platform-strategy` on `dev` uses `git pull origin dev`)
4. Update Slack Canvas with sync status

```python
results["phases"]["phase1"] = {
  "status": "pass|partial|fail",
  "projects": {"name": {"pulled": N, "pushed": N, "conflicts": bool}},
  "duration_s": N
}
```

**On failure**: Log per-project errors, continue (non-critical phases can still run).

**Persist & manifest**:
1. Write full phase payload to `outputs/daily-am/{date}/phase-1-git-sync.json`.
2. Update `manifest.json` with `phase-1` / `git-sync` entry and timing/summary.
3. Return only `{ "status", "file", "summary" }` upstream.

---

### Phase 2: Google Workspace (google-daily)

**Duration**: ~3-5 min | **Dependencies**: Phase 1 | **Sequential after Phase 1**

Read and follow the `google-daily` skill (`.cursor/skills/pipeline/google-daily/SKILL.md`).

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

**Persist & manifest**:
1. Write full phase payload to `outputs/daily-am/{date}/phase-2-google-workspace.json`.
2. Update `manifest.json` with `phase-2` / `google-workspace` entry.
3. Return only `{ "status", "file", "summary" }` upstream. Phase 3 sub-skills should read reply-needed counts/paths from this file or from skills’ own outputs — not from orchestrator chat history.

---

### Phase 3: Email Intelligence

**Duration**: ~5-8 min | **Dependencies**: Phase 2 (needs triage output) | **Sequential after Phase 2**

**Skip if** `--skip-email` or `--skip-phase 3` is set.

Run 4 email intelligence sub-skills sequentially:

#### 3a. email-auto-reply

Read and follow `email-auto-reply` skill (`.cursor/skills/pipeline/email-auto-reply/SKILL.md`).

- Read reply-needed emails from Phase 2 persisted output (`phase-2-google-workspace.json` or paths recorded there; do not rely on unstored orchestrator context)
- Retrieve context from Cognee knowledge graph and recall memory
- Generate 2-3 draft reply options per email
- Post drafts to Slack `#효정-할일` for async human approval

#### 3b. email-research-dispatcher

Read and follow `email-research-dispatcher` skill (`.cursor/skills/pipeline/email-research-dispatcher/SKILL.md`).

- Extract research-worthy topics from emails
- Run `parallel-web-search` per topic
- Synthesize findings and post to appropriate Slack channels

#### 3c. proactive-meeting-scheduler

Read and follow `proactive-meeting-scheduler` skill (`.cursor/skills/pipeline/proactive-meeting-scheduler/SKILL.md`).

- Detect implicit meeting requests ("let's discuss", "can we sync")
- Extract context and generate agendas
- Find available calendar slots via `gws-calendar`
- Propose meetings via Slack for approval

#### 3d. feedback-meeting-scheduler

Read and follow `feedback-meeting-scheduler` skill (`.cursor/skills/pipeline/feedback-meeting-scheduler/SKILL.md`).

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

**Persist & manifest**:
1. Write full phase payload to `outputs/daily-am/{date}/phase-3-email-intelligence.json`.
2. Update `manifest.json` with `phase-3` / `email-intelligence` entry (`status: skipped` if phase skipped).
3. Return only `{ "status", "file", "summary" }` upstream.

---

### Phase 4: Market Intelligence (today)

**Duration**: ~10-20 min | **Dependencies**: Phase 1 only | **PARALLEL with Phase 2-3**

**Skip if** `--skip-market` or `--skip-phase 4` is set, or not a trading day.

Read and follow the `today` skill (`.cursor/skills/pipeline/today/SKILL.md`).

Full pipeline:
1. DB/CSV freshness check
2. Yahoo Finance data sync (`weekly-stock-update`)
3. Fundamental data collection (quarterly financials)
4. Hot stock discovery (NASDAQ/KOSPI/KOSDAQ 100)
5. Multi-factor screening (P/E, RSI, volume, MA, FCF yield)
6. Turtle + Bollinger + Oscillator analysis (SMA 20/55/200, RSI, MACD, Stochastic, ADX)
7. TradingView Extended stages (default): live prices, backtests, sentiment, multi-timeframe analysis — skip with `--skip-tradingview`
8. Optional: `alphaear-news` + `alphaear-sentiment`
9. .docx report generation (includes TV data when available)
10. Slack posting to `#h-report` with stock thread to `#h-daily-stock-check`
11. Optional: AI-Trader platform sync (phase 5.6) — market intel fetch, signal feed browse, heartbeat poll. Skipped when `AI_TRADER_*` credentials not set or `--skip-ai-trader` flag passed.

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

**Persist & manifest**:
1. Write full phase payload to `outputs/daily-am/{date}/phase-4-market-intelligence.json` (if skipped, file still contains `{ "skipped": true, "reason": "..." }`).
2. Update `manifest.json` with `phase-4` / `market-intelligence` entry.
3. Return only `{ "status", "file", "summary" }` upstream.

---

### Phase 5: News & Content Intelligence

**Duration**: ~10-15 min | **Dependencies**: Phase 1 only | **PARALLEL with Phase 2-4**

**Skip if** `--skip-phase 5` is set.

Run two sub-skills. These can run sequentially within this phase:

#### 5a. bespin-news-digest

Read and follow `bespin-news-digest` skill (`.cursor/skills/pipeline/bespin-news-digest/SKILL.md`).

- Fetch latest Bespin Global news email from Gmail
- Extract all article URLs
- Per-article: Jina extraction + WebSearch + AI GPU Cloud classification
- Post 3-message Slack thread per article to `#press`
- Generate DOCX → Google Drive

#### 5b. twitter-timeline-to-slack

Read and follow `twitter-timeline-to-slack` skill (`.cursor/skills/pipeline/twitter-timeline-to-slack/SKILL.md`).

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

**Persist & manifest**:
1. Write full phase payload to `outputs/daily-am/{date}/phase-5-news-content.json`.
2. Update `manifest.json` with `phase-5` / `news-content` entry.
3. Return only `{ "status", "file", "summary" }` upstream.

---

### Phase 6: AI Research Intelligence

**Duration**: ~5-10 min | **Dependencies**: Phase 1 only | **PARALLEL with Phase 2-5**

**Skip if** `--skip-research` or `--skip-phase 6` is set.

Run two sub-skills:

#### 6a. hf-trending-intelligence

Read and follow `hf-trending-intelligence` skill (`.cursor/skills/hf/hf-trending-intelligence/SKILL.md`).

- Cross-reference HF daily papers, trending models, new datasets, community activity
- Score emerging trends before they go mainstream
- Post intelligence report to `#deep-research-trending` + Notion

#### 6b. paper-auto-classifier

Read and follow `paper-auto-classifier` skill (`.cursor/skills/research/paper-auto-classifier/SKILL.md`).

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

**Persist & manifest**:
1. Write full phase payload to `outputs/daily-am/{date}/phase-6-ai-research.json`.
2. Update `manifest.json` with `phase-6` / `ai-research` entry.
3. Return only `{ "status", "file", "summary" }` upstream.

---

### Phase 7: Dev Intelligence

**Duration**: ~3-5 min | **Dependencies**: Phase 1 only | **PARALLEL with Phase 2-6**

**Skip if** `--skip-phase 7` is set.

Run two sub-skills:

#### 7a. github-sprint-digest

Read and follow `github-sprint-digest` skill (`.cursor/skills/pipeline/github-sprint-digest/SKILL.md`).

- Fetch overnight GitHub activity (issues, PRs, reviews, comments) per user
- Aggregate across 5 managed projects
- Generate Korean summary
- Post to Notion sub-pages + Slack

#### 7b. standup-digest

Read and follow `standup-digest` skill (`.cursor/skills/pipeline/standup-digest/SKILL.md`).

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

**Persist & manifest**:
1. Write full phase payload to `outputs/daily-am/{date}/phase-7-dev-intelligence.json`.
2. Update `manifest.json` with `phase-7` / `dev-intelligence` entry.
3. Return only `{ "status", "file", "summary" }` upstream.

---

### Phase 8: Consolidated Morning Briefing

**Duration**: ~1 min | **Dependencies**: ALL phases complete | **Sequential (final)**

**Skip if** `--no-slack` is set.

**Input source (mandatory)**: Do **not** build the briefing from orchestrator memory or prior chat turns. **Read** `outputs/daily-am/{date}/manifest.json`, then **read** each `phase-0-preflight.json` … `phase-7-dev-intelligence.json` under the same directory. Derive all counts, status lines, and `[INCOMPLETE]` markers **only** from these files (and from explicit paths referenced inside them, e.g. report paths).

Post a master summary to `#효정-할일` using `slack_send_message` MCP tool.

**Main message** (Slack mrkdwn) — field values must be filled from phase files, not from recall:

```
*☀️ Morning Pipeline 완료* (YYYY-MM-DD, Nm Ns)

*Git Sync*: N/5 프로젝트 동기화, 총 M커밋 수신
*Calendar*: N개 이벤트 (HIGH N건), 집중 슬롯 N개
*Gmail*: N건 정리, 답장 필요 N건
*Market*: N개 종목 분석 — BUY N / SELL N / HOLD N
*News*: 기사 N건 (베스핀 N, 트위터 N)
*Research*: 논문 N건 (Tier A: N, Tier B: N)
*Dev*: N commits, N PRs, N blockers
*Paperclip*: {agent_count}개 에이전트 활성, 승인 대기 {approval_count}건, 예산 {budget_pct}% 사용

{[INCOMPLETE] sections if any phase failed}
```

**Thread replies** for each phase with detailed results — each reply body should be composed from the corresponding `phase-{N}-*.json` contents.

**Persist & manifest**:
1. Write `outputs/daily-am/{date}/phase-8-consolidated-briefing.json` containing: pointers to posted Slack timestamps (if any), `main_message_text`, per-thread summaries, and `sources: ["manifest.json", "phase-0-...json", ...]`.
2. Update `manifest.json`: append `phase-8` / `consolidated-briefing`, set `completed_at` to ISO now, set `overall_status` to `completed`, `completed_with_warnings`, or `failed` based on phase statuses in the manifest.
3. Optionally duplicate a compact snapshot to `outputs/pipeline-state/YYYY-MM-DD-am.json` for legacy consumers.

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

Each parallel phase runner **persists** its own `phase-{N}-{label}.json` and updates `manifest.json` when complete; the orchestrator collects only `{ status, file, summary }` from each subagent.

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

**Recovery / debugging**: Use `outputs/daily-am/{date}/manifest.json` to see phase order and status; inspect the latest successful `phase-{N}-{label}.json` files to resume mentally or re-run from a failed phase. If Phase 8 fails after posts, Slack content can be reconstructed from phase JSON files without relying on session context.

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
- Pipeline state is always persisted for debugging (`manifest.json` + per-phase JSON under `outputs/daily-am/{date}/`)
- Individual phase failures never cascade to other phases

## Coordinator Synthesis

When delegating to subagents:

- **Never use lazy delegation.** Provide specific inputs (file paths, data, context) to every subagent — not "based on your findings, do X."
- **Purpose statement required:** Every subagent prompt must include why the task matters and how its output is used downstream — e.g., "This work feeds the consolidated AM Slack briefing; phase outputs must match `outputs/daily-am/{date}/manifest.json` and `phase-{N}-{label}.json` so the final post reflects real phase status."
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
