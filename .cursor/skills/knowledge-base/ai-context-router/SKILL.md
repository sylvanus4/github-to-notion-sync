---
name: ai-context-router
description: >-
  Central context dispatcher for ai-* personal assistant skills. Queries MemKraft
  (personal memory) first, then LLM Wiki (company/team knowledge), optionally deep
  backends (gbrain, Cognee), and merges all results with provenance tags using
  Reciprocal Rank Fusion (RRF). Extends unified-knowledge-search with personal-first
  retrieval and provenance separation.
triggers:
  - ai-context-router
  - context routing
  - personal-first search
  - provenance search
  - 컨텍스트 라우팅
  - 개인 우선 검색
  - 프로비넌스 검색
  - ai context assembly
do_not_use_for:
  - Direct MemKraft CRUD operations (use memkraft skill)
  - Wiki management or compilation (use wiki-company or wiki-team)
  - General web search (use WebSearch or parallel-web-search)
  - Single-backend search without merging (use the specific backend skill)
  - Code review or debugging (use deep-review, diagnose)
---

# ai-context-router — Personal-First Context Assembly

## Purpose

The central dispatcher for all `ai-*` personal assistant skills. It assembles
context from multiple knowledge layers in a fixed priority order, merges results
with provenance tags, and delivers a unified context package that clearly separates
official knowledge from personal memory.

This skill extends the `unified-knowledge-search` RRF pattern with:
- **Personal-first retrieval**: MemKraft is always queried first and weighted higher
- **Provenance tagging**: every result carries its source tier tag
- **Tiered fallback**: graceful degradation when backends are unavailable

## Architecture

```
Query (from ai-* skill)
  │
  ├─→ Layer 1: MemKraft (personal memory)
  │     ├─ memory/topics/      (HOT/WARM/COLD topic files)
  │     ├─ memory/preferences/ (per-domain preferences)
  │     ├─ memory/unresolved/  (open questions)
  │     └─ memory/sessions/    (via recall skill)
  │
  ├─→ Layer 2: LLM Wiki (official knowledge)
  │     ├─ Company Wiki topics (high trust)
  │     └─ Team Wiki topics    (domain-scoped)
  │
  ├─→ Layer 3: Deep Backends (optional, entity-rich queries)
  │     ├─ gbrain (Postgres + pgvector)
  │     └─ Cognee (graph + vector)
  │
  ▼
RRF Merge with Provenance
  │
  ▼
Provenance-tagged context package
```

## Retrieval Order and Weights

| Layer | Backend | RRF Weight | Provenance Tags | When Queried |
|-------|---------|-----------|-----------------|--------------|
| 1 | MemKraft topics | 1.5× | `[PERSONAL]` | Always |
| 1 | MemKraft preferences | 1.5× | `[PREFERENCE]` | Always |
| 1 | MemKraft unresolved | 1.3× | `[UNRESOLVED]` | Always |
| 1 | MemKraft sessions (recall) | 1.2× | `[RECENT]` | Always |
| 2 | Company Wiki (kb-search) | 1.0× | `[COMPANY]` | Always |
| 2 | Team Wiki (kb-search --role) | 1.0× | `[TEAM:<domain>]` | Always |
| 3 | gbrain | 0.8× | `[ENTITY]` | On `--deep` flag or entity-rich query |
| 3 | Cognee | 0.8× | `[GRAPH]` | On `--deep` flag or relationship query |

MemKraft results receive a 1.2×–1.5× RRF weight multiplier to ensure personal
context surfaces above official knowledge for personal assistant use cases.

## Workflow

### Step 1: Query Classification

Classify the incoming query to determine which layers to activate:

- **Personal query** (e.g., "what did I decide about X"): MemKraft only, skip Wiki
- **Factual query** (e.g., "what is our deployment policy"): Wiki primary, MemKraft for context
- **Hybrid query** (e.g., "how should I handle X given our policy"): All layers
- **Entity query** (e.g., "what do we know about Company Y"): All layers + deep backends

### Step 2: MemKraft Query (Layer 1)

Query personal memory using the `memkraft` skill's query mode:

1. Search `memory/topics/` for matching content (prioritize HOT tier)
2. Search `memory/preferences/` for relevant domain preferences
3. Search `memory/unresolved/` for related open items
4. Search `memory/sessions/` via `recall` for session history
5. Tag each result with appropriate provenance

### Step 3: Wiki Query (Layer 2)

Query official knowledge using `kb-search`:

1. Search company-tier topics via `kb-search` (topics classified as "company" in `_wiki-registry.json`)
2. Search team-tier topics via `kb-search --role <domain>` if the query implies a domain
3. Tag company results with `[COMPANY]`, team results with `[TEAM:<domain>]`

### Step 4: Deep Backend Query (Layer 3, optional)

When `--deep` flag is set or query classification indicates entity/relationship needs:

1. Query gbrain via `hybrid_search` MCP tool
2. Query Cognee via `cognee search` CLI
3. Tag with `[ENTITY]` or `[GRAPH]`

### Step 5: RRF Merge with Provenance

Merge all results using weighted Reciprocal Rank Fusion:

```
RRF_score(doc) = Σ  weight_i / (k + rank_in_list_i)
                 i∈layers
```

Where `k = 60` (standard RRF constant) and `weight_i` is the layer-specific
multiplier from the table above.

1. Normalize results into common format (id, title, snippet, source, provenance_tag)
2. Apply weighted RRF across all result lists
3. Deduplicate by content similarity (threshold: 0.85)
4. Sort by descending weighted RRF score
5. Preserve provenance tags through the entire pipeline

### Step 6: Context Package Assembly

Assemble the final context package in the standard `ai-*` response format:

```markdown
## Official Knowledge (LLM Wiki)
- [COMPANY] <result from company wiki>
- [TEAM:engineering] <result from team wiki>

## Personal Context (MemKraft)
- [RECENT] <result from recent sessions>
- [PREFERENCE] <result from preferences>
- [UNRESOLVED] <open question related to query>

## Sources
- MemKraft: N results (M from HOT tier)
- Wiki: N results (company: X, team: Y)
- Deep: N results (gbrain: X, Cognee: Y) [if queried]
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `query` | (required) | Natural language query |
| `--deep` | false | Include Layer 3 backends (gbrain, Cognee) |
| `--personal-only` | false | Skip Wiki, MemKraft results only |
| `--wiki-only` | false | Skip MemKraft, Wiki results only |
| `--role <domain>` | auto | Scope team wiki to a specific domain |
| `--top-n` | 10 | Maximum results per layer |
| `--recency-boost` | true | Boost results from last 48 hours |

## Graceful Degradation

| Backends Available | Behavior |
|-------------------|----------|
| All layers | Full weighted RRF merge with provenance |
| MemKraft + Wiki | Standard personal-first merge (most common) |
| MemKraft only | Personal context only, note Wiki unavailable |
| Wiki only | Official knowledge only, note MemKraft unavailable |
| None | Error: no knowledge backends available |

## Integration

- **Upstream**: Called by all `ai-*` skills (ai-brief, ai-recall, ai-decide, ai-learn, ai-status)
- **Downstream**: Wraps `memkraft` (query mode), `kb-search`, `recall`, `gbrain`, `cognee`
- **Extends**: `unified-knowledge-search` RRF pattern with personal-first weighting
- **Config**: Reads `memory/memkraft.json` for tier thresholds; `knowledge-bases/_wiki-registry.json` for topic classification

## Checklist

- [ ] Receive query from ai-* skill
- [ ] Classify query type (personal / factual / hybrid / entity)
- [ ] Query MemKraft (topics, preferences, unresolved, sessions)
- [ ] Query Wiki (company tier, team tier with domain scoping)
- [ ] Optionally query deep backends (gbrain, Cognee)
- [ ] Apply weighted RRF merge with provenance preservation
- [ ] Deduplicate and rank results
- [ ] Assemble provenance-tagged context package
- [ ] Return structured context to calling ai-* skill
