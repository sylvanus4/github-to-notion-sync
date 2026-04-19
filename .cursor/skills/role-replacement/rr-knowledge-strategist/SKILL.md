---
name: rr-knowledge-strategist
version: 1.0.0
description: >-
  Role Replacement Case Study: Knowledge Manager / Strategy Analyst — evening pipeline
  orchestrating knowledge consolidation, role-based wiki build, historical KB context
  retrieval, multi-role strategic analysis, code shipping, skill evolution, memory
  maintenance (Dream Cycle), and weekly reporting into a unified end-of-day intelligence
  lifecycle. Thin harness composing daily-pm-orchestrator, kb-daily-build-orchestrator,
  kb-daily-report, knowledge-daily-aggregator, daily-strategy-post, autoskill-evolve,
  and memkraft-dream-cycle into a Knowledge Strategist role pipeline with MemKraft-powered
  strategic memory, KB historical grounding, and Slack distribution.
tags: [role-replacement, harness, knowledge, strategy, kb, evening-pipeline]
triggers:
  - rr-knowledge-strategist
  - knowledge manager replacement
  - strategy analyst automation
  - knowledge strategist role
  - evening knowledge pipeline
  - KB strategy lifecycle
  - 지식 관리자 대체
  - 전략 분석가 자동화
  - 지식 전략가
  - 이브닝 지식 파이프라인
  - KB 전략 라이프사이클
do_not_use:
  - Individual KB operations (invoke kb-* skills directly)
  - Morning pipeline (use daily-am-orchestrator)
  - General web research (use parallel-web-search)
  - Single-role analysis without evening pipeline context (use specific role-* skill)
  - Code review without knowledge lifecycle (use deep-review)
  - Manual memory edits (update files directly)
composes:
  - daily-pm-orchestrator
  - kb-daily-build-orchestrator
  - kb-daily-report
  - knowledge-daily-aggregator
  - daily-strategy-post
  - autoskill-evolve
  - memkraft-dream-cycle
  - memkraft
  - ai-context-router
---

# Role Replacement: Knowledge Manager / Strategy Analyst

## Human Role Being Replaced

A Knowledge Manager / Strategy Analyst who manually:
- Aggregates the day's outputs (email summaries, sprint digests, news analyses, meeting notes, code reviews, strategy briefings, paper reviews, trading analysis) into a structured knowledge base
- Runs the Cognee knowledge graph pipeline (ingest → entity extraction → relationship building → MEMORY.md update → KB routing → gbrain entity push)
- Triggers 7 role-specific KB collectors in parallel (sales, marketing, PM, engineering, design, finance, research) and compiles updated topics into an interconnected wiki
- Queries historical KB context (prior strategic decisions, recurring signal patterns) to ground today's strategy in accumulated knowledge rather than same-day data alone
- Runs multi-role strategic analysis (CEO, CTO, PM, CSO perspectives) and distributes strategy documents to Slack
- Ships code across 5+ repositories with domain-split commits, cursor-sync, and GitHub Project tracking
- Evolves the skill ecosystem (autoskill-evolve for transcript mining, skill-guide-generator for documentation)
- Runs the MemKraft Dream Cycle (session extraction, topic consolidation, attention decay, orphan resolution, preference promotion, archive sweep)
- Generates Friday weekly status reports and cross-project portfolio reports
- Posts consolidated EOD briefings to Slack with per-phase threaded details

This skill replaces 2-3 hours of daily manual evening work (knowledge aggregation, strategy synthesis, code shipping, memory maintenance) into a single automated pipeline.

## Architecture

```
Phase 0: MemKraft Context Pre-load
  └─ ai-context-router → strategic memory, KB topic freshness, prior decisions

Phase 1: Knowledge Consolidation (knowledge-daily-aggregator)
  └─ 9 internal phases: collect → extract → Cognee ingest → entity resolution
     → MEMORY.md → MemKraft route → KB route → gbrain → report

Phase 1.5: Role-Based Wiki KB Build (kb-daily-build-orchestrator) [PARALLEL with 1.8]
  └─ 7 collectors (2 batches) → kb-compile → kb-index → kb-lint → kb-daily-report

Phase 1.8: Strategic KB Query [SEQUENTIAL after Phase 1, before Phase 2]
  └─ scripts/kb_unified_query.py → historical context for entity + signal grounding

Phase 2: Strategic Analysis (daily-strategy-post) [SEQUENTIAL after 1.8]
  └─ 5 phases: aggregate → role-dispatch (CEO/CTO/PM/CSO) → executive synthesis
     → strategy documents → Slack distribution

Phase 3: Code Shipping (eod-ship) [PARALLEL with Phase 2]
  └─ cursor-sync → dev merge → release-ship (×5 repos) → Slack report

Phase 4: Skill Evolution [PARALLEL with Phases 2-3]
  ├─ autoskill-evolve → transcript mining → add/merge/discard decisions
  └─ skill-guide-generator → undocumented skill → guide documentation

Phase 5: Weekly Reports (Friday only) [PARALLEL with Phases 2-4]
  ├─ weekly-status-report → 7-day aggregate → .docx + Notion + Slack
  └─ portfolio-report-generator → cross-project health + blockers

Phase 5.5: MemKraft Dream Cycle
  └─ 6 phases: session extraction → topic consolidation → attention decay
     → orphan resolution → preference promotion → archive sweep

Phase 6: Consolidated EOD Briefing
  ├─ Build from phase JSON files ONLY (file-first rule)
  ├─ Slack main post + threaded per-phase details → #효정-할일
  └─ MemKraft write-back → strategic patterns, KB insights
```

## Execution

### Phase 0: MemKraft Context Pre-load

Before any evening work, load accumulated strategic context.

**Step 0a — Strategic memory retrieval:**

```
ai-context-router query:
  - "prior strategic decisions from past 7 days"
  - "KB topics with freshness below 50%"
  - "recurring knowledge gaps identified in Dream Cycles"
  - "strategy document themes from past 3 posts"
```

**Step 0b — Structure pre-loaded context:**

Organize retrieved context into three buckets:
1. **Strategic continuity**: Prior decisions and their rationale (feeds Phase 2 grounding)
2. **KB health signals**: Stale topics, coverage gaps (feeds Phase 1.5 collector prioritization)
3. **Skill evolution patterns**: Repeated agent corrections, transcript patterns (feeds Phase 4 focus)

**Step 0c — Persist context:**

Write `outputs/daily-pm/{date}/phase-0-memkraft-context.json`:

```json
{
  "date": "YYYY-MM-DD",
  "strategic_continuity": {
    "recent_decisions": [...],
    "active_themes": [...]
  },
  "kb_health": {
    "stale_topics": [...],
    "coverage_gaps": [...]
  },
  "skill_patterns": {
    "correction_clusters": [...],
    "candidate_skills": [...]
  },
  "provenance": {
    "memkraft_hits": N,
    "wiki_hits": N,
    "cognee_hits": N
  }
}
```

### Phase 1: Knowledge Consolidation

Invoke `knowledge-daily-aggregator` as defined in `daily-pm-orchestrator` Phase 1.

```bash
python scripts/knowledge_daily_aggregator.py --date {date}
```

The script executes 9 internal phases:
1. **Collect** — Scan `outputs/` for today's artifacts (stock reports, strategy analyses, screener results, etc.)
2. **Extract** — Structured entities, relationships, decisions, learnings, and trading signals
3. **Cognee ingest** — `cognee.add()` + `cognee.cognify()` for knowledge graph building
4. **Entity resolution** — Cross-day entity deduplication ("NVIDIA" / "Nvidia" → single entity)
5. **MEMORY.md update** — Append significant learnings with date stamp and category tags
6. **MemKraft routing** — Route personal outputs to MemKraft with provenance tags
7. **KB routing** — Route artifacts to 9-topic LLM Knowledge Base via `kb-daily-router`
8. **gbrain entity ingest** — Push entity-relevant items to gbrain (non-blocking)
9. **Report** — Write manifest with aggregated stats

**Output**: `outputs/knowledge-daily-aggregator/{date}/manifest.json` + per-phase JSON files.

**Persist & manifest**: Copy the report to `outputs/daily-pm/{date}/phase-1-knowledge-consolidation.json`.

**MemKraft enhancement**: Use Phase 0 KB health signals to prioritize collection in stale topic areas. If `kb_health.stale_topics` includes "competitive-intel", boost that collector's source scope.

### Phase 1.5: Role-Based Wiki KB Build

Invoke `kb-daily-build-orchestrator` as defined in `daily-pm-orchestrator` Phase 1.5.

**Parallel with Phase 1.8.** Skip if `--skip-kb-build` flag is set.

1. Pre-flight: verify config files (`competitor-registry.yaml`, `social-feeds.yaml`, `notion-meeting-sync.yaml`)
2. **Batch A** (3 parallel): sales, marketing, PM — heavier collectors
3. **Batch B** (4 parallel): engineering, design, finance, research — lighter collectors
4. Collection summary: aggregate results, identify topics needing recompilation
5. Wiki compilation: `kb-compile` + `kb-index` per updated topic (max 4 concurrent)
6. Quality check: `kb-lint` consistency validation
7. Intelligence report: `kb-daily-report` → Korean digest to Slack `#효정-의사결정`

**MemKraft enhancement**: Use Phase 0's `kb_health.stale_topics` to prioritize which collectors run first in Batch A/B ordering. If a topic's freshness score < 30%, boost its collector's source search depth.

**Output**: `outputs/kb-daily-build/{date}/` with collection summary, build report, and intelligence report.

**Persist & manifest**: Write to `outputs/daily-pm/{date}/phase-1.5-kb-build.json`.

### Phase 1.8: Strategic KB Query

Query the unified knowledge layer for historical context that grounds Phase 2 strategy.

**Sequential after Phase 1, before Phase 2.** Skip if `--skip-kb-context` flag is set.

**Step 1.8a — Extract query targets from Phase 1:**

Read `outputs/daily-pm/{date}/phase-1-knowledge-consolidation.json`:
- Top entities discovered today (companies, technologies, market signals)
- Key signal patterns (recurring trading themes, sector trends)

If Phase 1 produced no entities, skip with `status: "skipped"`.

**Step 1.8b — Query historical context (max 5 entities, max 3 signals):**

```bash
python scripts/kb_unified_query.py "prior strategic decisions related to {entity}" --sources all --top 5 --json
```

30-second timeout per query. Empty result on timeout, continue to next query.

**Step 1.8c — Structure and save:**

Write `outputs/daily-pm/{date}/phase-1.8-strategic-context.json` with `entity_context` and `signal_context` maps.

**MemKraft enhancement**: Cross-reference KB hits with Phase 0 `strategic_continuity.recent_decisions`. If a current entity was part of a recent decision, flag for continuity in Phase 2 strategy documents.

### Phase 2: Strategic Analysis

Invoke `daily-strategy-post` as defined in `daily-pm-orchestrator` Phase 2.

**Sequential after Phase 1.8.** Skip if `--skip-strategy` flag is set.

1. **Aggregate** (Phase 2.1): Collect daily intelligence + historical context from Phase 1.8
2. **Role dispatch** (Phase 2.2): Activate CEO, CTO, PM, CSO perspectives via `role-dispatcher`
3. **Executive synthesis** (Phase 2.3): Cross-role consensus, conflicts, action items via `executive-briefing`
4. **Strategy documents** (Phase 2.4): Three Korean documents — company/team/product level
5. **Distribute** (Phase 2.5): Post to Slack, optionally upload to Google Drive

**MemKraft enhancement**: Include Phase 0 `strategic_continuity` in the aggregate intelligence for role dispatchers. This ensures strategy documents reference prior decisions and maintain narrative continuity across days.

**Output**: `outputs/daily-strategy-post/{date}/` with per-phase JSON files.

**Persist & manifest**: Write to `outputs/daily-pm/{date}/phase-2-strategic-analysis.json`.

### Phase 3: Code Shipping

Invoke `eod-ship` as defined in `daily-pm-orchestrator` Phase 3.

**Parallel with Phase 2.** Skip if `--skip-phase 3` flag is set.

1. `cursor-sync` — Propagate today's `.cursor/` changes across 5 repos
2. Dev branch merge (when `eod-ship` / project-registry defines merging `origin/dev` into the current branch; not a single-repo exception)
3. `release-ship` for current project: domain-commit → push → issue → PR
4. `release-ship` × 5 managed projects (sequential)
5. Slack consolidated shipping report

**Output**: `outputs/daily-pm/{date}/phase-3-code-shipping.json`.

### Phase 4: Skill Evolution

**Parallel with Phases 2-3.** Skip if `--skip-skills` flag is set.

**Phase 4a — autoskill-evolve:**
1. Extract candidates from today's agent transcripts (`.jsonl`)
2. Judge each candidate against existing skills (add/merge/discard)
3. Apply decisions and log to changelog

**MemKraft enhancement**: Use Phase 0 `skill_patterns.correction_clusters` to prioritize candidate extraction. If a user correction pattern appears 3+ times, auto-promote as a high-confidence skill candidate.

**Phase 4b — skill-guide-generator:**
1. Scan all installed skills for undocumented entries
2. Generate guide entries following the standard template
3. Update the README index

**Output**: `outputs/daily-pm/{date}/phase-4-skill-evolution.json`.

### Phase 5: Weekly Reports (Friday Only)

**Parallel with Phases 2-4.** Runs only on Fridays or when `--friday` flag is set.

**Phase 5a — weekly-status-report:**
- Aggregate 7 days of GitHub sprint data, Notion project updates, Slack channel summaries
- Generate structured Korean weekly report as .docx + Notion page + Slack post

**Phase 5b — portfolio-report-generator:**
- Cross-project portfolio view: health scores, blockers, resource allocation

**Output**: `outputs/daily-pm/{date}/phase-5-weekly-reports.json`.

### Phase 5.5: MemKraft Dream Cycle

Run `memkraft-dream-cycle` for nightly memory maintenance.

**6 sub-phases:**
1. **Session extraction** — `python scripts/memory/extract-sessions.py --incremental`
2. **Topic consolidation** — Merge session findings into `memory/topics/` files
3. **Attention decay** — `python scripts/memory/attention_decay.py --apply` (HOT→WARM→COLD→archive)
4. **Orphan resolution** — Find unresolved items that now have answers
5. **Preference promotion** — Detect repeated patterns (≥3 occurrences) → promote to preferences
6. **Archive sweep** — Move entries with score < 0.1 to `memory/archive/`

**Output**: `memory/dream-cycle/{date}-dream-cycle.md` + `outputs/daily-pm/{date}/phase-5.5-dream-cycle.json`.

### Phase 6: Consolidated EOD Briefing

**File-first rule**: Build Slack content **exclusively** by reading `phase-1-*.json` through `phase-5.5-*.json` and `manifest.json`. Do not reconstruct from chat context.

**Main message** (Slack mrkdwn to `#효정-할일`):

```
*🌙 Evening Pipeline 완료* (YYYY-MM-DD, Nm Ns)

*Knowledge*: +N 엔티티, +N 관계 (Cognee), MEMORY.md N건 업데이트
*KB Build*: N 토픽 컴파일, N 린트 이슈, N 인텔리전스 항목
*Strategy*: N개 전략 문서 게시 (회사/팀/제품)
*Shipping*: N/5 프로젝트, N commits, N issues
*Skills*: N candidates (N added, N merged, N discarded)
*Weekly*: {보고서 링크 | N/A (금요일 아님)}
*Dream Cycle*: N 세션 추출, N 토픽 통합, N 엔트리 디케이, N 프로모션

{[INCOMPLETE] sections if any phase failed}
```

**Thread replies** for each phase with detailed results.

**MemKraft write-back**: After posting, persist strategic learnings:

```
ai-context-router write:
  tier: HOT
  entries:
    - "Strategy themes: {top 3 themes from Phase 2}"
    - "KB health delta: {topics improved/degraded}"
    - "Skill evolution: {new skills created/merged}"
    - "Dream Cycle: {tier transitions, promoted preferences}"
  provenance: rr-knowledge-strategist/{date}
```

## Usage

```
/rr-knowledge-strategist              # Full evening pipeline
/rr-knowledge-strategist --skip-kb    # Skip KB build (Phase 1.5)
/rr-knowledge-strategist --skip-strategy  # Skip strategy analysis
/rr-knowledge-strategist --only-knowledge # Phases 0, 1, 1.5, 5.5 only
/rr-knowledge-strategist --friday     # Force weekly reports
/rr-knowledge-strategist --no-slack   # Suppress Slack, still persist files
/rr-knowledge-strategist --dry-run    # Preview plan without execution
```

All flags pass through to `daily-pm-orchestrator` which handles phase selection, parallelism, and error isolation.

## Parallelism Strategy

| Batch | Phases | Max Concurrent |
|-------|--------|---------------|
| Sequential | Phase 0 (MemKraft pre-load) | 1 |
| Sequential | Phase 1 (Knowledge consolidation) | 1 |
| Parallel D | Phase 1.5 (KB Build) | 1 |
| Sequential | Phase 1.8 (KB Context) → Phase 2 (Strategy) | 1 |
| Parallel A | Phase 3 (Code Shipping) | 1 |
| Parallel B | Phase 4 (Skill Evolution) | 1 |
| Parallel C | Phase 5 (Weekly, Friday only) | 1 |
| Final | Phase 5.5 (Dream Cycle) | 1 |
| Final | Phase 6 (Briefing) — waits for ALL | 1 |

Total max concurrent subagents: 3 (Phases 3, 4, 5 running in parallel with Phase 2).

## Error Handling

| Failure Type | Action |
|---|---|
| Phase 0 (MemKraft pre-load) failure | Continue without strategic context; log warning |
| Phase 1 (Knowledge) failure | Continue Phases 3-5; skip Phase 2 (needs aggregated intel) |
| Phase 1.5 (KB Build) failure | Continue; KB build is valuable but not blocking |
| Phase 1.8 (KB Context) failure | Continue Phase 2 without historical grounding |
| Phase 2 (Strategy) failure | Log error; strategy is valuable but not blocking shipping |
| Phase 3 (Shipping) failure | Critical — report prominently in briefing |
| Phase 4 (Skills) failure | Low impact — log and continue |
| Phase 5 (Weekly) failure | Medium impact on Fridays — report in briefing |
| Phase 5.5 (Dream Cycle) failure | Memory maintenance deferred to next run |
| Slack MCP unavailable | Save all outputs to files; skip Slack posts |
| Phase-level timeout (>30 min) | Kill phase, mark [TIMEOUT], continue |

Each phase catches its own errors and never propagates failures to other parallel phases.

## MemKraft Integration

### Pre-load Context (Phase 0)
- **Tier**: HOT (session-critical strategic context)
- **Sources**: ai-context-router → MemKraft personal + LLM Wiki official
- **Purpose**: Ground the evening pipeline in accumulated knowledge

### Write-back (Phase 6)
- **Tier**: HOT for today's insights, WARM for trend observations
- **Content**: Strategy themes, KB health changes, skill evolution, Dream Cycle outcomes
- **Provenance**: `rr-knowledge-strategist/{date}`

### Dream Cycle (Phase 5.5)
- **Tier transitions**: HOT → WARM → COLD → archive based on access frequency
- **Preference promotion**: Repeated patterns (≥3) auto-promoted to preferences
- **Orphan resolution**: Unresolved items matched against new evidence

## Knowledge Flow Diagram

```
Daily Outputs (email, sprint, news, meetings, code, trading)
  │
  ├─[Phase 1]─→ Cognee KG → Entity Resolution → MEMORY.md → KB Router → gbrain
  │
  ├─[Phase 1.5]─→ 7 Collectors → Wiki Compile → Lint → Intelligence Report
  │
  ├─[Phase 1.8]─→ KB Unified Query → Historical Context
  │
  ├─[Phase 2]─→ Role Dispatch (CEO/CTO/PM/CSO) → Executive Synthesis → Strategy Docs → Slack
  │
  ├─[Phase 4]─→ Transcript Mining → Skill Candidates → Add/Merge/Discard
  │
  └─[Phase 5.5]─→ Session Extract → Topic Consolidate → Decay → Promote → Archive
                    │
                    └─→ Next morning: MemKraft pre-load feeds Phase 0 again ───→ [CYCLE]
```

## Gaps Addressed by This Skill

| Gap | Resolution |
|-----|-----------|
| No unified evening orchestration | This harness provides single-trigger evening pipeline |
| KB build detached from strategy | Phase 1.8 connects KB historical context to Phase 2 strategy documents |
| Dream Cycle runs in isolation | Phase 0 pre-load feeds Dream Cycle insights back into next-day strategy |
| No strategic continuity across days | MemKraft write-back (Phase 6) → pre-load (Phase 0) creates a daily strategic memory loop |
| Skill evolution unaware of knowledge patterns | Phase 0 `skill_patterns` from MemKraft prioritize autoskill-evolve extraction |
| KB collector prioritization is static | Phase 0 `kb_health` dynamically prioritizes collectors for stale topics |

## Honest Reporting

- Report outcomes faithfully — never claim all phases passed when any failed
- Never suppress errors, partial results, or skipped phases
- Surface unexpected findings even if they complicate the narrative
- If a phase produces no actionable output, say so explicitly

## Subagent Contract

Every subagent dispatch MUST include:
1. **Purpose statement** — one sentence explaining why this subagent exists
2. **Absolute file paths** — all input/output paths as absolute paths
3. **Return contract** — subagent must return JSON: `{"status": "ok|error", "file": "<output_path>", "summary": "<1-line>"}`
4. Load-bearing outputs must be written to disk, not passed via chat context

## Examples

**Standard evening dispatch:**
User: "rr-knowledge-strategist" or "지식 전략가"
→ Runs full pipeline: KB collection → wiki compile → strategic analysis → skill evolution → Dream Cycle → Slack

**KB-only build without strategy:**
User: "rr-knowledge-strategist --kb-only"
→ Runs Phases 1-3 only (collect, compile, report), skips strategy and evolution phases

## Operational Runbook

### Daily Schedule
- **16:30 KST**: Run `/rr-knowledge-strategist` (or trigger via `daily-pm-orchestrator`)
- **Estimated duration**: 20-45 min (varies by Friday/weekday, KB compilation load)

### Prerequisites
- Python venv with `cognee`, `fastembed`, `python-docx` installed
- `.env` with `ANTHROPIC_API_KEY`, Cognee config, gbrain config
- Slack MCP connected (`#효정-할일`, `#효정-의사결정`)
- Notion MCP connected (for PM collector)
- `knowledge-bases/` directory initialized with `_config/` files
- `memory/memkraft.json` configured for Dream Cycle parameters

### Verification
- Check `outputs/daily-pm/{date}/manifest.json` for `overall_status`
- Verify Slack thread in `#효정-할일` has phase-by-phase details
- Confirm `memory/dream-cycle/{date}-dream-cycle.md` exists after Phase 5.5
- Verify `MEMORY.md` has today's entries from Phase 1

### Recovery
- If `manifest.json` shows a failed phase, fix the issue and re-run: `/daily-pm --only-phase N`
- Prior phase JSON files remain valid checkpoints and do not need re-generation
- Dream Cycle failures auto-retry on next evening run

## Safety Rules

- Never force-push or hard-reset any git repository
- Never auto-merge conflicting branches — report and skip
- Skill evolution candidates require human review before major changes
- Weekly reports are generated but never sent to external parties automatically
- Pipeline state always persisted to `outputs/daily-pm/{date}/` for debugging
- Strategy documents posted to internal Slack channels only
- Dream Cycle never deletes entries permanently — archives with retrieval metadata
