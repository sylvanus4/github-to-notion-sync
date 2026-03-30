---
name: db-expert
description: >-
  Review PostgreSQL schemas, Alembic migrations, query plans, indexing
  strategies, and Redis caching patterns. Use when the user asks about database
  design, migration safety, query optimization, schema review, or connection
  pooling. Do NOT use for backend API design or service architecture (use
  backend-expert) or full-stack performance profiling (use
  performance-profiler). Korean triggers: "리뷰", "설계", "계획", "성능".
metadata:
  version: "1.0.0"
  category: "review"
  author: "thaki"
---
# DB Expert

Specialist for PostgreSQL 16, PgBouncer, Redis 7, and Qdrant. Migrations managed by Alembic at `db/migrations/`. Init scripts at `db/init.sql`.

## Schema Review

### Checklist

- [ ] Tables have explicit primary keys (prefer `BIGINT GENERATED ALWAYS AS IDENTITY` or UUID)
- [ ] Foreign keys have `ON DELETE` behavior defined (CASCADE / SET NULL / RESTRICT)
- [ ] `NOT NULL` constraints on columns that should never be empty
- [ ] `CHECK` constraints for domain rules (e.g., `status IN ('active','inactive')`)
- [ ] `created_at` / `updated_at` timestamps with `DEFAULT now()` and trigger for update
- [ ] Multi-tenant isolation via `tenant_id` column where applicable
- [ ] Naming convention: `snake_case` tables, singular nouns, `fk_<table>_<ref>` for foreign keys
- [ ] No reserved-word column names (`user`, `order`, `group`)

### Index Strategy

- [ ] Primary key auto-indexed (no duplicate index)
- [ ] Foreign keys have indexes (PostgreSQL does NOT auto-index FK columns)
- [ ] Composite indexes match query patterns (leftmost-prefix rule)
- [ ] Partial indexes for filtered queries (`WHERE deleted_at IS NULL`)
- [ ] GIN/GiST indexes for JSONB or full-text search columns
- [ ] No unused indexes (check `pg_stat_user_indexes.idx_scan = 0`)

## Alembic Migration Safety

### Pre-merge Checklist

- [ ] Migration is reversible (`downgrade()` implemented and tested)
- [ ] No `ALTER TABLE ... ADD COLUMN ... NOT NULL` without `DEFAULT` (locks table on PG < 11, still risky on large tables)
- [ ] `CREATE INDEX CONCURRENTLY` for large tables (requires `autocommit` mode in Alembic)
- [ ] No `DROP COLUMN` on high-traffic tables without feature flag / deploy-then-migrate
- [ ] Data migrations separated from schema migrations
- [ ] Migration tested against a copy of production data volume

### Dangerous Operations

| Operation | Risk | Safe alternative |
|-----------|------|-----------------|
| `DROP TABLE` | Data loss | Rename + deprecation period |
| `ALTER TYPE` on enum | Full table lock | Create new type, migrate, drop old |
| `ADD NOT NULL` column | Lock + fail if NULLs exist | Add nullable, backfill, then set NOT NULL |
| `RENAME COLUMN` | App breakage | Add new column, dual-write, drop old |

## Query Optimization

### Analysis Steps

1. Run `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` on the query
2. Check for sequential scans on large tables (> 10K rows)
3. Look for nested loop joins that should be hash joins
4. Verify index usage matches expectations
5. Check `rows` estimate vs actual (> 10x difference = stale statistics)

### Common Fixes

- Add missing indexes for `WHERE` / `JOIN` / `ORDER BY` columns
- Rewrite `NOT IN (subquery)` as `NOT EXISTS` (avoids NULL edge case)
- Use `LIMIT` + cursor pagination instead of `OFFSET` for large result sets
- Batch `INSERT` / `UPDATE` for bulk operations
- Use `MATERIALIZED VIEW` for expensive aggregation queries

## PgBouncer Notes

- Connection pool at port 5434 (proxies to PostgreSQL 5432)
- Pool mode: `transaction` (default) — no session-level features (LISTEN/NOTIFY, prepared statements)
- Set `statement_timeout` at the application level, not PgBouncer
- Max connections sized per service (check `pgbouncer.ini`)

## Redis Caching Patterns

- [ ] Cache key naming: `<service>:<entity>:<id>` (e.g., `admin:user:123`)
- [ ] TTL set on all keys (no unbounded cache growth)
- [ ] Cache invalidation on write (delete key or publish event)
- [ ] Use Redis pipelines for batch operations
- [ ] Pub/sub for cross-service event fanout (not for persistence)

## Examples

### Example 1: Migration safety review
User says: "Is this Alembic migration safe to run?"
Actions:
1. Check the migration file for dangerous operations (DROP, ALTER TYPE, ADD NOT NULL)
2. Verify downgrade() is implemented
3. Assess lock risk for large tables
Result: Migration safety assessment with risk rating and safer alternatives

### Example 2: Query optimization
User says: "This query is slow, can you help?"
Actions:
1. Run EXPLAIN ANALYZE on the query
2. Identify sequential scans, missing indexes, or stale statistics
3. Suggest index additions or query rewrites
Result: Query plan analysis with specific optimization recommendations

## Troubleshooting

### EXPLAIN ANALYZE not available
Cause: pg_stat_statements extension not enabled
Solution: Enable with `CREATE EXTENSION IF NOT EXISTS pg_stat_statements;` in PostgreSQL

### Alembic migration conflicts
Cause: Multiple developers creating migrations with the same head
Solution: Run `alembic heads` to check, then `alembic merge` to create a merge migration

## Output Format

```
Database Review Report
======================
Scope: [Schema / Migration / Query / Full]
Database: PostgreSQL 16

1. Schema Analysis
   Tables reviewed: [N]
   Issues:
   - [Table.Column]: [Issue] → [Fix]

2. Index Assessment
   Total indexes: [N] | Unused: [N]
   Missing:
   - [Table]: [Suggested index] (query pattern: [X])

3. Migration Safety
   File: [migration file]
   Reversible: [Yes / No]
   Lock risk: [None / Low / High]
   Recommendations:
   - [Step]: [Safer approach]

4. Query Performance
   Query: [identifier or first line]
   Plan: [Seq Scan / Index Scan / ...]
   Est. cost: [X] | Actual time: [X ms]
   Recommendation: [Optimization]

5. Connection / Caching
   PgBouncer: [Configured / Not configured]
   Redis cache hit ratio: [XX%]
   Issues:
   - [Key pattern]: [Problem] → [Fix]
```

## Additional Resources

For PostgreSQL anti-patterns and Alembic advanced patterns, see [references/reference.md](references/reference.md).
