---
description: "AI 학습 — 새 정보를 MemKraft 또는 LLM Wiki에 라우팅하여 저장"
---

# AI Learn

Read and follow the `ai-learn` skill (`.cursor/skills/standalone/ai-learn/SKILL.md`).

## Usage

```
/ai-learn <information> [--target <personal|team|company>] [--type <preference|decision|fact|policy|unresolved>] [--domain <domain>]
```

## What It Does

Classifies new information and routes it to the correct knowledge layer:
- **Personal** (preference, decision, fact) → MemKraft via `memkraft-ingest`
- **Team** (domain-specific practice) → Team Wiki via `wiki-team`
- **Company** (org-wide policy) → Company Wiki via `wiki-company` (requires approval)

Performs deduplication check before storing and confirms with provenance tag.

User input: $ARGUMENTS

## Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--target` | auto | Force target layer |
| `--type` | auto | Content type classification |
| `--domain` | auto | Team domain for team-tier routing |

## Examples

```
/ai-learn 나는 코드 리뷰 시 PR 크기를 300줄 이하로 선호한다
/ai-learn --target team --domain engineering Go 서비스는 반드시 health check 엔드포인트를 포함해야 한다
/ai-learn --target company 모든 프로덕션 배포는 수요일 QA를 통과해야 한다
/ai-learn --type unresolved vLLM 멀티노드 배포 시 NCCL 타임아웃 이슈 확인 필요
```
