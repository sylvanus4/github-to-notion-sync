---
name: graphify-query
description: >-
  Query Graphify knowledge graphs built by graphify-runner. Supports three
  modes: query (BFS/DFS traversal to answer questions), explain (node-centric
  exploration), and path (shortest path between two concepts). Reads from
  knowledge-bases/{topic}/graphify-out/graph.json. Use when the user asks to
  "query graphify", "ask the graph", "graphify query", "explain node",
  "graphify path", "graph Q&A", "graphify-query", "그래프 질문", "그래프 쿼리", "노드 설명",
  "경로 찾기", or wants to explore a Graphify knowledge graph interactively. Do
  NOT use for building graphs (use graphify-runner). Do NOT use for querying
  the markdown wiki (use kb-query). Do NOT use for general web search (use
  WebSearch). Korean triggers: "그래프 질문", "그래프 쿼리", "노드 설명", "경로 찾기", "그래피파이
  쿼리".
---

# Graphify Query — Knowledge Graph Explorer

Query, explain, and trace paths in Graphify knowledge graphs. Three modes cover different exploration patterns:

| Mode | Command | Purpose |
|------|---------|---------|
| `query` | Natural language question | BFS/DFS traversal to find related concepts |
| `explain` | Single concept name | Node-centric view of all connections |
| `path` | Two concept names | Shortest path between concepts |

## Prerequisites

- A graph must exist at `knowledge-bases/{topic}/graphify-out/graph.json`
- Built by graphify-runner (run it first if no graph exists)
- Python packages: `graphifyy`, `networkx`

## Input

- **topic**: KB topic name (required)
- **mode**: `query`, `explain`, or `path` (required)
- **question/concept(s)**: The actual query content (required)

## Workflow

### Step 0 — Validate Graph Exists

```python
from pathlib import Path

graph_path = Path(f"knowledge-bases/{topic}/graphify-out/graph.json")
if not graph_path.exists():
    print(f"No graph found at {graph_path}")
    print(f"Run graphify-runner on topic '{topic}' first.")
    raise SystemExit(1)
```

### Mode: query

Answer a natural language question by traversing the graph from matching start nodes.

**Traversal strategy**:
- **BFS** (default): "What is X connected to?" — broad context, nearest neighbors first, depth 3
- **DFS** (`--dfs`): "How does X reach Y?" — trace a specific chain, depth-limited to 6

```python
import json
import networkx as nx
from networkx.readwrite import json_graph
from pathlib import Path

data = json.loads(Path(f"knowledge-bases/{topic}/graphify-out/graph.json").read_text())
G = json_graph.node_link_graph(data, edges='links')

question = "USER_QUESTION"
mode = "bfs"  # or "dfs"
terms = [t.lower() for t in question.split() if len(t) > 3]

# Find best-matching start nodes
scored = []
for nid, ndata in G.nodes(data=True):
    label = ndata.get('label', '').lower()
    score = sum(1 for t in terms if t in label)
    if score > 0:
        scored.append((score, nid))
scored.sort(reverse=True)
start_nodes = [nid for _, nid in scored[:3]]

if not start_nodes:
    print("No matching nodes found for query terms:", terms)
    # Suggest: list available node labels for the user

# BFS traversal (depth 3)
subgraph_nodes = set(start_nodes)
subgraph_edges = []
frontier = set(start_nodes)
for _ in range(3):
    next_frontier = set()
    for n in frontier:
        for neighbor in G.neighbors(n):
            if neighbor not in subgraph_nodes:
                next_frontier.add(neighbor)
                subgraph_edges.append((n, neighbor))
    subgraph_nodes.update(next_frontier)
    frontier = next_frontier
```

After extracting the subgraph:
1. Read node labels, edge relations, confidence tags, source locations
2. Answer using **only** what the graph contains
3. Quote `source_location` when citing a specific fact
4. If the graph lacks enough information, say so — do not hallucinate edges

**Token budget**: Default 2000 tokens (~8000 chars). Rank nodes by relevance to question terms, truncate output at budget.

### Mode: explain

Give a plain-language explanation of a single node and everything connected to it.

```python
term = "CONCEPT_NAME"
term_lower = term.lower()

scored = sorted(
    [(sum(1 for w in term_lower.split() if w in G.nodes[n].get('label','').lower()), n)
     for n in G.nodes()],
    reverse=True
)

if not scored or scored[0][0] == 0:
    print(f"No node matching '{term}'")
    # Suggest similar node labels

nid = scored[0][1]
node_data = G.nodes[nid]
# Print: label, source file, file type, degree
# Print all connections: relation, target label, confidence, source file
```

After extracting connections, write a 3-5 sentence explanation covering:
- What this node represents
- What it connects to (grouped by relation type)
- Why those connections are significant
- Source citations from `source_location`

### Mode: path

Find the shortest path between two named concepts.

```python
import networkx as nx

src = find_node("CONCEPT_A")
tgt = find_node("CONCEPT_B")

try:
    path = nx.shortest_path(G, src, tgt)
    # Print each hop with edge relation and confidence
except nx.NetworkXNoPath:
    print(f"No path found between '{CONCEPT_A}' and '{CONCEPT_B}'")
except nx.NodeNotFound as e:
    print(f"Node not found: {e}")
```

After finding the path, explain in plain language what each hop means and why the connection chain is significant.

## Graph Statistics Helper

When no specific query is given, or when the user asks "what's in this graph?", provide overview stats:

```python
print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
# Top 10 nodes by degree (god nodes)
# Community count and sizes
# Edge type distribution
```

## Output Format

All query responses follow this structure:

1. **Query acknowledgment**: What was asked, which topic graph was searched
2. **Graph traversal result**: Raw node/edge data from the traversal
3. **Synthesized answer**: Plain-language answer citing source locations
4. **Follow-up suggestions**: Related questions the user might explore next

## Error Handling

- **No graph file**: Direct user to run `graphify-runner` first
- **No matching nodes**: List the 5 closest node labels as suggestions
- **Empty graph**: Report that the graph has 0 nodes, suggest rebuilding
- **Disconnected components**: If path query fails, check if nodes are in different components

## Verification

After each query, verify the answer is grounded in graph data:

- Every claim must trace to a specific node or edge in the subgraph
- Confidence tags (EXTRACTED/INFERRED/AMBIGUOUS) must be disclosed for key claims
- If the answer relies on AMBIGUOUS edges, flag this explicitly
