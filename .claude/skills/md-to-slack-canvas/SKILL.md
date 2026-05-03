---
name: md-to-slack-canvas
description: >-
  Publish local markdown files as Slack Canvas documents. Reads one file or
  globs a folder for *.md, extracts H1 as canvas title, transforms markdown to
  Slack Canvas flavor (header depth truncation, blockquote-to-callout
  conversion, table pipe escaping), and creates or updates canvases via Slack
  MCP. Use when the user asks to "upload markdown to Slack Canvas", "publish
  md to Slack Canvas", "create canvas from file", "push to canvas", "마크다운 슬랙
  캔버스", "슬랙 캔버스 업로드", "md-to-slack-canvas", "캔버스에 올려", "캔버스로 변환", "슬랙 캔버스에
  올려줘". Do NOT use for Slack message posting (use kwp-slack-slack-messaging).
  Do NOT use for Notion page publishing (use md-to-notion). Do NOT use for
  channel messaging or thread replies (use Slack MCP slack_send_message).
  Korean triggers: "슬랙 캔버스", "캔버스 업로드", "마크다운 캔버스", "캔버스에 올려".
---

# md-to-slack-canvas

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English. Slack status messages follow this rule; canvas body mirrors source markdown.

Lightweight publisher: point at local markdown files and get Slack Canvas
documents. Handles header depth truncation, blockquote-to-callout conversion,
and table escaping automatically.

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<path>` | Yes | File path or folder path containing `.md` files |
| `--channel <id>` | No | Post canvas link to this Slack channel after creation |
| `--update <canvas_id>` | No | Update an existing canvas instead of creating new |
| `--append` | No | Append content to end of existing canvas (requires `--update`) |
| `--skip-meta` | No | Skip README.md, CHANGELOG.md, LICENSE.md |
| `--title-prefix <str>` | No | Prepend string to each canvas title |
| `--dry-run` | No | List files and titles without creating canvases |

## Workflow

```
Step 1: Resolve   → Collect .md file paths from input
Step 2: Transform → Convert standard markdown to Canvas markdown flavor
Step 3: Publish   → Create or update canvases via Slack MCP
Step 4: Verify    → Read back canvas and confirm content
```

### Step 1: Resolve Input

Determine what `<path>` points to:

- **Single file**: Use that file directly
- **Folder**: Glob for `**/*.md` recursively, sort alphabetically
- If `--skip-meta` is set, exclude `README.md`, `CHANGELOG.md`, `LICENSE.md`
  (case-insensitive)

**CRITICAL**: Abort with a clear error if no `.md` files are found.

### Step 2: Transform to Canvas Markdown

For each markdown file, apply these transformations in order:

1. **Extract title**: Find the first `# ` line (H1). If absent, derive from
   filename (e.g., `release-plan.md` → "Release Plan")
2. **Strip H1**: Remove the title line from the body (Canvas `title` field
   handles it)
3. **Truncate deep headers**: Replace `####`, `#####`, `######` with `###`
   (Canvas supports max 3 levels)
4. **Convert blockquotes to callouts**: Transform `> text` blocks to Canvas
   callout syntax:
   ```
   ::: {.callout}
   text
   :::
   ```
   Skip blockquotes inside fenced code blocks.
5. **Escape table pipes**: Within markdown table cells, ensure literal `|`
   characters are escaped as `\|`
6. **Sanitize list items**: Remove any block quotes, code blocks, or headings
   nested inside list items (Canvas only allows inline formatting in lists)
7. **Validate links**: Ensure all links use full HTTP/HTTPS URLs (no relative
   links). Flag any relative links as warnings.
8. **Apply title prefix**: If `--title-prefix` is set, prepend to the title

If `--dry-run`, print `[N] {title} ({chars} chars) ← {filepath}` and stop.

### Step 3: Publish to Slack Canvas

**Create new canvas**:

```
CallMcpTool(
  server="plugin-slack-slack",
  toolName="slack_create_canvas",
  arguments={
    "title": "<extracted-title>",
    "content": "<transformed-content>"
  }
)
```

The response returns a canvas URL — save it for the verify step and user output.

**Update existing canvas** (when `--update` is provided without `--append`):

```
CallMcpTool(
  server="plugin-slack-slack",
  toolName="slack_update_canvas",
  arguments={
    "canvas_id": "<canvas-id>",
    "action": "replace",
    "content": "<transformed-content>"
  }
)
```

**CRITICAL**: `action=replace` without `section_id` overwrites the entire
canvas. This is the intended behavior for full-file publishing.

**Append to existing canvas** (when both `--update` and `--append` are provided):

```
CallMcpTool(
  server="plugin-slack-slack",
  toolName="slack_update_canvas",
  arguments={
    "canvas_id": "<canvas-id>",
    "action": "append",
    "content": "<transformed-content>"
  }
)
```

`action=append` without `section_id` adds the content to the end of the
canvas, preserving all existing content. Use this for incremental updates
such as appending dated log entries to a running canvas.

**Post link to channel** (when `--channel` is provided):

After successful canvas creation, post the canvas URL to the specified channel:

```
CallMcpTool(
  server="plugin-slack-slack",
  toolName="slack_send_message",
  arguments={
    "channel_id": "<channel-id>",
    "text": "New canvas published: <canvas-title>\n<canvas-url>"
  }
)
```

Process files sequentially. If one canvas creation fails, log the error and
continue with remaining files.

### Step 4: Verify

For each created canvas, read it back to confirm:

```
CallMcpTool(
  server="plugin-slack-slack",
  toolName="slack_read_canvas",
  arguments={
    "canvas_id": "<canvas-id>"
  }
)
```

Verify the returned content is non-empty. Report the final summary:

```
Created N canvas(es):
  [1] "Title" → <canvas-url>
  [2] "Title" → <canvas-url>
Failed: M file(s) — see errors above
```

## Error Handling

| Issue | Resolution |
|-------|------------|
| No `.md` files found | Abort: "Error: No markdown files found at {path}" |
| Path does not exist | Abort: "Error: Path not found: {path}" |
| Free Slack workspace | Abort: "Error: Canvas is not available on free Slack plans" |
| Canvas creation fails | Log error, continue with remaining files, report at end |
| No H1 found in file | Derive title from filename |
| Content has `####`+ headers | Auto-truncate to `###` (silent) |
| `--update` without canvas_id | Abort: "Error: Canvas ID required for --update" |
| `--append` without `--update` | Abort: "Error: --append requires --update <canvas_id>" |
| Relative links detected | Warn: "Warning: Relative link found — Canvas requires full URLs" |
| Canvas read-back empty | Warn: "Warning: Canvas {id} returned empty content" |

## Examples

### Single file upload

```
/md-to-slack-canvas output/analysis/nvidia-ecosystem-vs-thakicloud-2026-03-18.md
```

Creates a canvas titled "NVIDIA Ecosystem vs ThakiCloud" from the H1.

### Folder upload

```
/md-to-slack-canvas output/analysis/ --skip-meta
```

Creates one canvas per `.md` file in the folder.

### Upload and share to channel

```
/md-to-slack-canvas output/plans/release-plan.md --channel C0AA8NT4T8T
```

Creates the canvas and posts the link to the target Slack channel (e.g. `#team-tasks`).

### Update existing canvas (replace)

```
/md-to-slack-canvas output/plans/release-plan.md --update F07ABCCANVAS
```

Overwrites the existing canvas content with the file's transformed markdown.

### Append to existing canvas

```
/md-to-slack-canvas output/plans/daily-digest.md --update F07ABCCANVAS --append
```

Adds the file's content to the end of the canvas without touching existing content.

### Dry run preview

```
/md-to-slack-canvas docs/platform-overview/ --dry-run
```

Lists files and extracted titles without creating any canvases.

### With title prefix

```
/md-to-slack-canvas outputs/research/ --title-prefix "[Research] " --skip-meta
```

All canvas titles are prefixed with `[Research] `.

## Canvas Markdown Reference

See [references/canvas-markdown-spec.md](references/canvas-markdown-spec.md)
for the full Slack Canvas markdown syntax specification.
