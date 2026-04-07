---
description: "Identify and flag potential biases in a response, analysis, or dataset with debiased alternatives"
argument-hint: "<text, analysis, or topic to check for bias>"
---

# Systematic Bias Detection

Scan content for 8 cognitive bias types. Flag each instance with evidence, suggest debiased alternatives, and rate overall bias risk.

## Usage

```
/systematic-bias-check Our analysis shows microservices are always better than monoliths
/systematic-bias-check This market research concludes AI will replace 80% of jobs by 2030
/systematic-bias-check Our user interview findings from 5 enterprise customers
/systematic-bias-check 우리 포트폴리오 전략이 과거 3년간 시장을 이겼다는 결론
/systematic-bias-check The decision to hire only from top-tier universities
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Parse content** — Read the text, analysis, or topic from `$ARGUMENTS`
2. **Scan for 8 bias types:**

   | Bias | Signal |
   |------|--------|
   | Confirmation | Cherry-picked evidence supporting a predetermined conclusion |
   | Survivorship | Only looking at winners, ignoring failures |
   | Anchoring | Over-relying on the first piece of information |
   | Availability | Overweighting recent or vivid examples |
   | Selection | Non-representative sample or methodology |
   | Cultural | Assumptions rooted in one culture presented as universal |
   | Recency | Treating recent trends as permanent shifts |
   | Authority | Accepting claims because of who said them, not evidence |

3. **Flag each instance** — Cite the specific text and explain why it's biased
4. **Suggest debiased alternatives** — How to reframe or re-analyze
5. **Rate overall bias risk** — Low / Medium / High with justification

### Output Format

```
## Bias Check: [Subject]

### Detected Biases

#### 🔴 [Bias Type]: [Severity]
**Found in:** "[quoted text or claim]"
**Why it's biased:** [Explanation]
**Debiased alternative:** [Reframed version]

#### 🟡 [Bias Type]: [Severity]
...

### Overall Bias Risk: [Low/Medium/High]
[2-3 sentences explaining the aggregate bias risk and recommended actions]

### What Would Make This Analysis More Robust
- [Specific action 1]
- [Specific action 2]
```

### Constraints

- Must check all 8 bias types — even if some aren't found (note "Not detected")
- Flagged biases must cite specific evidence from the content, not speculate
- Debiased alternatives must be actionable, not just "be more careful"
- If the content is genuinely well-balanced, say so — don't manufacture bias findings

### Execution

Reference `ce-advanced-evaluation` (`.cursor/skills/ce/ce-advanced-evaluation/SKILL.md`) for bias mitigation techniques (position bias, length bias, self-enhancement bias). Apply the `critical-thinking` rule (`.cursor/rules/critical-thinking.mdc`).
