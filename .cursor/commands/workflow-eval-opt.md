## Workflow Eval-Opt

Wrap a generation task in an evaluator-optimizer loop for iterative quality refinement.

### Usage

```
/workflow-eval-opt                                     # interactive — define task and criteria
/workflow-eval-opt "generate stock report"             # default: 2 iterations, threshold 8.0
/workflow-eval-opt --max-iter 3 "draft customer email" # custom max iterations
/workflow-eval-opt --threshold 9.0 "write API docs"    # custom quality threshold
/workflow-eval-opt --evaluator code "refactor module"  # use code evaluator preset
/workflow-eval-opt --evaluator report "daily report"   # use report evaluator preset
```

### Workflow

1. **Define criteria** — Measurable quality dimensions BEFORE generating
2. **Generate** — First pass (generator agent)
3. **Evaluate** — Score against criteria (separate evaluator agent, readonly)
4. **Decision gate** — Pass / Refine / Best Effort
5. **Refine** — Feed feedback to generator, re-generate (scope-reduced)
6. **Stop** — Threshold met, max iterations, no improvement, or regression
7. **Report** — Iteration history, scores, final output

### Execution

Read and follow the `workflow-eval-opt` skill (`.cursor/skills/workflow-eval-opt/SKILL.md`) for evaluator configuration, stopping criteria, and pre-built evaluator presets (code, report, content).

### Examples

Report with quality gate:
```
/workflow-eval-opt "generate daily stock analysis report"
```

Code with security standards:
```
/workflow-eval-opt --evaluator code --threshold 0 "write auth endpoint with input validation"
```

Content with high bar:
```
/workflow-eval-opt --max-iter 3 --threshold 9.0 "draft investor quarterly update"
```
