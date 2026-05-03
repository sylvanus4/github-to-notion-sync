---
name: pm-data-analytics
description: PM data analytics — SQL query generation, cohort analysis, A/B test analysis with statistical significance.
arguments: [workflow, question]
---

Run data analytics workflow `$workflow` for `$question`.

## Workflows

| Workflow | Description |
|----------|-------------|
| sql | Generate SQL from natural language question |
| cohort | Retention or feature adoption cohort analysis |
| ab-test | A/B test result analysis with statistical significance |

## SQL Generation

- Infer table/column names from context
- Include CTEs for readability
- Add comments explaining logic
- Validate against known schema if available

## Cohort Analysis

- Time-based or behavior-based cohorts
- Retention curves with week-over-week breakdown
- Feature adoption by cohort segment

## A/B Test Analysis

- Sample size validation
- Statistical significance (p-value, confidence interval)
- Effect size and practical significance
- Recommendation: ship / iterate / kill

## Rules

- Always state assumptions about data structure
- Include sample size requirements before running tests
- Flag when data is insufficient for conclusions
