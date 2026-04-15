---
description: "AI 의사결정 — 프로비넌스 분리 증거 기반 의사결정 지원"
---

# AI Decide

Read and follow the `ai-decide` skill (`.cursor/skills/standalone/ai-decide/SKILL.md`).

## Usage

```
/ai-decide <decision question>
```

## What It Does

Retrieves official policies (Wiki), past decisions and preferences (MemKraft), detects conflicts between personal history and official policy, generates 2-4 evidence-backed options, and applies the Karpathy Opposite Direction Test before recommending.

User input: $ARGUMENTS

## Output Includes

- **Official Knowledge**: relevant company/team policies with `[COMPANY]`/`[TEAM]` tags
- **Personal Context**: past decisions, preferences, unresolved items with `[RECENT]`/`[PREFERENCE]` tags
- **Conflict Analysis**: where personal context aligns with or diverges from policy
- **Options Table**: each option with evidence source and risk assessment
- **Counter-argument**: strongest argument against the recommendation

## Examples

```
/ai-decide 새 마이크로서비스를 Go로 할지 Python으로 할지
/ai-decide 이번 릴리즈에 이 기능을 포함할지
/ai-decide 채용 후보 A vs B 중 누구를 선택할지
```
