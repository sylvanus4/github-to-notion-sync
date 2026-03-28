---
name: ce-tool-design
description: >-
  Principles for designing agent-facing tools as unambiguous contracts — the
  consolidation principle, architectural reduction, description engineering,
  response format optimization, error message design, and MCP naming. Use when
  the user asks to "design agent tools", "improve tool descriptions", "reduce
  tool count", "optimize tool schemas", or mentions tool design for agents,
  consolidation principle, architectural reduction, MCP tools, or tool-agent
  interfaces. Do NOT use for building MCP servers (use anthropic-mcp-builder).
  Do NOT use for general API design (use backend-expert). Do NOT use for
  Cursor-specific tool guidance (follow the tool_calling instructions).
  Korean triggers: "에이전트 도구 설계", "도구 통합", "도구 스키마", "MCP 도구",
  "아키텍처 축소".
metadata:
  upstream: "muratcankoylan/Agent-Skills-for-Context-Engineering/skills/tool-design"
  author: "Agent Skills for Context Engineering Contributors"
  version: "2.0.0"
  license: MIT
  category: knowledge
---

# Tool Design for Agents

Tools are contracts between deterministic systems and non-deterministic agents. Unlike human-facing APIs where documentation supplements understanding, agent-facing tools must be self-describing — the description is the only documentation the agent will ever read.

## Core Concepts

### The Consolidation Principle

Prefer single comprehensive tools over multiple narrow tools. Each tool added to an agent's context increases selection complexity and consumes tokens for its schema definition. Consolidate related operations under one tool with a parameter for the operation type.

**Before** (17 tools): `list_tables`, `get_schema`, `run_query`, `validate_sql`, ...
**After** (2 tools): `bash` (run any command), `sql` (execute any query)

### Architectural Reduction

Favor primitive, general-purpose tools (filesystem access, shell execution) over custom specialized tools — when the underlying data layer is well-documented and consistently structured, the model often performs better with fewer but more powerful tools.

### Tool Description Engineering

Every tool description must answer:
- **What** it does (in one sentence)
- **When** to use it (trigger conditions)
- **What inputs** it needs (typed parameters with descriptions)
- **What it returns** (output format and content)

### Error Message Design for Agents

Error messages must help agents self-correct. Include: what went wrong, why it failed, how to fix it, and a concrete example of correct usage.

```
Error: Invalid date format "2024-1-5"
Expected: ISO 8601 format (YYYY-MM-DD)
Fix: Use "2024-01-05"
Example: tool_call(date="2024-01-05")
```

### MCP Tool Naming

When tools are served via MCP, the pattern `ServerName:tool_name` creates automatic namespacing. Use snake_case for tool names, prefix with the domain, and keep names descriptive but concise.

## Examples

### Example 1: Consolidating five search tools into one
You expose multiple narrow search tools that overlap in purpose and inflate schema tokens. This skill supports merging them into a single `search` tool with a `scope` or `mode` parameter, one response shape, and a description that states when to use each mode so selection error drops.

### Example 2: Designing error messages agents can act on
Failures that only say "bad request" cause retry loops. This skill guides errors that state what failed, the expected format, how to fix it, and a minimal valid example so the agent can correct parameters without human help.

## Troubleshooting

1. **Vague descriptions cause tool misuse**: "Handles data" tells the agent nothing. Be specific.
2. **Cryptic parameter names**: `q` instead of `search_query` forces the agent to guess.
3. **Missing error recovery guidance**: The agent retries the same failed call in a loop.
4. **Tool schema token bloat**: JSON tool definitions inflate 2-3x compared to equivalent text. Audit token counts.
5. **Inconsistent naming across collections**: Mix of camelCase and snake_case breaks agent pattern recognition.
6. **Overloaded tools without clear mode selection**: A tool that does 10 things but does not explain when to use which mode.

## References

- [Architectural Reduction Reference](./references/architectural_reduction.md)
- [Best Practices Reference](./references/best_practices.md)
- Related CE skills: ce-context-fundamentals, ce-multi-agent-patterns, ce-hosted-agents
- Examples: Vercel d0 reduction from 17 to 2 tools, MCP specification
