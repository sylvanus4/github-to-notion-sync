---
name: executive-briefing
description: >-
  Synthesize multiple role-perspective analysis documents into a unified CEO
  executive briefing report in Korean. Identifies cross-role consensus,
  conflicting perspectives, prioritized action items, and a risk matrix.
  Outputs structured markdown and a .docx executive summary. Composes
  agency-executive-summary-generator, anthropic-docx, and visual-explainer.
  Use when the role-dispatcher invokes this skill after collecting role
  analyses, or when the user asks to "create executive briefing", "CEO 종합
  보고서", "경영진 브리핑 생성", "synthesize role analyses", "cross-role summary". Do NOT
  use for single-role analysis (use the specific role-{name} skill), daily
  morning briefing (use morning-ship), or investor presentation (use
  presentation-strategist). Korean triggers: "CEO 종합 보고서", "경영진 브리핑", "직무별
  종합".
---

# Executive Briefing Generator

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

Synthesizes analysis documents from multiple role-perspective skills into a comprehensive
CEO executive briefing with cross-functional insights, consensus mapping, and prioritized actions.

## Input Requirements

This skill expects a collection of role-perspective analysis documents, each following this structure:
- Role name and relevance score
- Executive summary bullets
- Detailed domain-specific analysis
- Risks & concerns
- Recommendations

Documents are typically located in `outputs/role-analysis/{topic-slug}/` or passed as context.

## Synthesis Pipeline

Execute sequentially:

### Phase 1: Content Aggregation
- Collect all role-perspective documents
- Record participation: which roles analyzed (relevance >= 5) vs skipped
- Extract key findings, risks, and recommendations from each

### Phase 2: Cross-Role Analysis (via `agency-executive-summary-generator`)
Apply McKinsey SCQA framework:
- **Situation**: Topic context and scope
- **Complication**: Key tensions revealed by cross-role analysis
- **Question**: What decision must the CEO make?
- **Answer**: Synthesized recommendation with confidence level

Identify:
- **Consensus**: Points where 3+ roles agree
- **Conflicts**: Points where roles disagree (and why)
- **Blind spots**: Important dimensions no role covered

### Phase 3: Risk Matrix
Aggregate risks from all roles into a unified matrix:
- Deduplicate similar risks
- Assign composite severity (impact x probability)
- Map mitigation owners by role

### Phase 4: Action Item Prioritization
Merge all role recommendations:
- Deduplicate and group by theme
- Prioritize by: urgency (time-sensitive), impact (business value), dependency (blocking others)
- Assign owner role and timeline

### Phase 5: Document Generation (via `anthropic-docx`)
Generate a professional .docx executive briefing with:
- Table of contents
- Executive summary (1 page)
- Cross-role analysis (2-3 pages)
- Risk matrix table
- Action items with owners
- Appendix: individual role summaries

### Phase 6: Visual Summary (via `visual-explainer`)
Create a self-contained HTML dashboard showing:
- Role participation heatmap
- Risk matrix scatter plot
- Action item timeline

## Output format

Produce the full briefing in Korean. Include: title with topic and date; dashboard summary (topic, participating roles count, overall impact level, one-line decision); per-role summary table; SCQA (Situation, Complication, Question, Answer); consensus list with evidence; conflicts table; prioritized action table; risk matrix; blind spots; appendix with per-role digests. Match tone to executive readers.

## Slack delivery format

Post to the Slack channel the user specifies (do not hard-code channel IDs). Use Korean copy per output rule.

**Main message**: topic line, participation summary, impact level, headline decision, top agreements, top actions with owners/deadlines.

**Thread**: one short message per participating role with relevance score and 3–5 bullets.

**Attachment**: executive briefing `.docx` when generated.

## Error Handling

- If fewer than 2 role analyses are available, warn that cross-role synthesis may be shallow
- If a role document is malformed or missing sections, extract what is available and note gaps
- If the .docx generation fails, produce markdown-only output and log the failure
- If Slack posting fails, save all outputs locally and notify the user with file paths
## Example

**Input**: 8 role-perspective documents about "New GPU inference service launch"

**Output highlights**:
- Participation: 8/10 roles relevant (HR 5/10, Finance 8/10 — included)
- Consensus: All 8 roles agree on strategic importance and timing
- Conflict: CTO wants phased rollout (3 sprints) vs Sales wants fast launch (1 sprint)
- Top Action: Approve $200K GPU capex (Finance) + start hiring 2 ML engineers (HR)
- Risk: Competitive response from hyperscalers within 3 months (CSO + Sales)


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
