# Token Diet Hygiene

## Before Adding a Rule
- Does this truly need to be in EVERY turn? If not, make it a skill instead
- Is the rule < 2 KB? Split or trim if larger
- Does an existing rule already cover this? Check for overlap first

## MCP Server Hygiene
- Target: 10 or fewer enabled MCP servers per project (each adds ~1000 tokens of schema)
- Disable unused MCP servers in project config

## Ghost Token Detection
Ghost tokens = invisible per-turn overhead from loaded-but-unused sources.
- Unused MCP server schemas: each adds ~1000 tokens even if never called
- Overly verbose skill descriptions in YAML frontmatter (target: <512 chars)
- Duplicate rules across CLAUDE.md and .claude/rules/ files
- MEMORY.md entries that no longer apply (stale project state)
- Always-applied rules that could be skills (loaded on demand instead)
Run `/token-diet` skill to measure actual per-turn overhead.

## Session Cost Awareness
- Use `model: "haiku"` for exploration subagents -- 10x cheaper
- Use `/clear` between unrelated tasks to reset context
- Prefix shell commands with `rtk` when available (60-90% output compression)
- At logical phase boundaries, consider context compaction
