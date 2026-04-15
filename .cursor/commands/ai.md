---
description: "AI 개인 어시스턴트 — 자연어 의도를 적절한 ai-* 스킬로 라우팅"
---

# AI — Personal Assistant Meta-Router

Parse `$ARGUMENTS` as natural language and route to the appropriate `ai-*` skill.

## Routing Table

| Intent Pattern | Routes To | Skill File |
|---|---|---|
| Morning briefing, "오늘 뭐 해야 해", today's priorities | `ai-brief` | `.cursor/skills/standalone/ai-brief/SKILL.md` |
| "기억나?", "이전에 어떻게", recall, remember, what did I | `ai-recall` | `.cursor/skills/standalone/ai-recall/SKILL.md` |
| "어떻게 할까", decide, choose, which option, should I | `ai-decide` | `.cursor/skills/standalone/ai-decide/SKILL.md` |
| "이거 기억해", learn, remember this, store, save as policy | `ai-learn` | `.cursor/skills/standalone/ai-learn/SKILL.md` |
| "상태 확인", status, health, system check, freshness | `ai-status` | `.cursor/skills/standalone/ai-status/SKILL.md` |

## Your Task

User input: $ARGUMENTS

1. Classify the user's intent from `$ARGUMENTS`
2. If intent clearly maps to one skill → read and follow that skill's SKILL.md
3. If intent is ambiguous → ask the user to clarify with the available options above
4. If `$ARGUMENTS` is empty → show the routing table and ask for input

## Examples

```
/ai 오늘 브리핑 해줘                    → ai-brief
/ai 지난주 아키텍처 결정 뭐였지          → ai-recall
/ai 이번 릴리즈에 포함할지 말지 결정 도와줘  → ai-decide
/ai PR은 300줄 이하로 하는 걸 선호해      → ai-learn
/ai 시스템 상태 점검                     → ai-status
```
