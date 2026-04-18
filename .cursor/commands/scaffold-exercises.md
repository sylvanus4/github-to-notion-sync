## Scaffold Exercises

Create structured exercise directories with problems, solutions, explainers, and tests for courses, onboarding, or workshops.

### Usage

```
/scaffold-exercises "React hooks fundamentals" --sections 3 --exercises-per-section 4
/scaffold-exercises "SQL query optimization" --audience intermediate
/scaffold-exercises "TypeScript generics" --format ts
```

### Workflow

1. **Define** — Gather topic, audience level, exercise count, and language/framework
2. **Structure** — Generate directory tree with sections, problems, starters, solutions, and tests
3. **Content** — Write problem statements, starter code, reference solutions, explainers, and test files
4. **Index** — Create README with table of contents, prerequisites, difficulty ratings, and setup instructions

### Execution

Read and follow the `scaffold-exercises` skill (`.cursor/skills/standalone/scaffold-exercises/SKILL.md`) for the full 4-phase scaffolding workflow.

### Examples

React course with progressive sections:
```
/scaffold-exercises "React hooks" --sections 3 --audience beginner
```

TypeScript kata set:
```
/scaffold-exercises "TypeScript type challenges" --exercises 10 --format ts --audience advanced
```
