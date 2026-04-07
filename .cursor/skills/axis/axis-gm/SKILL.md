---
name: axis-gm
description: >-
  Axis 4 of the 6-Axis Personal Assistant. General Manager — cross-axis
  coordination, executive briefings, decision tracking, OKR management, and
  organizational operations. Scans all other axes' outputs for synergies and
  produces consolidated briefings. Use when the user asks for "axis gm",
  "general manager axis", "총괄 축", "GM axis", "axis-gm", "cross-axis
  summary", or wants the executive overview across all axes. Do NOT use for
  single-axis operations (use the specific axis). Do NOT use for daily pipeline
  orchestration directly (use daily-am-orchestrator or daily-pm-orchestrator).
metadata:
  author: thaki
  version: "1.0.0"
  category: axis-orchestrator
  axis: 4
  automation_level: 0
---

# Axis 4: General Manager

Cross-axis coordination hub. Reads all other axes' `outputs/axis/*/` directories,
detects synergies, produces consolidated briefings, manages decision queues,
and tracks OKR progress. This is the only axis that reads other axes' outputs.

## Principles

- **Single Responsibility**: Coordination and synthesis only — never executes
  domain-specific work that belongs to another axis
- **Context Isolation**: Writes to `outputs/axis/gm/{date}/`, reads from all axes
- **Read-Only Cross-Axis**: Reads other axes' outputs but never writes to them
- **File-First Data Bus**: All cross-axis data flows through output files

## Phase Guard Protocol

GM is the last axis to run and aggregates upstream outputs. Before each
phase, check if outputs from the current dispatch cycle already exist.

| Phase | Guard File | Skip Condition |
|-------|-----------|----------------|
| 1 (Collect) | `outputs/axis/gm/{date}/axis-outputs.json` | File exists |
| 2 (Synergy) | `outputs/axis/gm/{date}/synergies.json` | File exists |
| 3 (Briefing) | `outputs/axis/gm/{date}/daily-briefing.md` | File exists |

Pass `--force` to bypass all guards and re-run from scratch.
When a phase is skipped, log `REUSED — {guard_file}` in the dispatch manifest.

## Composed Skills

### Role Analysis
- `role-dispatcher` (12 roles), `executive-briefing`, all `role-*` skills

### Decision Management
- `decision-router` — personal vs team decision classification
- `decision-tracker` — Notion decision log with status tracking

### Planning
- `planning-daily-briefing` — team daily brief
- `weekly-planning-digest` — weekly roll-up
- `meeting-action-tracker` — action item follow-up

### Pipeline Coordination
- `daily-am-orchestrator`, `daily-pm-orchestrator` — existing daily engines
- `morning-ship`, `eod-ship`, `sod-ship` — git sync pipelines

### Document Operations
- `doc-review-orchestrator`, `doc-quality-gate`, `cross-domain-sync-checker`

### Meeting Intelligence
- `meeting-digest`, `notion-meeting-sync`, `smart-meeting-scheduler`

### Strategy
- `daily-strategy-post`, `pm-product-strategy`, `sun-tzu-analyzer`

### Status Reporting
- `weekly-status-report`, `portfolio-report-generator`, `github-sprint-digest`

### Visualization
- `visual-explainer` — HTML dashboard generation

## Workflow

### Morning Run (triggered by `axis-dispatcher` after Axis 2 + Axis 6 complete)

```
Phase 1: Cross-axis scan        → outputs/axis/gm/{date}/cross-axis-scan.json
Phase 2: Synergy detection      → outputs/axis/gm/{date}/synergies.json
Phase 3: Decision queue         → outputs/axis/gm/{date}/decisions-pending.json
Phase 4: Consolidated brief     → outputs/axis/gm/{date}/morning-digest.md
```

**Phase 1 — Cross-Axis Scan** *(guarded)*
Check Phase Guard: if `outputs/axis/gm/{date}/axis-outputs.json` exists,
SKIP. Otherwise read all `outputs/axis/*/` directories for today's date.
Collect each axis's summary file (e.g., `morning-summary.json`,
`morning-briefing.md`). Create a unified status map: axis name → status →
key findings. Write to `axis-outputs.json`.

**Phase 2 — Synergy Detection** *(guarded)* (Cross-Axis Intelligence Layer)
Check Phase Guard: if `outputs/axis/gm/{date}/synergies.json` exists,
SKIP. Otherwise apply the 8 detection rules defined in `references/synergy-rules.md`:
- R001: Company overlap (Axis 1 recruitment ↔ Axis 2 investment)
- R002: Topic-project alignment (Axis 3 learning ↔ Axis 5 sidepm)
- R003: Calendar-deadline conflict (Axis 6 life ↔ Axis 1/5)
- R004: News-investment signal (Axis 3 learning ↔ Axis 2 investment)
- R005: Interview prep boost (Axis 1 recruitment ↔ Axis 3 learning)
- R006: Side project demo → recruitment (Axis 5 sidepm ↔ Axis 1 recruitment)
- R007: Email → multi-axis routing (Axis 6 life → all)
- R008: Market event → calendar block (Axis 2 investment ↔ Axis 6 life)

Use the 3-tier fuzzy matching strategy (exact → alias → semantic) with
the entity alias registry at `outputs/axis/gm/entity-aliases.json`.
Write detected synergies to `synergies.json`.

**Phase 3 — Decision Queue**
Collect items tagged as requiring human decision from any axis. Classify using
`decision-router` logic (personal → `#효정-의사결정`, team → `#7층-리더방`).
Write to `decisions-pending.json`.

**Phase 4 — Consolidated Brief**
Compile a Korean executive morning digest with sections:
1. Overall status (all 6 axes health: GREEN/YELLOW/RED)
2. Top 3 priorities across all axes
3. Synergies detected
4. Decisions pending
5. Today's focus recommendation

### Evening Run (triggered by `axis-dispatcher` ~17:00, last axis)

```
Phase E1: Daily digest          → outputs/axis/gm/{date}/daily-digest.md
Phase E2: Axis health scores    → outputs/axis/gm/{date}/axis-health.json
```

**Phase E1 — Daily Digest**
Compile all axes' morning + evening outputs into a daily summary.
Include accomplishments, blockers, and items deferred to tomorrow.

**Phase E2 — Axis Health Scores**
Score each axis 0-100 based on:
- Completion rate (phases completed / total phases)
- Error count
- Decision resolution rate
- Data freshness
Write to `axis-health.json`.

### Weekly Run (Friday PM)

```
Phase W1: Weekly OKR progress   → outputs/axis/gm/{date}/weekly-okr.md
Phase W2: Axis self-improvement  → outputs/axis/gm/{date}/improvement-recs.json
Phase W3: Executive weekly      → outputs/axis/gm/{date}/weekly-briefing.md
```

**Phase W1 — OKR Progress**
Read each axis's weekly output and compile OKR progress.

**Phase W2 — Self-Improvement Recommendations**
Run `intent-alignment-tracker` on each axis's outputs to measure how well
each axis served its purpose. Low-scoring axes get flagged for review.

**Phase W3 — Executive Weekly Briefing**
Compile all weekly data into a comprehensive briefing.

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 1 | `outputs/axis/gm/{date}/cross-axis-scan.json` | All axes' status |
| 2 | `outputs/axis/gm/{date}/synergies.json` | Cross-axis overlaps |
| 3 | `outputs/axis/gm/{date}/decisions-pending.json` | Human decisions needed |
| 4 | `outputs/axis/gm/{date}/morning-digest.md` | Consolidated brief |
| E1 | `outputs/axis/gm/{date}/daily-digest.md` | EOD summary |
| E2 | `outputs/axis/gm/{date}/axis-health.json` | Per-axis health scores |
| W1 | `outputs/axis/gm/{date}/weekly-okr.md` | OKR tracking |
| W2 | `outputs/axis/gm/{date}/improvement-recs.json` | Axis improvement recs |
| W3 | `outputs/axis/gm/{date}/weekly-briefing.md` | Weekly executive brief |

## Dashboard Generation

On-demand, generate a unified HTML dashboard via `visual-explainer` showing:
- 6-axis radar chart (health scores)
- Timeline of today's activities per axis
- Pending decisions with urgency coloring
- Synergy connections as a network graph

Write to `outputs/axis/gm/{date}/dashboard.html`.

## Slack Channels

- `#효정-할일` — consolidated briefings and axis alerts
- `#효정-의사결정` — personal decisions requiring action
- `#7층-리더방` — team/CTO decisions (via decision-router)

## Automation Level

Tracked centrally in `outputs/axis/automation-levels.json`.
Full protocol: `axis-dispatcher/references/automation-levels.md`.

- **Level 0 (current)**: Report only — digest and synergy detection
- **Level 1**: Suggest priority ordering + auto-route decisions
- **Level 2**: Auto-post synergy alerts, auto-generate cross-axis briefing

Decision routing escalation requires explicit approval even at Level 2.

## Error Recovery

Follow the protocol in `axis-dispatcher/references/failure-alerting.md`.

The GM axis is the most resilient — if any source axis has no outputs for
today, it marks that axis as "NO DATA" in the cross-axis scan and continues.
Only a complete filesystem failure prevents execution.

As part of Phase 1, read `errors.json` from each axis's output directory
to include failure summaries in the cross-axis briefing.
Write GM-specific errors to `outputs/axis/gm/{date}/errors.json`.

## Gotchas

- This axis runs AFTER other axes in the morning routine — it depends on
  their outputs existing. The `axis-dispatcher` must enforce this ordering.
- Cross-axis scan must handle missing directories gracefully (an axis may
  not have run today)
- Synergy detection should use fuzzy matching (company names may vary across
  axes, e.g., "NVIDIA" vs "NVDA" vs "엔비디아")
- Decision queue should deduplicate items that appear in multiple axes
