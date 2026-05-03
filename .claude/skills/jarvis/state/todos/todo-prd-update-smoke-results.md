---
id: prd-update-smoke-results
title: Update PRD v2 verification report with NVFP4 smoke 실측값
status: open
priority: P2
estimated_cost_usd: 0.00
estimated_time: 30min
related_todos: [vllm-deep-gemm, full-ptq-qwen3]
related_skills: [doc-updater-expert]
related_goals: []
source: output/serverless-prd/thakicloud-serverless-prd-v2.md
tags: [docs, prd, verification, smoke, nvfp4]
created_at: 2026-05-02
updated_at: 2026-05-02
---

# Update PRD v2 verification report with NVFP4 smoke 실측값

## Context

`output/serverless-prd/thakicloud-serverless-prd-v2.md`와 `docs/planned/serverless-pricing/serverless-inference-pricing-unified.md`에 NVFP4 양자화 워크플로 가정 (시간/비용/도구체인)이 들어있는데, 2026-05-01 스모크에서 실제로 검증된 수치로 업데이트해야 함.

또한 `docs/planned/serverless-pricing/nvfp4-quantization-reference.md`도 Qwen3-30B-A3B 실측 절차로 보강 가능.

## Acceptance criteria

- [ ] PRD v2 (`thakicloud-serverless-prd-v2.md`) 양자화 섹션에 다음 실측값 반영:
   - ModelOpt v0.43.0이 Qwen3-MoE를 native 지원 (auto-register `_QuantSparseMoe`, `_QuantAttention`)
   - Trace gate 23초, PTQ smoke (8 calib × full layers) 60초 on 1× B200
   - 출력 17.1GB (60GB BF16 → 3.5x 압축, group_size=16 W4A4)
   - 56,211 quantizers inserted across 48 layers + 128 experts
- [ ] `serverless-inference-pricing-unified.md` 비용 표에 RunPod B200 ondemand $5.49/hr column 추가 (Thaki 자체 $3.50/hr와 비교)
- [ ] `nvfp4-quantization-reference.md`에 다음 추가:
   - tokenizer 별도 저장 caveat
   - PEP 668 (Ubuntu 24.04) `--break-system-packages` 필수
   - vLLM `deep_gemm` 의존성 (smoke에서 별도 설치 필요)
   - 검증된 image: `runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404` (template `runpod-torch-v280`)
   - NGC `nvcr.io/nvidia/pytorch:25.02-py3` 회피 (US-CA-2에서 pull 행)
- [ ] 모든 변경에 `[validated 2026-05-01]` 또는 유사 마커 추가 (실측 vs 추정 구분)

## Notes / Implementation hint

소스: `output/qwen3-nvfp4-smoke/REPORT.md` 섹션 4-5 (단계별 실측 + 발견 버그 7개)

순서:
1. `nvfp4-quantization-reference.md` 먼저 — most-detailed reference
2. `serverless-inference-pricing-unified.md` cost table 갱신
3. `thakicloud-serverless-prd-v2.md` 양자화 paragraph 갱신
4. PRD verification 체크리스트 ([] → [x]) 표시 가능 부분 표시 (스모크가 닫은 게이트)

위험:
- PRD v2 검증 게이트는 full PTQ 결과로 채워야 하는 것이 많음 — 스모크는 [[full-ptq-qwen3]] 선행 조건 검증만. 헷갈리지 않게 "smoke validates pipeline; full PTQ validates quality" 명시
- 비용 컬럼 추가 시 Thaki 자체 $3.50/hr 비교 — 운영 시 RunPod 임대 vs 자체 fleet 결정 dependency, 별도 의사결정 필요할 수 있음 (PRD owner 확인)

체크포인트: 5+ 파일 변경 가능성 → 시작 전 `git stash` 또는 `hermes-checkpoint-rollback`

## History

- 2026-05-02 00:20 — created (source: REPORT.md §6 후속 작업)
