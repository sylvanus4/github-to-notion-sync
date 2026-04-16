---
name: ship
description: >-
  End-to-end pre-merge pipeline that reviews code with 4 parallel agents,
  auto-fixes findings, verifies with linting, creates bisect-able domain-split
  commits, and opens a PR. Uses code-review-graph MCP blast radius to expand
  review scope and prioritize fixes by graph risk scores. Enforces the Iron
  Law of Verification and Review Readiness checks. Use when the user runs
  /ship, asks to "ship it", "prepare for merge", "create a PR with review",
  or "commit and PR". Do NOT use for review-only (use /simplify or
  /deep-review), manual commits (use /domain-commit), or PR management
  (use /pr-create, /pr-review). Korean triggers: "출시", "리뷰", "생성",
  "파이프라인".
metadata:
  author: "thaki"
  version: "2.0.0"
  category: "execution"
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

## Iron Law of Verification

**Never claim completion without fresh evidence.** Before creating commits or PRs, the pipeline MUST:

1. Run lint/typecheck on all modified files and confirm PASS
2. Run relevant tests (if test files exist for modified code) and confirm PASS
3. Verify no files are left in an inconsistent state (partial edits, broken imports)

If any verification fails, the pipeline STOPS and reports the failure. It does NOT proceed to commit or PR creation with known failures.

## Review Readiness Dashboard

Before Step 5 (commits), display a pre-flight checklist:

```
Review Readiness
================
[✓] All lint checks pass
[✓] No Critical findings remaining
[✓] All auto-fixes verified
[?] Tests pass (N/A if no test runner configured)
[✓] No TODO/FIXME introduced without issue link
[✓] No secrets or credentials detected
[✓] Commit messages follow convention
```

If any `[✗]` items exist, pause and ask user whether to proceed or fix first.

## Bisect-able Commit Strategy

Commits are structured so `git bisect` can identify regressions:

1. Each commit must leave the codebase in a compilable, lint-passing state
2. Feature code and its tests go in the same commit (not separate)
3. Refactoring commits are separated from behavior-changing commits
4. Database migrations get their own commit, before the code that depends on them

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

### Step 1.5: Graph-Aware Context (when code-review-graph MCP is available)

Before launching review agents, enrich context using the code-review-graph MCP server. If the server is unavailable, skip this step entirely.

1. **Blast radius expansion**: Call `get_impact_radius_tool` with the changed files. Add impacted files (callers, dependents, test gaps) NOT already in scope. This ensures reviewers catch files that WILL break from the changes being shipped.

2. **Structural context**: Call `get_review_context_tool` with the expanded file list. Pass token-optimized structural summaries (callers, callees, inheritance, test coverage) to each review agent — replaces full-file reads for context.

3. **Risk-scored prioritization**: Call `detect_changes_tool` to get risk scores. High-risk files (Critical/High) get higher adversarial scrutiny in Step 2 and are prioritized in Step 3 auto-fix.

Pass the expanded file list, structural context, and risk scores to review agents in Step 2.

### Step 2: Parallel Review (4 Agents)

Launch 4 sub-agents via the Task tool (same pattern as `/simplify`):

```
Agent 1: Refactor Agent        → Code structure, SOLID, duplication
Agent 2: Quality Agent         → Readability, naming, patterns
Agent 3: Tech Debt + Analyzer  → TODO/FIXME, root cause, structural issues
Agent 4: Performance Agent     → Efficiency, Big-O, redundant operations
```

Sub-agent config: `subagent_type: generalPurpose`, `model: fast`, `readonly: true`.

**Agent framing:** Inherit adversarial review posture — frame review as bug-hunting, not validation. Zero-issue files should be re-examined with deliberate skepticism before accepting as clean. If re-examination still yields zero issues, report honestly as clean — do not fabricate findings.

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

### Step 5: Review Readiness Check

Display the Review Readiness Dashboard (see above). Verify all items pass before proceeding. If any fail, pause for user decision.

### Step 6: Bisect-able Domain-Split Commits (skip if `--dry-run`)

Follow the `domain-commit` skill pattern with bisect-able ordering:
1. Analyze all changes (staged + unstaged)
2. Group files by domain (backend, frontend, config, docs, tests)
3. **Order commits for bisect-ability**: migrations first → backend → frontend → tests → config → docs
4. Ensure each commit leaves the codebase compilable (feature + its tests in same commit)
5. Separate refactoring commits from behavior-changing commits
6. Create one commit per domain with proper `[TYPE] Summary` format
7. Run pre-commit hooks; fix and re-commit on failure

### Step 7: Create PR (skip if `--no-pr` or `--dry-run`)

1. Determine current branch name
2. Push branch to origin: `git push origin HEAD:tmp`
3. Generate PR title from commits: `#ISSUE [TYPE] Summary`
4. Generate PR body with:
   - Summary of changes (from review findings)
   - Files changed with domain breakdown
   - Review results (findings fixed/skipped)
5. Create PR via `gh pr create` or GitHub MCP

**CRITICAL**: Never push to upstream. Only push to origin.

### Step 8: Report

```
Ship Report
===========
Pipeline: review → fix → verify → commit → PR

Review:
  Files reviewed: [N]
  Findings: [N] (Critical: X, High: X, Medium: X, Low: X)
  Fixed: [N] | Skipped: [N]

Review Readiness:
  [✓] Lint pass | [✓] No Critical remaining | [✓] Tests pass | [✓] No secrets

Commits (bisect-able order):
  1. [TYPE] commit message 1  (compilable: ✓)
  2. [TYPE] commit message 2  (compilable: ✓)

PR:
  URL: https://github.com/org/repo/pull/N
  Title: [PR title]
  Base: main ← [branch]

Iron Law Verification: ALL PASS
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

## Gotchas

### CRG-Enhanced Review Readiness

When CRG graph is available, add these items to the Review Readiness Dashboard:

```
[✓] Blast radius reviewed (N impacted files beyond direct changes)
[✓] No high-risk files skipped (all Critical/High risk files from detect_changes reviewed)
[✓] Test gap coverage (CRG-detected untested callers addressed)
```

If CRG is unavailable, these items show as `[—] N/A (CRG graph not available)` — never block shipping because CRG is missing.

### Commit Ordering with Migrations

Database migrations MUST be committed before application code that depends on them. The domain-split algorithm in Step 6 must detect `migrations/` or `*.sql` files and ensure they are in an earlier commit than the code that references new tables/columns. Violating this breaks `git bisect` — the migration commit works alone, but the code commit before migration fails.

### Push to tmp Branch

This project uses `git push origin HEAD:tmp` (not direct branch push). The ship skill MUST follow this convention. Common failure: `git push -u origin HEAD` will be rejected. If push fails with "rejected", check whether `tmp` branch has diverged and suggest `git pull origin tmp` first.

### Pre-commit Hook Timeouts

The project's pre-commit hooks can take >4 minutes when E2E tests are included. If the commit step hangs:
- Wait up to 5 minutes before considering it stuck
- If stuck, suggest `git push --no-verify` as a documented workaround (per learned workspace facts)
- Report the timeout in the shipping summary so the user is aware

### Evaluator-Optimizer Scope Creep

Step 4.5 (Quick Re-Evaluation) is intentionally limited to 1 iteration. Do NOT expand this into a full evaluator-optimizer loop — ship must stay fast. If Critical findings remain after 1 retry:
- Report them clearly with file paths and line numbers
- Pause for user decision: "1 Critical finding unresolved after auto-fix. Proceed to commit or fix manually?"
- Never silently ship with unresolved Critical findings

### Dry-Run Output Fidelity

When running with `--dry-run`, the findings report must be identical in format and content to what would be produced in a real run — including CRG blast radius data, risk scores, and domain-agent findings. The only difference is that Steps 5-7 (commit, push, PR) are skipped. Never reduce review depth in dry-run mode.

## Coordinator Synthesis

When delegating to subagents:

- **Never use lazy delegation.** Provide specific inputs (file paths, line numbers, exact changes, or concrete data points) to every subagent — not "based on your findings, do X."
- **Purpose statement required:** Every subagent prompt must state how its output is used downstream.
- **Continue vs Spawn decision:**
  - Continue (resume) when worker context overlaps with the next task or fixing a previous failure
  - Spawn fresh when verifying another worker's output or when previous approach was fundamentally wrong
- Use `model: "fast"` for exploration/read-only subagents; default model for generation/analysis

## Honest Reporting

- Report review outcomes faithfully: if a check fails, say so with the relevant output
- Never claim "all checks pass" when output shows failures
- Never suppress or simplify failing checks to manufacture a green result
- When a check passes, state it plainly without unnecessary hedging
- The final report must accurately reflect what was found — not what was hoped

## Subagent Contract

Subagent prompts must include:
- Always use absolute file paths (subagent cwd may differ)
- Share file paths relevant to the task in the final response
- Include code snippets only when the exact text is load-bearing (a bug found, a signature needed)
- Do not recap code merely read — summarize what was learned
- Final response: concise report of what was done, key findings, and files changed
- Do not use emojis
