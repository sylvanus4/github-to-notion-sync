---
name: obsidian-notes
description: >-
  Manage Obsidian note metadata — tags, tasks, properties (frontmatter),
  templates, outlines, word counts, and bases via the CLI. Use when the user
  asks to manage tags, list tasks, edit properties, apply templates, view note
  outline, check word count, or work with Obsidian Bases. Do NOT use for file
  CRUD (use obsidian-files), daily notes (use obsidian-daily), search (use
  obsidian-search), plugin management (use obsidian-admin), or developer tools
  (use obsidian-dev). Korean triggers: "옵시디언 태그", "태그 관리", "옵시디언 작업", "할일 목록",
  "프로퍼티", "프론트매터", "옵시디언 템플릿", "노트 개요", "단어 수", "옵시디언 베이스".
---

# Obsidian CLI — Notes Metadata & Content

> **Requires:** Obsidian app running, CLI in PATH. See `obsidian-setup`.

## Prerequisites

- Obsidian CLI configured (`obsidian-setup`)
- Target vault open in Obsidian
- Templates core plugin enabled (for template commands)

## Quick Commands

### Tags

```bash
obsidian tags                                  # list all tags in vault
obsidian tags file="Project Alpha"             # list tags in specific file
obsidian tag:add file="Note" tag="important"   # add tag to note
obsidian tag:remove file="Note" tag="draft"    # remove tag from note
```

### Tasks

```bash
obsidian tasks                                 # list all tasks in vault
obsidian tasks daily                           # tasks from today's daily note
obsidian tasks file="Sprint Plan"              # tasks in specific file
obsidian tasks status=incomplete               # filter incomplete tasks
obsidian tasks status=complete                 # filter completed tasks
```

### Properties (Frontmatter)

```bash
obsidian properties file="Note"                           # view all properties
obsidian property:set file="Note" key="status" value="active"  # set property
obsidian property:get file="Note" key="status"            # get single property
obsidian property:remove file="Note" key="draft"          # remove property
```

### Templates

```bash
obsidian templates                             # list available templates
obsidian template:insert file="Note" template="Meeting"   # apply template
```

### Outline & Content Analysis

```bash
obsidian outline file="Architecture"           # heading structure
obsidian wordcount file="Report"               # word/char count
obsidian wordcount                             # current file stats
```

### Bases (Obsidian Databases)

```bash
obsidian bases                                 # list all bases
obsidian base:query name="Tasks DB"            # query a base
obsidian base:add name="Tasks DB" data="..."   # add row to base
```

## Discovering Commands

```bash
obsidian help tags             # tag management
obsidian help tasks            # task querying
obsidian help properties       # frontmatter management
obsidian help templates        # template operations
obsidian help outline          # outline commands
obsidian help bases            # Obsidian Bases
```

## Common Patterns

### Audit vault health

```bash
obsidian tags                  # overview of tag taxonomy
obsidian tasks status=incomplete  # outstanding work
```

### Standardize note metadata

```bash
obsidian property:set file="Design Doc" key="type" value="design"
obsidian property:set file="Design Doc" key="status" value="review"
obsidian tag:add file="Design Doc" tag="architecture"
```

### Batch template application

Apply a standard template to newly created notes:

```bash
obsidian create name="Meeting 2024-04-05"
obsidian template:insert file="Meeting 2024-04-05" template="Meeting"
```

### Export task inventory

```bash
obsidian tasks status=incomplete   # pipe to downstream tools
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Property type mismatch` | Setting wrong type for existing property | Check property type in Obsidian settings |
| `Template not found` | Template name doesn't match | Run `obsidian templates` to list available names |
| `Bases not available` | Feature not enabled or older version | Ensure Obsidian >= 1.12 with Bases enabled |
| `Tag format invalid` | Special characters in tag | Use alphanumeric and hyphens only |
