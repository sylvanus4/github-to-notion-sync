---
name: batch-agent-runner
description: >-
  Self-contained batch processing engine with TSV state tracking and parallel
  subagent workers. Processes lists of items (URLs, tickers, documents)
  through configurable evaluation pipelines with automatic resume, retry, and
  progress reporting.
---

# Batch Agent Runner

Process a list of items through a configurable pipeline using parallel subagents
with TSV-based state tracking for resumability and fault tolerance.

## When to Use

- Processing 3+ items through the same evaluation pipeline
- Running analysis across multiple tickers, URLs, documents, or entities
- Any batch job that benefits from parallel execution and crash recovery
- User says "batch", "batch run", "batch process", "일괄 처리", "배치 실행"

## Do NOT Use

- Single-item processing (invoke the target skill directly)
- Real-time streaming tasks
- Tasks requiring sequential dependency between items

## Architecture

```
Conductor (this skill)
├── Reads batch-input.tsv (or generates from user request)
├── Maintains batch-state.tsv (resumable progress)
├── Dispatches parallel Task subagents (max 4 concurrent)
│   └── Each worker: reads item → runs pipeline → writes output → updates state
└── Aggregates results → summary report
```

## File Layout

| File | Purpose |
|------|---------|
| `batch/batch-input.tsv` | Input items (ID, type, target, extra_args) |
| `batch/batch-state.tsv` | Progress tracker (ID, status, started_at, completed_at, output_path, error) |
| `batch/batch-prompt.md` | Worker prompt template with `{{ITEM}}` placeholder |
| `batch/outputs/` | Per-item output files |

## TSV State Format

```tsv
id	status	target	started_at	completed_at	output_path	error
001	pending	AAPL	—	—	—	—
002	running	TSLA	2026-04-06T09:00	—	—	—
003	done	NVDA	2026-04-06T09:00	2026-04-06T09:05	batch/outputs/003-NVDA.md	—
004	error	META	2026-04-06T09:01	2026-04-06T09:03	—	timeout
```

Valid statuses: `pending` → `running` → `done` | `error` | `skipped`

## Execution Flow

### Step 1: Initialize

1. Read or create `batch/batch-input.tsv` from user request
2. Create or resume `batch/batch-state.tsv`
   - If state file exists with incomplete items, offer to resume
3. Validate input format

### Step 2: Configure Pipeline

Determine what each worker should do. Options:
- **Skill mode**: run a specific skill on each item (e.g., `daily-stock-check` per ticker)
- **Custom prompt**: use `batch/batch-prompt.md` template
- **Command**: run a shell command per item

### Step 3: Dispatch Workers

```
For each PENDING item (up to 4 concurrent):
  1. Update state → running + timestamp
  2. Launch Task subagent with:
     - Item data from input TSV
     - Pipeline instructions (skill or prompt)
     - Output path assignment
  3. On completion: update state → done + output_path
  4. On failure: update state → error + error message
  5. Pick next pending item
```

Use `Task` tool with `subagent_type: "generalPurpose"` and `model: "fast"` for
cost efficiency unless the pipeline requires deep reasoning.

### Step 4: Aggregate Results

After all items complete:
1. Count: done / error / skipped / total
2. Generate summary report at `batch/batch-summary-{date}.md`
3. If errors > 0, list failed items with error messages
4. Report total elapsed time

## Worker Prompt Template

`batch/batch-prompt.md` uses mustache-style placeholders:

```markdown
## Task

Process the following item through the analysis pipeline.

**Item**: {{TARGET}}
**Type**: {{TYPE}}
**Extra Args**: {{EXTRA_ARGS}}

### Instructions

1. [Pipeline-specific steps here]
2. Save output to: {{OUTPUT_PATH}}
3. Return a one-line summary of the result.
```

## Resume Protocol

When `batch-state.tsv` exists with non-terminal items:
1. Items with status `running` for > 10 minutes → reset to `pending`
2. Items with status `error` → ask user: retry or skip
3. Items with status `pending` → process normally
4. Items with status `done` → skip (already complete)

## Commands

| Input | Action |
|-------|--------|
| `batch run <input>` | Start/resume batch from input file or inline list |
| `batch status` | Show current progress from state TSV |
| `batch retry` | Retry all errored items |
| `batch reset` | Clear state file, start fresh |

## Constraints

- Max 4 concurrent subagents (per workflow-patterns.mdc)
- Each worker must be stateless — all context from input TSV + prompt
- Never modify `batch-input.tsv` during execution
- Always update `batch-state.tsv` atomically (read-modify-write)
- Log wall-clock time per item for performance tracking
