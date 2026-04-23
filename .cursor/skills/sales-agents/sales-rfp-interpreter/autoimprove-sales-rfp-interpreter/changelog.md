# sales-rfp-interpreter Autoimprove Changelog

## Round 1: Bilingual Extraction & KB Fallback
- **Step 2 — Extract Requirements**: Added primary language detection, bilingual (Korean+English) extraction with deduplication, Korean priority signals (필수/권장/선택), Korean honorific hedging default-to-unclear rule, and KB lookup empty-result fallback
- **Composite score**: 7.2 → 8.4 (+1.2)
- **Accepted**: Yes — all 4 improving dimensions passed constraint gates

## Round 2: Constraint Gates (from audit-optimize phase)
- Added `## Constraints`, `## Gotchas`, `## Verification` sections
- 30-requirement cap, source-citation mandate for risk flags, downstream hand-off prohibition
- **Composite score**: 8.4 → 8.6 (+0.2)
- **Accepted**: Yes — completeness and safety improved

## Round 3: Skipped
- Convergence reached at composite 8.6/10 (threshold: 8.0)
- No further mutations needed

## Final Score: 8.6/10
