# Jarvis Backlog (Curated)

사람이 큐레이션하는 우선순위 큐. INDEX.md는 단순 목록, BACKLOG는 "지금 다음에 무엇을".

## P0 — Now

(none)

## P1 — Next

1. **[vllm-deep-gemm](todo-vllm-deep-gemm.md)** — $1, 15min
   - 스모크 100% 확정 → [[runpod-nvfp4-quantize]] v1.1 release 가능
   - 후속 [full-ptq-qwen3] 신뢰성 확보 위해 선행 권장

## P2 — Soon

2. **[prd-update-smoke-results](todo-prd-update-smoke-results.md)** — $0, 30min
   - 무료, 즉시 실행 가능 (병렬 가능)
   - PRD v2 검증 표 일부 채움

3. **[full-ptq-qwen3](todo-full-ptq-qwen3.md)** — $17, 3h
   - [vllm-deep-gemm] 선행 권장
   - 별도 budget 동의 필요 (단일 항목으로 가장 큰 비용)

## P3 — Later

(none)

## Notes

- 권장 순서: [vllm-deep-gemm] → [prd-update-smoke-results] (두 항목 병렬 가능, 의존 없음) → [full-ptq-qwen3]
- 총 예산 $18 (모두 합계). [full-ptq-qwen3] 실행 결정만 별도 승인 필요.
