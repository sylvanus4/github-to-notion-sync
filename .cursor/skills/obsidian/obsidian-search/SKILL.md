---
name: obsidian-search
description: >-
  Search Obsidian vault content, query backlinks, outgoing links, orphan
  notes, and dead-end notes via the CLI. Use when the user asks to search
  notes, find backlinks, check links, find orphan notes, find dead-end
  notes, get link context, or explore the vault graph. Do NOT use for
  file CRUD (use obsidian-files), daily notes (use obsidian-daily), tags
  or tasks (use obsidian-notes), or plugin management (use obsidian-admin).
  Korean triggers: "옵시디언 검색", "노트 검색", "백링크", "링크 찾기",
  "고아 노트", "데드엔드", "옵시디언 그래프", "연결된 노트".
metadata:
  version: "1.0.0"
  category: "integration"
---
# Obsidian CLI — Search & Link Graph

> **Requires:** Obsidian app running, CLI in PATH. See `obsidian-setup`.

## Prerequisites

- Obsidian CLI configured (`obsidian-setup`)
- Target vault open in Obsidian

## Quick Commands

### Full-Text Search

```bash
obsidian search query="meeting notes"               # basic search
obsidian search query="project:alpha status:active"  # complex query
obsidian search query="tag:#important"               # search by tag
```

### Contextual Search

```bash
obsidian search:context query="API design" lines=3   # search with surrounding lines
```

### Link Graph

```bash
# Backlinks — who links TO this note
obsidian backlinks file="Architecture"

# Outgoing links — what this note links TO
obsidian links file="Architecture"

# Orphan notes — notes with NO incoming links
obsidian orphans

# Dead-end notes — notes with NO outgoing links
obsidian deadends
```

## Discovering Commands

```bash
obsidian help search           # search command options
obsidian help backlinks        # backlink query details
obsidian help links            # outgoing link details
```

## Common Patterns

### Find all references to a concept

```bash
obsidian search query="kubernetes"
obsidian backlinks file="Kubernetes Guide"
```

### Vault hygiene — find disconnected notes

```bash
obsidian orphans       # notes nobody links to
obsidian deadends      # notes that link to nothing
```

### Research — gather context

```bash
obsidian search:context query="fine-tuning" lines=5
obsidian links file="LLM Training"
```

### Map a topic cluster

```bash
obsidian backlinks file="Trading Strategy"
obsidian links file="Trading Strategy"
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `No results` | Query too specific or vault not indexed | Simplify query; wait for Obsidian to index |
| `File not found` | Wrong file path for backlinks/links | Check exact note name with `obsidian list` |
| `Timeout` | Large vault search | Narrow query scope |
