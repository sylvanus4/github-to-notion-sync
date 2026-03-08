## NotebookLM Video

End-to-end pipeline: local markdown → expert EN/KO narrative rewrite → NotebookLM video explainer generation → MP4 download.

### Usage

```
/nlm-video <markdown-file>                              # EN + KO video explainer
/nlm-video <markdown-file> --lang en                    # English only
/nlm-video <markdown-file> --lang ko                    # Korean only
/nlm-video <markdown-file> --format brief               # brief format (shorter)
/nlm-video <markdown-file> --format cinematic           # cinematic style
/nlm-video <markdown-file> --style whiteboard           # whiteboard visual style
```

### Execution

1. Read and follow `.cursor/skills/nlm-video/SKILL.md`
2. Read the system prompt at `.cursor/skills/nlm-video/references/system-prompt.md`
3. Execute the 7-step pipeline using `notebooklm-mcp` MCP tools

MCP tools used: `notebook_create`, `source_add`, `studio_create`, `studio_status`, `download_artifact`.

### Pipeline

1. Read the local markdown file
2. Split by `##` headings into sections
3. Rewrite each section into expert narrative EN + KO (using system prompt)
4. Create NotebookLM notebook, upload EN and KO as text sources
5. `studio_create(artifact_type="video", video_format="explainer", confirm=True)`
6. Poll `studio_status` every 30s until complete (expect 5-10 min)
7. `download_artifact` with **absolute path** to `outputs/presentations/`

### Visual Styles

Available styles: `auto_select` (default), `classic`, `whiteboard`, `kawaii`, `anime`, `watercolor`, `retro_print`, `heritage`, `paper_craft`.

### Examples

Generate video from a proposal:
```
/nlm-video docs/proposals/gpu-cloud-strategy.md
```

Brief format with whiteboard style:
```
/nlm-video docs/proposals/gpu-cloud-strategy.md --format brief --style whiteboard
```

Korean-only video:
```
/nlm-video docs/proposals/gpu-cloud-strategy.md --lang ko
```
