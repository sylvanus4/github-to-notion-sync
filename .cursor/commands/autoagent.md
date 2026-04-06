# AutoAgent Commands

Dispatch AutoAgent operations via the appropriate skill.

## /autoagent loop

Run the meta-agent optimization loop on a harness.

**Required**: `--harness <path>` and `--tasks <path>`

**Modes**: `--mode prompt-only|code-only|full|team` (default: full)

```
/autoagent loop --harness agent.py --tasks data/bench/ --mode full --max-iter 20
```

Invokes: `autoagent-loop`

## /autoagent bench

Run a single benchmark evaluation (no mutations).

```
/autoagent bench --harness agent.py --tasks data/bench/
```

Invokes: `autoagent-benchmark`

## /autoagent diagnose

Analyze failure patterns from existing ATIF trajectories.

```
/autoagent diagnose --trajectories outputs/autoagent-trajectories/
```

Invokes: `autoagent-diagnostics`

## /autoagent scaffold

Generate a new agent harness from a template.

```
/autoagent scaffold --sdk openai --output agent.py
/autoagent scaffold --sdk claude --output agent.py
```

Uses: `HarnessTemplate.generate()` from `scripts/autoagent/`

## /autoagent status

Show current optimization status: best score, iteration count, recent experiments.

```
/autoagent status --ledger outputs/autoagent-ledger/ledger.json
```

Uses: `ExperimentLedger.summary()` from `scripts/autoagent/`

## /autoagent restore

Restore the best-performing harness snapshot.

```
/autoagent restore --ledger outputs/autoagent-ledger/ledger.json --output agent.py
```

Uses: `ExperimentLedger.restore_best()` from `scripts/autoagent/`
