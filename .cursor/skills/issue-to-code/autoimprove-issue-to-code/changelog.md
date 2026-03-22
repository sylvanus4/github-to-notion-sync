# issue-to-code Autoimprove Changelog

## Baseline Score: 80% (4/5 evals passing)

### Round 1: File existence validation mandate (KEPT ✅)
- **What:** Added "Verify every file path exists using Glob or Read before including in the plan — never reference made-up paths" to Step 3
- **Why:** EVAL 1 (reference specific real files) failed — skill searched for files but never explicitly mandated verifying they exist
- **Impact:** EVAL 1 now passes. Score: 100%
- **Files changed:** Step 3 item 1

### Round 2: Duplicate PR detection (KEPT ✅)
- **What:** Added instruction to check for existing open PRs referencing the issue before creating a new one
- **Why:** Without this check, the skill could create duplicate PRs for issues already being worked on
- **Impact:** Score stable at 100%. Prevents wasted effort.
- **Files changed:** Step 1 linked issues extraction

### Round 3: Test convention matching (KEPT ✅)
- **What:** Specified that tests must follow "same directory/naming pattern as existing tests discovered in Step 3"
- **Why:** Generic "write tests" instruction could lead to tests in wrong locations or with wrong naming
- **Impact:** Score stable at 100%. Ensures test discoverability.
- **Files changed:** Step 6 test instruction

### Round 4: Interface modification safety gate (KEPT ✅)
- **What:** Added guardrail to pause and flag for user approval if implementation requires modifying shared interfaces, types, or API contracts
- **Why:** Automated code generation modifying shared contracts can cascade breakage across the codebase
- **Impact:** Score stable at 100%. Aligns with observability.mdc "Stop if Suspicious" rule.
- **Files changed:** Guardrails section (new bullet)

## Final Score: 100% (5/5 evals passing)
## Improvement: +20 percentage points (80% → 100%)
