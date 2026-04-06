# Experiment Protocol

Detailed keep/discard rules and overfitting checks for the autoagent optimization loop.

## Decision Matrix

| Condition | Action | Ledger Entry |
|-----------|--------|-------------|
| `new_score > baseline + min_delta` | KEEP | `kept: true, delta: +N` |
| `new_score == baseline` (within tolerance) | DISCARD | `kept: false, delta: 0, reason: "no improvement"` |
| `new_score < baseline` | DISCARD | `kept: false, delta: -N, reason: "regression"` |
| `new_score > baseline` but fails overfitting check | KEEP with FLAG | `kept: true, delta: +N, metadata.overfit_flag: true` |
| Benchmark run failed (infra error) | SKIP | `kept: false, delta: null, reason: "eval_error"` |

## Score Computation

The aggregate score is computed by `ScoreAggregator.aggregate()`:

```
aggregate_score = passed_tasks / total_tasks
```

Per-category scores are also tracked for diagnosis:
```
category_scores = {
    "coding": passed_coding / total_coding,
    "reasoning": passed_reasoning / total_reasoning,
    ...
}
```

A mutation is considered an improvement only if the aggregate score improves. Category-specific improvements that decrease the aggregate are not kept.

## Overfitting Detection Heuristics

### Heuristic 1: Single-Task Lift

If a mutation improves score on exactly 1 task and has no effect on others:
- Flag as potential overfit
- Check: is the failing task an outlier (unusual format, ambiguous instruction)?
- If yes: the "fix" might be a task-specific hack

### Heuristic 2: Prompt Length Explosion

If the system prompt grows by more than 50% in a single mutation:
- Flag as potential overfit
- Long prompts often encode task-specific instructions rather than general capabilities

### Heuristic 3: Tool Proliferation

If the harness adds more than 2 tools in a single mutation:
- This violates the one-mutation-per-iteration rule
- Split into separate experiments (one tool per iteration)

## Mutation Log Format

Each experiment in the ledger records:

```json
{
    "iteration": 7,
    "timestamp": "2026-04-06T14:23:01",
    "mutation_description": "Added 'verify before asserting' instruction to system prompt",
    "baseline_score": 0.72,
    "new_score": 0.76,
    "delta": 0.04,
    "kept": true,
    "harness_snapshot": "outputs/autoagent-ledger/snapshots/harness_iter0007.py",
    "benchmark_results": {
        "total_tasks": 25,
        "passed": 19,
        "pass_rate": 0.76,
        "category_scores": {"coding": 0.80, "reasoning": 0.70}
    },
    "duration_seconds": 342.5,
    "metadata": {"overfit_flag": false, "mutation_type": "prompt_edit"}
}
```

## Recovery Procedures

### Discarded Mutation Recovery

When a mutation is discarded:
1. Read the best harness from `ExperimentLedger.get_best_harness()`
2. Overwrite the active harness file with `ExperimentLedger.restore_best(target_path)`
3. Verify the restored harness matches the snapshot checksum

### Ledger Corruption Recovery

If `ledger.json` is corrupted:
1. List snapshot files in `outputs/autoagent-ledger/snapshots/`
2. Find the highest-numbered snapshot
3. Use that as the current harness
4. Reconstruct the ledger from snapshot metadata (partial recovery)

### Mid-Run Interruption

The loop is designed to be interruptible:
- Ledger saves after every iteration
- Harness snapshots are atomic (copy, not move)
- Restarting with the same `--ledger-dir` resumes from the last completed iteration
