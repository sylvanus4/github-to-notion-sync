## Multi-Agent Consensus

Spawn multiple sub-agents to solve the same problem independently, then aggregate their answers into a consensus decision.

### Usage

```
/multi-agent-consensus "best caching strategy for our API"
/multi-agent-consensus --agents 5 "architecture for real-time notifications"
/multi-agent-consensus --mode vote "should we migrate to gRPC?"
```

### Workflow

1. **Define** — Frame the problem or decision clearly
2. **Dispatch** — Spawn N independent sub-agents with the same prompt
3. **Collect** — Gather each agent's analysis and recommendation
4. **Aggregate** — Merge results: voting, weighted scoring, or union of insights
5. **Synthesize** — Produce a consensus report with areas of agreement and divergence

### Execution

Read and follow the `hermes-mixture-of-agents` skill (`.cursor/skills/standalone/hermes-mixture-of-agents/SKILL.md`) for multi-model consensus via parallel LLM queries. For adversarial refinement with competition, use `autoreason` (`.cursor/skills/automation/autoreason/SKILL.md`). For parallel sub-agent dispatch, use `workflow-parallel` (`.cursor/skills/workflow/workflow-parallel/SKILL.md`).

### Examples

Architecture decision:
```
/multi-agent-consensus "evaluate 3 approaches to event sourcing for our platform"
```

Strategy consensus:
```
/multi-agent-consensus --agents 5 "pricing strategy for our SaaS tier"
```
