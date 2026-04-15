---
name: nlm-slides
description: >-
  End-to-end pipeline that transforms a local markdown document into professional
  NotebookLM slide decks. Splits sections, rewrites each into expert-level Korean,
  uploads to NotebookLM, generates slide decks, and downloads PDFs.
  Use when the user asks to "create NLM slides", "NLM 슬라이드", "슬라이드 만들어",
  "generate slides from doc", "convert document to slides", or convert a local
  document into NotebookLM slide decks.
  Do NOT use for ad-hoc studio_create on existing notebooks -- use notebooklm-studio.
  Do NOT use for video from local docs -- use nlm-video. Do NOT use for PowerPoint
  without NotebookLM -- use anthropic-pptx. Do NOT use for notebook CRUD -- use
  notebooklm.
metadata:
  author: thaki
  version: 1.1.0
  category: generation
---

# NLM Slides: Local Document to Expert Slide Deck Pipeline

End-to-end pipeline that transforms a local markdown document into professional NotebookLM slide decks in Korean, written in domain-expert tone with white background styling.

## Prerequisites

- `notebooklm-mcp` MCP server registered and authenticated (see `notebooklm` skill)
- A local markdown file with `##` section headings
- Authentication often expires between sessions; if `notebook_create` fails with "Authentication expired", run `nlm login` in terminal, then call `refresh_auth` MCP tool before retrying

## System Prompt

The expert rewrite system prompt is stored at `references/system-prompt.md` (relative to this skill). Read it before starting the pipeline. It defines:

- Expert tone and domain authority for Korean
- Presentation-friendly formatting rules
- White background tone directive
- Content density requirements

## Pipeline

### Step 1: Read the Local Markdown

Read the user-specified markdown file. Identify the document title (from `#` heading or filename).

### Step 2: Split by Sections

Split the markdown content at `##` heading boundaries. Each section becomes an independent unit for rewriting. Preserve the heading text as the section title.

### Step 3: Expert Rewrite (한국어)

Using the system prompt from `references/system-prompt.md`, rewrite each section into **한국어 전문가 버전**:

- 전문가 톤 (formal expert voice)
- 핵심 지표와 데이터를 강조하는 짧은 불릿 포인트 (≤6 단어 — Winston 규칙)
- 원본 섹션 구조에 맞는 명확한 헤더
- 프레젠테이션 최적화: 문단 없이 스캔 가능한 포인트만
- 슬라이드 섹션당 ≤40 단어 (Winston: 슬라이드는 발표자를 보조하지 대체하지 않음)
- 시각 자료가 도움이 될 곳에 `[시각: ...]` 힌트 삽입
- 발표자 내레이션은 발표자 노트에 배치

모든 섹션을 하나의 한국어 문서로 통합합니다.

### Step 4: Create NotebookLM Notebook

```
notebook_create(title="<Document Title> - Slides")
```

### Step 5: Upload Sources

Upload the rewritten Korean document as a text source:

```
source_add(notebook_id, source_type="text", title="<Title> (KO)", text=<korean_doc>, wait=True)
```

### Step 6: Generate Slide Deck

```
studio_create(notebook_id, artifact_type="slide_deck", slide_format="detailed_deck", confirm=True, language="ko")
```

Available `slide_format` options:
- `detailed_deck` (default) -- comprehensive slides with full content
- `presenter_slides` -- speaker-note style with key talking points (Winston-recommended: keeps slide face minimal, puts narration in notes)

Available `slide_length` options:
- `default` -- standard length
- `short` -- condensed version

Then poll until complete:

```
studio_status(notebook_id)
```

Poll every 30 seconds. Slide decks typically take **5-8 minutes** (not 2-4).

### Step 7: Download

Use an **absolute path** for `output_path` (MCP server resolves paths from its own cwd, not the workspace).

Determine the workspace root using the Cursor workspace path, then construct the absolute path:

```
download_artifact(
  notebook_id,
  artifact_type="slide_deck",
  output_path="<WORKSPACE_ROOT>/outputs/presentations/<title>-slides-<date>.pdf"
)
```

For PPTX format instead of PDF:

```
download_artifact(
  notebook_id,
  artifact_type="slide_deck",
  output_path="<WORKSPACE_ROOT>/outputs/presentations/<title>-slides-<date>.pptx",
  slide_deck_format="pptx"
)
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--lang ko` | 한국어 출력 (기본값) | 한국어 |
| `--format detailed_deck` | Comprehensive slides | `detailed_deck` |
| `--format presenter_slides` | Speaker-note style slides | `detailed_deck` |
| `--length short` | Condensed slide count | `default` |
| `--output pptx` | Download as PPTX instead of PDF | `pdf` |
| `--revise "instructions"` | Revise existing slides with specific instructions | -- |

### Revising Slides

After initial generation, use `studio_revise` to iterate on individual slides:

```
studio_revise(notebook_id, artifact_id, instructions="Make slide 3 more data-driven", confirm=True)
```

## Output Convention

Files are saved to `outputs/presentations/`. Default format is PDF (NotebookLM generates slides as PDF; use `slide_deck_format="pptx"` for PPTX):

```
outputs/presentations/
  gpu-cloud-strategy-slides-2026-03-08.pdf
  fed-rate-analysis-slides-2026-03-08.pdf
```

## Example

```
/nlm-slides docs/proposals/gpu-cloud-strategy.md
```

This will:
1. Read `docs/proposals/gpu-cloud-strategy.md`
2. Split into sections by `##` headings
3. Rewrite each section in expert Korean
4. Create notebook "GPU Cloud Strategy - Slides"
5. Upload Korean document as source
6. Generate slide deck
7. Download to `outputs/presentations/gpu-cloud-strategy-slides-2026-03-08.pdf`

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Authentication expired | Run `nlm login` in terminal, then call `refresh_auth` MCP tool |
| Slides lack depth | Check that the rewrite step produced substantive content, not summaries |
| Too much text on slides | Apply Winston density rules: ≤40 words visible per slide, ≤6 words per bullet; move narration to speaker notes |
| 언어 문제 | 시스템 프롬프트의 한국어 규칙을 확인하세요 |
| Generation timeout | Poll `studio_status` every 30-60s; slides take **5-8 minutes** typically |
| File not found after download | Use **absolute path** in `output_path`; MCP server resolves from its own cwd |
| Revise not working | Ensure `confirm=True` is passed to `studio_revise` |

## Related Skills

- **notebooklm** -- notebook/source CRUD
- **notebooklm-studio** -- ad-hoc studio content generation
- **nlm-video** -- same pipeline but for video generation
- **anthropic-pptx** -- local PowerPoint creation without NotebookLM
- **winston-speaking-coach** -- pre-production coaching for slide content audit and delivery

## Winston Framework Integration

Content rewriting in Step 3 enforces these Winston "How to Speak" principles:

| Principle | Application |
|-----------|-------------|
| **≤40 words per slide** | Rewrite step caps visible text per section |
| **≤6 words per bullet** | Keywords and metrics only — no sentences |
| **Image cues** | Rewrite inserts `[시각: ...]` placeholders for diagrams/charts |
| **Presenter Mode** | `presenter_slides` format keeps narration in notes, not on slide face |
| **Speaker ≠ Slide** | Content the presenter will say goes in speaker notes |

For a full Winston coaching session before generating slides, run `winston-speaking-coach` first and use its Slide Audit output to guide the rewrite.
