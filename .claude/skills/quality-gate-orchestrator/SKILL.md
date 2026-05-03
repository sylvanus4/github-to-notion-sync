---
name: quality-gate-orchestrator
description: >-
  Unified security and quality gate that runs deterministic CI checks first
  (lint, type-check, tests), then fans out 3 parallel AI-powered scans
  (security audit, dependency analysis, performance profiling), and merges all
  findings into a deduplicated PASS/FAIL dashboard. Use when the user asks for
  "quality gate", "full quality check", "security + quality scan",
  "pre-release quality", "품질 게이트", "보안 + 품질 검사", "전체 품질 체크", or wants a
  comprehensive code health assessment before shipping. Do NOT use for CI
  checks only (use ci-quality-gate). Do NOT use for security audit only (use
  security-expert). Do NOT use for the full release pipeline (use
  release-commander).
---

# Security & Quality Gate Orchestrator

Run deterministic CI checks as a gate, then fan out 3 AI-powered scans in parallel, and produce a unified dashboard with deduplicated findings.

## Usage

```
/quality-gate                           # Full gate (CI + 3 AI scans)
/quality-gate --skip security,perf      # Skip specific scans
/quality-gate --force                   # Continue even if CI fails
/quality-gate --dry-run                 # Show plan without executing
```

## Skip Flags

| Flag | Skips | Default |
|------|-------|---------|
| `ci` | CI quality gate (lint, type-check, tests) | included |
| `security` | `security-expert` AI scan | included |
| `deps` | `dependency-auditor` AI scan | included |
| `perf` | `performance-profiler` AI scan | included |

## Agent Team

| Agent | Skill | Execution | model | Output |
|-------|-------|-----------|-------|--------|
| CI Gate | `ci-quality-gate` | Shell (sequential) | N/A | `_workspace/quality-gate/00_ci-results.md` |
| Security Auditor | `security-expert` | Task (parallel) | fast | `_workspace/quality-gate/01_security.md` |
| Dependency Auditor | `dependency-auditor` | Task (parallel) | fast | `_workspace/quality-gate/01_deps.md` |
| Performance Profiler | `performance-profiler` | Task (parallel) | fast | `_workspace/quality-gate/01_perf.md` |

## Workflow

### Pre-flight

1. Parse `$ARGUMENTS` for `--skip`, `--force`, `--dry-run`.
2. Detect changed files via `git diff --name-only HEAD~1` (or `--staged` if uncommitted).
3. `Shell: mkdir -p _workspace/quality-gate`
4. If `--dry-run`, print the execution plan and stop.

### Phase 0: Deterministic CI Gate (Sequential)

Unless `--skip ci`:

Run CI quality checks via Shell commands (not Task tool — deterministic):

```bash
make test-ci  # or equivalent: ruff check, black --check, mypy, bandit
```

Write results to `_workspace/quality-gate/00_ci-results.md`.

**Gate check**: If CI fails AND `--force` is NOT set, stop and report failures.
If `--force` is set, continue with a warning in the dashboard.

### Phase 1: AI-Powered Scans (Fan-out)

Launch up to 3 sub-agents via the Task tool in a single message.

For each non-skipped scanner:

**Security Expert:**
```
You are a security auditor.

## Skill Reference
Read and follow `.cursor/skills/review/security-expert/SKILL.md`.

## Task
Perform a security audit on the current codebase, focusing on changed files:
{changed_files_list}

## Output
Write findings to `_workspace/quality-gate/01_security.md`.
Format: Markdown with sections for Critical, High, Medium, Low findings.
Each finding: file, line, description, recommendation, CVE if applicable.

## Completion
Return count of findings by severity.
```

**Dependency Auditor:**
```
You are a dependency security analyst.

## Skill Reference
Read and follow `.cursor/skills/review/dependency-auditor/SKILL.md`.

## Task
Audit all project dependencies for known vulnerabilities, license issues,
and outdated packages.

## Output
Write findings to `_workspace/quality-gate/01_deps.md`.
Format: Markdown with sections for CVEs, License Issues, Outdated Packages.

## Completion
Return count of findings by severity.
```

**Performance Profiler:**
```
You are a performance analyst.

## Skill Reference
Read and follow `.cursor/skills/review/performance-profiler/SKILL.md`.

## Task
Profile the codebase for performance issues, focusing on changed files:
{changed_files_list}

## Output
Write findings to `_workspace/quality-gate/01_perf.md`.
Format: Markdown with sections for N+1 queries, memory issues,
slow paths, caching opportunities.

## Completion
Return count of findings by severity.
```

Wait for all Phase 1 agents to complete.

### Phase 2: Dashboard Merge

Read `00_ci-results.md` and all `01_*.md` files.

Deduplication logic:
- Match CVEs across security + deps reports (same CVE = single entry)
- Match file+line findings across security + perf reports
- Keep the richer description when merging duplicates

Produce `outputs/quality-gate/dashboard-{date}.md`:

```markdown
# Quality Gate Dashboard — {date}

## Overall Verdict: {PASS | FAIL | WARN}

## CI Results
| Check | Status | Details |
|-------|--------|---------|
| Lint | ✅/❌ | {summary} |
| Type Check | ✅/❌ | {summary} |
| Tests | ✅/❌ | {pass}/{total} |
| Security Scan | ✅/❌ | {summary} |

## Findings by Severity
| Severity | Count | Source(s) |
|----------|-------|-----------|
| Critical | N | security, deps |
| High | N | security, perf |
| Medium | N | all |
| Low | N | all |

## Critical & High Findings (Detail)
{Deduplicated list, sorted by severity}

## Recommendations
{Top 3 actionable items}

---
Generated by quality-gate-orchestrator v1.0.0
Scans: {list of non-skipped scans}
Changed files analyzed: {count}
```

Also output the verdict to the conversation for immediate visibility.

## Error Handling

| Failure | Action |
|---------|--------|
| CI gate fails | Block unless `--force`. Report in dashboard. |
| 1 AI scan fails | Retry once. If still fails, note in dashboard: "_{scan}_ unavailable." |
| 2+ AI scans fail | Produce degraded dashboard with available data. |
| No changed files | Run full-codebase scan with warning about scope. |

## Data Flow

```
Pre-flight (detect changed files)
    │
    ▼
Phase 0: CI Gate (Shell)
    │  ❌ + no --force → STOP
    │  ✅ or --force
    ▼
    ├─► Security Expert  ──► 01_security.md ─┐
    ├─► Dependency Audit ──► 01_deps.md     ─┼─► Dashboard Merge ──► dashboard-{date}.md
    └─► Perf Profiler    ──► 01_perf.md     ─┘         │
                                                        ▼
                                                 PASS / FAIL / WARN
```

## Integration with release-commander

`release-commander` can optionally delegate its Group A (deterministic checks) and Group B (AI scans) to this orchestrator for a unified view. This is complementary — `release-commander` retains its own pipeline for the full release lifecycle.

## Verification Protocol

Before reporting any review or audit complete, verify findings with evidence:

```text
### Check: [what you are verifying]
**Command run:** [exact command executed]
**Output observed:** [actual output — copy-paste, not paraphrased]
**Result:** PASS or FAIL (with Expected vs Actual if FAIL)
```

A check without a command-run block is not a PASS — it is a skip.

Before issuing PASS: must include at least one adversarial probe (boundary input, concurrent request, missing data, permission edge case).

Before issuing FAIL: check if the issue is already handled elsewhere, intentional by design, or not actionable without breaking an external contract.

End verification with: `VERDICT: PASS`, `VERDICT: FAIL`, or `VERDICT: PARTIAL`.

## Honest Reporting

- Report review outcomes faithfully: if a check fails, say so with the relevant output
- Never claim "all checks pass" when output shows failures
- Never suppress or simplify failing checks to manufacture a green result
- When a check passes, state it plainly without unnecessary hedging
- The final report must accurately reflect what was found — not what was hoped

## Rationalization Detection

Recognize these rationalizations and do the opposite:

| Rationalization | Reality |
|----------------|---------|
| "The code looks correct based on my reading" | Reading is not verification. Run it. |
| "The implementer's tests already pass" | The implementer is an LLM. Verify independently. |
| "This is probably fine" | Probably is not verified. Run it. |
| "I don't have access to test this" | Did you check all available tools? |
| "This would take too long" | Not your call. Run the check. |
| "Let me check the code structure" | No. Start the server and hit the endpoint. |

If you catch yourself writing an explanation instead of running a command, stop. Run the command.


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
