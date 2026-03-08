## NotebookLM Slides

End-to-end pipeline: local markdown → expert EN/KO rewrite → NotebookLM slide deck generation → PDF/PPTX download.

### Usage

```
/nlm-slides <markdown-file>                              # EN + KO slide deck (PDF)
/nlm-slides <markdown-file> --lang en                    # English only
/nlm-slides <markdown-file> --lang ko                    # Korean only
/nlm-slides <markdown-file> --format presenter_slides    # speaker-note style
/nlm-slides <markdown-file> --length short               # condensed version
/nlm-slides <markdown-file> --output pptx                # download as PPTX
/nlm-slides <markdown-file> --revise "instructions"      # revise existing slides
```

### Execution

1. Read and follow `.cursor/skills/nlm-slides/SKILL.md`
2. Read the system prompt at `.cursor/skills/nlm-slides/references/system-prompt.md`
3. Execute the 7-step pipeline using `notebooklm-mcp` MCP tools

MCP tools used: `notebook_create`, `source_add`, `studio_create`, `studio_status`, `studio_revise`, `download_artifact`.

### Pipeline

1. Read the local markdown file
2. Split by `##` headings into sections
3. Rewrite each section into expert EN + KO (using system prompt)
4. Create NotebookLM notebook, upload EN and KO as text sources
5. `studio_create(artifact_type="slide_deck", slide_format="detailed_deck", confirm=True)`
6. Poll `studio_status` every 30s until complete (expect 5-8 min)
7. `download_artifact` with **absolute path** to `outputs/presentations/`

### Examples

Generate slides from a proposal:
```
/nlm-slides docs/proposals/gpu-cloud-strategy.md
```

English-only, presenter slides as PPTX:
```
/nlm-slides docs/proposals/gpu-cloud-strategy.md --lang en --format presenter_slides --output pptx
```

Revise after initial generation:
```
/nlm-slides docs/proposals/gpu-cloud-strategy.md --revise "Add more data charts to slide 3"
```
