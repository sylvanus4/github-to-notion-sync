## Ralplan

3-agent consensus planning with RALPLAN-DR structured deliberation. Runs Planner → Architect → Critic loop until consensus is reached (max 5 iterations).

### Usage

```
<task or feature to plan>
```

### Execution

Read and follow the `omc-ralplan` skill (`.cursor/skills/omc-ralplan/SKILL.md`) for the full workflow.

### Examples

```bash
# Consensus plan for a new feature
/omc-ralplan Add user authentication with OAuth2

# Architectural planning with review
/omc-ralplan Migrate database schema to support multi-tenancy

# Plan with automatic deliberate mode (high-risk)
/omc-ralplan Implement payment processing integration
```
