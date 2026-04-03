---
name: review-team-orchestrator
description: >-
  Multi-perspective code review team that fans out 3 independent review skills
  (deep-review, simplify, test-suite) in parallel, then deduplicates and
  merges all findings into a unified severity-ranked report. Each sub-skill
  runs its own internal agents (~12 total agents). Use when the user asks
  for "full code review", "review team", "multi-perspective review",
  "comprehensive review", "코드 리뷰 팀", "종합 리뷰", "다관점 리뷰",
  or wants all review perspectives combined. Do NOT use for single-perspective
  review (use deep-review, simplify, or test-suite directly). Do NOT use for
  release pipeline (use release-commander). Do NOT use for security-focused
  review only (use quality-gate-orchestrator).
metadata:
  version: "1.0.0"
  tags: ["orchestrator", "review", "code-review", "harness", "fan-out-fan-in"]
  pattern: "fan-out/fan-in + deduplication"
  composes:
    - deep-review
    - simplify
    - test-suite
---

# Code Review Multi-Perspective Team Orchestrator

Fan out 3 review skills in parallel, then deduplicate and merge findings into a unified report.

## Usage

```
/review-team                             # Full 3-way review
/review-team --skip test-suite           # Skip test review
/review-team --light                     # Reduced internal agents per skill
/review-team --scope src/services/       # Limit review scope
/review-team --dry-run                   # Show plan without executing
```

## Skip Flags

| Flag | Skips | Default |
|------|-------|---------|
| `deep` | `deep-review` (architecture + code quality) | included |
| `simplify` | `simplify` (complexity + refactoring) | included |
| `test` | `test-suite` (test coverage + quality) | included |

## Agent Team

| Agent | Skill | Internal Agents | model | Output |
|-------|-------|-----------------|-------|--------|
| Architecture + Quality | `deep-review` | 4 domain agents | (default) | `_workspace/review-team/01_deep-review.md` |
| Complexity + Refactoring | `simplify` | 4 review agents | (default) | `_workspace/review-team/01_simplify.md` |
| Test Coverage + Quality | `test-suite` | 2+N test agents | (default) | `_workspace/review-team/01_test-suite.md` |

**Total agents**: ~12 (significant token cost — use `--light` for cost-sensitive reviews).

## Workflow

### Pre-flight

1. Parse `$ARGUMENTS` for `--skip`, `--light`, `--scope`, `--dry-run`.
2. Detect changed files: `git diff --name-only HEAD~1` (or `--scope` directory).
3. `Shell: mkdir -p _workspace/review-team`
4. If `--dry-run`, print the execution plan and stop.
5. If `--light`, set instruction for each sub-skill to use 2 internal agents instead of 4.

### Phase 1: Parallel Reviews (Fan-out — 3 parallel Tasks)

Launch up to 3 sub-agents via the Task tool in a single message.

**Deep Review:**
```
You are a code architecture and quality reviewer.

## Skill Reference
Read and follow `.cursor/skills/review/deep-review/SKILL.md`.

## Task
Perform a comprehensive code review focusing on:
- Architecture and design patterns
- Code quality and maintainability
- Error handling and edge cases
- Security considerations
{If --scope: "Limit review to files in {scope}."}
{If --light: "Use only 2 internal review agents instead of 4 to reduce cost."}

Changed files for context:
{changed_files_list}

## Output
Write ALL findings to `_workspace/review-team/01_deep-review.md`.
Format each finding as:
- **[SEVERITY]** (Critical/High/Medium/Low)
- **File**: path:line
- **Issue**: description
- **Recommendation**: fix suggestion

## Completion
Return count of findings by severity.
```

**Simplify:**
```
You are a code complexity and refactoring reviewer.

## Skill Reference
Read and follow `.cursor/skills/review/simplify/SKILL.md`.

## Task
Review code for complexity reduction opportunities:
- Unnecessary complexity and over-engineering
- Code duplication and DRY violations
- Readability improvements
- Simplification opportunities
{If --scope: "Limit review to files in {scope}."}
{If --light: "Use only 2 internal review agents instead of 4 to reduce cost."}

Changed files for context:
{changed_files_list}

## Output
Write ALL findings to `_workspace/review-team/01_simplify.md`.
Use the same finding format as deep-review.

## Completion
Return count of findings by severity.
```

**Test Suite:**
```
You are a test coverage and quality reviewer.

## Skill Reference
Read and follow `.cursor/skills/review/test-suite/SKILL.md`.

## Task
Review test coverage and quality:
- Missing test coverage for changed code
- Test quality and assertion strength
- Edge case coverage gaps
- Untested error paths
{If --scope: "Limit review to files in {scope}."}
{If --light: "Use only 2 internal test agents to reduce cost."}

Changed files for context:
{changed_files_list}

## Output
Write ALL findings to `_workspace/review-team/01_test-suite.md`.
Use the same finding format as deep-review.

## Completion
Return count of findings by severity.
```

Wait for all Phase 1 agents to complete.

### Phase 2: Deduplication + Ranking

Read all `_workspace/review-team/01_*.md` files.

**Deduplication logic:**
1. Match findings by file+line across all 3 review outputs.
2. When the same issue is found by multiple reviewers:
   - Keep the highest severity classification
   - Merge descriptions (note which reviewers flagged it)
   - Keep the most specific recommendation
3. Group related findings (e.g., same pattern in different files).

**Severity ranking:**
1. Critical → Must fix before merge
2. High → Should fix before merge
3. Medium → Should fix, can defer
4. Low → Nice to have, optional

Write `_workspace/review-team/02_unified.md`.

### Phase 3: Report

Present the unified review report directly in the conversation (matching `deep-review` pattern — not saved to file).

```markdown
# Unified Code Review Report

## Summary
- **Total findings**: {count} ({deduplicated from {raw_count} across 3 reviewers})
- **By severity**: Critical: {n}, High: {n}, Medium: {n}, Low: {n}
- **Reviewers**: {list of active reviewers}

## Critical & High Findings

### 1. {Finding title}
- **Severity**: {Critical/High}
- **File**: {path:line}
- **Found by**: {reviewer1, reviewer2}
- **Issue**: {merged description}
- **Recommendation**: {best recommendation}

### 2. ...

## Medium & Low Findings
{Grouped by theme, abbreviated}

## Cross-Reviewer Agreements
{Findings flagged by 2+ reviewers — these are highest confidence}

## Contradictions
{Any findings where reviewers disagreed on severity or approach}
```

## Error Handling

| Failure | Action |
|---------|--------|
| 1 reviewer fails | Retry once. If still fails, proceed with remaining 2 reviewers. Note in report. |
| 2 reviewers fail | Proceed with single reviewer output. Warn user about limited coverage. |
| All reviewers fail | Abort with error. |
| Deduplication finds no overlap | Normal — present all findings unmerged. |
| Changed files list is empty | Review full codebase (warn about scope). |

## Cost Considerations

Each sub-skill runs 2-4 internal agents, totaling ~12 agents for a full review. This has significant token cost.

| Mode | Internal Agents | Estimated Cost |
|------|----------------|----------------|
| Full (`/review-team`) | ~12 agents | ~4x single review |
| Light (`/review-team --light`) | ~6 agents | ~2x single review |
| Single skip (`--skip test`) | ~8 agents | ~3x single review |

Use `--light` for routine reviews and full mode for pre-release or critical changes.

## Data Flow

```
Pre-flight (detect changed files)
    │
    ▼ Phase 1 (parallel)
    ├─► deep-review (4 agents)   ──► 01_deep-review.md  ─┐
    ├─► simplify (4 agents)      ──► 01_simplify.md      ─┼─► Dedup + Rank ──► 02_unified.md
    └─► test-suite (2+N agents)  ──► 01_test-suite.md    ─┘         │
                                                                     ▼
                                                              Unified Report
                                                         (conversation output)
```

## Relationship with release-commander

This orchestrator is a **standalone entry point** for comprehensive code review. It is separate from `release-commander`, which has its own pipeline calling review skills individually across groups. Users who want review-only should use `/review-team`; users who want the full release pipeline (review + security + changelog + PR) should use `/release-commander`.


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
