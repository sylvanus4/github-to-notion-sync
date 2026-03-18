---
description: Auto-assembles architecture review package: scans linked Notion docs + git history, compiles into review materials.
argument-hint: "<component-or-system-name>"
---

# /arch-review-prep

Auto-assembles an architecture review package by scanning Notion for related docs, analyzing git history, running codebase-archaeologist for ownership, generating a dependency diagram, and compiling materials for reviewers. Sends package to reviewers via Slack.

## What This Command Does

Accepts a component or system name, scans Notion for related architecture docs, analyzes recent git history for the component, runs codebase-archaeologist for ownership map, generates a dependency diagram, compiles a review package, and sends to reviewers via Slack.

## Required Input

- **Component or system name** — Name of the component/system to review (e.g., `auth-service`, `inference-api`).

## Execution Steps

1. **Accept component/system name** — Parse input.
2. **Scan Notion for related architecture docs** — Search Notion for ADRs, design docs, architecture pages.
3. **Analyze recent git history for the component** — Use git log, blame, and file change patterns.
4. **Run codebase-archaeologist for ownership map** — Generate ownership, churn, bus factor.
5. **Generate dependency diagram** — Use visual-explainer for dependency graph.
6. **Compile review package** — Merge docs, git analysis, ownership map, diagram into single package.
7. **Send to reviewers via Slack** — Post package summary and links to `#효정-할일` or specified channel.

## Output

- Architecture review package (markdown + assets)
- Ownership map
- Dependency diagram
- Slack post with package links

## Skills Used

- deep-review: Architecture review lens
- backend-expert: Backend architecture patterns
- refactor-simulator: Impact analysis
- cognee: Knowledge graph for related docs (optional)
- codebase-archaeologist: Ownership and churn
- visual-explainer: Dependency diagram

## Example Usage

```
/arch-review-prep auth-service
/arch-review-prep inference-api
```
