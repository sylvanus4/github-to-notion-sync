## Onboarding Accelerator

Generate a complete new developer onboarding kit: architecture overview, ownership maps, interactive diagrams, study vault, getting-started guide, and infrastructure docs — orchestrating 8 skills.

### Usage

```
/onboarding-accelerator                        # full onboarding kit
/onboarding-accelerator --role frontend        # frontend-focused kit
/onboarding-accelerator --role backend         # backend-focused kit
/onboarding-accelerator --section architecture # architecture + diagrams only
/onboarding-accelerator --section docs         # documentation only
/onboarding-accelerator --output docs/onboarding/  # custom output path
```

### Workflow

1. **Analyze** (parallel) — deep-review for architecture + codebase-archaeologist for ownership
2. **Visualize** (parallel) — visual-explainer for diagrams + design-architect for design system
3. **Document** (parallel) — technical-writer for guides + docs-tutor-setup for study vault
4. **Environment** (parallel) — local-dev-runner for setup + sre-devops-expert for infra
5. **Assemble** — Combine into structured kit with README entry point
6. **Report** — Deliverables list with suggested reading order

### Execution

Read and follow the `onboarding-accelerator` skill (`.cursor/skills/onboarding-accelerator/SKILL.md`) for pipeline groups, deliverable format, and output structure.

### Examples

Full onboarding kit:
```
/onboarding-accelerator
```

Frontend-focused onboarding:
```
/onboarding-accelerator --role frontend
```

Architecture section only:
```
/onboarding-accelerator --section architecture
```
