# LightEval Leaderboard Tasks Reference

## Open LLM Leaderboard v2 태스크 목록

전체 리더보드 suite를 구성하는 6개 태스크.

### Task Format

```
leaderboard|{task_name}|{n_shots}
```

### 공식 태스크

| Task String | 벤치마크 | N-shot | 설명 |
|-------------|----------|--------|------|
| `leaderboard\|ifeval\|0` | IFEval | 0-shot | Instruction Following Eval |
| `leaderboard\|bbh\|3` | BBH | 3-shot | BIG-Bench Hard (23 subtasks) |
| `leaderboard\|math_hard\|4` | MATH Lvl 5 | 4-shot | 대학 수준 수학 |
| `leaderboard\|gpqa:diamond\|0` | GPQA Diamond | 0-shot | 대학원 과학 QA |
| `leaderboard\|musr\|0` | MuSR | 0-shot | Multi-Step Reasoning |
| `leaderboard\|mmlu_pro\|5` | MMLU-Pro | 5-shot | 전문 지식 (14 분야) |

### Full Suite Command (한 줄)

```bash
"leaderboard|ifeval|0,leaderboard|bbh|3,leaderboard|math_hard|4,leaderboard|gpqa:diamond|0,leaderboard|musr|0,leaderboard|mmlu_pro|5"
```

## Backend 선택

| Backend | 명령어 | 장점 | 요구사항 |
|---------|--------|------|----------|
| vLLM | `lighteval vllm` | 5-10x 빠름, batch 처리 | CUDA GPU, vLLM 호환 아키텍처 |
| Accelerate | `lighteval accelerate` | 메모리 효율, 넓은 호환 | GPU (CPU도 가능하나 매우 느림) |
| Inference Providers | `lighteval eval` | GPU 불필요, API 기반 | HF Inference API 접근 |

## 예상 실행 시간 (A100 80GB 기준)

| 모델 크기 | 단일 태스크 | Full Suite (6개) |
|-----------|------------|-----------------|
| 1-3B | 5-15분 | 30분-1.5시간 |
| 7-8B | 15-30분 | 1.5-3시간 |
| 13-14B | 30-60분 | 3-6시간 |
| 32-34B | 1-2시간 | 6-12시간 |
| 70B+ | 2-4시간 | 12-24시간 |

## 출력 형식

`--output-dir` 하위에 생성:

```
results/{model_name_sanitized}/
  results_{timestamp}.json     # 요약 (태스크별 점수)

details/{model_name_sanitized}/
  details_{task}_{timestamp}.parquet  # 샘플별 (--save-details 시)
```

### results JSON 구조

```json
{
  "config": { "model_name": "...", "model_dtype": "..." },
  "results": {
    "leaderboard|ifeval|0": {
      "prompt_level_strict_acc": 0.72,
      "inst_level_strict_acc": 0.78
    },
    "leaderboard|bbh|3": {
      "acc_norm": 0.61
    }
  }
}
```

## Troubleshooting

- `Task not found`: `lighteval tasks list | grep leaderboard` 로 사용 가능한 태스크 확인
- vLLM OOM: `gpu_memory_utilization=0.85` 로 낮추기, 또는 `tensor_parallel_size=2`
- Chat template 오류: Instruct 모델만 `use_chat_template=true` 사용
- Tokenizer 경고: `trust_remote_code=true` 추가 (Qwen, Phi 등)
