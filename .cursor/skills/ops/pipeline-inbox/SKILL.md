---
name: pipeline-inbox
description: >-
  Drop URLs, tickers, or items now and process them later. A lightweight inbox
  pattern that decouples collection from processing. Items are appended to a
  persistent queue, then batch-processed on demand or at scheduled intervals.
user_invocable: true
---

# Pipeline Inbox

Collect items (URLs, tickers, topics, file paths) into a persistent queue for
deferred batch processing. Decouples "I found something interesting" from
"let me analyze it now."

## When to Use

- User shares multiple URLs or items during a conversation but wants to process later
- Building a backlog of items to analyze in a single batch run
- User says "inbox", "add to queue", "process later", "나중에 처리", "큐에 추가"
- Collecting items throughout the day for EOD processing

## Do NOT Use

- Single item that should be processed immediately (invoke the target skill)
- Items that require real-time response
- General task management (use tasks/todo.md)

## Data File

`data/ops/inbox.jsonl` — one JSON object per line (append-only):

```jsonl
{"id":"inbox-001","url":"https://example.com/article","type":"article","tags":["ai","research"],"added":"2026-04-06T10:30:00","status":"pending","notes":"Interesting paper on RAG"}
{"id":"inbox-002","target":"AAPL","type":"ticker","tags":["stock"],"added":"2026-04-06T11:00:00","status":"pending","notes":"Check earnings impact"}
```

### Field Definitions

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Auto-generated `inbox-NNN` |
| `url` or `target` | yes | The item to process (URL or identifier) |
| `type` | yes | `article`, `ticker`, `paper`, `tweet`, `repo`, `file`, `custom` |
| `tags` | no | Classification tags for routing |
| `added` | yes | ISO timestamp |
| `status` | yes | `pending`, `processing`, `done`, `error`, `skipped` |
| `notes` | no | User context about why this was queued |
| `output_path` | no | Set after processing |
| `pipeline` | no | Target skill/pipeline to use (auto-detected from type if omitted) |

## Operations

### Add Items

```
inbox add <url-or-item> [--type TYPE] [--tags tag1,tag2] [--notes "context"]
inbox add https://arxiv.org/abs/2401.12345 --type paper --tags ai,llm
inbox add TSLA --type ticker --notes "Check post-earnings momentum"
```

When adding:
1. Auto-detect type from URL pattern if not specified
2. Generate sequential ID
3. Append to `data/ops/inbox.jsonl`
4. Confirm addition with item count

### List Queue

```
inbox list [--status pending|done|error] [--type TYPE] [--tags TAG]
inbox list --status pending
```

Display: ID, type, target, tags, added date, status

### Process Queue

```
inbox process [--type TYPE] [--limit N] [--dry-run]
```

Processing flow:
1. Read all `pending` items from inbox
2. Group by type for pipeline routing:
   - `article` / `tweet` → `x-to-slack` or `unified-intel-intake`
   - `ticker` → `daily-stock-check`
   - `paper` → `paper-review`
   - `repo` → `tech-trend-analyzer`
   - `custom` → use `pipeline` field or ask user
3. Convert grouped items to `batch/batch-input.tsv`
4. Delegate to `batch-agent-runner` for parallel processing
5. Update inbox items with `done` status and `output_path`

### Drain (Clear Completed)

```
inbox drain [--before DATE]
```

Archive completed items to `data/ops/inbox-archive-{date}.jsonl` and remove
from active inbox.

### Stats

```
inbox stats
```

Show: total, pending, processing, done, error counts + breakdown by type.

## Auto-Routing Table

| Type | Default Pipeline | Target Skill |
|------|-----------------|--------------|
| `article` | intel-intake | unified-intel-intake |
| `tweet` | x-to-slack | x-to-slack |
| `paper` | paper-review | paper-review |
| `ticker` | stock-check | daily-stock-check |
| `repo` | tech-trend | tech-trend-analyzer |
| `file` | kb-ingest | kb-ingest |
| `custom` | (ask user) | — |

## Integration Points

- **batch-agent-runner**: Inbox delegates bulk processing to batch runner
- **today pipeline**: Can auto-process inbox items as a pipeline phase
- **daily-pm-orchestrator**: Optional EOD inbox drain
- **unified-intel-intake**: Handles article/tweet routing

## Constraints

- Inbox file is append-only during adds; status updates use read-modify-write
- Never delete items — archive them via `drain`
- Max 100 items per process run (paginate if larger)
- Deduplication: check URL/target uniqueness before adding
