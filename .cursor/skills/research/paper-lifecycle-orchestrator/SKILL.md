---
name: paper-lifecycle-orchestrator
description: >-
  End-to-end research paper lifecycle: auto-classify or accept paper URL,
  scout related papers, route to full review or slides-only based on depth
  flag, archive to index, and distribute via Slack and Notion. Uses expert
  pool routing to select the appropriate review pipeline. Use when the user
  asks for "paper lifecycle", "full paper pipeline", "논문 라이프사이클",
  "논문 전체 파이프라인", "paper end-to-end", or wants automated paper discovery
  through distribution. Do NOT use for paper review only (use paper-review).
  Do NOT use for slides generation only (use nlm-arxiv-slides). Do NOT use
  for related paper scouting only (use related-papers-scout).
metadata:
  version: "1.0.0"
  tags: ["orchestrator", "research", "paper", "harness", "pipeline-expert-pool"]
  pattern: "pipeline + expert pool (routing)"
  composes:
    - paper-auto-classifier
    - related-papers-scout
    - paper-review
    - nlm-arxiv-slides
    - paper-archive
---

# Research Paper Lifecycle Orchestrator

Pipeline from discovery to distribution: classify → scout → route (review or slides) → archive → distribute.

## Usage

```
/paper-lifecycle https://arxiv.org/abs/2403.xxxxx    # Full lifecycle for a paper
/paper-lifecycle auto                                  # Auto-classify and process
/paper-lifecycle https://arxiv.org/abs/... --depth slides-only  # Slides only
/paper-lifecycle https://arxiv.org/abs/... --depth scout-only   # Scout only
/paper-lifecycle --dry-run                             # Show plan without executing
```

## Depth Modes

| Mode | Phases | Description |
|------|--------|-------------|
| `full` (default) | 1→2→3→4→5 | Complete lifecycle with full paper review |
| `slides-only` | 1→2→3(slides)→4→5 | Skip full review, generate slides directly |
| `scout-only` | 1→2 | Discovery and scouting only, no review/archive |

## Agent Team

| Phase | Agent | Skill | Execution | Output |
|-------|-------|-------|-----------|--------|
| 1 | Classifier | `paper-auto-classifier` | Task | `_workspace/paper-lifecycle/01_classified.md` |
| 2 | Scout | `related-papers-scout` | Task | `_workspace/paper-lifecycle/02_scout.md` |
| 3a | Full Reviewer | `paper-review` | Task | `_workspace/paper-lifecycle/03_review.md` |
| 3b | Slides Generator | `nlm-arxiv-slides` | Task | `_workspace/paper-lifecycle/03_slides.pdf` |
| 4 | Archivist | `paper-archive` | inline | `outputs/papers/index.json` |
| 5 | Distributor | inline | inline | Slack + Notion |

## Workflow

### Pre-flight

1. Parse `$ARGUMENTS` for input (arXiv URL, paper ID, or `auto`), `--depth`, `--dry-run`.
2. `Shell: mkdir -p _workspace/paper-lifecycle`
3. If `--dry-run`, print the execution plan and stop.

### Phase 1: Discovery

If input is `auto`:

Launch 1 Task for `paper-auto-classifier`:

```
You are a research paper classifier.

## Skill Reference
Read and follow `.cursor/skills/research/paper-auto-classifier/SKILL.md`.

## Task
Poll recent arXiv submissions and classify papers by relevance to the project's
research areas (AI/ML, GPU computing, agent systems, financial AI).

## Output
Write classified papers to `_workspace/paper-lifecycle/01_classified.md`.
Format: ranked list with arXiv ID, title, classification score, and abstract summary.
Select the top-scoring paper for the pipeline.

## Completion
Return the top paper's arXiv ID and title.
```

If input is a paper URL/ID → skip Phase 1, write the URL directly to `_workspace/paper-lifecycle/01_classified.md`.

### Phase 2: Scout Related Papers

Launch 1 Task for `related-papers-scout`:

```
You are a research scout.

## Skill Reference
Read and follow `.cursor/skills/research/related-papers-scout/SKILL.md`.

## Context
Read the target paper from `_workspace/paper-lifecycle/01_classified.md`.

## Task
Find 5 related hot papers from top institutions. Apply the 9-month recency filter.

## Output
Write findings to `_workspace/paper-lifecycle/02_scout.md`.

## Completion
Return count of related papers found with brief titles.
```

If `--depth scout-only`, stop here and present the scout results.

### Phase 3: Expert Pool Routing

Route to the appropriate review pipeline based on `--depth` flag and classifier relevance score.

**Route A — Full Review** (default, `--depth full`):

Launch 1 Task for `paper-review` (treated as opaque — its 9 internal phases stay internal):

```
You are a comprehensive paper reviewer.

## Skill Reference
Read and follow `.cursor/skills/research/paper-review/SKILL.md`.

## Context
Target paper: {arXiv URL or ID from Phase 1}
Related papers context: read `_workspace/paper-lifecycle/02_scout.md`.

## Task
Run the full 9-phase paper review pipeline:
Ingest → Review → PM Analysis → NLM Slides → Notion → Slack
(DOCX and PPTX are off by default; the orchestrator does not enable them unless
the user explicitly passes --with-docx or --with-pptx.)

## Output
Write review summary to `_workspace/paper-lifecycle/03_review.md`.

## Completion
Return the review verdict and key findings.
```

**Route B — Slides Only** (`--depth slides-only`):

Launch 1 Task for `nlm-arxiv-slides` (treated as opaque — its 6-skill chain stays internal):

```
You are a slide deck generator.

## Skill Reference
Read and follow `.cursor/skills/nlm/nlm-arxiv-slides/SKILL.md`.

## Context
Target paper: {arXiv URL or ID from Phase 1}

## Task
Generate presentation slides from the paper.

## Output
Write slide summary to `_workspace/paper-lifecycle/03_slides.md`.
PDF output follows the nlm-arxiv-slides skill's standard output path.

## Completion
Return slide count and key topics covered.
```

### Phase 4: Archive

Register the paper in the archive index (inline logic, not a separate Task):

1. Read the paper metadata from Phase 1 output.
2. Read review/slides output from Phase 3.
3. Update `outputs/papers/index.json` with:
   - arXiv ID, title, authors, date
   - Review status (full/slides/scout-only)
   - File paths to generated artifacts
   - Related papers from Phase 2

### Phase 5: Distribution

Distribute to standard channels (inline logic):

1. **Slack `#deep-research-trending`** (`C0AN34G4QHK`):
   - Post paper summary with review verdict
   - Thread reply with key findings and related papers
   - Upload NLM slides PDF directly (not a link)

2. **Notion** (parent page `3209eddc34e6801b8921f55d85153730`):
   - Create sub-page with paper metadata, review summary, and related papers

## Error Handling

| Failure | Action |
|---------|--------|
| Classifier finds no relevant papers | Report "No relevant papers found" and stop. |
| Scout fails | Proceed without related papers context. Note in report. |
| Full review fails | Retry once. If still fails, fall back to slides-only mode. |
| Slides generation fails | Retry once. If still fails, produce text summary only. |
| Archive update fails | Log warning. Non-critical. |
| Slack/Notion distribution fails | Retry once. Log warning if still fails. |

## Data Flow

```
Input (arXiv URL | paper ID | "auto")
    │
    ▼
Phase 1: Discovery
    │   paper-auto-classifier (if "auto")
    │   or direct URL passthrough
    │   → 01_classified.md
    │
    ▼
Phase 2: Scout
    │   related-papers-scout
    │   → 02_scout.md
    │   [stop here if --depth scout-only]
    │
    ▼
Phase 3: Expert Pool Routing
    │   ┌─ --depth full → paper-review (9 phases, opaque)
    │   │                  → 03_review.md (+ DOCX/PPTX only if --with-docx/--with-pptx)
    │   │
    │   └─ --depth slides-only → nlm-arxiv-slides (6 skills, opaque)
    │                             → 03_slides.md + PDF
    │
    ▼
Phase 4: Archive
    │   → outputs/papers/index.json
    │
    ▼
Phase 5: Distribution
    ├─► Slack #deep-research-trending (+ NLM slides PDF)
    └─► Notion paper parent page
```
