---
description: "Generate a C-suite executive summary with situation, key findings, recommendations, and next steps"
argument-hint: "<report, analysis, or topic to summarize>"
---

# Executive Summary

Produce a business-grade executive summary using the SCQA framework (Situation, Complication, Question, Answer). Designed for time-constrained decision-makers.

## Usage

```
/exec-summary Q2 revenue dropped 15% despite increased ad spend
/exec-summary [paste full report here]
/exec-summary --with-metrics Evaluate our Kubernetes migration progress
/exec-summary outputs/papers/2604.03128/review-2604.03128-2026-04-07.md
/exec-summary 이번 분기 매출 하락 원인과 대응 방안을 경영진 보고서로 작성해줘
```

## Your Task

User input: $ARGUMENTS

### Mode Selection

Parse `$ARGUMENTS` for flags:

- **No flags** — Standard SCQA executive summary (default)
- `--with-metrics` — Include a key metrics table with baseline, current, target
- `--one-page` — Constrain entire output to fit one printed page (~500 words)
- `--with-risks` — Add a risk flags section with severity ratings
- `--board` — Board-presentation style: more formal, include financial implications

### Workflow

1. **Parse input** — Accept topic, pasted content, URL, or file path
2. **Extract core narrative** — What happened, why it matters, what to do
3. **Apply SCQA framework**
   - **Situation** — Stable context everyone agrees on (2-3 sentences)
   - **Complication** — What changed or went wrong (2-3 sentences)
   - **Question** — The strategic question this raises (1 sentence)
   - **Answer** — Recommended course of action (2-3 sentences)
4. **Add key findings** — 3-5 bullet points with supporting data
5. **Add recommendations** — Top 3 actions, each with impact estimate and effort level
6. **Add metrics table** (if `--with-metrics`) — Key numbers with trend indicators (↑↓→)
7. **Add risk flags** (if `--with-risks`) — Top risks with severity (🔴🟡🟢)
8. **Add next steps** — Concrete actions with owners and timelines

### Output Format

```
## Executive Summary: [Title]

### Situation
[Stable context]

### Complication
[What changed]

### Key Question
[Strategic question]

### Recommendation
[Proposed answer]

### Key Findings
1. [Finding with data]
2. [Finding with data]
3. [Finding with data]

### Recommended Actions
| # | Action | Impact | Effort | Owner |
|---|--------|--------|--------|-------|
| 1 | ...    | High   | Medium | TBD   |

### Next Steps
- [ ] [Action] — by [date]
```

### Constraints

- Lead with the conclusion, not the process
- Every finding must include a number or data point
- No jargon without definition
- Total length: max 1 page (~500 words) unless `--board` flag expands it

### Execution

Reference `agency-executive-summary-generator` (`.cursor/skills/agency/agency-executive-summary-generator/SKILL.md`) for McKinsey SCQA and Pyramid Principle patterns. For SCQA structuring, reference `scqa-writing-framework` (`.cursor/skills/standalone/scqa-writing-framework/SKILL.md`).
