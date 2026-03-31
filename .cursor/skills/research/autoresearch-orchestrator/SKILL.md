---
name: autoresearch-orchestrator
description: >-
  2-stage pipeline connecting AutoResearchClaw research execution with
  post-pipeline distribution. Stage 1 runs the 23-stage research CLI and
  captures the run_id, Stage 2 distributes deliverables to Notion, Slack,
  PPTX, NLM slides, and paper archive. Bridges the gap between the research
  CLI output and multi-channel distribution. Use when the user asks for
  "auto research end-to-end", "autoresearch pipeline", "full autonomous
  research", "자동 연구 파이프라인", "자동 연구 전체", "autoresearch", or wants
  to run AutoResearchClaw and automatically distribute results. Do NOT use
  for research execution only (use auto-research). Do NOT use for
  distribution only (use auto-research-distribute). Do NOT use for manual
  paper review (use paper-review).
metadata:
  version: "1.0.0"
  tags: ["orchestrator", "research", "autoresearch", "harness", "pipeline"]
  pattern: "pipeline (2-stage with run_id handoff)"
  composes:
    - auto-research
    - auto-research-distribute
---

# AutoResearch E2E Orchestrator

2-stage pipeline: run the 23-stage AutoResearchClaw CLI, capture run_id, then distribute deliverables across all channels.

## Usage

```
/autoresearch "topic description"        # Full pipeline: research + distribute
/autoresearch --run-id abc123            # Distribute an existing run
/autoresearch "topic" --skip distribute  # Research only
/autoresearch "topic" --dry-run          # Show plan without executing
```

## Skip Flags

| Flag | Skips | Default |
|------|-------|---------|
| `research` | `auto-research` (Stage 1) | included |
| `distribute` | `auto-research-distribute` (Stage 2) | included |

## Agent Team

| Stage | Agent | Skill | Execution | Output |
|-------|-------|-------|-----------|--------|
| 1 | Research Runner | `auto-research` | Task | `_workspace/autoresearch/00_run-id.txt` + `artifacts/{run_id}/` |
| 2 | Distributor | `auto-research-distribute` | Task | Notion + Slack + PPTX + NLM + archive |

## Workflow

### Pre-flight

1. Parse `$ARGUMENTS` for topic, `--run-id`, `--skip`, `--dry-run`.
2. Validate AutoResearchClaw installation: `ls ~/thaki/AutoResearchClaw/.venv/bin/researchclaw`
   - If not found → abort with message: "AutoResearchClaw not installed at ~/thaki/AutoResearchClaw/"
3. `Shell: mkdir -p _workspace/autoresearch`
4. If `--dry-run`, print the execution plan and stop.
5. If `--run-id` provided → skip Stage 1, write run_id to `_workspace/autoresearch/00_run-id.txt` and go to Stage 2.

### Stage 1: Research Execution

Unless `--skip research` or `--run-id` provided:

Launch 1 Task for `auto-research`:

```
You are an autonomous research executor.

## Skill Reference
Read and follow `.cursor/skills/research/auto-research/SKILL.md`.

## Task
Run the AutoResearchClaw 23-stage pipeline on the topic:
"{topic}"

Execute via CLI:
```bash
cd ~/thaki/AutoResearchClaw
source .venv/bin/activate
researchclaw run --topic "{topic}"
```

## Critical: Capture the run_id
The CLI outputs a run_id (UUID) near the start. Capture it immediately.
Write ONLY the run_id to `_workspace/autoresearch/00_run-id.txt`.

## Monitor
The 23-stage pipeline runs:
Topic Init → Literature (OpenAlex/Semantic Scholar/arXiv) → Hypothesis (debate) →
Experiment → Paper Writing (5K-6.5K words) → Peer Review → LaTeX Export

Monitor progress. If the pipeline stalls at any stage for >10 minutes, report the stage.

## Output
Final deliverables land in `artifacts/{run_id}/deliverables/`.

## Completion
Return the run_id and a summary of the research output (title, abstract, key findings).
```

Wait for Stage 1 to complete. Read the run_id from `_workspace/autoresearch/00_run-id.txt`.

### Stage 2: Distribution

Unless `--skip distribute`:

Launch 1 Task for `auto-research-distribute`:

```
You are a research distribution specialist.

## Skill Reference
Read and follow `.cursor/skills/research/auto-research-distribute/SKILL.md`.

## Context
Run ID: {run_id} (read from `_workspace/autoresearch/00_run-id.txt`)
Deliverables location: `artifacts/{run_id}/deliverables/`

## Task
Run the 6-phase distribution pipeline:
1. Archive — register in paper archive index
2. Notion — create research page with full paper content
3. PPTX — generate presentation from research findings
4. NLM slides — create NotebookLM-compatible slides
5. Slack — post to #deep-research-trending with paper summary
6. Paper archive — update outputs/papers/ index

## Output
Write distribution report to `_workspace/autoresearch/01_distribution.md`.
Include URLs for Notion page and Slack message.

## Completion
Return distribution status for each channel.
```

### Final Output

Summarize the complete pipeline run:

```markdown
# AutoResearch Pipeline Summary

## Topic: {topic}
## Run ID: {run_id}

## Research Output
- Paper: artifacts/{run_id}/deliverables/paper.pdf
- LaTeX: artifacts/{run_id}/deliverables/paper.tex
- Word count: ~{word_count}
- Key findings: {summary}

## Distribution Status
| Channel | Status | URL/Path |
|---------|--------|----------|
| Archive | ✅/❌ | outputs/papers/... |
| Notion | ✅/❌ | {notion_url} |
| PPTX | ✅/❌ | outputs/presentations/... |
| NLM | ✅/❌ | ... |
| Slack | ✅/❌ | #deep-research-trending |

---
Generated by autoresearch-orchestrator v1.0.0
```

## Error Handling

| Failure | Action |
|---------|--------|
| AutoResearchClaw not installed | Abort with installation instructions. |
| Research CLI fails at a stage | Report which stage failed. Offer retry or `--skip research` with manual `--run-id`. |
| run_id not captured | Abort Stage 2. List `artifacts/` directory to find the run manually. |
| Distribution partially fails | Report per-channel status. Retry failed channels individually. |
| Full pipeline hangs | After 30 minutes with no progress, kill the process and report last known stage. |

## Data Flow

```
Input (topic)
    │
    ▼
Stage 1: AutoResearchClaw CLI (23 stages)
    │   researchclaw run --topic "..."
    │   → run_id captured to 00_run-id.txt
    │   → artifacts/{run_id}/deliverables/
    │
    ▼
Stage 2: Distribution (6 channels)
    │   auto-research-distribute
    │   ├─► Paper archive (index.json)
    │   ├─► Notion page
    │   ├─► PPTX presentation
    │   ├─► NLM slides
    │   ├─► Slack #deep-research-trending
    │   └─► outputs/papers/ index
    │
    ▼
Pipeline Summary
```

## Re-distribution

To re-distribute an existing research run without re-running the research:

```
/autoresearch --run-id {existing_run_id}
```

This skips Stage 1 and goes directly to Stage 2 distribution.
