---
name: ship
description: >-
  End-to-end pre-merge pipeline that reviews code with 4 parallel agents,
  auto-fixes findings, verifies with linting, creates domain-split commits,
  and opens a PR. Use when the user runs /ship, asks to "ship it", "prepare
  for merge", "create a PR with review", or "commit and PR". Do NOT use for
  review-only (use /simplify or /deep-review), manual commits (use
  /domain-commit), or PR management (use /pr-create, /pr-review).
metadata:
  author: thaki
  version: 1.0.0
---

# Ship — Pre-Merge Pipeline

One command to go from "code is done" to "PR is ready". Runs parallel code review, auto-fixes issues, creates domain-split commits, and opens a PR.

## Usage

```
/ship                           # full pipeline: review → fix → commit → PR
/ship --no-pr                   # review → fix → commit (skip PR creation)
/ship --dry-run                 # review only, show what would happen
/ship --base main               # specify PR base branch (default: main)
/ship --no-fix                  # review → commit → PR (skip auto-fix)
```

Arguments can be combined: `/ship --base dev --no-fix`.

## Workflow

For detailed step configuration, see [references/pipeline-steps.md](references/pipeline-steps.md).

### Step 1: Identify Changed Files

```bash
git diff --name-only
git diff --cached --name-only
git diff HEAD --name-only
```

If no changes, fall back to `git diff HEAD~1 HEAD --name-only`.
If still empty, inform the user and stop.

### Step 2: Parallel Review (4 Agents)

Launch 4 sub-agents via the Task tool (same pattern as `/simplify`):

```
Agent 1: Refactor Agent        → Code structure, SOLID, duplication
Agent 2: Quality Agent         → Readability, naming, patterns
Agent 3: Tech Debt + Analyzer  → TODO/FIXME, root cause, structural issues
Agent 4: Performance Agent     → Efficiency, Big-O, redundant operations
```

Sub-agent config: `subagent_type: generalPurpose`, `model: fast`, `readonly: true`.

### Step 3: Auto-Fix (skip if `--no-fix` or `--dry-run`)

1. Aggregate and deduplicate findings
2. Sort by severity: Critical > High > Medium > Low
3. Apply fixes via StrReplace (highest severity first)
4. Track applied vs skipped fixes

### Step 4: Verify

1. Run `ReadLints` on all modified files
2. Fix any lint errors introduced
3. If `--dry-run`, present findings report and stop here

### Step 4.5: Quick Re-Evaluation (Evaluator-Optimizer)

**Pattern:** Lightweight evaluator-optimizer — verify that Critical/High findings from Step 2 are resolved after auto-fix.

1. Collect the list of original Critical and High findings from Step 2
2. If no Critical/High findings existed, skip this step
3. Launch 1 fast re-check agent on ONLY the files that were modified in Step 3
   - `subagent_type`: `generalPurpose`, `model`: `fast`, `readonly`: `true`
   - Prompt: "Verify these specific Critical/High findings are resolved: [list findings]. Review only the modified files."
4. If unresolved Critical findings remain:
   - Attempt one more fix pass on the unresolved Critical findings only
   - Run `ReadLints` again
   - If still unresolved after 1 retry, report the remaining Critical findings and pause for user decision
5. If only unresolved High findings remain: note them in the report but proceed

**Max iterations:** 1 (ship should stay fast — full refinement is for `/simplify --refine` or `/deep-review --refine`)

### Step 5: Domain-Split Commits (skip if `--dry-run`)

Follow the `domain-commit` skill pattern:
1. Analyze all changes (staged + unstaged)
2. Group files by domain (backend, frontend, config, docs, tests)
3. Create one commit per domain with proper `[TYPE] Summary` format
4. Run pre-commit hooks; fix and re-commit on failure

### Step 6: Create PR (skip if `--no-pr` or `--dry-run`)

1. Determine current branch name
2. Push branch to origin: `git push origin HEAD:tmp`
3. Generate PR title from commits: `#ISSUE [TYPE] Summary`
4. Generate PR body with:
   - Summary of changes (from review findings)
   - Files changed with domain breakdown
   - Review results (findings fixed/skipped)
5. Create PR via `gh pr create` or GitHub MCP

**CRITICAL**: Never push to upstream. Only push to origin.

### Step 7: Report

```
Ship Report
===========
Pipeline: review → fix → commit → PR

Review:
  Files reviewed: [N]
  Findings: [N] (Critical: X, High: X, Medium: X, Low: X)
  Fixed: [N] | Skipped: [N]

Commits:
  [TYPE] commit message 1
  [TYPE] commit message 2

PR:
  URL: https://github.com/org/repo/pull/N
  Title: [PR title]
  Base: main ← [branch]

Verification: lint PASS
```

## Examples

### Example 1: Full pipeline

User runs `/ship` after completing a feature.

Actions:
1. `git diff HEAD` finds 7 changed files
2. 4 review agents run in parallel
3. Findings: 1 High (duplicated logic), 3 Medium (naming, TODO, unused import)
4. Apply 4/4 fixes
5. Lint passes
6. 2 domain commits: `[feat] Add user profile API`, `[feat] Add profile UI components`
7. PR created with review summary
8. Report with PR URL

### Example 2: Dry-run preview

User runs `/ship --dry-run` to see what review would find.

Actions:
1. Find 5 changed files
2. 4 agents review in parallel
3. Findings: 2 High, 4 Medium
4. Present findings report — no fixes applied, no commits, no PR

### Example 3: Commit without PR

User runs `/ship --no-pr` to review, fix, and commit without creating a PR.

Actions:
1. Review + fix + verify
2. Create domain-split commits
3. Report without PR section

## Error Handling

| Scenario | Action |
|----------|--------|
| No changes detected | Inform user and stop |
| Sub-agent timeout | Re-launch once; if still fails, continue with partial results |
| Pre-commit hook fails | Fix lint errors and re-commit; if unfixable, report and stop |
| Push fails | Report error; user may need to set upstream or authenticate |
| PR creation fails | Report error with commit hashes; user can create PR manually |
| Branch already has open PR | Report existing PR URL instead of creating a new one |

## Troubleshooting

- **"No changes found"**: Ensure there are uncommitted changes or recent commits
- **"Push rejected"**: Check if the remote `tmp` branch is ahead; may need `git pull origin tmp`
- **"PR already exists"**: The skill detects existing PRs and reports their URL
- **Unwanted fixes**: Use `--no-fix` to skip auto-fix, or `--dry-run` to preview first
