## Workflow Parallel

Fan out independent tasks to parallel subagents with a defined aggregation strategy.

### Usage

```
/workflow-parallel                                          # interactive — define tasks
/workflow-parallel --strategy merge "t1" "t2" "t3" "t4"   # merge findings
/workflow-parallel --strategy vote "t1" "t2" "t3"          # majority vote
/workflow-parallel --strategy defer "t1" "t2" "t3"         # defer to specialist
/workflow-parallel --strategy union "t1" "t2" "t3"         # union all results
```

### Workflow

1. **Validate** — Confirm tasks are independent (no dependencies)
2. **Strategy** — Define aggregation before launch (merge / vote / defer / union)
3. **Launch** — Up to 4 parallel subagents; batch if more tasks
4. **Aggregate** — Apply strategy to combine results
5. **Conflicts** — Flag or resolve contradictory results
6. **Report** — Per-agent summary + aggregated results

### Execution

Read and follow the `workflow-parallel` skill (`.cursor/skills/workflow-parallel/SKILL.md`) for aggregation strategies, conflict resolution, and batching rules.

### Examples

Multi-domain code review (merge):
```
/workflow-parallel --strategy merge "review frontend" "review backend" "review security" "review tests"
```

Decision by vote:
```
/workflow-parallel --strategy vote "should we refactor module A?" "should we refactor module A?" "should we refactor module A?"
```

Batch document analysis (union):
```
/workflow-parallel --strategy union "analyze doc1" "analyze doc2" "analyze doc3" "analyze doc4" "analyze doc5" "analyze doc6"
```
