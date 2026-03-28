---
name: ce-evaluation
description: >-
  Evaluation methods for agent systems — outcome-based assessment, multi-dimensional
  rubrics, LLM-as-judge patterns, test set design, context-engineering evaluation,
  and continuous evaluation pipelines. Use when the user asks to "evaluate agent
  performance", "build test framework for agents", "measure agent quality", "create
  evaluation rubrics", or mentions agent evaluation, quality gates, test set design,
  or continuous evaluation for agents. Do NOT use for LLM prompt evaluation and
  judge prompts (use evals-skills). Do NOT use for AI report quality scoring
  (use ai-quality-evaluator). Do NOT use for advanced LLM-as-judge bias techniques
  (use ce-advanced-evaluation). Do NOT use for agent session evaluation (use
  ecc-eval-harness or intent-alignment-tracker).
  Korean triggers: "에이전트 평가", "품질 루브릭", "에이전트 테스트", "평가 파이프라인",
  "에이전트 품질 게이트".
metadata:
  upstream: "muratcankoylan/Agent-Skills-for-Context-Engineering/skills/evaluation"
  author: "Agent Skills for Context Engineering Contributors"
  version: "2.0.0"
  license: MIT
  category: knowledge
---

# Evaluation Methods for Agent Systems

The hardest part of building agents is knowing whether they work. Agent evaluation differs fundamentally from traditional software testing: outcomes are non-deterministic, paths are variable, and "correct" is often subjective. Evaluate outcomes over execution paths.

## Core Concepts

### Evaluate Outcomes, Not Execution Paths

Agents may take different paths to the same correct result. Test the end state, not the specific steps taken:

```python
# Bad: Tests execution path
assert agent.called_tool("search_database")
assert agent.called_tool("format_result")

# Good: Tests outcome
result = agent.run("Find the top 3 customers by revenue")
assert len(result.customers) == 3
assert result.customers[0].revenue > result.customers[1].revenue
```

### Multi-Dimensional Rubrics

Score agent outputs across multiple dimensions rather than a single pass/fail:

| Dimension | Weight | 1 (Poor) | 5 (Excellent) |
|-----------|--------|----------|---------------|
| Correctness | 40% | Factually wrong | Fully accurate |
| Completeness | 25% | Partial answer | Comprehensive |
| Relevance | 20% | Off-topic content | Focused on query |
| Efficiency | 15% | Excessive steps | Minimal tool use |

### LLM-as-Judge

Use a strong LLM to evaluate a weaker agent's output. Provide the judge with: the original query, the agent's output, the ground truth (if available), and a scoring rubric. See ce-advanced-evaluation for bias mitigation.

### Test Set Design

- **Stratify by complexity**: Include easy (known-answer), medium (multi-step), and hard (ambiguous) cases
- **Include failure cases**: Test that the agent correctly refuses impossible tasks
- **Version the test set**: Track which tests pass over time
- **Minimum viable test set**: 50-100 cases covering edge cases, typical cases, and adversarial cases

### Context-Engineering Evaluation

Test context management specifically:
- Does retrieval find the right documents?
- Does the system prompt survive long conversations?
- Does the agent maintain coherence after context compression?
- Do tool descriptions lead to correct tool selection?

### Continuous Evaluation

Run evaluations on every meaningful change:
- New model version → full eval suite
- System prompt change → targeted eval for affected capabilities
- Tool schema change → tool selection accuracy eval
- Memory system change → retrieval quality eval

## Examples

### Example 1: Outcome-based rubrics for code generation
Define weighted dimensions such as correctness, test coverage, and API contract adherence, then score final diffs and CI results rather than whether the agent used a specific tool call order. This aligns evaluation with what users care about while tolerating multiple valid solution paths.

### Example 2: Building diverse test sets
Stratify cases by complexity and risk (easy factual lookups, multi-step refactors, adversarial prompts) and version the set in git so regressions map to scenario classes. Refresh a slice periodically so the agent cannot overfit to a frozen golden path.

## Troubleshooting

1. **Overfitting to test cases**: Rotate test cases periodically; avoid optimizing for specific examples.
2. **Ignoring failure modes**: A 95% pass rate can hide a catastrophic 5%.
3. **Single-dimension scoring**: Accuracy alone misses completeness, safety, and efficiency.
4. **Testing in isolation**: Agents behave differently with real tools vs. mocked tools.
5. **Judge model bias**: LLM judges have systematic biases — see ce-advanced-evaluation.

## References

- [Evaluation Metrics Reference](./references/metrics.md)
- Related CE skills: ce-advanced-evaluation, ce-context-fundamentals, ce-context-degradation
- Frameworks: LMSYS Arena, RAGAS, DeepEval, custom rubric systems
