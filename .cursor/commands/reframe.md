---
description: "Force the AI to argue the opposite position with equal conviction — the reframe test"
argument-hint: "<statement, proposal, or conclusion to challenge>"
---

# Reframe Test

Before accepting any conclusion, argue the opposite position with equal conviction. If the opposing argument is weak, your original conclusion is strong. If it's compelling, you've found a blind spot. This command eliminates confirmation bias by making the AI its own adversary.

## Usage

```
/reframe "We should use microservices for the new platform"
/reframe "React is the best choice for our frontend"
/reframe "Hiring senior engineers is more cost-effective than training juniors"
/reframe "우리는 AI 기능을 자체 개발해야 한다"
/reframe "Remote work reduces productivity"
/reframe "We should raise our Series A now"
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **State the original position** — Summarize the input as a clear, falsifiable thesis
2. **Steelman the original** — Present the 3 strongest arguments FOR this position
3. **Flip and steelman the opposite** — Now argue the opposite position with genuine conviction:
   - Assume the opposite is true and find the best evidence
   - Adopt the mindset of someone who deeply believes the opposite
   - Do NOT strawman — present the strongest possible counter-case
   - Find at least 3 compelling arguments the original position ignores
4. **Identify the crux** — What is the single factual question that would settle this debate? (The "crux" is the disagreement that, if resolved, would change one side's mind)
5. **Verdict** — Based on the quality of arguments on both sides:
   - **Original holds:** The reframe exposed no serious weaknesses
   - **Reframe wins:** The opposite position is actually stronger
   - **Context-dependent:** Neither is universally correct — specify the conditions where each wins

### Output Format

```
## Reframe Test

### Original Position
> [Clear thesis statement]

### Case FOR (Steelman)
1. [Strongest argument]
2. [Second strongest]
3. [Third strongest]

### Case AGAINST (Reframe — argued with equal conviction)
1. [Strongest counter-argument]
2. [Second strongest counter]
3. [Third strongest counter]

### The Crux
[The single factual question that would settle this — e.g., "Does team velocity increase with microservices at our current team size of 8?"]

### Verdict: [Original Holds / Reframe Wins / Context-Dependent]

[2-3 sentence explanation of why, referencing specific arguments above]

**If context-dependent:**
- Original wins when: [conditions]
- Reframe wins when: [conditions]
```

### Constraints

- The reframe section must be argued with genuine conviction, not as a devil's advocate exercise with obvious hedging
- Both sides must have exactly 3 arguments — no imbalance allowed
- The crux must be a concrete, answerable question, not a vague philosophical one
- Never default to "it depends" without specifying exact conditions for each side
- If you catch yourself writing a weak reframe, stop and try harder — weak opposition means weak analysis
- Korean input → Korean output
