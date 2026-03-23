---
name: mirofish-graph-explorer
description: Explore and query MiroFish GraphRAG knowledge graphs — browse entities, relationships, entity types, and graph topology built from seed documents. Use when the user asks to "explore graph", "browse knowledge graph", "show entities", "graph data", "entity relationships", "그래프 탐색", "지식 그래프", "엔티티 관계", "mirofish graph", or any request to inspect the knowledge graph structure before or after simulation. Do NOT use for building graphs (use mirofish). Do NOT use for running simulations (use mirofish or mirofish-financial-sim). Do NOT use for general knowledge graph operations outside MiroFish (use cognee).
---

# MiroFish Graph Explorer

## Overview

Inspect and query the GraphRAG knowledge graphs that MiroFish builds from seed documents. Understand entity relationships, verify graph quality before simulation, and explore post-simulation graph updates.

## Prerequisites

MiroFish backend running at `http://localhost:5001`. At least one knowledge graph must be built.

## Quality Contract (graph exploration vs simulation evals)

This skill does **not** run simulations or author full seed documents. Map user requests as follows:

| Eval | How this skill satisfies it |
|------|---------------------------|
| EVAL 1 (seed structure) | When the user only needs graph data, **cite** that a proper seed for *new* graphs must follow `mirofish` (H1 title, ISO date, ≥3 `##` sections, ≥5 entities). If they need a new semiconductor graph, tell them to run ontology with a seed listing fabs, tickers (e.g. NVDA, TSM), and policies — then return exploration results. |
| EVAL 2 (simulation config) | State explicitly: **this skill is read-only** — no default rounds/agent counts here. For “탐색만” requests, defaults are N/A; if they ask to simulate after exploration, hand off to `mirofish` / `mirofish-financial-sim` with rounds 20–25 and ~26 agents after prepare. |
| EVAL 3 (output structure) | Every graph summary you return MUST include: **graph_id** (or project id), **timestamp**, **entity counts** (total + by type if available), **≥3 example entities** relevant to the query (e.g. semiconductor: company + concept + person), and **1–2 relationship insights** (e.g. high-degree nodes, clusters). |
| EVAL 4 (API usage) | Use only the documented endpoints below (`/api/graph/...`, `/api/simulation/entities/...`). Do **not** invent `POST /graph` or `POST /simulation/run` — those are not valid shortcuts. |

### Example: “반도체 관련 엔티티 탐색”

1. `GET /api/graph/project/list` → pick `project_id` / latest `graph_id` (or ask user).
2. `GET /api/simulation/entities/<graph_id>/by-type/organization` (and `concept`, `person`) — filter client-side for 키워드: 반도체, semiconductor, NVDA, TSM, foundry, etc.
3. Optionally `GET /api/graph/data/<graph_id>` for edges involving those node ids (may be large — prefer entity endpoints first).
4. Respond with the EVAL 3 bullet structure.

## API Reference

### Project Management

```bash
# List all projects
curl -s http://localhost:5001/api/graph/project/list | python3 -m json.tool

# Get project details
curl -s http://localhost:5001/api/graph/project/<project_id> | python3 -m json.tool

# Reset project (clears all graphs and simulations)
curl -X POST http://localhost:5001/api/graph/project/<project_id>/reset
```

### Graph Data Exploration

```bash
# Get full graph data (nodes + edges)
curl -s http://localhost:5001/api/graph/data/<graph_id> | python3 -m json.tool

# List entities from graph
curl -s http://localhost:5001/api/simulation/entities/<graph_id> | python3 -m json.tool

# Get specific entity details
curl -s http://localhost:5001/api/simulation/entities/<graph_id>/<entity_uuid> | python3 -m json.tool

# Filter entities by type (person, organization, event, location, concept)
curl -s http://localhost:5001/api/simulation/entities/<graph_id>/by-type/person | python3 -m json.tool
```

### Task Monitoring

```bash
# Check graph build status
curl -s http://localhost:5001/api/graph/task/<task_id> | python3 -m json.tool

# List all build tasks
curl -s http://localhost:5001/api/graph/tasks | python3 -m json.tool
```

## Graph Structure

MiroFish GraphRAG produces the following entity types:

| Entity Type | Description | Example |
|-------------|-------------|---------|
| `person` | Individual agents with personality and biography | "Warren Buffett", "Retail Investor A" |
| `organization` | Companies, institutions, government bodies | "Federal Reserve", "NVIDIA Corp" |
| `event` | Historical or hypothetical events | "2024 FOMC Meeting", "Q4 Earnings" |
| `location` | Geographic locations | "Wall Street", "Silicon Valley" |
| `concept` | Abstract ideas, policies, financial instruments | "Interest Rate", "Quantitative Easing" |

## Graph Quality Checklist

Before starting a simulation, verify:

1. **Entity count:** Are enough entities extracted? (aim for 10-50 for focused simulations)
2. **Relationship density:** Do entities have meaningful connections? (orphan entities produce poor simulations)
3. **Entity types:** Is there diversity? (mix of persons, organizations, and concepts produces richer interactions)
4. **Key actors:** Are the critical stakeholders represented as entities?
5. **Temporal markers:** Are time-sensitive events properly captured?

## Error Handling

| Error | Action |
|-------|--------|
| "Graph not found" | No graph built yet. Build one first using the `mirofish` skill Phase 1. |
| Empty entity list | Seed document may be too short or vague. Re-run ontology generation with richer text. |
| MiroFish backend unreachable | Start with `cd ~/thaki/MiroFish && npm run dev`. Verify: `curl -s http://localhost:5001/health` |
| Entity type filter returns empty | Try different entity types: `person`, `organization`, `event`, `location`, `concept` |
| Graph data endpoint timeout | Large graphs (1000+ entities) may be slow. Use entity filtering endpoints instead. |

## Workflow

1. Build a graph using the `mirofish` skill's Phase 1
2. Use this skill to inspect and validate the graph
3. If graph quality is insufficient, regenerate ontology with refined seed text
4. Once satisfied, proceed to simulation with the `mirofish` skill's Phase 2+

## Examples

```
/mirofish-graph -- Show me all entities in the latest knowledge graph
/mirofish-graph -- List all person-type entities from graph abc123
/mirofish-graph -- What relationships exist between "Federal Reserve" and other entities?
/mirofish-graph -- How many entities were extracted from the uploaded document?
/mirofish-graph -- Show the full graph topology for my financial scenario project
```
