## Agentic Competency Framework

Self-assess, map, and develop the 7 core agentic engineering competencies (Specification Accuracy, Evaluation & Quality, Task Decomposition, Failure Patterns, Trust & Security, Context Architecture, Cost & Token Economics).

### Usage

```
/agentic-competency assess              # Mode 1: Self-assessment with radar chart
/agentic-competency map                  # Mode 2: Explore skill-to-competency mapping
/agentic-competency map --competency 3   # Mode 2: Focus on a specific competency (1-7)
/agentic-competency plan                 # Mode 3: Generate personalized development plan
/agentic-competency plan --weeks 4       # Mode 3: 4-week plan (default: 2 weeks)
```

### Workflow

1. **Assess** — Answer 7 structured questions (1-5 per competency) → radar chart + gap analysis
2. **Map** — Explore which project skills develop which competencies with practice scenarios
3. **Plan** — Generate a weekly learning plan targeting gaps with specific skill exercises

### Execution

Read and follow the `agentic-competency-framework` skill (`.cursor/skills/agentic-competency-framework/SKILL.md`) for assessment rubrics, skill mappings, and detailed workflows.

### Examples

Quick self-assessment:
```
/agentic-competency assess
```

Explore a specific competency:
```
/agentic-competency map --competency 3
```

Generate full development plan:
```
/agentic-competency plan
```
