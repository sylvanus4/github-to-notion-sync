---
description: "Distribute AutoResearchClaw outputs (paper, LaTeX, experiments) to Notion, Slack, NotebookLM, PPTX, and paper-archive"
---

# Auto Research Distribute — Research Output Distribution

## Skill Reference

Read and follow the skill at `.cursor/skills/auto-research-distribute/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine the **deliverables path** from user input:

- If a path is provided, use it directly
- If `--latest` or no path, find the most recent run under `~/thaki/AutoResearchClaw/artifacts/`
- If `--run-id <id>` is given, resolve `artifacts/<id>/deliverables/`

Determine which channels to distribute to:

- **all** (default): Paper archive + Notion + PPTX + NotebookLM + Slack
- **skip-notion**: Skip Notion upload
- **skip-pptx**: Skip PPTX generation
- **skip-nlm**: Skip NotebookLM upload
- **skip-slack**: Skip Slack notification
- **only-slack**: Post to Slack only
- **only-notion**: Upload to Notion only
- **dry-run**: Locate and inspect deliverables without distributing

### Step 2: Locate Deliverables

1. Read `deliverables/manifest.json` from the resolved path
2. Verify key files exist: `paper_final.md`, `paper.tex`, `pipeline_summary.json`
3. If `deliverables/` is missing, check if the pipeline completed successfully

### Step 3: Distribute

Follow the distribution phases from the skill:

1. **Paper Archive**: Register in `paper-archive` with metadata
2. **Notion**: Create structured sub-pages under research parent page
3. **PPTX**: Generate summary slides via `anthropic-pptx`
4. **NotebookLM**: Upload paper + key experiment results
5. **Slack**: Post structured thread to `#deep-research`

### Step 4: Summary

Report which channels received the outputs and provide direct links (Notion URL, Slack link).

## Constraints

- Read deliverables from the AutoResearchClaw artifacts directory — never from the project workspace
- If a file is missing, skip that channel and report the gap
- Never modify the original deliverables
- Slack thread: main message with paper title + abstract, reply with experiment results + links
