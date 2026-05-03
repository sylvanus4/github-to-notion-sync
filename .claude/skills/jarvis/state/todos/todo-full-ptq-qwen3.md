---
id: full-ptq-qwen3
title: Run production-grade NVFP4 PTQ on Qwen3-30B-A3B
status: open
priority: P2
estimated_cost_usd: 17.00
estimated_time: 3h
related_todos: [vllm-deep-gemm, prd-update-smoke-results]
related_skills: [runpod-nvfp4-quantize]
related_goals: []
source: docs/planned/serverless-pricing/serverless-inference-pricing-unified.md
tags: [ptq, full, qwen3, moe, hf-hub, production]
created_at: 2026-05-02
updated_at: 2026-05-02
---

# Run production-grade NVFP4 PTQ on Qwen3-30B-A3B

## Context

[[vllm-deep-gemm]]가 닫히면 [[runpod-nvfp4-quantize]] 스킬이 풀-스케일 PTQ를 위한 검증된 도구가 된다. 그 다음 단계로 **production-grade** 양자화: 8.6K calibration set (Thaki 권장 — 다국어/JSON/tool-call/long-context 혼합) × 전 layer.

산출물은 ThakiCloud serverless inference 라인업의 첫 NVFP4 운영 모델이 됨 (PRD v2 검증 게이트 채우기).

**선행 조건**: [[vllm-deep-gemm]] 완료 (S7 게이트 닫혀야 production 검증 가능).

## Acceptance criteria

- [ ] 8.6K calibration set 준비 (Thaki 권장 분포: KO 1500 + EN 1500 + tool-call 1000 + math 500 + code 1500 + long-context 500 + safety 300 + summarization 300 + multilingual 2000)
   - 일부 공개셋 + 일부 internal — Thaki 데이터 풀 접근 권한 확인 필요
- [ ] 1× B200 (또는 4× TP for 시간 단축)에서 full PTQ 완료
   - check_cmd: `python3 -c "import json; d=json.load(open('artifact/smoke_meta.json')); assert d['max_samples']>=8000"`
- [ ] 가중치 17 ± 1 GB (BF16 60GB → 3.5x 압축 비율 유지)
- [ ] Quality bench: BF16 baseline 대비
   - MMLU-Pro (200문항 subset): −1%p 이내
   - HumanEval (50문항): −1-2%p 이내
   - GSM8K/MATH (50문항): −1%p 이내
   - JSON validity (300 prompt): ≥99%
   - Tool-call schema exact match: BF16 parity
   - Korean technical QA (100문항): BF16 parity
- [ ] `ThakiCloud/Qwen3-30B-A3B-NVFP4` (smoke와 별도 repo) HF Hub private 생성 + 풀 가중치 push
- [ ] vLLM `--quantization modelopt_fp4` 정상 로딩 + 단발 추론
- [ ] `output/qwen3-nvfp4-prod/REPORT.md` 작성 (smoke REPORT.md 형식 준용)

## Notes / Implementation hint

비용 시나리오:
| 옵션 | GPU | wall-clock | 비용 |
|------|-----|-----------|------|
| 1× B200 ondemand | 1× | 3h | $16.47 |
| 4× B200 TP=4 (병렬) | 4× | 1h | $21.96 |
| 1× B200 spot (CLI 미지원, manual bid) | 1× | 3-4h | $10-12 (preempt 위험) |

권장: 1× B200 ondemand (preempt 없음, 시간 단축 가치 < spot 절감). 만약 [[runpod-nvfp4-quantize]] 스킬 v1.1에 `MODE=full` 분기 추가되면 4× TP=4 시도 가치 있음.

위험:
- 8.6K calibration이 single B200 메모리에 한꺼번에 안 들어갈 수 있음 — micro-batch 처리 필요
- ModelOpt PTQ가 8.6K × 1 forward = 약 30-60분 calibration 단계만, 그 후 quantize+export
- 품질 게이트 실패 시 calibration 분포 재조정 후 재실행 ($16 추가 비용 위험)

선행 작업:
1. [[vllm-deep-gemm]] 완료 (vLLM 검증 가능)
2. Calibration 8.6K 큐레이션 (별도 sub-task: `prepare-calib-8k`)
3. 4× B200 옵션이면 MODE=full 분기 [[runpod-nvfp4-quantize]] 스킬에 추가

## History

- 2026-05-02 00:20 — created (source: smoke 후속 plan, REPORT.md §6)
