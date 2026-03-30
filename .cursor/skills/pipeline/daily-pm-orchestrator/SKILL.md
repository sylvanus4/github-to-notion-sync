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
  version: "1.0.0"
  category: "orchestration"
---
# Daily PM Orchestrator — Evening Pipeline (4:30 PM)

Orchestrate 5 phases of evening automation across 8+ skills with parallel execution, Friday-conditional weekly reports, consolidated Slack briefing, and robust error handling.

## Configuration

- **Slack channel**: `#효정-할일` (Channel ID: `C0AA8NT4T8T`)
- **Design doc**: `docs/daily-automation-guide.md`
- **Pipeline state**: `outputs/pipeline-state/YYYY-MM-DD-pm.json`

## Usage

```
/daily-pm                         # full evening pipeline
/daily-pm --skip-phase 2          # skip Strategic Analysis
/daily-pm --only-phase 3          # run only Code Shipping
/daily-pm --skip-strategy         # skip daily-strategy-post
/daily-pm --skip-skills           # skip skill evolution
/daily-pm --friday                # force weekly reports even if not Friday
/daily-pm --no-slack              # suppress Slack notifications
/daily-pm --dry-run               # preview plan without execution
```

## Workflow

### Initialization

1. Record start time: `pipeline_start = now()`
2. Initialize results tracker:
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
3. Determine if today is Friday (for weekly reports)
4. Parse flags (`--skip-phase`, `--only-phase`, `--friday`, etc.)

---

### Phase 1: Knowledge Consolidation (knowledge-daily-aggregator)

**Duration**: ~5-10 min | **Dependencies**: None | **Sequential (first)**

Read and follow the `knowledge-daily-aggregator` skill (`.cursor/skills/pipeline/knowledge-daily-aggregator/SKILL.md`).

1. **Collect daily outputs**: Scan for today's artifacts:
   - Email summaries from morning gmail-daily-triage
   - Sprint digests from github-sprint-digest
   - News analyses from bespin-news-digest and twitter-timeline-to-slack
   - Meeting notes (if any meetings were analyzed today)
   - Code review outputs from any deep-review/simplify runs
   - Strategy briefings from any role-dispatcher runs
   - Paper reviews from paper-review or paper-auto-classifier
   - Stock analysis reports from today pipeline

2. **Cognee ingestion**: Ingest collected outputs into the knowledge graph
   ```bash
   cognee add --text "..." --dataset daily-YYYY-MM-DD
   cognee cognify
   ```

3. **Entity/relationship extraction**: Extract new entities and relationships

4. **MEMORY.md update**: Append new decisions, tasks, and issues discovered

```python
results["phases"]["phase1"] = {
  "status": "pass|partial|fail",
  "sources_collected": N,
  "entities_added": N,
  "relationships_added": N,
  "memory_entries": N,
  "duration_s": N
}
```

---

### Phase 2: Strategic Analysis (daily-strategy-post)

**Duration**: ~5-10 min | **Dependencies**: Phase 1 | **Sequential after Phase 1**

**Skip if** `--skip-strategy` or `--skip-phase 2` is set.

Read and follow the `daily-strategy-post` skill (`.cursor/skills/pipeline/daily-strategy-post/SKILL.md`).

1. Collect all daily intelligence (aggregated in Phase 1):
   - Email trends and topics
   - Sprint data and blockers
   - News highlights
   - Research discoveries
   - Market signals

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

---

### Phase 6: Consolidated EOD Briefing

**Duration**: ~1 min | **Dependencies**: ALL phases complete | **Sequential (final)**

**Skip if** `--no-slack` is set.

Post a master summary to `#효정-할일` using `slack_send_message` MCP tool.

**Main message** (Slack mrkdwn):

```
*🌙 Evening Pipeline 완료* (YYYY-MM-DD, Nm Ns)

*Knowledge*: +N 엔티티, +N 관계 (Cognee), MEMORY.md N건 업데이트
*Strategy*: N개 전략 문서 게시 (회사/팀/제품)
*Shipping*: N/5 프로젝트, N commits, N issues
*Skills*: N candidates (N added, N merged, N discarded)
*Weekly*: {보고서 링크 | N/A (금요일 아님)}

{[INCOMPLETE] sections if any phase failed}
```

**Thread replies** for each phase with detailed results.

Save pipeline state to `outputs/pipeline-state/YYYY-MM-DD-pm.json`.

---

## Parallelism Execution Strategy

| Batch | Phases | Notes |
|---|---|---|
| Sequential | Phase 1 (Knowledge) | Must run first |
| Sequential | Phase 1 → Phase 2 (Strategy) | Needs aggregated intelligence |
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
- Pipeline state is always persisted for debugging
- Individual phase failures never cascade to other phases
