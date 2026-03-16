# Cognee Configuration Reference

Full environment variable registry and configuration deep-dive.

## Table of Contents

- [LLM Configuration](#llm-configuration)
- [Embedding Configuration](#embedding-configuration)
- [Database Configuration](#database-configuration)
- [Server Configuration](#server-configuration)
- [Storage Configuration](#storage-configuration)
- [Observability](#observability)
- [User Management](#user-management)
- [Programmatic Configuration](#programmatic-configuration)
- [Provider-Specific Setup](#provider-specific-setup)

## LLM Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `LLM_API_KEY` | API key for LLM provider | _(required)_ | `sk-...` |
| `LLM_PROVIDER` | LLM provider name | `openai` | `openai`, `anthropic`, `ollama`, `gemini`, `groq`, `custom` |
| `LLM_MODEL` | Model identifier | `openai/gpt-4o-mini` | `anthropic/claude-sonnet-4-20250514`, `ollama/llama3` |
| `LLM_ENDPOINT` | Custom API endpoint | _(auto from provider)_ | `http://localhost:11434` (Ollama) |
| `LLM_API_VERSION` | API version (Azure) | _(none)_ | `2024-12-01-preview` |
| `LLM_MAX_TOKENS` | Max output tokens | `16384` | `8192` |

### Rate Limiting

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_RATE_LIMIT_ENABLED` | Enable rate limiting | `false` |
| `LLM_RATE_LIMIT_REQUESTS` | Max requests per interval | `60` |
| `LLM_RATE_LIMIT_INTERVAL` | Interval in seconds | `60` |

## Embedding Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `EMBEDDING_PROVIDER` | Embedding provider | _(same as LLM)_ | `openai`, `gemini`, `fastembed` |
| `EMBEDDING_MODEL` | Embedding model name | _(auto)_ | `text-embedding-3-small` |
| `EMBEDDING_API_KEY` | Embedding API key | _(falls back to LLM_API_KEY)_ | `sk-...` |
| `EMBEDDING_ENDPOINT` | Custom embedding endpoint | _(auto)_ | `http://localhost:8080` |

## Database Configuration

### Relational Store (Metadata)

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_PROVIDER` | Database backend | `sqlite` |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DB_NAME` | Database name | `cognee_db` |
| `DB_USERNAME` | Database username | _(none)_ |
| `DB_PASSWORD` | Database password | _(none)_ |

### Vector Store

| Variable | Description | Default |
|----------|-------------|---------|
| `VECTOR_DB_PROVIDER` | Vector database | `lancedb` |
| `VECTOR_DB_URL` | Vector DB connection URL | _(local)_ |
| `VECTOR_DB_KEY` | Vector DB API key | _(none)_ |

Supported providers: `lancedb` (default/local), `pgvector`, `qdrant`, `weaviate`, `chromadb`

### Graph Store

| Variable | Description | Default |
|----------|-------------|---------|
| `GRAPH_DATABASE_PROVIDER` | Graph database | `kuzu` |
| `GRAPH_DATABASE_URL` | Graph DB URL | _(local)_ |
| `GRAPH_DATABASE_USERNAME` | Graph DB username | _(none)_ |
| `GRAPH_DATABASE_PASSWORD` | Graph DB password | _(none)_ |

Supported providers: `kuzu` (default/local), `neo4j`, `falkordb`, `networkx`

## Server Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | API server host | `0.0.0.0` |
| `ENVIRONMENT` | Environment mode | `local` |
| `DEBUG` | Debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `CORS_ALLOWED_ORIGINS` | CORS origins | `*` |

## Storage Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `STORAGE_BACKEND` | Storage backend | _(local filesystem)_ |
| `STORAGE_BUCKET_NAME` | S3 bucket name | _(none)_ |
| `CACHE_ROOT_DIRECTORY` | Cache directory | `.cognee_cache` |

## Observability

| Variable | Description | Default |
|----------|-------------|---------|
| `COGNEE_TRACING_ENABLED` | Enable OTEL tracing | `false` |
| `OTEL_SERVICE_NAME` | Service name for traces | `cognee` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP exporter endpoint | _(none)_ |
| `OTEL_EXPORTER_OTLP_HEADERS` | OTLP exporter headers | _(none)_ |
| `LANGFUSE_PUBLIC_KEY` | Langfuse public key | _(none)_ |
| `LANGFUSE_SECRET_KEY` | Langfuse secret key | _(none)_ |
| `LANGFUSE_HOST` | Langfuse host URL | _(none)_ |

## User Management

| Variable | Description | Default |
|----------|-------------|---------|
| `DEFAULT_USER_EMAIL` | Default user email | _(auto-generated)_ |
| `DEFAULT_USER_PASSWORD` | Default user password | _(auto-generated)_ |

## Programmatic Configuration

Configuration can also be set via the Python API:

```python
import cognee

cognee.config.set_llm_provider("openai")
cognee.config.set_llm_model("gpt-4o-mini")
cognee.config.set_llm_api_key("sk-...")
cognee.config.set_llm_endpoint("https://api.openai.com/v1")

cognee.config.set_vector_db_provider("lancedb")
cognee.config.set_graph_database_provider("kuzu")
```

Or via CLI:

```bash
cognee-cli config set llm_model gpt-4o-mini
cognee-cli config set graph_database_provider neo4j
cognee-cli config list
```

## Provider-Specific Setup

### OpenAI (default)

```bash
LLM_API_KEY="sk-..."
LLM_MODEL="openai/gpt-4o-mini"
LLM_PROVIDER="openai"
```

### Anthropic Claude

```bash
pip install cognee[anthropic]
LLM_API_KEY="sk-ant-..."
LLM_MODEL="anthropic/claude-sonnet-4-20250514"
LLM_PROVIDER="anthropic"
```

### Ollama (local)

```bash
pip install cognee[ollama]
LLM_PROVIDER="ollama"
LLM_MODEL="ollama/llama3"
LLM_ENDPOINT="http://localhost:11434"
```

### Azure OpenAI

```bash
LLM_PROVIDER="custom"
LLM_MODEL="azure/gpt-4o-mini"
LLM_ENDPOINT="https://your-resource.openai.azure.com/"
LLM_API_KEY="your-azure-key"
LLM_API_VERSION="2024-12-01-preview"
```

### PostgreSQL + pgvector

```bash
pip install cognee[postgres]
DB_PROVIDER="postgres"
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="cognee_db"
DB_USERNAME="postgres"
DB_PASSWORD="password"
VECTOR_DB_PROVIDER="pgvector"
```

### Neo4j

```bash
pip install cognee[neo4j]
GRAPH_DATABASE_PROVIDER="neo4j"
GRAPH_DATABASE_URL="bolt://localhost:7687"
GRAPH_DATABASE_USERNAME="neo4j"
GRAPH_DATABASE_PASSWORD="password"
```
