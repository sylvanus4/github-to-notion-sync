## Design Interface

Generate multiple radically different interface designs for a module using parallel sub-agents, each with different tradeoffs.

### Usage

```
/design-interface "settings page"              # generate 3-5 competing designs
/design-interface --count 5 "onboarding flow"  # specify number of variants
/design-interface --stack react                 # target a specific framework
```

### Workflow

1. **Understand requirements** — Clarify the interface purpose, users, and constraints
2. **Spawn sub-agents** — Launch 3-5 parallel design agents with different philosophies
3. **Generate variants** — Each agent produces a complete interface design with rationale
4. **Compare** — Present all designs side-by-side with tradeoff analysis
5. **Refine** — Iterate on the chosen design based on user feedback

### Execution

Read and follow the `anthropic-frontend-design` skill (`.cursor/skills/anthropic/anthropic-frontend-design/SKILL.md`) for design quality standards. Use parallel sub-agents via the Task tool to generate competing designs simultaneously.

### Examples

Design a settings page with multiple options:
```
/design-interface "user settings page with profile, notifications, and billing tabs"
```

Design an onboarding flow:
```
/design-interface --count 4 "first-time user onboarding wizard"
```
