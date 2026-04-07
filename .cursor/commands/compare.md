---
description: "Compare 2-4 items across consistent dimensions with a structured matrix and a clear recommendation"
argument-hint: "<item A> vs <item B> [vs <item C>]"
---

# Side-by-Side Comparison

Compare multiple items across consistent evaluation dimensions. Produces a structured matrix with a final recommendation.

## Usage

```
/compare React vs Vue vs Svelte for a dashboard app
/compare PostgreSQL vs MySQL for time-series data
/compare --weighted Kubernetes vs Docker Swarm vs Nomad
/compare --with-research FastAPI vs Express vs Gin for microservices
/compare Sonnet vs GPT-4 vs Gemini for code generation
/compare 토스증권 vs 키움증권 vs KIS 자동매매 적합성 비교
```

## Your Task

User input: $ARGUMENTS

### Mode Selection

Parse `$ARGUMENTS` for flags:

- **No flags** — Comparison matrix with qualitative assessment (default)
- `--weighted` — Add numerical scores (1-10) per dimension with weighted total
- `--with-research` — Ground comparison with current data via web search
- `--for <context>` — Tailor evaluation dimensions to a specific use case
- `--concise` — Output only the table and winner, no prose

### Workflow

1. **Parse items** — Extract 2-4 items to compare from `$ARGUMENTS` (split on "vs", "versus", "or")
2. **Define dimensions** — Choose 5-8 evaluation criteria relevant to the domain (e.g., Performance, Ecosystem, Learning Curve, Cost, Scalability)
3. **Research** (if `--with-research`) — Gather current benchmarks, pricing, and community metrics
4. **Evaluate each item** — Assess against every dimension with brief justification
5. **Score** (if `--weighted`) — Assign 1-10 scores per dimension; calculate weighted totals
6. **Identify winner** — Determine the best option overall and the best option per dimension
7. **Write recommendation** — State who should choose what, and under which conditions

### Output Format

```
## Comparison: [Item A] vs [Item B] vs [Item C]

| Dimension | [Item A] | [Item B] | [Item C] |
|-----------|----------|----------|----------|
| [Dim 1]   | [Assessment] | [Assessment] | [Assessment] |
| [Dim 2]   | ...      | ...      | ...      |

### Winner: [Item]
[2-3 sentences explaining when and why this is the best choice]

### When to Choose Each
- **[Item A]** — Best when [condition]
- **[Item B]** — Best when [condition]
- **[Item C]** — Best when [condition]
```

### Constraints

- Every item must be evaluated against every dimension — no gaps in the matrix
- Assessments must be factual, not opinions; cite benchmarks or data when available
- Never declare a winner without stating the conditions under which it wins
- If items are too different to compare meaningfully, say so and suggest a better framing

### Execution

Reference `feynman-source-comparison` (`.cursor/skills/research/feynman-source-comparison/SKILL.md`) for structured agreement/disagreement matrix methodology. If `--with-research` is set, use `parallel-web-search` for current data.
