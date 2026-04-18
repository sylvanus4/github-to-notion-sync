## Context Optimize

Diagnose per-turn token consumption and recommend optimizations to reduce context size and costs.

### Usage

```
/context-optimize                      # full token usage diagnosis
/context-optimize --rules              # focus on rules overhead
/context-optimize --skills             # focus on skill descriptions
/context-optimize --mcp                # focus on MCP server schemas
```

### Workflow

1. **Measure** — Calculate token usage from rules, AGENTS.md, MEMORY.md, MCP schemas, and skill descriptions
2. **Rank** — Sort by token cost: which sources consume the most
3. **Recommend** — Suggest specific optimizations (compression, removal, lazy loading)
4. **Estimate savings** — Project token and cost reduction per recommendation
5. **Report** — Token budget breakdown with actionable optimization plan

### Execution

Read and follow the `token-diet` skill (`.cursor/skills/standalone/token-diet/SKILL.md`) for token measurement, cost analysis, and optimization recommendations.

### Examples

Full token diagnosis:
```
/context-optimize
```

Focus on MCP overhead:
```
/context-optimize --mcp
```
