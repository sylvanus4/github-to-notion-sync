---
name: ce-context-fundamentals
description: >-
  Foundational understanding of context engineering for AI agent systems —
  context windows, attention mechanics, progressive disclosure, and context
  budgeting. Use when the user asks to "understand context", "explain context
  windows", "design agent architecture", "debug context issues", "optimize
  context usage", or discusses context components, attention mechanics,
  progressive disclosure, context budgeting, token allocation, or context
  quality. Do NOT use for context compression techniques (use
  ce-context-compression). Do NOT use for context degradation diagnosis (use
  ce-context-degradation). Do NOT use for Cursor-specific context compaction
  (use ecc-strategic-compact). Do NOT use for iterative codebase retrieval
  (use ecc-iterative-retrieval). Korean triggers: "컨텍스트 엔지니어링", "컨텍스트 윈도우",
  "어텐션 메커니즘", "토큰 예산", "프로그레시브 디스클로저".
---

# Context Engineering Fundamentals

Context is the complete state available to a language model at inference time — system instructions, tool definitions, retrieved documents, message history, and tool outputs. Context engineering is the discipline of curating the smallest high-signal token set that maximizes the likelihood of desired outcomes.

## Core Concepts

Treat context as a finite attention budget, not a storage bin. Every token added competes for the model's attention and depletes a budget that cannot be refilled mid-inference. The engineering problem is maximizing utility per token against three constraints: the hard token limit, the softer effective-capacity ceiling (typically 60-70% of the advertised window), and the U-shaped attention curve that penalizes information placed in the middle of context.

Apply four principles when assembling context:

1. **Informativity over exhaustiveness** — include only what matters for the current decision; design systems that can retrieve additional information on demand.
2. **Position-aware placement** — place critical constraints at the beginning and end of context, where recall accuracy runs 85-95%; the middle drops to 76-82% (the "lost-in-the-middle" effect).
3. **Progressive disclosure** — load skill names and summaries at startup; load full content only when a skill activates for a specific task.
4. **Iterative curation** — context engineering is not a one-time prompt-writing exercise but an ongoing discipline applied every time content is passed to the model.

## Detailed Topics

### The Anatomy of Context

**System Prompts**: Organize into distinct sections using XML tags or Markdown headers. Calibrate instruction altitude to balance two failure modes — too-low hardcodes brittle logic; too-high provides vague guidance. Start minimal, then add instructions reactively based on observed failure modes.

**Tool Definitions**: Write descriptions that answer what the tool does, when to use it, and what it returns. Keep the tool set minimal — tool schemas typically inflate 2-3x compared to equivalent plain-text descriptions after JSON serialization.

**Retrieved Documents**: Maintain lightweight identifiers and load data dynamically using just-in-time retrieval. Strong identifiers (e.g., `customer_pricing_rates.json`) let agents locate relevant files without search tools.

**Message History**: Serves as the agent's scratchpad memory. For long-running tasks, it can grow to dominate context usage — monitor and apply compaction before it crowds out active instructions.

**Tool Outputs**: Typically dominate context — research shows observations can reach 83.9% of total tokens in agent trajectories. Apply observation masking: replace verbose outputs with compact references.

### Context Windows and Attention Mechanics

Design for the attention gradient: assume effective capacity is 60-70% of the advertised window. A 200K-token model starts degrading around 120-140K tokens.

Implement progressive disclosure at three levels:
1. **Skill selection** — load only names and descriptions at startup
2. **Document loading** — load summaries first; fetch detail sections only when needed
3. **Tool result retention** — keep recent results in full; compress or evict older results

### Context Quality Versus Quantity

Reject the assumption that larger context windows solve memory problems. Apply the signal-density test: for each piece of context, ask whether removing it would change the model's output. Redundant content actively dilutes attention from high-signal content.

## Practical Guidance

### Context Budgeting

Allocate explicit budgets per component and monitor during development. Implement compaction triggers at 70-80% utilization. For sub-agent architectures, enforce a compression ratio: a sub-agent may explore using tens of thousands of tokens but must return a condensed summary of 1,000-2,000 tokens.

### Hybrid Context Strategies

- **Low volatility** (project conventions): pre-load at session start
- **High volatility** (code state, external data): retrieve just-in-time

## Examples

**Example 1: Organizing System Prompts**
```markdown
<BACKGROUND_INFORMATION>
You are a Python expert helping a development team.
</BACKGROUND_INFORMATION>

<INSTRUCTIONS>
- Write clean, idiomatic Python code
- Include type hints for function signatures
</INSTRUCTIONS>

<TOOL_GUIDANCE>
Use bash for shell operations, python for code tasks.
</TOOL_GUIDANCE>
```

**Example 2: Progressive Document Loading**
```markdown
# Step 1: Load summary
docs/api_summary.md          # Lightweight overview

# Step 2: Load specific section as needed
docs/api/endpoints.md        # Only when API calls needed
```

## Troubleshooting

1. **Nominal window is not effective capacity**: Budget for 60-70% of the nominal window as usable capacity.
2. **Character-based token estimates silently drift**: Use the provider's actual tokenizer for budget-critical calculations.
3. **Tool schemas inflate 2-3x after JSON serialization**: Audit serialized tool token counts, not source-code line counts.
4. **Message history balloons silently in agentic loops**: Set a hard token ceiling on history and trigger compaction proactively.
5. **Critical instructions in the middle get lost**: Never place safety constraints or guardrails in the middle of a long system prompt.
6. **Progressive disclosure that loads too eagerly defeats its purpose**: Set strict activation thresholds.
7. **Mixing instruction altitudes causes inconsistent behavior**: Group instructions by altitude level.

## References

- [Context Components Reference](./references/context-components.md)
- Related CE skills: ce-context-degradation, ce-context-optimization, ce-multi-agent-patterns, ce-tool-design
- Research: Anthropic's "Effective Context Engineering for AI Agents", lost-in-the-middle effect research
