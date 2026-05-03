---
name: evals-skills
description: >-
  Orchestrate LLM eval pipeline tasks: audit existing evals, analyze errors in
  traces, generate synthetic test data, write LLM judge prompts, validate
  evaluators against human labels, evaluate RAG pipelines, and build
  annotation interfaces. Based on hamelsmu/evals-skills (50+ company
  patterns). Use when the user asks for "eval audit", "error analysis", "judge
  prompt", "validate evaluator", "synthetic data", "evaluate RAG", "annotation
  interface", "review traces", "evals", or "LLM evaluation". Do NOT use for
  general code review (use backend-expert or frontend-expert), ML model
  training, unit testing (use qa-test-expert), or non-LLM evaluation tasks.
  Korean triggers: "LLM 평가", "eval 파이프라인".
---

# Evals Skills — LLM Evaluation Pipeline Toolkit

Orchestrate LLM product evaluation tasks using 7 specialized sub-skills from [hamelsmu/evals-skills](https://github.com/hamelsmu/evals-skills).

## Sub-Skill Index

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| eval-audit | Starting point: audit an eval pipeline or bootstrap from scratch | [references/eval-audit.md](references/eval-audit.md) |
| error-analysis | Read traces systematically and categorize failure modes | [references/error-analysis.md](references/error-analysis.md) |
| generate-synthetic-data | Bootstrap eval datasets when real traces are sparse | [references/generate-synthetic-data.md](references/generate-synthetic-data.md) |
| write-judge-prompt | Design binary pass/fail LLM-as-Judge for subjective criteria | [references/write-judge-prompt.md](references/write-judge-prompt.md) |
| validate-evaluator | Calibrate LLM judges against human labels (TPR/TNR) | [references/validate-evaluator.md](references/validate-evaluator.md) |
| evaluate-rag | Evaluate retrieval and generation quality in RAG pipelines | [references/evaluate-rag.md](references/evaluate-rag.md) |
| build-review-interface | Build browser-based annotation interfaces for trace review | [references/build-review-interface.md](references/build-review-interface.md) |

For writing guidelines when creating custom eval skills, see [references/meta-skill.md](references/meta-skill.md).
For learning resources and course links, see [references/questions.md](references/questions.md).

## Workflow

### Step 1: Identify the Right Sub-Skill

Ask the user what they need or infer from context:

| User Intent | Sub-Skill |
|-------------|-----------|
| "Are my evals any good?" / No eval setup exists | eval-audit |
| "What's failing?" / Need to categorize failures | error-analysis |
| "I don't have enough test data" | generate-synthetic-data |
| "I need an LLM judge for X" | write-judge-prompt |
| "Is my judge accurate?" / Need TPR/TNR | validate-evaluator |
| "My RAG pipeline has issues" | evaluate-rag |
| "I need a UI to review traces" | build-review-interface |

### Step 2: Read the Reference and Execute

Read the selected reference file and follow its instructions. Each reference contains the complete procedure: overview, prerequisites, core steps, and anti-patterns.

### Step 3: Chain Sub-Skills as Needed

The recommended progression for a new eval pipeline:

```
error-analysis (or generate-synthetic-data if no traces)
  -> write-judge-prompt (for subjective failure modes)
    -> validate-evaluator (calibrate against human labels)
```

For RAG-specific pipelines, use `evaluate-rag` which covers both retrieval metrics and generation evaluation.

Use `eval-audit` at any point to check overall pipeline health.

## Examples

### Example 1: Audit an existing eval pipeline

User says: "We have some evals but I'm not sure they're catching real issues"

Actions:
1. Read [references/eval-audit.md](references/eval-audit.md)
2. Gather eval artifacts (traces, judge prompts, labeled data)
3. Run 6 diagnostic checks (error analysis, evaluator design, judge validation, human review, labeled data, pipeline hygiene)
4. Produce prioritized findings report with fixes

Result: Prioritized list of eval pipeline problems with concrete next steps.

### Example 2: Build a judge for tone mismatch

User says: "Our support bot sometimes uses the wrong tone. I need an evaluator for that."

Actions:
1. Read [references/write-judge-prompt.md](references/write-judge-prompt.md)
2. Define binary pass/fail criteria for tone matching
3. Write judge prompt with task description, definitions, few-shot examples, structured output
4. Recommend validation with [references/validate-evaluator.md](references/validate-evaluator.md)

Result: Binary pass/fail LLM judge prompt targeting tone mismatch, ready for validation.

### Example 3: Bootstrap evals from scratch

User says: "We have no evals at all. Where do I start?"

Actions:
1. Read [references/eval-audit.md](references/eval-audit.md) -- "No Eval Infrastructure" section
2. If no production traces: read [references/generate-synthetic-data.md](references/generate-synthetic-data.md) to create test inputs
3. Read [references/error-analysis.md](references/error-analysis.md) to categorize failures from traces
4. For each failure mode needing judgment: use write-judge-prompt, then validate-evaluator

Result: End-to-end eval pipeline built from scratch following the recommended progression.

## Error Handling

| Error | Action |
|-------|--------|
| No traces or eval artifacts available | Start with generate-synthetic-data to create test inputs |
| User wants a Likert scale (1-5) evaluator | Recommend binary pass/fail instead; explain via write-judge-prompt anti-patterns |
| Eval pipeline uses ROUGE/BERTScore as primary metric | Flag as a finding; recommend binary evaluators grounded in failure modes |
| No domain expert available for labeling | Minimum viable: one trusted person labels 50-100 traces |
| User wants to skip error analysis | Strongly recommend completing it first -- evaluators built without it measure generic qualities instead of actual failure modes |
