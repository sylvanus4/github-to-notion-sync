## AI Quality

Score and validate AI-generated financial reports across 5 quality dimensions before publishing.

### Usage

```
/ai-quality                               # Evaluate today's report
/ai-quality <date>                        # Evaluate report for a specific date
/ai-quality compare <date1> <date2>       # Compare quality between two dates
/ai-quality gate                          # Run quality gate before Slack posting
```

### Workflow

1. **Locate artifacts** — Find analysis JSON and report .docx for the target date
2. **Gather ground truth** — Get DB prices and raw signal data
3. **Score 5 dimensions** — Accuracy (30%), Consistency (20%), Coverage (20%), Actionability (20%), Tone (10%)
4. **Detect hallucinations** — Flag claims not traceable to data sources
5. **Apply gate decision** — PASS (8.0+), REVIEW (6.0-7.9), or FAIL (below 6.0)

### Execution

Read and follow the `ai-quality-evaluator` skill (`.cursor/skills/ai-quality-evaluator/SKILL.md`) for scoring rubrics, hallucination detection methods, and gate decision logic.

### Examples

Evaluate today's report:
```
/ai-quality
```

Pre-publish quality gate:
```
/ai-quality gate
```

Compare quality trend:
```
/ai-quality compare 2026-03-06 2026-03-07
```
