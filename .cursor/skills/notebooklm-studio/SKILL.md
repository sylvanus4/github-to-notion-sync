---
name: notebooklm-studio
description: >-
  Generate content from Google NotebookLM notebooks -- audio podcasts, video
  explainers, reports, quizzes, flashcards, mind maps, slide decks, infographics,
  and data tables. Download artifacts and export to Google Docs/Sheets.
  Use when the user asks to "create a podcast", "generate audio overview",
  "make a video", "create flashcards", "generate a report", "make a slide deck",
  "create an infographic", "generate mind map", "create data table",
  "generate quiz", "download artifact", "export to Google Docs",
  "revise slides", "check generation status", "studio content",
  "팟캐스트 생성", "오디오 생성", "비디오 생성", "플래시카드 만들기",
  "슬라이드 생성", "인포그래픽 생성", "마인드맵", "퀴즈 생성",
  "리포트 생성", "아티팩트 다운로드", "NLM studio", "NLM 콘텐츠 생성",
  "NotebookLM 콘텐츠", "NotebookLM podcast", "NLM 팟캐스트",
  or any NotebookLM content generation request.
  Do NOT use for notebook/source/note CRUD or querying -- use notebooklm.
  Do NOT use for web/Drive research pipelines -- use notebooklm-research.
  Do NOT use for end-to-end slide pipelines from local docs -- use nlm-slides.
  Do NOT use for end-to-end video pipelines from local docs -- use nlm-video.
  Do NOT use for local audio/video transcription -- use transcribee.
metadata:
  author: thaki
  version: 1.0.0
  category: generation
---

# NotebookLM Studio: Content Generation

Generate rich content from Google NotebookLM notebooks -- podcasts, videos, reports, study materials, presentations, and infographics. Download and export artifacts via the `notebooklm-mcp` MCP server.

## Prerequisites

- `notebooklm-mcp` MCP server registered and authenticated (see `notebooklm` skill)
- A notebook with at least one processed source (required for content generation)

## Available Tools

### Studio Content (4 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `studio_create` | Create any artifact type | `notebook_id`, `artifact_type`, `confirm=True`, type-specific params |
| `studio_status` | Check generation progress | `notebook_id` |
| `studio_delete` | Delete an artifact | `notebook_id`, `artifact_id`, `confirm=True` |
| `studio_revise` | Revise slides in existing deck | `notebook_id`, `artifact_id`, `instructions`, `confirm=True` |

### Download & Export (2 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `download_artifact` | Download any artifact type | `notebook_id`, `artifact_type`, `output_path` |
| `export_artifact` | Export to Google Docs/Sheets | `notebook_id`, `artifact_id` |

## Artifact Types Reference

| Type | Formats / Options | Typical Duration |
|------|-------------------|-----------------|
| `audio` | deep_dive, brief, critique, debate | 2-5 min |
| `video` | explainer, brief | 3-8 min |
| `report` | Briefing Doc, Study Guide, Blog Post | 1-2 min |
| `quiz` | `question_count` (default 10) | 1-2 min |
| `flashcards` | difficulty: easy, medium, hard | 1-2 min |
| `mind_map` | -- | 1-2 min |
| `slide_deck` | -- | 2-4 min |
| `infographic` | orientation: landscape/portrait; style: professional/modern | 2-4 min |
| `data_table` | -- | 1-2 min |

## Common Workflows

### Generate a podcast

1. `studio_create(notebook_id, artifact_type="audio", format="deep_dive", confirm=True)`
2. `studio_status(notebook_id)` -- poll until complete (check every 30s)
3. `download_artifact(notebook_id, artifact_type="audio", output_path="podcast.mp3")`

### Generate study materials

```
studio_create(notebook_id, artifact_type="quiz", question_count=10, confirm=True)
studio_create(notebook_id, artifact_type="flashcards", difficulty="hard", confirm=True)
studio_create(notebook_id, artifact_type="report", report_format="Study Guide", confirm=True)
```

### Create a presentation

1. `studio_create(notebook_id, artifact_type="slide_deck", confirm=True)`
2. `studio_status(notebook_id)` -- poll until complete
3. `studio_revise(notebook_id, artifact_id, instructions="Add more data charts", confirm=True)`
4. `download_artifact(notebook_id, artifact_type="slide_deck", output_path="deck.pptx")`

### Generate an infographic

```
studio_create(notebook_id, artifact_type="infographic", orientation="landscape", style="professional", confirm=True)
```

### Export to Google Docs

```
export_artifact(notebook_id, artifact_id)
```

## Polling Strategy

Content generation takes 1-5 minutes. Recommended polling approach:

1. Call `studio_create` to start generation
2. Wait 30 seconds
3. Call `studio_status` to check progress
4. If not complete, wait another 30 seconds and repeat
5. Once complete, call `download_artifact`

Do not poll more frequently than every 15 seconds to avoid rate limits.

## Stock Analytics Integration

### Daily report to podcast pipeline

1. Run the `today` skill to generate `outputs/reports/daily-YYYY-MM-DD.docx`
2. Create a notebook: `notebook_create(title="Daily Report 2026-03-08")`
3. Add the report: `source_add(notebook_id, source_type="file", file_path="outputs/reports/daily-2026-03-08.docx", wait=True)`
4. Generate podcast: `studio_create(notebook_id, artifact_type="audio", format="deep_dive", confirm=True)`
5. Download: `download_artifact(notebook_id, artifact_type="audio", output_path="outputs/podcasts/daily-2026-03-08.mp3")`

### Financial analysis study materials

1. Create a notebook from multiple analysis reports
2. Generate flashcards: `studio_create(notebook_id, artifact_type="flashcards", difficulty="medium", confirm=True)`
3. Generate quiz: `studio_create(notebook_id, artifact_type="quiz", question_count=15, confirm=True)`

### Accelerated learning study materials

1. Create a notebook loaded with textbooks and papers (see `notebooklm` skill)
2. Generate debate podcast on expert disagreements: `studio_create(notebook_id, artifact_type="audio", audio_format="debate", confirm=True)`
3. Generate flashcards on mental models: `studio_create(notebook_id, artifact_type="flashcards", difficulty="hard", confirm=True)`
4. Generate deep-understanding quiz: `studio_create(notebook_id, artifact_type="quiz", question_count=15, confirm=True)`
5. Generate intellectual landscape mind map: `studio_create(notebook_id, artifact_type="mind_map", confirm=True)`
6. Generate study guide: `studio_create(notebook_id, artifact_type="report", report_format="Study Guide", confirm=True)`

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Generation stuck | Call `studio_status` -- may still be processing (up to 10 min for audio) |
| Download fails | Ensure generation completed via `studio_status` first |
| "No sources" error | Add and process at least one source before creating content |
| Slide revise fails | Pass `confirm=True` -- destructive operations require confirmation |

## CLI Reference

```bash
nlm studio create <notebook_id> --type audio --format deep_dive --confirm
nlm studio status <notebook_id>
nlm download audio <notebook_id> <artifact_id>
nlm slides revise <notebook_id> <artifact_id> --instructions "..."
```

## Related Skills

- **notebooklm** -- notebook/source/note CRUD and querying
- **notebooklm-research** -- web/Drive research pipelines
- **nlm-deep-learn** -- accelerated learning pipeline using studio artifacts for study materials
- **today** -- daily stock analysis pipeline (produces .docx reports for podcast conversion)
- **anthropic-docx** -- Word document generation
