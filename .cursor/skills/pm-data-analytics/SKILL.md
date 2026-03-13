---
name: pm-data-analytics
description: >-
  Orchestrate data analytics workflows for PMs: SQL query generation from
  natural language, cohort analysis (retention, feature adoption), and A/B test
  analysis (statistical significance, sample size, recommendations). Based on
  phuryn/pm-skills. Use when the user asks for "SQL query", "cohort analysis",
  "A/B test analysis", "retention analysis", "write query", or "analyze test
  results". Do NOT use for general data exploration (use
  kwp-data-data-exploration), statistical methods (use
  kwp-data-statistical-analysis), or dashboard building (use
  kwp-data-interactive-dashboard-builder). Korean triggers: "SQL 쿼리", "코호트 분석",
  "A/B 테스트 분석", "리텐션 곡선", "통계적 유의성", "데이터 분석", "쿼리 생성",
  "샘플 크기", "실험 결과".
metadata:
  author: "thaki"
  version: "1.0.0"
  upstream: "https://github.com/phuryn/pm-skills"
  category: "product"
---
# PM Data Analytics

Orchestrate data analytics workflows for product managers using phuryn/pm-skills — SQL query generation from natural language, cohort analysis (retention, feature adoption), and A/B test analysis with statistical rigor.

## Sub-Skill Index

| Sub-Skill | When to Use | Reference |
|-----------|--------------|-----------|
| ab-test-analysis | Evaluate experiment results, statistical significance, ship/extend/stop decisions | [references/ab-test-analysis.md](references/ab-test-analysis.md) |
| cohort-analysis | Retention by cohort, feature adoption trends, churn patterns, engagement analysis | [references/cohort-analysis.md](references/cohort-analysis.md) |
| sql-queries | Generate SQL from natural language, build data reports, translate business questions | [references/sql-queries.md](references/sql-queries.md) |

## Workflow

1. **Identify sub-skill**: From the user's request and trigger words, pick the matching sub-skill from the index.
2. **Read reference**: Load the corresponding `references/<name>.md` file and review its Instructions, How It Works, and Output Format.
3. **Follow instructions**: Replace `$ARGUMENTS` in the reference with the user's context; follow the framework and output process; produce structured output (markdown, tables, SQL, or Python as specified).

## Examples

### Example 1: A/B Test Analysis
- **Trigger**: "Our checkout A/B test ran for 2 weeks. Control 4.2% conversion, variant 4.8%. Should we ship?"
- **Action**: Use ab-test-analysis reference; validate sample size, calculate p-value and lift; apply decision framework.
- **Result**: Summary table with recommendation (Ship/Extend/Stop), reasoning, and next steps.

### Example 2: Cohort Analysis
- **Trigger**: "Analyze retention patterns from this CSV. Which signup cohorts show best long-term engagement?"
- **Action**: Use cohort-analysis reference; validate data, compute retention rates, visualize curves; identify patterns.
- **Result**: Data summary, retention heatmap/charts, 2–3 insights, research recommendations.

### Example 3: SQL Query
- **Trigger**: "Write a query for users who signed up in the last 30 days with at least 5 sessions. PostgreSQL."
- **Action**: Use sql-queries reference; infer or request schema; generate optimized query with explanation.
- **Result**: Production-ready SQL, plain-English explanation, performance notes.

## Error Handling

| Situation | Action |
|-----------|--------|
| Ambiguous request (e.g. "analyze data") | Ask: SQL query, cohort analysis, or A/B test? Suggest sql-queries or cohort-analysis. |
| Multiple sub-skills implied | Start with the most specific (e.g. ab-test-analysis if experiment data is present). |
| Missing context (schema, metrics) | Request: database schema, metric definitions, or test setup details. |
| Request out of scope (data exploration, dashboards) | Redirect: kwp-data-data-exploration or kwp-data-interactive-dashboard-builder. |
