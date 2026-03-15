---
description: Publish local markdown files as structured Notion sub-pages under a parent page
argument-hint: "<file-or-folder> --parent <notion-page-id>"
---

## md-to-notion

Publish local markdown files (single file or entire folder) as Notion sub-pages.
Extracts H1 headings as page titles, converts pipe tables to bulleted lists for
Notion compatibility, and batch-creates pages via MCP.

### Usage

```
/md-to-notion <file.md> --parent <notion-page-id>
/md-to-notion <folder/> --parent <notion-page-id>
/md-to-notion <folder/> --parent <id> --icon 📋
/md-to-notion <folder/> --parent <id> --skip-meta
/md-to-notion <folder/> --parent <id> --title-prefix "Sprint2: "
/md-to-notion <folder/> --parent <id> --dry-run
/md-to-notion <file.md> --parent <id> --no-table-convert
```

### Options

| Option | Description |
|--------|-------------|
| (positional) | File path or folder path containing `.md` files |
| `--parent <id>` | **(Required)** Notion parent page ID for sub-pages |
| `--icon <emoji>` | Apply a uniform emoji icon to all created pages |
| `--skip-meta` | Skip README.md, CHANGELOG.md, LICENSE.md |
| `--no-table-convert` | Keep pipe tables as-is (skip conversion to lists) |
| `--title-prefix <str>` | Prepend a string to each page title |
| `--dry-run` | List files and extracted titles without creating pages |

### Workflow

1. **Resolve** -- Collect `.md` file paths from input (single file or recursive glob)
2. **Parse** -- Extract H1 as title, strip it from body, convert pipe tables
3. **Publish** -- Batch-create Notion sub-pages via `notion-create-pages` MCP
4. **Verify** -- Fetch parent page and confirm all sub-pages are visible

### Execution

Read and follow the `md-to-notion` skill (`.cursor/skills/md-to-notion/SKILL.md`).

### Examples

Upload a single markdown file:
```
/md-to-notion output/meetings/2026-03-14/summary.md --parent 3239eddc34e680e8a7a5d5b5eac18b38
```

Upload an entire folder with icon:
```
/md-to-notion output/meetings/2026-03-14/ --parent 3239eddc34e680e8a7a5d5b5eac18b38 --icon 📋
```

Preview what would be uploaded (dry run):
```
/md-to-notion docs/platform-overview/ --parent abc123def456 --dry-run
```

Add a prefix to all page titles:
```
/md-to-notion output/meetings/2026-03-14/ --parent abc123 --title-prefix "Sprint2: "
```

### Differences from Related Commands

| Command | What It Does | When to Use Instead |
|---------|-------------|---------------------|
| `/meeting-digest` | Analyze meeting content with PM skills + upload to Notion | When you need PM analysis, not just raw upload |
| `/notion-docs-sync` | Bidirectional sync via `.notion-sync.yaml` config | When you need ongoing sync with DB schema tracking |
