---
name: code-review-graph
description: >-
  Manage the code-review-graph MCP server lifecycle: install, build, update,
  query, and visualize the AST-based code knowledge graph. Tree-sitter parses
  the codebase into function/class/import nodes with
  call/inheritance/test-coverage edges, enabling blast-radius analysis and
  token-optimized review co
disable-model-invocation: true
---

# Code Review Graph

Manage the code-review-graph MCP server lifecycle: install, build, update, query, and visualize the AST-based code knowledge graph. Tree-sitter parses the codebase into function/class/import nodes with call/inheritance/test-coverage edges, enabling blast-radius analysis and token-optimized review context (8.2x average reduction).

## Triggers

Use when the user asks to "build code graph", "code review graph", "graph status", "visualize code graph", "blast radius", "update code graph", "graph health", "code-review-graph", "코드 그래프", "그래프 빌드", "블라스트 래디어스", "코드 그래프 상태", or any lifecycle operation for the code-review-graph MCP server.

Do NOT use for code review itself (use deep-review, simplify, code-review-all, or ship — these skills query the graph automatically when available). Do NOT use for Knowledge Base wiki graphs (use graphify-runner). Do NOT use for architecture annotation graphs (use lat-md). Do NOT use for document knowledge graphs (use cognee).

## Prerequisites

- Python 3.10+
- `pip` or `pipx` (or `uv`/`uvx` for faster installs)

## Workflow

### 1. Check Installation

```bash
pip show code-review-graph
```

If not installed, proceed to step 2.

### 2. Install

```bash
pip install code-review-graph
code-review-graph install --platform cursor
```

Optional dependency groups:
```bash
pip install code-review-graph[embeddings]          # sentence-transformers
pip install code-review-graph[communities]         # Leiden community detection (igraph)
pip install code-review-graph[all]                 # All optional dependencies
```

### 3. Build Graph (First Time)

```bash
code-review-graph build
```

Initial build takes ~10s for 500 files. The graph is stored locally in `.code-review-graph/` (SQLite).

### 4. Incremental Update

```bash
code-review-graph update
```

Re-parses only changed files via SHA-256 hash diff. Completes in <2s for 2,900-file projects. Auto-hooks trigger this on file edits and git commits.

### 5. Status Check

```bash
code-review-graph status
```

Shows graph size (nodes, edges), health, and last update timestamp.

### 6. Visualize

```bash
code-review-graph visualize
```

Generates an interactive D3.js HTML graph with edge-type toggles and search.

### 7. Watch Mode

```bash
code-review-graph watch
```

Continuous graph updates as files change.

### 8. Wiki Generation

```bash
code-review-graph wiki
```

Auto-generates markdown wiki from detected community structure.

## MCP Server

The graph exposes 22 MCP tools via `code-review-graph serve`. Review skills (deep-review, simplify, code-review-all, ship, refactor-simulator) query these tools automatically when the server is available. See `references/mcp-tools.md` for the full tool catalog.

### Key Tools for Review Skills

| Tool | Purpose |
|------|---------|
| `get_impact_radius_tool` | Blast radius of changed files |
| `get_review_context_tool` | Token-optimized structural summary |
| `detect_changes_tool` | Risk-scored change impact |
| `query_graph_tool` | Callers, callees, imports, inheritance |
| `list_flows_tool` | Execution flows sorted by criticality |
| `list_communities_tool` | Detected code communities |
| `get_architecture_overview_tool` | Architecture map with coupling warnings |

### MCP Prompts (5 Workflow Templates)

| Prompt | Description |
|--------|-------------|
| `review_changes` | Review changes since last commit |
| `architecture_map` | Architecture overview |
| `debug_issue` | Debug with graph context |
| `onboard_developer` | Onboard with structural map |
| `pre_merge_check` | Pre-merge validation |

## Supported Languages (19 + Jupyter)

Python, TypeScript/TSX, JavaScript, Vue, Go, Rust, Java, Scala, C#, Ruby, Kotlin, Swift, PHP, Solidity, C/C++, Dart, R, Perl, Lua, Jupyter/Databricks (.ipynb)

## Configuration

Exclusions: `.code-review-graphignore` at repo root (glob patterns). In git repos, only tracked files are indexed.

## Troubleshooting

- **MCP server not responding**: Check `code-review-graph status`, rebuild with `code-review-graph build`
- **Stale graph**: Run `code-review-graph update` or enable watch mode
- **Missing nodes**: Verify language support, check `.code-review-graphignore` for over-exclusion
