# Code Review Graph Integration

When `code-review-graph` MCP server available, use graph tools for token-efficient context instead of brute-force file reading.

## Graph-Aware File Selection

Before reading changed files for review:
1. `get_impact_radius_tool` with changed files -> blast-radius file set
2. `get_review_context_tool` with blast-radius -> token-optimized structural summaries
3. `detect_changes_tool` -> risk-scored change impact

Use blast-radius set instead of raw `git diff --name-only` for review scope.

## Tool Mapping

| Need | Tool |
|------|------|
| Affected files | `get_impact_radius_tool` |
| Compact structural context | `get_review_context_tool` |
| Risk-scored impact | `detect_changes_tool` |
| Callers of function | `query_graph_tool` (query_type: callers) |
| Callees of function | `query_graph_tool` (query_type: callees) |
| Affected execution flows | `get_affected_flows_tool` |
| Batch files for parallel review | `list_communities_tool` |
| Architecture overview | `get_architecture_overview_tool` |
| Rename impact preview | `refactor_tool` |

## Fallback

If MCP server unavailable, fall back to `git diff`-based file selection. Never block review because graph is down.
