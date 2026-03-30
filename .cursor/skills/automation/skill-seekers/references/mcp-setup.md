# Skill Seekers MCP Server Setup

## Installation

```bash
pip install skill-seekers[mcp]
```

## Transport Options

### HTTP Transport (recommended for Cursor)

Start the server:

```bash
python -m skill_seekers.mcp.server_fastmcp --transport http --port 8765
```

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "skill-seekers": {
      "url": "http://localhost:8765/sse"
    }
  }
}
```

### stdio Transport

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "skill-seekers": {
      "command": "python",
      "args": ["-m", "skill_seekers.mcp.server_fastmcp"],
      "cwd": "/path/to/Skill_Seekers",
      "env": {}
    }
  }
}
```

Replace `/path/to/Skill_Seekers` with the actual path where Skill Seekers is installed or cloned.

## Available MCP Tools (26 total)

### Core Tools (9)

| Tool | Description |
|------|-------------|
| `list_configs` | List available scraping configuration presets |
| `generate_config` | Generate a config file for a documentation URL |
| `validate_config` | Validate a config file for correctness |
| `estimate_pages` | Estimate pages to be scraped from a URL |
| `scrape_docs` | Scrape documentation from a URL or config |
| `package_skill` | Package scraped output for a target platform |
| `upload_skill` | Upload packaged skill to cloud storage |
| `enhance_skill` | Run enhancement pass on scraped content |
| `install_skill` | Full pipeline: scrape + enhance + package + install |

### Extended Tools (10)

| Tool | Description |
|------|-------------|
| `scrape_github` | Scrape a GitHub repository (code + docs + insights) |
| `scrape_pdf` | Extract content from PDF files |
| `unified_scrape` | Multi-source scrape from unified config |
| `merge_sources` | Merge multiple scraped source directories |
| `detect_conflicts` | Detect conflicts with existing installed skills |
| `add_config_source` | Add a source to unified config |
| `fetch_config` | Fetch a preset config by name |
| `list_config_sources` | List sources in a unified config |
| `remove_config_source` | Remove a source from unified config |
| `split_config` | Split a unified config into individual configs |

### Vector Database Tools (4)

| Tool | Description |
|------|-------------|
| `export_to_chroma` | Export to ChromaDB vector store |
| `export_to_weaviate` | Export to Weaviate vector store |
| `export_to_faiss` | Export to FAISS vector store |
| `export_to_qdrant` | Export to Qdrant vector store |

### Cloud Storage Tools (3)

| Tool | Description |
|------|-------------|
| `cloud_upload` | Upload to S3/GCS/Azure Blob |
| `cloud_download` | Download from cloud storage |
| `cloud_list` | List files in cloud storage |

## Verifying the MCP Server

After adding to `.cursor/mcp.json`, restart Cursor. The MCP tools should appear in the tool list. Test with:

```
Use skill-seekers to list available config presets
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `GITHUB_TOKEN` | GitHub API token for repo scraping (optional, avoids rate limits) |
| `OPENAI_API_KEY` | Required for video transcription (Whisper) |
| `AWS_*` / `GCS_*` / `AZURE_*` | Cloud storage credentials (optional) |
