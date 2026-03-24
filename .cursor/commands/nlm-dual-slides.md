## NLM Dual-Audience Slides

End-to-end pipeline: single document → dual-audience rewrite (elementary + expert) → two NotebookLM slide decks → Google Drive upload → Slack summary with Drive links.

### Usage

```
/nlm-dual-slides <file-or-url>                             # Full pipeline (both audiences, Drive, Slack)
/nlm-dual-slides <file-or-url> --skip-elementary            # Expert slides only
/nlm-dual-slides <file-or-url> --skip-expert                # Elementary slides only
/nlm-dual-slides <file-or-url> --lang en                    # English only
/nlm-dual-slides <file-or-url> --lang ko                    # Korean only
/nlm-dual-slides <file-or-url> --skip-drive                 # Skip Google Drive upload
/nlm-dual-slides <file-or-url> --skip-slack                 # Skip Slack posting
/nlm-dual-slides <file-or-url> --drive-folder FOLDER_ID     # Upload to specific Drive folder
/nlm-dual-slides <file-or-url> --channel ai-coding-radar    # Post to a different Slack channel
/nlm-dual-slides <file-or-url> --revise                     # Revise expert deck for white-bg refinement
```

### Execution

1. Read and follow `.cursor/skills/nlm-dual-slides/SKILL.md`
2. Read both system prompts:
   - `.cursor/skills/nlm-dual-slides/references/expert-prompt.md`
   - `.cursor/skills/nlm-dual-slides/references/elementary-prompt.md`
3. Execute the 6-phase pipeline using `notebooklm-mcp` MCP tools, `gws` CLI, and Slack MCP

MCP tools used: `notebook_create`, `source_add`, `studio_create`, `studio_status`, `studio_revise`, `download_artifact`, `slack_send_message`.

### Pipeline

1. **Ingest** — Read markdown file, PDF, or arXiv URL; split by `##` headings
2. **Dual Rewrite** — Rewrite each section into 4 variants (expert EN/KO + elementary EN/KO) using the two system prompts
3. **Create Notebooks** — Create two NLM notebooks; upload EN + KO sources to each
4. **Generate Slides** — `studio_create` for both notebooks (parallel); poll `studio_status` every 30s (5-8 min each); download PDFs
5. **Drive Upload** — `gws drive +upload` both PDFs; extract shareable links
6. **Slack Post** — Post summary + Drive links to `#deep-research-trending`; thread replies with per-audience details

### Examples

Generate dual slides from a paper:
```
/nlm-dual-slides output/papers/sefo-v3/SEFO-v3-EN.md
```

Expert slides only, skip Slack:
```
/nlm-dual-slides output/papers/sefo-v3/SEFO-v3-EN.md --skip-elementary --skip-slack
```

From an arXiv URL with Drive folder:
```
/nlm-dual-slides https://arxiv.org/abs/2403.12345 --drive-folder 1a2b3c4d5e
```

Elementary slides only in Korean:
```
/nlm-dual-slides docs/proposals/gpu-cloud-strategy.md --skip-expert --lang ko
```
