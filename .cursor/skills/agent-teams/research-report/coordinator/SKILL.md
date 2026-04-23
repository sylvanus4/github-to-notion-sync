---
name: research-report-coordinator
description: >
  Hub agent for the Research and Report multi-agent team. Decomposes research goals,
  dispatches 4 expert agents (Research, Analysis, Writing, Reviewer) via Task tool
  with explicit accumulated context, enforces quality gates, and manages review loops.
  Use when the user asks to "research and report", "deep research with report",
  "연구 보고서 생성", "리서치 리포트", "research-report team", or wants a comprehensive
  research-backed report produced by a coordinated agent team.
  Do NOT use for single-perspective analysis (use role-* skills).
  Do NOT use for daily stock reports (use today pipeline).
  Do NOT use for paper review (use paper-review).
metadata:
  tags: [orchestration, research, multi-agent]
  compute: local
---

# Research and Report Team — Coordinator

## Role

Hub agent that orchestrates a 4-expert research team through a Pipeline-with-Review-Loop pattern.
Responsible for goal decomposition, sequential expert dispatch with accumulated context,
quality gate enforcement, and conditional re-routing on review failure.

## Orchestration Flow

### Step 1 — Parse & Decompose

Extract from user input:
- **Topic** (required): The research subject
- **Scope** (optional): Boundaries, time range, geography
- **Depth** (optional): "quick" (1-page), "standard" (3-5 pages), "deep" (10+ pages). Default: standard
- **Output format** (optional): markdown, docx, both. Default: markdown
- **Language** (optional): Korean (default), English

### Step 2 — Initialize Workspace

```bash
mkdir -p _workspace/research-report
```

Write `_workspace/research-report/goal.md`:
```markdown
# Research Goal
- Topic: {extracted topic}
- Scope: {extracted scope}
- Depth: {depth level}
- Output: {format}
- Language: {language}
```

Write `_workspace/research-report/context.json`:
```json
{
  "goal_set": true,
  "research_complete": false,
  "analysis_complete": false,
  "writing_complete": false,
  "review_complete": false,
  "review_iteration": 0,
  "review_scores": [],
  "errors": []
}
```

### Step 3 — Dispatch Research Expert

Launch a Task subagent (subagent_type: generalPurpose):

**Prompt template:**
> Read the skill at `.cursor/skills/agent-teams/research-report/research-expert/SKILL.md` and follow its instructions exactly.
>
> **Goal:** (paste full content of goal.md)
>
> **Input file:** `_workspace/research-report/goal.md`
> **Output file:** `_workspace/research-report/research-output.md`
>
> Execute the research phase. Write your output to the specified file.

After completion:
- Read `_workspace/research-report/research-output.md`
- Update context.json: `research_complete: true`
- If output is empty or missing, log error and retry once with broadened scope

### Step 4 — Dispatch Analysis Expert

Launch a Task subagent:

**Prompt template:**
> Read the skill at `.cursor/skills/agent-teams/research-report/analysis-expert/SKILL.md` and follow its instructions exactly.
>
> **Goal:** (paste goal.md content)
> **Research Data:** (paste research-output.md content OR reference file path)
>
> **Input files:** `_workspace/research-report/goal.md`, `_workspace/research-report/research-output.md`
> **Output file:** `_workspace/research-report/analysis-output.md`

After completion:
- Read analysis-output.md, update context.json: `analysis_complete: true`

### Step 5 — Dispatch Writing Expert

Launch a Task subagent:

**Prompt template:**
> Read the skill at `.cursor/skills/agent-teams/research-report/writing-expert/SKILL.md` and follow its instructions exactly.
>
> **Goal:** (paste goal.md)
> **Research Data:** (paste or reference research-output.md)
> **Analysis:** (paste or reference analysis-output.md)
> **Revision feedback (if any):** (paste review-feedback.json if iteration > 0)
>
> **Input files:** All files in `_workspace/research-report/`
> **Output file:** `_workspace/research-report/draft-report.md`

After completion:
- Read draft-report.md, update context.json: `writing_complete: true`

### Step 6 — Dispatch Reviewer Expert

Launch a Task subagent:

**Prompt template:**
> Read the skill at `.cursor/skills/agent-teams/research-report/reviewer-expert/SKILL.md` and follow its instructions exactly.
>
> **Goal:** (paste goal.md)
> **Research Data:** (reference research-output.md)
> **Analysis:** (reference analysis-output.md)
> **Draft Report:** (paste draft-report.md content)
>
> **Input files:** All files in `_workspace/research-report/`
> **Output file:** `_workspace/research-report/review-feedback.json`

After completion:
- Read review-feedback.json, update context.json: `review_complete: true`

### Step 7 — Quality Gate

Read `review-feedback.json` and evaluate:

| Condition | Action |
|-----------|--------|
| `overall_score >= 80` | Proceed to Final Assembly |
| `overall_score < 80` AND `review_iteration < 2` | Increment iteration counter, append reviewer feedback to context, go back to Step 5 |
| `review_iteration >= 2` | Accept best draft, proceed to Final Assembly with quality warning |

### Step 8 — Final Assembly

1. Read all workspace files
2. Combine into `_workspace/research-report/final-report.md`
3. If docx requested, invoke `anthropic-docx` skill to generate .docx
4. Present the final report to the user
5. Clean up: optionally archive workspace to `outputs/research-report/{date}/`

## Context Passing Protocol

Every Task subagent prompt MUST include:
1. The **skill file path** to read for instructions
2. The **full accumulated context** — either inline (for small outputs) or as file paths (for large outputs)
3. **Input file paths** the expert should read
4. **Output file path** the expert must write to

Never assume a subagent has access to prior conversation context. Always pass everything explicitly.

## Quality Gate Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Accuracy | 25% | Facts verified against sources |
| Depth | 20% | Sufficient analysis for the requested depth level |
| Structure | 15% | Logical organization, clear sections |
| Actionability | 15% | Concrete recommendations, not vague advice |
| Citations | 15% | All claims backed by source references |
| Clarity | 10% | Readable prose, no jargon without definition |

Overall score = weighted average. Threshold: 80/100.

## Error Protocol

- **Empty output**: Retry once with broadened or clarified prompt
- **Repeated failure**: Skip agent, log gap in context.json, proceed with available data
- **Timeout**: Kill after 5 minutes, proceed with partial results
