---
description: "AI 상태 — MemKraft + LLM Wiki 지식 시스템 건강 대시보드"
---

# AI Status

Read and follow the `ai-status` skill (`.cursor/skills/standalone/ai-status/SKILL.md`).

## Usage

```
/ai-status
```

## What It Does

Reports the health of the entire personal knowledge infrastructure:

- **MemKraft**: tier distribution (HOT/WARM/COLD), freshness scores, unresolved item count and age, preference coverage, Dream Cycle last run
- **LLM Wiki**: company/team topic counts, compilation coverage, average freshness
- **System Readiness Score**: 0-100 composite score with 🟢/🟡/🔴 status
- **Recommended Actions**: prioritized maintenance steps

## Readiness Thresholds

| Score | Status | Meaning |
|-------|--------|---------|
| 80-100 | 🟢 Healthy | System ready for reliable AI assistance |
| 50-79 | 🟡 Attention | Some maintenance needed |
| 0-49 | 🔴 Critical | Run Dream Cycle and Wiki compilation immediately |

## Examples

```
/ai-status
```
