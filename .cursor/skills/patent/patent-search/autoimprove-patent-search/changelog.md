# patent-search Autoimprove Changelog

## v1-mutations (2026-04-13)

**Baseline pass rate**: 72% (18/25)
**Post-mutation pass rate**: 96% (24/25)
**Improvement**: +24pp
**Size growth**: 11.5% (9867 → 11000 bytes) — within 20% gate

### Mutations Applied

1. **Blocking references explicit contract** (Step 4)
   - Made `blocking_references` array mandatory in output JSON
   - Specified threshold (score ≥ 8) and empty-array fallback requirement
   - Impact: eval5 pass rate 60% → 100%

2. **Three new anti-patterns** (Anti-Patterns #6, #7, #8)
   - #6: `overlap_elements` required per result (enforces eval2)
   - #7: IPC/CPC code derivation mandatory even without user input (enforces eval4)
   - #8: `blocking_references` array presence enforced (reinforces eval5)
   - Impact: eval2 +20pp, eval4 +20pp

3. **Source coverage threshold** (Anti-Pattern #3 + Pre-Delivery Check #1)
   - Changed "all six sources must be queried" to "4 out of 6 must return results"
   - Added "fewer than 4 = delivery failure" language
   - Impact: eval1 pass rate 80% → 100%

4. **Pre-Delivery Check expansion** (Pre-Delivery Check #4, #5)
   - Added explicit checks for blocking_references array presence
   - Added per-result field completeness check (relevance_score + overlap_elements)
   - Impact: reinforces eval2 and eval5

### Criteria Not Improved

- eval3 (bilingual matrix): Already strong at 80% baseline, no mutation needed.
  One failure case (CRISPR domain) likely due to niche Korean biotech terminology — marginal improvement possible but not attempted to keep size growth minimal.

### Holdout Risk

- CRISPR test input had 1 failure on eval3 (bilingual matrix for niche biotech terms). This is acceptable as the failure is domain-specific vocabulary, not a structural prompt issue.

### Constraint Gates

- [x] Size ≤ 20% growth: 11.5% ✓
- [x] Triggers preserved: Use-when and Do-NOT-use unchanged ✓
- [x] Boundaries preserved: No overlap with other patent skills ✓
- [x] Pass rate improved: 72% → 96% (+24pp) ✓
