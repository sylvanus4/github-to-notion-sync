---
name: ce-multi-agent-patterns
description: >-
  Design patterns for multi-agent architectures — supervisor/orchestrator,
  peer-to-peer swarm, hierarchical decomposition, context isolation, consensus
  mechanisms, and failure mode mitigation. Use when the user asks to "design
  multi-agent system", "coordinate agents", "implement agent orchestration",
  "plan sub-agent architecture", or mentions multi-agent coordination, context
  isolation, agent handoffs, or agent communication patterns. Do NOT use for
  running existing workflow orchestration (use mission-control). Do NOT use
  for workflow pattern selection (use workflow-patterns rule). Do NOT use for
  parallel agent dispatch (use sp-parallel-agents or workflow-parallel).
  Korean triggers: "멀티에이전트", "에이전트 오케스트레이션", "컨텍스트 격리", "에이전트 핸드오프", "에이전트
  조율".
---

# Multi-Agent Architecture Patterns

Sub-agents exist primarily to isolate context, not to simulate organizational roles. The core value of multi-agent systems is distributing work across separate context windows, enabling each agent to operate with focused, high-quality context rather than a single bloated window.

## Core Concepts

### Three Dominant Patterns

1. **Supervisor/Orchestrator**: A coordinator agent delegates tasks and collects results. Best for well-defined, decomposable tasks. The supervisor acts as a context bottleneck — keep its context lean by having sub-agents return structured summaries.

2. **Peer-to-Peer / Swarm**: Agents communicate through shared state or direct handoffs. Use when task boundaries are fluid and agents need to self-organize. AutoGen-style "chat" between agents falls here.

3. **Hierarchical**: Multi-level delegation trees. Use for complex tasks requiring both specialization and coordination. Each level in the hierarchy isolates its own context window.

### Token Economics

Multi-agent architectures cost more tokens than single-agent approaches. Approximate multipliers: 2-agent system ~2.5x, 4-agent system ~5x, 8-agent system ~12x. The overhead comes from each sub-agent's system prompt, tool definitions, and coordination messages.

### Context Isolation Mechanisms

- **Full context delegation**: Sub-agent gets complete problem context plus instructions. High fidelity, high token cost.
- **Instruction passing**: Sub-agent gets only task instructions and relevant data slices. Lower cost, requires precise decomposition.
- **File system memory**: Agents read/write shared files, loading only what they need. Lowest context cost, highest coordination complexity.

### Consensus and Coordination

- **Weighted voting**: Multiple agents evaluate independently, votes are aggregated
- **Debate protocols**: Agents argue positions, a judge agent decides
- **Sequential refinement**: Each agent improves on the previous agent's output

## Failure Modes

| Failure | Cause | Mitigation |
|---------|-------|------------|
| Supervisor bottleneck | Coordinator overloaded | Limit sub-agent count; use hierarchical decomposition |
| Coordination overhead | Too many messages | Use file system for state sharing |
| Divergence | Agents work on conflicting assumptions | Share key decisions through immutable state |
| Error propagation | One agent failure cascades | Validate sub-agent outputs before passing downstream |
| Sycophantic consensus | Agents converge without genuine evaluation | Use adversarial agent roles; require evidence |

## Examples

### Example 1: Supervisor pattern for customer service
Use a lean supervisor that routes intents (billing, shipping, returns) to specialized sub-agents and merges structured summaries back to the user. This keeps each sub-agent’s context focused on one domain and avoids duplicating full chat history in every branch.

### Example 2: Swarm pattern for code review
Run parallel reviewer agents (style, security, tests) with a shared checklist or file-backed state, then aggregate or debate before a final merge decision. The pattern fits when review dimensions are independent and you want breadth without a single overloaded reviewer context.

## Troubleshooting

1. **Agent sprawl**: Adding agents increases coordination overhead faster than capability.
2. **Anthropomorphizing agents**: Naming agents "researcher" or "critic" does not make them better at those roles.
3. **Sycophantic consensus**: Agents tend to agree with each other without genuine evaluation. Force adversarial perspectives.
4. **Context duplication**: Passing the same context to multiple agents multiplies cost without benefit.
5. **Handoff information loss**: Summarize at each handoff boundary. The game-of-telephone effect is real.

## References

- [Multi-Agent Frameworks Reference](./references/frameworks.md)
- Related CE skills: ce-context-fundamentals, ce-tool-design, ce-filesystem-context, ce-hosted-agents
- Frameworks: LangGraph, AutoGen, CrewAI multi-agent implementations
