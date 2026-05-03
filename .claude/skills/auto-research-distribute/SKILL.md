---
name: auto-research-distribute
description: >-
  Distribute AutoResearchClaw pipeline outputs (paper, LaTeX, experiments) to
  Notion, Slack, NotebookLM, PPTX, and paper-archive. Use when the user asks
  to "distribute research results", "post research to Slack", "upload paper to
  Notion", "auto-research-distribute", "연구 결과 배포", "논문 배포", "연구 Notion 업로드",
  "연구 결과 공유", "논문 슬랙 공유", or after completing an auto-research pipeline run.
  Do NOT use for running the research pipeline itself (use auto-research),
  reviewing existing papers (use paper-review), or publishing arbitrary
  markdown to Notion (use md-to-notion).
disable-model-invocation: true
---

# AutoResearchClaw — Post-Pipeline Distribution

Take deliverables from a completed AutoResearchClaw pipeline run and distribute
them across the project ecosystem: paper-archive, Notion, Slack, NotebookLM,
and PPTX.

## Prerequisites

- A completed AutoResearchClaw pipeline run with deliverables directory
- Slack MCP configured (for `#deep-research-trending` channel posting)
- Notion MCP configured (for research page creation)
- NotebookLM MCP configured (optional, for study artifacts)

## Reference Files

- `references/distribution-channels.md` — Channel configs and templates

## Pipeline Overview

```
Phase 1: Locate Deliverables    → Find and validate artifact files
Phase 2: Paper Archive           → Register in paper-archive index
Phase 3: Notion Upload           → Create structured Notion sub-pages
Phase 4: PPTX Generation        → Generate executive summary slides
Phase 5: NotebookLM Upload      → Create notebook with study artifacts
Phase 6: Slack Notification      → Post summary thread to #deep-research-trending
```

## Execution

### Phase 1: Locate Deliverables

1. Find the deliverables directory. It is either:
   - Provided by user: `--artifacts-dir <path>`
   - Auto-detected: `~/thaki/AutoResearchClaw/artifacts/rc-*/deliverables/`

2. Verify required files exist:

```bash
ls <artifacts-dir>/deliverables/
# Expected: paper_final.md, paper.tex, references.bib, manifest.json
```

3. Read `manifest.json` for metadata:

```bash
cat <artifacts-dir>/deliverables/manifest.json
```

4. Read `pipeline_summary.json` for run context:

```bash
cat <artifacts-dir>/pipeline_summary.json
```

### Phase 2: Paper Archive

Register the paper in the project's paper-archive index.

1. Read the `paper-archive` skill
2. Extract metadata from `paper_final.md`:
   - Title (first H1)
   - Abstract
   - Keywords/domains
   - Run ID, date, conference target
3. Create archive entry with `paper_type: "generated"` to distinguish from reviewed papers

### Phase 3: Notion Upload

Create structured Notion pages using `md-to-notion`.

1. Read the `md-to-notion` skill
2. Upload `paper_final.md` as a Notion sub-page under the research parent page
   (parent: `3209eddc34e6801b8921f55d85153730` — same as paper-review)
3. Add metadata properties:
   - Run ID
   - Conference target
   - Experiment mode
   - Quality score (from `pipeline_summary.json`)
   - Citation verification score

**Skip with**: `--skip-notion`

### Phase 4: PPTX Generation

Generate an executive summary presentation.

1. Read the `anthropic-pptx` skill
2. Generate a 10-15 slide deck from `paper_final.md` covering:
   - Title slide
   - Research problem & motivation
   - Literature gap
   - Methodology
   - Key results (with charts from `deliverables/charts/`)
   - Conclusion & future work
3. Save as `<artifacts-dir>/deliverables/presentation.pptx`

**Skip with**: `--skip-pptx`

### Phase 5: NotebookLM Upload

Upload sources and generate study artifacts.

1. Read the `notebooklm` skill
2. Create a new notebook titled: `[AutoResearch] <paper-title>`
3. Upload `paper_final.md` as text source
4. Read the `notebooklm-studio` skill
5. Generate study artifacts (all non-audio artifacts in Korean):
   - Slide deck (for quick review, `language="ko"`)
   - Audio podcast (for commute review)

**Skip with**: `--skip-nlm`

### Phase 6: Slack Notification

Post a structured 3-message thread to `#deep-research-trending` (`C0AN34G4QHK`).

**Message 1 (main)**: Summary announcement

```
🔬 *AutoResearch Complete: <paper-title>*
📊 Run: `<run-id>` | Mode: `<experiment-mode>` | Conference: `<target>`
✅ Quality: <score>/10 | Citations: <verified>/<total> verified
```

**Message 2 (thread)**: Key findings (3-5 bullet points from abstract/conclusion)

**Message 3 (thread)**: Links and deliverables

```
📎 Deliverables:
• Notion: <notion-url>
• PPTX: <file-path>
• LaTeX: <file-path>
• NotebookLM: <notebook-url>
```

**Skip with**: `--skip-slack`

**Override channel**: `--channel "#channel-name"`

## Options

- `--artifacts-dir "path"` — Path to run artifacts directory (required if not auto-detected)
- `--skip-notion` — Skip Notion upload
- `--skip-slack` — Skip Slack notification
- `--skip-nlm` — Skip NotebookLM upload
- `--skip-pptx` — Skip PPTX generation
- `--channel "#channel"` — Override Slack channel (default: `#deep-research-trending`)

## Output Convention

- PPTX: `<artifacts-dir>/deliverables/presentation.pptx`
- Notion pages: under parent `3209eddc34e6801b8921f55d85153730`
- Slack: `#deep-research-trending` channel (`C0AN34G4QHK`)
- Paper archive: `outputs/papers/` index

## Skills Composed

| Skill | Phase | Role |
|---|---|---|
| `paper-archive` | 2 | Register paper in archive index |
| `md-to-notion` | 3 | Upload markdown to Notion sub-pages |
| `anthropic-pptx` | 4 | Generate executive summary slides |
| `notebooklm` | 5 | Create and manage NotebookLM notebook |
| `notebooklm-studio` | 5 | Generate study artifacts (slides, podcast) |
| Slack MCP | 6 | Post summary to Slack channel |

## Examples

### Example 1: Distribute latest run to all channels

User says: "auto-research-distribute"

Actions:
1. Find latest run: `ls ~/thaki/AutoResearchClaw/artifacts/rc-*/deliverables/ | tail -1`
2. Verify files: `paper_final.md`, `paper.tex`, `manifest.json` all present
3. Register in paper-archive with `paper_type: "generated"`
4. Upload to Notion under research parent page
5. Generate 12-slide PPTX summary
6. Create NotebookLM notebook + slide deck + podcast
7. Post 3-message Slack thread to `#deep-research-trending`

Result: Research outputs distributed to 5 channels with links in Slack thread.

### Example 2: Slack-only notification

User says: "Post research results to Slack only"

Actions:
1. Locate deliverables, read `manifest.json`
2. Skip Phases 2-5 (archive, Notion, PPTX, NLM)
3. Post summary thread to `#deep-research-trending`

## Troubleshooting

### Missing Deliverables

If `deliverables/` directory doesn't exist, check if the pipeline completed:

```bash
cat <run-dir>/pipeline_summary.json | python3 -m json.tool
```

Stages must complete through Stage 22 (EXPORT_PUBLISH) for deliverables to be packaged.

### Notion Upload Fails

- Check Notion MCP is connected
- Verify parent page ID is accessible
- Large papers (>15KB) are automatically split into linked sub-pages

### NotebookLM Quota

- NotebookLM has rate limits on notebook and source creation
- If creation fails, retry after a few minutes
- Check auth: `nlm login` if authentication errors occur
