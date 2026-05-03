---
name: hf-leaderboard-submit
description: >-
  Open LLM Leaderboard 제출 준비/검증/상태 확인/결과 분석 파이프라인. LightEval
  또는 lm-evaluation-harness로 사전 평가 후 리더보드 제출. Use when "리더보드
  제출", "leaderboard submit", "모델 평가 제출", "제출 상태", "submission status".
  Do NOT use for rank tracking (hf-leaderboard-tracker), general eval
  (hf-evaluation), or training (hf-model-trainer).
---

# Open LLM Leaderboard 제출 파이프라인

HuggingFace Open LLM Leaderboard에 모델을 제출하기 위한 end-to-end 워크플로우.
모델 readiness 검증 -> LightEval 사전 평가 -> 제출 -> 상태 확인 -> 결과 분석.

## 출력 언어

모든 출력물은 한국어로 작성. 모델명, 벤치마크명, 기술 용어는 원어 유지.

## Version

1.1.0

## Prerequisites

- `hf` CLI installed and authenticated (`hf whoami` 확인)
- Python 3.10+ with `uv` (PEP 723 스크립트 자동 의존성)
- GPU 환경 (사전 평가 시): CUDA 지원 GPU + vLLM 호환
- `HF_TOKEN` 환경변수 설정 (Write 권한)
- 대안: `lm-evaluation-harness` (EleutherAI) -- LightEval 미설치 환경에서 사용

## Required Skills

- `hf-hub` -- HF CLI 및 Hub 인터랙션
- `hf-evaluation` -- 평가 실행 (lighteval/inspect-ai)
- `hf-models` -- 모델 검색 및 메타데이터 확인

## Open LLM Leaderboard 개요

### 벤치마크 구성 (v2, 현행)

| 벤치마크 | 영역 | 설명 |
|----------|------|------|
| IFEval | Instruction Following | 지시 따르기 정확도 |
| BBH (BIG-Bench Hard) | Reasoning | 복합 추론 23개 태스크 |
| MATH (Lvl 5) | Mathematics | 대학 수준 수학 문제 |
| GPQA | Science | 대학원 수준 과학 QA |
| MuSR | Multi-step Reasoning | 다단계 추론 |
| MMLU-Pro | Knowledge | 전문 지식 14개 분야 |

### 핵심 데이터셋

| Dataset | 용도 |
|---------|------|
| `open-llm-leaderboard/contents` | 리더보드 현재 결과 (parquet) |
| `open-llm-leaderboard/requests` | 제출 요청 상태 추적 |
| `open-llm-leaderboard/results` | 평가 완료 결과 집계 |
| `open-llm-leaderboard/{org}__{model}-details` | 모델별 상세 결과 |

### 제출 요건

1. **Public model**: HF Hub에 공개 상태
2. **Causal LM / Instruct**: `AutoModelForCausalLM`으로 로드 가능
3. **Valid config**: `config.json`, `tokenizer_config.json` 존재
4. **Model card**: README.md 존재 (선택이나 강력 권장)
5. **License 명시**: gated model은 평가 제한될 수 있음
6. **가중치 완전성**: safetensors/bin 파일 누락 없이 업로드 완료
7. **크기 제한**: 현재 ~140B 파라미터까지 지원 (인프라 의존)

## Pipeline Phases

### Phase 1 -- 모델 Readiness 검증

대상 모델의 리더보드 제출 가능 여부를 사전 검증한다.

#### 1.1 기본 메타데이터 확인

```bash
# HF Hub에서 모델 정보 조회
hf repo info <org/model-name> --type model
```

MCP tool 사용 시:
- `mcp__hf__hub_repo_details` 로 repo 상태 확인
- 확인 항목: public 여부, gated 여부, last_modified, tags, library_name

**모델 미존재 시 (404):**
- repo ID 오타 확인 (대소문자, org명)
- `mcp__hf__hf_hub_query`로 해당 org의 모델 목록 검색하여 유사 모델 제안
- 업로드 전 상태라면 Phase 1 즉시 FAIL, 업로드 후 재검증 안내

#### 1.2 필수 파일 및 Tag 기반 검증

**MCP 기반 (tag 추론):** `hub_repo_details`가 반환하는 tags에서 추론:

| Tag | 의미 |
|-----|------|
| `safetensors` | .safetensors 가중치 존재 |
| `transformers` | config.json + tokenizer 존재 (transformers 호환) |
| `text-generation` | CausalLM pipeline 호환 |
| `conversational` | chat template 포함 |

**CLI 기반 (파일 직접 확인):**
```bash
hf repo ls <org/model-name> --type model | grep -E "(config\.json|tokenizer_config\.json|README\.md|\.safetensors)"
```

체크리스트:
- [ ] `config.json` 존재 (`transformers` tag로 추론 가능)
- [ ] `tokenizer_config.json` 또는 `tokenizer.json` 존재 (`transformers` tag)
- [ ] `generation_config.json` 존재 (선택)
- [ ] Model weights (`.safetensors` 또는 `.bin`) (`safetensors` tag)
- [ ] `README.md` 존재 (model card 유무)

#### 1.3 Architecture 호환성

`hub_repo_details`의 tags에서 architecture 확인:
- `text-generation` tag + `transformers` tag = AutoModelForCausalLM 호환 확률 높음
- Architecture tag 예: `llama`, `mistral`, `qwen2`, `qwen3_moe`, `phi3` 등

지원 아키텍처 (AutoModelForCausalLM):
- LlamaForCausalLM, MistralForCausalLM, Qwen2ForCausalLM, Qwen2MoeForCausalLM
- GPTNeoXForCausalLM, Phi3ForCausalLM, GemmaForCausalLM, StableLmForCausalLM 등

미지원 (리더보드 제출 불가):
- encoder-only (BERT, RoBERTa), encoder-decoder (T5, BART), vision-only (ViT)

#### 1.4 기존 제출 확인

중복 제출 방지를 위해 기존 요청/결과 확인:

```bash
# requests 데이터셋에서 해당 모델 검색
# MCP: hf_hub_query로 open-llm-leaderboard/{org}__{model}-details 존재 여부 확인
```

**Output:** Readiness report (PASS/FAIL per item)

### Phase 2 -- LightEval 사전 평가 (Local)

리더보드 제출 전 사내 GPU에서 일부 벤치마크를 돌려 예상 점수를 확인한다.

#### 2.1 LightEval Task Format

Open LLM Leaderboard v2 태스크:

```
leaderboard|ifeval|0
leaderboard|bbh|3
leaderboard|math_hard|4
leaderboard|gpqa:diamond|0
leaderboard|musr|0
leaderboard|mmlu_pro|5
```

#### 2.2 Quick Smoke Test (1개 태스크)

가장 빠른 IFEval로 기본 동작 확인:

```bash
# vLLM backend (빠름, GPU 필요)
lighteval vllm \
  "pretrained=<org/model-name>" \
  "leaderboard|ifeval|0" \
  --output-dir ./output/leaderboard-pretest/

# 또는 accelerate backend (느리지만 메모리 효율)
lighteval accelerate \
  "model_name=<org/model-name>" \
  "leaderboard|ifeval|0" \
  --output-dir ./output/leaderboard-pretest/
```

#### 2.3 Full Leaderboard Suite (6개 태스크)

전체 벤치마크 사전 실행:

```bash
lighteval vllm \
  "pretrained=<org/model-name>,dtype=bfloat16,gpu_memory_utilization=0.9" \
  "leaderboard|ifeval|0,leaderboard|bbh|3,leaderboard|math_hard|4,leaderboard|gpqa:diamond|0,leaderboard|musr|0,leaderboard|mmlu_pro|5" \
  --output-dir ./output/leaderboard-pretest/ \
  --save-details
```

Chat/Instruct 모델:
```bash
lighteval vllm \
  "pretrained=<org/model-name>,dtype=bfloat16,use_chat_template=true" \
  "leaderboard|ifeval|0,leaderboard|bbh|3,leaderboard|math_hard|4,leaderboard|gpqa:diamond|0,leaderboard|musr|0,leaderboard|mmlu_pro|5" \
  --output-dir ./output/leaderboard-pretest/ \
  --save-details
```

#### 2.4 대안: lm-evaluation-harness (EleutherAI)

LightEval 미설치 환경에서 EleutherAI의 `lm-evaluation-harness` 사용:

```bash
pip install lm-eval

# IFEval 단일 태스크
lm_eval --model hf \
  --model_args pretrained=<org/model-name>,dtype=bfloat16 \
  --tasks leaderboard_ifeval \
  --output_path ./output/leaderboard-pretest/

# Full suite (Open LLM Leaderboard v2 태스크)
lm_eval --model hf \
  --model_args pretrained=<org/model-name>,dtype=bfloat16 \
  --tasks leaderboard_ifeval,leaderboard_bbh,leaderboard_math_hard,leaderboard_gpqa,leaderboard_musr,leaderboard_mmlu_pro \
  --output_path ./output/leaderboard-pretest/ \
  --batch_size auto
```

**LightEval vs lm-evaluation-harness 선택:**

| 항목 | LightEval | lm-evaluation-harness |
|------|-----------|----------------------|
| 유지보수 | HuggingFace (리더보드 운영 팀) | EleutherAI |
| vLLM 지원 | 네이티브 | 플러그인 (`lm_eval --model vllm`) |
| 태스크 이름 | `leaderboard\|ifeval\|0` | `leaderboard_ifeval` |
| 리더보드 정합성 | 공식 (동일 코드베이스) | 높음 (호환 유지) |
| 설치 용이성 | `pip install lighteval` | `pip install lm-eval` |

권장: LightEval 우선 (리더보드와 동일 코드), 환경 문제 시 lm-eval 폴백.

#### 2.5 HF Jobs 원격 실행 (GPU 미보유 시)

`hf-evaluation` 스킬의 vLLM 실행 경로 활용:

```bash
hf jobs uv run <skill-path>/scripts/lighteval_vllm_uv.py \
  --flavor a10g-small \
  --secret HF_TOKEN=$HF_TOKEN \
  -- --model <org/model-name> \
     --tasks "leaderboard|ifeval|0,leaderboard|bbh|3,leaderboard|math_hard|4,leaderboard|gpqa:diamond|0,leaderboard|musr|0,leaderboard|mmlu_pro|5"
```

#### 2.6 결과 해석

LightEval 출력 구조:
```
output/leaderboard-pretest/
  results/<model-name>/
    results_*.json      # 태스크별 점수
    details_*.parquet   # 샘플별 상세 (--save-details)
```

점수 해석 기준 (2026 기준 대략적 참고치):

| 벤치마크 | 7B 평균 | 70B 평균 | 상위 10% |
|----------|---------|---------|---------|
| IFEval | 40-55 | 70-80 | 85+ |
| BBH | 45-55 | 65-75 | 80+ |
| MATH | 10-25 | 35-50 | 60+ |
| GPQA | 25-30 | 35-45 | 50+ |
| MuSR | 35-45 | 50-60 | 65+ |
| MMLU-Pro | 30-40 | 55-65 | 75+ |

**Output:** 예상 점수표 + 제출 권고 (상위 N% 예상 진입)

### Phase 3 -- 리더보드 제출

#### 3.1 제출 방법

Open LLM Leaderboard는 Space UI를 통한 제출을 지원:

1. Space 접속: `open-llm-leaderboard/open_llm_leaderboard`
2. "Submit" 탭에서 모델 repo ID 입력
3. Model type 선택 (pretrained / fine-tuned / instruction-tuned / merges/moerges)
4. Precision 선택 (float16 / bfloat16 / 4bit / 8bit)
5. Weight type: Original / Delta / Adapter
6. 제출

#### 3.2 제출 시 선택 옵션

| 항목 | 옵션 | 권장 |
|------|------|------|
| Model type | pretrained, fine-tuned, instruction-tuned, merges | 정확히 분류 |
| Precision | float16, bfloat16, 4bit, 8bit | 모델 학습 시 사용한 precision |
| Weight type | Original, Delta, Adapter | Original (full weights) 권장 |

#### 3.3 제출 후 예상 대기 시간

- Queue 상태에 따라 수시간~수일
- 작은 모델 (7B): 보통 몇 시간
- 큰 모델 (70B+): 수일 소요 가능

### Phase 4 -- 제출 상태 확인

#### 4.1 requests 데이터셋 조회

```python
# MCP tool 또는 datasets API로 확인
# open-llm-leaderboard/requests 에서 모델 검색
```

MCP 활용:
```
mcp__hf__hf_hub_query: "Search datasets by open-llm-leaderboard, find requests dataset, look for {model-name}"
```

상태 분류:
- **PENDING**: 대기열 진입, 평가 시작 전
- **RUNNING**: 평가 진행 중
- **FINISHED**: 완료, 결과 공개
- **FAILED**: 실패 (모델 로드 오류, OOM 등)

#### 4.2 결과 데이터셋 확인

평가 완료 시 상세 결과 데이터셋 자동 생성:

```
open-llm-leaderboard/{org}__{model-name}-details
```

MCP로 확인:
```
mcp__hf__hub_repo_details: repo_ids=["open-llm-leaderboard/{org}__{model}-details"]
```

#### 4.3 contents 데이터셋에서 최종 순위

```
mcp__hf__hf_hub_query: "From open-llm-leaderboard/contents dataset, find row for {model-name}, show all scores"
```

### Phase 5 -- 결과 분석 및 보고

#### 5.1 벤치마크별 분석

결과 확인 후 각 벤치마크 성능을 분석:

```markdown
# Open LLM Leaderboard 결과 분석: {model-name}

## 종합 점수
- **Average**: {avg_score}
- **순위**: #{rank} / {total} 모델

## 벤치마크별 성적

| 벤치마크 | 점수 | 카테고리 내 순위 | 사전 평가 대비 |
|----------|------|----------------|--------------|
| IFEval | {score} | #{rank} | +/- {delta} |
| BBH | {score} | #{rank} | +/- {delta} |
| MATH | {score} | #{rank} | +/- {delta} |
| GPQA | {score} | #{rank} | +/- {delta} |
| MuSR | {score} | #{rank} | +/- {delta} |
| MMLU-Pro | {score} | #{rank} | +/- {delta} |

## 강점/약점 분석
- 강점: {상위 벤치마크}
- 약점: {하위 벤치마크}
- 개선 방향: {제안}
```

#### 5.2 동급 모델 비교

같은 파라미터 크기 대의 모델과 비교:

```
mcp__hf__hf_hub_query: "From open-llm-leaderboard/contents, find models with similar parameter count to {N}B, top 10 by average score"
```

## Error Recovery

| Phase | Error | Recovery |
|-------|-------|----------|
| 1 | Model repo not found | repo ID 정확성 확인, public 여부 체크 |
| 1 | Gated model | 리더보드가 접근 불가할 수 있음, gating 해제 권장 |
| 2 | CUDA OOM | `gpu_memory_utilization` 낮추기, 더 큰 GPU, quantized 평가 |
| 2 | vLLM architecture 미지원 | `accelerate` backend로 전환 |
| 2 | LightEval task not found | `lighteval tasks list` 로 정확한 task name 확인 |
| 3 | 제출 UI 접근 불가 | HF Space 상태 확인, 잠시 후 재시도 |
| 4 | requests에서 모델 미발견 | repo ID 정확성 재확인, 대기열 지연 가능 |
| 4 | FAILED 상태 | 에러 로그 확인, 모델 호환성 문제 해결 후 재제출 |

## 워크플로우 요약

```
[1. Readiness 검증] ─ PASS → [2. LightEval 사전 평가] ─ 점수 양호 →
[3. 리더보드 제출] → [4. 상태 확인 (주기적)] → [5. 결과 분석/보고]
                                                         │
                                      FAIL ← [모델 수정 후 재제출]
```

## 권장 워크플로우 (ThakiCloud 내부)

1. 모델을 HF Hub에 올림 (thaki-AI org)
2. 사내 GPU에서 LightEval로 full suite 실행 (smoke test 먼저)
3. 점수가 목표 대비 양호하면 리더보드 제출
4. 제출 불필요한 경우라도 model card에 eval 결과 추가 (`hf-evaluation` 스킬 활용)
5. 결과 공개 후 `hf-leaderboard-tracker` 로 지속 모니터링

## 관련 스킬

| Skill | 역할 |
|-------|------|
| `hf-evaluation` | 평가 실행 + 모델카드 업데이트 |
| `hf-leaderboard-tracker` | 리더보드 순위 변동 추적 |
| `hf-model-trainer` | 모델 학습/파인튜닝 |
| `hf-models` | 모델 검색/비교 |
| `hf-hub` | HF CLI 기본 작업 |
