## NLM arXiv Slides

End-to-end pipeline: download an arXiv paper PDF, extract and rewrite content into expert-level EN + KO, upload to NotebookLM with web research enrichment, query for analysis, generate slide deck PDFs, and download them. Orchestrates 6 skills: defuddle, anthropic-pdf, nlm-slides, notebooklm, notebooklm-research, notebooklm-studio.

### Usage

```
/nlm-arxiv-slides <arXiv-URL>                                        # full pipeline with defaults
/nlm-arxiv-slides <arXiv-URL> --skip-research                        # skip web research enrichment
/nlm-arxiv-slides <arXiv-URL> --lang en                              # English only
/nlm-arxiv-slides <arXiv-URL> --extra-artifacts "audio,quiz"         # also generate podcast + quiz
/nlm-arxiv-slides <arXiv-URL> --skip-analysis --length short         # quick slides, no analysis doc
/nlm-arxiv-slides <arXiv-URL> --output pptx                          # download as PPTX
```

### Pipeline

1. **Parse** — Extract arXiv paper ID from URL (supports `/abs/` and `/pdf/` formats)
2. **Download** — Fetch PDF via curl + extract abstract metadata via Defuddle
3. **Extract** — Pull full text from PDF using pdfplumber
4. **Rewrite** — Transform into expert-level EN + KO with visual hints for slides
5. **Notebook** — Create NotebookLM notebook
6. **Sources** — Upload original PDF + rewritten EN/KO documents
7. **Research** — Web research for related context (optional, skip with `--skip-research`)
8. **Analyze** — Query notebook for contributions, innovations, and limitations; save analysis doc
9. **Generate** — Create slide deck via studio_create
10. **Poll** — Wait for slide generation (5-8 minutes typical)
11. **Download** — Save slide PDF to `outputs/presentations/`

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--lang en/ko` | Generate single-language version only | Both EN + KO |
| `--skip-research` | Skip web research enrichment (Phase 7) | Research enabled |
| `--skip-analysis` | Skip notebook query analysis (Phase 8) | Analysis enabled |
| `--format` | `detailed_deck` or `presenter_slides` | `detailed_deck` |
| `--length` | `default` or `short` | `default` |
| `--output` | `pdf` or `pptx` | `pdf` |
| `--extra-artifacts` | Additional artifacts: `audio`, `quiz`, `flashcards`, `mind_map`, `report` | Slides only |
| `--revise "text"` | Revise slides with specific instructions | -- |

### Execution

1. Read and follow `.cursor/skills/nlm-arxiv-slides/SKILL.md`
2. Read the system prompt at `.cursor/skills/nlm-arxiv-slides/references/system-prompt.md`
3. Read the analysis queries at `.cursor/skills/nlm-arxiv-slides/references/analysis-queries.md`
4. Execute the 11-phase pipeline using `notebooklm-mcp` MCP tools

MCP tools used: `notebook_create`, `source_add`, `notebook_query`, `note`, `research_start`, `research_status`, `research_import`, `studio_create`, `studio_status`, `download_artifact`, `studio_revise`.

### Examples

Analyze a paper on LLM hallucinations:
```
/nlm-arxiv-slides https://arxiv.org/abs/2509.04664
```

Quick slides without research or analysis:
```
/nlm-arxiv-slides https://arxiv.org/abs/2509.04664 --skip-research --skip-analysis
```

Full analysis with podcast and quiz:
```
/nlm-arxiv-slides https://arxiv.org/abs/2401.12345 --extra-artifacts "audio,quiz,flashcards"
```

Korean-only slides:
```
/nlm-arxiv-slides https://arxiv.org/abs/2509.04664 --lang ko
```
