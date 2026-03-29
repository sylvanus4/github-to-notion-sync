## Learner

Extract reusable skills from the current conversation using a 3-gate quality filter: not Googleable, codebase-specific, and required real debugging effort. Captures decision-making heuristics — not code snippets.

### Usage

```
[topic or context]
```

### Execution

Read and follow the `omc-learner` skill (`.cursor/skills/omc-learner/SKILL.md`) for the full workflow.

### Examples

```bash
# Extract a skill from the current debugging session
/omc-learner

# Extract with a specific topic hint
/omc-learner JWT session race condition

# Save a discovered pattern
/omc-learner Alembic enum migration gotcha
```
