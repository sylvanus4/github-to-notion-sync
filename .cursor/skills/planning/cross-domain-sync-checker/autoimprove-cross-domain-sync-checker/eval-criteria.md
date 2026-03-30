# Eval Criteria: cross-domain-sync-checker

## Binary Evals

EVAL 1: Multi-Domain Coverage
Question: Does the report cover at least 3 domains (e.g., PRD/spec, design/Figma, code, policy)?
Pass condition: Analysis spans 3+ domains with specific findings per domain pair
Fail condition: Only covers 1-2 domains or doesn't compare cross-domain alignment

EVAL 2: Weighted Score Present
Question: Does the report include a weighted sync score with the defined formula (30/25/25/20)?
Pass condition: Numeric score calculated using the 4-axis weighting, with per-axis breakdowns
Fail condition: No numeric score, or a score without the specified weighting breakdown

EVAL 3: Verdict Classification
Question: Is every comparison pair assigned a verdict (Match/Partial/Mismatch/Missing/Extra)?
Pass condition: Each cross-domain comparison has one of the 5 defined verdict types
Fail condition: Comparisons described without using the standardized verdict labels

EVAL 4: Action Items Per Team
Question: Does the output include team-specific action items (not just generic "fix this")?
Pass condition: Action items specify which team (planning/design/dev) owns each fix
Fail condition: Action items not attributed to specific teams

## Test Scenarios

1. "기획 디자인 개발 간 싱크 상태를 점검해줘"
2. "Check if the PRD matches the current Figma designs and code implementation"
3. "정책-디자인-코드 정합성을 크로스체크해줘"
4. "Run a full cross-domain sync check for the billing feature"
