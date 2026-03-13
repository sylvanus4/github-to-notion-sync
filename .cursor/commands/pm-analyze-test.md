---
description: Analyze A/B test results with statistical rigor — significance, sample size validation, ship/extend/stop recommendation.
argument-hint: "<control metric> | <variant metric> | <sample size> | <duration>"
---

# PM Analyze Test

Analyze A/B test results with statistical rigor — significance, sample size validation, and ship/extend/stop recommendation. References pm-data-analytics skill, ab-test-analysis sub-skill. Includes design validation, practical significance, and business impact estimation.

## Usage

```
/pm-analyze-test Checkout test: control 4.2%, variant 4.8%, 50k per arm, 2 weeks — ship?
/pm-analyze-test 체크아웃 A/B 테스트: 대조 4.2%, 변형 4.8%, 2주 — 출시해도 될까?
```

## Workflow

### Step 1: Load skill and reference

Read the `pm-data-analytics` skill (`.cursor/skills/pm-data-analytics/SKILL.md`) and `references/ab-test-analysis.md`.

### Step 2: Collect test parameters

Extract or request:

- Control and variant metric values (e.g., conversion rates)
- Sample size per arm (or total traffic)
- Test duration
- Primary metric and any secondary metrics
- Business context (revenue impact, risk tolerance)

### Step 3: Validate design

- Check if sample size was adequate (power, MDE)
- Identify potential confounds (seasonality, external events)
- Flag design issues (early stopping, metric pollution)

### Step 4: Run statistical analysis

- Compute p-value and confidence intervals
- Calculate lift and practical significance (e.g., minimum detectable effect)
- Assess business impact (revenue, users affected)
- Apply decision framework: Ship / Extend / Stop

### Step 5: Output

Deliver:

1. Summary table (control, variant, lift, p-value, CI)
2. Recommendation (Ship / Extend / Stop) with reasoning
3. Sample size validation note
4. Practical significance assessment
5. Next steps (rollout plan, follow-up tests)

## Notes

- p < 0.05 is convention; consider multiple comparisons if many metrics.
- "Extend" when underpowered or inconclusive; avoid stopping early.
- Always weigh statistical vs practical significance (e.g., 0.1% lift with 1B users).
