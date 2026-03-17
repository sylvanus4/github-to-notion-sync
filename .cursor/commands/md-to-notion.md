---
description: Publish local markdown files as structured Notion sub-pages with table conversion and auto-splitting
argument-hint: "<file-or-folder> [--parent <notion-page-id>]"
---

## md-to-notion

Publish local markdown files (single file or entire folder) as Notion sub-pages.
Extracts H1 headings as page titles, converts pipe tables to Notion `<table>`
HTML blocks, auto-splits large documents into linked sub-pages, and preserves
ASCII diagrams in code blocks.

### Usage

```
/md-to-notion <file.md>
/md-to-notion <folder/>
/md-to-notion <file.md> --parent <notion-page-id>
/md-to-notion <folder/> --parent <id> --icon 📋
/md-to-notion <folder/> --parent <id> --skip-meta
/md-to-notion <folder/> --parent <id> --title-prefix "Sprint2: "
/md-to-notion <folder/> --parent <id> --dry-run
/md-to-notion <file.md> --parent <id> --no-table-convert
/md-to-notion <file.md> --parent <id> --split-threshold 12000
```

### Options

| Option | Description |
|--------|-------------|
| (positional) | File path or folder path containing `.md` files |
| `--parent <id>` | Notion parent page ID. Defaults to AI 자동 정리 page (`3239eddc...`) |
| `--icon <emoji>` | Apply a uniform emoji icon to all created pages |
| `--skip-meta` | Skip README.md, CHANGELOG.md, LICENSE.md |
| `--no-table-convert` | Keep pipe tables as-is (skip conversion to `<table>` blocks) |
| `--title-prefix <str>` | Prepend a string to each page title |
| `--split-threshold <N>` | Character limit before auto-splitting (default: 15000) |
| `--dry-run` | List files and extracted titles without creating pages |

### Workflow

1. **Spec** -- Fetch Notion enhanced Markdown spec for reference
2. **Resolve** -- Collect `.md` file paths from input (single file or recursive glob)
3. **Parse** -- Run `scripts/convert_tables.py` to extract H1 titles, convert tables, split large docs
4. **Publish** -- Create Notion sub-pages via `notion-create-pages` MCP
5. **Verify** -- Fetch parent page and confirm all sub-pages are visible

### Execution

Read and follow the `md-to-notion` skill (`.cursor/skills/md-to-notion/SKILL.md`).

### Examples

Upload a single markdown file (uses default parent):
```
/md-to-notion output/plans/release-plan.ko.md
```

Upload with explicit parent:
```
/md-to-notion output/plans/release-plan.ko.md --parent 3239eddc34e680e8a7a5d5b5eac18b38
```

Upload an entire folder with icon:
```
/md-to-notion output/meetings/2026-03-14/ --icon 📋
```

Auto-split a large document (50KB+):
```
/md-to-notion output/plans/big-report.md --parent abc123... --split-threshold 12000
```

Preview what would be uploaded (dry run):
```
/md-to-notion docs/platform-overview/ --parent abc123... --dry-run
```

### Differences from Related Commands

| Command | What It Does | When to Use Instead |
|---------|-------------|---------------------|
| `/meeting-digest` | Analyze meeting content with PM skills + upload to Notion | When you need PM analysis, not just raw upload |
| `/notion-meeting-sync` | Batch-sync meeting DB from Notion with PPTX generation | When you need database-driven meeting sync |
