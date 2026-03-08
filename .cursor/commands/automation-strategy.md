## Automation Strategy

Strategic automation planning — decide what to automate, design human-in-the-loop checkpoints, and calculate automation ROI.

### Usage

```
/automation-strategy                      # Interactive: choose mode
/automation-strategy assess <process>     # Score a process for automation potential
/automation-strategy audit                # Full automation audit of all processes
/automation-strategy hitl <process>       # Design human-in-the-loop for a process
/automation-strategy roi                  # Calculate automation ROI for the pipeline
/automation-strategy plan                 # Generate phased automation plan
```

### Workflow

1. **Assess** — Score processes with ARIA framework (Frequency, Volume, Consistency, Error cost, Time saved)
2. **Risk** — Evaluate automation risks with impact/probability matrix
3. **Design** — Choose checkpoint pattern (Review-Before-Publish, Alert-on-Anomaly, Escalation Ladder, Confidence-Gated)
4. **Audit** — Review all automated processes for accuracy, reliability, and ROI
5. **Plan** — Recommend implementation order by ROI and risk

### Execution

Read and follow the `automation-strategist` skill (`.cursor/skills/automation-strategist/SKILL.md`) for the ARIA framework, risk categories, checkpoint patterns, and anti-patterns.

### Examples

Should we automate Slack posting?
```
/automation-strategy assess "Slack report posting"
```

Full pipeline automation audit:
```
/automation-strategy audit
```

Design human review for reports:
```
/automation-strategy hitl "report publishing"
```
