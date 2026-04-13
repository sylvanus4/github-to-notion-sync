# code-review-graph MCP Tools Reference

22 MCP tools exposed by `code-review-graph serve`. Review skills query these automatically when the server is available.

## Graph Lifecycle

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `build_or_update_graph_tool` | Build or incrementally update the graph | `repo_path` (optional) |

## Blast Radius & Review Context

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `get_impact_radius_tool` | Blast radius of changed files — traces callers, dependents, and tests | `changed_files: list[str]` |
| `get_review_context_tool` | Token-optimized review context with structural summary | `changed_files: list[str]` |
| `detect_changes_tool` | Risk-scored change impact analysis mapping diffs to affected functions, flows, and test gaps | — |

## Graph Queries

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `query_graph_tool` | Query callers, callees, tests, imports, inheritance for a node | `node_name: str`, `query_type: str` |
| `semantic_search_nodes_tool` | Search code entities by name or meaning | `query: str` |
| `embed_graph_tool` | Compute vector embeddings for semantic search | — |
| `find_large_functions_tool` | Find functions/classes exceeding a line-count threshold | `threshold: int` |

## Execution Flows

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `list_flows_tool` | List execution flows sorted by criticality | — |
| `get_flow_tool` | Get details of a single execution flow | `flow_id: str` |
| `get_affected_flows_tool` | Find flows affected by changed files | `changed_files: list[str]` |

## Community Detection

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `list_communities_tool` | List detected code communities | — |
| `get_community_tool` | Get details of a single community | `community_id: str` |

## Architecture

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `get_architecture_overview_tool` | Architecture overview from community structure, with coupling warnings | — |
| `list_graph_stats_tool` | Graph size and health metrics | — |

## Refactoring

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `refactor_tool` | Rename preview, dead code detection, community-driven suggestions | `action: str`, `target: str` |
| `apply_refactor_tool` | Apply a previously previewed refactoring | `refactor_id: str` |

## Documentation

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `get_docs_section_tool` | Retrieve documentation sections | `section: str` |
| `generate_wiki_tool` | Generate markdown wiki from communities | — |
| `get_wiki_page_tool` | Retrieve a specific wiki page | `page: str` |

## Multi-Repo

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `list_repos_tool` | List registered repositories | — |
| `cross_repo_search_tool` | Search across all registered repositories | `query: str` |

## MCP Prompts (5 Workflow Templates)

| Prompt | Description |
|--------|-------------|
| `review_changes` | Review changes since last commit with blast-radius context |
| `architecture_map` | Auto-generated architecture overview |
| `debug_issue` | Debug with structural graph context |
| `onboard_developer` | Onboard new developers with codebase map |
| `pre_merge_check` | Pre-merge validation with impact analysis |
