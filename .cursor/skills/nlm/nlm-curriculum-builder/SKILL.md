---
name: nlm-curriculum-builder
description: >-
  Build a complete lecture curriculum in hours using NotebookLM: gather source
  materials, generate topical authority maps, ingest into NLM with a
  curriculum-designer persona, produce syllabi, per-module lesson plans,
  and 7 artifact types (slides, audio, quiz, flashcards, study guide,
  video, mind map) per module — then package and distribute.
  Use when the user asks to "build curriculum", "create course",
  "design a course", "lecture curriculum", "syllabus generator",
  "curriculum builder", "NLM curriculum", "커리큘럼 구축",
  "강의 설계", "교수요목 생성", "강좌 만들기",
  "nlm-curriculum-builder", or any request to build a multi-module
  academic or professional curriculum using NotebookLM.
  Do NOT use for personal accelerated learning -- use nlm-deep-learn.
  Do NOT use for ad-hoc studio_create on existing notebooks -- use notebooklm-studio.
  Do NOT use for single-topic slide generation -- use nlm-slides.
  Do NOT use for product discovery frameworks -- use nlm-discovery-lab.
metadata:
  author: thaki
  version: 1.0.0
  category: orchestration
---

# NLM Curriculum Builder

Compress weeks of curriculum development into hours. Upload source materials to NotebookLM, set a curriculum-designer persona with Bloom's Taxonomy alignment, generate a structured syllabus and per-module lesson plans, then batch-produce slides, quizzes, flashcards, audio overviews, video explainers, mind maps, and study guides for every module. Inspired by NYU/Stanford professors who now build entire courses in a single afternoon with NotebookLM.

## Prerequisites

- `notebooklm-mcp` MCP server registered and authenticated (see `notebooklm` skill)
- At least one source material (PDF, URL, YouTube transcript, or Google Doc)
- `anthropic-docx` skill available for DOCX generation
- Optionally: `gws-drive` for Google Drive upload, Slack MCP for distribution

## System Prompt

The curriculum-designer persona is stored at `references/system-prompt.md` (relative to this skill). Read it before Phase 3. It defines:

- Bloom's Taxonomy alignment for all learning objectives and assessments
- Backward Design (Understanding by Design) methodology
- Constructive Alignment between objectives, activities, and assessments
- Source grounding and citation rules
- 한국어 출력 규칙
- Quality gates for measurability and assessment coverage

## Templates

Two output templates guide structured generation:

- `references/syllabus-template.md` — master syllabus format (Phase 4)
- `references/lesson-plan-template.md` — per-module lesson plan format (Phase 5)

Read each template before the corresponding phase.

## Pipeline

### Phase 1: Gather Input

Collect from the user:
- **Course title and description**
- **Target audience** (undergraduate, graduate, professional, executive)
- **Number of weeks/modules** (default: 12)
- **Learning objectives** (3-5 high-level course outcomes)
- **Source materials** — at least one:
  - Local files (PDFs, DOCX, TXT)
  - URLs (papers, articles, documentation)
  - YouTube videos (transcript auto-extracted)
  - Google Docs / Slides
- **Output preferences** — which artifact types to generate per module (default: slides + quiz + flashcards + study guide)
- **Language** — 한국어 (기본값)

Use `AskQuestion` tool for structured collection when details are missing. Persist gathered input:

```
Write to: outputs/curriculum/{course-slug}/phase1-input.json
```

### Phase 2: Topical Authority Map

Generate a structured course map via LLM reasoning (without NLM — uses the agent's own knowledge plus any provided source summaries):

1. Break the course into modules/weeks based on the target audience and week count
2. For each module produce: topic title, 3-5 subtopics, 5-10 key questions, prerequisite modules
3. Generate a prerequisite dependency DAG across modules
4. Ensure Bloom's progression: early modules target Remember/Understand, later modules target Analyze/Evaluate/Create

```
Write to: outputs/curriculum/{course-slug}/authority-map.md
```

### Phase 3: Source Ingestion

1. **Create notebook:**
```
notebook_create(title="Curriculum: <Course Title>")
```

2. **Set curriculum-designer persona** using the system prompt from `references/system-prompt.md`:
```
chat_configure(notebook_id, goal="custom", custom_prompt="<system-prompt content>")
```

3. **Upload user-provided sources** sequentially with `wait=True`:
```
source_add(notebook_id, source_type="file", file_path="<path>", wait=True)
source_add(notebook_id, source_type="url", url="<url>", wait=True)
```

4. **Optionally run web research** for each module's key questions to discover supplementary sources (skip with `--skip-research`):
```
research_start(notebook_id, query="<module topic> curriculum resources key concepts", source="web", mode="fast")
research_status(notebook_id, task_id)
research_import(notebook_id, task_id)
```

5. **Save ingestion log:**
```
Write to: outputs/curriculum/{course-slug}/phase3-sources.json
```

**Source limit:** NotebookLM supports up to 50 sources per notebook. For courses exceeding 50 sources, create per-module notebooks in addition to the master notebook.

### Phase 4: Syllabus Generation

Read `references/syllabus-template.md` before generating.

1. **Query the notebook** to generate the master syllabus:
```
notebook_query(notebook_id, query="Based on all uploaded sources, generate a complete course syllabus for '<Course Title>' targeting <audience>. Include: course description, 5 measurable learning outcomes aligned to Bloom's Taxonomy, a <N>-week module sequence with topics and readings, assessment strategy with weights, required materials from the sources. Follow backward design: start with desired outcomes, then assessments, then activities.")
```

2. **Structure the response** using the syllabus template
3. **Save as notebook note** and local file:
```
note(notebook_id, action="create", title="Master Syllabus", content=<structured_syllabus>)
Write to: outputs/curriculum/{course-slug}/syllabus.md
```

4. **Generate DOCX** via `anthropic-docx` for formal distribution:
```
Write to: outputs/curriculum/{course-slug}/syllabus.docx
```

### Phase 5: Lesson Planning (Per Module)

Read `references/lesson-plan-template.md` before generating.

For each module in the syllabus:

1. **Query the notebook:**
```
notebook_query(notebook_id, query="Generate a detailed lesson plan for Module <N>: <Topic>. Include: 3 Bloom's-aligned learning objectives, essential questions, required readings with specific source sections, a timed lecture outline (60 min), at least 1 active learning activity, an assessment with rubric, and connection to the next module.")
```

2. **Structure** using the lesson plan template
3. **Save as notebook note** and local file:
```
note(notebook_id, action="create", title="Module <N>: <Topic> — Lesson Plan", content=<plan>)
Write to: outputs/curriculum/{course-slug}/module-{NN}/lesson-plan.md
```

Repeat for all modules. Process sequentially to maintain cross-module coherence.

### Phase 6: Material Generation (Per Module)

For each module, generate the user-selected artifacts via `studio_create`. Default set: slides + quiz + flashcards + study guide.

| Artifact | `artifact_type` | Output File | Purpose |
|----------|----------------|-------------|---------|
| Slide deck | `slide_deck` | `slides.pdf` | Lecture slides for instructor |
| Audio overview | `audio` | `audio-overview.mp3` | Pre-class listening for students |
| Quiz | `quiz` | `quiz.html` | Knowledge assessment |
| Flashcards | `flashcards` | `flashcards.html` | Study aids |
| Study guide | `report` | `study-guide.md` | Comprehensive review document |
| Video explainer | `video` | `video-explainer.mp4` | Visual concept explanation |
| Mind map | `mind_map` | `mind-map.json` | Topic relationship visualization |

For each artifact:
```
studio_create(notebook_id, artifact_type="<type>", confirm=True, focus_prompt="...", language="ko")
```

Type-specific options: `slide_format` (detailed_deck|presenter_slides), `question_count` (int), `difficulty` (easy|medium|hard), `report_format` (Briefing Doc|Study Guide), `custom_prompt` (for reports).

Poll `studio_status(notebook_id)` every 30 seconds until completion.

Download completed artifacts:
```
download_artifact(notebook_id, artifact_type="<type>", output_path="<abs_path>/outputs/curriculum/{course-slug}/module-{NN}/<filename>")
```

For slide decks: optionally use `studio_revise` for per-slide refinement if quality is insufficient.

**Rate limiting:** Process one artifact type across all modules before moving to the next type (batch by type, not by module) to reduce API pressure.

### Phase 7: Package and Distribute

1. **Compile manifest** listing all generated files:
```
Write to: outputs/curriculum/{course-slug}/manifest.json
```

2. **Generate consolidated curriculum overview DOCX** via `anthropic-docx`:
```
Write to: outputs/curriculum/{course-slug}/curriculum-overview.docx
```

3. **Optionally upload to Google Drive** via `gws-drive` (with `--drive`):
   - Create folder: `Curriculum: <Course Title>`
   - Upload all artifacts

4. **Optionally post to Slack** `#효정-할일` (with `--slack`):
   - Course title, module count, artifact count
   - Link to Drive folder if uploaded
   - Summary of Bloom's progression and assessment strategy

5. **Final directory structure:**
```
outputs/curriculum/{course-slug}/
  phase1-input.json
  authority-map.md
  phase3-sources.json
  syllabus.md
  syllabus.docx
  curriculum-overview.docx
  manifest.json
  module-01/
    lesson-plan.md
    slides.pdf
    audio-overview.mp3
    quiz.html
    flashcards.html
    study-guide.md
    video-explainer.mp4
    mind-map.json
  module-02/
    ...
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--lang ko` | 한국어 출력 (기본값) | 한국어 |
| `--weeks N` | Number of course weeks/modules | 12 |
| `--artifacts "slides,quiz,flashcards,report"` | Select artifact types per module | slides + quiz + flashcards + report |
| `--all-artifacts` | Generate all 7 artifact types per module | Default set only |
| `--skip-research` | Skip web research enrichment in Phase 3 | Research enabled |
| `--skip-materials` | Stop after lesson plans (skip Phase 6) | Full pipeline |
| `--drive` | Upload final package to Google Drive | No upload |
| `--slack` | Post summary to Slack #효정-할일 | No post |
| `--share "email1,email2"` | Share NotebookLM notebook with collaborators | No sharing |
| `--resume` | Resume from last completed phase (idempotency) | Start from Phase 1 |

## Examples

```
/nlm-curriculum-builder "Introduction to Machine Learning" --sources ~/textbooks/ml-intro.pdf ~/papers/gradient-descent.pdf --urls "https://cs229.stanford.edu/" "https://www.youtube.com/watch?v=..." --weeks 14 --lang ko --artifacts "slides,quiz,flashcards,report" --drive
```

This will:
1. Collect course info (ML intro, 14 weeks, Korean, 4 artifact types)
2. Generate topical authority map with 14 modules
3. Create NLM notebook, upload 2 PDFs + 2 URLs, optionally run web research
4. Generate master syllabus with Bloom's-aligned outcomes
5. Generate 14 per-module lesson plans with timed lecture outlines
6. Batch-generate slides, quizzes, flashcards, and study guides for each module
7. Package everything, generate overview DOCX, upload to Google Drive

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Syllabus too generic | Upload more targeted sources (research papers > general textbooks for depth) |
| Bloom's levels not progressing | Explicitly prompt for level progression in the authority map query |
| Lesson plans lack activities | Strengthen the lesson plan query — request "at least 2 active learning exercises" |
| Sources stuck processing | Use `wait=True, wait_timeout=300` on `source_add` |
| Too many modules for one notebook | Create per-module notebooks when sources exceed 50 |
| Studio artifacts low quality | Add the syllabus and lesson plan as notes before generating artifacts — richer context improves output |
| Quiz questions test recall only | Add note with Bloom's level expectations before generating quiz |
| Resume not working | Check `manifest.json` for phase completion markers |
| Persona not applied | Verify `chat_configure` was called after `notebook_create` and before queries |
| DOCX generation fails | Ensure `anthropic-docx` skill is available and `python-docx` is installed |

## When to Use the Meta-Harness Instead

For advanced scenarios, delegate to `nlm-curriculum-harness` (the multi-agent meta-harness):

| Scenario | Use This Skill | Use Meta-Harness |
|----------|---------------|-----------------|
| Simple single-pass curriculum | Yes | — |
| New tech emerged, update existing course | — | `tech-update` mode |
| 1-3 day compressed bootcamp | — | `rapid-bootcamp` mode |
| Compare against competitor courses | — | `benchmark` mode |
| Combine 3+ technologies into one course | — | `multi-tech-fusion` mode |
| Full build with quality gate loop | — | `full-build` mode |
| Needs evaluator-optimizer iteration | — | Any mode (built-in QE agent) |

## Related Skills

- **nlm-curriculum-harness** — multi-agent meta-harness for advanced curriculum operations
- **notebooklm** — notebook/source CRUD and querying
- **notebooklm-research** — web/Drive research and source import
- **notebooklm-studio** — ad-hoc studio content generation and download
- **nlm-deep-learn** — personal accelerated learning (learner-focused, not curriculum)
- **nlm-slides** — expert-level Korean slide generation
- **nlm-dual-slides** — dual-audience (elementary + expert) slide decks
- **anthropic-docx** — Word document generation
- **gws-drive** — Google Drive upload
- **docs-tutor** — local StudyVault quizzing (without NotebookLM)
