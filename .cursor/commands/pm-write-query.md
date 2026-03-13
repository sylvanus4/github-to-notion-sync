---
description: Generate SQL queries from natural language — BigQuery, PostgreSQL, MySQL. Includes schema detection, CTE optimization, edge case handling.
argument-hint: "<natural language query> | <database type> | [schema or table names]"
---

# PM Write Query

Generate SQL queries from natural language descriptions. Supports BigQuery, PostgreSQL, MySQL. References pm-data-analytics skill, sql-queries sub-skill. Includes schema detection, CTE optimization, and edge case handling.

## Usage

```
/pm-write-query Users who signed up in last 30 days with 5+ sessions, PostgreSQL
/pm-write-query 최근 30일 내 가입한 사용자 중 세션 5회 이상인 사용자, PostgreSQL
```

## Workflow

### Step 1: Load skill and reference

Read the `pm-data-analytics` skill (`.cursor/skills/pm-data-analytics/SKILL.md`) and `references/sql-queries.md`.

### Step 2: Parse request

Extract from the user input:

- Natural language query (business question)
- Database type (BigQuery, PostgreSQL, MySQL, or Snowflake if supported)
- Schema hints (table names, column names) if provided
- Edge cases (nulls, duplicates, date boundaries)

### Step 3: Infer or request schema

If schema is not provided:

- Ask for table names and key columns, or
- Infer common patterns (e.g., `users`, `sessions`, `created_at`)
- Document assumptions explicitly

### Step 4: Generate query

Produce production-ready SQL with:

- CTEs for readability when logic is complex
- Proper JOINs, filters, and aggregations
- Handling of nulls, duplicates, and date ranges
- Index-friendly patterns where applicable
- Comments for non-obvious logic

### Step 5: Output

Deliver:

1. Plain-English explanation of the query
2. Full SQL with formatting
3. Performance notes and edge case handling
4. Optional: validation queries for spot checks

## Notes

- Always specify database type; syntax varies (e.g., `DATE_TRUNC` vs `DATE_TRUNC`).
- Use CTEs for queries with 2+ logical steps.
- For production use, validate against actual schema before running.
