---
description: "Apply 3-5 analytical frameworks simultaneously to a topic and cross-reference for blind spots and synthesis"
argument-hint: "<topic to analyze through multiple frameworks>"
---

# Parallel Lenses

Apply multiple analytical frameworks to the same topic in parallel, then cross-reference findings to surface blind spots and deeper insights.

## Usage

```
/parallel-lenses Why is our user retention dropping?
/parallel-lenses Should we pivot from B2B to B2C?
/parallel-lenses --lenses first-principles,systems-thinking,game-theory Market entry strategy for Southeast Asia
/parallel-lenses 기술 부채 해결 vs 신기능 개발 우선순위 결정
/parallel-lenses --with-verdict The future of edge computing vs centralized cloud
```

## Your Task

User input: $ARGUMENTS

### Mode Selection

Parse `$ARGUMENTS` for flags:

- **No flags** — Auto-select 3-4 frameworks based on topic (default)
- `--lenses <f1,f2,...>` — Specify frameworks (e.g., `first-principles,swot,jobs-to-be-done,porter`)
- `--with-verdict` — Add a final verdict section that picks a recommended lens
- `--matrix` — Output a cross-reference matrix instead of sequential sections

### Available Frameworks

| Framework | Focus |
|-----------|-------|
| `first-principles` | Decompose to fundamental truths, rebuild from scratch |
| `systems-thinking` | Map feedback loops, identify leverage points |
| `game-theory` | Analyze strategic interactions, Nash equilibria, incentives |
| `jobs-to-be-done` | What "job" the user is hiring the product for |
| `porter` | Five forces competitive analysis |
| `design-thinking` | Empathize, define, ideate, prototype, test |
| `constraint-theory` | Find the bottleneck that limits the whole system |
| `inversion` | What would make this fail? Work backward from failure |
| `economic` | Cost-benefit, opportunity cost, marginal analysis |

### Workflow

1. **Parse topic** — Extract the question or decision from `$ARGUMENTS`
2. **Select frameworks** — Choose 3-4 most relevant frameworks (or use `--lenses` override)
3. **Run each framework in parallel**
   - Apply the framework rigorously to the topic
   - Produce 3-5 key insights unique to this lens
   - Note what this lens reveals that others might miss
4. **Cross-reference** — Compare findings across all lenses
   - Where do frameworks agree? (strong signal)
   - Where do they conflict? (interesting tension)
   - What does only one framework surface? (potential blind spot)
5. **Synthesize** — Combine into an integrated analysis
6. **Verdict** (if `--with-verdict`) — Recommend which framework is most illuminating for this specific topic

### Output Format

```
## Parallel Lenses: [Topic]

### Lens 1: [Framework Name]
**Core question:** [What this framework asks]
- [Insight 1]
- [Insight 2]
- [Insight 3]
**Unique contribution:** [What only this lens reveals]

### Lens 2: [Framework Name]
...

### Cross-Reference Matrix
| Insight | [Lens 1] | [Lens 2] | [Lens 3] |
|---------|----------|----------|----------|
| [Finding A] | ✅ | ✅ | — |
| [Finding B] | — | ✅ | ⚠️ |

### Integrated Analysis
[Synthesis combining the strongest insights from all lenses]
```

### Constraints

- Each lens must produce genuinely different insights — not repackaging the same point
- At least one lens must surface a non-obvious or contrarian insight
- Cross-reference must identify at least one area of conflict between frameworks
- Do not privilege any single framework without justification

### Execution

Reference `first-principles-analysis` (`.cursor/skills/standalone/first-principles-analysis/SKILL.md`) for the first-principles lens. Reference `system-thinker` (`.cursor/skills/standalone/system-thinker/SKILL.md`) for the systems-thinking lens. For parallel execution of lenses, reference `workflow-parallel` (`.cursor/skills/workflow/workflow-parallel/SKILL.md`).
