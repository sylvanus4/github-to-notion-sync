---
name: crg-review-delta
description: >-
  Token-efficient code review using the code-review-graph's structural
  context. Reviews only changed code with full dependency awareness, reducing
  LLM token consumption by providing AST-derived context instead of raw file
  content.
---

# CRG Review Delta

Token-efficient code review using the code-review-graph's structural context. Reviews only changed code with full dependency awareness, reducing LLM token consumption by providing AST-derived context instead of raw file content.

## Triggers

Use when the user asks to "review my changes", "delta review", "review diff", "변경사항 리뷰", "델타 리뷰", "토큰 효율 리뷰", "CRG review", "review with graph context", or wants a focused review of uncommitted or staged changes.

Do NOT use for PR-level review with blast-radius (use crg-review-pr). Do NOT use for building the graph (use crg-build-graph). Do NOT use for architecture queries (use crg-query).

## Workflow

### Step 1: Ensure Graph Is Current

```bash
code-review-graph update
```

This incrementally updates the graph for files changed since the last commit (default: HEAD~1).

### Step 2: Get Structural Context for Changed Files

Use the MCP tools to gather context. Call the CRG MCP server tools:

1. **Get changed symbols**: Identify which functions, classes, and methods were modified.
2. **Get callers/callees**: For each changed symbol, retrieve its direct callers and callees to understand impact.
3. **Get file structure**: Get the structural outline of changed files.

### Step 3: Review with Context

Combine the structural context with the actual diff to perform a focused review:

1. Check if changed function signatures match caller expectations.
2. Verify that callers of modified functions handle any new error cases or changed return types.
3. Flag unused imports or dead code paths introduced by the change.
4. Check for circular dependency introduction.

### Step 4: Report

Produce a structured review with:
- **Impact summary**: Which downstream functions/files are affected.
- **Issues found**: Categorized by severity (Critical / Warning / Info).
- **Token savings**: Estimate how many tokens were saved vs. reading full files.

## Output

Structured Korean review report with severity-ranked findings and affected dependency chains.
