---
name: nlm-dual-slides
description: >-
  Generate two audience-tailored NotebookLM slide decks (elementary + expert)
  from a single document, upload both PDFs to Google Drive, and post a summary
  with Drive links to Slack. Use when the user asks to "create dual slides",
  "elementary and expert slides", "dual audience slides", "nlm-dual-slides",
  "이중 슬라이드", "초등학생용 전문가용 슬라이드", "두 가지 슬라이드", "이중 청중 슬라이드",
  "/nlm-dual-slides", or needs two presentation levels from the same content.
  Do NOT use for single-audience slides only -- use nlm-slides.
  Do NOT use for ad-hoc studio_create on existing notebooks -- use notebooklm-studio.
  Do NOT use for video generation -- use nlm-video.
  Do NOT use for PowerPoint without NotebookLM -- use anthropic-pptx.
metadata:
  author: thaki
  version: "1.0.0"
  category: generation
---

# NLM Dual-Audience Slides: Elementary + Expert Slide Deck Pipeline

End-to-end pipeline that transforms a single document (markdown, PDF, or arXiv URL) into **two** NotebookLM slide decks — one for elementary-level audiences and one for domain experts — then uploads both to Google Drive and posts a summary with Drive links to Slack.

## Prerequisites

- `notebooklm-mcp` MCP server registered and authenticated (see `notebooklm` skill)
- `gws` CLI installed and authenticated (see `gws-workspace` skill)
- Slack MCP (`plugin-slack-slack`) configured
- If `notebook_create` fails with "Authentication expired", run `nlm login` in terminal, then call `refresh_auth` MCP tool before retrying

## System Prompts

Two audience-specific rewrite prompts are stored in `references/` (relative to this skill):

| Prompt File | Audience | Key Characteristics |
|---|---|---|
| `references/expert-prompt.md` | Domain experts | White background, architecture diagrams, benchmark tables, mathematical frameworks, ablation results, data-driven clean layout |
| `references/elementary-prompt.md` | Elementary students (grades 3-5) | Simple analogies, colorful icons, one concept per slide, no equations, grade-school vocabulary |

Read **both** prompts before starting the pipeline.

## Pipeline

### Phase 1 — Content Ingestion

Accept one of three input types:

**Local markdown file:**
- Read the file directly
- Extract title from `#` heading or filename

**PDF file:**
- Extract text using `anthropic-pdf` skill patterns (Read tool on PDF path)
- Parse section boundaries from headings

**arXiv URL:**
- Extract paper ID from the URL
- Use `alphaxiv-paper-lookup` for structured overview, OR
- Use `defuddle` to extract clean markdown from the arXiv abstract page
- Use `anthropic-pdf` to read the full PDF if needed

Split content at `##` heading boundaries. Each section becomes an independent rewrite unit.

### Phase 2 — Dual Audience Rewrite

Read both system prompts from `references/`. For each section of the source content, produce **four** rewritten documents:

**Using `references/expert-prompt.md`:**
1. Expert English version — authoritative, data-dense, with `[Visual: ...]` annotations for architecture diagrams, benchmark tables, equation blocks, ablation matrices
2. Expert Korean version — same structure, natural Korean technical prose

**Using `references/elementary-prompt.md`:**
3. Elementary English version — fun analogies, simple language, one concept per section, colorful visual suggestions
4. Elementary Korean version — 쉬운 존댓말, kid-friendly Korean examples

Combine sections into four complete documents:
- `expert_en` — all expert English sections
- `expert_ko` — all expert Korean sections
- `elementary_en` — all elementary English sections
- `elementary_ko` — all elementary Korean sections

### Phase 3 — Create NotebookLM Notebooks

Create two separate notebooks:

```
notebook_create(title="{Title} - Elementary Slides")
notebook_create(title="{Title} - Expert Slides")
```

Upload corresponding source documents as text sources:

```
# Elementary notebook
source_add(notebook_id=ELEM_NB_ID, source_type="text", title="{Title} Elementary (EN)", text=elementary_en, wait=True)
source_add(notebook_id=ELEM_NB_ID, source_type="text", title="{Title} Elementary (KO)", text=elementary_ko, wait=True)

# Expert notebook
source_add(notebook_id=EXPERT_NB_ID, source_type="text", title="{Title} Expert (EN)", text=expert_en, wait=True)
source_add(notebook_id=EXPERT_NB_ID, source_type="text", title="{Title} Expert (KO)", text=expert_ko, wait=True)
```

### Phase 4 — Generate + Download Slides

Start slide generation for **both** notebooks (can run in parallel). Default output language is **Korean** (`language="ko"`):

```
studio_create(notebook_id=ELEM_NB_ID, artifact_type="slide_deck", slide_format="detailed_deck", language="ko", confirm=True)
studio_create(notebook_id=EXPERT_NB_ID, artifact_type="slide_deck", slide_format="detailed_deck", language="ko", confirm=True)
```

Poll both notebooks every 30 seconds until complete (typically 5-8 minutes each):

```
studio_status(notebook_id=ELEM_NB_ID)
studio_status(notebook_id=EXPERT_NB_ID)
```

**Optional expert revision**: If the expert slides need refinement for white-background data-driven layout:

```
studio_revise(notebook_id=EXPERT_NB_ID, artifact_id=ARTIFACT_ID,
  instructions="Ensure white background on all slides. Use clean data tables for benchmark results. Render equations with high contrast. Minimize decorative elements.",
  confirm=True)
```

Download both slide decks using **absolute paths**:

```
download_artifact(
  notebook_id=ELEM_NB_ID,
  artifact_type="slide_deck",
  output_path="<WORKSPACE_ROOT>/outputs/presentations/{id}-Elementary-Slides-{DATE}.pdf"
)

download_artifact(
  notebook_id=EXPERT_NB_ID,
  artifact_type="slide_deck",
  output_path="<WORKSPACE_ROOT>/outputs/presentations/{id}-Expert-Slides-{DATE}.pdf"
)
```

### Phase 5 — Google Drive Upload

Upload both PDFs using the `gws` CLI:

```bash
gws drive +upload ./outputs/presentations/{id}-Elementary-Slides-{DATE}.pdf
gws drive +upload ./outputs/presentations/{id}-Expert-Slides-{DATE}.pdf
```

If `--drive-folder` is specified:

```bash
gws drive +upload ./outputs/presentations/{id}-Elementary-Slides-{DATE}.pdf --parent FOLDER_ID
gws drive +upload ./outputs/presentations/{id}-Expert-Slides-{DATE}.pdf --parent FOLDER_ID
```

Extract file IDs from the upload output. Construct shareable links:
- `https://drive.google.com/file/d/{ELEM_FILE_ID}/view`
- `https://drive.google.com/file/d/{EXPERT_FILE_ID}/view`

### Phase 6 — Slack Distribution

Post to the configured channel (default: `#deep-research-trending`, ID `C0AN34G4QHK`) using the Slack MCP `slack_send_message` tool.

**Message 1 — Main summary** (Korean):

```
📊 *{Title} — 이중 청중 슬라이드 생성 완료*

{content의 2-3문장 요약}

📎 *Google Drive 링크:*
• 초등학생용 슬라이드: {elementary_drive_link}
• 전문가용 슬라이드: {expert_drive_link}
```

Call `slack_send_message` with `channel_id` and `message`. Capture the returned `thread_ts`.

**Message 2 — Elementary slides thread reply**:

```
🎨 *초등학생용 슬라이드 요약*
• 대상: 초등학교 3-5학년 수준
• 특징: 쉬운 비유, 아이콘 기반 시각 자료, 핵심 개념 1개/슬라이드
• {key points from the elementary version}
```

Call `slack_send_message` with `thread_ts` from Message 1.

**Message 3 — Expert slides thread reply**:

```
🔬 *전문가용 슬라이드 요약*
• 대상: 도메인 전문가 / 기술 리더
• 특징: 흰색 배경, 벤치마크 비교표, 수학적 프레임워크, 절제 실험 결과
• {key technical points from the expert version}
```

Call `slack_send_message` with `thread_ts` from Message 1.

## Options

| Option | Description | Default |
|---|---|---|
| `--lang en` | Generate English version only | Both EN + KO |
| `--lang ko` | Generate Korean version only | Both EN + KO |
| `--skip-elementary` | Skip elementary slides | Both audiences |
| `--skip-expert` | Skip expert slides | Both audiences |
| `--skip-drive` | Skip Google Drive upload | Drive enabled |
| `--skip-slack` | Skip Slack posting | Slack enabled |
| `--drive-folder ID` | Google Drive folder ID for uploads | Drive root |
| `--channel name` | Slack channel name | `deep-research-trending` |
| `--nlm-lang CODE` | NotebookLM slide output language (BCP-47) | `ko` (Korean) |
| `--revise` | Run `studio_revise` on expert deck for white-bg refinement | disabled |

## Output Convention

```
outputs/presentations/
  {id}-Elementary-Slides-{DATE}.pdf
  {id}-Expert-Slides-{DATE}.pdf
```

Where `{id}` is a slug derived from the document title (e.g., `sefo-v3`, `gpu-cloud-strategy`) and `{DATE}` is `YYYY-MM-DD`.

## Examples

### Example 1: Markdown file — full pipeline

```
/nlm-dual-slides output/papers/sefo-v3/SEFO-v3-EN.md
```

This will:
1. Read `output/papers/sefo-v3/SEFO-v3-EN.md`
2. Split into sections by `##` headings
3. Rewrite each section into 4 variants (expert EN/KO + elementary EN/KO)
4. Create two NotebookLM notebooks ("SEFO v3 - Elementary Slides", "SEFO v3 - Expert Slides")
5. Upload EN + KO sources to each notebook
6. Generate slide decks for both notebooks (parallel)
7. Download PDFs to `outputs/presentations/sefo-v3-Elementary-Slides-2026-03-22.pdf` and `sefo-v3-Expert-Slides-2026-03-22.pdf`
8. Upload both PDFs to Google Drive
9. Post summary + Drive links to `#deep-research-trending` with threaded details

### Example 2: arXiv URL — expert only, custom Drive folder

```
/nlm-dual-slides https://arxiv.org/abs/2403.12345 --skip-elementary --drive-folder 1a2b3c4d5e
```

This will:
1. Extract paper ID `2403.12345`, fetch structured overview via `alphaxiv-paper-lookup`
2. Skip elementary rewrite — produce only expert EN/KO documents
3. Create one NotebookLM notebook ("Paper Title - Expert Slides")
4. Generate expert slide deck, download PDF
5. Upload to the specified Google Drive folder
6. Post summary with Drive link to `#deep-research-trending`

### Example 3: PDF file — elementary only, Korean, skip Slack

```
/nlm-dual-slides docs/proposals/gpu-cloud-strategy.pdf --skip-expert --lang ko --skip-slack
```

This will:
1. Extract text from PDF using `anthropic-pdf` patterns
2. Skip expert rewrite — produce only elementary Korean document
3. Create one NotebookLM notebook, upload Korean source
4. Generate elementary slide deck, download PDF
5. Upload to Google Drive
6. No Slack posting

## Troubleshooting

| Symptom | Fix |
|---|---|
| Authentication expired (NLM) | Run `nlm login` in terminal, then call `refresh_auth` MCP tool |
| Authentication expired (Drive) | Run `gws auth login` |
| Slides lack depth (expert) | Check that expert rewrite followed `references/expert-prompt.md` — ensure architecture diagrams, benchmark tables, equations are present |
| Slides too complex (elementary) | Check that elementary rewrite followed `references/elementary-prompt.md` — ensure no jargon, no equations, analogies present |
| Generation timeout | Poll `studio_status` every 30-60s; slides take **5-8 minutes** per deck |
| File not found after download | Use **absolute path** in `output_path`; NLM MCP resolves from its own cwd |
| Drive upload fails | Verify `gws auth status` and retry; check file path exists |
| Slack posting fails | Verify channel ID `C0AN34G4QHK` is accessible; use `slack_search_channels` to confirm |

## Skills Composed

| Skill | Phase | Purpose |
|---|---|---|
| `nlm-slides` | 1-2 | Content ingestion + rewrite patterns |
| `nlm-arxiv-slides` | 1 | arXiv URL handling (when applicable) |
| `anthropic-pdf` | 1 | PDF text extraction (when applicable) |
| `defuddle` | 1 | Web page / arXiv abstract extraction |
| `alphaxiv-paper-lookup` | 1 | Structured arXiv overview |
| `notebooklm` | 3 | Notebook creation + source upload |
| `notebooklm-studio` | 4 | Slide generation + polling + download |
| `gws-drive` | 5 | Google Drive file upload |
| Slack MCP | 6 | Channel messaging with threads |

## Related Skills

- **nlm-slides** — single-audience expert slide deck pipeline
- **nlm-arxiv-slides** — arXiv paper to NLM slides (single audience)
- **notebooklm-studio** — ad-hoc studio content generation
- **paper-review** — full paper review pipeline (includes NLM slides)
- **gws-drive** — Google Drive file management
