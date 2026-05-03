---
name: crg-refactor
description: >-
  Use the code-review-graph to safely plan and validate refactoring
  operations: rename preview, dead code detection, move analysis, and
  dependency untangling.
---

# CRG Refactor

Use the code-review-graph to safely plan and validate refactoring operations: rename preview, dead code detection, move analysis, and dependency untangling.

## Triggers

Use when the user asks to "preview rename", "find dead code", "safe refactor", "리팩토링 미리보기", "데드 코드 탐지", "이름 변경 영향", "CRG refactor", "refactoring impact", "move function analysis", "unused code", or wants graph-backed refactoring guidance.

Do NOT use for code review (use crg-review-delta or crg-review-pr). Do NOT use for building the graph (use crg-build-graph). Do NOT use for architecture queries without refactoring intent (use crg-query).

## Operations

### Rename Preview

Before renaming a symbol, preview all locations that reference it:

1. Search the graph for the symbol by name.
2. Retrieve all callers, importers, and type references.
3. List every file and line that would need updating.
4. Flag any dynamic references (string-based lookups, reflection) that the graph cannot track.

### Dead Code Detection

Find functions, classes, or methods with zero callers in the graph:

1. Query the graph for all defined symbols.
2. Filter to symbols with no incoming edges (no callers, no importers).
3. Exclude entry points (main functions, API endpoints, test functions, CLI commands).
4. Report candidates with confidence level.

### Move Analysis

When moving a function or class to a different module:

1. Identify all current importers of the symbol.
2. Check if the destination module would create circular dependencies.
3. List all import statements that would need updating.
4. Verify the destination module's existing dependencies are compatible.

### Dependency Untangling

Identify tightly coupled file groups and suggest how to reduce coupling:

1. Find file pairs with bidirectional imports.
2. Identify hub files with high fan-in and fan-out.
3. Suggest interface extraction or dependency inversion opportunities.

## Output

Structured Korean report with refactoring candidates, impact scope, risk assessment, and specific file:line references for each proposed change.
