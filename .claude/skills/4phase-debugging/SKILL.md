---
name: 4phase-debugging
description: >-
  Systematic 4-phase sequential debugging methodology that forbids random
  "just try changing stuff" edits — Reproduce (create smallest failing test),
  Narrow (isolate root cause via binary search), Fix (apply single minimal
  change), Verify (confirm fix + no regressions). Distinct from diagnose (3
  parallel analysis agents for fast triage) and hypothesis-investigation
  (scientific-method loop for non-trivial bugs) — this skill enforces a strict
  sequential discipline where each phase gates the next. Use when the user
  asks to "debug systematically", "4-phase debug", "stop guessing and debug
  properly", "sequential debugging", "reproduce then fix", "체계적 디버깅", "4단계
  디버깅", "재현부터 수정까지", "순차 디버깅", "찍어보지 말고 디버깅", "reproduce first", "smallest
  failing test", or has a bug where previous fix attempts failed because the
  root cause wasn't properly isolated. Do NOT use for fast parallel diagnosis
  of production incidents (use diagnose). Do NOT use for complex bugs
  requiring hypothesis generation and evidence persistence (use
  hypothesis-investigation). Do NOT use for code review without a specific bug
  (use deep-review or simplify). Do NOT use for flaky test investigation (use
  hypothesis-qa). Do NOT use for performance profiling (use
  performance-profiler).
---

# 4-Phase Systematic Debugging

A strict sequential debugging methodology: Reproduce → Narrow → Fix → Verify. Each phase must complete before the next begins. No guessing. No shotgun edits. No "let me just try this real quick."

## When to Use

- A bug report arrives and you need a disciplined approach
- Previous fix attempts failed because the root cause wasn't isolated
- The bug is reproducible but the cause is unclear
- You want to guarantee no regressions from the fix
- Training yourself or others out of "change stuff and see" debugging habits

## When NOT to Use

- Production incident requiring fast parallel triage (use `diagnose`)
- Complex non-trivial bugs needing hypothesis trees and evidence logs (use `hypothesis-investigation`)
- Flaky tests that fail intermittently (use `hypothesis-qa`)
- Code review without a specific bug to fix (use `deep-review`)
- Performance regressions requiring profiling (use `performance-profiler`)

## The Iron Rules

Before starting, internalize these:

1. **No fix attempt before Phase 2 (Narrow) is complete.** If you don't know the root cause, any "fix" is a guess.
2. **One change at a time.** Multi-change commits mask which change actually fixed the bug.
3. **Every fix must have a test.** If it's not tested, it's not fixed — it's deferred.
4. **The smallest reproduction wins.** A 3-line failing test is worth more than a 50-step manual reproduction.

## Workflow

### Phase 1: Reproduce

**Goal**: Create the smallest possible reproduction that consistently triggers the bug.

1. **Understand the report**:
   - What is the expected behavior?
   - What is the actual behavior?
   - What environment/inputs trigger it?
2. **Reproduce manually first**:
   - Follow the exact steps from the bug report
   - If it doesn't reproduce, identify missing context (environment, data state, timing)
3. **Create an automated reproduction**:
   - Write a failing test that captures the bug
   - If the full scenario is complex, isolate the failing behavior:
     ```
     Original: 50-step user flow → failure at step 47
     Reduced:  3-line unit test → same failure
     ```
4. **Minimize the reproduction**:
   - Remove irrelevant setup, data, and code paths
   - The ideal reproduction has zero unnecessary lines
5. **Confirm reliability**: Run the failing test 3 times — it must fail every time

**Phase 1 Gate**: You have a reliable, minimal failing test. If you cannot reproduce, STOP and gather more information. Do not proceed.

### Phase 2: Narrow

**Goal**: Identify the exact line(s) of code responsible for the bug.

1. **Form initial hypotheses** (list 2-5 possible causes):
   - Data issue? Logic error? Race condition? Missing validation? Wrong assumption?
2. **Binary search the cause**:
   - If the bug is in a pipeline/flow: add logging at midpoints to determine which half contains the bug
   - If the bug is in a function: comment out halves to isolate the faulty block
   - If the bug is in recent changes: `git bisect` to find the introducing commit
3. **Read the code around the suspected area**:
   - Don't just read the failing line — read 50 lines of context above and below
   - Check the function's callers and callees
   - Look for implicit assumptions (null checks, type coercions, default values)
4. **Confirm the root cause**:
   - You should be able to state: "The bug is caused by [specific mechanism] at [specific location]"
   - If your explanation has the word "maybe" or "probably", you haven't narrowed enough

**Phase 2 Gate**: You can explain the root cause in one clear sentence without uncertainty. If not, continue narrowing.

### Phase 3: Fix

**Goal**: Apply the minimum change that addresses the root cause.

1. **Design the fix before writing code**:
   - State what the fix changes and why
   - Predict: what was broken before → what will be correct after
   - Consider edge cases the fix might introduce
2. **Apply a single, minimal change**:
   - The ideal fix touches 1-5 lines
   - If your fix requires >20 lines, question whether you're addressing a symptom or the cause
   - Do NOT refactor, rename, or clean up surrounding code in the same change
3. **Write the fix in a separate commit from any cleanup**:
   - Bug fix = one commit
   - Cleanup/refactor = separate commit (if needed)

**Phase 3 Gate**: Your fix is committed. It touches the minimum number of lines to address the root cause.

### Phase 4: Verify

**Goal**: Confirm the fix works and causes no regressions.

1. **Run the reproduction test**: The previously failing test must now pass
2. **Run the full test suite**: Zero regressions
   - If any other test breaks, your fix has side effects — return to Phase 2
3. **Manual verification** (if applicable):
   - Follow the original bug report steps — the bug no longer occurs
4. **Edge case verification**:
   - Test boundary inputs related to the fix
   - Test the "opposite" of the bug condition
5. **Document the fix**:
   - In the commit message or PR description:
     - Root cause (one sentence)
     - Fix applied (one sentence)
     - How verified (test names or manual steps)

**Phase 4 Gate**: All tests pass. The reproduction test passes. The fix is documented.

## Gotchas

1. **Skipping Phase 1 because "I think I know what's wrong."** You probably don't. 70% of bugs have a different root cause than the initial guess. Reproduce first, always.
2. **Fixing symptoms instead of root causes.** Adding a null check that prevents a crash without understanding WHY the value is null. The null check masks the real bug, which will resurface later.
3. **Making multiple changes in Phase 3.** If you fix the bug AND refactor AND rename a variable in one commit, and a new bug appears tomorrow, you won't know which change caused it. One fix per commit.
4. **Declaring victory without running the full test suite.** Your fix might pass the specific reproduction test but break 3 other tests. Phase 4 requires the FULL suite, not just the one test.

## Verification

After completing all 4 phases:
1. The failing test from Phase 1 now passes
2. The full test suite passes with zero regressions
3. The commit message includes root cause and fix description
4. The fix touches ≤ 20 lines of logic (if more, justify why)
5. No unrelated changes are mixed into the fix commit

## Anti-Example

```
# BAD: Skip reproduction, jump to fix
"I bet it's a null pointer — let me add a null check"
→ You haven't reproduced it. You don't know if it's null, undefined, wrong type, or stale cache.
  Write a failing test first.

# BAD: Multi-change fix commit
commit message: "Fix login bug, also refactor auth module and update deps"
→ Three changes in one commit. If auth breaks tomorrow, was it the fix, the refactor, or the dep update?
  Separate commits.

# BAD: Phase 2 with "probably"
"The bug is probably caused by the race condition in the event handler"
→ "Probably" means you haven't narrowed. Add logging, use git bisect, or binary search the code path.
  No Phase 3 until you can remove the word "probably."

# BAD: Passing one test = verified
"My reproduction test passes now, ship it!"
→ Run the full suite. Your fix might break 5 other tests.
```

## Constraints

- Phase gates are mandatory — do not skip to a later phase
- Phase 1 MUST produce a reliable automated failing test (manual-only reproduction is insufficient)
- Phase 2 MUST end with a root cause statement that contains no uncertainty words ("maybe", "probably", "might")
- Phase 3 fix MUST be a separate commit from any cleanup or refactoring
- Phase 4 MUST include a full test suite run, not just the reproduction test
- Do NOT apply more than one logical change per fix commit
- Freedom level: **Rigid** — the 4 phases are sequential and non-negotiable; you may adapt the specific techniques within each phase

## Output

1. Reproduction: Failing test (file path and test name)
2. Root cause: One-sentence explanation with code location
3. Fix: Diff of the change applied
4. Verification: Full test suite results + reproduction test result
5. Documentation: Commit message with root cause, fix, and verification summary
