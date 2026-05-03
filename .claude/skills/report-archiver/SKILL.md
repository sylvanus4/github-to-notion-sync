---
name: report-archiver
description: >-
  Manage the lifecycle of evaluation reports and analysis outputs: archive,
  index, search, compare across dates, prune stale entries, and export
  collections. Central registry for all structured outputs from ops skills.
---

# Evaluation Report Archiver

Manage the complete lifecycle of evaluation reports, scan results, and analysis
outputs produced by ops skills. Provides indexing, search, comparison, and
archival across time.

## When to Use

- Finding past evaluation reports by entity, date, or grade
- Comparing evaluations of the same entity across different dates
- Archiving or pruning old reports
- Building a portfolio of evaluations for trend analysis
- User says "archive", "find report", "compare evaluations", "리포트 검색", "평가 이력"

## Do NOT Use

- Generating new evaluations (use evaluation-engine)
- General file search (use Grep or Glob)
- Knowledge base article management (use kb-* skills)

## Index File

`data/ops/report-index.jsonl` -- one entry per archived report:

```jsonl
{"id":"eval-001","entity":"AAPL","domain":"stock-evaluation","date":"2026-04-06","grade":"B","composite":7.2,"path":"data/ops/evaluations/stock-evaluation-AAPL-2026-04-06.md","tags":["stock","tech"]}
{"id":"eval-002","entity":"attention-paper","domain":"paper-evaluation","date":"2026-04-05","grade":"A","composite":8.8,"path":"data/ops/evaluations/paper-evaluation-attention-2026-04-05.md","tags":["paper","llm"]}
{"id":"scan-001","entity":"github-trending","domain":"portal-scan","date":"2026-04-06","grade":null,"composite":null,"path":"data/ops/scans/github-trending-2026-04-06.jsonl","tags":["scan","github"]}
```

### Index Fields

| Field | Description |
|-------|-------------|
| `id` | Auto-generated `{type}-NNN` |
| `entity` | What was evaluated (ticker, paper title, tool name) |
| `domain` | Rubric domain or output type |
| `date` | ISO date of report |
| `grade` | Letter grade (A-F) or null for non-graded outputs |
| `composite` | Numeric composite score or null |
| `path` | Relative file path |
| `tags` | Classification tags |

## Operations

### Index (Register)

```
archive index <file-or-glob>
archive index data/ops/evaluations/*.md
```

Scan files, extract metadata from YAML frontmatter or report headers, and
append to `data/ops/report-index.jsonl`. Skip already-indexed paths.

### Search

```
archive search [--entity NAME] [--domain DOMAIN] [--grade A-F] [--after DATE] [--before DATE] [--tags tag1,tag2]
archive search --entity AAPL --after 2026-03-01
archive search --domain paper-evaluation --grade A
```

Query the index and display matching reports with summary info.

### Compare

```
archive compare <entity> [--last N]
archive compare AAPL --last 5
```

Load the last N evaluations of the same entity, build a trend table:

```
| Date       | Composite | Grade | Fundamentals | Technicals | Sentiment |
|------------|-----------|-------|--------------|------------|-----------|
| 2026-04-06 | 7.2       | B     | 7.5          | 6.8        | 7.0       |
| 2026-03-30 | 6.8       | B     | 7.0          | 6.5        | 6.9       |
| 2026-03-23 | 7.5       | B     | 7.8          | 7.2        | 7.1       |
```

Highlight improving and declining dimensions.

### Stats

```
archive stats [--domain DOMAIN]
```

Summary statistics: total reports, reports by domain, grade distribution,
average composite by domain, reports per week trend.

### Prune

```
archive prune --before DATE [--domain DOMAIN] [--dry-run]
```

Move reports older than DATE to `data/ops/archive/` directory and remove
from active index. Always dry-run first.

### Export

```
archive export [--domain DOMAIN] [--format csv|json|md] [--output PATH]
```

Export index data in specified format for external analysis.

## Auto-Indexing

When other ops skills create output files:
- `evaluation-engine` saves to `data/ops/evaluations/` -> auto-index
- `portal-scanner` saves to `data/ops/scans/` -> auto-index
- `batch-agent-runner` saves to `batch/outputs/` -> auto-index on request

## Integration Points

- **evaluation-engine**: Reports are auto-registered after generation
- **portal-scanner**: Scan results are indexed for history tracking
- **batch-agent-runner**: Batch outputs can be bulk-indexed
- **pipeline-inbox**: Search archive before re-evaluating (dedup)
- **today pipeline**: Daily reports feed into archive
- **knowledge-daily-aggregator**: Archive data enriches knowledge graph

## Constraints

- Index file is append-only during registration; prune uses read-modify-write
- Never delete report files directly; use prune to archive
- Composite scores must match report content (validation on index)
- Max 10,000 entries in active index; prune older entries to archive
