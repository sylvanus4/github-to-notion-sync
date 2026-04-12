---
name: daily-pm-orchestrator
description: >-
  Evening Pipeline orchestrator: 5 phases covering knowledge consolidation,
  strategic analysis, code shipping, skill evolution, and weekly reports (Friday
  only) — with a consolidated EOD Slack briefing. Runs at 4:30 PM daily. Use
  when the user runs /daily-pm, asks to "run evening pipeline", "evening
  automation", "오후 파이프라인", "이브닝 오케스트레이터", "daily-pm", "daily evening",
  or wants to run the full evening automation. Do NOT use for partial evening
  routines (use eod-ship), individual skills (invoke them directly), or morning
  pipeline (use daily-am-orchestrator).
metadata:
  author: "thaki"
  version: "1.2.0"
  category: "orchestration"
---
# Daily PM Orchestrator — Evening Pipeline (4:30 PM)

Orchestrate 5 phases of evening automation across 8+ skills with parallel execution, Friday-conditional weekly reports, consolidated Slack briefing, and robust error handling.

## Configuration

- **Slack channel**: `#효정-할일` (Channel ID: `C0AA8NT4T8T`)
- **Design doc**: `docs/daily-automation-guide.md`
- **Pipeline state (canonical)**: `outputs/daily-pm/{date}/manifest.json` (see Pipeline Output Protocol)
- **Legacy mirror (optional)**: `outputs/pipeline-state/YYYY-MM-DD-pm.json` — may duplicate key fields from manifest for older tooling

## Pipeline Output Protocol

File-first execution: every phase persists structured JSON before downstream stages or the final briefing consume results.

- **Output directory**: `outputs/daily-pm/{date}/` where `{date}` is `YYYY-MM-DD` in the pipeline’s timezone.
- **Per-phase files**: Each phase writes exactly one file: `outputs/daily-pm/{date}/phase-{N}-{label}.json` (see Output Artifacts table below).
- **Manifest**: `outputs/daily-pm/{date}/manifest.json` tracks all phases, timing, status, and output file names. Initialize at run start; set `completed_at`, `overall_status`, and `warnings` when the run finishes (or fails).
- **Subagent Return Contract**: Any subagent dispatched for a phase returns **only** this JSON shape (no large payloads in chat): `{ "status": "completed|skipped|failed", "file": "outputs/daily-pm/{date}/phase-N-....json", "summary": "one-line summary" }`. The orchestrator merges `file` into the manifest and reads `summary` for logs.
- **Final briefing (Phase 6)**: Builds Slack content **exclusively** by reading `phase-1-*.json` through `phase-6-*.json` (or the latest manifest `phases[]` entries pointing to those files). Do not reconstruct totals from chat context or unstaged memory.

### manifest.json schema

```json
{
  "pipeline": "daily-pm",
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

While the run is in progress, `overall_status` may be `"running"` until Phase 6 finalizes the manifest.

### Output Artifacts

| Phase | Label | Output file | Skip flag |
| --- | --- | --- | --- |
| 0.5 | Paperclip evening check | `outputs/daily-pm/{date}/phase-0.5-paperclip.json` | (optional; graceful degradation) |
| 1 | Knowledge consolidation | `outputs/daily-pm/{date}/phase-1-knowledge-consolidation.json` | (none; first phase) |
| 1.5 | Role-Based Wiki KB Build | `outputs/daily-pm/{date}/phase-1.5-kb-build.json` | `--skip-kb-build`, `--skip-phase 1.5` |
| 1.8 | Strategic KB query | `outputs/daily-pm/{date}/phase-1.8-strategic-context.json` | `--skip-kb-context`, `--skip-phase 1.8` |
| 2 | Strategic analysis | `outputs/daily-pm/{date}/phase-2-strategic-analysis.json` | `--skip-strategy`, `--skip-phase 2` |
| 3 | Code shipping | `outputs/daily-pm/{date}/phase-3-code-shipping.json` | `--skip-phase 3` |
| 4 | Skill evolution | `outputs/daily-pm/{date}/phase-4-skill-evolution.json` | `--skip-skills`, `--skip-phase 4` |
| 5 | Weekly reports | `outputs/daily-pm/{date}/phase-5-weekly-reports.json` | Friday / `--friday`, `--skip-phase 5` |
| 6 | EOD briefing | `outputs/daily-pm/{date}/phase-6-eod-briefing.json` | `--no-slack` (still persist summary payload) |

## Usage

```
/daily-pm                         # full evening pipeline
/daily-pm --skip-phase 2          # skip Strategic Analysis
/daily-pm --only-phase 3          # run only Code Shipping
/daily-pm --skip-strategy         # skip daily-strategy-post
/daily-pm --skip-kb-context       # skip Phase 1.8 KB historical context
/daily-pm --skip-skills           # skip skill evolution
/daily-pm --friday                # force weekly reports even if not Friday
/daily-pm --no-slack              # suppress Slack notifications
/daily-pm --dry-run               # preview plan without execution
```

## Workflow

### Initialization

1. Record start time: `pipeline_start = now()`
2. Ensure output directory exists: `outputs/daily-pm/{date}/`
3. Initialize `manifest.json` at `outputs/daily-pm/{date}/manifest.json` with `pipeline: "daily-pm"`, `date`, `started_at`, `completed_at: null`, `phases: []`, `flags` (from CLI), `overall_status: "running"`, `warnings: []`
4. Initialize in-memory results tracker (must stay in sync with manifest phase entries):
   ```python
   results = {
     "date": "YYYY-MM-DD",
     "pipeline": "pm",
     "phases": {},
     "start_time": pipeline_start,
     "end_time": None,
     "is_friday": bool,
     "status": "running"
   }
   ```
5. Determine if today is Friday (for weekly reports)
6. Parse flags (`--skip-phase`, `--only-phase`, `--friday`, etc.) and append parsed flags to `manifest.json` → `flags`

---

### Phase 0.5: Paperclip Evening Check (Optional)

**Duration**: ~30s | **Dependencies**: None | **Critical**: NO

Run Paperclip end-of-day governance tasks: daily cost summary, task sync, and agent status update. Skip if Paperclip is unavailable (graceful degradation).

**Step 0.5a — Health check:**

```
Tool: paperclip_dashboard
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

If the call fails (connection refused, timeout), log "Paperclip unavailable — skipping evening governance" and skip the rest of Phase 0.5.

**Step 0.5b — Daily cost summary:**

```
Tool: paperclip_get_budget
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

Record today's spend vs budget for inclusion in the Phase 6 briefing. If budget >= 90% spent, add a warning to `manifest.json` → `warnings[]`.

**Step 0.5c — Task sync (paperclip-bridge):**

Run bidirectional sync between `tasks/todo.md` and Paperclip issues:

1. Read `tasks/todo.md` for items without `[PC:xxx]` annotations → create Paperclip issues via `paperclip_create_issue`
2. Query Paperclip for issues completed today → mark corresponding todo items as done
3. Update `[PC:xxx]` annotations in `tasks/todo.md`

Follow the `paperclip-bridge` skill workflow for conflict resolution rules.

**Step 0.5d — Heartbeat all agents (EOD status):**

```
Tool: paperclip_list_agents
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

For each agent with `status != "terminated"`:

```
Tool: paperclip_heartbeat
Input: { "agentId": "<agent-id>", "status": "evening pipeline completed" }
```

**Persist & manifest**: Write `outputs/daily-pm/{date}/phase-0.5-paperclip.json`. Update `manifest.json`.

---

### Phase 1: Knowledge Consolidation (knowledge-daily-aggregator)

**Duration**: ~3-5 min | **Dependencies**: None | **Sequential (first)**

Run the `knowledge_daily_aggregator.py` script which implements the full `knowledge-daily-aggregator` skill pipeline:

```bash
python scripts/knowledge_daily_aggregator.py --date {date}
```

The script executes 6 internal phases:

1. **Phase 1 — Collect**: Scans `outputs/today/{date}/`, `outputs/role-analysis/`, `outputs/sun-tzu/`, `outputs/twitter/`, and other pipeline output directories for today's artifacts (stock reports, strategy analyses, screener results, etc.)

2. **Phase 2 — Extract**: Extracts structured entities, learnings, and trading signals from collected artifacts using pattern matching and JSON parsing

3. **Phase 3 — Cognee ingest**: Ingests extracted knowledge into the Cognee knowledge graph using Claude API (for entity extraction) and FastEmbed (for local embeddings at zero API cost):
   - `cognee.add()` — stores text in vector DB
   - `cognee.cognify()` — builds knowledge graph with entity/relationship extraction
   - Gracefully handles Cognee failures (status: "partial") and continues

4. **Phase 4 — Entity resolution**: Placeholder for future cross-day entity deduplication

5. **Phase 5 — MEMORY.md update**: Appends a summary pointer line to `MEMORY.md`

6. **Phase 6 — Report**: Writes final manifest with aggregated stats

**Output directory**: `outputs/knowledge-daily-aggregator/{date}/` with per-phase JSON files.

**Configuration prerequisites**:
- `.env` must have `ANTHROPIC_API_KEY` set
- Cognee is configured via `.env` for Claude API (`LLM_PROVIDER=anthropic`, `LLM_MODEL=claude-sonnet-4-6`) + FastEmbed embeddings
- `pip install cognee fastembed` must be installed

```python
results["phases"]["phase1"] = {
  "status": "pass|partial|fail",
  "sources_collected": N,
  "entities_added": N,
  "learnings": N,
  "signals": N,
  "cognee_status": "completed|partial|skipped",
  "memory_entries": N,
  "duration_s": N
}
```

**Persist & manifest**: Copy the script's report (`outputs/knowledge-daily-aggregator/{date}/phase-6-report.json`) to `outputs/daily-pm/{date}/phase-1-knowledge-consolidation.json`. Append or update `manifest.json` → `phases[]` with `id: "phase-1"`, `label: "knowledge-consolidation"`, `status`, `output_file`, `started_at`, `elapsed_ms`, and a one-line `summary`.

On failure: **Warn and continue** — knowledge consolidation failure should not block shipping or strategy phases.

---

### Phase 1.5: Role-Based Wiki KB Build (kb-daily-build-orchestrator)

**Duration**: ~5-15 min | **Dependencies**: Phase 1 | **PARALLEL with Phase 1.8**

**Skip if** `--skip-kb-build` or `--skip-phase 1.5` is set.

Run the `kb-daily-build-orchestrator` skill (`.cursor/skills/kb-collectors/kb-daily-build-orchestrator/SKILL.md`).

Triggers all 7 role-specific KB collectors in parallel (sales, marketing, PM, engineering, design, finance, research), then compiles updated KB topics into wiki format.

1. Dispatch `/daily-kb-build` (or invoke the orchestrator skill directly)
2. Collectors run in 2 parallel batches:
   - Batch A: sales, marketing, PM (heavier — competitor scraping, Notion sync)
   - Batch B: engineering, design, finance, research (lighter — repo scan, web search)
3. After collection, compile updated topics with `kb-compile` and `kb-index`
4. Run `kb-lint` quality check

```python
results["phases"]["phase1_5"] = {
  "status": "pass|partial|fail|skipped",
  "files_collected": N,
  "topics_compiled": N,
  "lint_issues": N,
  "duration_s": N
}
```

**Persist & manifest**: Write Phase 1.5 result to `outputs/daily-pm/{date}/phase-1.5-kb-build.json`. Update `manifest.json` → `phases[]` with `id: "phase-1.5"`, `label: "kb-build"`.

On failure: **Warn and continue** — KB build failure does not block strategy, shipping, or skill evolution.

---

### Phase 1.8: Strategic KB Query (Unified Query Layer)

**Duration**: ~1-2 min | **Dependencies**: Phase 1 | **Sequential after Phase 1, before Phase 2**

**Skip if** `--skip-kb-context` or `--skip-phase 1.8` is set.

Query the unified knowledge layer (`scripts/kb_unified_query.py`) to retrieve historical strategic context that grounds Phase 2 strategy documents in accumulated knowledge rather than same-day data alone.

**Step 1.8a — Extract query targets from Phase 1:**

Read `outputs/daily-pm/{date}/phase-1-knowledge-consolidation.json` and extract:
1. Top entities discovered today (companies, technologies, market signals)
2. Key signal patterns from the aggregator (e.g., recurring trading themes, sector trends)

If Phase 1 failed or produced no entities, skip Phase 1.8 with `status: "skipped"`.

**Step 1.8b — Query historical context:**

For each extracted entity (max 5), run:

```bash
python scripts/kb_unified_query.py "prior strategic decisions related to {entity}" --sources all --top 5 --json
```

For each signal pattern (max 3), run:

```bash
python scripts/kb_unified_query.py "historical trend for {signal_pattern}" --sources all --top 5 --json
```

Apply a 30-second timeout per query. If exceeded, record an empty result and continue.

**Step 1.8c — Structure and save:**

Save to `outputs/daily-pm/{date}/phase-1.8-strategic-context.json`:

```json
{
  "date": "2026-04-07",
  "entity_context": {
    "NVIDIA": {
      "query": "prior strategic decisions related to NVIDIA",
      "kb_hits": 4,
      "cognee_hits": 1,
      "summary": "4 prior KB entries reference NVIDIA GPU demand cycle...",
      "relevance": 0.82
    }
  },
  "signal_context": {
    "sector_rotation_defensive": {
      "query": "historical trend for defensive sector rotation",
      "kb_hits": 2,
      "cognee_hits": 3,
      "summary": "Historical defensive rotations lasted 8-15 days...",
      "relevance": 0.75
    }
  },
  "sources_available": ["kb_fts", "cognee_graph"],
  "warnings": []
}
```

**Step 1.8d — Persist & manifest:** Update `manifest.json` → `phases[]` with `id: "phase-1.8"`, `label: "strategic-kb-context"`, `status`, `output_file: "phase-1.8-strategic-context.json"`, timing, and summary.

On failure: **Continue** — strategic context is advisory. Phase 2 (strategy post) proceeds without historical grounding if queries fail.

```python
results["phases"]["phase1_8"] = {
  "status": "pass|partial|fail|skipped",
  "entities_queried": N,
  "signals_queried": N,
  "total_kb_hits": N,
  "total_cognee_hits": N,
  "duration_s": N
}
```

---

### Phase 2: Strategic Analysis (daily-strategy-post)

**Duration**: ~5-10 min | **Dependencies**: Phase 1 | **Sequential after Phase 1**

**Skip if** `--skip-strategy` or `--skip-phase 2` is set.

Read and follow the `daily-strategy-post` skill (`.cursor/skills/pipeline/daily-strategy-post/SKILL.md`).

1. Collect all daily intelligence (aggregated in Phase 1) and historical context (Phase 1.8):
   - Email trends and topics
   - Sprint data and blockers
   - News highlights
   - Research discoveries
   - Market signals
   - KB historical context from `phase-1.8-strategic-context.json` (if available)

2. Run multi-role strategic analysis:
   - Company-level strategy (CEO/CSO perspective)
   - Team-level strategy (CTO/PM perspective)
   - Product-level strategy (Developer/UX perspective)

3. Post strategy documents to Slack

```python
results["phases"]["phase2"] = {
  "status": "pass|partial|fail",
  "documents_posted": N,
  "key_insights": [...],
  "duration_s": N
}
```

4. **Persist & manifest**: Write the full Phase 2 result object to `outputs/daily-pm/{date}/phase-2-strategic-analysis.json` (or a minimal `{status, reason}` object if skipped). Update `manifest.json` → `phases[]` for `phase-2` with `output_file`, timing, and `summary`.

---

### Phase 3: Code Shipping (eod-ship)

**Duration**: ~5-15 min | **Dependencies**: Phase 1 | **PARALLEL with Phase 2**

**Skip if** `--skip-phase 3` is set.

Read and follow the `eod-ship` skill (`.cursor/skills/pipeline/eod-ship/SKILL.md`).

Full pipeline:
1. **cursor-sync**: Sync `.cursor/` assets (commands, skills, rules) to all 5 repos
2. **Dev branch merge** (ai-platform-webui): Pull dev branch, merge into tmp
3. **release-ship** for current project:
   - Domain-split commits (domain-commit)
   - Git push
   - PR creation/update
4. **release-ship** for each of 5 managed projects (sequentially)
5. **Slack notification**: Consolidated shipping report

```python
results["phases"]["phase3"] = {
  "status": "pass|partial|fail",
  "projects_shipped": N,
  "total_commits": N,
  "total_issues": N,
  "cursor_sync": {"files_synced": N},
  "duration_s": N
}
```

6. **Persist & manifest**: Write the full Phase 3 result to `outputs/daily-pm/{date}/phase-3-code-shipping.json`. Update `manifest.json` for `phase-3`. If a subagent ran all or part of eod-ship, require return contract `{ status, file, summary }` where `file` points to this JSON path after write.

---

### Phase 4: Skill Evolution

**Duration**: ~3-5 min | **Dependencies**: Phase 1 | **PARALLEL with Phase 2-3**

**Skip if** `--skip-skills` or `--skip-phase 4` is set.

Run two sub-skills sequentially:

#### 4a. autoskill-evolve

Read and follow `autoskill-evolve` skill (`.cursor/skills/automation/autoskill-evolve/SKILL.md`).

1. Extract candidates from today's agent transcript files (`.jsonl`)
2. Judge each candidate against existing skills (add/merge/discard)
3. Apply decisions: create new skills or merge into existing ones
4. Log all decisions to changelog

#### 4b. skill-guide-generator

Read and follow `skill-guide-generator` skill (`.cursor/skills/automation/skill-guide-generator/SKILL.md`).

1. Scan all installed skills
2. Identify skills without corresponding guide documentation
3. Generate guide entries following the standard template
4. Update the README index

```python
results["phases"]["phase4"] = {
  "status": "pass|partial|fail",
  "autoskill": {"candidates": N, "added": N, "merged": N, "discarded": N},
  "guides": {"undocumented_found": N, "guides_generated": N},
  "duration_s": N
}
```

5. **Persist & manifest**: Write the full Phase 4 result to `outputs/daily-pm/{date}/phase-4-skill-evolution.json`. Update `manifest.json` for `phase-4`. Subagents for 4a/4b should return `{ status, file, summary }` after writing merged phase JSON (or append sub-results inside the single phase file).

---

### Phase 5: Weekly Reports (Friday only)

**Duration**: ~10-15 min | **Dependencies**: Phase 1 | **PARALLEL with Phase 2-4**

**Condition**: Only runs on Fridays OR when `--friday` flag is set.

**Skip if** not Friday (and no `--friday` flag) or `--skip-phase 5` is set.

Run two sub-skills:

#### 5a. weekly-status-report

Read and follow `weekly-status-report` skill (`.cursor/skills/pipeline/weekly-status-report/SKILL.md`).

- Aggregate 7 days of GitHub sprint data, Notion project updates, Slack channel summaries
- Generate structured Korean weekly report
- Output: .docx + Notion page + Slack post to `#효정-할일`

#### 5b. portfolio-report-generator

Read and follow `portfolio-report-generator` skill (`.cursor/skills/pipeline/portfolio-report-generator/SKILL.md`).

- Aggregate weekly status from all 5 managed projects
- Generate cross-project portfolio view: health scores, blockers, resource allocation
- Output: Notion page + Slack post + optional Google Drive upload

```python
results["phases"]["phase5"] = {
  "status": "pass|partial|fail|skipped",
  "is_friday": bool,
  "weekly_report": {"generated": bool, "path": "..."},
  "portfolio_report": {"generated": bool, "projects": N},
  "duration_s": N
}
```

3. **Persist & manifest**: Write the full Phase 5 result to `outputs/daily-pm/{date}/phase-5-weekly-reports.json` (include `status: "skipped"` and reason when not Friday / skipped). Update `manifest.json` for `phase-5`.

---

### Phase 6: Consolidated EOD Briefing

**Duration**: ~1 min | **Dependencies**: ALL phases complete | **Sequential (final)**

**Slack posting**: If `--no-slack` is set, skip MCP `slack_send_message` calls only; still load phase JSON files, compose text, write `phase-6-eod-briefing.json`, and finalize `manifest.json`.

1. **Load inputs (files only)**: Read `outputs/daily-pm/{date}/phase-1-knowledge-consolidation.json`, `phase-2-strategic-analysis.json`, `phase-3-code-shipping.json`, `phase-4-skill-evolution.json`, and `phase-5-weekly-reports.json`. Do not use chat history or unstaged context for numeric totals. If a file is missing (e.g. skipped phase), infer `status` from `manifest.json` → `phases[]` for that `id`.

2. **Compose briefing payload**: Build the main message and per-phase thread texts **only** from fields in those JSON files (and manifest summaries as fallback).

3. **Post** a master summary to `#효정-할일` using `slack_send_message` MCP tool when not `--no-slack`.

**Main message** (Slack mrkdwn) — values must be filled from the phase JSON files:

```
*🌙 Evening Pipeline 완료* (YYYY-MM-DD, Nm Ns)

*Knowledge*: +N 엔티티, +N 관계 (Cognee), MEMORY.md N건 업데이트
*Strategy*: N개 전략 문서 게시 (회사/팀/제품)
*Shipping*: N/5 프로젝트, N commits, N issues
*Skills*: N candidates (N added, N merged, N discarded)
*Weekly*: {보고서 링크 | N/A (금요일 아님)}
*Paperclip*: 일일 비용 ${cost_today}, 예산 {budget_pct}% 사용, 태스크 동기화 {sync_count}건

{[INCOMPLETE] sections if any phase failed}
```

**Thread replies** for each phase with detailed results derived from the same files.

4. **Persist & manifest**: Write `outputs/daily-pm/{date}/phase-6-eod-briefing.json` containing `{ "main_message_text": "...", "thread_plan": [...], "slack_posted": bool, "no_slack": bool }`. Set `manifest.json` → `completed_at` to ISO now, compute `overall_status` (`completed` | `completed_with_warnings` | `failed`) from phase statuses, append any cross-phase `warnings`, and set each phase’s final `summary` if not already set.

5. **Optional legacy mirror**: Copy or derive a compact snapshot to `outputs/pipeline-state/YYYY-MM-DD-pm.json` for backward compatibility (same date key as `{date}`).

---

## Parallelism Execution Strategy

| Batch | Phases | Notes |
|---|---|---|
| Sequential | Phase 1 (Knowledge) | Must run first |
| Parallel D | Phase 1.5 (KB Build) | After Phase 1, parallel with Phase 1.8 |
| Sequential | Phase 1 → Phase 1.8 (KB Context) → Phase 2 (Strategy) | Needs aggregated intelligence + historical context |
| Parallel A | Phase 3 (Code Shipping) | After Phase 1 |
| Parallel B | Phase 4 (Skill Evolution) | After Phase 1 |
| Parallel C | Phase 5 (Weekly, Friday only) | After Phase 1 |
| Final | Phase 6 (Briefing) — waits for ALL | Sequential |

Total max concurrent subagents: 3 (Phases 3, 4, 5 running in parallel with Phase 2).

---

## Friday-Conditional Logic

```python
import datetime
is_friday = datetime.datetime.now().weekday() == 4  # 0=Mon, 4=Fri

if is_friday or args.friday:
    run_phase5()  # weekly-status-report + portfolio-report-generator
else:
    results["phases"]["phase5"] = {"status": "skipped", "reason": "not Friday"}
```

When `--friday` flag is passed, Phase 5 runs regardless of the actual day.

---

## Error Handling

Recovery checkpoints: the latest successful phase output is always under `outputs/daily-pm/{date}/phase-N-*.json`; `manifest.json` lists which phases completed. Re-run from the first failed or missing phase after fixing the issue.

| Failure Type | Action |
|---|---|
| Phase 1 failure (Knowledge) | Continue Phases 3-5 (they don't strictly need it), skip Phase 2 |
| Phase 2 failure (Strategy) | Log error, continue — strategy is valuable but not blocking |
| Phase 3 failure (Shipping) | Critical for code — report prominently in briefing |
| Phase 4 failure (Skills) | Low impact — log and continue |
| Phase 5 failure (Weekly) | Medium impact on Fridays — report in briefing |
| Slack MCP unavailable | Log results to file, skip Slack posts |
| Phase-level timeout (>30 min) | Kill phase, mark `[TIMEOUT]`, continue |

Each phase catches its own errors and never propagates failures to other parallel phases.

---

## Examples

### Example 1: Full weekday pipeline (non-Friday)

```
/daily-pm
```

Runs Phases 1-4 and 6. Phase 5 skipped (not Friday). Knowledge → Strategy sequential, then Code Shipping + Skill Evolution in parallel.

### Example 2: Full Friday pipeline

```
/daily-pm
```

Runs all 6 phases including weekly reports. Same as above but with Phase 5 generating weekly-status-report and portfolio-report-generator.

### Example 3: Force weekly reports

```
/daily-pm --friday
```

Runs Phase 5 regardless of day. Useful for generating mid-week reports.

### Example 4: Skip strategy, only ship

```
/daily-pm --only-phase 3
```

Runs Phase 1 (knowledge, prerequisite), Phase 3 (shipping), Phase 6 (briefing).

### Example 5: Dry run

```
/daily-pm --dry-run
```

Prints execution plan showing phase ordering, Friday detection, and estimated durations.

## Safety Rules

- Never force-push or hard-reset any git repository
- Never auto-merge conflicting branches — report and skip
- Skill evolution candidates require human review before major changes
- Weekly reports are generated but never sent to external parties automatically
- Pipeline state is always persisted under `outputs/daily-pm/{date}/` (`manifest.json` + per-phase JSON) for debugging; optional legacy `outputs/pipeline-state/YYYY-MM-DD-pm.json`
- Individual phase failures never cascade to other phases

## Coordinator Synthesis

When delegating to subagents:

- **Never use lazy delegation.** Provide specific inputs (file paths, data, context) to every subagent — not "based on your findings, do X."
- **Purpose statement required:** Every subagent prompt must include why the task matters and how its output is used downstream — e.g., "This work feeds the EOD Slack briefing; knowledge, strategy, shipping, skill evolution, and Friday weekly outputs must be reflected honestly from `outputs/daily-pm/{date}/` artifacts."
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
