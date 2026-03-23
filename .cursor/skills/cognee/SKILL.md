---
name: cognee
description: >-
  Build persistent AI memory and knowledge graphs from documents using the
  cognee knowledge engine (CLI + Python API). Ingest text, PDF, DOCX, CSV,
  images, and audio; extract entities and relationships; search with
  graph-enhanced RAG. Use when the user asks to "build knowledge graph",
  "create AI memory", "semantic search over documents", "cognee add",
  "cognee cognify", "cognee search", "ingest documents", "index documents
  for RAG", or wants to convert documents into a searchable knowledge base.
  Do NOT use for general web search (use WebSearch).
  Do NOT use for paper review (use paper-review if available).
  Do NOT use for general web scraping (use scrapling or defuddle).
  Korean triggers: "지식 그래프", "AI 메모리", "시맨틱 검색", "문서 인덱싱",
  "cognee", "지식 엔진".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---

# Cognee — Knowledge Engine

Build persistent, learnable AI memory from diverse data sources. Cognee combines vector search + graph DB + cognitive science to create knowledge graphs that enable semantic search, entity-relationship extraction, and agent memory.

## Prerequisites

1. **Python 3.10+** required
2. **Install cognee**:

```bash
pip install cognee
# or with uv
uv pip install cognee
```

3. **Set environment variables** (minimal):

```bash
export LLM_API_KEY="your-openai-api-key"  # pragma: allowlist secret
export LLM_MODEL="openai/gpt-4o-mini"
export LLM_PROVIDER="openai"
```

See [references/configuration.md](references/configuration.md) for the full env var registry and [references/api-reference.md](references/api-reference.md) for detailed Python/REST API documentation.

4. **Optional extras** — install only what you need:

| Extra | Command | Purpose |
|-------|---------|---------|
| `postgres` | `pip install cognee[postgres]` | PostgreSQL + pgvector backend |
| `neo4j` | `pip install cognee[neo4j]` | Neo4j graph database |
| `anthropic` | `pip install cognee[anthropic]` | Anthropic Claude LLM |
| `ollama` | `pip install cognee[ollama]` | Ollama local models |
| `docs` | `pip install cognee[docs]` | Unstructured document parsing (DOCX, PPTX, XLSX) |
| `scraping` | `pip install cognee[scraping]` | Web scraping (Tavily, Playwright) |
| `codegraph` | `pip install cognee[codegraph]` | Code graph analysis |
| `graphiti` | `pip install cognee[graphiti]` | Graphiti integration |

## Workflow

### Step 1: Add Data

Ingest raw data into cognee. Accepts text strings, file paths, directories, and URLs.

**CLI:**

```bash
cognee-cli add "Your text content here"
cognee-cli add /path/to/document.pdf --dataset-name my_dataset
cognee-cli add /path/to/docs/ --dataset-name onboarding
```

**Python API:**

```python
import cognee

await cognee.add("Cognee turns documents into AI memory.")
await cognee.add("/path/to/file.pdf", dataset_name="research")
await cognee.add(["/path/to/doc1.pdf", "/path/to/doc2.txt"], dataset_name="batch")
```

Supported formats: `.txt`, `.md`, `.csv`, `.pdf`, `.png`, `.jpg`, `.mp3`, `.wav`, `.py`, `.js`, `.docx`, `.pptx`

### Step 2: Build Knowledge Graph (Cognify)

Process ingested data into a structured knowledge graph with entities, relationships, and embeddings.

**CLI:**

```bash
cognee-cli cognify
cognee-cli cognify --datasets my_dataset onboarding
cognee-cli cognify --background --verbose
```

**Python API:**

```python
await cognee.cognify()
await cognee.cognify(datasets=["my_dataset"])
```

### Step 3: Search

Query the knowledge graph. Multiple search modes available.

**CLI:**

```bash
cognee-cli search "What are the key findings?"
cognee-cli search "Summarize the research" --query-type GRAPH_COMPLETION
cognee-cli search "Find mentions of AI" --query-type CHUNKS --top-k 5
cognee-cli search "Query" --datasets my_dataset --output-format json
```

**Python API:**

```python
from cognee import SearchType

results = await cognee.search("What does Cognee do?")
results = await cognee.search(
    "Find all entities related to machine learning",
    query_type=SearchType.GRAPH_COMPLETION,
    datasets=["research"],
    top_k=10,
)
```

### Step 4 (Optional): Memify

Enrich the existing graph with additional inferred relationships.

```python
await cognee.memify()
```

## Search Types

| Type | Speed | Best For |
|------|-------|----------|
| `GRAPH_COMPLETION` | Slower | Complex questions, analysis, summaries (default) |
| `RAG_COMPLETION` | Medium | Direct document retrieval, fact-finding |
| `CHUNKS` | Fast | Finding specific passages, citations |
| `CHUNKS_LEXICAL` | Fast | Exact-term matching, keyword lookup |
| `SUMMARIES` | Fast | Quick overviews, document abstracts |
| `CYPHER` | Variable | Direct graph queries (advanced) |
| `FEELING_LUCKY` | Variable | Auto-selects the best search type |
| `CODING_RULES` | Medium | Code-specific search |

## CLI Quick Reference

| Command | Description |
|---------|-------------|
| `cognee-cli add <data> [-d name]` | Add text, files, or directories |
| `cognee-cli cognify [-d name] [-b] [-v]` | Build knowledge graph |
| `cognee-cli search <query> [-t type] [-k N]` | Search the graph |
| `cognee-cli delete [-d name] [--all]` | Delete datasets |
| `cognee-cli config list` | List configuration keys |
| `cognee-cli config set <key> <value>` | Set a config value |
| `cognee-cli config get [key]` | Get a config value |
| `cognee-cli -ui` | Start web UI (port 3000) + API (port 8000) |
| `cognee-cli --version` | Show version |

## Docker Usage

```bash
docker pull cognee/cognee:latest

docker-compose up -d cognee
docker-compose --profile postgres --profile neo4j up -d
```

Web UI at `http://localhost:3000`, API at `http://localhost:8000`.

## Examples

### Example 1: Index project documentation

**User says:** "Index all the markdown files in docs/ into a knowledge graph"

**Actions:**
1. Run `cognee-cli add docs/ --dataset-name project_docs`
2. Run `cognee-cli cognify --datasets project_docs --verbose`
3. Confirm completion

**Result:** Knowledge graph built from all docs; ready for semantic search.

### Example 2: Search ingested documents

**User says:** "What does the architecture documentation say about caching?"

**Actions:**
1. Run `cognee-cli search "caching architecture" --datasets project_docs --top-k 5`
2. Parse and present results to the user

**Result:** Graph-enhanced answer synthesizing relevant passages about caching.

### Example 3: Full Python pipeline

**User says:** "Write a script to ingest this PDF and search it"

**Actions:**
1. Write an async Python script using `cognee.add()`, `cognee.cognify()`, `cognee.search()`

```python
import cognee
import asyncio

async def main():
    await cognee.add("/path/to/report.pdf", dataset_name="reports")
    await cognee.cognify(datasets=["reports"])
    results = await cognee.search("key findings", datasets=["reports"])
    for r in results:
        print(r)

asyncio.run(main())
```

**Result:** End-to-end pipeline script for document ingestion and search.

### Example 4: Clean reset and re-index

**User says:** "Delete everything and re-index from scratch"

**Actions:**
1. Run `cognee-cli delete --all --force`
2. Run `cognee-cli add /path/to/data/ --dataset-name fresh`
3. Run `cognee-cli cognify --datasets fresh`

**Result:** Fresh knowledge graph from clean state.

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| Missing API key | `LLM_API_KEY not set` or auth error | Set `LLM_API_KEY` env var |
| Model not found | `Model X not available` | Check `LLM_MODEL` matches provider; e.g. `openai/gpt-4o-mini` |
| No data added | `SearchPreconditionError` | Run `cognee.add()` then `cognee.cognify()` before searching |
| Dataset not found | `No datasets found` | Verify dataset name with `cognee-cli config list` |
| Import error | `ModuleNotFoundError` for extras | Install the required extra: `pip install cognee[postgres]` |
| DB connection error | PostgreSQL/Neo4j connection refused | Check DB is running and env vars are set correctly |
| Large dataset timeout | Processing hangs on large files | Use `--background` flag or `--chunks-per-batch 50` |
| Embedding dimension mismatch | Vector store error after changing models | Delete and rebuild: `cognee.prune.prune_system()` |
