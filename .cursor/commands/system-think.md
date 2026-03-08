## System Think

Design end-to-end automated systems by mapping data flows, finding bottlenecks, creating feedback loops, and converting manual processes.

### Usage

```
/system-think                             # Interactive: choose mode
/system-think map                         # Map current daily pipeline data flow
/system-think map <process>               # Map a specific process
/system-think bottleneck                  # Analyze bottlenecks in the current pipeline
/system-think feedback <prediction>       # Design a feedback loop for a prediction
/system-think convert <process>           # Convert a manual process to automated
```

### Workflow

1. **Map** — Trace data from source to output, annotate triggers and formats
2. **Bottleneck** — Profile stages, classify issues, prioritize fixes
3. **Feedback** — Define prediction, ground truth, comparison, and model update
4. **Convert** — Document manual steps, classify automation potential, design system

### Execution

Read and follow the `system-thinker` skill (`.cursor/skills/system-thinker/SKILL.md`) for the DFTS framework, bottleneck classification, and feedback loop templates.

### Examples

Map the daily pipeline:
```
/system-think map daily-pipeline
```

Design signal accuracy tracking:
```
/system-think feedback "buy signal accuracy"
```

Automate weekly review:
```
/system-think convert "Monday morning stock check"
```
