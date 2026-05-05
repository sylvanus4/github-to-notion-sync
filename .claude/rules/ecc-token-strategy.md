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

- **2K token rule**: any tool call expected to return >2K tokens -> delegate to subagent. Subagent reads, processes, returns summary only. Main context stays clean.
- Prefer Agent tool for exploration -- read many files, return only summary
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

## Context Mode (MCP/Tool Output Sandboxing)

MCP tool responses are the largest hidden context cost. Playwright page reads, GitHub API, browser tools, and any external MCP server can dump thousands of tokens per call.

**Auto-sandbox rule**: when ANY tool call returns >200 lines or >2KB of structured data:
1. Write raw output to `/tmp/ctx-{task-id}.json` or `.sqlite`
2. Return only schema + row count + sample to main context
3. Query the file for specific fields when needed

**MCP-specific targets** (highest token waste):

| MCP Tool | Sandbox Strategy |
|----------|-----------------|
| Playwright (page content) | Save HTML/text to `/tmp/ctx-playwright-*.txt`, return page title + key elements only |
| GitHub API (PR diff, issues) | Save full response to `/tmp/ctx-gh-*.json`, return summary counts + key fields |
| Browser tools (screenshots, DOM) | Save to file, return description + relevant selectors |
| Notion/Slack (thread reads) | Save full thread to file, return message count + key quotes |
| Any MCP returning >50 items | Save to SQLite, return COUNT + sample 3 rows |

**Never** dump raw MCP responses into main context. Sandbox first, summarize second.

## Prompt Caching

Prompt caching = free cost reduction. Claude Code enables it automatically, but you must not break it.

**Cache-breaking actions** (avoid these mid-session):
- Adding or removing tools/MCP servers
- Modifying system prompt or CLAUDE.md
- Writing to MEMORY.md (persists to disk but does NOT update in-context copy)

**Cache-preserving hygiene**:
- Place stable content (system prompt, tools) at beginning, dynamic content at end
- Monitor cache hit rate -- treat cache breaks as incidents
- Avoid timestamps or volatile data in system prompt
- Use messages to convey updates instead of modifying system prompt
