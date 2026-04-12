---
name: md-to-notion
description: >-
  Publish local markdown files as Notion sub-pages under a specified parent page.
  Reads one file or globs a folder for *.md, extracts H1 as page title, converts
  pipe tables to Notion <table> HTML blocks for proper rendering, splits large
  documents (>15KB) into linked sub-pages, preserves ASCII diagrams in code blocks,
  and batch-creates pages via the Notion MCP. Use when the user asks to "upload
  markdown to Notion", "publish md to Notion", "push files to Notion", "마크다운
  노션 업로드", "md를 노션에 올려줘", "노션 페이지로 변환", "마크다운 노션
  퍼블리시", "md-to-notion", "노션에 올려", "노션 페이지 만들어", or wants to turn
  local markdown into structured Notion pages.
  Do NOT use for bidirectional Notion sync with YAML config (use notion-docs-sync).
  Do NOT use for meeting digest analysis and upload (use meeting-digest).
  Do NOT use for Notion database operations or page queries (use Notion MCP directly).
  Korean triggers: "노션 업로드", "마크다운 노션", "노션 페이지", "노션에 올려", "노션에 정리".
metadata:
  author: "thaki"
  version: "2.0.2"
  category: "execution"
---
# md-to-notion

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English. User-facing status messages and summaries follow this rule; page body mirrors the source markdown language.

Lightweight one-shot publisher: point at local markdown files and a Notion
parent page, get structured sub-pages. Handles pipe-table conversion, large
document splitting, and ASCII art preservation automatically.

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<path>` | Yes | File path or folder path containing `.md` files |
| `--parent <id>` | No | Notion parent page ID (32-char hex). Default: `3239eddc34e680e8a7a5d5b5eac18b38` (AI 자동 정리). Also reads `NOTION_DEFAULT_PAGE_ID` from `.env`. |
| `--icon <emoji>` | No | Uniform emoji icon for all created pages (default: 📄) |
| `--skip-meta` | No | Skip README.md, CHANGELOG.md, LICENSE.md |
| `--no-table-convert` | No | Keep pipe tables as-is (skip conversion) |
| `--title-prefix <str>` | No | Prepend string to each page title |
| `--split-threshold <N>` | No | Character limit before auto-splitting (default: 15000) |
| `--dry-run` | No | List files and titles without creating pages |

## Authentication Strategy

This skill uses **token-first** Notion authentication:

1. **Primary (Token)**: Check for `NOTION_TOKEN` in `.env` or environment.
   When available, use `scripts/notion_api.py` (`NotionClient`) for all
   Notion REST API calls (create page, append blocks, get page).
2. **Fallback (MCP)**: Only when `NOTION_TOKEN` is NOT available, fall back
   to `plugin-notion-workspace-notion` MCP server for browser-based auth.

**Detection**: Run `python -c "from scripts.notion_api import is_token_available; print(is_token_available())"`.
If `True`, use token path. If `False`, use MCP path.

## Workflow

```
Step 0: Auth      → Detect NOTION_TOKEN availability
Step 1: Resolve   → Collect .md file paths from input
Step 2: Parse     → Extract titles, convert tables, check size, split if needed
Step 3: Publish   → Create Notion sub-pages (token API or MCP fallback)
Step 4: Verify    → Confirm pages appear under parent
```

### Step 0: Detect Authentication Method

Check `NOTION_TOKEN` availability:

```bash
python -c "from scripts.notion_api import is_token_available; print(is_token_available())"
```

- If `True`: All Steps 3-4 use `scripts/notion_api.py` (direct REST API).
- If `False`: All Steps 3-4 use Notion MCP as fallback.

When using MCP fallback, optionally fetch the Notion markdown spec:

```
FetchMcpResource(
  server="plugin-notion-workspace-notion",
  uri="notion://docs/enhanced-markdown-spec"
)
```

### Step 1: Resolve Input

Determine what `<path>` points to:

- **Single file**: Use that file directly
- **Folder**: Glob for `**/*.md` recursively, sort alphabetically
- If `--skip-meta` is set, exclude files named `README.md`, `CHANGELOG.md`,
  `LICENSE.md` (case-insensitive)

**CRITICAL**: Abort with a clear error if no `.md` files are found.

### Step 2: Parse Each File

Create a temporary directory for intermediate files, then run the bundled
conversion script:

```bash
TMPDIR=$(mktemp -d /tmp/notion-upload-XXXXXX)

python .cursor/skills/md-to-notion/scripts/convert_tables.py \
  --threshold <split-threshold> \
  --outdir "$TMPDIR" \
  <file1.md> [file2.md ...]
```

The script prints `OUTDIR=<path>` to stdout. If `--outdir` is omitted, the
script auto-creates a unique `/tmp/notion-upload-*/` directory.

The script performs these steps per file:

1. **Read** the file content
2. **Extract title**: Find the first `# ` line (H1). If absent, derive from
   filename (e.g., `action-items.md` → "Action Items")
3. **Strip H1**: Remove the title line from the body
4. **Convert pipe tables** (unless `--no-table-convert`): Transform pipe tables
   to Notion `<table header-row="true">` HTML blocks. Tables inside fenced code
   blocks are preserved as-is, which also protects ASCII art diagrams.
   See [references/table-conversion.md](references/table-conversion.md).
5. **Size check**: If converted content exceeds `--split-threshold` characters,
   split by H2 sections into multiple parts
6. **Output JSON** to `$TMPDIR/notion_page_N.json` with fields:
   - `title`: extracted page title
   - `content`: converted markdown body (if not split)
   - `split`: boolean flag
   - `parts`: array of `{subtitle, body}` objects (if split)

Apply `--title-prefix` to titles after extraction.

If `--dry-run`, print `[N] {title} ({chars} chars) ← {filepath}` and stop.

### Step 3: Publish to Notion

#### Path A: Token-based (preferred)

When `NOTION_TOKEN` is available, use `scripts/notion_api.py`:

```python
from scripts.notion_api import NotionClient

client = NotionClient()

# For each JSON file from Step 2:
blocks = NotionClient.md_to_blocks(content)
page = client.create_page(
    parent_id="<parent-id>",
    title="<extracted-title>",
    children=blocks[:100],
    icon_emoji="<emoji>",  # omit if --icon not provided
)
# Remaining blocks auto-appended by create_page if >100
```

The client handles batching (100 blocks per request) and retry (429/5xx)
automatically.

#### Path B: MCP fallback

When `NOTION_TOKEN` is NOT available, use MCP:

```
CallMcpTool(
  server="plugin-notion-workspace-notion",
  toolName="notion-create-pages",
  arguments={
    "parent": {"page_id": "<parent-id>"},
    "pages": [
      {
        "properties": {"title": "<extracted-title>"},
        "icon": "<emoji>",
        "content": "<processed-markdown-body>"
      }
    ]
  }
)
```

**Common error**: passing `parent` as a bare string causes
`"Expected object, received string"`. Always use `{"page_id": "..."}`.

Omit the `icon` field entirely if `--icon` was not provided.
Batch up to 100 pages per call (Notion API limit).

#### Split Document Upload

When a file is split (JSON has `"split": true`):

1. **Create a parent page** under the user's `--parent` with the file's title.
   Include a brief callout in the content explaining the document is split:

   ```markdown
   > This document is split into sub-pages due to size.
   > Original file: `<filepath>`

   Sub-pages are listed below.
   ```

2. **Create sub-pages** under the newly created parent page, one per part.
   Use `Part {N}: {subtitle}` as each sub-page title (localized labels in Korean deliverables if required).

3. **Record** the parent page ID from step 1 for verification.

#### Manual multi-part publish (MCP payload safety)

When a single part is still large enough to risk MCP/JSON payload limits, or the
user supplied **pre-defined** part files (e.g. `part-0.md`, `part-1.md`) instead
of one monolithic file:

1. Run `notion-create-pages` **per part** (or batch only the smaller parts) using
   the same `parent` object shape as above—do not pass `parent` as a bare string.
2. **Order**: create a smaller part first to validate credentials and markdown
   rendering, then upload heavier parts (mirrors successful production sessions
   where Part 1 was smaller than Part 0).
3. Reuse the same intermediate parent page pattern as split uploads so the
   Notion tree stays navigable (index parent + linked sub-pages).

This path complements automatic H2 splitting; use it when tooling limits or
editor-authored chunk boundaries apply.

### Step 4: Verify

After all pages are created, fetch the original parent page to confirm:

```
CallMcpTool(
  server="plugin-notion-workspace-notion",
  toolName="notion-fetch",
  arguments={"id": "<parent-id>"}
)
```

Check that each created title appears in the response. Report any missing pages.

For split documents, also fetch the intermediate parent page to confirm all
sub-pages are present.

### Step 5: Cleanup Temporary Files

After all pages are verified (or on any error after the temporary directory was
created), delete the temporary directory and all its contents:

```bash
rm -rf "$TMPDIR"
```

This prevents leftover intermediate JSON files from accumulating in `/tmp/`.
This cleanup step is **mandatory** — never leave temporary files behind.

## Error Handling

| Issue | Resolution |
|-------|------------|
| `--parent` not provided | Abort: "Error: --parent is required. Provide a Notion parent page ID." |
| No `.md` files found | Abort: "Error: No markdown files found at {path}" |
| Path does not exist | Abort: "Error: Path not found: {path}" |
| `parent: "Expected object, received string"` | Fix: use `{"page_id": "..."}` format |
| Content too large for single page | Auto-split by H2 headings (handled by script) |
| No H1 found in file | Fallback: derive title from filename |
| Single page creation fails | Log error, continue with remaining files, report at end |
| Notion API rate limit (429) | Retry with exponential backoff: 2s, 4s, 8s (max 3) |
| Parent page not found | Abort: "Error: Parent page {id} not found or inaccessible" |
| Verification shows missing pages | Warn: "Warning: {N} pages not found under parent" |

## Examples

### Single file upload

```
/md-to-notion output/plans/release-plan.ko.md --parent <your-notion-parent-page-id>
```

### Folder upload with icon

```
/md-to-notion output/meetings/2026-03-14/ --parent 3239eddc... --icon 📋 --skip-meta
```

### Large document (auto-split)

```
/md-to-notion output/plans/big-report.md --parent abc123... --split-threshold 12000
```

The 50KB report is split into 4 sub-pages under a new parent page.

### Dry run preview

```
/md-to-notion docs/platform-overview/ --parent abc123... --dry-run
```

### Inline content (no file)

When the user provides markdown content directly (not from a file), create the
page directly via MCP without the script. Convert any pipe tables manually
following [references/table-conversion.md](references/table-conversion.md).
