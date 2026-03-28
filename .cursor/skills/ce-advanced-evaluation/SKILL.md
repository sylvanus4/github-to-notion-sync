---
name: ce-advanced-evaluation
description: >-
  Production-grade techniques for LLM-as-judge evaluation — direct scoring,
  pairwise comparison, bias mitigation (position, length, self-enhancement),
  metric selection frameworks, and automated rubric generation. Use when the
  user asks to "implement LLM-as-judge", "compare model outputs", "mitigate
  evaluation bias", "create scoring rubrics", or mentions direct scoring,
  pairwise comparison, position bias, evaluation pipelines, or automated
  quality assessment. Do NOT use for general agent evaluation strategy (use
  ce-evaluation). Do NOT use for LLM prompt evals and judge prompts (use
  evals-skills). Do NOT use for AI report quality scoring (use
  ai-quality-evaluator). Do NOT use for agent session evaluation metrics
  (use intent-alignment-tracker or ecc-eval-harness).
  Korean triggers: "LLM 판사", "평가 바이어스", "직접 스코어링", "페어와이즈 비교",
  "루브릭 생성".
metadata:
  upstream: "muratcankoylan/Agent-Skills-for-Context-Engineering/skills/advanced-evaluation"
  author: "Agent Skills for Context Engineering Contributors"
  version: "2.0.0"
  license: MIT
  category: knowledge
---

# Advanced Evaluation Techniques

Advanced evaluation uses LLMs as evaluators to assess LLM outputs at scale. The core challenge is that LLM judges have systematic biases that must be understood and mitigated to produce reliable quality signals.

## Core Concepts

### Direct Scoring

The judge assigns a numerical score to a single output against a rubric. Best for: absolute quality measurement, threshold-based gating, tracking quality over time.

**Key design decisions:**
- Scale: 1-5 (more reliable) vs. 1-10 (more granular, less consistent)
- Anchoring: Provide specific examples for each score level
- Chain-of-thought: Require the judge to explain before scoring (improves consistency by 15-20%)

### Pairwise Comparison

The judge compares two outputs and selects the better one. Best for: model comparison, A/B testing, ranking alternatives.

**Why pairwise often outperforms direct scoring:**
- Relative judgments are more consistent than absolute ones
- Eliminates scale interpretation inconsistency
- Higher inter-rater agreement (human-LLM and LLM-LLM)

### The Bias Landscape

| Bias | Effect | Mitigation |
|------|--------|-----------|
| Position bias | Prefers first (or last) option in comparisons | Randomize order; run both orderings |
| Length bias | Prefers longer responses | Normalize by length; penalize padding |
| Self-enhancement bias | LLMs rate their own outputs higher | Use different model families for generation and judging |
| Verbosity bias | Confuses detail with quality | Specify in rubric that conciseness matters |
| Authority bias | Prefers confident-sounding but wrong outputs | Require evidence citation in rubric |

### Metric Selection Framework

Match the evaluation metric to the task type:

| Task Type | Primary Metric | Secondary Metric |
|-----------|---------------|-----------------|
| Classification | Accuracy, F1 | Confidence calibration |
| Generation | Human preference, rubric score | Fluency, coherence |
| Extraction | Precision, recall | Exact match on key fields |
| Reasoning | Correctness of final answer | Step validity |
| Code | Test pass rate | Style, efficiency |

### Rubric Generation

Auto-generate evaluation rubrics:
1. Collect 20-30 examples of good and bad outputs
2. Ask an LLM to identify distinguishing dimensions
3. Define 3-5 levels per dimension with concrete examples
4. Validate rubric with human evaluation on a held-out set
5. Iterate until human-LLM agreement exceeds 80%

## Examples

### Example 1: Detecting position bias in LLM judges
You notice your pairwise comparison judge systematically prefers whichever response appears first. This skill teaches you to randomize presentation order, run both orderings, and discard results where the judge contradicts itself across orderings.

### Example 2: Calibrating rubric anchors
Your 1-5 scoring rubric produces mostly 3s and 4s, losing discriminative power. This skill shows how to collect 20-30 real examples, define concrete anchor descriptions for each score level, and validate until human-LLM agreement exceeds 80%.

## Troubleshooting

1. **Single-judge unreliability**: Use multi-judge panels (3+ judges) for high-stakes decisions.
2. **Rubric drift**: Re-validate rubrics monthly as task distributions change.
3. **Bias compounding**: Multiple biases interact — position bias + length bias can strongly favor verbose first options.
4. **Cost at scale**: Judge calls are LLM calls too. Budget 10-20% of generation cost for evaluation.
5. **Treating LLM scores as ground truth**: LLM judges are noisy estimators, not oracles. Always maintain a human-eval baseline.

## References

- [Bias Mitigation Reference](./references/bias-mitigation.md)
- [Evaluation Pipeline Reference](./references/evaluation-pipeline.md)
- [Implementation Patterns Reference](./references/implementation-patterns.md)
- [Metrics Guide Reference](./references/metrics-guide.md)
- Related CE skills: ce-evaluation, ce-context-fundamentals
- Research: LMSYS Chatbot Arena methodology, position bias studies, Anthropic eval practices
