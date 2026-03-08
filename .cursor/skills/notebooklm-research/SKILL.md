---
name: notebooklm-research
description: >-
  Run web and Google Drive research through NotebookLM -- start research queries,
  poll progress, and import discovered sources into notebooks.
  Use when the user asks to "research a topic in NotebookLM", "start NLM research",
  "web research and import sources", "Drive research", "deep research in NLM",
  "find sources for notebook", "discover sources", "import research sources",
  "research and build notebook", "NLM deep research", "poll research status",
  "NLM 리서치", "노트북LM 연구", "웹 리서치 시작", "소스 탐색",
  "리서치 시작", "딥 리서치", "드라이브 검색", "소스 발견",
  "NLM 웹 리서치", "리서치 결과 가져오기",
  or any NotebookLM research/discovery workflow.
  Do NOT use for notebook/source/note CRUD or querying -- use notebooklm.
  Do NOT use for content generation (audio, video, reports) -- use notebooklm-studio.
  Do NOT use for general web search without NotebookLM -- use parallel-web-search.
  Do NOT use for finance-specific web search -- use alphaear-search.
metadata:
  author: thaki
  version: 1.0.0
  category: research
---

# NotebookLM Research: Web & Drive Discovery

Run research queries through Google NotebookLM to discover relevant sources from the web or Google Drive, then import them into notebooks. Uses the `notebooklm-mcp` MCP server.

## Prerequisites

- `notebooklm-mcp` MCP server registered and authenticated (see `notebooklm` skill)
- A target notebook to import discovered sources into

## Available Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `research_start` | Start web or Drive research | `notebook_id`, `query`, `mode` (web/drive/deep) |
| `research_status` | Poll research progress | `notebook_id`, `task_id`, `max_wait` |
| `research_import` | Import discovered sources | `notebook_id`, `task_id`, `source_ids` (optional) |

## Workflow

### Standard research pipeline

1. **Start research:**

   ```
   research_start(notebook_id, query="semiconductor supply chain trends 2026", mode="web")
   ```

   Returns a `task_id` for tracking.

2. **Poll until complete:**

   ```
   research_status(notebook_id, task_id, max_wait=300)
   ```

   Returns discovered source list when done. `max_wait` is in seconds.

3. **Import sources:**

   ```
   research_import(notebook_id, task_id)
   ```

   Imports all discovered sources. Optionally pass `source_ids` to import a subset.

### Deep research mode

For comprehensive research covering more sources:

```
research_start(notebook_id, query="AI trends in financial markets", mode="deep")
```

Deep research takes longer (2-5 min) but returns more comprehensive results.

### Google Drive research

Search your Google Drive for relevant documents:

```
research_start(notebook_id, query="quarterly earnings report", mode="drive")
```

### Selective import

After reviewing discovered sources, import only the relevant ones:

1. `research_status(notebook_id, task_id)` -- review source list
2. `research_import(notebook_id, task_id, source_ids=["src_1", "src_3", "src_5"])`

## Polling Strategy

Research discovery typically takes 1-3 minutes (5+ for deep mode):

1. Call `research_start` to begin
2. Call `research_status` with `max_wait=300` -- it will block until complete or timeout
3. If timed out, call `research_status` again
4. Once complete, call `research_import`

## Stock Analytics Integration

### Research-driven stock analysis notebook

1. Create notebook: `notebook_create(title="NVIDIA Supply Chain Analysis")`
2. Start research: `research_start(notebook_id, query="NVIDIA supply chain semiconductor 2026", mode="deep")`
3. Wait: `research_status(notebook_id, task_id, max_wait=300)`
4. Import all: `research_import(notebook_id, task_id)`
5. Query: `notebook_query(notebook_id, query="What are the key supply chain risks?")`
6. Generate podcast: `studio_create(notebook_id, artifact_type="audio", format="deep_dive", confirm=True)`

### Market event research

When a significant market event occurs:

1. Create notebook: `notebook_create(title="Fed Rate Decision March 2026")`
2. Research: `research_start(notebook_id, query="Federal Reserve rate decision March 2026 market impact", mode="deep")`
3. Import sources and query for investment implications
4. Generate a briefing doc: `studio_create(notebook_id, artifact_type="report", report_format="Briefing Doc", confirm=True)`

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Research returns no results | Try a broader or different query; check auth status |
| Import fails | Verify research completed via `research_status` first |
| Timeout on deep research | Increase `max_wait` to 600 seconds |
| Drive research empty | Ensure Google Drive is connected to the same Google account |

## CLI Reference

```bash
nlm research start <notebook_id> --query "search terms" --mode deep
nlm research status <notebook_id> --task-id <task_id>
nlm research import <notebook_id> --task-id <task_id>
```

## Related Skills

- **notebooklm** -- notebook/source/note CRUD and querying
- **notebooklm-studio** -- content generation from research notebooks
- **alphaear-search** -- finance-specific web search (Jina/DDG/Baidu)
- **alphaear-news** -- real-time financial news aggregation
