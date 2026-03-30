# Cognee API Reference

Detailed Python API and REST API documentation.

## Table of Contents

- [Python API](#python-api)
  - [cognee.add()](#cogneeadd)
  - [cognee.cognify()](#cogneecognify)
  - [cognee.search()](#cogneesearch)
  - [cognee.memify()](#cogneememify)
  - [cognee.delete()](#cogneedelete)
  - [cognee.config](#cogneeconfig)
  - [SearchType Enum](#searchtype-enum)
  - [Observability API](#observability-api)
- [REST API](#rest-api)
- [MCP Server](#mcp-server)
- [Complete Pipeline Example](#complete-pipeline-example)

## Python API

All Python API functions are async and must be called with `await`.

### `cognee.add()`

Ingest raw data for knowledge graph processing.

```python
await cognee.add(
    data: Union[str, List[str], BinaryIO],
    dataset_name: str = "main_dataset",
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `data` | `str`, `list[str]`, `BinaryIO` | Text, file path(s), directory path, URL, or binary stream |
| `dataset_name` | `str` | Dataset name for organizing data (default: `main_dataset`) |

**Supported input types:**
- Text strings: `"Your content here"`
- File paths: `"/path/to/document.pdf"`
- File URLs: `"file:///absolute/path"` or `"file://relative/path"`
- S3 paths: `"s3://bucket-name/path/to/file"`
- Lists: `["/path/to/doc1.pdf", "/path/to/doc2.txt"]`
- Directories: `"/path/to/docs/"` (recursively adds all files)

**Supported file formats:** `.txt`, `.md`, `.csv`, `.pdf`, `.png`, `.jpg`, `.jpeg`, `.mp3`, `.wav`, `.py`, `.js`, `.ts`, `.docx`, `.pptx`

### `cognee.cognify()`

Transform ingested data into a structured knowledge graph.

```python
await cognee.cognify(
    datasets: Optional[List[str]] = None,
    chunker = TextChunker,
    chunk_size: Optional[int] = None,
    ontology_file_path: Optional[str] = None,
    run_in_background: bool = False,
    chunks_per_batch: Optional[int] = None,
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `datasets` | `list[str]` | Dataset name(s) to process; all if None |
| `chunker` | class | Chunking strategy class (default: `TextChunker`) |
| `chunk_size` | `int` | Max tokens per chunk; auto-calculated if None |
| `ontology_file_path` | `str` | Path to RDF/OWL ontology for domain-specific entities |
| `run_in_background` | `bool` | Process asynchronously in background |
| `chunks_per_batch` | `int` | Chunks per processing batch (use 50 for large documents) |

**Processing pipeline:**
1. Document classification
2. Permission validation
3. Text chunking
4. Entity extraction
5. Relationship detection
6. Graph construction with embeddings
7. Content summarization

### `cognee.search()`

Search and query the knowledge graph.

```python
from cognee import SearchType

results = await cognee.search(
    query_text: str,
    query_type: SearchType = SearchType.GRAPH_COMPLETION,
    datasets: Optional[List[str]] = None,
    top_k: int = 10,
    system_prompt_path: str = "answer_simple_question.txt",
    system_prompt: Optional[str] = None,
    only_context: bool = False,
    session_id: Optional[str] = None,
    verbose: bool = False,
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `query_text` | `str` | Natural language question or search query |
| `query_type` | `SearchType` | Search mode (see SearchType enum below) |
| `datasets` | `list[str]` | Dataset(s) to search; all if None |
| `top_k` | `int` | Max results to return (default: 10) |
| `system_prompt_path` | `str` | Custom system prompt file for LLM search |
| `system_prompt` | `str` | Inline system prompt (overrides path) |
| `only_context` | `bool` | Return raw context without LLM generation |
| `session_id` | `str` | Session ID for caching interactions |
| `verbose` | `bool` | Include detailed graph representation in results |

### `cognee.memify()`

Enrich the knowledge graph with additional inferred relationships and reasoning.

```python
await cognee.memify()
```

### `cognee.delete()`

Remove data from the knowledge base.

```python
await cognee.delete(dataset_name: str)
```

### `cognee.prune.prune_system()`

Reset the entire cognee system (databases, caches, embeddings).

```python
await cognee.prune.prune_system()
```

### `cognee.visualize_graph()`

Generate a graph visualization.

```python
await cognee.visualize_graph()
```

### `cognee.config`

Programmatic configuration interface.

```python
cognee.config.set_llm_provider("openai")
cognee.config.set_llm_model("gpt-4o-mini")
cognee.config.set_llm_api_key("sk-...")
cognee.config.set_llm_endpoint("https://api.openai.com/v1")
cognee.config.set_vector_db_provider("lancedb")
cognee.config.set_graph_database_provider("kuzu")
```

### SearchType Enum

```python
from cognee import SearchType

SearchType.GRAPH_COMPLETION          # Graph-enhanced LLM Q&A (default)
SearchType.RAG_COMPLETION            # Traditional RAG without graph
SearchType.CHUNKS                    # Raw text chunks (vector similarity)
SearchType.CHUNKS_LEXICAL            # Lexical chunk matching (Jaccard)
SearchType.SUMMARIES                 # Pre-computed hierarchical summaries
SearchType.CYPHER                    # Direct Cypher graph queries
SearchType.FEELING_LUCKY             # Auto-selects best search type
SearchType.CODING_RULES              # Code-specific search
SearchType.TEMPORAL                  # Time-aware search
SearchType.NATURAL_LANGUAGE          # Natural language queries
SearchType.GRAPH_COMPLETION_COT      # Graph + chain-of-thought
SearchType.GRAPH_SUMMARY_COMPLETION  # Graph + summary-based completion
SearchType.TRIPLET_COMPLETION        # Triplet-based completion
```

### Observability API

```python
cognee.enable_tracing()
cognee.disable_tracing()
trace = cognee.get_last_trace()
all_traces = cognee.get_all_traces()
cognee.clear_traces()
```

## REST API

Cognee exposes a FastAPI server on port 8000.

### Start the Server

```bash
cognee-cli -ui
# Or directly:
uvicorn cognee.api.server:app --host 0.0.0.0 --port 8000
```

### Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/add` | Add data |
| `POST` | `/api/v1/cognify` | Build knowledge graph |
| `POST` | `/api/v1/search` | Search the graph |
| `DELETE` | `/api/v1/datasets/{id}` | Delete a dataset |
| `GET` | `/api/v1/datasets` | List datasets |
| `GET` | `/api/v1/settings` | Get current settings |
| `POST` | `/api/v1/settings` | Update settings |

### Example: REST API Usage

```bash
# Add text data
curl -X POST http://localhost:8000/api/v1/add \
  -H "Content-Type: application/json" \
  -d '{"data": "Your text content", "dataset_name": "demo"}'

# Build knowledge graph
curl -X POST http://localhost:8000/api/v1/cognify \
  -H "Content-Type: application/json" \
  -d '{"datasets": ["demo"]}'

# Search
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query_text": "What is this about?", "query_type": "GRAPH_COMPLETION"}'
```

### OpenAPI Spec

Full OpenAPI specification available at: `https://docs.cognee.ai/cognee_openapi_spec.json`

When the server is running: `http://localhost:8000/docs` (Swagger UI)

## MCP Server

Cognee includes an MCP server for IDE integration.

```bash
# Start with docker-compose
docker-compose up -d cognee-mcp
# Available at http://localhost:8001
```

## Complete Pipeline Example

```python
import cognee
import asyncio

async def full_pipeline():
    # 1. Configure (optional — can also use env vars)
    cognee.config.set_llm_model("gpt-4o-mini")

    # 2. Add data from multiple sources
    await cognee.add("AI is transforming software development.", dataset_name="tech")
    await cognee.add("/path/to/research.pdf", dataset_name="tech")

    # 3. Build knowledge graph
    await cognee.cognify(datasets=["tech"])

    # 4. Search with different modes
    # Graph-enhanced Q&A
    answers = await cognee.search(
        "How is AI transforming development?",
        query_type=cognee.SearchType.GRAPH_COMPLETION,
        datasets=["tech"],
    )
    print("Graph Q&A:", answers)

    # Raw chunks for citations
    chunks = await cognee.search(
        "AI development",
        query_type=cognee.SearchType.CHUNKS,
        top_k=5,
    )
    print("Chunks:", chunks)

    # 5. Optional: enrich graph
    await cognee.memify()

asyncio.run(full_pipeline())
```
