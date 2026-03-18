---
description: Publish local markdown files as Slack Canvas documents with auto-transformation
argument-hint: "<file-or-folder> [--channel <id>] [--update <canvas-id>] [--append]"
---

## md-to-slack-canvas

Publish local markdown files as Slack Canvas documents. Transforms standard
markdown to Canvas-flavored markdown (header depth truncation, blockquote-to-callout
conversion, table pipe escaping) and creates or updates canvases via Slack MCP.

### Usage

```
/md-to-slack-canvas <file.md>
/md-to-slack-canvas <folder/>
/md-to-slack-canvas <file.md> --channel C0AA8NT4T8T
/md-to-slack-canvas <file.md> --update F07ABCCANVAS
/md-to-slack-canvas <file.md> --update F07ABCCANVAS --append
/md-to-slack-canvas <folder/> --skip-meta --title-prefix "[Report] "
/md-to-slack-canvas <folder/> --dry-run
```

### Options

| Option | Description |
|--------|-------------|
| (positional) | File path or folder path containing `.md` files |
| `--channel <id>` | Post canvas link to this Slack channel after creation |
| `--update <canvas_id>` | Update existing canvas instead of creating new (replaces all content) |
| `--append` | Append content to end of existing canvas (requires `--update`) |
| `--skip-meta` | Skip README.md, CHANGELOG.md, LICENSE.md |
| `--title-prefix <str>` | Prepend string to each canvas title |
| `--dry-run` | List files and titles without creating canvases |

### Workflow

1. **Resolve** -- Collect `.md` file paths from input (single file or recursive glob)
2. **Transform** -- Convert standard markdown to Canvas markdown flavor (header truncation, callout conversion, pipe escaping)
3. **Publish** -- Create or update canvases via `slack_create_canvas` / `slack_update_canvas` MCP
4. **Verify** -- Read back canvases via `slack_read_canvas` and confirm content

### Execution

Read and follow the `md-to-slack-canvas` skill (`.cursor/skills/md-to-slack-canvas/SKILL.md`).

### Examples

Upload a single analysis file:
```
/md-to-slack-canvas output/analysis/nvidia-ecosystem-vs-thakicloud-2026-03-18.md
```

Upload and share to a channel:
```
/md-to-slack-canvas output/plans/release-plan.md --channel C0AA8NT4T8T
```

Update an existing canvas with fresh content (replaces all):
```
/md-to-slack-canvas output/plans/release-plan.md --update F07ABCCANVAS
```

Append content to the end of an existing canvas:
```
/md-to-slack-canvas output/plans/daily-digest.md --update F07ABCCANVAS --append
```

Preview without creating:
```
/md-to-slack-canvas docs/platform-overview/ --dry-run
```

### Differences from Related Commands

| Command | What It Does | When to Use Instead |
|---------|-------------|---------------------|
| `/md-to-notion` | Publish markdown as Notion sub-pages | When target is Notion, not Slack |
| `/x-to-slack` | Analyze tweet/URL and post to Slack messages | When posting URL analysis as threaded messages |
