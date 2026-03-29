---
name: commit-to-issue
description: >-
  Analyze recent git commits and create GitHub issues with project field setup
  on ThakiCloud project boards. Use when the user asks to "create issues from
  commits", "track commits as issues", "register work to project", "sync commits
  to GitHub project", or "turn commits into issues". Do NOT use for committing
  local changes (use domain-commit), PR creation or review (use
  pr-review-captain), or CI pipeline validation (use ci-quality-gate). Korean
  triggers: "커밋", "리뷰", "분석", "생성".
metadata:
  version: "1.0.0"
  category: "execution"
  author: "thaki"
---
# Commit-to-Issue

Turns git commit history into tracked GitHub issues with full project board integration. Analyzes commits, groups them into logical issue batches, creates issues with structured bodies, adds them to a ThakiCloud project, and configures all project fields (Status, Priority, Size, Sprint, Estimate).

## Prerequisites

- `gh` CLI authenticated with access to the target repository and ThakiCloud org
- For issue templates, see [references/issue-templates.md](references/issue-templates.md)
- For project field IDs and GraphQL, see [references/project-config.md](references/project-config.md)
- For Epic/sub-issue management, see [references/epic-sub-issues.md](references/epic-sub-issues.md)

## Workflow

### Step 1: Gather commit context

Identify the commits to convert into issues. Support three modes:

- **Date range**: `git log --since="YYYY-MM-DD" --until="YYYY-MM-DD" --format="%h %ai %s" --all`
- **Last N commits**: `git log --oneline -N`
- **Branch diff**: `git log --oneline main..HEAD`

Also run `git remote -v` to extract the repo owner and name (e.g., `sylvanus4/call-center-tts`).

### Step 2: Analyze and group commits

Read each commit's changed files with `git show --stat <hash>`. Group related commits into logical issue batches by module or domain. Each batch becomes one issue.

Determine for each issue:
- **Title**: `[TYPE] Summary` per CONTRIBUTING.md convention
- **Body**: Use the issue body template from [references/issue-templates.md](references/issue-templates.md)
- **Estimate**: Story points as specified by the user (default 0.5)

### Step 3: Confirm with user

Present the issue plan as a table before creating:

```
| # | Title | Files | Estimate |
|---|-------|-------|----------|
```

Wait for user approval. Adjust grouping or estimates if requested.

### Step 4: Create issues

For each issue batch:

```bash
gh issue create --repo OWNER/REPO --title "[TYPE] Title" --assignee @me --body "$(cat <<'EOF'
...issue body...
EOF
)"
```

Collect all issue URLs and numbers.

### Step 5: Add to project and set fields

Add each issue to the target project and configure fields. For project field IDs, option IDs, and GraphQL queries, see [references/project-config.md](references/project-config.md).

1. `gh project item-add PROJECT_NUM --owner ORG --url ISSUE_URL`
2. Query project for item IDs via GraphQL
3. Set fields: Status, Priority, Size, Sprint, Estimate

### Step 6: Report

Output a summary table with all created issues, project field settings, and URLs.

## Output Format

```
GitHub Issue Tracking Report
=============================
Repository: [owner/repo]
Project: [org] #[number]
Issues created: [N]
Total estimate: [X.X] SP

| # | Title | Estimate | Sprint | URL |
|---|-------|----------|--------|-----|

Project Fields (all issues):
  Status: [value]
  Priority: [value]
  Size: [value]
  Sprint: [value]
```

## Examples

### Example 1: Track yesterday's commits as issues
User says: "Create issues from yesterday's commits on project #5"
Actions:
1. Run `git log --since` for yesterday's date range
2. Analyze 5 commits across 3 modules (data, training, serving)
3. Group into 3 issues by module, present plan for approval
4. Create 3 issues with structured bodies via `gh issue create`
5. Add to ThakiCloud project #5 and set Status/Priority/Size/Sprint/Estimate
Result: 3 issues created with full project field configuration, summary table shown

### Example 2: Commit then track
User says: "Commit my changes and register them as issues"
Actions:
1. Invoke domain-commit skill to create domain-split commits
2. Analyze the new commits and group into issue batches
3. Create issues from the commits and add to project
Result: Clean commits + tracked issues on the project board

### Example 3: Track a feature branch
User says: "Turn this branch's commits into issues for project #5"
Actions:
1. Run `git log main..HEAD` to get branch-only commits
2. Group commits by domain into issue batches
3. Create issues and add to project with field setup
Result: All branch work tracked as project issues

## Troubleshooting

### Issue creation fails with permission error
Cause: `gh` CLI not authenticated or lacks repo write access
Solution: Run `gh auth status` to verify, then `gh auth login` if needed

### Project item-add fails for cross-org repo
Cause: The repo is outside the ThakiCloud org but the project is org-scoped
Solution: Cross-repo items are supported in GitHub Projects V2. Verify `gh` has org access with `gh api orgs/ThakiCloud`

### Sprint field not setting correctly
Cause: The iteration ID is outdated (sprints rotate weekly)
Solution: Re-query the project fields to get the current sprint iteration ID. See [references/project-config.md](references/project-config.md) for the query.

## Safety Rules

- **Never push to upstream** unless the user explicitly requests it
- **Standalone mode**: Show issue plan and confirm with user before creating issues
- **Pipeline mode** (invoked by release-ship, eod-ship, or any batch pipeline): Auto-confirm issue creation — the pipeline caller has already been approved by the user
- **Always set assignee** to `@me`
- **Reference local guides** in the `references/` directory for issue templates, project config, and Epic patterns
