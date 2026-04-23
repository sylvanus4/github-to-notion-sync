# sales-security-qa Autoimprove Changelog

## Round 1: Bilingual Q&A Parsing & KB Fallback
- **Step 1 — Classify the Question**: Added Korean security terminology extraction (개인정보, 망분리, 접근통제), Korean segment detection signals (공공/금융/enterprise), ask-user rule for ambiguous segments
- **Step 2 — Policy Knowledge Lookup**: Added KB empty-result fallback (0.5 max confidence, requires-confirmation classification, mandatory security team verification note)
- **Composite score**: 7.2 → 8.4 (+1.2)
- **Accepted**: Yes — robustness improved from 5→8

## Round 2: Constraint Gates (from audit-optimize phase)
- Added `## Constraints`, `## Gotchas`, `## Verification` sections
- Version-pinned policy doc gotcha, segment misidentification warning, confidence score calibration guide
- **Composite score**: 8.4 → 8.8 (+0.4)
- **Accepted**: Yes — completeness and robustness improved

## Round 3: Skipped
- Convergence reached at 8.8/10

## Final Score: 8.8/10
