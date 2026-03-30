---
name: pr-to-issue-linker
description: >-
  Automatically detect and maintain bidirectional links between PRs and issues.
  On PR creation, find related issues from branch names, commit messages, and
  code changes. Update issues with PR status and auto-close on merge. Use when
  the user asks to "link PRs to issues", "bidirectional PR tracking",
  "PR-이슈 연결", "양방향 PR 추적", "pr-to-issue-linker", or wants automated
  PR-issue relationship management. Do NOT use for creating issues from commits
  (use commit-to-issue), PR review (use deep-review), or sprint triage (use
  sprint-orchestrator).
metadata:
  version: "1.0.0"
  category: "execution"
  author: "thaki"
---
# PR-to-Issue Linker

Maintain bidirectional links between PRs and issues for complete traceability from requirement to implementation.

## When to Use

- After PR creation to auto-link to related issues
- During sprint tracking to see issue→PR progress
- As part of the release pipeline to verify all issues have PRs

## Workflow

### Step 1: Detect PR-Issue Relationships

On PR creation or update, detect related issues through multiple signals:

**Branch name** (highest confidence):
```
issue/123-add-auth    → Issue #123
feature/PROJ-456      → Issue #456
fix/bug-789           → Issue #789
```

**Commit messages** (high confidence):
```
Resolves #123         → Issue #123
Fixes #456            → Issue #456
Closes #789           → Issue #789
Related to #101       → Issue #101 (soft link)
```

**PR body** (medium confidence):
Parse PR description for issue references (`#NNN`, issue URLs).

**Code analysis** (low confidence):
If no explicit references found, analyze changed files against open issue descriptions to find potential matches.

### Step 2: Classify Link Type

| Type | Signal | Action on Merge |
|------|--------|-----------------|
| `resolves` | "Resolves #N", "Fixes #N", "Closes #N" | Auto-close issue |
| `addresses` | "Addresses #N", "Part of #N" | Update issue, don't close |
| `related` | "Related to #N", "See #N" | Cross-reference only |

### Step 3: Update Issue with PR Info

Add a structured comment to the linked issue:

```markdown
🔗 **PR Linked**: #<pr-number> — <pr-title>

| Field | Value |
|-------|-------|
| Branch | `issue/<number>-<summary>` |
| Author | @<author> |
| Status | Open (Draft) |
| CI | ⏳ Running |
| Link Type | Resolves |

Files changed: <count>
Lines: +<additions> / -<deletions>
```

### Step 4: Track PR Lifecycle

Update the issue comment as the PR progresses:

| PR Event | Issue Update |
|----------|-------------|
| PR opened | Add "PR Linked" comment |
| Review requested | Update: "Review requested from @reviewer" |
| Review approved | Update: "✅ Approved by @reviewer" |
| CI passes | Update: "CI ✅" |
| CI fails | Update: "CI ❌ — <failure summary>" |
| PR merged | Close issue (if `resolves` type) + final comment |
| PR closed (not merged) | Update: "PR closed without merge" |

### Step 5: Update GitHub Project Fields

When PR is linked:
- Set issue `Status` to "In Progress" (if was "Ready")
- Add PR URL to custom "PR Link" field

When PR is merged:
- Set issue `Status` to "Done"
- Set `Completed Date` field

### Step 6: Generate Traceability Report

On-demand report showing issue→PR coverage:

```
PR-Issue Traceability Report
=============================
Sprint: Sprint 14

Issues with PRs: 12/15 (80%)
Issues without PRs: 3
  #130 — API v2 migration (no work started)
  #131 — Performance tests (assigned, no branch)
  #135 — Docs update (low priority)

PRs without issues: 2
  #201 — Dependency update (chore, no issue needed)
  #205 — Hotfix typo (trivial)

Merged PRs closing issues: 8
Open PRs: 4
```

## Error Handling

| Error | Action |
|-------|--------|
| PR has no issue references in branch, commits, or body | Skip linking; add comment to PR suggesting to add "Resolves #N" or use issue branch naming |
| Linked issue not found (deleted or wrong repo) | Log warning; do not update issue; optionally comment on PR about the invalid reference |
| GitHub API rate limit exceeded | Pause and retry with exponential backoff; report rate limit status to user |
| Cross-repo linking not supported | Document limitation; only link issues within the same repository as the PR |
| PR already linked to issue | Skip duplicate comment; update existing comment with latest PR status |

## Examples

### Example 1: Auto-link on PR creation
Trigger: New PR created with branch `issue/123-add-auth`
Actions:
1. Detect issue #123 from branch name
2. Verify issue exists and is open
3. Add PR-linked comment to issue
4. Update project board status
Result: Issue #123 shows linked PR with live status

### Example 2: Sprint coverage check
User says: "Check PR coverage for current sprint"
Actions:
1. List all issues in current sprint
2. Find linked PRs for each
3. Report coverage gaps
Result: Traceability report with coverage percentage
