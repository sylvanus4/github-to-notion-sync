---
description: "LLM Knowledge Base — create, build, query, enhance, and manage personal knowledge bases"
---

# Knowledge Base

## Skill Reference

Read and follow the skill at `.cursor/skills/knowledge-base/kb-orchestrator/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Orchestrate the LLM Knowledge Base system. Parse `$ARGUMENTS` to determine the mode:

| Input | Mode | Description |
|---|---|---|
| `init {topic}` | init | Create a new KB with directory structure |
| `build {topic} [urls...]` | build | Ingest sources + compile wiki |
| `add {topic} {url/path}` | add | Quick-add single source + incremental compile |
| `query {topic} {question}` | query | Research and answer from KB |
| `enhance {topic}` | enhance | Lint + fix + recompile |
| `status {topic}` | status | Show KB overview and stats |
| `full {topic} [urls...]` | full-pipeline | End-to-end pipeline |
| `list` | list | List all existing knowledge bases |
| (no args) | interactive | Ask the user what they want to do |

If `$ARGUMENTS` is empty or unclear, ask the user to specify the topic and mode.

All output should be in the user's preferred language.
