## NotebookLM Research

Run web or Google Drive research through NotebookLM to discover and import relevant sources.

### Usage

```
/nlm-research                                                  # interactive — choose notebook and research query
/nlm-research web <notebook> "search query"                    # web research
/nlm-research deep <notebook> "search query"                   # deep research (more sources, slower)
/nlm-research drive <notebook> "search query"                  # search Google Drive
/nlm-research status <notebook> <task_id>                      # check research progress
/nlm-research import <notebook> <task_id>                      # import discovered sources
```

### Execution

Read and follow `.cursor/skills/notebooklm-research/SKILL.md`.

Use the `notebooklm-mcp` MCP server tools: `research_start`, `research_status`, `research_import`.

### Examples

Research a market topic:
```
/nlm-research deep <notebook_id> "semiconductor supply chain disruptions 2026"
```

Search Google Drive for existing documents:
```
/nlm-research drive <notebook_id> "quarterly earnings analysis"
```

Full research pipeline:
```
/nlm-research web <notebook_id> "AI model market impact"
```
