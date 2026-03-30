---
name: ce-context-engineering-index
description: >-
  Index and navigation hub for the Context Engineering skill collection — 13
  specialized skills covering fundamentals, degradation, compression, optimization,
  multi-agent patterns, memory systems, tool design, filesystem context, hosted
  agents, evaluation, advanced evaluation, project development, and BDI mental
  states. Use when the user asks to "list context engineering skills", "which CE
  skill should I use", "context engineering overview", "navigate CE skills", or
  needs guidance on which context engineering skill applies to their task. Do NOT
  use for individual skill execution (invoke the specific ce-* skill directly).
  Do NOT use for general skill discovery (use skill-guide).
  Korean triggers: "컨텍스트 엔지니어링 목록", "CE 스킬 가이드", "컨텍스트 스킬 인덱스",
  "CE 스킬 어떤 거 써야 해".
metadata:
  upstream: "muratcankoylan/Agent-Skills-for-Context-Engineering"
  author: "Agent Skills for Context Engineering Contributors"
  version: "2.0.0"
  license: MIT
  category: knowledge
---

# Context Engineering Skills Collection

This is the index for the Context Engineering (CE) skill collection, converted from [Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering). These skills provide comprehensive knowledge about designing, optimizing, and evaluating context management for AI agent systems.

## Skill Catalog

### Foundational (Understanding Context)

| Skill | When to Use |
|-------|-------------|
| `ce-context-fundamentals` | Understanding context windows, attention mechanics, progressive disclosure, budgeting |
| `ce-context-degradation` | Diagnosing and fixing lost-in-middle, poisoning, distraction, confusion, clash |
| `ce-context-compression` | Compressing sessions — anchored summarization, opaque compression, artifact trails |

### Architectural (Designing Systems)

| Skill | When to Use |
|-------|-------------|
| `ce-multi-agent-patterns` | Multi-agent coordination — supervisor, swarm, hierarchical, context isolation |
| `ce-memory-systems` | Agent memory — working/short/long-term, knowledge graphs, Mem0/Zep/Letta/Cognee |
| `ce-tool-design` | Designing agent-facing tools — consolidation, schemas, error messages, MCP |
| `ce-filesystem-context` | File-based context — scratch pads, plan persistence, dynamic skill loading |
| `ce-hosted-agents` | Hosted infrastructure — sandboxes, warm pools, self-spawning, multiplayer |

### Operational (Measuring & Optimizing)

| Skill | When to Use |
|-------|-------------|
| `ce-context-optimization` | KV-cache, observation masking, partitioning, budget management |
| `ce-evaluation` | Agent evaluation — rubrics, LLM-as-judge, test sets, continuous eval |
| `ce-advanced-evaluation` | LLM judge bias mitigation — position, length, self-enhancement, rubric generation |

### Methodology (Building Projects)

| Skill | When to Use |
|-------|-------------|
| `ce-project-development` | LLM project methodology — task-model fit, manual prototype, pipeline architecture |
| `ce-bdi-mental-states` | BDI cognitive modeling — beliefs, desires, intentions, LAG, T2B2T |

## Decision Tree

```
What's your context engineering challenge?
├── "I don't understand how context works"
│   → ce-context-fundamentals
├── "My agent is degrading / forgetting / confused"
│   → ce-context-degradation
├── "My context is too large / expensive"
│   ├── Compression strategies → ce-context-compression
│   └── Optimization techniques → ce-context-optimization
├── "I'm designing a multi-agent system"
│   → ce-multi-agent-patterns
├── "I need persistent memory across sessions"
│   → ce-memory-systems
├── "I'm designing tools for agents"
│   → ce-tool-design
├── "I want to use files for context overflow"
│   → ce-filesystem-context
├── "I'm building hosted/background agents"
│   → ce-hosted-agents
├── "How do I evaluate my agent?"
│   ├── General evaluation → ce-evaluation
│   └── LLM-as-judge bias → ce-advanced-evaluation
├── "I'm starting a new LLM project"
│   → ce-project-development
└── "I need formal agent reasoning"
    → ce-bdi-mental-states
```

## Relationship to Existing Skills

These CE skills are **knowledge skills** that teach principles. They complement but do not replace existing **execution skills**:

- Context compaction → `ecc-strategic-compact` (Cursor-specific)
- Context retrieval → `ecc-iterative-retrieval` (Cursor-specific)
- LLM evaluations → `evals-skills` (prompt/judge evaluation)
- Knowledge graphs → `cognee` (Cognee operations)
- Memory persistence → `recall` (cross-session recall)
- Multi-skill orchestration → `mission-control` (runtime execution)
- Prompt design → `prompt-architect` (framework-based optimization)

## Attribution

Upstream repository: [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)
License: MIT
