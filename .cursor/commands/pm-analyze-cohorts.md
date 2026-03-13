---
description: Cohort analysis of user engagement — retention curves, feature adoption, engagement trends. Supports CSV upload or SQL framework design.
argument-hint: "<CSV path or SQL context> | <cohort dimension> | <metric to analyze>"
---

# PM Analyze Cohorts

Cohort analysis of user engagement data — retention curves, feature adoption, and engagement trends. References pm-data-analytics skill, cohort-analysis sub-skill. Supports data upload (CSV) or analysis framework design (SQL queries).

## Usage

```
/pm-analyze-cohorts Analyze retention by signup month from this CSV [attach file]
/pm-analyze-cohorts 가입 월별 리텐션 분석해줘, CSV 데이터 있어
```

## Workflow

### Step 1: Load skill and reference

Read the `pm-data-analytics` skill (`.cursor/skills/pm-data-analytics/SKILL.md`) and `references/cohort-analysis.md`.

### Step 2: Determine input mode

- **CSV upload**: User provides file path or pastes data. Validate columns (user_id, cohort date, activity date, metrics).
- **SQL framework**: User has data in DB. Design SQL to compute cohort tables and retention metrics.

### Step 3: Define cohort and metrics

Clarify or infer:

- Cohort dimension (signup date, first purchase, first feature use)
- Retention metric (DAU, sessions, revenue, feature adoption)
- Time buckets (day, week, month)
- Analysis period and cohort inclusion criteria

### Step 4: Compute and visualize

- Build cohort retention matrix
- Compute retention rates per cohort
- Identify patterns: best/worst cohorts, engagement decay, feature adoption curves
- Produce 2–3 actionable insights
- Suggest follow-up research or experiments

### Step 5: Output

Deliver:

1. Data summary and validation notes
2. Retention heatmap or curves (describe if no viz tool)
3. Key insights with evidence
4. Optional: SQL templates for reproducible analysis
5. Recommendations for further analysis

## Notes

- Minimum viable columns: user_id, cohort date, activity date.
- Watch for survivorship bias; define active-user criteria clearly.
- Monthly cohorts are common for B2B; weekly for high-frequency products.
