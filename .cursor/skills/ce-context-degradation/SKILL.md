---
name: ce-context-degradation
description: >-
  Patterns for recognizing and mitigating context failures in AI agent systems —
  lost-in-middle, context poisoning, distraction, confusion, and clash. Use when
  the user asks to "diagnose context problems", "fix lost-in-middle issues",
  "debug agent failures", "understand context poisoning", or mentions context
  degradation, attention patterns, context clash, context confusion, or agent
  performance degradation. Do NOT use for context compression strategies (use
  ce-context-compression). Do NOT use for Cursor-specific context compaction
  (use ecc-strategic-compact). Do NOT use for general bug diagnosis (use diagnose).
  Korean triggers: "컨텍스트 저하", "로스트 인 미들", "컨텍스트 포이즌", "어텐션 패턴",
  "에이전트 성능 저하".
metadata:
  upstream: "muratcankoylan/Agent-Skills-for-Context-Engineering/skills/context-degradation"
  author: "Agent Skills for Context Engineering Contributors"
  version: "2.0.0"
  license: MIT
  category: knowledge
---

# Context Degradation Patterns

Diagnose and fix context failures before they cascade. Context degradation is not binary — it is a continuum that manifests through five distinct, predictable patterns: lost-in-middle, poisoning, distraction, confusion, and clash.

## Core Concepts

Structure context placement around the attention U-curve: beginning and end positions receive reliable attention, while middle positions suffer 10-40% reduced recall accuracy (Liu et al., 2023).

### Five Degradation Patterns

1. **Lost-in-Middle**: Information in the center of context receives less attention. Place critical information at the beginning and end.
2. **Context Poisoning**: Once a hallucination or tool error enters context, it compounds through repeated self-reference. Detection requires tracking claim provenance.
3. **Context Distraction**: Even a single irrelevant document measurably degrades performance — the effect follows a step function, not a linear curve.
4. **Context Confusion**: When context contains multiple task types, models incorporate constraints from the wrong task. Segment different tasks into separate context windows.
5. **Context Clash**: Multiple correct-but-contradictory sources appear in context. Establish source priority rules before conflicts arise.

## The Four-Bucket Mitigation Framework

- **Write** — Save context outside the window using scratchpads or file systems. Use when context utilization exceeds 70%.
- **Select** — Pull only relevant context into the window through retrieval and filtering.
- **Compress** — Reduce tokens while preserving information through summarization and observation masking.
- **Isolate** — Split context across sub-agents or sessions to prevent any single context from growing past its degradation threshold.

## Counterintuitive Findings

- Shuffled context can outperform coherent context for retrieval tasks
- Single distractors have outsized impact compared to adding more distractors
- Low needle-question similarity accelerates degradation

## Examples

### Example 1: Lost-in-the-middle in large contexts
A long agent trace buries the user’s safety constraints and the latest error message in the middle of the window. The model answers as if those details were never seen. This skill applies by explaining the attention U-curve and moving critical facts to the start or end of context, or splitting work so no single window is overloaded.

### Example 2: Context poisoning from bad tool outputs
A tool returns a plausible but wrong API shape; the assistant cites it in the next turn and downstream reasoning compounds the error. Treating that as degradation means tracking provenance, stripping or correcting bad observations before they re-enter, and isolating tasks so one wrong blob doesn’t dominate the session.

## Troubleshooting

1. **Normal variance looks like degradation**: Establish a baseline over multiple runs before diagnosing.
2. **Model-specific thresholds go stale**: Re-benchmark quarterly and after any major model update.
3. **Needle-in-haystack scores create false confidence**: Use task-specific benchmarks that mirror actual workload patterns.
4. **Contradictory retrieved documents poison silently**: Implement contradiction detection in the retrieval layer.
5. **Prompt quality problems masquerade as degradation**: Verify the same prompt works at low context lengths first.
6. **Degradation is non-linear with a cliff edge**: Set compaction triggers well before the cliff (at 70% of known onset).

## References

- [Degradation Patterns Reference](./references/patterns.md)
- Related CE skills: ce-context-fundamentals, ce-context-optimization, ce-evaluation
- Research: Liu et al., 2023 "Lost in the Middle", RULER benchmark
