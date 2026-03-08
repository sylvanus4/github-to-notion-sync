---
name: nlm-video
description: >-
  End-to-end pipeline that transforms a local markdown document into professional
  NotebookLM video explainers. Splits sections, rewrites each into expert-level
  English and Korean narration, uploads to NotebookLM, generates videos, and
  downloads MP4 files.
  Use when the user asks to "create NLM video", "NLM 비디오", "비디오 만들어",
  "비디오 생성", "영상 만들어줘", "동영상 생성", "영상으로 만들어",
  "문서로 영상", "문서를 비디오로", "마크다운으로 비디오",
  "이 문서로 영상 만들어", "NLM 동영상", "설명 영상 생성",
  "NLM video explainer", "generate video from doc", "video from markdown",
  "make video from document", "expert video explainer",
  "NotebookLM video", "convert document to video",
  "turn this into a video", "영어 한국어 비디오", "nlm-video", "/nlm-video",
  or any request to convert a local document into NotebookLM videos.
  Do NOT use for ad-hoc studio_create calls on existing notebooks -- use
  notebooklm-studio. Do NOT use for slide generation from local docs -- use
  nlm-slides. Do NOT use for local video transcription -- use transcribee.
  Do NOT use for notebook management or source CRUD -- use notebooklm.
metadata:
  author: thaki
  version: 1.1.0
  category: generation
---

# NLM Video: Local Document to Expert Video Pipeline

End-to-end pipeline that transforms a local markdown document into professional NotebookLM video explainers in both English and Korean, written in domain-expert narrative tone with white background styling.

## Prerequisites

- `notebooklm-mcp` MCP server registered and authenticated (see `notebooklm` skill)
- A local markdown file with `##` section headings
- Authentication often expires between sessions; if `notebook_create` fails with "Authentication expired", run `nlm login` in terminal, then call `refresh_auth` MCP tool before retrying

## System Prompt

The expert rewrite system prompt is stored at `references/system-prompt.md` (relative to this skill). Read it before starting the pipeline. It defines:

- Expert narrative tone optimized for spoken delivery
- Transition cues and flow structure
- White background tone directive
- Content density and pacing requirements

## Pipeline

### Step 1: Read the Local Markdown

Read the user-specified markdown file. Identify the document title (from `#` heading or filename).

### Step 2: Split by Sections

Split the markdown content at `##` heading boundaries. Each section becomes an independent unit for rewriting. Preserve the heading text as the section title.

### Step 3: Expert Rewrite (EN + KO)

Using the system prompt from `references/system-prompt.md`, rewrite each section into **two versions**:

**English version:**
- Professional, authoritative domain-expert narrative tone
- Content structured for **spoken delivery** -- natural sentence flow
- Transition phrases between sections ("Now let's examine...", "Building on this...")
- Key data points woven into narrative rather than isolated bullets

**Korean version:**
- 전문가의 내레이션 톤 (formal narrative voice)
- Same structure and data points as the English version
- Natural Korean spoken phrasing with smooth transitions
- 핵심 지표를 자연스러운 문맥 안에서 전달

Combine all English sections into one document. Combine all Korean sections into one document.

### Step 4: Create NotebookLM Notebook

```
notebook_create(title="<Document Title> - Video")
```

### Step 5: Upload Sources

Upload both rewritten documents as text sources:

```
source_add(notebook_id, source_type="text", title="<Title> (EN)", text=<english_doc>, wait=True)
source_add(notebook_id, source_type="text", title="<Title> (KO)", text=<korean_doc>, wait=True)
```

### Step 6: Generate Video

```
studio_create(notebook_id, artifact_type="video", video_format="explainer", confirm=True)
```

Available `video_format` options:
- `explainer` (default) -- full explanatory video with detailed narration
- `brief` -- condensed overview hitting key points
- `cinematic` -- experimental cinematic style

Available `visual_style` options:
- `auto_select` (default), `classic`, `whiteboard`, `kawaii`, `anime`, `watercolor`, `retro_print`, `heritage`, `paper_craft`

Then poll until complete:

```
studio_status(notebook_id)
```

Poll every 30 seconds. Videos typically take **5-10 minutes**.

### Step 7: Download

Use an **absolute path** for `output_path` (MCP server resolves paths from its own cwd, not the workspace).

Determine the workspace root using the Cursor workspace path, then construct the absolute path:

```
download_artifact(
  notebook_id,
  artifact_type="video",
  output_path="<WORKSPACE_ROOT>/outputs/presentations/<title>-video-<date>.mp4"
)
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--lang en` | Generate English version only | Both EN + KO |
| `--lang ko` | Generate Korean version only | Both EN + KO |
| `--format brief` | Brief format instead of full explainer | `explainer` |
| `--format explainer` | Full explainer format | `explainer` |
| `--format cinematic` | Experimental cinematic style | `explainer` |
| `--style whiteboard` | Visual style override | `auto_select` |

## Video Formats

| Format | Description | Typical Duration |
|--------|-------------|-----------------|
| `explainer` | Full explanatory video with detailed narration | 3-5 min |
| `brief` | Condensed overview hitting key points | 1-2 min |
| `cinematic` | Experimental cinematic style (may vary) | 3-5 min |

## Visual Styles

| Style | Description |
|-------|-------------|
| `auto_select` | NLM chooses the best style (default) |
| `classic` | Clean professional look |
| `whiteboard` | Hand-drawn whiteboard aesthetic |
| `kawaii` | Cute/colorful cartoon style |
| `anime` | Anime-inspired visuals |
| `watercolor` | Watercolor painting aesthetic |
| `retro_print` | Vintage print look |
| `heritage` | Traditional/heritage styling |
| `paper_craft` | Paper craft / collage style |

## Output Convention

Files are saved to `outputs/presentations/`:

```
outputs/presentations/
  gpu-cloud-strategy-video-2026-03-08.mp4
  fed-rate-analysis-video-2026-03-08.mp4
```

When generating single-language versions:

```
outputs/presentations/
  gpu-cloud-strategy-video-en-2026-03-08.mp4
  gpu-cloud-strategy-video-ko-2026-03-08.mp4
```

## Example

```
/nlm-video docs/proposals/gpu-cloud-strategy.md
```

This will:
1. Read `docs/proposals/gpu-cloud-strategy.md`
2. Split into sections by `##` headings
3. Rewrite each section in expert narrative EN and KO
4. Create notebook "GPU Cloud Strategy - Video"
5. Upload EN and KO documents as sources
6. Generate video explainer
7. Download to `outputs/presentations/gpu-cloud-strategy-video-2026-03-08.mp4`

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Video generation slow | Normal -- videos take 5-10 minutes; keep polling |
| Content too superficial | Check that the rewrite step produced narrative depth, not just bullets |
| Wrong language | Use `--lang en` or `--lang ko` to generate single-language versions |
| Download fails | Ensure generation completed via `studio_status` first |
| File not found after download | Use absolute path in `output_path`; MCP server resolves from its own cwd |
| `format` parameter ignored | Use `video_format` (not `format`) in `studio_create` |

## Related Skills

- **notebooklm** -- notebook/source CRUD
- **notebooklm-studio** -- ad-hoc studio content generation
- **nlm-slides** -- same pipeline but for slide deck generation
- **transcribee** -- transcribe existing videos
