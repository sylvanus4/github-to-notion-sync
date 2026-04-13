# patent-us-review Autoimprove Changelog

## Summary
- **Baseline pass rate**: 60%
- **v1-mutations pass rate**: 96%
- **Improvement**: +36%p
- **Size growth**: 10741 → 12721 bytes (18.4%, within 20% gate)
- **Mutations applied**: 5

## Mutations

### M1: Alice Completeness Gate (EVAL 1)
- **Target**: Step 2 (35 USC 101 analysis)
- **Change**: Added mandatory "Alice Completeness Gate" requiring explicit enumeration of all independent claims with confirmed 2A/2B analysis completion before proceeding to Step 3
- **Rationale**: Prevents incomplete Alice analysis by enforcing a checklist before moving forward

### M2: CRITICAL Issue Completeness Rule (EVAL 2)
- **Target**: Step 7 (Severity-Ranked Issue List)
- **Change**: Added "CRITICAL Issue Completeness Rule" requiring every CRITICAL-severity row to contain: (1) specific statutory basis, (2) concrete example citing claim language, (3) actionable fix suggestion
- **Rationale**: Eliminates vague CRITICAL findings that lack actionable remediation guidance

### M3: Scorecard Completeness Gate (EVAL 3)
- **Target**: Step 8 (Claim-by-Claim Scorecard)
- **Change**: Added "Scorecard Completeness Gate" mandating exactly N rows for N claims, with N/A marking for un-evaluable columns rather than row omission
- **Rationale**: Ensures no claim is silently skipped in the per-claim grading

### M4: 112(f) Trigger Expression Scan List (EVAL 4)
- **Target**: Step 5 (35 USC 112 analysis)
- **Change**: Expanded the 112(f) Interpretation Check with an explicit list of trigger expressions ("configured to", "adapted to", "operable to", "module for", "mechanism for", "unit for", nonce word patterns) and mandatory "No trigger found" statement when clean
- **Rationale**: Prevents silent skip of 112(f) analysis by providing a concrete checklist of expressions to scan for

### M5: Anti-Software-Bias Self-Check (EVAL 5)
- **Target**: Step 2 (35 USC 101 analysis), after Alice Completeness Gate
- **Change**: Added "Anti-Software-Bias Self-Check" requiring re-evaluation of Medium/High risk ratings against Anti-Pattern #1 to confirm ratings are based on full 2A/2B analysis, not mere software classification
- **Rationale**: Prevents premature 101 failure for software inventions that have legitimate practical applications
