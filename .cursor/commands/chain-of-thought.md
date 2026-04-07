---
description: "Show the complete reasoning chain from premises to conclusion with all intermediate steps"
argument-hint: "<question requiring multi-step reasoning>"
---

# Chain of Thought Reasoning

Show every step of the reasoning process from premises to conclusion. No leaps, no shortcuts — every inference is explicit.

## Usage

```
/chain-of-thought Should we migrate from REST to GraphQL?
/chain-of-thought Why is our Kubernetes pod OOMKilled with 4GB memory limit?
/chain-of-thought Is it cheaper to run inference on-prem vs cloud at 10K req/day?
/chain-of-thought 삼성전자 주가가 반도체 업황과 상관관계가 약해진 이유
/chain-of-thought Why does adding an index sometimes make queries slower?
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **State the question** — Restate `$ARGUMENTS` as a precise question
2. **List known facts/premises** — Tag each as `[Premise]`
3. **Show each logical step:**
   - Tag inferences as `[Inference]` with justification
   - Tag assumptions as `[Assumption]` — something believed but not proven
   - Show how each step follows from previous steps
4. **Arrive at conclusion** — Tag as `[Conclusion]`
5. **Assess confidence** — State confidence level (High/Medium/Low) and identify what could change the conclusion
6. **List alternative conclusions** — If the reasoning could lead elsewhere under different assumptions

### Output Format

```
## Question
[Precise restatement]

## Reasoning Chain

1. [Premise] ...
2. [Premise] ...
3. [Inference] From (1) and (2): ...
4. [Assumption] ...
5. [Inference] From (3) and (4): ...
6. [Conclusion] Therefore: ...

## Confidence: [High/Medium/Low]
[What would change this conclusion]

## Alternative Conclusions
- If [assumption X] is wrong → [different conclusion]
```

### Constraints

- Every inference must cite which premises or prior inferences it depends on
- Assumptions must be explicitly flagged — never hidden in an inference
- The chain must be linear and traceable — a reader should be able to follow from step 1 to conclusion without gaps
- If the reasoning genuinely cannot reach a confident conclusion, say so
