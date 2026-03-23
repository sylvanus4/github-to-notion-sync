## First Principles Analysis

Decompose any topic into fundamental truths by systematically stripping inherited assumptions. Identifies what is provably true, discards conventional wisdom that lacks foundation, and rebuilds understanding from bedrock truths only.

### Usage

```
# Analyze a topic
/first-principles "Why do companies adopt Kubernetes?"
/first-principles "SaaS 가격 정책은 왜 구독 모델이어야 하나?"

# Broad topic — you'll be asked to narrow
/first-principles "AI strategy"
```

### Workflow

1. **Assumption Inventory** — List every assumption people commonly make (8-15 items across structural, causal, boundary, value, historical categories)
2. **Assumption Stripping** — Test each: provably true? or inherited belief? Classify as Bedrock / Conditional / Inherited
3. **Bedrock Truth Extraction** — Keep only what survives; state why each is fundamentally true
4. **Rebuild from Fundamentals** — Reconstruct understanding from bedrock truths only; compare against conventional wisdom; surface novel insights

### Output

A structured analysis containing: assumption inventory with categories, assumption verdicts with reasoning, bedrock truths, rebuilt understanding with delta-vs-conventional-wisdom table, novel insights, and actionable implications.

### Execution

Read and follow the `first-principles-analysis` skill (`.cursor/skills/first-principles-analysis/SKILL.md`) for the full framework, output template, domain hints, examples, and error handling.
