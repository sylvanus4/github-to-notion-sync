---
name: ce-context-optimization
description: >-
  Techniques to extend effective context capacity — KV-cache optimization,
  observation masking, context partitioning, budget management, and decision
  frameworks for choosing optimization strategies. Use when the user asks to
  "optimize context", "reduce token costs", "improve context efficiency",
  "implement KV-cache optimization", "partition context", or mentions context
  limits, observation masking, context budgeting, or extending effective context
  capacity. Do NOT use for context compression strategies (use ce-context-compression).
  Do NOT use for Cursor-specific context compaction (use ecc-strategic-compact).
  Do NOT use for token cost optimization in LLM API calls (use ecc-token-strategy
  rule). Do NOT use for context degradation diagnosis (use ce-context-degradation).
  Korean triggers: "컨텍스트 최적화", "KV 캐시", "관찰 마스킹", "컨텍스트 파티셔닝",
  "토큰 비용 절감".
metadata:
  upstream: "muratcankoylan/Agent-Skills-for-Context-Engineering/skills/context-optimization"
  author: "Agent Skills for Context Engineering Contributors"
  version: "1.1.0"
  license: MIT
  category: knowledge
---

# Context Optimization Techniques

Context optimization extends the effective capacity of an agent's context window without changing the model or the window size. The goal is to maximize task-relevant information density while minimizing wasted tokens.

## Core Concepts

### KV-Cache Optimization

The KV-cache stores the key-value pairs from attention computation. When the prefix of a prompt is stable across turns (system prompt, tool definitions), the cache can be reused, saving both compute and time.

**Rules for cache-friendly context design:**
- Place stable content (system prompt, tool schemas) at the beginning
- Place dynamic content (conversation history, tool results) at the end
- Avoid reordering existing context between turns
- The cache is prefix-based: any change invalidates everything after it

### Observation Masking

When tool outputs are large (multi-page documents, API responses), mask them after the turn in which they were processed. The agent has already extracted the relevant information into its reasoning; the raw output no longer contributes value.

```
Turn 5: [tool_result: 4000 tokens of JSON] → Agent extracts 3 key fields
Turn 6+: Replace with [tool_result: "3 fields extracted, see agent analysis above"]
```

### Context Partitioning

Divide context into functional zones with explicit boundaries:

| Zone | Content | Update Frequency |
|------|---------|-----------------|
| Identity | System prompt, persona | Never |
| Knowledge | Domain rules, schemas | Per-task |
| History | Conversation turns | Per-turn |
| Working | Current task state | Per-turn |

### Budget Management

Allocate token budgets per zone and enforce them:
- System prompt: 15-25% of context
- Tool definitions: 10-20%
- Conversation history: 30-40%
- Working memory: 20-30%

When a zone exceeds its budget, apply zone-specific compression (summarize history, prune old tool results, consolidate working notes).

### Decision Framework

| Symptom | Likely Cause | Optimization |
|---------|-------------|-------------|
| Increasing latency per turn | Context growth | Observation masking + history compression |
| Rising token costs | Context duplication | KV-cache alignment + deduplication |
| Agent forgets early instructions | Lost-in-middle | Context partitioning + anchoring |
| Tool misuse | Schema bloat | Tool consolidation + description reduction |

## Performance Targets

- System prompt cache hit rate: >95%
- Observation masking: reduce retained tool output by 70-90%
- Context partitioning: maintain zone budgets within ±10%
- Overall: 40-60% token reduction with <5% quality loss

## Examples

### Example 1: KV-cache optimization for multi-turn chat
Keep system prompt, tool schemas, and persona blocks as a stable prefix across turns so the provider can reuse KV-cache for that prefix. Append only new user turns and fresh tool results at the end, and avoid reordering earlier blocks so you do not invalidate the cached prefix.

### Example 2: Observation masking in tool-heavy agents
After a large API or document response is summarized into the assistant message, replace the raw tool payload in subsequent turns with a short pointer (e.g., extracted fields plus a one-line reference). This preserves reasoning continuity while stopping megatoken JSON from living forever in context.

## Troubleshooting

1. **Over-optimization**: Removing too much context causes agent quality to degrade silently.
2. **Cache invalidation surprise**: Any prefix change invalidates the entire downstream cache.
3. **Masking too early**: Mask observations only after the agent has finished reasoning about them.
4. **Fixed budgets on variable tasks**: Adjust zone budgets dynamically based on task complexity.
5. **Measuring tokens, not quality**: Optimize for task success rate, not minimum token count.

## References

- [Optimization Techniques Reference](./references/optimization_techniques.md)
- Related CE skills: ce-context-fundamentals, ce-context-compression, ce-context-degradation
