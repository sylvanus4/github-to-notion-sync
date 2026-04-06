---
name: release-ship
description: >-
  Lightweight shipping pipeline: domain-split commits, git push, and PR
  creation/update in one flow. Use when the user asks to "release-ship", "commit
  and push", "commit and PR", "push and create PR", "커밋하고 PR", "커밋하고 푸시", "ship
  without review", or wants to go from uncommitted changes to an open PR without
  code review. Do NOT use for review-included shipping (use ship), full release
  validation pipeline (use release-commander), domain-split commits only without
  push/PR (use domain-commit), or single-file trivial commits.
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# Release Ship — Commit, Push, Issue, PR, and Merge Pipeline

Lightweight pipeline to go from uncommitted changes to a merged PR. Chains domain-split commits, push, issue creation with project linking, PR creation, and auto-merge without code review overhead.

## Repository-Specific Behavior

### ai-platform-webui (ThakiCloud/ai-platform-webui)

**Exception**: This repo works exclusively on the `tmp` branch. PR creation and merge steps are **always skipped**. The pipeline is:

```
commit → push → issue → report
```

No cross-branch merges. No PRs targeting `dev` or `main`. All work stays on `tmp`.

### Other repos

Full pipeline applies: `commit → push → issue → PR → merge`.

## Usage

```
/release-ship                    # full pipeline (webui: commit→push→issue→report)
/release-ship --no-pr            # commit → push → issue (skip PR and merge)
/release-ship --no-issue         # commit → push → PR → merge (skip issue creation)
/release-ship --no-merge         # commit → push → issue → PR (skip merge)
/release-ship --base dev         # specify PR base branch (default: auto-detect)
/release-ship --update           # force-update existing PR body
```

## Workflow

### Step 1: Pre-flight

```bash
git status --short
git branch --show-current
git log --oneline -5
```

1. If working directory is clean, stop and inform the user.
2. Extract the current branch name.
3. Extract issue number from branch: `issue/{NUMBER}-*` or `epic/{NUMBER}`.
4. Check for existing PRs: `gh pr list --head tmp --json number,url --jq '.[0]'`.

### Step 2: Domain-Split Commits

Follow the `domain-commit` skill pattern. For domain-to-path mapping and hook remediation, see [domain-commit references](../domain-commit/references/hooks-and-domains.md).

1. Categorize **all** files (both modified `M` and untracked `??`) by domain prefix into commit batches.
2. **Critical**: Never silently skip untracked content files. Files in `output/`, `docs/`, `ai-platform/`, `scripts/`, `tasks/` etc. must be included. Unmapped paths go to the catch-all `chore:` batch.
3. For each batch:
   - `git add <files>`
   - Commit with `TYPE: Summary` format (Conventional Commits, HEREDOC).
   - If pre-commit fails: unstage, fix, re-stage, create new commit.
   - If pre-commit auto-fixes files: re-add and create new commit.
4. Verify: `git status --short` must be empty. If any content files remain, commit them as `chore: Add remaining files`.

### Step 2.5: Pre-Push Quality Gate

Before `git push origin HEAD:tmp`, verify:
- [ ] All pre-commit hooks passed (no bypassed commits via `--no-verify`)
- [ ] `git status --short` is empty (all changes committed)
- [ ] All commit messages follow `TYPE: Summary` format — Conventional Commits (check via `git log --oneline -N`)
- [ ] No sensitive files staged (`.env`, `credentials`, `secrets`, `*.key`, `*.pem`)
- [ ] Total diff is reviewable (`git diff --stat HEAD~N` shows < 500 lines, or split plan exists)

If diff exceeds 500 lines, warn the user and suggest splitting into sequential domain-commit batches with intermediate pushes.

### Step 3: Push

```bash
git push origin HEAD:tmp
```

If push fails (e.g., rejected), inform the user with remediation steps (`git pull origin tmp`).

**Repo detection** (used in Steps 5 and 6):

```bash
REPO_URL=$(git remote get-url origin)
IS_WEBUI=false
echo "$REPO_URL" | grep -q 'ai-platform-webui' && IS_WEBUI=true
```

If `IS_WEBUI` is true, skip Steps 5 and 6 entirely (proceed to Step 4, then Step 7).

If both `--no-pr` and `--no-issue` flags are set, skip to Step 7 (Report).

### Step 4: Create Issues and Link to Project

If `--no-issue` flag is set, skip to Step 5 (PR).

This step converts the domain-split commits from Step 2 into tracked GitHub issues on ThakiCloud Project #5. It follows patterns from the [commit-to-issue](../commit-to-issue/SKILL.md) skill. For project field IDs, option IDs, and GraphQL queries, see [commit-to-issue/references/project-config.md](../commit-to-issue/references/project-config.md).

#### 4a. Analyze commits from Step 2

Collect only the commits created in Step 2 (not all branch history):

```bash
git log --oneline -N  # where N = number of commits created in Step 2
```

Each domain-split commit maps 1:1 to one issue.

#### 4b. Create issues

For each commit:

```bash
ISSUE_URL=$(gh issue create \
  --repo OWNER/REPO \
  --title "TYPE: Summary from commit" \
  --assignee sylvanus4 \
  --body "$(cat <<'EOF'
## Description
<Derived from commit message and changed files>

## Commits
- `<hash>` <commit message>

## Files Changed
- file1
- file2
EOF
)")
```

Collect all created issue URLs and numbers for Step 5 (PR body).

#### 4c. Add issues to Project #5 and set ALL fields (MANDATORY)

For each created issue:

```bash
gh project item-add 5 --owner ThakiCloud --url $ISSUE_URL
```

Then set ALL 5 project fields using the `set_all_fields()` Python script from [commit-to-issue/references/project-config.md](../commit-to-issue/references/project-config.md). This step is NOT optional.

**Procedure:**

1. Query current sprint iteration ID via date-based selection (sprint IDs rotate weekly — never hardcode)
2. For each issue: query project item ID, count changed files, then call `set_all_fields(item_id, sprint_id, label=label, file_count=N)`
3. Verify all fields were set successfully

**Default field values (auto-determined by file count):**

| Field | Default | Override When |
|-------|---------|--------------|
| Assignee | `sylvanus4` | Never override |
| Status | Done (`98236657`) | Use In Progress for WIP |
| Priority | P2 (`473ded73`) | P1 for critical, P0 for urgent |
| Size | Auto by file count | Override with explicit size_id |
| Sprint | Current (query by date) | Never override |
| Estimate | Auto by file count | Override with explicit value |

**CRITICAL**: Do NOT skip this step. Do NOT set only Status. ALL 5 fields are required for every issue. If a field set fails, retry once before reporting partial failure.

#### 4d. Verify issues and PR on Project #5

After all issues are created and fields set, verify they appear correctly on GitHub Project #5:

```bash
gh project item-list 5 --owner ThakiCloud --format json --limit 50
```

For each issue created in Step 4b, verify:
1. Issue appears in Project #5 item list
2. All 5 fields (Status, Priority, Size, Sprint, Estimate) have non-null values

If any issue is missing from Project #5 or has incomplete fields, retry `item-add` and `set_all_fields()` once before recording failure.

Record verification result: `{project5_check: {issues_verified: N, issues_total: M, missing_issues: [...], fields_incomplete: [...]}}`.

### Step 5: PR Create or Update

**Skip this step** if `IS_WEBUI` is true (ai-platform-webui works on `tmp` only — no PRs).

Determine target branch (override with `--base`):

| Branch pattern | Target |
|----------------|--------|
| `issue/*` | `dev` |
| `epic/*` | `dev` |
| `release-*` | `main` |
| other | `dev` |

If `--no-pr` flag is set, skip to Step 7 (Report).

For PR body and title format, see [references/pr-template.md](references/pr-template.md).

#### 5a. If PR already exists

```bash
PR_NUMBER=$(gh pr list --head tmp --json number --jq '.[0].number')
```

Update the PR body with current changes. For the PR body template, see [references/pr-template.md](references/pr-template.md).

#### 5b. If no PR exists

Create a new PR. Title format: `#<ISSUE_NUMBER> TYPE: Summary` (English).

If issues were created in Step 4, populate the `## Issue?` section with `Resolves #N1, Resolves #N2, ...` so they auto-close on merge.

```bash
gh pr create \
  --title "#${ISSUE_NUMBER} TYPE: Summary" \
  --body "$(cat <<'EOF'
## Issue?
Resolves #N1, Resolves #N2

## Changes?
- Change description 1
- Change description 2

## Why we need?
Brief explanation

## Test?
- [ ] Test item 1

## CC (Optional)

## Anything else? (Optional)
EOF
)" \
  --base $TARGET_BRANCH \
  --head tmp \
  --assignee sylvanus4
```

For the full PR body template, see [references/pr-template.md](references/pr-template.md).

### Step 6: Merge PR (Auto-Merge by Default)

**Skip this step** if `IS_WEBUI` is true (ai-platform-webui works on `tmp` only — no merges).

If `--no-pr` or `--no-merge` flag is set, skip to Step 7 (Report).

Auto-merge the PR created or updated in Step 5. This is the DEFAULT behavior — do NOT ask the user whether to merge. Just merge it.

```bash
gh pr merge $PR_NUMBER --squash --delete-branch
```

If merge fails due to CI or review requirements, try admin merge:

```bash
gh pr merge $PR_NUMBER --squash --delete-branch --admin
```

If admin merge also fails, report the error with the PR URL. Do NOT block the Report step.

#### 6a. Add PR to Project #5

After PR is created (Step 5) or before merge, add the PR to Project #5:

```bash
gh project item-add 5 --owner ThakiCloud --url $PR_URL
```

Verify the PR appears in Project #5 item list. Record: `{pr_on_project5: true/false}`.

If `item-add` fails, retry once. Non-blocking — continue to merge even if Project #5 linking fails.

#### 6b. Switch to base branch after merge

After a successful merge, pull the updated base branch and switch to it:

```bash
git checkout $TARGET_BRANCH
git pull origin $TARGET_BRANCH
```

If the checkout or pull fails (e.g., uncommitted changes), warn the user but do not block the Report step.

### Step 7: Report

**ai-platform-webui** format (no PR/Merge):

```
Release Ship Report
====================
Pipeline: commit → push → issue → report (webui: tmp-only mode)

Commits:
  TYPE: commit message 1
  TYPE: commit message 2

Push:
  Branch: tmp → origin/tmp

Issues:
  #N1 TYPE: Title → Project #5 (Done, P2, S, Sprint X)
  #N2 TYPE: Title → Project #5 (Done, P2, S, Sprint X)

GitHub Project #5 검증:
  이슈 등록: N/N 확인 ✅ (or ⚠️ M개 누락)
  필드 완성도: N/N 완전 ✅ (or ⚠️ M개 불완전)
```

**Other repos** format (full pipeline):

```
Release Ship Report
====================
Pipeline: commit → push → issue → PR → merge

Commits:
  TYPE: commit message 1
  TYPE: commit message 2

Push:
  Branch: [branch] → origin/tmp

Issues:
  #N1 TYPE: Title → Project #5 (Done, P2, S, Sprint X)
  #N2 TYPE: Title → Project #5 (Done, P2, S, Sprint X)

PR:
  URL: https://github.com/ThakiCloud/REPO/pull/N
  Title: [PR title]
  Base: [target] ← [branch]
  Status: [Created | Updated]

Merge:
  PR #N merged via squash into [base branch]
  Branch: deleted
```

If `--no-issue` was used, omit the Issues section. If `--no-pr` was used, omit the PR and Merge sections. If `--no-merge` was used, omit the Merge section.

## Examples

### Example 1: ai-platform-webui (tmp-only mode)

User runs `/release-ship` on `tmp` in `ai-platform-webui`.

1. `git status` finds 6 changed files across `.cursor/skills/`, `.cursor/commands/`, `docs/`
2. 3 domain-split commits created
3. Push to `origin/tmp`
4. Create 3 issues from commits → add to Project #5 with fields (Done, P2, S, current sprint, 0.5 SP each)
5. PR and merge skipped (webui: tmp-only mode)
6. Report with commit list, issue URLs — no PR/merge sections

### Example 2: Full pipeline from other repo

User runs `/release-ship` in `ai-template`.

1. Domain-split commits created
2. Push to origin
3. Issues created and added to Project #5
4. PR created targeting `main`
5. Squash-merge PR into `main`, source branch deleted
6. Report with merge status

### Example 3: Push without PR

User runs `/release-ship --no-pr` to commit and push only.

1. Domain-split commits created
2. Push to origin
3. Issues created and added to Project #5
4. Report without PR and Merge sections

### Example 4: Existing PR update (non-webui repos)

User runs `/release-ship` on a branch that already has an open PR.

1. Domain-split commits for new changes
2. Push to origin
3. Issues created from new commits and added to Project #5
4. Existing PR #15 detected → update PR body with new changes and issue references
5. Squash-merge PR
6. Report shows "Status: Updated"

### Example 5: Skip issue creation

User runs `/release-ship --no-issue` to ship without creating issues.

1. Domain-split commits created
2. Push to origin
3. Issue creation skipped
4. PR created without issue references
5. Squash-merge PR
6. Report without Issues section

## Error Handling

| Scenario | Action |
|----------|--------|
| No changes detected | Inform user and stop |
| Pre-commit hook fails | Fix lint errors, re-commit (never amend) |
| Push rejected | Report error; suggest `git pull origin tmp` |
| Issue creation fails (permission) | Report error; continue with PR creation |
| Project item-add fails | Report error; continue with PR creation |
| Sprint field outdated | Re-query current sprint iteration via GraphQL |
| PR creation fails | Report error with commit hashes; user can create manually |
| Branch already has PR | Update existing PR body instead of creating duplicate |
| No issue number in branch | Create PR without issue reference in title |
| Merge fails (CI required) | Report error with PR URL; user can merge manually |
| Merge fails (review required) | Report error; suggest `gh pr review --approve` |
| Merge fails (conflicts) | Report error; suggest resolving conflicts |
| `gh` CLI not authenticated | Report error; suggest `gh auth login` |

## Safety Rules

- **Never force push** (`--force`) to any branch
- **Never push directly** to `main` or `dev`
- **Never amend** failed commits; create new ones
- **Never commit** `.env`, credentials, or secret files
- **Only push to origin**, never upstream
- **Standalone mode**: Show issue plan and confirm with user before creating issues
- **Pipeline mode** (invoked by eod-ship, sod-ship, morning-ship, or any batch pipeline): Auto-confirm issue creation — do NOT skip this step. The pipeline caller has already been approved by the user.
- **Reference local guides**: [commit-to-issue/references/](../commit-to-issue/references/) for issue config, [references/pr-template.md](references/pr-template.md) for PR format
- **Never merge** without a successfully created PR in the same pipeline run
- **ai-platform-webui**: Never create PRs or merge to other branches — `tmp` is the only working branch
- **ai-platform-webui**: Never delete `tmp` branch (it is reused permanently)
