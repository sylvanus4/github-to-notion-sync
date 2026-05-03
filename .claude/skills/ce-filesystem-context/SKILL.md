---
name: ce-filesystem-context
description: >-
  Filesystem-based context engineering patterns — scratch pads, plan
  persistence, sub-agent file workspaces, dynamic skill loading, terminal log
  persistence, and agent self-modification. Use when the user asks to "offload
  context to files", "implement dynamic context discovery", "use filesystem
  for agent memory", "reduce context window bloat", or mentions file-based
  context management, tool output persistence, agent scratch pads, or
  just-in-time context loading. Do NOT use for Cursor-specific iterative
  retrieval (use ecc-iterative-retrieval). Do NOT use for memory framework
  selection (use ce-memory-systems). Do NOT use for general context
  optimization (use ce-context-optimization). Korean triggers: "파일시스템 컨텍스트",
  "스크래치 패드", "동적 스킬 로딩", "에이전트 파일 메모리", "컨텍스트 오프로딩".
---

# Filesystem-Based Context Engineering

Use the filesystem as the primary overflow layer for agent context. Context windows are limited while tasks often require more information than fits in a single window. Files let agents store, retrieve, and update effectively unlimited context through a single interface.

## Core Concepts

### Four Context Failure Modes

1. **Missing context**: Persist tool outputs and intermediate results to files
2. **Under-retrieved context**: Structure files for targeted retrieval (grep-friendly formats)
3. **Over-retrieved context**: Offload bulk content; return compact references
4. **Buried context**: Combine glob and grep for structural search alongside semantic search

### Six Filesystem Patterns

1. **Scratch Pad**: Redirect large tool outputs (>2000 tokens) to files, returning compact summaries and file references
2. **Plan Persistence**: Write plans in structured format (YAML/JSON) for re-reading at each turn
3. **Sub-Agent Communication**: Route sub-agent findings through per-agent workspace directories
4. **Dynamic Skill Loading**: Store skills as files, include only names in static context, load full content on demand
5. **Terminal/Log Persistence**: Persist terminal output to searchable files
6. **Self-Modification**: Agents write learned preferences to their own instruction files

### Filesystem Search Techniques

- `ls`/`list_dir`: Discover directory structure
- `glob`: Find files matching patterns
- `grep`: Search file contents with context
- `read_file` with line ranges: Read specific sections without loading entire files

Use filesystem search for structural/exact-match queries; semantic search for conceptual queries.

## Examples

### Example 1: Scratchpads for multi-step reasoning
A research agent dumps large tool outputs to dated files under a scratch directory and keeps only short pointers in the chat. Each step reads the prior summary plus targeted file slices, so the active window stays small without losing where evidence lives.

### Example 2: Persisting plans across agent restarts
The main loop writes a YAML plan to disk after every milestone. When the session restarts with an empty history, the agent reloads that plan first, so goals and completed steps survive context loss without re-deriving everything from chat.

## Troubleshooting

1. **Scratch directory unbounded growth**: Implement retention policies at session boundaries.
2. **Race conditions in multi-agent file access**: Enforce per-agent directory isolation.
3. **Stale file references after moves/renames**: Always verify file existence before reading cached paths.
4. **Glob pattern false matches**: Scope globs to specific directories and extensions.
5. **File size assumptions**: Check file size before reading; use line-range reads for large files.
6. **Hardcoded absolute paths break in containers**: Use relative paths from project root.

## References

- [Implementation Patterns Reference](./references/implementation-patterns.md)
- Related CE skills: ce-context-optimization, ce-memory-systems, ce-multi-agent-patterns, ce-context-compression
