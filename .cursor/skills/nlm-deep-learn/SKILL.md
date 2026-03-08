---
name: nlm-deep-learn
description: >-
  Accelerated learning pipeline: upload sources to NotebookLM, extract core
  mental models, map expert disagreements and consensus, run deep-understanding
  quizzes with gap analysis, generate study artifacts (debate podcast,
  flashcards, quiz, mind map, study guide).
  Use when the user asks to "deep learn", "accelerated learning",
  "compress learning", "mental models for", "48-hour learning",
  "NLM deep learn", "가속 학습", "멘탈 모델 추출", "심층 이해 퀴즈",
  or any request to deeply learn a subject using NotebookLM.
  Do NOT use for ad-hoc studio_create -- use notebooklm-studio.
  Do NOT use for product discovery -- use nlm-discovery-lab.
  Do NOT use for local StudyVault quizzing -- use docs-tutor.
metadata:
  author: thaki
  version: 1.0.0
  category: orchestration
---

# NLM Deep Learn: Accelerated Learning Pipeline

Compress a semester of learning into hours. Mass-upload source materials to NotebookLM, extract the mental models experts share, map the intellectual landscape of debates and consensus, then test deep understanding through interactive quizzes powered by the full corpus. The difference between a semester and 48 hours isn't the amount of content — it's knowing which questions to ask.

## Prerequisites

- `notebooklm-mcp` MCP server registered and authenticated (see `notebooklm` skill)
- At least one source material (PDF, URL, or text) — more sources produce richer results

## System Prompt

The intellectual landscape document rewrite system prompt is stored at `references/system-prompt.md` (relative to this skill). Read it before Phase 4. It defines:

- Socratic, depth-first tone for each language
- Structure: Mental Models -> Debates -> Consensus -> Open Questions -> Study Path
- EN + KO bilingual rules
- Quality gates for depth vs. surface-level summarization

## Question Rules

Deep understanding question design rules are stored at `references/question-rules.md` (relative to this skill). Read it before Phase 5. It defines:

- Question types that expose deep understanding vs. memorization
- Zero-hint policy for quiz options
- Difficulty calibration based on proficiency
- Gap follow-up protocol

## Pipeline

### Phase 1: Gather Input

Collect from the user:
- **Subject** (the topic or field to learn, e.g., "Transformer architectures in NLP")
- **Learning goal** (what competence looks like, e.g., "hold a conversation with a thesis advisor")
- **Source materials** — at least one, ideally many:
  - Local files (PDFs, DOCX, TXT)
  - URLs (papers, articles, documentation)
  - Raw text (lecture transcripts, notes)
- **Prior knowledge** (optional: what the user already knows to skip basics)
- **Time budget** (optional: affects quiz rounds and artifact selection)

### Phase 2: Source Ingestion

1. Create notebook:
```
notebook_create(title="Deep Learn: <Subject>")
```

2. Upload all source materials sequentially with `wait=True`:
```
source_add(notebook_id, source_type="file", file_path="<absolute_path>", wait=True)
source_add(notebook_id, source_type="url", url="<url>", wait=True)
source_add(notebook_id, source_type="text", text="<transcript>", title="<title>", wait=True)
```

3. Optionally run web research for additional coverage:
```
research_start(notebook_id, query="<subject> comprehensive overview key concepts expert perspectives", source="web", mode="fast")
research_status(notebook_id, task_id)
research_import(notebook_id, task_id)
```

### Phase 3: Mental Model Extraction

Query the notebook to extract the foundational thinking frameworks:

```
notebook_query(notebook_id, query="What are the 5 core mental models that every expert in <subject> shares? For each mental model, explain: (1) what it is, (2) why experts consider it fundamental, (3) how it changes the way you think about problems in this field.")
```

Save the response as a note for reference:
```
note(notebook_id, action="create", title="Core Mental Models", content=<response>)
```

### Phase 4: Intellectual Landscape Mapping

Run three queries to build a complete map of the field:

**Query 1 — Expert Disagreements:**
```
notebook_query(notebook_id, query="Show me the 3 places where experts in <subject> fundamentally disagree, and what each side's strongest argument is. Include the evidence each side cites and why the debate remains unresolved.")
```

**Query 2 — Established Consensus:**
```
notebook_query(notebook_id, query="What are the core principles in <subject> that virtually all experts agree on? What makes these non-controversial? Are there any caveats or boundary conditions where even the consensus breaks down?")
```

**Query 3 — Open Questions:**
```
notebook_query(notebook_id, query="What are the biggest unsolved problems or open questions in <subject>? For each, explain why it matters, what approaches have been tried, and what would a breakthrough look like.")
```

Compile all three responses into an intellectual landscape document using the system prompt from `references/system-prompt.md`. Save locally:

```
Write to: outputs/deep-learn/<subject>-<date>/intellectual-landscape.md
```

Save as a notebook note for quiz context:
```
note(notebook_id, action="create", title="Intellectual Landscape", content=<compiled_document>)
```

### Phase 5: Deep Understanding Quiz Loop

Read `references/question-rules.md` before generating questions.

**Repeat for `--rounds` iterations (default: 3):**

1. **Generate questions** via notebook query:
```
notebook_query(notebook_id, query="Generate <N> questions that would expose whether someone deeply understands <subject> versus someone who just memorized facts. Each question should require applying mental models, not recalling definitions. Format: numbered list with the question, 4 answer options (A-D), and the correct answer marked.")
```

2. **Parse** the response into structured questions (question text, 4 options, correct answer).

3. **Present quiz** using AskQuestion:
   - `--questions` per round (default: 5)
   - 4 options each, single-select
   - Header format: `"Q1. <Topic>"` (max 12 chars)
   - No hints in option descriptions

4. **Grade and explain** — for each wrong answer:
```
notebook_query(notebook_id, query="The student answered '<wrong_answer>' to the question '<question>'. The correct answer is '<correct_answer>'. Explain why their answer is wrong and what mental model or concept they are missing. Connect this to the broader intellectual landscape of <subject>.")
```

5. **Show results table:**

| Question | Correct | Your Answer | Result |
|----------|---------|-------------|--------|
| Q1 | B | A | Wrong |
| Q2 | C | C | Correct |

6. **Track proficiency** — update `outputs/deep-learn/<subject>-<date>/proficiency.md`:

```markdown
# <Subject> — Proficiency Tracker

| Concept | Attempts | Correct | Last Tested | Status |
|---------|----------|---------|-------------|--------|
| mental model X | 2 | 1 | 2026-03-08 | Wrong |

### Gap Notes

**mental model X**
- Confused: what the student mixed up
- Key insight: the correct understanding
- Source: which source material covers this
```

Proficiency badges: Wrong 0-39% / Fair 40-69% / Good 70-89% / Mastered 90-100%

7. **Ask to continue** — offer options via AskQuestion:
   - "Continue studying" (another quiz round with adjusted difficulty)
   - "Focus on weak areas" (regenerate questions targeting gaps)
   - "Generate study artifacts" (proceed to Phase 7)
   - "Done for now" (save progress and stop)

### Phase 6: Gap Analysis Summary

After all quiz rounds, compile a gap analysis:

```
notebook_query(notebook_id, query="Based on these areas where the student struggled: <list_of_gaps>. Create a targeted study plan that addresses each gap. For each gap: (1) which mental model is weak, (2) which sources cover this best, (3) a concrete exercise to build understanding.")
```

Save as note:
```
note(notebook_id, action="create", title="Gap Analysis & Study Plan", content=<response>)
```

### Phase 7: Artifact Generation

Generate 5 study artifacts from the loaded notebook. Skip if `--skip-artifacts` is set.

1. **Expert Debate Podcast** — two-sided debate on key disagreements:
```
studio_create(notebook_id, artifact_type="audio", audio_format="debate", confirm=True)
```

2. **Mental Model Flashcards** — core concepts distilled:
```
studio_create(notebook_id, artifact_type="flashcards", difficulty="hard", confirm=True)
```

3. **Deep Understanding Quiz** — exportable quiz for later review:
```
studio_create(notebook_id, artifact_type="quiz", question_count=15, confirm=True)
```

4. **Intellectual Landscape Mind Map** — visual overview of the field:
```
studio_create(notebook_id, artifact_type="mind_map", confirm=True)
```

5. **Comprehensive Study Guide** — reference document:
```
studio_create(notebook_id, artifact_type="report", report_format="Study Guide", confirm=True)
```

Poll `studio_status(notebook_id)` every 30 seconds between each generation. Download all artifacts:

```
download_artifact(notebook_id, artifact_type="audio", output_path="<absolute_path>/outputs/deep-learn/<subject>-<date>/expert-debate.mp3")
download_artifact(notebook_id, artifact_type="flashcards", output_path="<absolute_path>/outputs/deep-learn/<subject>-<date>/mental-model-flashcards.pdf")
download_artifact(notebook_id, artifact_type="quiz", output_path="<absolute_path>/outputs/deep-learn/<subject>-<date>/deep-understanding-quiz.pdf")
download_artifact(notebook_id, artifact_type="mind_map", output_path="<absolute_path>/outputs/deep-learn/<subject>-<date>/landscape-mind-map.pdf")
download_artifact(notebook_id, artifact_type="report", output_path="<absolute_path>/outputs/deep-learn/<subject>-<date>/study-guide.pdf")
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--lang en` | Generate English content only | Both EN + KO |
| `--lang ko` | Generate Korean content only | Both EN + KO |
| `--rounds N` | Number of quiz rounds | 3 |
| `--questions N` | Questions per quiz round | 5 |
| `--skip-artifacts` | Skip studio artifact generation | Artifacts enabled |
| `--artifacts "audio,quiz"` | Generate only specified artifact types | All 5 artifacts |
| `--sources-only` | Stop after source ingestion (Phase 2) | Full pipeline |
| `--skip-research` | Skip web research enrichment | Research enabled |
| `--share "email1,email2"` | Share notebook with collaborators | No sharing |

## Output Convention

Files are saved to `outputs/deep-learn/`:

```
outputs/deep-learn/
  transformer-architectures-2026-03-08/
    intellectual-landscape.md
    proficiency.md
    expert-debate.mp3
    mental-model-flashcards.pdf
    deep-understanding-quiz.pdf
    landscape-mind-map.pdf
    study-guide.pdf
```

## Examples

```
/nlm-deep-learn "Transformer Architectures in NLP" --sources ~/papers/attention-is-all-you-need.pdf ~/papers/bert.pdf ~/papers/gpt-3.pdf --urls "https://jalammar.github.io/illustrated-transformer/" --rounds 4 --questions 8
```

This will:
1. Collect subject (Transformer Architectures), sources (3 papers + 1 URL)
2. Create NotebookLM notebook, upload all 4 sources, optionally run web research
3. Extract 5 core mental models (attention mechanism, positional encoding, self-supervision, scaling laws, transfer learning)
4. Map intellectual landscape: debates (scaling vs. efficiency, autoregressive vs. bidirectional, emergent abilities), consensus (attention works, pre-training matters), open questions (reasoning capability, data efficiency)
5. Run 4 rounds of 8 deep-understanding questions with explanations for wrong answers
6. Generate gap analysis targeting weak concepts
7. Create expert debate podcast, flashcards, quiz, mind map, and study guide
8. Download all artifacts to `outputs/deep-learn/transformer-architectures-2026-03-08/`

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Mental models too generic | Upload more specialized sources (papers > textbooks for depth) |
| Quiz questions test recall not understanding | Strengthen the question rules — ensure "why" and "how" framing |
| Debate podcast one-sided | Ensure disagreement query returned genuine controversies |
| Sources stuck processing | Use `wait=True, wait_timeout=300` on source_add |
| Too many quiz rounds | Reduce with `--rounds 2` or choose "Generate study artifacts" early |
| Proficiency file not updating | Check write permissions on `outputs/deep-learn/` directory |
| Flashcards too surface-level | Add the intellectual landscape note before generating flashcards |

## Related Skills

- **notebooklm** — notebook/source CRUD and querying
- **notebooklm-research** — web/Drive research and import
- **notebooklm-studio** — ad-hoc studio content generation
- **docs-tutor** — local StudyVault quizzing (without NotebookLM)
- **nlm-discovery-lab** — product discovery pipeline
- **nlm-strategy-hub** — strategic analysis pipeline
