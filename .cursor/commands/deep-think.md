---
description: "Maximum-depth analysis combining chain-of-thought, deliberate thinking, bias check, and self-evaluation in a single pass"
argument-hint: "<complex question requiring the deepest possible analysis>"
---

# Deep Think — Maximum Depth Analysis

The most thorough analysis mode. Combines chain-of-thought reasoning, deliberate slow thinking, systematic bias detection, and self-evaluation into a single comprehensive pass. Use for high-stakes decisions where cutting corners is unacceptable.

## Usage

```
/deep-think Should we pivot from B2B SaaS to platform-as-a-service?
/deep-think Is our current multi-tenant architecture going to scale to 10K customers?
/deep-think Evaluate whether we should build vs buy our ML inference stack
/deep-think 현재 투자 포트폴리오 전략의 근본적 약점과 대안 분석
/deep-think Will AI coding assistants make traditional IDEs obsolete within 5 years?
```

## Your Task

User input: $ARGUMENTS

### Workflow

#### Phase 1 — Chain of Thought
1. State the question precisely
2. List all known facts and premises
3. Show each logical step with tagged inferences and assumptions
4. Arrive at an initial conclusion with confidence level

#### Phase 2 — Deliberate Slow Thinking
5. Identify why this question is hard — what are the competing forces?
6. Consider 3+ alternative framings
7. Evaluate evidence for and against each framing
8. Apply the Karpathy Opposite Direction Test: construct the strongest case for the opposite of the Phase 1 conclusion

#### Phase 3 — Bias Check
9. Scan the analysis so far for the 8 bias types (confirmation, survivorship, anchoring, availability, selection, cultural, recency, authority)
10. Flag any detected biases with evidence
11. Generate debiased alternatives for each flagged bias

#### Phase 4 — Self-Evaluation
12. Score the analysis across 5 dimensions (Accuracy, Completeness, Clarity, Actionability, Evidence Quality) at 1-10
13. If any dimension scores below 7, revise that section
14. Re-score after revision

#### Phase 5 — Synthesis
15. Produce the final answer incorporating all phases
16. State remaining uncertainty and what would change the conclusion
17. Provide a clear, actionable recommendation

### Output Format

```
## Deep Analysis: [Topic]

### Phase 1: Reasoning Chain
[Premises] → [Inferences] → [Initial Conclusion]
Confidence: [High/Medium/Low]

### Phase 2: Deliberate Examination
**Why this is hard:** [...]
**Alternative framings:** [...]
**Strongest counterargument:** [...]

### Phase 3: Bias Audit
| Bias Type | Detected? | Evidence | Debiased Alternative |
|-----------|-----------|----------|---------------------|
| ... | ... | ... | ... |

### Phase 4: Quality Scorecard
| Dimension | Score | Note |
|-----------|-------|------|
| Accuracy | X/10 | [...] |
| Completeness | X/10 | [...] |
| Clarity | X/10 | [...] |
| Actionability | X/10 | [...] |
| Evidence | X/10 | [...] |
| **Composite** | **X.X/10** | |

### Phase 5: Final Synthesis
**Conclusion:** [...]
**Confidence:** [High/Medium/Low]
**Remaining uncertainty:** [...]
**Actionable recommendation:** [...]
```

### Constraints

- This is the most expensive command in terms of output — use only when the decision justifies the depth
- Every phase must produce substantive output — no "Phase 3: No biases detected" without actually checking
- The final synthesis must integrate insights from all 4 preceding phases, not just restate Phase 1
- If the composite quality score is below 7.0 after revision, explicitly state what additional information would be needed

### Execution

Apply the `critical-thinking` rule (`.cursor/rules/critical-thinking.mdc`) throughout. Reference `ce-advanced-evaluation` (`.cursor/skills/ce/ce-advanced-evaluation/SKILL.md`) for the scoring rubric. Reference `workflow-eval-opt` (`.cursor/skills/workflow/workflow-eval-opt/SKILL.md`) for the evaluator-optimizer loop.
