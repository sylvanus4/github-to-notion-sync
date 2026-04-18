## Grill Me

Socratic deep interview that asks relentless clarifying questions one at a time until every branch of the decision tree is resolved before implementation begins.

### Usage

```
/grill-me                              # start interview about current task
/grill-me "Add user authentication"    # interview about a specific feature
/grill-me --threshold 15               # set ambiguity threshold to 15%
```

### Workflow

1. **Understand intent** — Read the user's feature/task description
2. **Ask one question at a time** — Target the highest-ambiguity area first
3. **Score clarity** — Track ambiguity score across weighted dimensions
4. **Iterate** — Continue until ambiguity drops below threshold (default 20%)
5. **Output spec** — Produce a structured specification with acceptance criteria

### Execution

Read and follow the `omc-deep-interview` skill (`.cursor/skills/omc/omc-deep-interview/SKILL.md`) for question methodology, scoring rubric, and output format.

### Examples

Grill before building a feature:
```
/grill-me "Add Stripe subscription billing"
```

Grill before a risky migration:
```
/grill-me "Migrate from REST to GraphQL"
```

Quick interview with lower threshold:
```
/grill-me --threshold 30 "Add dark mode"
```
