---
name: ce-memory-systems
description: >-
  Design and implementation of agent memory systems — working memory, short-term,
  long-term, entity memory, temporal knowledge graphs, and production frameworks
  (Mem0, Zep, Letta, LangMem, Cognee). Use when the user asks to "design agent
  memory", "implement persistent memory", "choose memory framework", "build
  knowledge graph for agents", or mentions agent memory layers, memory
  consolidation, retrieval strategies, or episodic/semantic memory. Do NOT use
  for Cognee operations directly (use cognee skill). Do NOT use for Cursor
  continuous learning instincts (use ecc-continuous-learning). Do NOT use for
  project-level context management (use context-engineer).
  Korean triggers: "에이전트 메모리", "지식 그래프", "메모리 프레임워크", "영구 메모리",
  "메모리 시스템 설계".
metadata:
  upstream: "muratcankoylan/Agent-Skills-for-Context-Engineering/skills/memory-systems"
  author: "Agent Skills for Context Engineering Contributors"
  version: "2.0.0"
  license: MIT
  category: knowledge
---

# Memory Systems for Agents

Memory systems extend agents beyond single-turn interactions by providing persistent, retrievable knowledge stores. The architecture spans from simple file-based scratch pads to sophisticated temporal knowledge graphs with automatic entity extraction.

## Core Concepts

### Memory Layers

| Layer | Persistence | Capacity | Access Pattern |
|-------|------------|----------|----------------|
| Working memory | Current turn | ~128K tokens | Immediate |
| Short-term memory | Current session | Limited by context | Turn-by-turn append |
| Long-term memory | Cross-session | Effectively unlimited | Search/retrieve |
| Entity memory | Cross-session | Per-entity records | Entity lookup |
| Temporal KG | Cross-session | Graph-structured | Temporal + semantic |

### Production Framework Comparison

| Framework | Architecture | Best For |
|-----------|-------------|----------|
| Mem0 | Graph-enhanced vector store | Personalization, user preferences |
| Zep/Graphiti | Temporal Knowledge Graph | Relationship-rich, evolving data |
| Letta | Tiered OS-inspired memory | Complex multi-step reasoning |
| LangMem | LangGraph-integrated | LangGraph pipelines |
| Cognee | Knowledge graph + RAG | Document ingestion, structured knowledge |
| File-system | Directory-based | Simple, transparent, debuggable |

### Retrieval Strategies

- **Semantic search**: Embedding similarity for conceptual queries
- **Entity-based search**: Direct entity lookup for known entities
- **Temporal search**: Time-windowed retrieval for recent events
- **Hybrid search**: Combine semantic + temporal + entity for comprehensive recall

### Memory Consolidation

Run consolidation periodically: merge duplicate facts, resolve contradictions, update confidence scores, and promote short-term memories to long-term. Design consolidation as an explicit pipeline step, not an implicit background process.

## Examples

### Example 1: Episodic memory for customer support context
Store per-ticket events (what was tried, what the user said, resolutions) as retrievable episodes so the agent can resume multi-day threads without replaying full transcripts. Pair episodic stores with entity memory for account IDs and order numbers.

### Example 2: Choosing between Mem0 and a knowledge graph
Prefer Mem0-style graph-enhanced vectors when personalization and fuzzy recall of user prefs dominate. Prefer a temporal knowledge graph (e.g., Zep/Graphiti, Cognee) when relationships and time-evolving facts are first-class and you need structured traversals, not just similarity search.

## Troubleshooting

1. **Memory without retrieval evaluation**: Storing memories is useless if retrieval quality is not measured.
2. **Unbounded memory growth**: Implement retention policies — not everything should be remembered forever.
3. **Memory poisoning**: Invalid memories corrupt downstream reasoning. Validate before storing.
4. **Retrieval latency in hot paths**: Memory lookups add latency; cache frequently accessed memories.
5. **Framework lock-in**: Abstract the memory interface so frameworks can be swapped.

## References

- [Memory Implementation Reference](./references/implementation.md)
- Related CE skills: ce-context-fundamentals, ce-filesystem-context, ce-evaluation
- Frameworks: Mem0, Zep/Graphiti, Letta, LangMem, Cognee
