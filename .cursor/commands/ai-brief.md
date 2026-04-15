---
description: "AI 브리핑 — MemKraft + LLM Wiki 기반 프로비넌스 태그 포함 아침 브리핑"
---

# AI Brief

Read and follow the `ai-brief` skill (`.cursor/skills/standalone/ai-brief/SKILL.md`).

## Usage

```
/ai-brief [--quick | --deep]
```

## Modes

| Flag | Behavior |
|------|----------|
| (none) | Full: Calendar + Email + MemKraft + Wiki |
| `--quick` | MemKraft unresolved + Calendar only |
| `--deep` | Full + gbrain/Cognee entity context |

## What It Does

Generates a provenance-tagged morning briefing combining:
- **MemKraft** (personal memory): recent decisions, preferences, unresolved items
- **LLM Wiki** (official knowledge): relevant policies, team knowledge
- **Calendar**: today's schedule
- **Email**: urgent/important items

Every piece of information carries a source tag (`[COMPANY]`, `[RECENT]`, `[PREFERENCE]`, etc.) so you can distinguish personal context from organizational fact.

## Examples

```
/ai-brief
/ai-brief --quick
/ai-brief --deep
```
