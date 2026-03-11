## Paper Review Pipeline

End-to-end academic paper review: ingest paper → Korean review → multi-perspective PM analysis → DOCX report → PPTX presentation → NotebookLM slide deck → Slack distribution. Orchestrates 14+ skills across 7 phases.

### Usage

```
/paper-review <arXiv-URL>                                    # full pipeline with all phases
/paper-review /path/to/paper.pdf                             # local PDF input
/paper-review paper.md --skip-pm                             # review + docs only, no PM analysis
/paper-review <URL> --skip-slack --skip-nlm                  # no Slack posting or NLM slides
/paper-review <URL> --perspectives "strategy,statistics"     # run only selected perspectives
/paper-review <URL> --channel "research-pr"                  # post to a different Slack channel
```

### Pipeline

1. **Ingest** — Parse arXiv URL / local PDF / markdown → structured text
2. **Review** — Generate structured Korean paper review (core deliverable)
3. **Analyze** — Run 6 PM/research perspectives in parallel (optional)
4. **DOCX** — Consolidate into a professional Word report
5. **PPTX** — Generate PowerPoint presentation via PptxGenJS
6. **NLM Slides** — Create NotebookLM slide deck from DOCX
7. **Slack** — Upload NLM slides + threaded summary + DOCX + PPTX to Slack

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--skip-pm` | Skip PM analysis (Phase 3) | PM enabled |
| `--skip-pptx` | Skip PPTX generation (Phase 5) | PPTX enabled |
| `--skip-docx` | Skip DOCX generation (Phase 4; also skips Phase 6) | DOCX enabled |
| `--skip-nlm` | Skip NotebookLM slide generation (Phase 6) | NLM enabled |
| `--skip-slack` | Skip Slack distribution (Phase 7) | Slack enabled |
| `--channel <name>` | Target Slack channel | `research` |
| `--perspectives "..."` | Comma-separated perspectives to run | All 6 |
| `--lang ko` | Korean review only (default) | Korean |
| `--lang both` | Review in both Korean and English | Korean |

### Execution

1. Read and follow `.cursor/skills/paper-review/SKILL.md`
2. Read reference files as needed per each phase:
   - `references/review-template.md` (Phase 2)
   - `references/analysis-perspectives.md` (Phase 3)
   - `references/docx-structure.md` (Phase 4)
   - `references/pptx-structure.md` (Phase 5)
   - `references/nlm-slack-integration.md` (Phase 6-7)
3. Execute phases sequentially, respecting option flags

MCP tools used: `notebook_create`, `source_add`, `studio_create`, `studio_status`, `download_artifact`, `slack_send_message`, `slack_search_channels`.

Shell tools: `curl` for arXiv PDF download, Defuddle extraction, and Slack file uploads via `files.uploadV2` API.

### Examples

Full pipeline for an arXiv paper:
```
/paper-review https://arxiv.org/abs/2509.04664
```

Local PDF with only strategy + statistics perspectives:
```
/paper-review /path/to/paper.pdf --perspectives "strategy,statistics"
```

Quick review without PM analysis or Slack:
```
/paper-review paper.md --skip-pm --skip-slack
```

Post to a custom Slack channel:
```
/paper-review https://arxiv.org/abs/2509.04664 --channel "press"
```
