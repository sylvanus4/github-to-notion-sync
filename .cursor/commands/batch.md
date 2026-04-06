---
description: "Run, monitor, and manage batch processing jobs via batch-agent-runner"
---

# /batch Command

Execute and manage batch processing jobs using the batch-agent-runner skill.

## Sub-commands

| Sub-command | Description |
|-------------|-------------|
| `run <task> <items-file> [--workers N] [--skill SKILL]` | Start a new batch job |
| `status` | Show current batch state |
| `resume` | Resume pending/error items |
| `retry` | Retry all error items |
| `cancel` | Cancel pending items |
| `results [--format md\|tsv\|json]` | Show batch results summary |
| `clean` | Archive completed batch state |

## Usage

```
/batch run "evaluate stock" data/watchlist.txt --workers 3 --skill evaluation-engine
/batch run "review paper" data/papers.txt --workers 2 --skill paper-review
/batch status
/batch resume
/batch retry
/batch results --format md
/batch clean
```

## Items File Format

One item per line (URL, ticker, file path, or any string identifier):

```
AAPL
MSFT
NVDA
TSLA
```

or:

```
https://arxiv.org/abs/2401.12345
https://arxiv.org/abs/2401.67890
```

## State File

Batch state is tracked in `batch/batch-state.tsv`:

```tsv
id	item	status	started	completed	output_path	error
1	AAPL	done	2026-04-06T09:00	2026-04-06T09:05	batch/outputs/AAPL.md	
2	MSFT	done	2026-04-06T09:00	2026-04-06T09:04	batch/outputs/MSFT.md	
3	NVDA	pending					
4	TSLA	error	2026-04-06T09:01		 	timeout after 300s
```

## Worker Execution

Each worker is a subagent that:
1. Claims the next `pending` item (marks as `running`)
2. Reads the batch prompt template from `batch/batch-prompt.md`
3. Executes the task for that item
4. Writes output to `batch/outputs/{item}.md`
5. Updates state to `done` or `error`

## Defaults

- `--workers`: 2 (max 4 per workflow-patterns constraint)
- `--skill`: none (uses batch-prompt.md generic template)
- Output directory: `batch/outputs/`
