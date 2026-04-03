---
name: release-commander
description: >-
  Full release lifecycle orchestrator that chains 10 existing skills into a
  single pipeline: code review, security scan, test validation, performance
  check, i18n sync, dependency audit, changelog generation, domain-split
  commits, PR summary, and PR creation. Use when the user asks to "prepare
  release", "release pipeline", "full release check", "release commander",
  "릴리즈", "릴리즈 준비", or wants a comprehensive pre-release validation. Do NOT use
  for code review only (use deep-review or simplify), commit only (use
  domain-commit), PR only (use ship), or individual checks (use the specific
  skill directly).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# Release Commander — Full Release Lifecycle Pipeline

One command to take code from "feature complete" to "release-ready PR" with comprehensive validation. Orchestrates 10 specialized skills across 4 sequential groups.

> **Note**: For a unified quality gate view of Group A + B scans (security, dependency, performance + CI), consider using `/quality-gate` (`quality-gate-orchestrator`) as a standalone check. The quality gate orchestrator provides deduplicated findings with a PASS/FAIL dashboard. `release-commander` retains its own group pipeline for the full release lifecycle.

## Usage

```
/release-commander                              # full pipeline
/release-commander --skip security,i18n         # skip specific checks
/release-commander --dry-run                    # validation only, no commits/PR
/release-commander --base release-v1.2          # specify PR base branch
/release-commander --changelog-only             # generate changelog from recent commits
```

## Pipeline Overview

```
Group A (parallel): Review
  ├─ deep-review       → Full-stack code review (4 agents)
  ├─ security-expert   → Threat model + vulnerability scan
  └─ performance-profiler → Latency, queries, bundle size

    ↓ Gate: all reviews pass or findings are Low/Medium only

Group B (parallel): Validate
  ├─ test-suite        → Run tests, generate missing, fix failures
  ├─ i18n-sync         → Translation key completeness
  └─ dependency-auditor → CVE scan, outdated packages

    ↓ Gate: tests pass, no critical CVEs, translations complete

Group C (sequential): Package
  ├─ technical-writer  → Generate CHANGELOG entry
  └─ domain-commit     → Domain-split commits with pre-commit hooks

    ↓ Gate: commits created, lint passes

Group D (sequential): Ship
  ├─ pr-review-captain → PR summary, risk assessment, review checklist
  └─ ship (PR step)    → Push branch + create PR
```

## Workflow

### Step 1: Pre-flight Check

Before launching the pipeline:

1. Verify there are uncommitted or recent changes to release
2. Identify the target branch (`--base`, default: `main`)
3. Check for existing open PRs on the current branch
4. Parse `--skip` flags: split by comma, valid values are `security`, `i18n`, `deps`, `perf`, `tests`. Invalid values are ignored with a warning.
5. Verify each referenced skill exists on disk before adding to the pipeline. If a skill file is missing (e.g., `i18n-sync` not installed), skip it with a warning rather than failing.

If no changes detected, inform the user and stop.

### Step 2: Group A — Parallel Review

Launch 3 sub-agents via the Task tool:

**Agent 1: deep-review**
- `subagent_type: generalPurpose`
- Prompt: Read and follow `.cursor/skills/review/deep-review/SKILL.md`. Run a full-stack review on the changed files. Scope: diff. Return findings grouped by severity.

**Agent 2: security-expert**
- `subagent_type: generalPurpose`
- Prompt: Read and follow `.cursor/skills/review/security-expert/SKILL.md`. Perform threat modeling and vulnerability assessment on the changed files. Focus on OWASP Top 10 and secret detection.

**Agent 3: performance-profiler**
- `subagent_type: generalPurpose`
- Prompt: Read and follow `.cursor/skills/review/performance-profiler/SKILL.md`. Check for N+1 queries, bundle size impact, and latency concerns in the changed files.

**Gate check**: If any Critical or High findings are reported:
- Present findings to the user
- Ask whether to proceed, fix, or abort
- If fixing, apply fixes and re-run the failed check

### Step 3: Group B — Parallel Validation

Launch 3 sub-agents:

**Agent 4: test-suite**
- Run test lifecycle: coverage review → generate missing tests → execute suite
- Scope: changed files and their test files

**Agent 5: i18n-sync** (skip if `--skip i18n`)
- Check translation key completeness across all locale files
- Report missing keys with draft translations

**Agent 6: dependency-auditor** (skip if `--skip deps`)
- Scan for CVEs in Python, Go, and Node.js dependencies
- Report severity and recommend updates

**Gate check**: If tests fail or critical CVEs found:
- Present failures to the user
- Attempt auto-fix for test failures (retry once)
- For CVEs, recommend patch updates

### Step 3½: Cross-Group Consistency Gate

Before packaging, verify that Group A and Group B findings are consistent:

- [ ] **No conflicting remediations** — Security fixes don't break tests; dependency updates don't introduce new security findings
- [ ] **All Critical/High findings addressed** — Every Critical or High finding from Group A has either been fixed, accepted by the user, or has a documented exception
- [ ] **Coverage not regressed** — Test coverage has not decreased compared to the base branch

If any criterion fails, present the inconsistency to the user before proceeding to Group C.

### Step 4: Group C — Package

Sequential execution:

**Step 4a: technical-writer**
- Generate a CHANGELOG entry from commit messages and review findings
- Format: date, version, categorized changes (Added, Changed, Fixed, Security)
- Append to `CHANGELOG.md` (create if missing)

**Step 4b: domain-commit**
- Follow domain-commit skill pattern
- Group changes by domain (backend, frontend, config, docs, tests)
- Create one commit per domain with `[TYPE] Summary` format
- Run pre-commit hooks; fix and retry on failure

### Step 5: Group D — Ship

Sequential execution:

**Step 5a: pr-review-captain**
- Generate PR summary from all review findings and commits
- Produce risk assessment and review checklist
- Generate release notes (user-facing changes)

**Step 5b: Create PR**
- Push branch: `git push origin HEAD:tmp`
- Create PR via `gh pr create` with:
  - Title: derive issue number from branch name (e.g., `issue/#42-feature` → `#42`). If branch doesn't match `issue/#N*` pattern, omit the issue number. Format: `[release] Release summary` or `#42 [release] Release summary`
  - Body: review summary, risk assessment, changelog excerpt, review checklist
- **CRITICAL**: Never push to upstream. Only push to origin.

### Step 6: Release Report

```
Release Commander Report
=========================
Pipeline: review → validate → package → ship

Review (Group A):
  deep-review:         [N] findings (Critical: X, High: X, Med: X, Low: X)
  security-expert:     [N] findings ([N] fixed, [N] accepted)
  performance-profiler: [PASS|WARN] — [summary]

Validation (Group B):
  test-suite:          [PASS|FAIL] — [N] tests, [N]% coverage
  i18n-sync:           [PASS|WARN] — [N] missing keys
  dependency-auditor:  [PASS|WARN] — [N] CVEs found

Package (Group C):
  changelog:           Updated CHANGELOG.md
  commits:             [N] domain-split commits

Ship (Group D):
  PR:                  https://github.com/org/repo/pull/N
  Title:               [PR title]
  Base:                [base] ← [branch]

Overall: [READY FOR REVIEW | NEEDS ATTENTION]
```

## Examples

### Example 1: Full release pipeline

User: `/release-commander`

All 4 groups run sequentially. 10 skills execute. PR created with comprehensive review summary, security sign-off, test results, and release notes.

### Example 2: Dry run

User: `/release-commander --dry-run`

Groups A and B run (review + validation). Report generated without commits or PR. User can review findings before committing.

### Example 3: Skip specific checks

User: `/release-commander --skip security,i18n`

Skips security-expert and i18n-sync. Runs deep-review, performance-profiler, test-suite, dependency-auditor, then packages and ships.

## Error Handling

| Scenario | Action |
|----------|--------|
| No changes detected | Inform user and stop |
| Critical security finding | Halt pipeline, present finding, require user decision |
| Tests fail after retry | Report failures, ask user to fix manually |
| Pre-commit hook fails | Fix lint errors automatically, retry once |
| Push rejected | Report error; suggest `git pull origin tmp` |
| PR already exists | Update existing PR instead of creating new one |
| Sub-agent timeout | Re-launch once; continue with partial results |
| CHANGELOG.md doesn't exist | Create it with initial structure |

## Troubleshooting

- **"No changes detected"**: Ensure you have uncommitted changes or recent commits. Try `git log --oneline -5` to verify.
- **Skill not found warning**: The pipeline gracefully skips missing skills. Install the missing skill or use `--skip` to suppress the warning.
- **Push rejected**: Usually means the remote `tmp` branch is ahead. Run `git pull origin tmp` before retrying.
- **PR already exists**: The pipeline detects existing PRs via `gh pr list --head tmp` and updates them instead.

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
