---
name: simplify
description: >-
  Run parallel code review agents to analyze code for reuse opportunities, code
  quality, tech debt, and performance issues, then auto-fix findings by
  priority. Supports 3 scoping modes: diff (changed files), today (daily work),
  and full (entire project). Use when the user runs /simplify, asks to "simplify
  code", "review and fix changes", "clean up my code", or "review today's work".
  Do NOT use for single-domain review (use /refactor, /performance, etc.
  individually), creating new features, or general Q&A. Korean triggers: "리뷰",
  "분석", "수정", "성능".
metadata:
  author: "thaki"
  version: "2.0.0"
  category: "execution"
---
# Simplify — Parallel Code Review & Auto-Fix

Analyze code through 4 parallel review agents, aggregate findings, and auto-fix issues by priority. Supports 3 scoping modes: changed files, daily work, or full project.

## Scoping Modes

Determine the scope from the user's input:

| Mode | Trigger | Scope |
|------|---------|-------|
| `diff` (default) | `/simplify` or `/simplify diff` | Git diff (unstaged + staged + HEAD) |
| `today` | `/simplify today` | All files changed today (`--since=midnight`) |
| `full` | `/simplify full` or `/simplify project` | All source files in the project |

Mode keywords can be combined with other arguments: `/simplify today focus on performance`.

## Workflow

### Step 1: Identify Target Files

Resolve files based on the scoping mode:

**Mode: diff (default)**
```bash
git diff --name-only          # unstaged
git diff --cached --name-only # staged
git diff HEAD --name-only     # combined
```
If no changes found, fall back to `git diff HEAD~1 HEAD --name-only`.
If still empty, inform the user and stop.

**Mode: today**
```bash
git log --since=midnight --name-only --pretty=format: | sort -u
```
Shows all files touched in today's commits plus current uncommitted changes.
Combine with `git diff --name-only` for uncommitted work.

**Mode: full**
```bash
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.java" -o -name "*.swift" -o -name "*.kt" \) \
  -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/dist/*" -not -path "*/build/*" -not -path "*/__pycache__/*" -not -path "*/vendor/*"
```
For large projects (50+ files), split into batches of ~20 files per agent round.
Warn the user if over 100 files: "Full project scan covers N files. This may take several minutes. Proceed?"

If a specific directory is provided (e.g., `/simplify src/api/`), scope to that directory regardless of mode.

Read each target file to build the review context.

### Step 2: Launch 4 Parallel Review Agents

Use the Task tool to spawn 4 sub-agents simultaneously. Each agent receives the list of changed files and their contents.

For detailed prompt templates, see [references/agent-prompts.md](references/agent-prompts.md).

```
Agent 1: Refactor Agent        → Code structure, SOLID, duplication
Agent 2: Quality Agent         → Readability, naming, patterns, security
Agent 3: Tech Debt + Analyzer  → TODO/FIXME, root cause, structural issues
Agent 4: Performance Agent     → Efficiency, Big-O, redundant operations
```

Sub-agent configuration:
- `subagent_type`: `generalPurpose`
- `model`: `fast` (read-only analysis; keeps cost low and speed high)
- `readonly`: `true`

Each agent must return findings in this structure:

```
CATEGORY: [agent category]
FINDINGS:
- severity: [Critical|High|Medium|Low]
  file: [path]
  line: [number or range]
  issue: [description]
  fix: [suggested change]
```

### Step 3: Aggregate Findings

Collect all agent outputs and merge into a single findings list.

### Step 4: Deduplicate and Prioritize

1. Remove duplicate findings (same file + same line + similar issue)
2. Sort by severity: Critical > High > Medium > Low
3. Within same severity, group by file for efficient fixing

### Step 5: Apply Fixes

For each finding (highest severity first):

1. Read the target file
2. Apply the suggested fix using StrReplace
3. Track applied vs skipped fixes

Skip a fix if:
- The fix would conflict with a previously applied fix
- The suggested change is ambiguous or risky
- The file has been modified by a prior fix in a way that invalidates the line reference

### Step 6: Verify

1. Run `ReadLints` on all modified files to catch regressions
2. Fix any lint errors introduced by the changes

### Step 7: Re-Evaluate (Evaluator-Optimizer Loop)

**Trigger:** Runs automatically when `--refine` flag is set. Skipped by default.

**Pattern:** Evaluator-Optimizer — re-run focused review agents on modified files to verify fixes resolved the original findings and did not introduce new issues.

1. Collect the list of files modified in Step 5
2. Launch 1-2 focused review agents (pick the 2 most relevant from Step 2) on ONLY the modified files
   - `subagent_type`: `generalPurpose`, `model`: `fast`, `readonly`: `true`
   - Prompt: "Review these files for remaining issues. Focus on verifying that prior Critical/High findings are resolved."
3. Compare re-evaluation findings against the original findings list
4. If new Critical or High findings exist AND iteration count < 2:
   - Apply fixes for the new findings (same rules as Step 5)
   - Increment iteration counter
   - Return to sub-step 1 of this step
5. If quality threshold is met OR max iterations (2) reached, proceed to report

**Stopping criteria (any one sufficient):**
- No Critical or High findings remain
- Total new findings <= 2 (Low severity only)
- Max 2 refinement iterations reached
- No improvement between iterations (same or more findings)

**If max iterations exhausted with remaining findings:** Include them in the report under "Remaining Issues (post-refinement)".

### Step 8: Report

Present the final report using the template in [references/report-template.md](references/report-template.md).

## Output

Present a summary report to the user:

```
Simplify Review Report
======================
Changed Files: [N]
Total Findings: [N] (Critical: X, High: X, Medium: X, Low: X)

Findings by Category:
  Refactor:     [N] findings
  Quality:      [N] findings
  Tech Debt:    [N] findings
  Performance:  [N] findings

Applied Fixes: [N] / [N]
Skipped:       [N] (reason for each)

Top Changes:
  1. [file] — [what was fixed]
  2. [file] — [what was fixed]
  ...
```

## Optional Arguments

The user can control scope and focus:

```
# Scoping modes
/simplify                          # diff mode (default) — review uncommitted changes
/simplify diff                     # explicit diff mode
/simplify today                    # today mode — all files changed today
/simplify full                     # full mode — entire project
/simplify project                  # alias for full mode

# Focus (combinable with any mode)
/simplify focus on performance     # diff + prioritize performance
/simplify today focus on security  # today + prioritize security

# Directory scope (overrides mode)
/simplify src/api/                 # scan specific directory only

# Evaluator-Optimizer refinement (combinable with any mode)
/simplify --refine                 # re-evaluate after fixes (max 2 iterations)
/simplify today --refine           # today mode + re-evaluation loop
```

When a focus is specified, still run all 4 agents but highlight and prioritize findings matching the focus area.

## Examples

### Example 1: diff mode — Post-implementation cleanup

User runs `/simplify` after implementing a feature.

Actions:
1. `git diff HEAD` finds 5 changed files
2. 4 agents run in parallel (~15 seconds with fast model)
3. Findings: 2 High (duplicated logic, magic strings), 4 Medium (naming, TODO), 1 Low (comment style)
4. Apply 6/7 fixes, skip 1 (ambiguous refactor)
5. ReadLints confirms no regressions
6. Report presented with summary table

### Example 2: today mode — End-of-day review

User runs `/simplify today` before wrapping up for the day.

Actions:
1. `git log --since=midnight` + `git diff` finds 12 files across 4 commits + uncommitted changes
2. 4 agents run in parallel, each reviewing all 12 files
3. Findings: 1 Critical (SQL injection in new endpoint), 3 High, 5 Medium, 2 Low
4. Apply 10/11 fixes, skip 1 (requires architectural decision)
5. Verification passes
6. Comprehensive daily report covering all today's work

### Example 3: full mode — Project-wide scan

User runs `/simplify full` for a periodic codebase health check.

Actions:
1. Find all source files: 47 files across `src/`, `lib/`, `tests/`
2. Split into 2 batches (~24 files each), run 4 agents per batch
3. Findings: 2 Critical, 8 High, 15 Medium, 10 Low across entire codebase
4. Apply fixes by severity, skip architectural changes
5. Full project health report with category breakdown

### Example 4: Focused performance review

User runs `/simplify today focus on performance` after a day of optimization work.

Actions:
1. `git log --since=midnight` finds 3 changed files in `src/utils/`
2. 4 agents run; Performance agent findings highlighted first
3. Findings: 1 High (O(n²) loop), 2 Medium (redundant parsing, unused import)
4. All 3 fixes applied
5. Verification passes
6. Report highlights performance improvements

## Error Handling

| Scenario | Action |
|----------|--------|
| No git changes detected (diff mode) | Suggest `today` or `full` mode, or specify files |
| No commits today (today mode) | Fall back to `diff` mode; if also empty, inform user |
| Too many files (full mode, 100+) | Warn user with file count, ask for confirmation or directory scope |
| Sub-agent timeout | Re-launch failed agent once; if still fails, report partial results |
| Sub-agent returns empty | Note the category as "no issues found" and continue |
| Lint errors after fix | Auto-fix lint errors; if unfixable, revert that specific fix |
| Conflicting fixes | Apply first fix, skip subsequent conflicting ones with explanation |

## Troubleshooting

- **"No changes found"**: Try `/simplify today` for today's work or `/simplify full` for the entire project
- **Slow execution on full mode**: Large projects are batched; expect 30-60 seconds for 50+ files
- **Slow execution on diff/today**: All 4 agents run in parallel; typical time is 10-20 seconds
- **Unexpected fixes**: Each fix is applied via StrReplace with exact string matching; review the diff after completion
