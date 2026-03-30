# DB Expert — Reference

## Alembic Configuration for This Project

- Config at `db/alembic.ini`, env at `db/migrations/env.py`
- Versions directory: `db/migrations/versions/`
- Async engine support via `asyncpg`

### Generate a Migration

```bash
cd db
alembic revision --autogenerate -m "description"
```

### Run Migrations

```bash
alembic upgrade head      # apply all
alembic downgrade -1      # rollback one
alembic history --verbose # show history
```

### Concurrent Index Creation

Alembic does not natively support `CREATE INDEX CONCURRENTLY`. Use raw SQL:

```python
from alembic import op

def upgrade():
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS
        ix_calls_tenant_id ON calls (tenant_id)
    """)

# Must set in env.py:
# context.configure(..., transaction_per_migration=True)
# And run migration outside a transaction block
```

## PostgreSQL Anti-Patterns

### 1. OFFSET Pagination on Large Tables

**Problem**: `OFFSET 10000` scans and discards 10000 rows.

**Fix**: Keyset (cursor) pagination:
```sql
SELECT * FROM calls
WHERE id > :last_seen_id
ORDER BY id
LIMIT 50;
```

### 2. SELECT * in Application Code

**Problem**: Fetches unnecessary columns, breaks when schema changes.

**Fix**: Always specify columns explicitly in SQLAlchemy queries.

### 3. Missing Index on Foreign Keys

**Problem**: PostgreSQL does not auto-create indexes on FK columns. JOIN/DELETE performance degrades.

**Fix**: Always create an index on FK columns:
```sql
CREATE INDEX ix_stt_segments_call_id ON stt_segments (call_id);
```

### 4. N+1 Query Pattern

**Problem**: Loop fetches related records one by one.

**Fix**: Use SQLAlchemy `selectinload()` or `joinedload()`:
```python
stmt = select(Call).options(selectinload(Call.segments))
```

### 5. Long-Running Transactions

**Problem**: Holds locks, bloats WAL, prevents autovacuum.

**Fix**:
- Set `statement_timeout` (e.g., 30s for web requests)
- Use `idle_in_transaction_session_timeout`
- Batch large updates into chunks

## Key Tables (from db/init.sql)

| Table | Purpose | Key columns |
|-------|---------|-------------|
| tenants | Multi-tenant root | id, name, plan |
| users | User accounts | id, tenant_id, email, role |
| agents | AI agent configs | id, tenant_id, model_config |
| calls | Call sessions | id, tenant_id, agent_id, status |
| stt_segments | Speech-to-text segments | id, call_id, text, speaker |
| knowledge_documents | RAG knowledge base | id, tenant_id, status, embedding_status |

## Redis Key Conventions

```
# Session cache
session:<session_id> → JSON (TTL: 24h)

# User cache
admin:user:<user_id> → JSON (TTL: 1h)

# Rate limit counters
ratelimit:<service>:<endpoint>:<client_ip> → INT (TTL: window)

# Pub/Sub channels
events:<tenant_id>:<event_type>
```
