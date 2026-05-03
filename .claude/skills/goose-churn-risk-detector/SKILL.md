---
name: goose-churn-risk-detector
description: >-
  Analyze a SaaS product and its ICP to identify the most likely churn risks —
  grouped by activation failure, value realization gaps, competitive
  displacement, and expansion blockers. Produces a risk matrix with severity
  scoring and prescriptive retention plays for each risk. Pure reasoning
  skill.
---

# Goose Churn Risk Detector

Analyze a SaaS product and its ICP to identify the most likely churn risks — grouped by activation failure, value realization gaps, competitive displacement, and expansion blockers. Produces a risk matrix with severity scoring and prescriptive retention plays for each risk. Pure reasoning skill.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/churn-risk-detector.

## When to Use

- "What are the biggest churn risks for our product?"
- "Analyze churn risk patterns"
- "이탈 위험 분석", "SaaS 이탈 리스크 감지"
- "Build a churn prevention playbook"

## Do NOT Use

- For general customer feedback analysis (use customer-feedback-processor)
- For cohort retention analysis (use pm-data-analytics)
- For customer win-back sequences (use goose-customer-win-back-sequencer)

## Methodology

### Risk Category 1: Activation Failure
- Time-to-value too long
- Onboarding drop-off points
- Feature discovery gaps
- Integration/setup friction

### Risk Category 2: Value Realization Gaps
- Core use case not being achieved
- Usage pattern decline (frequency, depth, breadth)
- Feature adoption plateau
- ROI not measurable or visible

### Risk Category 3: Competitive Displacement
- Competitor feature parity or superiority
- Pricing pressure from alternatives
- Platform consolidation (customer reducing vendor count)
- Open-source alternatives emerging

### Risk Category 4: Expansion Blockers
- Team adoption ceiling (single user, no virality)
- Upgrade path unclear or overpriced
- Missing features for next segment (SMB → Mid-Market)
- Champion departure risk

### Severity Scoring
Each risk scored on:
- **Likelihood** (1-5): how probable based on product/market
- **Impact** (1-5): revenue impact if materialized
- **Detectability** (1-5): how easily you can spot it early
- **Risk Score** = Likelihood × Impact × (6 - Detectability)

### Retention Plays
For each high-severity risk, prescribe:
- Early warning signal to monitor
- Intervention trigger (when to act)
- Retention play (specific action)
- Owner (CS, Product, Marketing, Sales)

## Output: Churn Risk Matrix with severity scores and retention playbook
