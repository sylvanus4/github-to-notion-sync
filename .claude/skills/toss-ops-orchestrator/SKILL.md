---
name: toss-ops-orchestrator
description: >-
  Unified Toss Securities operations workflow that orchestrates all 8 Toss
  integration skills in a composite pipeline: snapshot → parallel monitoring
  (FX, risk, portfolio recon, watchlist) → signal bridge → reporting (journal
  + morning briefing). Gracefully skips if tossctl is unavailable. Use when
  the user asks for "toss operations", "toss full check", "toss-ops", "증권 종합
  운영", "토스 전체 체크", "토스 오퍼레이션", or wants a comprehensive Toss Securities status
  update. Do NOT use for individual Toss checks (use the specific toss-*
  skill). Do NOT use for the daily pipeline (use today, which delegates to
  this orchestrator at Phase 1.5/5.5).
---

# Toss Securities Operations Orchestrator

Orchestrate all 8 Toss Securities integration skills into a single composite workflow: sequential snapshot, parallel monitoring, sequential decision chain, and reporting.

## Usage

```
/toss-ops                               # Full Toss operations workflow
/toss-ops --skip fx,journal             # Skip specific components
/toss-ops --mode snapshot-only          # Only run Phase 1 snapshot
/toss-ops --mode monitor-only           # Only run Phase 1+2
/toss-ops --dry-run                     # Show plan without executing
```

## Skip Flags

| Flag | Skips | Default |
|------|-------|---------|
| `snapshot` | `toss-daily-snapshot` | included |
| `fx` | `toss-fx-monitor` | included |
| `risk` | `toss-risk-monitor` | included |
| `recon` | `toss-portfolio-recon` | included |
| `watchlist` | `toss-watchlist-sync` | included |
| `signal` | `toss-signal-bridge` | included |
| `journal` | `toss-trade-journal` | included |
| `briefing` | `toss-morning-briefing` | included |

## Agent Team

| Phase | Agent | Skill | Execution | Output |
|-------|-------|-------|-----------|--------|
| 1 | Snapshot | `toss-daily-snapshot` | Task (sequential) | `outputs/toss/summary-{date}.json` |
| 2 | FX Monitor | `toss-fx-monitor` | Task (parallel) | `_workspace/toss-ops/02_fx.md` |
| 2 | Risk Monitor | `toss-risk-monitor` | Task (parallel) | `_workspace/toss-ops/02_risk.md` |
| 2 | Portfolio Recon | `toss-portfolio-recon` | Task (parallel) | `_workspace/toss-ops/02_recon.md` |
| 2 | Watchlist Sync | `toss-watchlist-sync` | Task (parallel) | `_workspace/toss-ops/02_watchlist.md` |
| 3 | Signal Bridge | `toss-signal-bridge` | Task (sequential) | `_workspace/toss-ops/03_signal-preview.md` |
| 4 | Trade Journal | `toss-trade-journal` | Task (sequential) | `_workspace/toss-ops/04_journal.md` |
| 4 | Morning Briefing | `toss-morning-briefing` | Task (sequential) | Slack post |

## Workflow

### Pre-flight

1. Check `tossctl` availability: `Shell: which tossctl`
   - If unavailable → log warning and skip entire harness gracefully. Return message: "tossctl not available — Toss operations skipped."
2. Parse `$ARGUMENTS` for `--skip`, `--mode`, `--dry-run`.
3. `Shell: mkdir -p _workspace/toss-ops`
4. If `--dry-run`, print the execution plan and stop.

### Phase 1: Account Snapshot (Sequential)

Launch 1 Task for `toss-daily-snapshot`:

```
You are a portfolio data collector.

## Skill Reference
Read and follow `.cursor/skills/trading/toss-daily-snapshot/SKILL.md`.

## Task
Capture current account status, positions, and watchlist.
Archive to `outputs/toss/summary-{date}.json`.

## Output
Also write a human-readable summary to `_workspace/toss-ops/01_snapshot.md`.

## Completion
Return a one-line summary of portfolio value and position count.
```

Wait for completion. If `--mode snapshot-only`, stop here.

### Phase 2: Parallel Monitoring (Fan-out)

Launch up to 4 sub-agents via the Task tool in a single message.

For each non-skipped monitor, use this prompt template (adapted per skill):

```
You are a {role} specialist.

## Skill Reference
Read and follow `.cursor/skills/trading/{skill-name}/SKILL.md`.

## Context
Read the account snapshot at `_workspace/toss-ops/01_snapshot.md`.

## Task
{Specific task for this monitor: FX rate tracking / risk assessment / portfolio drift / watchlist sync}

## Output
Write results to `_workspace/toss-ops/02_{agent-slug}.md`.

## Completion
Return a one-line status summary.
```

Wait for all Phase 2 agents to complete. If `--mode monitor-only`, stop here.

### Phase 3: Signal Bridge (Sequential — Decision Chain)

Unless `--skip signal`:

Launch 1 Task for `toss-signal-bridge`:

```
You are a trading signal evaluator.

## Skill Reference
Read and follow `.cursor/skills/trading/toss-signal-bridge/SKILL.md`.

## Context
Read all monitoring outputs at `_workspace/toss-ops/01_snapshot.md` and `_workspace/toss-ops/02_*.md`.
Also check for screener data at `outputs/screener-{date}.json` if available.

## Task
Evaluate signals from monitoring data and screener. Generate order previews in dry-run mode only.
DO NOT execute any actual trades.

## Output
Write signal previews to `_workspace/toss-ops/03_signal-preview.md`.

## Completion
Return count of actionable signals found.
```

### Phase 4: Reporting (Sequential)

Run trade journal and morning briefing sequentially.

**Trade Journal** (unless `--skip journal`):

```
You are a trade record keeper.

## Skill Reference
Read and follow `.cursor/skills/trading/toss-trade-journal/SKILL.md`.

## Task
Log recent trades and update P&L tracking.
Read context from `_workspace/toss-ops/01_snapshot.md`.

## Output
Write journal update to `_workspace/toss-ops/04_journal.md`.
```

**Morning Briefing** (unless `--skip briefing`):

```
You are a portfolio briefing analyst.

## Skill Reference
Read and follow `.cursor/skills/trading/toss-morning-briefing/SKILL.md`.

## Context
Read ALL workspace outputs: `_workspace/toss-ops/01_snapshot.md`, `_workspace/toss-ops/02_*.md`,
`_workspace/toss-ops/03_signal-preview.md`, `_workspace/toss-ops/04_journal.md`.

## Task
Produce a consolidated morning briefing combining portfolio status, risk assessment,
FX impact, signals, and overnight P&L. Post to Slack #h-daily-stock-check.

## Completion
Return briefing summary.
```

## Error Handling

| Failure | Action |
|---------|--------|
| tossctl unavailable | Skip entire orchestrator. Return graceful message. |
| Snapshot fails | Abort — downstream phases depend on snapshot data. |
| 1 monitor fails | Retry once. If still fails, proceed without that data. Note in briefing. |
| Signal bridge fails | Skip signals. Proceed to reporting. |
| Journal/briefing fails | Log warning. Non-critical for data pipeline. |

## Data Flow

```
Pre-flight (check tossctl)
    │
    ▼
Phase 1: Snapshot (sequential)
    │   outputs/toss/summary-{date}.json
    │   _workspace/toss-ops/01_snapshot.md
    │
    ▼
    ├─► FX Monitor     ──► 02_fx.md        ─┐
    ├─► Risk Monitor   ──► 02_risk.md       ─┤  Phase 2 (parallel)
    ├─► Portfolio Recon ──► 02_recon.md      ─┤
    └─► Watchlist Sync ──► 02_watchlist.md   ─┘
                                              │
                                              ▼
Phase 3: Signal Bridge (sequential)
    │   03_signal-preview.md
    │
    ▼
Phase 4: Reporting (sequential)
    ├─► Trade Journal   ──► 04_journal.md
    └─► Morning Briefing ──► Slack #h-daily-stock-check
```

## Integration with `today`

The `today` pipeline delegates to this orchestrator at:
- **Phase 1.5**: Snapshot + monitoring (Phase 1-2 of this orchestrator)
- **Phase 5.5**: Signal bridge + reporting (Phase 3-4 of this orchestrator)

The `skip-toss` flag in `today` controls whether this orchestrator is invoked.

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
