---
name: simplification-cascade
description: >-
  Decompose convoluted "god functions" and tangled logic into smaller,
  composable pieces through a layered cascade — each pass targets one specific
  smell (deep nesting → extract, mixed concerns → split, implicit state → make
  explicit). Distinct from omc-ai-slop-cleaner (deletion-first AI slop
  cleanup) and simplify (parallel multi-agent review) — this skill applies a
  sequential, layer-by-layer decomposition where each cascade level has a
  single focus. Use when the user asks to "simplify this function", "break
  down god function", "simplification cascade", "decompose complex logic",
  "layered refactor", "god 함수 분해", "단계별 단순화", "중첩 제거", "관심사 분리", "복잡도 줄이기",
  "레이어별 리팩토링", or has a function/module exceeding 100 lines with deep nesting
  and mixed responsibilities. Do NOT use for deleting dead or duplicated
  AI-generated code (use omc-ai-slop-cleaner). Do NOT use for multi-domain
  parallel code review (use simplify or deep-review). Do NOT use for
  architecture-level restructuring (use improve-codebase-architecture). Do NOT
  use for code that is already clean but needs performance optimization (use
  performance-profiler).
---

# Simplification Cascade

Reduce complex code into smaller, composable pieces through sequential decomposition passes — each cascade level targets exactly one complexity smell.

## When to Use

- Functions exceeding 100 lines with 3+ levels of nesting
- Modules mixing data fetching, business logic, error handling, and UI rendering
- Legacy code where "nobody wants to touch it"
- Pre-refactor preparation: understand the structure before redesigning it

## When NOT to Use

- Removing dead code or AI-generated slop (use `omc-ai-slop-cleaner`)
- Multi-domain parallel code review (use `simplify` or `deep-review`)
- Full architecture redesign (use `improve-codebase-architecture`)
- Clean code that just needs performance tuning (use `performance-profiler`)

## Workflow

### Phase 1: Complexity Audit

1. Read the target function/module and measure:
   - **Line count**: Total lines of logic (excluding blank lines and comments)
   - **Max nesting depth**: Deepest level of indentation
   - **Cyclomatic complexity**: Count of independent paths (if/else, switch, loops, try/catch)
   - **Concern count**: Number of distinct responsibilities (fetch, validate, transform, render, log, etc.)
   - **Implicit state**: Variables mutated across multiple scopes
2. Record these metrics as the **Before Snapshot**
3. Identify which cascade levels apply (see Phase 2)

### Phase 2: Apply Cascade Levels

Execute levels sequentially. Each level has a single focus. After each level, verify tests still pass before proceeding.

#### Level 1: Flatten Deep Nesting (Guard Clauses)

- Convert nested `if/else` chains into early returns
- Replace `if (condition) { ...100 lines... }` with `if (!condition) return`
- Goal: Max nesting depth ≤ 2

#### Level 2: Extract Pure Functions

- Identify blocks of code that take inputs and produce outputs without side effects
- Extract each into a named function with clear parameters and return type
- Goal: Each extracted function ≤ 20 lines

#### Level 3: Separate Concerns

- Split the remaining function by responsibility:
  - Data fetching → separate function/module
  - Validation → separate function
  - Transformation → separate function
  - Side effects (DB writes, API calls, logging) → separate function
- Goal: Each function does exactly one thing

#### Level 4: Make Implicit State Explicit

- Replace mutable variables shared across scopes with:
  - Function parameters (pass data in)
  - Return values (pass data out)
  - Explicit state objects (named, typed)
- Eliminate closure-captured mutation
- Goal: No variable is mutated in more than one function

#### Level 5: Name and Document the Pipeline

- Compose the extracted functions into a readable pipeline:
  ```
  const result = pipe(
    validate(input),
    transform,
    enrich,
    persist
  )
  ```
- Or use clear sequential calls with descriptive variable names
- Add a one-line comment above each call explaining "why", not "what"
- Goal: The top-level function reads like a table of contents

### Phase 3: After Snapshot

1. Re-measure all metrics from Phase 1
2. Produce a comparison table:

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Line count | 287 | 42 (top) + 5×25 (helpers) | -43% top-level |
| Max nesting | 6 | 2 | -4 levels |
| Cyclomatic complexity | 23 | 5 (top) | -78% |
| Concern count | 5 | 1 per function | ✓ |
| Implicit state vars | 8 | 0 | ✓ |

3. Verify all tests pass with the refactored code

## Gotchas

1. **Skipping the test verification between cascade levels.** If you extract a function in Level 2 and introduce a bug, but don't test until Level 5, you won't know which level broke it. Run tests after every level.
2. **Extracting too aggressively.** A 3-line helper function that's only called once adds indirection without value. Extract when the block has a clear name and is ≥ 5 lines or is called from multiple places.
3. **Renaming during the cascade.** Resist the urge to rename variables/functions mid-cascade. Renaming changes should be a separate commit to keep the refactoring diff clean and reviewable.
4. **Forgetting to update call sites.** After extracting a function, search for all call sites of the original code path. Grep for the function name and verify every caller passes the right arguments.

## Verification

After completing the cascade:
1. Run the full test suite — zero regressions
2. Verify the After Snapshot metrics show improvement in every dimension
3. Confirm max nesting depth is ≤ 2 in the refactored code
4. Check that no extracted function exceeds 30 lines
5. Ensure no variable is mutated across function boundaries

## Anti-Example

```
# BAD: Applying all levels simultaneously
"I'll just rewrite the whole function from scratch"
→ This is not a cascade. You lose traceability and introduce risk.
  Apply one level at a time with test verification between each.

# BAD: Extracting a 2-line block into its own function
const isValid = (x) => x != null && x.length > 0;
→ Inline this. It adds indirection without meaningful abstraction.

# BAD: Mixing renaming with structural changes
// In the same commit: extract function AND rename 'data' to 'userProfile'
→ Separate commits. Structural changes in one, renames in another.
```

## Constraints

- Never apply more than one cascade level without running tests between them
- Each extracted function must be ≤ 30 lines
- The final top-level function should read as a pipeline / table of contents
- Do NOT rename variables during structural cascade levels — renaming is a separate pass
- Do NOT rewrite from scratch — cascade is incremental by definition
- Freedom level: **Rigid** — follow the 5 levels in order; skip a level only if the audit confirms it doesn't apply

## Output

1. Before Snapshot (metrics table)
2. Per-level diff summary (what was extracted/changed at each level)
3. After Snapshot (metrics table)
4. Comparison table (before vs after)
5. Refactored code committed in per-level increments
