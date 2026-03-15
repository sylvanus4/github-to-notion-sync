---
name: md-to-notion
description: >-
  Publish local markdown files as Notion sub-pages under a specified parent page.
  Reads one file or globs a folder for *.md, extracts H1 as page title, converts
  pipe tables to bulleted lists for Notion compatibility, and batch-creates pages
  via the Notion MCP. Use when the user asks to "upload markdown to Notion",
  "publish md to Notion", "push files to Notion", "마크다운 노션 업로드",
  "md를 노션에 올려줘", "노션 페이지로 변환", "마크다운 노션 퍼블리시",
  "md-to-notion", or wants to turn local markdown into structured Notion pages.
  Do NOT use for bidirectional Notion sync with YAML config (use notion-docs-sync).
  Do NOT use for meeting digest analysis and upload (use meeting-digest).
  Do NOT use for Notion database operations or page queries (use Notion MCP directly).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# md-to-notion

Lightweight one-shot publisher: point at local markdown files and a Notion
parent page, get structured sub-pages. No config files, no scripts, no sync
state — just MCP tool calls.

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<path>` | Yes | File path or folder path containing `.md` files |
| `--parent <id>` | Yes | Notion parent page ID (32-char hex, with or without hyphens) |
| `--icon <emoji>` | No | Uniform emoji icon for all created pages |
| `--skip-meta` | No | Skip README.md, CHANGELOG.md, LICENSE.md |
| `--no-table-convert` | No | Keep pipe tables as-is (skip conversion) |
| `--title-prefix <str>` | No | Prepend string to each page title |
| `--dry-run` | No | List files and titles without creating pages |

## Workflow

```
Step 1: Resolve    → Collect .md file paths from input
Step 2: Parse      → Extract titles, process content per file
Step 3: Publish    → Batch-create Notion sub-pages via MCP
Step 4: Verify     → Confirm pages appear under parent
```

### Step 1: Resolve Input

Determine what `<path>` points to:

- **Single file**: Use that file directly
- **Folder**: Glob for `**/*.md` recursively, sort alphabetically
- If `--skip-meta` is set, exclude files named `README.md`, `CHANGELOG.md`,
  `LICENSE.md` (case-insensitive)

**CRITICAL**: Abort with a clear error if no `.md` files are found.

### Step 2: Parse Each File

For each markdown file:

1. **Read** the file content
2. **Extract title**: Find the first `# ` line (H1 heading). If no H1 exists,
   use the filename stem with spaces (e.g., `action-items.md` → "action items")
3. **Strip H1**: Remove the title line from the content body
4. **Convert pipe tables** (unless `--no-table-convert`):
   Transform pipe tables to bulleted lists for Notion rendering.
   See [references/table-conversion.md](references/table-conversion.md)
   for the detailed conversion algorithm.
5. **Apply title prefix**: If `--title-prefix` is set, prepend it to the title
6. **Dry-run check**: If `--dry-run`, print `[N] {title} ← {filepath}` and skip
   to the next file

### Step 3: Publish to Notion

Create pages using the `notion-create-pages` MCP tool. Batch up to 100 pages
per call (Notion API limit).

```
CallMcpTool(
  server="plugin-notion-workspace-notion",
  toolName="notion-create-pages",
  arguments={
    "parent": {"page_id": "<parent-id>"},
    "pages": [
      {
        "properties": {"title": "<extracted-title>"},
        "icon": "<emoji-if-provided>",
        "content": "<processed-markdown-body>"
      }
    ]
  }
)
```

Omit the `icon` field entirely if `--icon` was not provided.

If more than 100 files exist, split into multiple MCP calls.

### Step 4: Verify

After all pages are created, fetch the parent page to confirm sub-pages exist:

```
CallMcpTool(
  server="plugin-notion-workspace-notion",
  toolName="notion-fetch",
  arguments={"id": "<parent-id>"}
)
```

Check that each created title appears in the response. Report any missing pages.

## Examples

### Example 1: Single file upload

User says: `/md-to-notion output/meetings/2026-03-14/summary.md --parent 3239eddc34e680e8a7a5d5b5eac18b38`

Actions:
1. Read `summary.md`, extract H1 title "26-03-Sprint2 회고 요약"
2. Strip H1, convert any pipe tables to bulleted lists
3. Create one Notion sub-page titled "26-03-Sprint2 회고 요약" under the parent
4. Verify the page appears

Result: One Notion sub-page created under the specified parent.

### Example 2: Folder upload with icon

User says: `/md-to-notion output/meetings/2026-03-14/ --parent abc123... --icon 📋 --skip-meta`

Actions:
1. Glob `output/meetings/2026-03-14/**/*.md`, find `summary.md`, `action-items.md`
2. Parse each file: extract titles, convert tables
3. Batch-create 2 Notion pages with 📋 icon
4. Verify both pages appear under parent

Result: Two sub-pages created with 📋 icon.

### Example 3: Dry run preview

User says: `/md-to-notion docs/platform-overview/ --parent abc123... --dry-run`

Actions:
1. Glob folder, find 5 markdown files
2. Print preview: `[1] Platform Architecture ← docs/platform-overview/architecture.md` ...
3. No pages created

Result: Preview listing without any Notion API calls.

### Example 4: Title prefix for batch context

User says: `/md-to-notion output/meetings/2026-03-14/ --parent abc123... --title-prefix "Sprint2: "`

Actions:
1. Glob folder, find `summary.md` (title: "회의 요약"), `action-items.md` (title: "액션 아이템")
2. Apply prefix: "Sprint2: 회의 요약", "Sprint2: 액션 아이템"
3. Create 2 pages with prefixed titles
4. Verify

Result: Two pages with "Sprint2: " prefix in titles.

## Error Handling

| Issue | Resolution |
|-------|------------|
| `--parent` not provided | Abort with: "Error: --parent <notion-page-id> is required" |
| No `.md` files found at path | Abort with: "Error: No markdown files found at {path}" |
| Path does not exist | Abort with: "Error: Path not found: {path}" |
| Single page creation fails | Log the error, continue with remaining files, report failures at end |
| Notion API rate limit (429) | Retry with exponential backoff: 2s, 4s, 8s (max 3 retries) |
| Parent page not found | Abort with: "Error: Parent page {id} not found or inaccessible" |
| Verification shows missing pages | Warn: "Warning: {N} pages not found under parent after creation" |
