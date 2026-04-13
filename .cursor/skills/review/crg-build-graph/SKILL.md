# CRG Build Graph

Build or update the code-review-graph AST-based knowledge graph. Supports full rebuild, incremental update from Git diff, and status checks.

## Triggers

Use when the user asks to "build graph", "update graph", "rebuild code graph", "그래프 빌드", "그래프 갱신", "CRG 빌드", "refresh graph", "index codebase", or after major code changes that require graph re-indexing.

Do NOT use for first-time installation (use crg-setup). Do NOT use for reviewing code (use crg-review-delta or crg-review-pr). Do NOT use for querying architecture (use crg-query).

## Modes

### Full Build

Rebuild the entire graph from scratch. Use after large refactors, branch switches, or when the graph seems stale.

```bash
code-review-graph build --full
```

### Incremental Update

Update only files changed since the last build. Default mode for routine use.

```bash
code-review-graph build
```

### Git-Aware Update

Update based on uncommitted changes or a specific commit range.

```bash
# Uncommitted changes
code-review-graph build --diff HEAD

# Specific commit range
code-review-graph build --diff <base>..<head>
```

### Status Check

Show current graph stats without modifying anything.

```bash
code-review-graph status
```

## Output

Report the graph stats (nodes, edges, files indexed) and any parsing errors. If files were skipped due to `.code-review-graphignore`, mention the count.
