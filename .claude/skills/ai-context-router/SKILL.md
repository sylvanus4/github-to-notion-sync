---
name: ai-context-router
description: >-
  Central context dispatcher for ai-* personal assistant skills. Queries
  MemKraft (personal memory) first, promotes gbrain to Layer 0 for
  entity-specific queries via 5-step brain-first protocol, then LLM Wiki
  (company/team knowledge), optionally Cognee for graph queries, and merges
  all results with provenance tags using Reciprocal Rank Fusion (RRF). Extends
  unified-knowledge-search with personal-first retrieval, brain-first entity
  lookup, and provenance separation.
---

# ai-context-router — Personal-First Context Assembly

## Purpose

The central dispatcher for all `ai-*` personal assistant skills. It assembles
context from multiple knowledge layers in a fixed priority order, merges results
with provenance tags, and delivers a unified context package that clearly separates
official knowledge from personal memory.

This skill extends the `unified-knowledge-search` RRF pattern with:
- **Personal-first retrieval**: MemKraft is always queried first and weighted higher
- **Brain-first entity lookup**: gbrain is promoted to Layer 0 for entity-specific queries via the 5-step mandatory protocol (search → check freshness → read page → compile if stale → cite)
- **Provenance tagging**: every result carries its source tier tag
- **Tiered fallback**: graceful degradation when backends are unavailable

## Architecture

```
Query (from ai-* skill)
  │
  ├─→ Layer 0: Brain-First Gate (entity queries only)
  │     └─ 5-step mandatory protocol:
  │         1. gbrain search (hybrid: vector + keyword)
  │         2. Freshness check (< 7 days = fresh)
  │         3. Read matching brain page
  │         4. Compile if stale (trigger recompilation)
  │         5. Cite with [Source: brain/<path>] tag
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
  ├─→ Layer 3: Deep Backends (optional, relationship queries)
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
| 0 | gbrain (brain-first) | 1.6× | `[BRAIN]` | Entity-specific queries (auto-detected) |
| 1 | MemKraft topics | 1.5× | `[PERSONAL]` | Always |
| 1 | MemKraft preferences | 1.5× | `[PREFERENCE]` | Always |
| 1 | MemKraft unresolved | 1.3× | `[UNRESOLVED]` | Always |
| 1 | MemKraft sessions (recall) | 1.2× | `[RECENT]` | Always |
| 2 | Company Wiki (kb-search) | 1.0× | `[COMPANY]` | Always |
| 2 | Team Wiki (kb-search --role) | 1.0× | `[TEAM:<domain>]` | Always |
| 3 | Cognee | 0.8× | `[GRAPH]` | On `--deep` flag or relationship query |

gbrain Layer 0 activates automatically when the query classifier detects entity-specific
intent (people, companies, deals, projects). Non-entity queries skip Layer 0.
MemKraft results receive a 1.2×–1.5× RRF weight multiplier to ensure personal
context surfaces above official knowledge for personal assistant use cases.

## Workflow

### Step 1: Query Classification

Classify the incoming query to determine which layers to activate:

- **Personal query** (e.g., "what did I decide about X"): MemKraft only, skip Wiki
- **Factual query** (e.g., "what is our deployment policy"): Wiki primary, MemKraft for context
- **Hybrid query** (e.g., "how should I handle X given our policy"): All layers
- **Entity query** (e.g., "what do we know about Company Y"): Brain-first (Layer 0) + all layers

### Step 1b: Brain-First Gate (Layer 0, entity queries only)

When query classification detects entity-specific intent (people, companies, deals, projects),
execute the 5-step mandatory brain-first protocol before any other layer:

1. `gbrain search "<entity>" --hybrid --limit 10` (vector + keyword)
2. Freshness check: if `updated_at < 7 days ago` → fresh; otherwise → stale
3. Read matching brain page content
4. If stale → trigger `gbrain compile --entity "<entity>"` for recompilation
5. Tag results with `[BRAIN]` provenance and cite as `[Source: brain/<path>]`

Non-entity queries skip this step entirely.

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

When `--deep` flag is set or query classification indicates relationship/graph needs:

1. Query Cognee via `cognee search` CLI
2. Tag with `[GRAPH]`

Note: gbrain entity queries are handled at Layer 0 (Step 1b) and are NOT part of this step.

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
- Brain: N results [entity queries only, Layer 0]
- Deep: N results (Cognee) [if queried]
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `query` | (required) | Natural language query |
| `--deep` | false | Include Layer 3 backend (Cognee graph queries) |
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
- [ ] Optionally query deep backend (Cognee) — gbrain entity queries handled at Layer 0
- [ ] Apply weighted RRF merge with provenance preservation
- [ ] Deduplicate and rank results
- [ ] Assemble provenance-tagged context package
- [ ] Return structured context to calling ai-* skill
