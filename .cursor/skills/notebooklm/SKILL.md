---
name: notebooklm
description: >-
  Manage Google NotebookLM notebooks, sources, notes, queries, and sharing via
  the notebooklm-mcp MCP server. Use when the user asks to "list notebooks",
  "create a notebook", "add a source", "add URL to notebook", "query notebook",
  "ask notebook", "share notebook", "manage notes", "delete notebook",
  "rename notebook", "sync Drive sources", "get source content",
  "노트북LM", "노트북 생성", "노트북 목록", "소스 추가", "노트북 공유",
  "노트북 질문", "노트북 삭제", "노트 관리", "NLM 노트북",
  "NotebookLM", "NLM", "nlm notebook", "notebook source", "nlm query",
  or any notebook/source/note CRUD operation.
  Do NOT use for content generation (audio, video, reports, quizzes, slides,
  flashcards, mind maps, infographics, data tables) -- use notebooklm-studio.
  Do NOT use for web/Drive research pipelines -- use notebooklm-research.
  Do NOT use for general web search -- use parallel-web-search.
metadata:
  author: thaki
  version: 1.0.0
  category: integration
---

# NotebookLM: Core Notebook Management

Manage Google NotebookLM notebooks, sources, notes, queries, and sharing through the `notebooklm-mcp` MCP server (29 tools total; this skill covers 20 core tools).

## Prerequisites

The `notebooklm-mcp` MCP server must be registered in `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "notebooklm-mcp": {
      "command": "notebooklm-mcp"
    }
  }
}
```

Authentication is required before first use:

```bash
nlm login          # launches browser for Google cookie extraction
nlm login --check  # verify auth status
```

Cookies persist for 2-4 weeks. The server auto-refreshes CSRF tokens on failure.

## Available Tools

### Notebooks (6 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `notebook_list` | List all notebooks | -- |
| `notebook_create` | Create a new notebook | `title` (required) |
| `notebook_get` | Get notebook details with sources | `notebook_id` (required) |
| `notebook_describe` | Get AI summary and suggested topics | `notebook_id` (required) |
| `notebook_rename` | Rename a notebook | `notebook_id`, `title` (required) |
| `notebook_delete` | Delete a notebook | `notebook_id`, `confirm=True` (required) |

### Sources (6 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `source_add` | Add URL, text, file, or Drive source | `notebook_id`, `source_type` (url/text/file/drive), type-specific params |
| `source_list_drive` | List sources with Drive freshness status | `notebook_id` |
| `source_sync_drive` | Sync stale Drive sources | `notebook_id` |
| `source_delete` | Delete a source | `notebook_id`, `source_id`, `confirm=True` |
| `source_describe` | Get AI summary with keywords | `notebook_id`, `source_id` |
| `source_get_content` | Get raw text content of a source | `notebook_id`, `source_id` |

**`source_add` parameter reference:**

```
source_type="url"   → url="https://..."
source_type="text"  → text="...", title="..."
source_type="file"  → file_path="/path/to.pdf"
source_type="drive" → document_id="...", doc_type="doc|slides|sheets|pdf"

Common options: wait=True (block until processed), wait_timeout=120
```

### Querying (2 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `notebook_query` | Ask AI about sources in notebook | `notebook_id`, `query` |
| `chat_configure` | Set chat goal and response length | `notebook_id`, `goal`, `response_length` |

### Notes (1 unified tool)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `note` | Manage notes (list/create/update/delete) | `notebook_id`, `action`, `content`, `title`, `note_id`, `confirm` |

**`note` action reference:**

```
action="list"                                    → list all notes
action="create", content="...", title="..."      → create a note
action="update", note_id="...", content="..."    → update a note
action="delete", note_id="...", confirm=True     → delete a note
```

### Sharing (3 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `notebook_share_status` | Get sharing settings | `notebook_id` |
| `notebook_share_public` | Enable/disable public link | `notebook_id`, `enabled` (bool) |
| `notebook_share_invite` | Invite collaborator by email | `notebook_id`, `email`, `role` (editor/viewer) |

### Auth & Server (2 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `refresh_auth` | Reload auth tokens | -- |
| `server_info` | Get version and check for updates | -- |

## Common Workflows

### Create a notebook and add sources

1. `notebook_create(title="Stock Analysis Q1 2026")`
2. `source_add(notebook_id, source_type="url", url="https://...", wait=True)`
3. `source_add(notebook_id, source_type="text", text="...", title="Meeting Notes")`
4. `notebook_query(notebook_id, query="What are the key trends?")`

### Add a local file as source

```
source_add(notebook_id, source_type="file", file_path="/path/to/report.pdf", wait=True)
```

### Sync Google Drive sources

1. `source_list_drive(notebook_id)` -- check freshness status
2. `source_sync_drive(notebook_id)` -- sync stale sources

### Share a notebook publicly

1. `notebook_share_public(notebook_id, enabled=True)`
2. `notebook_share_status(notebook_id)` -- get the public link

### Stock analytics integration

After generating a daily report with the `today` skill:

1. `notebook_create(title="Daily Report 2026-03-08")`
2. `source_add(notebook_id, source_type="file", file_path="outputs/reports/daily-2026-03-08.docx")`
3. `notebook_query(notebook_id, query="Summarize the buy/sell signals")`

### Load sources for accelerated learning

1. `notebook_create(title="Deep Learn: Machine Learning")`
2. Upload multiple sources:
   - `source_add(notebook_id, source_type="file", file_path="/path/to/textbook1.pdf", wait=True)`
   - `source_add(notebook_id, source_type="url", url="https://arxiv.org/...", wait=True)`
   - `source_add(notebook_id, source_type="text", text="<lecture transcript>", title="Lecture 1", wait=True)`
3. `notebook_query(notebook_id, query="What are the 5 core mental models that every expert in this field shares?")`

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Auth expired | Run `nlm login` or call `refresh_auth` MCP tool |
| "Session not found" | Restart Cursor to reconnect MCP server |
| Rate limited | Free tier: ~50 queries/day; wait or upgrade |
| Source stuck processing | Call `source_add` with `wait=True, wait_timeout=300` |

## CLI Reference

The `nlm` CLI provides direct terminal access to the same operations:

```bash
nlm notebook list
nlm notebook create "My Notebook"
nlm source add <notebook_id> --url "https://..."
nlm notebook query <notebook_id> "summarize this"
nlm share public <notebook_id>
nlm login --check
nlm doctor
```

## Related Skills

- **notebooklm-studio** -- content generation (audio, video, reports, quizzes, slides, infographics)
- **notebooklm-research** -- web/Drive research pipelines
- **nlm-deep-learn** -- accelerated learning pipeline (mental models, debates, deep-understanding quizzes)

## Examples

### Example 1: Standard usage

**User says:** "List notebooks"

**Actions:**
1. Gather necessary context from the project and user
2. Execute the skill workflow as documented above
3. Deliver results and verify correctness