## Workflow

Select and execute the right workflow pattern (Sequential, Parallel, or Evaluator-Optimizer) for a set of tasks. Uses the decision tree from `workflow-patterns.mdc`.

### Usage

```
/workflow                              # interactive — asks which pattern fits
/workflow sequential [tasks...]        # execute tasks in dependency order
/workflow parallel [tasks...]          # fan out independent tasks to parallel agents
/workflow eval-opt [task]              # wrap a task in an evaluator-optimizer loop
```

### Decision Tree

1. Can a single agent handle this? → No workflow needed.
2. Do tasks have sequential dependencies? → `/workflow-sequential`
3. Can subtasks run independently? → `/workflow-parallel`
4. Does quality need iterative refinement? → `/workflow-eval-opt`

### Execution

If a specific pattern is provided, read and follow the corresponding skill:
- Sequential → `.cursor/skills/workflow-sequential/SKILL.md`
- Parallel → `.cursor/skills/workflow-parallel/SKILL.md`
- Eval-opt → `.cursor/skills/workflow-eval-opt/SKILL.md`

If no pattern is specified, analyze the user's tasks against the decision tree, recommend a pattern, and ask for confirmation before executing.

### Examples

Interactive pattern selection:
```
/workflow
```

Sequential data pipeline:
```
/workflow sequential "check freshness" "import CSV" "fetch Yahoo" "verify sync"
```

Parallel code review:
```
/workflow parallel "review frontend" "review backend" "review security" "review tests"
```

Iterative report refinement:
```
/workflow eval-opt "generate stock analysis report"
```
