---
description: "AI 리콜 — MemKraft 우선 프로비넌스 태그 포함 기억 검색"
---

# AI Recall

Read and follow the `ai-recall` skill (`.cursor/skills/standalone/ai-recall/SKILL.md`).

## Usage

```
/ai-recall <query> [--personal-only] [--wiki-only] [--deep] [--time-range <24h|7d|30d|all>]
```

## What It Does

Searches personal memory (MemKraft) first, then official knowledge (LLM Wiki), merging results with provenance tags via weighted RRF. Answers "what did I decide?" separately from "what does the policy say?"

User input: $ARGUMENTS

## Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--personal-only` | false | MemKraft results only |
| `--wiki-only` | false | Wiki results only |
| `--deep` | false | Include gbrain/Cognee |
| `--time-range` | all | Filter by recency |

## Examples

```
/ai-recall 지난주 아키텍처 결정
/ai-recall --personal-only 내가 선호하는 배포 방식
/ai-recall --deep Company X 관련 정보
/ai-recall --time-range 7d 최근 미팅 결론
```
