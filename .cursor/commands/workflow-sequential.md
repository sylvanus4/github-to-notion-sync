## Workflow Sequential

Execute tasks in dependency order with checkpoints, error recovery, and conditional skipping.

### Usage

```
/workflow-sequential                                    # interactive — define tasks
/workflow-sequential "task1" "task2" "task3"            # linear chain
/workflow-sequential --error-policy retry "t1" "t2"    # retry on failure
/workflow-sequential --checkpoint commit "t1" "t2"     # commit after each task
```

### Workflow

1. **Validate** — Build dependency graph, detect cycles, topological sort
2. **Execute** — Run each task in order, passing outputs forward
3. **Checkpoint** — Verify output after each task; optionally commit
4. **Error handling** — Apply per-task policy (halt / retry / skip-warn)
5. **Report** — Per-task status, timing, and pipeline outcome

### Execution

Read and follow the `workflow-sequential` skill (`.cursor/skills/workflow-sequential/SKILL.md`) for task graph validation, checkpoint protocol, and error handling.

### Examples

Data sync pipeline:
```
/workflow-sequential "check DB status" "import CSVs" "fetch Yahoo Finance" "verify sync"
```

Build pipeline with retry:
```
/workflow-sequential --error-policy retry "lint" "test" "build" "deploy"
```
