---
name: axis-learning
description: >-
  Axis 3 of the 6-Axis Personal Assistant. Continuous learning — paper review,
  knowledge base management, HuggingFace research radar, and structured study
  programs. Maintains a personal learning queue and tracks skill growth. Use
  when the user asks for "axis learning", "learning axis", "학습 축", "research
  axis", "axis-learning", or wants to manage their learning pipeline. Do NOT
  use for reviewing a single paper (use paper-review). Do NOT use for KB
  operations only (use kb-orchestrator). Do NOT use for HF trending only
  (use hf-trending-intelligence).
metadata:
  author: thaki
  version: "1.0.0"
  category: axis-orchestrator
  axis: 3
  automation_level: 0
---

# Axis 3: Learning

Manages continuous learning through paper reviews, knowledge base curation,
AI research radar, and structured study programs. Maintains a persistent
learning queue and tracks progress.

## Principles

- **Single Responsibility**: Only learning and knowledge growth
- **Context Isolation**: Writes to `outputs/axis/learning/{date}/`
- **Failure Isolation**: Paper review failure does not block KB compilation
- **File-First Data Bus**: Learning artifacts as files for cross-axis use

## Phase Guard Protocol

Before running the HF trending intelligence pipeline, check if it was
already invoked today (e.g., by a standalone `hf-trending-intelligence`
call). If outputs exist, reuse them instead of re-running.

| Phase | Guard File | Skip Condition |
|-------|-----------|----------------|
| 1 (AI radar) | `outputs/hf-trending/{date}/hf-trending-intelligence-report.md` | File exists with today's date |
| 3 (KB router) | `outputs/axis/learning/{date}/kb-routing.json` | File exists |

Pass `--force` to bypass all guards and re-run from scratch.
When a phase is skipped, log `REUSED — {guard_file}` in the dispatch manifest.

## Composed Skills

### Paper Discovery & Review
- `hf-papers` — daily HuggingFace papers
- `hf-trending-intelligence` — full AI radar pipeline
- `hf-topic-radar` — topic-focused trending scan
- `hf-leaderboard-tracker` — model benchmark tracking
- `paper-review` — full paper review with PM analysis
- `paper-auto-classifier` — auto-classify by topic
- `paper-archive` — central catalog
- `related-papers-scout` — find related work
- `paper-lifecycle-orchestrator` — end-to-end paper pipeline
- `alphaxiv-paper-lookup` — quick paper overview
- `feynman-*` skills (6 total) — advanced paper operations

### Knowledge Base
- `kb-orchestrator` — KB lifecycle
- All `kb-*` skills (9 total): ingest, compile, query, search, index, lint, output, auto-builder, daily-router
- `cognee` — knowledge graph engine

### Learning Programs
- `nlm-deep-learn` — accelerated learning with NLM
- `nlm-curriculum-builder` — course curriculum
- `docs-tutor`, `docs-tutor-setup` — interactive quizzes
- `adaptive-tutor` — 10-mode teaching

### Content Creation from Learning
- `nlm-slides`, `nlm-dual-slides`, `nlm-arxiv-slides` — slide generation
- `notebooklm`, `notebooklm-studio`, `notebooklm-research` — NLM operations
- `auto-research`, `auto-research-distribute` — autonomous research pipeline

### Research Operations
- `parallel-deep-research`, `deep-research-pipeline` — web research
- `tech-trend-analyzer` — technology trend evaluation

## Workflow

### Morning Run (triggered by `axis-dispatcher` ~07:30)

```
Phase 1: AI research radar      → outputs/axis/learning/{date}/ai-radar.json
Phase 2: Learning queue check   → outputs/axis/learning/{date}/queue-status.json
Phase 3: KB daily router        → outputs/axis/learning/{date}/kb-routing.json
Phase 4: Learning brief         → outputs/axis/learning/{date}/learning-briefing.md
```

**Phase 1 — AI Research Radar** *(guarded)*
Check Phase Guard: if `outputs/hf-trending/{date}/hf-trending-intelligence-report.md`
exists, read it and transform to `ai-radar.json` — SKIP re-invoking
`hf-trending-intelligence`. Otherwise run `hf-trending-intelligence` to detect
trending papers, models, and spaces. Cross-reference with tracked research
topics. Write to `ai-radar.json`.

**Phase 2 — Learning Queue Check**
Read `outputs/axis/learning/learning-queue.json` (persistent).
Surface items due for study today, papers queued for review, and
KB topics needing compilation. Write to `queue-status.json`.

**Phase 3 — KB Daily Router**
Run `kb-daily-router` to classify yesterday's pipeline outputs and
route them to appropriate KB topics. Write routing results.

**Phase 4 — Learning Brief**
Compile a Korean learning briefing:
1. Top 3 trending AI papers/models today
2. Learning items due today
3. KB health status
4. Study time recommendation

### Evening Run (triggered by `axis-dispatcher` ~17:00)

```
Phase E1: Paper queue process   → outputs/axis/learning/{date}/papers-processed.json
Phase E2: KB compile cycle      → outputs/axis/learning/{date}/kb-compile.json
```

**Phase E1 — Paper Queue Processing**
For each paper in today's queue (max 2 per day to avoid overload):
1. Run `paper-review` or `alphaxiv-paper-lookup` (depending on depth flag)
2. Archive to `paper-archive`
3. Mark as processed in learning queue

**Phase E2 — KB Compile Cycle**
If any new raw sources were routed in Phase 3, run `kb-compile` on
the affected KB topics.

### Weekly (Friday PM)

```
Phase W1: Learning progress     → outputs/axis/learning/{date}/weekly-progress.md
Phase W2: KB health report      → outputs/axis/learning/{date}/kb-health.json
```

**Phase W1 — Learning Progress**
Summarize papers reviewed, KB articles added, courses progressed.

**Phase W2 — KB Health**
Run `kb-lint` across all KBs. Report gaps and stale content.

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 1 | `outputs/axis/learning/{date}/ai-radar.json` | HF trending intelligence |
| 2 | `outputs/axis/learning/{date}/queue-status.json` | Learning queue status |
| 3 | `outputs/axis/learning/{date}/kb-routing.json` | KB daily routing |
| 4 | `outputs/axis/learning/{date}/learning-briefing.md` | Morning brief |
| E1 | `outputs/axis/learning/{date}/papers-processed.json` | Papers reviewed today |
| E2 | `outputs/axis/learning/{date}/kb-compile.json` | KB compilation results |
| W1 | `outputs/axis/learning/{date}/weekly-progress.md` | Weekly learning summary |
| W2 | `outputs/axis/learning/{date}/kb-health.json` | KB lint results |

## Persistent State

| File | Purpose |
|------|---------|
| `outputs/axis/learning/learning-queue.json` | Cross-day learning queue |
| `outputs/axis/learning/topics-config.json` | Tracked research topics |

Learning queue schema:
```json
[
  {
    "id": "learn-001",
    "type": "paper",
    "title": "Attention Is All You Need",
    "source": "arxiv:1706.03762",
    "priority": "high",
    "depth": "full",
    "status": "pending",
    "queued_at": "2026-04-07",
    "processed_at": null
  }
]
```

## Slack Channels

- `#deep-research-trending` — AI research radar posts
- `#효정-할일` — learning brief and study reminders

## Automation Level

Tracked centrally in `outputs/axis/automation-levels.json`.
Full protocol: `axis-dispatcher/references/automation-levels.md`.

- **Level 0 (current)**: Report only — radar and queue status
- **Level 1**: Auto-review queued papers + human approves KB additions
- **Level 2**: Auto-start paper-review for score > 8.5, auto-ingest to KB

KB compilation (expensive) requires explicit approval even at Level 2.

## Error Recovery

Follow the protocol in `axis-dispatcher/references/failure-alerting.md`.

HF API rate limits may cause Phase 1 to fail. If the trending scan fails,
fall back to `hf-papers` (simpler daily papers list). KB operations are
independent and can retry individually.

Write errors to `outputs/axis/learning/{date}/errors.json` using the
standard error record format (severity S1-S4, phase, impact, recovery).

## Gotchas

- HF trending intelligence is expensive (many API calls); consider caching
  with `hf-topic-radar` for focused scans on specific topics
- Paper review for a single paper can take 5-10 minutes; limit to 2/day
- KB compilation can be slow for large topic wikis; schedule during PM
- NLM (NotebookLM) operations require the `notebooklm-mcp` server
