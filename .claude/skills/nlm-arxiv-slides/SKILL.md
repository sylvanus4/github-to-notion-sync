---
name: nlm-arxiv-slides
description: >-
  End-to-end pipeline that takes an arXiv paper URL, downloads the PDF,
  extracts and rewrites content into expert-level Korean, uploads to
  NotebookLM with optional web research enrichment, queries for key analysis,
  generates slide deck PDFs, and downloads them. Orchestrates 6 skills:
  defuddle, anthropic-pdf, nlm-slides, notebooklm, notebooklm-research,
  notebooklm-studio. Use when the user asks to "arxiv to slides", "paper to
  slides", "arxiv slides", "analyze arxiv paper", "arXiv 분석", "논문 슬라이드", "논문
  분석 슬라이드", "arXiv 논문 슬라이드", "arXiv paper slides", "nlm-arxiv-slides",
  "/nlm-arxiv-slides", or any request to convert an arXiv paper into
  NotebookLM slide decks. Do NOT use for ad-hoc studio_create on existing
  notebooks -- use notebooklm-studio. Do NOT use for local markdown to slides
  -- use nlm-slides. Do NOT use for general paper reading without slides --
  use anthropic-pdf. Do NOT use for non-arXiv URLs -- use nlm-slides with
  defuddle.
disable-model-invocation: true
---

# NLM arXiv Slides: arXiv Paper to Expert Slide Deck Pipeline

End-to-end pipeline that transforms an arXiv paper into professional NotebookLM slide decks in Korean, combining PDF analysis, expert rewriting, web research enrichment, and automated slide generation.

## Prerequisites

- `notebooklm-mcp` MCP server registered and authenticated (see `notebooklm` skill)
- `curl` available for PDF download and Defuddle abstract extraction
- `opendataloader-pdf` Python package + JDK 11+ (preferred PDF parser); `pdfplumber` as fallback (`pip install opendataloader-pdf pdfplumber`)
- Authentication often expires between sessions; if `notebook_create` fails with "Authentication expired", run `nlm login` in terminal, then call `refresh_auth` MCP tool before retrying

## Reference Files

Read these before executing the pipeline:

- `references/system-prompt.md` — Expert rewrite prompt adapted for academic papers (section-aware, visual hints for figures/equations/diagrams)
- `references/analysis-queries.md` — Predefined `notebook_query` templates for paper analysis (contributions, innovations, methodology, limitations)

## Pipeline

### Phase 1: Parse arXiv URL

Extract the paper ID from the user-provided URL.

Supported URL formats:
- `https://arxiv.org/abs/2509.04664`
- `https://arxiv.org/pdf/2509.04664`
- `https://arxiv.org/abs/2509.04664v2` (versioned)

Extract the ID (e.g., `2509.04664`) and construct:
- PDF URL: `https://arxiv.org/pdf/{ID}`
- Abstract URL: `https://arxiv.org/abs/{ID}`

### Phase 2: Download PDF + Fetch Structured Overview

Run three commands in parallel:

**Fetch AlphaXiv structured overview (token-efficient, preferred metadata source):**
```bash
curl -sL --max-time 30 "https://alphaxiv.org/overview/{ID}.md"
```

**Download PDF (needed as NotebookLM source in Phase 6):**
```bash
curl -L -o /tmp/arxiv-{ID}.pdf "https://arxiv.org/pdf/{ID}"
```

**Extract abstract metadata via Defuddle (fallback for metadata):**
```bash
curl -s "https://defuddle.md/arxiv.org/abs/{ID}"
```

**Choose metadata source (priority order):**

1. **AlphaXiv overview** (preferred): If valid markdown returned, parse for title,
   authors, abstract, date, and structured analysis. Save to `/tmp/arxiv-{ID}-alphaxiv.md`.
2. **Defuddle** (fallback): If AlphaXiv returns 404, use Defuddle output for
   title, authors, abstract, date.

Skills used: **alphaxiv-paper-lookup**, **defuddle**

### Phase 3: Extract Text from PDF (conditional)

**If AlphaXiv overview is available**: PDF text extraction is optional. The
structured overview provides sufficient content for the Phase 4 expert rewrite.
Skip this phase unless you need verbatim equation/table/figure data that the
overview lacks.

**If AlphaXiv is unavailable (404)**: Run OpenDataLoader extraction (fallback: pdfplumber):

```python
import opendataloader_pdf, os

pdf_path = "/tmp/arxiv-{ID}.pdf"
output_dir = "/tmp/odl-output"
os.makedirs(output_dir, exist_ok=True)

try:
    opendataloader_pdf.convert(input_path=pdf_path, output_dir=output_dir, format="markdown", quiet=True)
    stem = os.path.splitext(os.path.basename(pdf_path))[0]
    with open(os.path.join(output_dir, f"{stem}.md"), "r") as f:
        text = f.read()
except Exception:
    import pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)

with open("/tmp/arxiv-{ID}-extracted.md", "w") as f:
    f.write(text)
```

Combine all available sources into a structured document:
```
# {Paper Title}
**Authors:** {authors}
**arXiv:** {ID} | **Date:** {date}

## Abstract
{abstract}

## AlphaXiv Structured Overview
{alphaxiv overview content, if available — omit this section if 404}

## Full Paper Content
{extracted text from PDF, if OpenDataLoader/pdfplumber was run — omit if skipped}
```

Skills used: **anthropic-pdf** (patterns, conditional)

### Phase 4: Expert Rewrite (한국어)

Read the system prompt from `references/system-prompt.md`.

Split the extracted text into logical sections (look for headings like Introduction, Related Work, Methods/Methodology, Experiments/Results, Discussion, Conclusion).

Rewrite each section into **한국어 전문가 버전** following the system prompt:

- 전문가 톤 (formal expert voice)
- 핵심 기여와 발견을 **굵게** 강조
- `[시각: ...]` 힌트로 다이어그램, 수식, 결과 표 위치 표시
- 섹션당 3-6개 불릿 포인트
- 자연스러운 한국어 학술/기술 표현

하나의 한국어 문서로 통합합니다.

Skills used: **nlm-slides** (rewrite patterns)

### Phase 4.5: Content Quality Gate

Before creating the NotebookLM notebook, verify the expert rewrite output:
- [ ] 한국어 문서가 존재하고 단어 수 >= 300
- [ ] 섹션 헤딩이 최소 3개 (`##` 섹션)
- [ ] 원본에 그림/차트/수식이 있는 곳에 `[시각: ...]` 힌트 존재
- [ ] 원시 LaTeX나 깨진 포맷이 없음 (예: 코드 블록 밖의 `$`, `\begin{}`)

한국어 문서가 품질 기준 미달(< 300 단어 또는 < 3 섹션)이면 `references/system-prompt.md` 프롬프트를 사용하여 부족한 섹션을 다시 작성합니다.

### Phase 5: Create NotebookLM Notebook

```
notebook_create(title="arXiv: {Paper Title} - Analysis")
```

Save the `notebook_id` for subsequent steps.

Skills used: **notebooklm**

### Phase 6: Add Sources

Upload two sources sequentially with `wait=True`:

1. **Original PDF** (preserves figures, tables, equations):
```
source_add(notebook_id, source_type="file", file_path="/tmp/arxiv-{ID}.pdf", wait=True, wait_timeout=300)
```

2. **전문가 분석 (KO)**:
```
source_add(notebook_id, source_type="text", title="전문가 분석 (KO)", text=<korean_doc>, wait=True)
```

Use `wait_timeout=300` for the PDF source — academic papers with many figures can take longer to process.

Skills used: **notebooklm**

### Phase 7: Web Research Enrichment (Optional)

Skip if `--skip-research` is set.

Run web research to add related context:
```
research_start(notebook_id, query="{paper title} related work key findings implications", mode="web")
research_status(notebook_id, task_id, max_wait=300)
research_import(notebook_id, task_id)
```

Skills used: **notebooklm-research**

### Phase 8: Notebook Query for Analysis

Read query templates from `references/analysis-queries.md`.

Run analysis queries sequentially:

```
notebook_query(notebook_id, query="What are the 3-5 most important contributions of this paper? For each, explain the significance and how it advances the field.")
```

```
notebook_query(notebook_id, query="What are the key technical innovations or novel methods introduced? Explain the core mechanism and why existing approaches were insufficient.")
```

```
notebook_query(notebook_id, query="What are the main limitations, open questions, and promising future directions identified or implied by this work?")
```

Compile responses into an analysis summary and save:

```
Write to: outputs/papers/arxiv-{ID}-analysis-{DATE}.md
```

Also save as a notebook note for richer slide generation:
```
note(notebook_id, action="create", title="Paper Analysis Summary", content=<analysis_summary>)
```

Skills used: **notebooklm**

### Phase 9: Generate Slide Deck

```
studio_create(notebook_id, artifact_type="slide_deck", slide_format="detailed_deck", confirm=True, language="ko")
```

### Phase 10: Poll Status

Poll every 30 seconds until complete:
```
studio_status(notebook_id)
```

Slides typically take **5-8 minutes** for academic papers with rich source material.

### Phase 11: Download Slide PDF

Use an **absolute path** for `output_path` (MCP server resolves paths from its own cwd, not the workspace).

```
download_artifact(
  notebook_id,
  artifact_type="slide_deck",
  output_path="<WORKSPACE_ROOT>/outputs/presentations/arxiv-{ID}-slides-{DATE}.pdf"
)
```

Skills used: **notebooklm-studio**

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--lang ko` | 한국어 출력 (기본값) | 한국어 |
| `--skip-research` | Skip web research enrichment (Phase 7) | Research enabled |
| `--skip-analysis` | Skip notebook query analysis (Phase 8) | Analysis enabled |
| `--format detailed_deck` | Comprehensive slides | `detailed_deck` |
| `--format presenter_slides` | Speaker-note style slides | `detailed_deck` |
| `--length short` | Condensed slide count | `default` |
| `--output pptx` | Download as PPTX instead of PDF | `pdf` |
| `--extra-artifacts "audio,quiz"` | Generate additional artifacts beyond slides | Slides only |
| `--revise "instructions"` | Revise existing slides with specific instructions | -- |

### Extra Artifacts

When `--extra-artifacts` is specified, generate additional studio artifacts after slides:

| Type | Command | Typical Duration |
|------|---------|-----------------|
| `audio` | `studio_create(notebook_id, artifact_type="audio", audio_format="deep_dive", confirm=True)` | 2-5 min |
| `quiz` | `studio_create(notebook_id, artifact_type="quiz", question_count=10, confirm=True)` | 1-2 min |
| `flashcards` | `studio_create(notebook_id, artifact_type="flashcards", difficulty="hard", confirm=True)` | 1-2 min |
| `mind_map` | `studio_create(notebook_id, artifact_type="mind_map", confirm=True)` | 1-2 min |
| `report` | `studio_create(notebook_id, artifact_type="report", report_format="Study Guide", confirm=True)` | 1-2 min |

Download each extra artifact to `outputs/papers/arxiv-{ID}-{artifact_type}-{DATE}.{ext}`.

### Revising Slides

After initial generation, use `studio_revise` to iterate:
```
studio_revise(notebook_id, artifact_id, instructions="Add more data visualization suggestions to slide 4", confirm=True)
```

## Output Convention

Primary outputs:

```
outputs/
├── papers/
│   └── arxiv-2509.04664-analysis-2026-03-08.md
└── presentations/
    └── arxiv-2509.04664-slides-2026-03-08.pdf
```

With extra artifacts:

```
outputs/papers/
  arxiv-2509.04664-analysis-2026-03-08.md
  arxiv-2509.04664-audio-2026-03-08.mp3
  arxiv-2509.04664-quiz-2026-03-08.pdf
  arxiv-2509.04664-flashcards-2026-03-08.pdf
```

## Example

```
/nlm-arxiv-slides https://arxiv.org/abs/2509.04664
```

This will:
1. Parse ID `2509.04664` from the URL
2. Download PDF and extract abstract via Defuddle
3. Extract full text using OpenDataLoader (fallback: pdfplumber)
4. Rewrite into expert Korean document with visual hints
5. Create notebook "arXiv: Why Language Models Hallucinate - Analysis"
6. Upload PDF + Korean document as sources
7. Run web research for related context
8. Query for contributions, innovations, and limitations
9. Save analysis to `outputs/papers/arxiv-2509.04664-analysis-2026-03-08.md`
10. Generate slide deck and download to `outputs/presentations/arxiv-2509.04664-slides-2026-03-08.pdf`

```
/nlm-arxiv-slides https://arxiv.org/abs/2401.12345 --skip-research --extra-artifacts "audio,quiz"
```

This will run the pipeline without web research and also generate a deep-dive podcast and quiz alongside the slides.

## Skills Orchestrated

| Skill | Phase | Purpose |
|-------|-------|---------|
| alphaxiv-paper-lookup | 2 | Structured arXiv overview (token-efficient, primary metadata source) |
| defuddle | 2 | Extract arXiv abstract page metadata (fallback when AlphaXiv unavailable) |
| opendataloader | 3 | High-fidelity PDF-to-Markdown conversion (primary, conditional) |
| anthropic-pdf | 3 | PDF text extraction via pdfplumber (fallback, skippable when AlphaXiv available) |
| nlm-slides | 4 | Expert rewrite + visual hint patterns |
| notebooklm | 5-6, 8 | Notebook CRUD + source add + query |
| notebooklm-research | 7 | Web research enrichment |
| notebooklm-studio | 9-11 | Slide generation + polling + download |

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Authentication expired | Run `nlm login` in terminal, then call `refresh_auth` MCP tool |
| PDF download fails | Check arXiv URL is valid; try adding `v1` suffix (e.g., `2509.04664v1`) |
| opendataloader-pdf not found | `pip install opendataloader-pdf` + verify JDK 11+; falls back to pdfplumber |
| pdfplumber not found | Run `pip install pdfplumber` in the backend venv (fallback parser) |
| Extracted text garbled | Paper may use complex layouts; fall back to uploading PDF directly via `source_add(source_type="file")` |
| Slides lack depth | Ensure expert rewrite produced substantive content; check `references/system-prompt.md` was applied |
| Generation timeout | Poll `studio_status` every 30-60s; slides take **5-8 minutes** typically |
| File not found after download | Use **absolute path** in `output_path`; MCP server resolves from its own cwd |
| Research enrichment fails | Skip with `--skip-research`; pipeline works without it |

## Related Skills

- **alphaxiv-paper-lookup** — Structured arXiv paper overview (used in Phase 2 for token-efficient ingestion)
- **nlm-slides** — Local markdown to slides pipeline
- **nlm-deep-learn** — Accelerated learning with quizzes and study artifacts
- **notebooklm** — Notebook/source CRUD and querying
- **notebooklm-research** — Web/Drive research and import
- **notebooklm-studio** — Ad-hoc studio content generation
- **anthropic-pdf** — PDF reading, creation, manipulation
- **defuddle** — Clean markdown extraction from web pages
