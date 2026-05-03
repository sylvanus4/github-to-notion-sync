# OMC Task Lifecycle FSM

When running OMC skills (omc-company, omc-e2r), enforce this task lifecycle:

```
Pending -> Processing -> Completed -> Accepted -> Finished
                |              |
                v              v
             Failed         Rejected -> Processing (retry)
```

## 7 Invariants (Deadlock-Free Guarantee)

1. **DAG Invariant**: Task dependency graph must be acyclic. Validate before execution.
2. **Mutual Exclusion**: One agent per task. Never dispatch two agents to the same task.
3. **Schedule Idempotency**: Dispatching an already-Completed task is a no-op.
4. **Review Termination**: Max 3 review iterations per task. Escalate after that.
5. **Cascade Safety**: Rejecting a task blocks only direct dependents, not the entire graph.
6. **Dependency Completeness**: A task enters Processing only when ALL dependencies are Accepted.
7. **Recovery Precision**: On failure, retry from last checkpoint with error context, not from scratch.

## State Transition Rules

- Only forward transitions allowed (Pending -> Processing -> Completed -> Accepted -> Finished)
- Rejected -> Processing is the only backward transition (with reviewer feedback attached)
- Failed tasks can retry (Failed -> Pending) max 2 times
- Use TaskCreate/TaskUpdate to track state changes
