# Jarvis TODO Index

Last updated: 2026-05-02 00:20 KST · 자동 생성 가능 (`jarvis todo reindex`) · 진실원은 개별 todo 파일

## Open (3)

| ID | P | Title | Cost | Time | Tags |
|----|---|-------|------|------|------|
| [vllm-deep-gemm](todo-vllm-deep-gemm.md) | P1 | Fix vLLM deep_gemm install — close S7 in NVFP4 smoke | $1.00 | 15min | smoke, vllm, nvfp4 |
| [full-ptq-qwen3](todo-full-ptq-qwen3.md) | P2 | Run production-grade NVFP4 PTQ on Qwen3-30B-A3B | $17.00 | 3h | ptq, full, qwen3 |
| [prd-update-smoke-results](todo-prd-update-smoke-results.md) | P2 | Update PRD v2 verification report with NVFP4 smoke 실측값 | $0.00 | 30min | docs, prd |

## In Progress (0)

(none)

## Blocked (0)

(none)

## Done (0)

(none)

## Archived (0)

See `_archive/`.

---

## Dependency Graph

```
vllm-deep-gemm (P1, $1)
       ↓ blocks
full-ptq-qwen3 (P2, $17) ──┐
                           │
prd-update-smoke-results ──┴─ depends partly on both (full PTQ results fill more PRD gates)
(P2, $0)
```

## By Tag

- **smoke**: [vllm-deep-gemm](todo-vllm-deep-gemm.md)
- **vllm**: [vllm-deep-gemm](todo-vllm-deep-gemm.md), [full-ptq-qwen3](todo-full-ptq-qwen3.md)
- **nvfp4**: [vllm-deep-gemm](todo-vllm-deep-gemm.md), [full-ptq-qwen3](todo-full-ptq-qwen3.md), [prd-update-smoke-results](todo-prd-update-smoke-results.md)
- **ptq**: [full-ptq-qwen3](todo-full-ptq-qwen3.md)
- **docs**: [prd-update-smoke-results](todo-prd-update-smoke-results.md)
- **runpod**: [vllm-deep-gemm](todo-vllm-deep-gemm.md), [full-ptq-qwen3](todo-full-ptq-qwen3.md)

## By Skill

- [runpod-nvfp4-quantize](../../../runpod-nvfp4-quantize/SKILL.md): [vllm-deep-gemm](todo-vllm-deep-gemm.md), [full-ptq-qwen3](todo-full-ptq-qwen3.md)
- doc-updater-expert: [prd-update-smoke-results](todo-prd-update-smoke-results.md)

## By Source

- [output/qwen3-nvfp4-smoke/REPORT.md](../../../../../output/qwen3-nvfp4-smoke/REPORT.md): [vllm-deep-gemm](todo-vllm-deep-gemm.md)
- [docs/planned/serverless-pricing/serverless-inference-pricing-unified.md](../../../../../docs/planned/serverless-pricing/serverless-inference-pricing-unified.md): [full-ptq-qwen3](todo-full-ptq-qwen3.md)
- [output/serverless-prd/thakicloud-serverless-prd-v2.md](../../../../../output/serverless-prd/thakicloud-serverless-prd-v2.md): [prd-update-smoke-results](todo-prd-update-smoke-results.md)
