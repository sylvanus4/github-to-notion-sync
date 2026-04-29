## Paper Review (Deep Analysis + Peer Review)

Deep academic paper analysis: ingest paper → structured Korean review → evidence-based peer review with severity grading (FATAL/MAJOR/MINOR) → revision plan. Pure analysis only — no PM perspectives, no DOCX/PPTX, no Notion/Slack distribution.

### Usage

```
/paper-review <arXiv-URL>                                    # full deep analysis
/paper-review /path/to/paper.pdf                             # local PDF input
/paper-review paper.md                                       # local markdown input
/paper-review <URL> --skip-peer-review                       # Korean review only, no peer review
```

### Pipeline

1. **Ingest** — Parse arXiv URL / local PDF / markdown → structured text
2. **Review** — Generate structured Korean paper review (core deliverable)
3. **Peer Review** — Evidence-based peer review with severity grading + revision plan
4. **Verify** — Cross-check claims, citations, and consistency
5. **Deliver** — Consolidated Korean analysis output

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--skip-peer-review` | Skip Phase 3 peer review | Peer review enabled |
| `--severity-threshold` | Minimum severity to include (MINOR/MAJOR/FATAL) | MINOR |

### Execution

1. Read and follow `.cursor/skills/research/paper-review/SKILL.md`
2. Read `references/review-template.md` as needed for Phase 2

### Examples

Full deep analysis for an arXiv paper:
```
/paper-review https://arxiv.org/abs/2509.04664
```

Local PDF with review only (no peer review):
```
/paper-review /path/to/paper.pdf --skip-peer-review
```

### Related Commands

- `/paper-review-pipeline` — Full end-to-end pipeline with PM analysis + DOCX/PPTX + NLM slides + Notion/Slack distribution
