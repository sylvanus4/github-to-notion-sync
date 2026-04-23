# sales-partner-orchestrator Autoimprove Changelog

## Round 1: Bilingual Commitment Extraction
- **Step 2 — Extract Commitments**: Added Korean+English dual extraction with semantic deduplication, firm-vs-tentative commitment classification (high-confidence firm commitments vs. tentative intent requiring human confirmation), ambiguous owner flagging for "we/우리" pronouns, no arbitrary deadline inference (null + flag for human assignment)
- **Composite score**: 6.8 → 8.4 (+1.6) — largest improvement across all 5 skills
- **Accepted**: Yes — robustness 5→8, safety 7→9

## Round 2: Constraint Gates (from audit-optimize phase)
- Added `## Constraints`, `## Gotchas`, `## Verification` sections
- Email thread context loss gotcha, partner name spelling variation detection, dedup threshold guidance
- **Composite score**: 8.4 → 8.8 (+0.4)
- **Accepted**: Yes

## Round 3: Skipped
- Convergence at 8.8/10

## Final Score: 8.8/10
