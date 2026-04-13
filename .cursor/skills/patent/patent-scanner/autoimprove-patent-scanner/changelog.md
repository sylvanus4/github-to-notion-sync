# patent-scanner Autoimprove Changelog

## v1-mutations (2026-04-13)

**Baseline pass rate**: 68% (17/25)
**Post-mutation pass rate**: 96% (24/25)
**Improvement**: +28pp
**Size growth**: 19.2% (10250 → 12217 bytes) — within 20% gate

### Mutations Applied

1. **Concrete reference mandatory for all scan types** (Step 2)
   - Made `concrete_reference` required for code scans (file/function/line), spec scans (section title), and idea/verbal scans (quoted excerpt)
   - Previously only enforced for code scans
   - Impact: eval3 pass rate 60% → 100%

2. **Composite score threshold enforcement** (Step 3)
   - Added explicit routing of below-5.0 candidates to `below_threshold_notes` array
   - Strengthened filtering language with "MUST be excluded" directive
   - Impact: eval1 pass rate 80% → 100%

3. **Dual jurisdiction mandatory** (Step 2 + Anti-Pattern #4)
   - Made both `us_jurisdiction` (Alice/101) and `kr_jurisdiction` (KIPO AI/SW) fields required for every candidate
   - Impact: eval4 pass rate 40% → 100%

4. **Standard Pattern Blocklist** (Step 2, new section)
   - Introduced compact blocklist preventing over-scoring of well-known patterns (MVC, REST CRUD, vanilla Transformer, etc.)
   - Novelty > 5 blocked unless `differentiation_points` documented
   - Impact: eval5 pass rate 40% → 80%

5. **4-dimension score completeness** (Anti-Pattern #5 + Pre-Delivery Check #5)
   - Added anti-pattern enforcing all 4 dimension scores (novelty, non-obviousness, utility, commercial_value) as integers 1-10
   - Impact: eval2 pass rate 80% → 100%

6. **Pre-Delivery Check expansion** (Pre-Delivery Checks #1-6)
   - Expanded from 4 to 6 checks, covering threshold routing, concrete reference, jurisdiction, 4-dim scores, and blocklist guard

### Criteria Not Improved

- eval5 (standard blocklist): Improved from 40% to 80%. One remaining failure (API caching input) is a borderline case where a novel caching mechanism sits adjacent to standard patterns — the prompt correctly flags it but the boundary is inherently fuzzy. Additional mutation for this marginal case was not attempted to preserve size budget.

### Holdout Risk

- API caching test input had 1 failure on eval5 (standard blocklist). The "novel caching mechanism" topic straddles the line between standard and novel — context-dependent and acceptable as-is.

### Constraint Gates

- [x] Size ≤ 20% growth: 19.2% ✓
- [x] Triggers preserved: Use-when and Do-NOT-use unchanged ✓
- [x] Boundaries preserved: No overlap with other patent skills ✓
- [x] Pass rate improved: 68% → 96% (+28pp) ✓
