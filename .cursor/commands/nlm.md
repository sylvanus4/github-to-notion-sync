## NotebookLM

Manage Google NotebookLM notebooks, sources, notes, queries, and sharing.

### Usage

```
/nlm                                          # interactive — list notebooks and choose action
/nlm list                                     # list all notebooks
/nlm create "My Research Notebook"            # create a new notebook
/nlm add <notebook> --url "https://..."       # add a URL source
/nlm add <notebook> --file "/path/to/doc.pdf" # add a local file
/nlm query <notebook> "summarize key points"  # query notebook AI
/nlm share <notebook>                         # manage sharing
/nlm notes <notebook>                         # manage notes
```

### Execution

Read and follow `.cursor/skills/notebooklm/SKILL.md`.

Use the `notebooklm-mcp` MCP server tools: `notebook_list`, `notebook_create`, `notebook_get`, `source_add`, `notebook_query`, `notebook_share_*`, `note`.

### Examples

List notebooks:
```
/nlm list
```

Create and populate a notebook:
```
/nlm create "Stock Analysis Q1 2026"
```

Add a source to a notebook:
```
/nlm add <notebook_id> --url "https://finance.yahoo.com/news/..."
```

Query a notebook:
```
/nlm query <notebook_id> "What are the key buy signals?"
```
