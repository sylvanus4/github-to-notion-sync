# CRG Query

Query the code-review-graph for architecture insights: dependency chains, call flows, module boundaries, symbol lookups, and structural patterns across the codebase.

## Triggers

Use when the user asks to "query the graph", "show dependencies", "who calls this function", "architecture query", "의존성 조회", "호출 흐름", "아키텍처 쿼리", "CRG query", "show call chain", "find imports", "module structure", or wants structural codebase insights without reading full files.

Do NOT use for code review (use crg-review-delta or crg-review-pr). Do NOT use for building the graph (use crg-build-graph). Do NOT use for refactoring analysis (use crg-refactor).

## Query Types

### Symbol Lookup

Find where a function, class, or variable is defined and used.

Use CRG MCP tools to search for a symbol by name and retrieve:
- Definition location (file, line)
- All references (callers, importers)
- Type information (function, class, method, variable)

### Call Chain

Trace the call chain from a given function — upstream (who calls it) and downstream (what it calls).

Useful for understanding:
- How deep a function's dependency tree goes
- Which entry points reach a given internal function
- Whether a function is a leaf node or a hub

### Dependency Graph

Map import/export relationships between files or modules.

Useful for:
- Identifying circular dependencies
- Understanding module boundaries
- Finding tightly coupled file groups

### File Structure

Get a structural outline of any file showing all classes, functions, and their relationships without reading the full file content.

### Cross-Module Flow

Trace data flow across module boundaries by following function calls that cross file or directory boundaries.

## Output

Structured Korean response with the query results, formatted as tables or trees depending on the query type. Include file paths and line numbers for all references.
