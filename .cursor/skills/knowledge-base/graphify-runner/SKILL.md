---
name: graphify-runner
description: >-
  Build Graphify knowledge graphs for Knowledge Base topics. Reads raw sources
  from knowledge-bases/{topic}/raw/, runs the Graphify 2-pass pipeline
  (Tree-sitter AST + semantic extraction), and outputs graph.json,
  GRAPH_REPORT.md, and optional Obsidian vault to knowledge-bases/{topic}/graphify-out/.
  Operates in frozen mode — no --watch, no hooks, manual invocation only.
  Use when the user asks to "build graphify", "graphify build", "run graphify
  on KB", "graphify-runner", "KB 그래프 빌드", "지식 그래프 생성",
  "graphify 실행", or wants to generate Graphify outputs for one or all
  KB topics.
  Do NOT use for querying existing graphs (use graphify-query).
  Do NOT use for compiling the markdown wiki (use kb-compile).
  Do NOT use for the full KB pipeline (use kb-orchestrator with --with-graphify).
  Korean triggers: "그래피파이 빌드", "지식 그래프 생성", "graphify 실행",
  "KB 그래프", "그래피파이 실행".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
  tags: ["knowledge-base", "graphify", "knowledge-graph", "frozen-mode"]
---

# Graphify Runner — Knowledge Graph Builder for KB Topics

Build Graphify knowledge graphs from KB raw sources. This skill wraps the Graphify Python API in a controlled, frozen-mode pipeline: no auto-sync, no watch mode, no hook installation. Every invocation is explicit and manual.

## Architecture Context

This skill runs **in parallel** with the existing `kb-compile` wiki builder. Both consume the same `raw/` sources but produce independent outputs:

| System | Input | Output | Purpose |
|--------|-------|--------|---------|
| kb-compile | `raw/` | `wiki/` | Structured markdown wiki with cross-references |
| graphify-runner | `raw/` | `graphify-out/` | Knowledge graph (JSON) + community detection + Obsidian vault |

Neither system modifies the other's output. They are complementary views of the same source material.

## Frozen Mode Constraints

- **No `--watch`**: Never enable filesystem watching
- **No `graphify hook install`**: Never install git/editor hooks
- **No `graphify claude install`**: Never register as a Claude Code slash command
- **No auto-mutation**: Graphify does not modify raw/ or wiki/ — it only writes to graphify-out/
- **Manual invocation only**: Run explicitly via this skill or kb-orchestrator --with-graphify

## Prerequisites

- `graphifyy` Python package installed (`pip install graphifyy`)
- Raw sources must exist in `knowledge-bases/{topic}/raw/`
- At least one supported file in raw/ (Markdown, PDF, images, code)

## Input / Output

**Input**: Topic name (single topic or "all" for every topic under `knowledge-bases/`)

**Output directory**: `knowledge-bases/{topic}/graphify-out/`

```
knowledge-bases/{topic}/graphify-out/
├── graph.json              # GraphRAG-ready knowledge graph
├── GRAPH_REPORT.md         # Community detection report with god nodes
├── obsidian/               # (optional) Obsidian vault with backlinks
│   ├── MOC.md
│   ├── {node}.md ...
│   └── {topic}.canvas
├── index.html              # (optional) Interactive vis.js graph
├── .graphify_detect.json   # File detection results
├── .graphify_extract.json  # Merged extraction (AST + semantic)
└── .graphify_analysis.json # Community/cohesion analysis
```

## Workflow

### Step 0 — Resolve Topics

```
If topic == "all":
    topics = list all subdirectories under knowledge-bases/ that contain a raw/ subdirectory
Else:
    topics = [topic]
    Verify knowledge-bases/{topic}/raw/ exists
```

### Step 1 — Verify Installation

```bash
python3 -c "import graphify; print('graphify OK')"
```

If import fails, run `pip install graphifyy` and retry. If still failing, stop with error.

### Step 2 — Per-Topic Build Loop

For each topic in topics, execute Steps 2a-2f sequentially.
Report progress: `[{i}/{total}] Building graphify for: {topic}`

#### Step 2a — Detect Files

```python
import json
from graphify.detect import detect
from pathlib import Path

input_path = Path(f"knowledge-bases/{topic}/raw")
result = detect(input_path)
output_dir = Path(f"knowledge-bases/{topic}/graphify-out")
output_dir.mkdir(parents=True, exist_ok=True)
Path(f"{output_dir}/.graphify_detect.json").write_text(json.dumps(result, indent=2))
```

Print summary: `Corpus: X files · ~Y words (code: N, docs: N, papers: N, images: N)`

If `total_files == 0`, skip this topic with a warning.

#### Step 2b — Extract (AST + Semantic)

**Part A — Structural extraction** (for code files only):

```python
from graphify.extract import collect_files, extract

code_files = []
for f in result.get('files', {}).get('code', []):
    p = Path(f)
    code_files.extend(collect_files(p) if p.is_dir() else [p])

if code_files:
    ast_result = extract(code_files)
else:
    ast_result = {'nodes': [], 'edges': [], 'input_tokens': 0, 'output_tokens': 0}

Path(f"{output_dir}/.graphify_ast.json").write_text(json.dumps(ast_result, indent=2))
```

**Part B — Semantic extraction** (for docs, papers, images):

Use subagents (Task tool) to extract semantic entities and relationships from non-code files. Split into chunks of 20-25 files, dispatch subagents in parallel, each following the Graphify extraction schema (nodes, edges, hyperedges with confidence scoring).

Each subagent must:
- Read assigned files from the raw/ directory
- Extract nodes (concepts, entities) and edges (relationships) with confidence labels (EXTRACTED/INFERRED/AMBIGUOUS)
- Return valid JSON matching the Graphify extraction schema

Merge all subagent results, deduplicating by node ID.

**Part C — Merge AST + Semantic**:

```python
# Merge AST nodes + semantic nodes, deduplicate by id
seen = {n['id'] for n in ast_result['nodes']}
merged_nodes = list(ast_result['nodes'])
for n in semantic_result['nodes']:
    if n['id'] not in seen:
        merged_nodes.append(n)
        seen.add(n['id'])

merged = {
    'nodes': merged_nodes,
    'edges': ast_result['edges'] + semantic_result['edges'],
    'hyperedges': semantic_result.get('hyperedges', []),
    'input_tokens': semantic_result.get('input_tokens', 0),
    'output_tokens': semantic_result.get('output_tokens', 0),
}
Path(f"{output_dir}/.graphify_extract.json").write_text(json.dumps(merged, indent=2))
```

#### Step 2c — Build Graph + Cluster + Analyze

```python
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_json

extraction = json.loads(Path(f"{output_dir}/.graphify_extract.json").read_text())
detection = json.loads(Path(f"{output_dir}/.graphify_detect.json").read_text())

G = build_from_json(extraction)
communities = cluster(G)
cohesion = score_all(G, communities)
gods = god_nodes(G)
surprises = surprising_connections(G, communities)
labels = {cid: f'Community {cid}' for cid in communities}
questions = suggest_questions(G, communities, labels)
tokens = {'input': extraction.get('input_tokens', 0), 'output': extraction.get('output_tokens', 0)}

report = generate(G, communities, cohesion, labels, gods, surprises, detection, tokens, str(input_path), suggested_questions=questions)
Path(f"{output_dir}/GRAPH_REPORT.md").write_text(report)
to_json(G, communities, f"{output_dir}/graph.json")

analysis = {
    'communities': {str(k): v for k, v in communities.items()},
    'cohesion': {str(k): v for k, v in cohesion.items()},
    'gods': gods,
    'surprises': surprises,
    'questions': questions,
}
Path(f"{output_dir}/.graphify_analysis.json").write_text(json.dumps(analysis, indent=2))
```

If graph is empty (0 nodes), stop this topic with error and continue to next.

Print: `Graph: N nodes, E edges, C communities`

#### Step 2d — Label Communities

Read `.graphify_analysis.json`. For each community, examine its node labels and assign a 2-5 word human-readable name.

Regenerate the report with real labels:

```python
from graphify.analyze import suggest_questions

labels = {0: "Example Label", 1: "Another Label"}  # actual labels
questions = suggest_questions(G, communities, labels)
report = generate(G, communities, cohesion, labels, gods, surprises, detection, tokens, str(input_path), suggested_questions=questions)
Path(f"{output_dir}/GRAPH_REPORT.md").write_text(report)
Path(f"{output_dir}/.graphify_labels.json").write_text(json.dumps({str(k): v for k, v in labels.items()}))
```

#### Step 2e — Export Obsidian Vault (Default)

```python
from graphify.export import to_obsidian, to_canvas

n = to_obsidian(G, communities, f"{output_dir}/obsidian", community_labels=labels, cohesion=cohesion)
to_canvas(G, communities, f"{output_dir}/obsidian/{topic}.canvas", community_labels=labels)
```

Print: `Obsidian vault: {n} notes + canvas`

#### Step 2f — Export Wiki Index (Optional)

If `--wiki` flag was given, generate a flat markdown wiki from the graph:

```python
from graphify.export import to_wiki
to_wiki(G, communities, f"{output_dir}/wiki", community_labels=labels)
```

### Step 3 — Summary Report

After all topics complete, print a consolidated summary:

```
Graphify Build Complete
═══════════════════════
Topics processed: N
  ✓ topic-1: 45 nodes, 78 edges, 5 communities
  ✓ topic-2: 23 nodes, 41 edges, 3 communities
  ✗ topic-3: skipped (no files in raw/)
Output: knowledge-bases/{topic}/graphify-out/
```

## Flags

| Flag | Default | Effect |
|------|---------|--------|
| (no flags) | — | Build graph + report + Obsidian vault |
| `--mode deep` | off | Aggressive INFERRED edge extraction |
| `--wiki` | off | Also generate flat markdown wiki |
| `--no-obsidian` | off | Skip Obsidian vault generation |
| `--no-viz` | off | Skip HTML visualization |

## Error Handling

- **Missing topic directory**: Stop with `knowledge-bases/{topic}/ not found`
- **Empty raw/ directory**: Skip topic with warning, continue to next
- **Graphify import failure**: Attempt `pip install graphifyy`, retry once
- **Empty graph (0 nodes)**: Log error for topic, continue to next
- **Subagent extraction failure**: If >50% of chunks fail, stop topic with error

## Intermediate File Persistence

All intermediate files are persisted in `knowledge-bases/{topic}/graphify-out/` for debuggability and resumability:

| File | Stage | Purpose |
|------|-------|---------|
| `.graphify_detect.json` | 2a | File detection results |
| `.graphify_ast.json` | 2b-A | AST extraction output |
| `.graphify_extract.json` | 2b-C | Merged extraction (AST + semantic) |
| `.graphify_analysis.json` | 2c | Community/cohesion analysis |
| `.graphify_labels.json` | 2d | Community labels |
| `graph.json` | 2c | Final knowledge graph |
| `GRAPH_REPORT.md` | 2d | Human-readable report |

## Verification

After build completes for a topic, verify:

1. `knowledge-bases/{topic}/graphify-out/graph.json` exists and is valid JSON
2. `knowledge-bases/{topic}/graphify-out/GRAPH_REPORT.md` exists and is non-empty
3. Graph has at least 1 node (empty graphs indicate extraction failure)

```bash
python3 -c "
import json
from pathlib import Path
g = json.loads(Path('knowledge-bases/{topic}/graphify-out/graph.json').read_text())
nodes = len(g.get('nodes', []))
edges = len(g.get('edges', []))
print(f'Verified: {nodes} nodes, {edges} edges')
assert nodes > 0, 'Empty graph'
"
```
