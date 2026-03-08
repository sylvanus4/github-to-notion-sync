## AI Workflow

Design and orchestrate AI-powered stock analysis workflows by composing existing skills and scripts into multi-stage pipelines.

### Usage

```
/ai-workflow                              # Interactive: choose template and customize
/ai-workflow daily                        # Daily Analysis Pipeline template
/ai-workflow quick                        # Quick Signal Scan template
/ai-workflow event <URL or headline>      # Event-Driven Research template
/ai-workflow weekly                       # Weekly Deep Dive template
/ai-workflow map                          # Map current data flow without executing
```

### Workflow

1. **Select template** — Choose from daily, quick, event-driven, or weekly
2. **Customize stages** — Add, remove, or reorder pipeline stages
3. **Set error policies** — Abort, skip, or retry per stage
4. **Execute** — Run the workflow with parallel stages where possible
5. **Aggregate** — Combine outputs into the final deliverable
6. **Document** — Save the workflow definition for reuse

### Execution

Read and follow the `ai-workflow-integrator` skill (`.cursor/skills/ai-workflow-integrator/SKILL.md`) for templates, building blocks, and error handling.

### Examples

Custom daily pipeline without discovery:
```
/ai-workflow daily skip-discover
```

Event-driven tweet analysis:
```
/ai-workflow event https://x.com/user/status/123
```

Quick morning signal scan:
```
/ai-workflow quick
```
