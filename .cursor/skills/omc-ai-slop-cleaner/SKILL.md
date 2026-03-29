---
name: omc-ai-slop-cleaner
description: >-
  Clean AI-generated code slop with a regression-safe, deletion-first,
  smell-classified pass-by-pass workflow. Preserves behavior while removing
  duplication, dead code, needless abstractions, and boundary violations.
  Supports scoped file lists and reviewer-only mode (--review). Use when the
  user asks to "clean AI slop", "deslop", "anti-slop", "remove AI code smell",
  "clean up AI-generated code", "simplify bloated code", "remove dead code",
  "consolidate duplicates", "AI 코드 정리", "AI 슬롭 제거", "코드 슬롭 정리",
  "중복 제거", "죽은 코드 삭제", "불필요한 추상화 제거", or wants regression-safe
  cleanup of code that works but feels bloated, repetitive, or over-abstracted.
  Do NOT use for new feature builds or product changes. Do NOT use for broad
  redesigns (use deep-review).   Do NOT use for formatting-only cleanup (use
  linters). Do NOT use when behavior is unclear and cannot be protected with
  tests.
metadata:
  author: "oh-my-claudecode"
  version: "1.0.0"
  category: "code-quality"
---

# AI Slop Cleaner: Regression-Safe Code Cleanup

Adapted from [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) ai-slop-cleaner skill. Implements smell-classified, pass-by-pass code cleanup with behavior preservation.

## Instructions

### Execution Posture

- **Preserve behavior** unless the user explicitly asks for behavior changes
- **Lock behavior** with focused regression tests first whenever practical
- **Write a cleanup plan** before editing code
- **Prefer deletion** over addition
- **Reuse existing** utilities and patterns before introducing new ones
- **Avoid new dependencies** unless explicitly requested
- **Keep diffs small**, reversible, and smell-focused

### Step 1: Protect Current Behavior

Before editing any code:

1. Identify what must stay the same (public APIs, user-facing behavior, data contracts).
2. Add or run the narrowest regression tests needed to lock that behavior.
3. If tests cannot come first, record the verification plan explicitly before touching code.

Use a `Task` subagent (`subagent_type="generalPurpose"`, `model="fast"`) to identify existing test coverage for the target files.

### Step 2: Write a Cleanup Plan

Before editing code, produce a structured plan:

1. **Bound the scope** to the requested files or feature area.
2. **List concrete smells** to remove (see classification below).
3. **Order work** from safest deletion to riskier consolidation.

### Step 3: Classify the Slop

Categorize each issue into one of these smell types:

| Smell | Description | Examples |
|-------|-------------|---------|
| **Duplication** | Repeated logic, copy-paste branches, redundant helpers | Same validation in 3 places, near-identical handlers |
| **Dead code** | Unused code, unreachable branches, stale flags, debug leftovers | Commented-out blocks, unused imports, feature flags for shipped features |
| **Needless abstraction** | Pass-through wrappers, speculative indirection, single-use helper layers | `createUserWrapper()` that just calls `createUser()`, one-use utility classes |
| **Boundary violations** | Hidden coupling, misplaced responsibilities, wrong-layer imports | UI components making DB calls, services importing from presentation layer |
| **Missing tests** | Behavior not locked, weak regression coverage, edge-case gaps | Core business logic without unit tests, error paths untested |

### Step 4: Run One Smell-Focused Pass at a Time

Execute passes in this order:

1. **Pass 1: Dead code deletion** — safest, highest signal-to-noise improvement
2. **Pass 2: Duplicate removal** — consolidate repeated logic into shared utilities
3. **Pass 3: Naming and error-handling cleanup** — improve clarity without changing structure
4. **Pass 4: Test reinforcement** — add missing tests for preserved behavior

After each pass:
- Re-run targeted verification (tests, lint, typecheck)
- Do NOT bundle unrelated refactors into the same edit set

### Step 5: Quality Gates

After all passes:
- Keep regression tests green
- Run the relevant lint, typecheck, and unit/integration tests for touched area
- Run existing static or security checks when available
- If a gate fails, fix the issue or back out the risky cleanup

### Step 6: Evidence-Dense Report

Always close with:

```
## Cleanup Report

**Changed files:** [list]
**Simplifications:**
- [what was removed/consolidated and why]
**Behavior lock / verification:**
- [tests run, results]
**Remaining risks:**
- [anything still concerning]
**Lines removed:** {n} | **Lines added:** {n} | **Net:** {delta}
```

### Review Mode

When invoked with `--review` intent (e.g., "review the slop cleanup", "check the cleanup"):

1. Do **NOT** edit files.
2. Review the cleanup plan, changed files, and regression coverage.
3. Check for:
   - Leftover dead code or unused exports
   - Duplicate logic that should have been consolidated
   - Needless wrappers or abstractions that still blur boundaries
   - Missing tests for preserved behavior
   - Cleanup that appears to have changed behavior without intent
4. Produce a reviewer verdict with required follow-ups.
5. Hand needed changes back to a separate writer pass.

### Scoped File-List Usage

This skill can be bounded to an explicit file list:

- **Good:** `omc-ai-slop-cleaner src/auth/login.ts src/auth/register.ts`
- **Good:** Run on only the files changed in a recent session
- Preserve the same regression-safe workflow even when scope is a short file list
- Do NOT silently expand scope beyond the specified files

## Error Handling

- **No existing tests for target files**: Write minimal regression tests first, or record explicit verification steps before editing.
- **Test suite fails after a cleanup pass**: Revert the pass that broke tests, then re-attempt with a smaller scope.
- **Cannot determine if code is dead**: Mark as "potentially dead" in the report rather than deleting — let the user decide.
- **Scope is too large to clean in one session**: Prioritize by smell severity (dead code first), report remaining work.
- **Lint/typecheck commands not found**: Skip that gate and note it in the report.

## When to Use

- Code works but feels bloated, repetitive, or over-abstracted
- Follow-up implementation left duplicate logic, dead code, or wrapper layers
- User wants a bounded cleanup pass without behavior changes
- Post-implementation cleanup of AI-generated code

## When NOT to Use

- New feature build or product change — execute the feature directly
- Broad redesign — use deep-review for multi-domain analysis
- Formatting-only cleanup — use linters directly
- Behavior is too unclear to protect with tests — clarify first

## Examples

<example>
User: "Clean up the AI slop in src/services/auth/"

Step 1 — Behavior lock:
- Found 12 existing tests for auth module, all passing
- Added 3 edge-case tests for token refresh flow (previously untested)

Step 2 — Cleanup plan:
- Pass 1: Remove 3 dead utility functions (unused since v2.0 migration)
- Pass 2: Consolidate duplicate validation in login/register handlers
- Pass 3: Rename ambiguous `handleAuth()` to `authenticateWithProvider()`
- Pass 4: Add missing test for error path in token rotation

Step 3 — Classification:
- Dead code: `legacyHashPassword()`, `oldSessionCleanup()`, `debugAuthLog()`
- Duplication: Email validation duplicated in login.ts:45 and register.ts:23
- Needless abstraction: `AuthServiceWrapper` just proxies to `AuthService`

[Executes passes 1-4 with verification after each]

## Cleanup Report
**Changed files:** auth/login.ts, auth/register.ts, auth/utils.ts, auth/wrapper.ts (deleted)
**Simplifications:**
- Removed 3 dead functions (67 lines)
- Consolidated email validation into shared util (saved 23 lines)
- Removed AuthServiceWrapper pass-through (saved 41 lines)
**Behavior lock:** 15/15 tests passing (12 existing + 3 new)
**Remaining risks:** None — all changes are deletion or consolidation
**Lines removed:** 131 | **Lines added:** 14 | **Net:** -117
</example>

<example>
User: "Review the cleanup I did on the data pipeline"

[Review mode — no edits]

## Reviewer Verdict: NEEDS WORK

**Leftover issues:**
1. `transformData()` in pipeline.ts:89 is now unused after consolidation but wasn't deleted
2. Duplicate retry logic remains in fetcher.ts:23 and fetcher.ts:67 (only fetcher.ts:112 was consolidated)
3. Missing test: the error path in `processChunk()` lost coverage when `chunkHelper()` was removed

**Required follow-ups:**
- Delete unused `transformData()`
- Consolidate remaining retry logic
- Add test for `processChunk()` error path
</example>
