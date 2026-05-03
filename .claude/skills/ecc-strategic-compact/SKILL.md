---
name: ecc-strategic-compact
description: >-
  Suggests context compaction at logical workflow boundaries (after research,
  after debugging, before new phase) rather than arbitrary auto-compaction.
  Includes a decision guide for when to compact and what survives. Use when
  running long sessions, switching task phases, or approaching context limits.
  Do NOT use for short single-task sessions. Do NOT use for memory persistence
  (use recall or context-engineer). Korean triggers: "컨텍스트 압축", "컴팩션".
---

# Strategic Compact Skill

Suggests manual `/compact` at strategic points in your workflow rather than relying on arbitrary auto-compaction.

## When to Activate

- Running long sessions that approach context limits (200K+ tokens)
- Working on multi-phase tasks (research → plan → implement → test)
- Switching between unrelated tasks within the same session
- After completing a major milestone and starting new work
- When responses slow down or become less coherent (context pressure)

## Why Strategic Compaction?

Auto-compaction triggers at arbitrary points:
- Often mid-task, losing important context
- No awareness of logical task boundaries
- Can interrupt complex multi-step operations

Strategic compaction at logical boundaries:
- **After exploration, before execution** — Compact research context, keep implementation plan
- **After completing a milestone** — Fresh start for next phase
- **Before major context shifts** — Clear exploration context before different task

## How It Works

The `suggest-compact.js` script runs on PreToolUse (Edit/Write) and:

1. **Tracks tool calls** — Counts tool invocations in session
2. **Threshold detection** — Suggests at configurable threshold (default: 50 calls)
3. **Periodic reminders** — Reminds every 25 calls after threshold

## Hook Setup

Add to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [{ "type": "command", "command": "node ~/.claude/skills/strategic-compact/suggest-compact.js" }]
      },
      {
        "matcher": "Write",
        "hooks": [{ "type": "command", "command": "node ~/.claude/skills/strategic-compact/suggest-compact.js" }]
      }
    ]
  }
}
```

## Configuration

Environment variables:
- `COMPACT_THRESHOLD` — Tool calls before first suggestion (default: 50)

## Compaction Decision Guide

Use this table to decide when to compact:

| Phase Transition | Compact? | Why |
|-----------------|----------|-----|
| Research → Planning | Yes | Research context is bulky; plan is the distilled output |
| Planning → Implementation | Yes | Plan is in TodoWrite or a file; free up context for code |
| Implementation → Testing | Maybe | Keep if tests reference recent code; compact if switching focus |
| Debugging → Next feature | Yes | Debug traces pollute context for unrelated work |
| Mid-implementation | No | Losing variable names, file paths, and partial state is costly |
| After a failed approach | Yes | Clear the dead-end reasoning before trying a new approach |

## What Survives Compaction

Understanding what persists helps you compact with confidence:

| Persists | Lost |
|----------|------|
| CLAUDE.md instructions | Intermediate reasoning and analysis |
| TodoWrite task list | File contents you previously read |
| Memory files (`~/.claude/memory/`) | Multi-step conversation context |
| Git state (commits, branches) | Tool call history and counts |
| Files on disk | Nuanced user preferences stated verbally |

## Best Practices

1. **Compact after planning** — Once plan is finalized in TodoWrite, compact to start fresh
2. **Compact after debugging** — Clear error-resolution context before continuing
3. **Don't compact mid-implementation** — Preserve context for related changes
4. **Read the suggestion** — The hook tells you *when*, you decide *if*
5. **Write before compacting** — Save important context to files or memory before compacting
6. **Use `/compact` with a summary** — Add a custom message: `/compact Focus on implementing auth middleware next`

## Cache-Safe Forking

When compacting, the compaction request MUST use the identical system prompt,
tools, and conversation history prefix as the parent session. Only append the
compaction instruction as a final user message.

**Why:** The API caches by prefix match. If the compaction call uses a different
system prompt or omits tools, the entire cached prefix is invalidated — the user
pays full price for all input tokens that were previously cached.

**Rules:**
- Same system prompt, user context, tool definitions as the parent conversation
- Prepend the parent's conversation messages, append compaction prompt at the end
- Reserve a "compaction buffer" in the context window for the summary output tokens
- NEVER strip tool schemas from compaction requests — they are part of the cached prefix
- Artifact trails (file paths, function names, error signatures) should survive
  compaction to maintain file-first pipeline compatibility

This pattern also applies to subagent spawning — subagents that share the parent's
prefix get cache hits on the shared portion. See `ecc-token-strategy.mdc` for the
full cache preservation rules.

## Related

- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) — Token optimization section
- Memory persistence hooks — For state that survives compaction
- `continuous-learning` skill — Extracts patterns before session ends
- `ecc-token-strategy.mdc` — Prompt Cache Preservation section

## Examples

### Example 1: Applying the pattern

**User says:** "Running long sessions"

**Actions:**
1. Read and understand the current project context
2. Apply the strategic compact methodology as described in this skill
3. Report findings and recommendations
## Error Handling

| Issue | Resolution |
|-------|-----------|
| Unexpected input format | Validate input before processing; ask user for clarification |
| External service unavailable | Retry with exponential backoff; report failure if persistent |
| Output quality below threshold | Review inputs, adjust parameters, and re-run the workflow |
