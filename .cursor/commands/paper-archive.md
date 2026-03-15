---
description: Manage the paper archive — register, search, browse, deduplicate, and sync papers across NotebookLM and Notion.
---

## Paper Archive

Central catalog for all reviewed, discovered, and scouted papers. Provides
search, deduplication, relationship tracking, and sync to NotebookLM/Notion.

### Usage

```bash
/paper-archive register <arXiv-ID or URL>
/paper-archive list [--status reviewed|discovered|all] [--tag TAG]
/paper-archive search <query>
/paper-archive check <arXiv-ID or URL>
/paper-archive relate <paper-A> <paper-B> [--type cites|extends|contradicts|related|supersedes]
/paper-archive graph [paper-ID]
/paper-archive sync-nlm
/paper-archive sync-notion
/paper-archive stats
/paper-archive export [--format md|json]
```

### Sub-Commands

| Command | Description |
|---------|-------------|
| `register` | Add a paper to the archive with auto-fetched metadata |
| `list` | Browse papers with status/tag filters |
| `search` | Full-text search across titles, tags, summaries, authors |
| `check` | Dedup check — is this paper already archived? |
| `relate` | Add a relationship between two papers |
| `graph` | Show relationship graph (mermaid diagram) |
| `sync-nlm` | Sync reviewed papers to a NotebookLM "Paper Library" notebook |
| `sync-notion` | Sync reviewed papers to the Notion paper database |
| `stats` | Archive summary statistics |
| `export` | Export as markdown report or JSON |

### Examples

```bash
# Register a new paper
/paper-archive register https://arxiv.org/abs/2603.03823

# Check if a paper is already in the archive
/paper-archive check 2603.01145

# List all reviewed papers tagged with "llm-agents"
/paper-archive list --status reviewed --tag llm-agents

# Search for papers about code generation
/paper-archive search "code generation benchmark"

# Link two papers
/paper-archive relate 2603.03823 2603.01145 --type cites

# View relationships for a paper
/paper-archive graph 2603.03823

# Sync all reviewed papers to NotebookLM
/paper-archive sync-nlm

# Show archive statistics
/paper-archive stats

# Export the full archive as markdown
/paper-archive export --format md
```

### Skill Reference

This command uses the **paper-archive** skill at `.cursor/skills/paper-archive/SKILL.md`.
Read and follow the skill instructions before proceeding.

User input:

$ARGUMENTS
