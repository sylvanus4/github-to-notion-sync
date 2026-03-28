---
name: ce-bdi-mental-states
description: >-
  BDI (Beliefs-Desires-Intentions) mental state modeling for AI agents — formal
  ontology of agent cognition, cognitive chain patterns, world state grounding,
  goal-directed planning, and Logic Augmented Generation (LAG). Use when the user
  asks to "model agent beliefs", "implement BDI for agents", "design goal-directed
  agents", "build deliberative agents", or mentions BDI architecture, mental states,
  beliefs-desires-intentions, agent reasoning frameworks, or cognitive architectures
  for agents. Do NOT use for agent memory persistence (use ce-memory-systems). Do NOT
  use for multi-agent orchestration (use ce-multi-agent-patterns). Do NOT use for
  prompt architecture design (use prompt-architect).
  Korean triggers: "BDI 아키텍처", "에이전트 신념", "목표 지향 에이전트", "인지 체인",
  "로직 증강 생성".
metadata:
  upstream: "muratcankoylan/Agent-Skills-for-Context-Engineering/skills/bdi-mental-states"
  author: "Agent Skills for Context Engineering Contributors"
  version: "2.0.0"
  license: MIT
  category: knowledge
---

# BDI Mental State Modeling for Agents

BDI (Beliefs, Desires, Intentions) is a formal framework for modeling agent cognition. It provides a structured way to represent what an agent knows, what it wants, and what it has committed to doing — enabling more transparent, debuggable, and goal-directed agent behavior.

## Core Concepts

### The BDI Framework

| Component | Definition | Agent Equivalent |
|-----------|-----------|-----------------|
| Beliefs | What the agent thinks is true about the world | Context, retrieved facts, tool outputs |
| Desires | What the agent wants to achieve | User goals, system objectives, sub-goals |
| Intentions | What the agent has committed to doing | Current plan, active tool calls, queued actions |

### Mental Reality Architecture

**Endurants** (persistent entities):
- Agent identity and capabilities
- Domain knowledge and constraints
- User preferences and history

**Perdurants** (time-bound processes):
- Current conversation context
- Active plans and their progress
- Pending observations awaiting processing

### Cognitive Chain Pattern

Structure agent reasoning as an explicit cognitive chain:

```
Perceive → Believe → Desire → Intend → Act → Observe → Update Beliefs
```

Each step is traceable and inspectable:
1. **Perceive**: What new information arrived?
2. **Believe**: How does this update my model of the world?
3. **Desire**: Given updated beliefs, what do I want?
4. **Intend**: What plan will achieve my desires?
5. **Act**: Execute the next step of the plan
6. **Observe**: What was the result?
7. **Update**: Revise beliefs based on observations

### World State Grounding

Agents must maintain a grounded model of the current world state:
- Distinguish between **observed facts** (high confidence) and **inferred beliefs** (lower confidence)
- Track belief provenance: where did each belief come from?
- Handle belief revision: what happens when new evidence contradicts existing beliefs?
- Temporal decay: beliefs about dynamic states lose confidence over time

### Goal-Directed Planning

Transform desires into executable intentions:
- **Goal decomposition**: Break high-level desires into sub-goals
- **Plan selection**: Choose among alternative plans based on beliefs about feasibility
- **Intention persistence**: Maintain commitments unless there's good reason to reconsider
- **Replanning triggers**: Define conditions under which the agent should abandon or revise plans

### Logic Augmented Generation (LAG)

Combine LLM generation with formal logic:
- Use LLMs for natural language understanding and generation
- Use formal logic for constraint satisfaction and plan validation
- The LLM proposes, logic verifies, the LLM refines
- Enables guarantees that pure LLM generation cannot provide

### T2B2T Paradigm (Triples-to-Beliefs-to-Triples)

Bridge between knowledge graphs and mental states:
1. Extract triples from observations (subject-predicate-object)
2. Convert triples into structured beliefs with confidence scores
3. Reason over beliefs to form intentions
4. Express intentions as triples for execution
5. Update the knowledge graph with results

## Examples

### Example 1: Modeling agent beliefs from tool observations
After each tool call, you record observations as beliefs with provenance (which tool, which timestamp) instead of treating the model's free-text summary as truth. This skill shows how to revise beliefs when new evidence arrives and to avoid ungrounded belief drift.

### Example 2: Formal intention tracking for multi-step planning
A long-horizon task needs commitments to sub-steps (which API next, what success looks like). This skill frames desires as goals, intentions as executable commitments, and replanning triggers so you can inspect why the agent chose or abandoned a step.

## Troubleshooting

1. **Over-formalizing**: Not every agent needs full BDI. Simple reactive agents with clear rules often outperform.
2. **Belief explosion**: Tracking too many beliefs consumes context. Prune aggressively.
3. **Intention rigidity**: Agents that never reconsider plans miss opportunities.
4. **Grounding failure**: Beliefs not tied to observations drift from reality.
5. **Complexity vs. transparency**: The BDI overhead is only worth it if you actually inspect mental states for debugging.

## References

- [BDI Ontology Core Reference](./references/bdi-ontology-core.md)
- [Framework Integration Reference](./references/framework-integration.md)
- [RDF Examples Reference](./references/rdf-examples.md)
- [SPARQL Competency Reference](./references/sparql-competency.md)
- Related CE skills: ce-memory-systems, ce-multi-agent-patterns, ce-context-fundamentals
- Literature: Bratman (1987), Rao & Georgeff (1991), Jason/AgentSpeak
