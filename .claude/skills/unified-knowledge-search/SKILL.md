---
name: unified-knowledge-search
description: >-
  Federated search across all knowledge backends — MemKraft (personal memory
  with HOT/WARM/COLD tiers), gbrain (Postgres + pgvector), Karpathy KB (SQLite
  FTS5 + optional embeddings), Cognee (graph + vector), and recall memory
  (BM25/semantic). Merges results using Reciprocal Rank Fusion (RRF) with prov
---

# unified-knowledge-search

Federated search across all knowledge backends — MemKraft (personal memory with HOT/WARM/COLD tiers), gbrain (Postgres + pgvector), Karpathy KB (SQLite FTS5 + optional embeddings), Cognee (graph + vector), and recall memory (BM25/semantic). Merges results using Reciprocal Rank Fusion (RRF) with provenance tags for a single ranked answer list. Supports `--personal-first` mode (default for `ai-*` skills) that applies recency-weighted boosting to MemKraft results.

## Triggers

Use when the user asks to "search everything", "unified search", "find across all knowledge", "federated search", "search all backends", "통합 검색", "전체 지식 검색", "모든 KB 검색", "unified-knowledge-search", or when a pipeline skill needs cross-backend knowledge retrieval. Also used as the search layer for `ai-context-router` in `--personal-first` mode.

Do NOT use for gbrain-only entity lookup (use gbrain MCP `hybrid_search` directly).
Do NOT use for KB-only wiki search (use kb-search).
Do NOT use for Cognee-only graph queries (use cognee).
Do NOT use for session memory recall only (use recall).
Do NOT use for MemKraft-only personal memory queries (use memkraft).
Do NOT use for web search (use WebSearch or parallel-web-search).

## Architecture

```
Query
  │
  ├─→ MemKraft search (HOT/WARM/COLD tier scan, recency-weighted)
  ├─→ gbrain hybrid_search (keyword + vector, pgvector)
  ├─→ kb-search (SQLite FTS5 + optional vector)
  ├─→ Cognee search (graph-enhanced RAG)
  └─→ recall search (BM25/semantic over session memory)
  │
  ▼
RRF Merge (k=60, with optional personal-first weighting)
  │
  ▼
Deduplicated, ranked results with provenance tags + source attribution
```

### Personal-First Mode

When invoked with `--personal-first` (default for all `ai-*` skills via `ai-context-router`):

- MemKraft results receive a **1.5x RRF weight multiplier** (recency bias)
- HOT-tier entries receive an additional **1.2x boost** over WARM/COLD
- Results are tagged with provenance: `[PERSONAL]`, `[PREFERENCE]`, `[RECENT]`, `[UNRESOLVED]`, `[COMPANY]`, `[TEAM:<domain>]`, `[ARCHIVED]`

Standard mode (no flag): all backends weighted equally, provenance tags still applied.

## Reciprocal Rank Fusion (RRF)

Each backend returns its own ranked list. RRF combines them:

```
RRF_score(doc) = Σ  1 / (k + rank_in_list_i)
                 i∈backends
```

Where `k = 60` (standard RRF constant). A document appearing in multiple backends gets boosted; a document ranked #1 in one backend and absent from others still scores well.

## Workflow

### Step 1: Query Expansion

Expand the user query into backend-appropriate forms:
- **MemKraft**: original query + preference/unresolved keyword variants (scans HOT → WARM → COLD tiers)
- **gbrain**: original query + entity-name variant (e.g., "Garry Tan" → also search "garry-tan")
- **KB**: original query (FTS5 handles stemming)
- **Cognee**: original query (graph traversal handles relationships)
- **recall**: original query (BM25 handles term matching)

### Step 2: Parallel Dispatch

Fan out to all available backends simultaneously using parallel subagents:

1. **MemKraft**: Scan `memory/` directory (HOT → WARM → COLD tiers) using `python scripts/memory/search_memory.py "<query>" --tier all --json --top 10` (skip if `memkraft.json` not found)
2. **gbrain**: Call `hybrid_search` MCP tool with `{"query": "<expanded>", "limit": 10}`
3. **KB search**: Run `python scripts/kb_search.py "<query>" --json --top 10`
4. **Cognee**: Run `cognee search "<query>"` (skip if Cognee not initialized)
5. **recall**: Run `python scripts/memory/search_memory.py "<query>" --top 10` (skip if index unavailable)

Each backend may be unavailable — skip gracefully and merge from available backends only.

### Step 3: Result Normalization

Normalize each backend's results into a common format:

```json
{
  "id": "<unique-identifier>",
  "title": "<result title or page slug>",
  "snippet": "<relevant excerpt, max 300 chars>",
  "source": "memkraft|gbrain|kb|cognee|recall",
  "source_detail": "<topic name, slug, or memory file>",
  "rank": 1,
  "backend_score": 0.85
}
```

### Step 4: RRF Merge

1. Assign RRF scores across all backend result lists
2. Deduplicate by content similarity (same entity/article from different backends)
3. Sort by descending RRF score
4. Return top-N results (default: 10)

### Step 5: Output

Present results with source attribution:

```
## Search Results for: "<query>"

**Backends queried**: gbrain ✓, KB ✓, Cognee ✓, recall ✗ (unavailable)

| Rank | Title | Source | RRF Score | Snippet |
|------|-------|--------|-----------|---------|
| 1 | Garry Tan | gbrain | 0.032 | CEO of Y Combinator, active investor... |
| 2 | AI Startup Ecosystem | KB:ai-research | 0.028 | Overview of YC-backed AI companies... |
| 3 | Meeting: YC Demo Day | gbrain | 0.024 | Notes from 2026 YC Demo Day... |
```

## Backend Availability

The skill degrades gracefully when backends are unavailable:

| Backends Available | Behavior |
|-------------------|----------|
| All 5 | Full RRF merge across all sources |
| 4 of 5 | RRF across available; note missing backend |
| 3 of 5 | RRF across available; reduced confidence |
| 1-2 of 5 | Direct passthrough or minimal RRF |
| 0 of 5 | Error: no knowledge backends available |

## Configuration

Settings in `.cursor/skills/knowledge-base/unified-knowledge-search/config.json`:

```json
{
  "rrf_k": 60,
  "default_top_n": 10,
  "backends": {
    "memkraft": { "enabled": true, "limit": 10, "tiers": ["HOT", "WARM", "COLD"] },
    "gbrain": { "enabled": true, "limit": 10 },
    "kb": { "enabled": true, "limit": 10, "mode": "auto" },
    "cognee": { "enabled": true, "limit": 10 },
    "recall": { "enabled": true, "limit": 10 }
  },
  "personal_first": {
    "memkraft_weight": 1.5,
    "hot_tier_boost": 1.2
  },
  "dedup_similarity_threshold": 0.85
}
```

## MCP Tools Used

| Backend | Tool / Command |
|---------|---------------|
| MemKraft | `python scripts/memory/search_memory.py --tier all` |
| gbrain | `hybrid_search` MCP tool |
| KB | `python scripts/kb_search.py` |
| Cognee | `cognee search` CLI |
| recall | `python scripts/memory/search_memory.py` |

## Error Handling

- Backend timeout (>5s): skip backend, proceed with others
- Backend error: log warning, exclude from RRF merge
- Empty results from all backends: report "no results found" with query suggestions
- Deduplication conflict: prefer the result with higher backend_score

## Checklist

- [ ] Receive query from user or pipeline (detect `--personal-first` flag)
- [ ] Expand query for backend-specific formats (including MemKraft tier scan)
- [ ] Dispatch to all 5 available backends in parallel
- [ ] Normalize results into common format with provenance tags
- [ ] Apply RRF merge with deduplication (personal-first weighting if flagged)
- [ ] Present ranked results with source attribution and provenance
- [ ] Report which backends were queried and any unavailability
