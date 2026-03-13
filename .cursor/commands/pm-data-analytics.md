---
description: PM data analytics workflows — SQL query generation, cohort analysis, and A/B test analysis
argument-hint: "<analysis request or data context>"
---

## PM Data Analytics

Data analytics workflows for PMs: SQL query generation, cohort analysis, and A/B test analysis.

### Usage

```
<sub-skill> [context]
```

### Sub-Skills

| Sub-Skill | Shorthand | What it does |
|-----------|-----------|--------------|
| sql-queries | `sql` | Generate SQL from natural language (BigQuery, PostgreSQL, MySQL, Snowflake) |
| cohort-analysis | `cohort` | Cohort analysis: retention curves, feature adoption, churn patterns |
| ab-test-analysis | `abtest` | A/B test analysis: statistical significance, sample size, ship/extend/stop |

### Execution

Read and follow the `pm-data-analytics` skill (`.cursor/skills/pm-data-analytics/SKILL.md`) for the full workflow, sub-skill selection, and error handling.

### Examples

```bash
# Generate SQL query
/pm-data-analytics sql -- users who signed up in last 30 days with 5+ sessions, PostgreSQL

# Cohort analysis
/pm-data-analytics cohort -- analyze retention by signup month from this CSV

# A/B test analysis
/pm-data-analytics abtest -- checkout test: control 4.2%, variant 4.8%, 2 weeks, should we ship?
```
