---
name: omc-ultraqa
description: >-
  Autonomous QA cycling workflow that runs test → diagnose → fix → repeat
  until a quality goal is met (max 5 cycles). Supports goal types: tests,
  build, lint, typecheck, and custom patterns. Uses an architect-diagnosis
  subagent for root cause analysis before each fix attempt. Detects repeated
  failures and exits early to prevent infinite loops. Use when the user asks
  to "fix all tests", "make tests pass", "fix build", "fix lint errors",
  "ultraqa", "QA cycle", "test fix loop", "autonomous QA", "keep fixing until
  green", "make CI pass", "테스트 통과시켜", "빌드 고쳐", "린트 에러 수정", "자동 QA", "테스트 루프",
  "CI 통과", or wants an automated diagnose-fix-verify cycle until quality gates
  pass. Do NOT use for writing new tests from scratch (use qa-test-expert or
  test-suite). Do NOT use for test strategy design (use qa-test-expert). Do
  NOT use for single known bug fixes (use diagnose). Do NOT use for code
  review (use simplify or deep-review).
---

# UltraQA: Autonomous QA Cycling

Adapted from [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) ultraqa skill. Implements autonomous diagnose-fix-verify cycling until quality goals are met.

## Instructions

### Goal Parsing

Parse the quality goal from the user's request:

| Goal Type | What to Check | Typical Command |
|-----------|---------------|-----------------|
| `tests` | All test suites pass | `pytest` / `vitest run` / `npm test` |
| `build` | Build succeeds with exit 0 | `npm run build` / `make build` |
| `lint` | No lint errors | `ruff check` / `eslint` / `npm run lint` |
| `typecheck` | No type errors | `mypy` / `tsc --noEmit` / `pyright` |
| `custom` | Custom success pattern in output | User-specified command + pattern |

If no structured goal is provided, interpret the argument as a custom goal.

Prefix supported commands with `rtk` for token-efficient output (per rtk-token-optimization rule).

### Cycle Workflow (Max 5 Cycles)

#### 1. RUN QA

Execute verification based on goal type:

```
[ULTRAQA Cycle {n}/5] Running {goal_type}...
```

Run the appropriate command and capture full output.

#### 2. CHECK RESULT

- **PASS** → Exit with success: `[ULTRAQA COMPLETE] Goal met after {n} cycles`
- **FAIL** → Continue to step 3

#### 3. ARCHITECT DIAGNOSIS

Spawn a `Task` subagent (`subagent_type="generalPurpose"`) as an architect-diagnostician:

```
Prompt: "DIAGNOSE FAILURE:
Goal: {goal_type}
Output: {test/build/lint output}
Provide:
1. Root cause (not symptoms)
2. Specific files and lines to modify
3. Exact fix recommendations
4. Why previous fixes (if any) didn't work: {previous_failures}"
```

#### 4. FIX ISSUES

Apply the architect's recommendations. For each fix:
- Make the minimal change that addresses the root cause
- Do NOT introduce new features or refactors during the fix
- If multiple independent issues exist, fix them in priority order

#### 5. REPEAT

Return to step 1 with the next cycle number.

### Exit Conditions

| Condition | Action |
|-----------|--------|
| **Goal Met** | `[ULTRAQA COMPLETE] Goal met after {n} cycles` |
| **Cycle 5 Reached** | `[ULTRAQA STOPPED] Max cycles reached. Remaining issues: {diagnosis}` |
| **Same Failure 3x** | `[ULTRAQA STOPPED] Same failure detected 3 times. Root cause: {analysis}`. Consider invoking `hypothesis-qa` for structured hypothesis-driven triage. |
| **Environment Error** | `[ULTRAQA ERROR] {dependency/port/config issue}` |

### Observability

Output clear progress each cycle:

```
[ULTRAQA Cycle 1/5] Running tests...
[ULTRAQA Cycle 1/5] FAILED — 3 tests failing
[ULTRAQA Cycle 1/5] Diagnosing root cause...
[ULTRAQA Cycle 1/5] Fix: auth.test.ts — missing mock for UserService
[ULTRAQA Cycle 2/5] Running tests...
[ULTRAQA Cycle 2/5] PASSED — All 47 tests pass
[ULTRAQA COMPLETE] Goal met after 2 cycles
```

### Failure Tracking

Track each failure to detect patterns:
- Record the error signature (test name, error message, file:line)
- Compare with previous cycle failures
- If the same error signature appears 3 times → early exit with root cause analysis

### Important Rules

1. **Track failures** — record each failure signature to detect repeating patterns
2. **Early exit on pattern** — 3x same failure = stop and surface the root cause
3. **Clear output** — user should always know current cycle and status
4. **Minimal fixes** — fix the diagnosed issue only; do not refactor during QA cycling
5. **Respect bugfix-loop rule** — if no progress after the fix, question the approach rather than trying variations of the same fix

## Error Handling

- **Cannot determine the test/build/lint command**: Ask the user for the correct command before starting cycles.
- **Same failure 3 times**: Early exit with root cause analysis — do not keep trying the same approach. If the failure is non-deterministic or root cause remains unclear, delegate to `hypothesis-qa` for structured Observe → Hypothesize → Experiment → Conclude triage.
- **Environment issue (missing DB, port conflict)**: Exit immediately with `[ULTRAQA ERROR]` and the required setup action.
- **Architect diagnosis subagent fails**: Attempt a direct diagnosis from the error output; if insufficient, ask the user for guidance.
- **Fix introduces new failures**: Revert the fix, re-diagnose with both the original and new failures as context.

## When to Use

- Tests are failing and need iterative diagnosis + fix
- Build is broken and needs systematic repair
- Lint/typecheck errors need batch resolution
- CI pipeline is red and needs to be greened
- User wants autonomous "keep fixing until it works" behavior

## When NOT to Use

- Writing new tests from scratch — use qa-test-expert or test-suite
- Test strategy design — use qa-test-expert
- Single known bug with clear diagnosis — use diagnose directly
- Code review without fix intent — use simplify or deep-review

## Examples

<example>
User: "Make all tests pass"

[ULTRAQA Cycle 1/5] Running tests...
[ULTRAQA Cycle 1/5] FAILED — 5 tests failing:
  - test_auth_login: AssertionError (expected 200, got 401)
  - test_auth_refresh: ConnectionError (mock not configured)
  - test_user_create: ValidationError (missing field 'email')
  - test_user_update: same ValidationError
  - test_user_delete: TimeoutError

[ULTRAQA Cycle 1/5] Diagnosing...
  Root cause: Auth mock fixture was removed in recent refactor.
  3 user tests share a missing email validator import.
  Timeout is a test environment issue.

[ULTRAQA Cycle 1/5] Fixing:
  - Restored auth mock fixture in conftest.py
  - Added email validator import to user tests
  - Increased timeout for delete test

[ULTRAQA Cycle 2/5] Running tests...
[ULTRAQA Cycle 2/5] PASSED — All 23 tests pass

[ULTRAQA COMPLETE] Goal met after 2 cycles
</example>

<example>
User: "Fix the build"

[ULTRAQA Cycle 1/5] Running build...
[ULTRAQA Cycle 1/5] FAILED — TypeScript error: Cannot find module '@/utils/helpers'

[ULTRAQA Cycle 1/5] Diagnosing...
  Root cause: tsconfig paths alias '@/utils' doesn't match actual directory structure after reorganization.
  File was moved from src/utils/helpers.ts to src/shared/utils/helpers.ts.

[ULTRAQA Cycle 1/5] Fixing: Updated tsconfig paths and 4 import statements.

[ULTRAQA Cycle 2/5] Running build...
[ULTRAQA Cycle 2/5] PASSED — Build succeeded (exit 0)

[ULTRAQA COMPLETE] Goal met after 2 cycles
</example>

<example>
Same failure 3 times — early exit:

[ULTRAQA Cycle 3/5] FAILED — Same error: "Cannot connect to database"
[ULTRAQA STOPPED] Same failure detected 3 times.
Root cause: Test database container is not running. This is an environment issue, not a code issue.
Action needed: Start the test database with `docker compose up -d test-db`
</example>

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
