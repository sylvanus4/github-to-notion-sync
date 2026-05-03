---
name: issue-to-code
description: >-
  Generate code drafts from GitHub issue descriptions. Reads the issue,
  analyzes codebase context via semantic search, creates an implementation
  plan, generates code on a feature branch, and opens a draft PR with
  "Resolves #N". Use when the user asks to "implement this issue", "issue to
  code", "generate code from issue", "이슈에서 코드 생성", "이슈 구현", "issue-to-code",
  or wants automated first-draft implementations from issue specifications. Do
  NOT use for manual coding tasks without an issue, PR review (use
  deep-review), or committing existing changes (use domain-commit).
disable-model-invocation: true
---

# Issue-to-Code Draft Generator

Automate the first step of development: transform a GitHub issue into a code draft with a ready-to-review PR.

## When to Use

- When a new issue is assigned and needs an initial implementation draft
- As part of the sprint-orchestrator pipeline for auto-drafting low-complexity issues
- When the user provides an issue number or URL and asks for a draft implementation

## Workflow

### Step 1: Fetch Issue Context

Use the GitHub MCP to retrieve the full issue:

```
gh issue view <issue-number> --json title,body,labels,assignees,milestone,comments
```

Extract:
- **Requirements**: From issue body (user stories, acceptance criteria, technical specs)
- **Labels**: For classification (bug, feature, enhancement, documentation)
- **Linked issues/PRs**: For dependency context. Check for existing open PRs referencing this issue — if one exists, report it instead of creating a duplicate.
- **Comments**: For clarifications and discussion history

### Step 2: Classify Complexity

Score the issue complexity (1-5) based on:
- Number of acceptance criteria
- Cross-file impact (single file vs multi-file vs multi-service)
- Test requirements mentioned
- Labels (`good-first-issue` = low, `epic` = high)

If complexity > 3, generate a plan document instead of code. Present to user for approval before proceeding.

### Step 3: Analyze Codebase Context

Use semantic search and grep to build implementation context:

1. **Find relevant files**: Search for entities mentioned in the issue (class names, API endpoints, component names). **Verify every file path exists** using Glob or Read before including in the plan — never reference made-up paths.
2. **Map dependencies**: Identify import chains and interfaces the implementation must satisfy
3. **Read conventions**: Check existing patterns in the same module (error handling, naming, testing style)
4. **Identify test patterns**: Find existing test files for the target module

### Step 4: Generate Implementation Plan

Before writing code, produce a structured plan:

```
Implementation Plan for #<issue-number>
=======================================
Issue: <title>
Complexity: <1-5>
Estimated files: <count>

Changes:
1. <file-path> — <description of change>
2. <file-path> — <description of change>

New files:
1. <file-path> — <purpose>

Tests:
1. <test-file-path> — <test cases to add>

Dependencies:
- <any new packages needed>
```

For complexity >= 3, pause and present this plan to the user before proceeding.

### Step 5: Create Feature Branch

```bash
git checkout -b issue/<issue-number>-<short-summary>
```

Branch naming follows the project's `CONTRIBUTING.md` convention.

### Step 6: Generate Code

Implement changes file-by-file following the plan:
- Follow existing code conventions discovered in Step 3
- Include proper error handling matching project patterns
- Add type hints/annotations matching project style
- Write tests for new functionality in the same directory/naming pattern as existing tests discovered in Step 3

### Step 7: Create Draft PR

```bash
git add -A
git commit -m "feat: <summary from issue>

- <change description>
- Resolves #<issue-number>"

git push origin HEAD:tmp
gh pr create --head tmp --base dev --draft \
  --title "#<issue-number> feat: <summary>" \
  --body "## Summary
Automated draft implementation for #<issue-number>.

## Changes
<list of changes>

## Test Plan
- [ ] Unit tests added
- [ ] Manual verification needed

> This is an AI-generated draft. Human review required before merge."
```

### Step 8: Report Results

```
Issue-to-Code Report
====================
Issue: #<number> — <title>
Branch: issue/<number>-<summary>
PR: #<pr-number> (draft)

Files Changed: <count>
Tests Added: <count>
Complexity: <score>/5

Status: Draft PR created — ready for human review
```

## Examples

### Example 1: Simple feature
User says: "Implement issue #42"
Actions:
1. Fetch issue #42 details
2. Classify as complexity 2 (single component change)
3. Analyze relevant codebase files
4. Generate code + tests
5. Create draft PR
Result: Draft PR with implementation ready for review

### Example 2: Complex feature
User says: "Draft code for issue #100"
Actions:
1. Fetch issue #100 details
2. Classify as complexity 4 (multi-service change)
3. Present implementation plan for approval
4. After approval, generate code incrementally
5. Create draft PR
Result: Implementation plan + draft PR after user approval

## Error Handling

| Error | Action |
|-------|--------|
| GitHub issue not found | Report error with issue number; suggest user verify URL or permissions |
| issue lacks sufficient detail | Generate implementation plan with assumptions; ask user to confirm before coding |
| complexity exceeds threshold | Produce plan document only; require user approval before generating code |
| branch creation fails | Check for uncommitted changes; suggest `git stash` or resolve conflicts |
| draft PR creation fails | Verify `gh` auth and remote; retry push; report PR creation error with manual steps |

## Guardrails

- **Never auto-merge**: Always create draft PRs requiring human review
- **Complexity gate**: Complexity >= 3 requires user approval of the plan
- **Test requirement**: Every code change must include corresponding test changes
- **No secrets**: Never hardcode credentials; use environment variables
- **Convention adherence**: Follow existing project patterns, not introduce new ones
- **Interface safety**: If the implementation requires modifying shared interfaces, types, or API contracts, pause and flag for user approval before proceeding
