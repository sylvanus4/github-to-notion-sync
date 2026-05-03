# Agent Token Strategy

## Model Routing

| Tier | When | Cost |
|------|------|------|
| `haiku` | Subagent exploration, file reading, simple lookups, grep tasks | ~1x |
| `sonnet` | Day-to-day coding, reviews, test writing, implementation | ~4x |
| `opus` | Complex architecture, multi-step reasoning, debugging subtle issues | ~19x |

- Default to cheapest tier that meets task needs
- Use `model: "haiku"` for Agent tool subagents doing exploration/file reading
- Only escalate to Opus for multi-step reasoning or architectural decisions

## Context Window Hygiene

- Prefer Agent tool for exploration -- read many files, return only summary, keep main context clean
- Avoid reading large files (>1K lines) in main context -- use Grep or read specific line ranges
- Write long outputs to scratch files, return summary + path to main context

## Scratch-File Offloading

When tool output >200 lines or generating long-form content:
1. Write full output to `/tmp/scratch-{task}.md`
2. Return only short summary + file path
3. Read scratch file back only if specific sections needed

## Subagent Cost Control

- Exploration tasks: use `model: "haiku"` in Agent tool
- Implementation tasks: use default model
- One focused task per subagent
- Include explicit return instructions ("return only: X, Y, Z")

### Spawn Depth Rules

- Max spawn depth: 2 (parent -> subagent -> one more tier)
- Haiku subagents NEVER spawn further subagents (if it needs to, task was wrong-sized)
- If a subagent realizes it needs a smarter model, return to parent -- never self-escalate

## Preferred Tools (cheapest first)

- WebFetch for public pages (free, text-only)
- agent-browser CLI for dynamic pages or auth walls (fewer tokens than screenshot tools)
- pdftotext for PDFs instead of Read tool
- When a fetch pattern repeats 3+ times, wrap as reusable tool

## Context Mode (SQLite/File Sandboxing)

When tool calls return structured data (JSON, tables, logs):
- Write raw output to `/tmp/ctx-{task-id}.json` or `.sqlite`
- Return only schema + row count + sample to main context
- Query the file for specific fields when needed
This prevents large API/DB responses from flooding the context window.

## Prompt Cache Preservation

- NEVER add or remove tools mid-session
- Use messages to convey updates instead of modifying system prompt
- Mid-session writes to MEMORY.md persist to disk but do NOT update in-context copy
- Monitor cache hit rate -- treat cache breaks as incidents
- Place stable content (system prompt, tools) at beginning, dynamic content at end
- Avoid timestamps or volatile data in system prompt
