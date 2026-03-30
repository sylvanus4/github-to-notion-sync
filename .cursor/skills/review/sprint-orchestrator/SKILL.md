---
name: sprint-orchestrator
description: >-
  Auto-triage incoming GitHub issues and PRs: classify by type, assign priority
  (P0-P3), suggest assignees from CODEOWNERS/git blame, update GitHub Project
  fields, and generate per-user digests. Use when the user asks to "triage
  issues", "auto-assign sprint items", "sprint orchestrator", "스프린트 관리",
  "이슈 자동 분류", "sprint-orchestrator", or wants overnight issue/PR triage
  and assignment. Do NOT use for creating issues from commits (use
  commit-to-issue), daily GitHub activity digests only (use
  github-sprint-digest), or manual sprint planning (use agency-sprint-prioritizer).
metadata:
  version: "1.0.0"
  category: "execution"
  author: "thaki"
---
# Sprint Orchestrator

Automated sprint triage: classify, prioritize, assign, and organize incoming issues and PRs overnight so the team starts each day with a clean, prioritized backlog.

## When to Use

- As part of the morning pipeline (after `sod-ship`, before sprint digest)
- When a batch of new issues/PRs needs triage
- At sprint boundaries to organize the incoming backlog

## Workflow

### Step 1: Fetch New Items

Query GitHub for untriaged items since last run:

```bash
gh issue list --repo <repo> --state open --label "" --json number,title,body,labels,createdAt,author
gh pr list --repo <repo> --state open --json number,title,body,labels,createdAt,author,reviewRequests
```

Filter to items created since last triage timestamp (stored in `.sprint-orchestrator-state.json`).

### Step 2: Classify Each Item

For each issue/PR, use LLM classification:

| Type | Criteria |
|------|----------|
| `bug` | Error reports, regression, "doesn't work", stack traces |
| `feature` | New functionality, user stories, "as a user I want" |
| `enhancement` | Improvements to existing features, UX tweaks |
| `chore` | Dependencies, CI/CD, documentation, refactoring |
| `security` | Vulnerability reports, CVEs, access control |

Apply the classified label via GitHub API.

### Step 3: Assign Priority

Score priority based on:
- **P0 (Critical)**: Production down, security vulnerability, data loss risk
- **P1 (High)**: User-facing bug, blocker for current sprint, regression
- **P2 (Medium)**: Feature request aligned with sprint goal, enhancement
- **P3 (Low)**: Nice-to-have, tech debt, cosmetic issues

Factors: label keywords, author (team member vs external), linked milestone, mentioned components.

Update GitHub Project `Priority` field.

### Step 4: Suggest Assignee

Determine the best assignee using:

1. **CODEOWNERS**: Match changed files (for PRs) against CODEOWNERS rules
2. **Git blame**: Most recent contributors to affected files
3. **Workload balance**: Current assignee counts from GitHub Projects
4. **Expertise**: Past issue/PR history on similar topics

For PRs, also add appropriate reviewers.

### Step 5: Update GitHub Project Fields

For each triaged item, update via GraphQL:

```
- Status: "Triage" → "Ready" (or "In Progress" if auto-assigned)
- Priority: P0-P3
- Size: XS/S/M/L/XL (estimated from complexity)
- Sprint: Current sprint (if priority <= P1)
- Estimate: Story points (1/2/3/5/8)
```

### Step 6: Generate Triage Summary

Post a summary to Slack:

```
Sprint Triage Summary
=====================
Period: <last-run> → <now>
New Items: <count>

P0 (Critical): 1
  #201 — Production API timeout on /users endpoint → @backend-dev

P1 (High): 3
  #198 — Login fails after password reset → @auth-dev
  #199 — Dashboard chart data missing → @frontend-dev
  #200 — Dependency CVE in jsonwebtoken → @security-dev

P2 (Medium): 5
  [list...]

P3 (Low): 2
  [list...]

Unassigned (needs manual review): 0
```

### Step 7: Persist State

Save triage timestamp and item IDs to state file for deduplication on next run.

## Integration Points

- **Morning pipeline**: Runs after `sod-ship`, before `github-sprint-digest`
- **feedback-meeting-scheduler**: Feeds blocked/stale items for meeting proposals
- **standup-digest**: Provides per-person assignment data

## Error Handling

| Error | Action |
|-------|--------|
| GitHub MCP auth failure | Prompt user to run `gh auth login` or verify `GITHUB_TOKEN`; skip triage and report auth status |
| No open issues/PRs found | Post empty summary to Slack with "No new items to triage"; persist state and exit normally |
| Project board not configured | Log warning, skip Step 5 (Project field updates); complete classification and post summary without Project sync |
| Label creation fails | Retry with existing labels; if label missing, add to manual-review list and note in summary |
| Assignee not in org | Omit assignee suggestion for that item; add to "Unassigned (needs manual review)" in summary |

## Examples

### Example 1: Morning triage
User says: "Triage overnight issues"
Actions:
1. Fetch new issues/PRs since yesterday
2. Classify, prioritize, and suggest assignees
3. Update GitHub Project fields
4. Post summary to Slack
Result: All new items triaged with priority and assignee suggestions

### Example 2: Sprint start triage
User says: "Organize backlog for new sprint"
Actions:
1. Fetch all open untriaged items
2. Full classification and prioritization
3. Assign to current sprint based on priority and capacity
Result: Sprint-ready backlog with estimated story points
