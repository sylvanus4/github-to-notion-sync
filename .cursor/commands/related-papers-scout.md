## Related Papers Scout

Discover hot related papers from top institutions (Google, MIT, Stanford, NVIDIA) or with high Twitter/GitHub traction. Multi-source search across Semantic Scholar API, arXiv, Papers With Code, and Twitter/GitHub.

### Usage

```
/related-papers-scout <arXiv-URL>                                          # full pipeline
/related-papers-scout /path/to/paper.pdf                                   # local PDF input
/related-papers-scout paper.md --skip-slack                                # no Slack posting
/related-papers-scout <URL> --channel "press"                              # post to a different channel
/related-papers-scout <URL> --top 10 --institutions "google,meta,nvidia"   # 10 papers, custom institutions
/related-papers-scout <URL> --recency-months 6                             # only papers from last 6 months
```

### Pipeline

1. **Ingest** — Parse arXiv URL / local PDF / markdown -> title, abstract, key terms, arXiv ID
2. **Search** — 4 parallel agents: Semantic Scholar API, arXiv/Scholar, Papers With Code, Twitter/GitHub
3. **Rank** — Score by institution (30%), citations (20%), GitHub stars (20%), community buzz (15%), recency (15%)
4. **Deep Dive** — Parallel subagents produce structured Korean summaries per paper
5. **Report** — Consolidated markdown report saved to `outputs/papers/`
6. **Slack** — Main summary + 5 threaded paper summaries to target channel

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--skip-slack` | Skip Slack distribution | Slack enabled |
| `--channel <name>` | Target Slack channel | `research` |
| `--top N` | Number of papers to find | 5 |
| `--institutions "..."` | Comma-separated institution filter | `google,mit,stanford,nvidia` |
| `--recency-months N` | Max age of papers in months | 18 |

### Execution

1. Read and follow `.cursor/skills/related-papers-scout/SKILL.md`
2. Execute phases sequentially, respecting option flags
3. Phase 2 uses 4 parallel subagents; Phase 4 uses parallel subagents for deep dives

MCP tools used: `slack_send_message`, `slack_search_channels`.

Shell tools: `curl` for Semantic Scholar API and Defuddle extraction, `pdfplumber` for PDF parsing.

### Examples

Full pipeline for an arXiv paper:
```
/related-papers-scout https://arxiv.org/abs/2509.04664
```

Local PDF without Slack posting:
```
/related-papers-scout /path/to/paper.pdf --skip-slack
```

Custom institutions and count:
```
/related-papers-scout https://arxiv.org/abs/2509.04664 --top 10 --institutions "google,meta,nvidia,microsoft"
```
