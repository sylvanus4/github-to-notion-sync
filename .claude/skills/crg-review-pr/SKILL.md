---
name: crg-review-pr
description: >-
  Comprehensive pull request review powered by code-review-graph's
  blast-radius analysis. Identifies all functions, classes, and files
  potentially affected by PR changes, then performs a targeted multi-dimension
  review.
disable-model-invocation: true
---

# CRG Review PR

Comprehensive pull request review powered by code-review-graph's blast-radius analysis. Identifies all functions, classes, and files potentially affected by PR changes, then performs a targeted multi-dimension review.

## Triggers

Use when the user asks to "review this PR with graph", "PR blast radius review", "PR 영향 분석 리뷰", "PR 블래스트 리뷰", "comprehensive PR review", "CRG PR review", "graph-aware PR review", or wants to understand the full impact of a pull request.

Do NOT use for uncommitted change review (use crg-review-delta). Do NOT use for building the graph (use crg-build-graph). Do NOT use for architecture queries (use crg-query).

## Workflow

### Step 1: Update Graph to PR State

```bash
code-review-graph update --base <base-branch>
```

This incrementally updates the graph for files changed between the base branch and HEAD.

### Step 2: Blast-Radius Analysis

For each changed file, use CRG MCP tools to:

1. **Identify changed symbols**: Functions, classes, methods that were added, modified, or deleted.
2. **Trace callers (1-2 hops)**: Find all direct and indirect callers of changed symbols.
3. **Trace callees**: Identify what the changed code depends on.
4. **Cross-file dependencies**: Map which other files import or are imported by changed files.

### Step 3: Multi-Dimension Review

Using the blast-radius context, review across these dimensions:

1. **API Contract**: Do signature changes break callers? Are return types consistent?
2. **Error Propagation**: Do new error paths propagate correctly to callers?
3. **Side Effects**: Do changes introduce unintended side effects in dependent code?
4. **Test Coverage**: Are blast-radius files covered by tests in the PR?
5. **Circular Dependencies**: Does the PR introduce circular imports?

### Step 4: Generate Report

Produce a structured report:

```markdown
## Blast Radius Summary
- Files directly changed: N
- Files in blast radius: M
- Functions affected: K

## Critical Findings
...

## Warnings
...

## Recommendations
...
```

## Output

Korean-language PR review report with blast-radius map, severity-ranked findings, and test coverage gaps for affected code paths.
