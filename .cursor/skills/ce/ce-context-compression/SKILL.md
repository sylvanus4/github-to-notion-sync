---
name: ce-context-compression
description: >-
  Strategies for compressing agent context when sessions exhaust memory — anchored
  iterative summarization, opaque compression, regenerative summaries, artifact
  trail preservation, and probe-based evaluation. Use when the user asks to
  "compress context", "summarize conversation history", "implement compaction",
  "reduce token usage", or mentions context compression, structured summarization,
  tokens-per-task optimization, or long-running agent sessions exceeding context
  limits. Do NOT use for Cursor-specific context compaction (use ecc-strategic-compact).
  Do NOT use for general context optimization techniques (use ce-context-optimization).
  Do NOT use for memory system design (use ce-memory-systems or cognee).
  Korean triggers: "컨텍스트 압축", "대화 요약", "토큰 절감", "세션 압축",
  "컴팩션 전략".
metadata:
  upstream: "muratcankoylan/Agent-Skills-for-Context-Engineering/skills/context-compression"
  author: "Agent Skills for Context Engineering Contributors"
  version: "1.2.0"
  license: MIT
  category: knowledge
---

# Context Compression Strategies

When agent sessions generate millions of tokens of conversation history, compression becomes mandatory. The correct optimization target is tokens per task: total tokens consumed to complete a task, including re-fetching costs when compression loses critical information.

## Core Concepts

Select from three production-ready approaches:

1. **Anchored Iterative Summarization**: For long-running sessions where file tracking matters. Maintain structured persistent summaries with explicit sections. When compression triggers, summarize only the newly-truncated span and merge with the existing summary.

2. **Opaque Compression**: For short sessions where re-fetching costs are low. Produces compressed representations achieving 99%+ compression ratios but sacrificing interpretability.

3. **Regenerative Full Summary**: When summary readability is critical and sessions have clear phase boundaries.

### Artifact Trail Problem

Artifact trail integrity is the weakest dimension across all compression methods (scoring only 2.2-2.5 out of 5.0). Preserve these explicitly in every compression cycle:
- Which files were created (full paths)
- Which files were modified and what changed (include function names)
- Which files were read but not changed
- Specific identifiers: function names, variable names, error messages

### Compression Trigger Strategies

| Strategy | Trigger Point | Trade-off |
|----------|---------------|-----------|
| Fixed threshold | 70-80% context utilization | Simple but may compress too early |
| Sliding window | Keep last N turns + summary | Predictable context size |
| Importance-based | Compress low-relevance first | Complex but preserves signal |
| Task-boundary | Compress at logical completions | Clean summaries but unpredictable |

### Compression Quality Evaluation

Use probe-based evaluation rather than ROUGE or embedding similarity:

| Probe Type | What It Tests |
|------------|---------------|
| Recall | Factual retention |
| Artifact | File tracking |
| Continuation | Task planning |
| Decision | Reasoning chain |

## Cache-Safe Compression

When compression triggers a forked request (compaction call, subagent spawn), the fork
MUST share the parent conversation's prefix — system prompt, tool definitions, and
conversation history — to get cache hits on the shared portion. Append the compression
instruction as a final user message.

**Rules:**
- Same system prompt, user context, and tool definitions as the parent conversation
- Tool schemas must NEVER be compressed or stripped — they are part of the fixed cached prefix
- Artifact trails (file paths, function names, error signatures) should survive compression
  to maintain file-first pipeline compatibility
- Reserve a "compaction buffer" in the context window for the summary output tokens

This pattern prevents the most expensive mistake in compression: paying full price for
all input tokens that were previously cached. See `ecc-token-strategy.mdc` →
Prompt Cache Preservation and `ecc-strategic-compact` → Cache-Safe Forking for details.

## Examples

### Example 1: Compressing a 200k-token conversation
A multi-hour coding session has grown past the model’s effective capacity. Rather than truncating blindly, you trigger compression at a task boundary, preserve artifact trails (paths and edits), and keep probes to verify the summary still answers “what did we change and why.”

### Example 2: Anchored summarization vs regenerative summary
For ongoing work where file-level accuracy matters, anchored iterative summarization merges new spans into a structured running summary. When phases are discrete and readability matters more than diff fidelity, a regenerative full summary at phase end can replace a long tail of turns with one clean narrative.

## Troubleshooting

1. **Never compress tool definitions or schemas**: Compressing function call schemas destroys agent functionality.
2. **Compressed summaries hallucinate facts**: Validate compressed output against source material.
3. **Compression breaks artifact references**: Preserve identifiers verbatim in dedicated sections.
4. **Early turns contain irreplaceable constraints**: Protect early turns from compression.
5. **Aggressive ratios compound across cycles**: After three cycles at 95%, only 0.0125% of original tokens remain.
6. **Code and prose need different compression**: Summarize prose aggressively while preserving code blocks verbatim.

## References

- [Evaluation Framework Reference](./references/evaluation-framework.md)
- Related CE skills: ce-context-degradation, ce-context-optimization, ce-evaluation, ce-memory-systems
- Related rules: `ecc-token-strategy.mdc` (Prompt Cache Preservation), `ecc-strategic-compact` (Cache-Safe Forking)
- Research: Factory Research compression evaluation, Netflix "The Infinite Software Crisis"
