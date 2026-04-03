---
description: "Compile raw sources into a structured markdown wiki with concepts, cross-references, and indexes"
---

# KB Compile

## Skill Reference

Read and follow the skill at `.cursor/skills/knowledge-base/kb-compile/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Compile the wiki for a Knowledge Base topic. `$ARGUMENTS` should contain:

1. **Topic name** — the KB topic to compile (e.g., `transformer-architectures`)
2. **Flags** (optional):
   - `--full` — full recompile (default for first compile)
   - `--incremental` — only process new/changed raw sources

If topic is missing, list available KBs and ask which to compile.
