---
name: autoagent-loop
description: >-
  Autonomous agent harness optimization loop that iteratively improves a
  single-file agent harness (or skill) by mutating prompt, tools, and
  orchestration, running benchmarks, and keeping only score-improving changes.
  Adapts the meta-agent `program.md` pattern from kevinrgu/autoagent with
  score-driven
---

# AutoAgent Loop

Autonomous agent harness optimization loop that iteratively improves a single-file agent harness (or skill) by mutating prompt, tools, and orchestration, running benchmarks, and keeping only score-improving changes. Adapts the meta-agent `program.md` pattern from kevinrgu/autoagent with score-driven hill climbing and one-mutation-at-a-time discipline.

## When to Use

Use when the user asks to "autoagent loop", "autoagent", "autonomous harness optimization", "meta-agent loop", "harness hill-climb", "autoagent-loop", "오토에이전트", "하네스 최적화 루프", "에이전트 자율 개선", "score-driven agent optimization", or wants to run an iterative optimization loop on an agent harness or skill that keeps only improvements and discards regressions.

## When NOT to Use

- For prompt-only optimization without harness code changes — use `skill-autoimprove`
- For code-only optimization without prompt changes — use `meta-harness-optimizer`
- For multi-agent team design from scratch — use `harness`
- For continuous AFK loops with a task list — use `ralph-loop`
- For running benchmarks only without the optimization loop — use `autoagent-benchmark`
- For diagnosing failures only without the loop — use `autoagent-diagnostics`

## Prerequisites

- Python 3.11+
- `scripts/autoagent/` package installed (harness_template, harbor_adapter, atif_logger, experiment_ledger, failure_analyzer)
- Docker (required for `full` and `benchmark` modes; optional for `prompt-only` mode)
- Task suite: at least 5 benchmark tasks in Harbor JSON/YAML format or skill-autoimprove eval definitions

## Modes

| Mode | Mutation Scope | Benchmark | Delegates To |
|------|---------------|-----------|-------------|
| `prompt-only` | System prompt text only | Local eval (no Docker) | `skill-autoimprove` |
| `code-only` | Harness code: tools, retrieval, state | Docker-isolated | `meta-harness-optimizer` |
| `full` | Prompt + tools + orchestration | Docker-isolated | Internal (this skill) |
| `team` | Multi-agent team composition | Docker-isolated | `harness` + internal |

Default mode: `full`.

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--harness` | (required) | Path to harness file (agent.py) or SKILL.md |
| `--tasks` | (required) | Path to task suite directory or file |
| `--mode` | `full` | One of: prompt-only, code-only, full, team |
| `--max-iterations` | 20 | Maximum optimization iterations |
| `--min-delta` | 0.001 | Minimum score improvement to keep a mutation |
| `--patience` | 5 | Stop if no improvement for N consecutive iterations |
| `--sdk` | `openai` | SDK for new harness scaffolding: openai or claude |
| `--ledger-dir` | `outputs/autoagent-ledger` | Directory for experiment ledger |

## Pipeline

### Phase 1: Initialize

1. Load or scaffold harness file using `HarnessTemplate`
2. Load task suite using `TaskLoader`
3. Initialize `ExperimentLedger` at `--ledger-dir`
4. Initialize `ATIFLogger` at `outputs/autoagent-trajectories/`

### Phase 2: Baseline

1. Build Docker image from harness (skip if `prompt-only` mode)
2. Run full task suite using `DockerBenchmarkRunner` (or local eval for `prompt-only`)
3. Aggregate scores using `ScoreAggregator`
4. Record baseline in ledger

### Phase 3: Optimization Loop (repeat until stop condition)

For each iteration:

**Step 3a: Diagnose** — Analyze failures from the previous run:
- Invoke `FailureAnalyzer.analyze()` on ATIF trajectories
- Identify the highest-impact failure pattern
- Generate a prioritized fix suggestion

**Step 3b: Mutate** — Apply a single mutation guided by the diagnosis:
- `prompt-only`: Modify system prompt text in the editable section
- `code-only`: Modify tool implementations, retrieval logic, or state management
- `full`: Choose the highest-leverage mutation type (prompt, tool, config, or orchestration)
- `team`: Add/remove/reconfigure agents in the team composition

The mutation MUST be a single atomic change (one-mutation-per-iteration rule).

**Step 3c: Evaluate** — Re-run the benchmark:
- Build new Docker image (if code changed)
- Run full task suite
- Aggregate scores
- Record ATIF trajectories

**Step 3d: Decide** — Keep or discard:
- If `new_score > baseline_score + min_delta`: **KEEP** the mutation
- Else: **DISCARD** and restore the previous harness
- Apply overfitting check: "would this change still help if the easiest-to-fix task disappeared?"

**Step 3e: Log** — Update the experiment ledger with the full record.

### Phase 4: Report

1. Generate experiment summary from ledger
2. Produce markdown report with:
   - Score progression chart data
   - Kept vs discarded mutations table
   - Final harness diff from seed
   - Failure pattern evolution
3. Save report to `outputs/autoagent-ledger/report.md`

### Stop Conditions

- `max-iterations` reached
- `patience` exceeded (no improvement for N consecutive iterations)
- Score plateaued (detected by `ExperimentLedger.plateaued()`)
- Human interruption

## Output Artifacts

| Phase | Stage | Output File |
|-------|-------|-------------|
| 2 | Baseline | `outputs/autoagent-ledger/snapshots/harness_iter0001.py` |
| 3 | Each iteration | `outputs/autoagent-ledger/snapshots/harness_iter{N}.py` |
| 3 | Trajectories | `outputs/autoagent-trajectories/{trajectory_id}.json` |
| 3 | Ledger | `outputs/autoagent-ledger/ledger.json` |
| 4 | Report | `outputs/autoagent-ledger/report.md` |

## Key Rules (from program.md)

1. **One mutation per iteration** — Never compound changes. Isolation makes cause-effect clear.
2. **Score is the judge** — Keep/discard based on numeric score delta only. "It looks better" is not evidence.
3. **Overfitting prevention** — After each kept mutation, ask: "Remove the task this change was designed for. Is the change still worthwhile?" If no, flag it.
4. **Failure classes, not individuals** — Group failing tasks by root cause. Fix the class, not one task.
5. **Simplicity tiebreaker** — At equal scores, prefer fewer tools, shorter prompts, simpler orchestration.
6. **Fixed boundary inviolable** — Never modify content below the `FIXED ADAPTER BOUNDARY` marker in the harness.
7. **Log everything** — Record every experiment in the ledger, including discarded ones.

## Composability

- **Inner prompt loop**: `skill-autoimprove` handles prompt-layer mutations when mode is `prompt-only`
- **Inner code loop**: `meta-harness-optimizer` handles code-layer mutations when mode is `code-only`
- **Team design**: `harness` generates multi-agent team configurations for `team` mode
- **Failure diagnosis**: `autoagent-diagnostics` classifies failure patterns between iterations
- **Benchmark execution**: `autoagent-benchmark` runs Docker-isolated task suites

## Error Handling

- If Docker build fails: log the error, attempt to fix Dockerfile, retry once. If still failing, switch to local eval mode and warn.
- If a single task times out: record as `timeout` in ATIF, score as 0, continue with remaining tasks.
- If all tasks fail: do not mutate. Run `autoagent-diagnostics` for root cause, present to user.
- If ledger file is corrupted: restore from the most recent snapshot and replay from that point.

## Gotchas

- Docker must be running for `full`, `code-only`, and `team` modes. Check with `docker ps` before starting.
- The `--patience` parameter should be set higher (8-10) for large task suites where score improvements are incremental.
- In `prompt-only` mode, the harness file is not needed — the skill operates on a SKILL.md directly via `skill-autoimprove`.
- The overfitting check is advisory — it flags suspicious improvements but does not auto-discard. Human judgment required.

## Examples

### Run full optimization on a harness

```
User: autoagent loop --harness scripts/autoagent/examples/agent.py --tasks data/bench/coding-tasks/ --max-iterations 15
```

### Prompt-only optimization on a skill

```
User: autoagent prompt-only --harness .cursor/skills/trading/daily-stock-check/SKILL.md --tasks data/eval/stock-eval/
```

### Resume from existing ledger

```
User: autoagent full --harness scripts/autoagent/examples/agent.py --tasks data/bench/ --ledger-dir outputs/autoagent-ledger
```
