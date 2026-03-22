# sentence-polisher Autoimprove Changelog

## Baseline Score: 60% (3/5 evals passing)

### Round 1: Add before/after list to Change Summary format (KEPT ✅)
- **What:** Added `### Changes Applied` subsection to output format with numbered before→after pairs
- **Why:** EVAL 3 (change summary completeness) failed 3/3 — format only showed counts, not specifics
- **Impact:** EVAL 3 now passes. Score: 80%
- **Files changed:** Output format template, Example 1, Example 2

### Round 2: Mandatory Konglish detection (KEPT ✅)
- **What:** Added explicit "Konglish detection is MANDATORY" instruction and strengthened bilingual mode description
- **Why:** EVAL 1 (Konglish replacement) failed 2/3 — skill had Konglish in taxonomy but no hard mandate to always replace
- **Impact:** EVAL 1 now passes. Score: 100%
- **Files changed:** Korean-specific scan section, bilingual mode detection table

### Round 3: Add mixed-language example (KEPT ✅)
- **What:** Added Example 3 showing bilingual Korean-English Slack message with Konglish corrections
- **Why:** Skill had Korean-only and English-only examples but no mixed-language example, despite bilingual mode being a core feature
- **Impact:** Score stable at 100%. Adds coverage for the most common real-world usage pattern.
- **Files changed:** Examples section (new Example 3, renumbered pipeline example to Example 4)

### Round 4: Chunking consistency clarification (KEPT ✅)
- **What:** Specified "honorific level, tense, and terminology" as consistency dimensions for long-text chunking
- **Why:** Error handling table said "maintain cross-paragraph consistency" without specifying what to keep consistent
- **Impact:** Score stable at 100%. Prevents regression in long-text scenarios.
- **Files changed:** Error Handling table

## Final Score: 100% (5/5 evals passing)
## Improvement: +40 percentage points (60% → 100%)
