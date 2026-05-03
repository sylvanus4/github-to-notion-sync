---
name: test-suite
description: >-
  Run a full test lifecycle pipeline: 2 parallel review agents (Test Coverage,
  Test Quality) analyze existing tests, then a Test Generator creates missing
  tests, and a Test Runner executes the suite with retry logic. Supports
  diff/today/full scoping. Use when the user runs /test-suite, asks for "test
  review", "check test coverage", "generate missing tests", "run and fix
  tests", or "full test audit". Do NOT use for single-file test writing,
  manual test execution only (use shell), or code review without test focus
  (use /simplify). Korean triggers: "테스트", "감사", "리뷰", "분석".
---

# Test Suite — Test Full-Lifecycle Orchestrator

Analyze test coverage and quality from 2 perspectives simultaneously, auto-generate missing tests, then execute the suite and fix failures. Covers the entire test lifecycle from audit to green CI.

## Scoping Modes

| Mode | Trigger | Scope |
|------|---------|-------|
| `diff` (default) | `/test-suite` | Source + test files from git diff |
| `today` | `/test-suite today` | All files changed today |
| `full` | `/test-suite full` | All source and test files |

Optional flags:
- `--no-gen`: skip test generation (review only)
- `--no-run`: skip test execution
- Combinable: `/test-suite today --no-gen`

## Workflow

### Step 1: Identify Target Files

Resolve files using the scoping mode, then classify:

**Source files**: `*.ts`, `*.tsx`, `*.js`, `*.jsx`, `*.py`, `*.go`, `*.rs`, `*.java`, `*.kt` (excluding test files)
**Test files**: `*.test.*`, `*.spec.*`, files in `tests/`, `__tests__/`, `test/`
**Config files**: `jest.config.*`, `vitest.config.*`, `pytest.ini`, `pyproject.toml`, `playwright.config.*`

Build a source-to-test mapping by matching file names and directory structure.

### Step 2: Launch 2 Parallel Review Agents

Use the Task tool to spawn 2 read-only sub-agents. Each receives source files, test files, and the source-to-test mapping. For detailed prompts, see [references/agent-prompts.md](references/agent-prompts.md).

```
Agent 1: Test Coverage Agent → Missing tests, untested paths, coverage gaps
Agent 2: Test Quality Agent  → Assertion strength, flakiness, test structure
```

Sub-agent configuration:
- `subagent_type`: `generalPurpose`
- `model`: `fast`
- `readonly`: `true`

Each agent returns findings in this structure:

```
CATEGORY: [agent category]
FINDINGS:
- severity: [Critical|High|Medium|Low]
  file: [path]
  line: [number or range]
  issue: [description]
  fix: [suggested change or test to write]
```

### Step 3: Aggregate and Prioritize

1. Merge all agent outputs into a single findings list
2. Remove duplicates (same file + same issue)
3. Sort: Critical > High > Medium > Low
4. Separate into two groups:
   - **Coverage gaps** (need new tests) — feed to Test Generator
   - **Quality issues** (need test modifications) — feed to Test Generator

### Step 4: Test Generator Agent (skip if `--no-gen`)

Launch a write-enabled sub-agent that receives:
- The aggregated findings
- The source files needing tests
- Existing test files (for pattern matching)
- Test framework configuration

```
Agent 3: Test Generator → Write missing tests, fix quality issues
```

Sub-agent configuration:
- `subagent_type`: `generalPurpose`
- `model`: `fast`
- `readonly`: `false`

The generator:
- Creates new test files for untested source files
- Adds missing test cases to existing test files
- Follows the project's existing patterns (framework, assertion style, file naming)
- Fixes quality issues (weak assertions, missing edge cases)
- Does NOT delete or restructure existing passing tests

### Step 5: Test Runner Agent (skip if `--no-run`)

Launch an execution sub-agent that:
1. Detects the test framework from config files and package.json/pyproject.toml
2. Runs the test suite (scoped to affected tests when possible)
3. Captures pass/fail results with failure details
4. If tests fail, attempts a targeted fix and re-runs (max 2 retries)
5. Reports final results

```
Agent 4: Test Runner → Execute tests, fix failures, report results
```

Sub-agent configuration:
- `subagent_type`: `generalPurpose`
- `model`: `fast`
- `readonly`: `false`

Framework detection priority:
1. `vitest.config.*` or `vite.config.*` with test → vitest
2. `jest.config.*` or package.json `jest` field → jest
3. `pytest.ini` or `pyproject.toml` `[tool.pytest]` → pytest
4. `playwright.config.*` → playwright test
5. `go.mod` → go test
6. Fall back to `npm test` or warn if undetectable

### Step 6: Report

Present report using the template in [references/report-template.md](references/report-template.md).

## Optional Arguments

```
/test-suite                            # diff mode — test files from uncommitted changes
/test-suite today                      # today mode — all test files changed today
/test-suite full                       # full mode — entire project test audit
/test-suite --no-gen                   # review only, skip test generation
/test-suite --no-run                   # skip test execution
/test-suite src/services/              # scope to specific directory
/test-suite full --no-run              # audit + generate, skip execution
```

## Examples

### Example 1: Post-feature test audit

User runs `/test-suite` after implementing a new API endpoint.

Actions:
1. `git diff HEAD` finds 4 source files and 1 test file
2. 2 review agents analyze in parallel
3. Findings: 1 Critical (endpoint has no tests), 2 High (missing error path tests), 3 Medium
4. Test Generator creates 1 new test file, adds 5 test cases to existing file
5. Test Runner executes: 18/20 pass, 2 fail
6. Runner fixes 2 failures and re-runs: 20/20 pass
7. Report with coverage improvement metrics

### Example 2: Full project test health check

User runs `/test-suite full` for a comprehensive test audit.

Actions:
1. Find 45 source files, 22 test files
2. Coverage Agent finds 12 untested source files
3. Quality Agent finds 8 weak assertions, 3 flaky patterns
4. Generator creates 8 new test files, fixes 6 quality issues
5. Runner executes full suite: 142/145 pass
6. After retry: 145/145 pass
7. Comprehensive test health report

### Example 3: Review-only mode

User runs `/test-suite full --no-gen --no-run` to see the current test landscape.

Actions:
1. Find all source and test files
2. 2 review agents analyze in parallel
3. Present findings: coverage gaps, quality issues, recommendations
4. No files modified, no tests executed

## Error Handling

| Scenario | Action |
|----------|--------|
| No test files found | Report coverage gaps only; generator creates from scratch |
| No source files found | Inform user; nothing to test |
| Test framework not detected | Warn and ask user; skip execution |
| Generator creates invalid tests | Runner catches failures; attempt fix up to 2 retries |
| All retries exhausted | Report remaining failures; user must fix manually |
| Sub-agent timeout | Re-launch once; if still fails, report partial results |

## Troubleshooting

- **"Test framework not detected"**: Ensure config files exist or specify the framework in the command
- **"No test files"**: Normal for new projects; the generator will create initial test files
- **Generated tests are wrong**: Use `--no-gen` to review first, then write tests manually using findings as a guide
- **Flaky test failures**: Quality Agent detects flakiness patterns; address those findings first

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
