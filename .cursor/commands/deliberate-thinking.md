---
description: "Engage System 2 thinking — slow, careful, methodical analysis before answering"
argument-hint: "<complex question or decision>"
---

# Deliberate Slow Thinking

System 2 thinking mode. Slow, careful, methodical. Resist the urge to pattern-match an answer — actually think through the problem.

## Usage

```
/deliberate-thinking Should we build a multi-tenant architecture or single-tenant?
/deliberate-thinking What's the right pricing model for our GPU cloud platform?
/deliberate-thinking Is our codebase heading toward a complexity cliff?
/deliberate-thinking 현재 포트폴리오의 리스크 분산이 적절한지 평가
/deliberate-thinking Should we hire 3 juniors or 1 senior engineer?
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Pause and restate** — Rephrase the question in your own words to confirm understanding
2. **Identify what makes this hard** — Why can't this be answered with a quick heuristic? What are the competing forces?
3. **Consider 3+ alternative framings** — How would different people frame this problem?
4. **Evaluate evidence** — For each framing, what evidence supports and contradicts it?
5. **Identify what you might be wrong about** — Apply the Karpathy Opposite Direction Test: construct the strongest case for the opposite conclusion
6. **Construct answer** — Build from the strongest reasoning path, acknowledging alternatives
7. **Flag remaining uncertainty** — What additional information would change your answer?

### Output Format

```
## Deliberate Analysis: [Topic]

### Restated Question
[Precise restatement]

### Why This Is Hard
[2-3 sentences on the competing forces]

### Alternative Framings
1. **[Framing A]** — [How this changes the analysis]
2. **[Framing B]** — [How this changes the analysis]
3. **[Framing C]** — [How this changes the analysis]

### Evidence Assessment
| Claim | Supporting Evidence | Contradicting Evidence |
|-------|-------------------|----------------------|
| ...   | ...               | ...                  |

### Devil's Advocate
[Strongest case for the opposite of your conclusion]

### Conclusion
[Answer built from the strongest reasoning path]

### Remaining Uncertainty
[What would change this answer]
```

### Constraints

- Resist the first answer that comes to mind — explicitly consider why it might be wrong
- Every conclusion must acknowledge at least one valid counterargument
- If you find yourself strongly agreeing with the user's implied preference, that's a red flag for sycophancy — push harder on the opposite case

### Execution

Apply the `critical-thinking` rule (`.cursor/rules/critical-thinking.mdc`) for anti-sycophancy, opposite direction testing, and failure-first elimination.
