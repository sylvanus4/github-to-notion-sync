## Obsidian

Search, create, and manage notes in an Obsidian vault with wikilinks, backlinks, and index consistency.

### Usage

```
/obsidian search "kubernetes"          # search vault content
/obsidian create "Meeting Notes"       # create a new note
/obsidian backlinks "Project Alpha"    # find all backlinks to a note
/obsidian orphans                      # find orphan notes without links
```

### Workflow

1. **Navigate** — Search vault content, list backlinks, find orphan notes
2. **Create** — Add new notes with proper wikilinks and frontmatter
3. **Link** — Maintain bidirectional link consistency across the vault
4. **Organize** — Index notes, detect dead-end and orphan notes
5. **Sync** — Optionally bridge vault content to the Knowledge Base pipeline

### Execution

Read and follow the `obsidian-files` skill (`.cursor/skills/obsidian/obsidian-files/SKILL.md`) for file CRUD. Use `obsidian-search` (`.cursor/skills/obsidian/obsidian-search/SKILL.md`) for search and backlink queries. Use `obsidian-notes` (`.cursor/skills/obsidian/obsidian-notes/SKILL.md`) for metadata and tags.

### Examples

Search the vault:
```
/obsidian search "deployment checklist"
```

Find orphan notes:
```
/obsidian orphans
```
