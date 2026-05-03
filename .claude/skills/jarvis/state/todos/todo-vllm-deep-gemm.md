---
id: vllm-deep-gemm
title: Fix vLLM deep_gemm install — close S7 in NVFP4 smoke
status: open
priority: P1
estimated_cost_usd: 1.00
estimated_time: 15min
related_todos: [full-ptq-qwen3, prd-update-smoke-results]
related_skills: [runpod-nvfp4-quantize]
related_goals: []
source: output/qwen3-nvfp4-smoke/REPORT.md
tags: [smoke, vllm, nvfp4, runpod, deep-gemm, B200]
created_at: 2026-05-02
updated_at: 2026-05-02
---

# Fix vLLM deep_gemm install — close S7 in NVFP4 smoke

## Context

Qwen3-30B-A3B NVFP4 smoke (2026-05-01) PASSed S1–S6 + S8–S10 but S7 (vLLM 로딩) 실패:

```
RuntimeError: DeepGEMM backend is not available or outdated.
Please install or update the `deep_gemm` to a newer version to enable FP8 kernels.
```

vLLM 0.7+의 NVFP4 inference 경로가 `deep_gemm` (NVIDIA Blackwell SM100 FP8/FP4 kernels) 의존. RunPod template `runpod-torch-v280`에 미포함. 모델 아티팩트 자체는 유효함 (17GB safetensors, hf_quant_config.json 정상).

이 TODO는 스모크 게이트 100% 닫고 [[runpod-nvfp4-quantize]] 스킬을 v1.1로 확정.

## Acceptance criteria

- [ ] `python3 -m pip install --break-system-packages "deep-gemm"` 성공 (RunPod B200 + runpod-torch-v280)
   - check_cmd: `ssh ... 'python3 -c "import deep_gemm; print(deep_gemm.__version__)"' && echo OK`
- [ ] 또는 source 빌드 fallback: `pip install git+https://github.com/deepseek-ai/DeepGEMM.git`
- [ ] vLLM constructor가 `/workspace/output/nvfp4`를 에러 없이 로드
- [ ] vllm_sanity.py가 ≥1 token 생성 (텍스트 내용 무관, smoke는 부분 양자화)
- [ ] `runpod_bootstrap.sh`에 deep-gemm 설치 단계 추가 (vllm install 직전)
- [ ] [[runpod-nvfp4-quantize]] SKILL.md Known Issues 표에서 해당 항목 제거 또는 ✓ 표시
- [ ] `output/qwen3-nvfp4-smoke/REPORT.md`에 후속 실측 결과 append
- [ ] 스킬 frontmatter version 또는 lifecycle note에 v1.1 기록

## Notes / Implementation hint

```bash
# bootstrap.sh 패치 위치 (S5 vLLM install 직전):
echo "=== install deep_gemm (NVFP4 backend) ===" | tee "$LOG_DIR/05a-deep-gemm.log"
python3 -m pip install --break-system-packages --no-cache-dir --quiet \
    "deep-gemm" 2>&1 | tail -5 | tee -a "$LOG_DIR/05a-deep-gemm.log" \
    || python3 -m pip install --break-system-packages --no-cache-dir \
        git+https://github.com/deepseek-ai/DeepGEMM.git \
        2>&1 | tail -10 | tee -a "$LOG_DIR/05a-deep-gemm.log"
```

비용 통제:
- 별도 신규 PTQ run 불필요 — 기존 아티팩트가 HF Hub 또는 RunPod volume snapshot에 있으면 vLLM phase만 재실행
- 만약 아티팩트 없으면 짧은 smoke (8 calib × full) 다시 돌려야 함 — 약 5-10분 추가 ($0.46-0.92)

위험:
- `deep-gemm` PyPI 패키지명 정확하지 않을 수 있음 — `pip search deep-gemm` 확인 필요
- 소스 빌드 시 nvcc + CUDA dev tools 필요 (runpod-torch-v280에 포함되어 있어야 함)
- B200 SM100 wheel이 없으면 30+분 빌드 가능

## History

- 2026-05-02 00:20 — created (source: REPORT.md S7 failure)
