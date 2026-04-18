---
name: gbrain-maintain
version: 1.0.0
description: >-
  Comprehensive brain health maintenance: 13-dimension diagnostics, benchmark
  scoring, heartbeat loop, compiled-truth refresh, and Slack report output.
  Wraps `gbrain health`, `gbrain doctor`, `gbrain features`, `gbrain autopilot`,
  and `gbrain search` into an actionable maintenance workflow.
trigger: >-
  Use when the user asks to "check brain health", "maintain brain", "brain
  diagnostics", "gbrain maintain", "brain health score", "stale truths",
  "브레인 건강", "gbrain 점검", "브레인 유지보수", "stale compiled truth",
  "brain benchmark", "brain heartbeat", "gbrain-maintain", or any request
  to audit, benchmark, or repair the gbrain knowledge base.
do_not_use: >-
  Do NOT use for pipeline entity extraction (use gbrain-ingest). Do NOT use
  for morning briefing generation (use gbrain-briefing). Do NOT use for
  session-start preflight (use session-preflight). Do NOT use for general
  KB wiki compilation (use kb-compile).
composable_with:
  - gbrain-ingest
  - gbrain-briefing
  - session-preflight
  - ai-context-router
tags: [gbrain, health, maintenance, diagnostics, brain]
---

# gbrain-maintain

Comprehensive brain health maintenance skill adapted from `garrytan/gbrain`
`maintain` skill (v0.10). Provides 13-dimension health checks, benchmark
scoring, heartbeat cadence, compiled-truth refresh, and Slack report output.

## Prerequisites

- `gbrain` CLI installed and authenticated (`gbrain auth status`)
- Brain repository configured (`gbrain config`)
- Postgres/pgvector backend accessible

## Modes

| Mode | Trigger | Description |
|------|---------|-------------|
| `diagnose` | Default | Full 13-dimension health check |
| `fix` | `--fix` | Auto-remediate issues found |
| `heartbeat` | `--heartbeat` | Quick 3-check pulse (health, autopilot, stale) |
| `benchmark` | `--benchmark` | Score brain against quality benchmarks |
| `report` | `--report` | Generate and post Slack report |

## Workflow

### Step 1: Core Diagnostics (13 dimensions)

Run the full diagnostic suite:

```bash
gbrain doctor --json 2>/dev/null
gbrain health --json 2>/dev/null
gbrain features --json 2>/dev/null
gbrain autopilot status --json 2>/dev/null
```

#### Dimensions checked

| # | Dimension | Source | Pass criteria |
|---|-----------|--------|---------------|
| 1 | Page count | `gbrain health` | > 0 |
| 2 | Embedding coverage | `gbrain health` | > 90% |
| 3 | Stale compiled truths | `gbrain search "compiled-truth" --limit 50 --json` | 0 stale |
| 4 | Orphan pages (no backlinks) | `gbrain doctor` | < 10% of total |
| 5 | Broken internal links | `gbrain doctor` | 0 |
| 6 | Missing citations | `gbrain doctor` | < 5% of facts |
| 7 | Filing violations | `gbrain doctor` | 0 |
| 8 | Duplicate entities | `gbrain doctor` | 0 |
| 9 | Autopilot status | `gbrain autopilot status` | running |
| 10 | Last sync timestamp | `gbrain autopilot status` | < 24h ago |
| 11 | v0.10 features enabled | `gbrain features` | all enabled |
| 12 | Health composite score | `gbrain health` | >= 70/100 |
| 13 | Timeline coverage | `gbrain doctor` | > 80% entities have timeline |

### Step 2: Benchmark Scoring

Compute a weighted composite score:

| Dimension | Weight |
|-----------|--------|
| Embedding coverage | 20% |
| Citation compliance | 15% |
| Backlink coverage | 15% |
| Filing accuracy | 10% |
| Stale truth ratio | 15% |
| Autopilot health | 10% |
| Feature enablement | 5% |
| Timeline coverage | 10% |

Grade bands:
- **A** (90-100): Excellent — no action needed
- **B** (75-89): Good — minor improvements suggested
- **C** (60-74): Fair — several issues need attention
- **D** (40-59): Poor — immediate maintenance required
- **F** (0-39): Critical — brain is degraded

### Step 3: Heartbeat (quick pulse)

For `--heartbeat` mode, run only:

1. `gbrain health --json` → extract composite score
2. `gbrain autopilot status --json` → check running + last sync
3. `gbrain search "compiled-truth" --limit 10 --json` → count stale

Output a one-line status:
```
Brain: 85/100 | Autopilot: running (last sync 2h ago) | Stale truths: 0
```

### Step 4: Auto-Remediation (`--fix`)

When `--fix` is specified, attempt automatic fixes in order:

1. **Stale compiled truths**: re-compile via `gbrain compile <slug>`
2. **Missing embeddings**: `gbrain embed --all`
3. **Orphan pages**: suggest backlink candidates (do not auto-delete)
4. **Broken links**: list broken targets for manual resolution
5. **Missing citations**: flag pages for citation review
6. **Filing violations**: suggest correct directories

Never delete pages automatically. Suggest destructive actions for human approval.

### Step 5: Report Generation (`--report`)

Produce a structured markdown report:

```markdown
# Brain Health Report — {date}

## Summary
- **Score**: {score}/100 ({grade})
- **Pages**: {count}
- **Embedding Coverage**: {pct}%
- **Autopilot**: {status}

## Dimension Breakdown
| Dimension | Status | Detail |
|-----------|--------|--------|
| ... | PASS/WARN/FAIL | ... |

## Issues Found
1. {issue description} — {severity} — {suggested fix}

## Actions Taken (if --fix)
1. {action} — {result}

## Recommendations
- {recommendation}
```

Optionally post to Slack `#효정-할일` as a threaded message.

### Step 6: Persist Results

Save report to `outputs/gbrain-maintain/{date}/report.md`.

Save JSON diagnostics to `outputs/gbrain-maintain/{date}/diagnostics.json`:
```json
{
  "date": "YYYY-MM-DD",
  "score": 85,
  "grade": "B",
  "dimensions": { ... },
  "issues": [ ... ],
  "actions_taken": [ ... ]
}
```

## Conventions

Follow all conventions in `gbrain-conventions/`:
- `brain-first.md` — always check brain before external APIs
- `quality.md` — citation format, back-linking, notability gate
- `filing-rules.md` — subject-based filing protocol

## References

- Upstream: `garrytan/gbrain` `skills/maintain/SKILL.md`
- Local diagnostics: `gbrain doctor`, `gbrain health`, `gbrain features`
- Composable: `gbrain-ingest`, `gbrain-briefing`, `session-preflight`
