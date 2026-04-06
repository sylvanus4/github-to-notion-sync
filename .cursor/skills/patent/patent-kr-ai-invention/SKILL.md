---
name: patent-kr-ai-invention
description: >-
  Specialized review for AI and software inventions under KIPO examination
  guidelines. Covers hardware-software cooperation requirements, AI/ML model
  patentability assessment, training data/method claims, data-driven invention
  formatting, and KIPO-specific claim structures for neural networks,
  reinforcement learning, and generative AI. Produces compliance checklist and
  restructuring suggestions. Use when the user asks to "review AI patent for
  KIPO", "AI 발명 심사 기준", "소프트웨어 특허 검토", "KIPO AI guidelines",
  "인공지능 발명 검토", or "AI/ML 특허성 평가". Do NOT use for general Korean
  patent review (use patent-kr-review). Do NOT use for US AI patent review
  (use patent-us-review with Alice/Mayo focus). Do NOT use for drafting AI
  patents from scratch (use patent-kr-drafting with AI flag). Korean triggers:
  "AI 발명 검토", "인공지능 특허", "소프트웨어 발명", "KIPO AI 심사기준",
  "머신러닝 특허".
metadata:
  version: "1.0.0"
  category: "review"
  author: "thaki"
---

# Korean AI/SW Invention Review — KIPO AI 심사 가이드라인

## Role

KIPO AI/SW 발명 심사 가이드라인 전문가 수준의 리뷰어. 인공지능 관련
발명(기계학습, 딥러닝, 강화학습, 생성형 AI 등)의 특허 출원이 KIPO 심사기준을
충족하는지 검토하고, 하드웨어-소프트웨어 협동(hardware-software cooperation)
요건, 발명의 성립성, 청구항 구조를 분석.

## Prerequisites

- AI/SW invention patent draft (claims + specification)
- Write tool for persisting results to `outputs/patent-kr-ai/{date}/`

## Workflow

### Step 0: 입력 검증 (Input Validation)

본 스킬 실행 전에 다음을 확인한다.

| 항목 | 규칙 |
|------|------|
| **(a) AI/SW 발명 청구항 + 명세서** | 청구항과 발명의 설명(명세서) **전문 또는 분석에 필요한 최소 범위**가 필수. 미제공 시 중단 또는 한계 명시. |
| **(b) AI 발명 유형 사전 분류** | 사용자 입력 또는 명세서를 바탕으로 **학습 / 추론 / 데이터 / 모델 구조 / 시스템 / 응용** 중 해당 유형을 **사전에** 택하거나 복수 표시한다. |
| **(c) 학습 데이터·알고리즘 기재 여부** | 명세서에 학습 데이터, 학습·추론 알고리즘의 재현 가능한 기재가 있는지 **사전 확인**한다. |

**명세서에 신경망 구조 기재가 없는 경우:** 체크리스트 항목 5(신경망 구조) 및 실시 가능성에 **기재 보충 필요**를 **사전 고지**한다.

### Step 1: AI Invention Classification

분류:

| 유형 | 설명 | 예시 |
|------|------|------|
| 학습 방법 | 모델 훈련 과정 자체의 발명 | 새로운 학습 알고리즘, 손실 함수 |
| 추론 방법 | 훈련된 모델의 적용 방법 | 실시간 추론 최적화, 모델 압축 |
| 학습 데이터 | 데이터 수집/전처리/증강 방법 | 능동 학습, 데이터 정제 파이프라인 |
| 모델 구조 | 신경망 아키텍처 자체 | 새로운 어텐션 메커니즘, 네트워크 토폴로지 |
| 시스템 구성 | AI를 포함한 전체 시스템 | 자율주행 시스템, 추천 시스템 |
| 응용 분야 | 특정 도메인 적용 | 의료 영상 분석, 금융 사기 탐지 |

### Step 2: 발명의 성립성 (Patent Eligibility)

KIPO 기준에 따른 발명의 성립성 판단:

**소프트웨어 관련 발명의 성립 요건**:
1. 소프트웨어에 의한 정보 처리가 하드웨어를 이용하여 구체적으로 실현되는가?
2. 자연법칙을 이용한 기술적 사상의 창작인가?

**Hardware-Software Cooperation Check**:

| 체크 항목 | 기준 | 결과 |
|----------|------|------|
| 프로세서 명시 | 청구항에 프로세서/CPU/GPU 언급 | ✅/❌ |
| 메모리 명시 | 데이터 저장/로딩 하드웨어 언급 | ✅/❌ |
| 입출력 장치 | 센서/디스플레이/통신 모듈 등 | ✅/❌ |
| 구체적 처리 | 하드웨어를 이용한 구체적 정보처리 기재 | ✅/❌ |
| 기술적 효과 | 처리 속도/정확도/메모리 효율 등 구체적 효과 | ✅/❌ |

**불인정 사례** (성립성 부정):
- 수학적 알고리즘 자체 (하드웨어 협동 없음)
- 인간의 정신적 판단 과정 그 자체
- 학습된 모델의 파라미터 데이터 자체

### Step 3: 청구항 구조 분석

AI 발명의 권장 청구항 구조 비교:

**방법 청구항** (적합한 구조):
```
프로세서에 의해 수행되는 [발명명] 방법으로서,
[학습 데이터]를 수집하는 단계;
상기 [학습 데이터]를 이용하여 [신경망 모델]을 학습시키는 단계;
상기 학습된 [신경망 모델]에 [입력 데이터]를 입력하여 [결과]를 출력하는 단계;
및
상기 [결과]에 기초하여 [구체적 동작]을 수행하는 단계
를 포함하는 [발명명] 방법.
```

**장치 청구항** (적합한 구조):
```
[발명명] 장치로서,
[학습 데이터]를 저장하는 메모리; 및
상기 메모리와 연결된 프로세서를 포함하며,
상기 프로세서는,
  상기 [학습 데이터]를 이용하여 [신경망 모델]을 학습시키고,
  학습된 [신경망 모델]에 [입력 데이터]를 입력하여 [결과]를 산출하고,
  상기 [결과]에 기초하여 [구체적 동작]을 수행하도록 구성되는,
[발명명] 장치.
```

각 청구항 검증:
- 하드웨어 요소 포함 여부
- 알고리즘이 하드웨어에서 구체적으로 실현되는 과정 기재
- 입력-처리-출력 흐름의 명확성

### Step 4: 명세서 기재 충분성 (AI-specific)

AI 발명 특유의 기재 요건 점검:

| 기재 항목 | 요구 수준 | 확인 결과 |
|----------|----------|----------|
| 학습 데이터 유형/구조 | 구체적 기재 | ✅/❌ |
| 학습 알고리즘/절차 | 재현 가능한 수준 | ✅/❌ |
| 신경망 구조 | 레이어 구성, 활성화 함수 등 | ✅/❌ |
| 하이퍼파라미터 | 주요 값 또는 범위 | ✅/❌ |
| 손실 함수/최적화 | 수학적 정의 또는 설명 | ✅/❌ |
| 입력/출력 데이터 형식 | 구체적 기재 | ✅/❌ |
| 성능 지표 | 정확도/속도/효율 등 수치 | ✅/❌ |
| 비교 실험 | 종래기술 대비 성능 비교 | ✅/❌ (권장) |

### Step 5: AI-Specific Gotchas

다음 주의사항 체크:

1. **학습된 모델 자체는 발명 아님**: 모델의 파라미터/가중치는 데이터이며
   발명이 아님. 학습 방법 또는 추론 방법이 발명의 대상.

2. **학습 데이터 기재**: 학습 데이터의 종류, 수집 방법, 전처리 과정을
   명세서에 구체적으로 기재해야 함. "빅데이터를 이용하여"는 불충분.

3. **재현성 (Reproducibility)**: 통상의 기술자가 명세서만으로 동일한
   성능을 달성할 수 있어야 함. 비결정적(stochastic) 학습의 경우,
   성능 범위를 명시.

4. **블랙박스 기재 금지**: "딥러닝으로 분류한다"만으로는 불충분. 신경망의
   구조, 학습 절차, 추론 과정을 구체적으로 기재.

5. **공지 모델 활용**: ResNet, BERT, GPT 등 공지 모델을 활용하는 경우,
   기존 모델 대비 차별점(개선된 전처리, 후처리, 적용 방법 등)을
   명확히 기재.

6. **생성형 AI**: 생성 결과물 자체는 발명이 아님. 생성 방법, 품질 제어
   방법, 특정 도메인에 특화된 생성 과정이 발명의 대상.

### Step 6: Compliance Checklist

종합 체크리스트:

| # | 항목 | 기준 | 결과 | 비고 |
|---|------|------|------|------|
| 1 | 하드웨어-소프트웨어 협동 | 필수 | ✅/❌ | |
| 2 | 프로세서/메모리 명시 | 필수 | ✅/❌ | |
| 3 | 기술적 효과 기재 | 필수 | ✅/❌ | |
| 4 | 학습 데이터 구체적 기재 | 필수 | ✅/❌ | |
| 5 | 신경망 구조 기재 | 권장 | ✅/❌ | |
| 6 | 하이퍼파라미터 기재 | 권장 | ✅/❌ | |
| 7 | 성능 수치 기재 | 권장 | ✅/❌ | |
| 8 | 비교 실험 결과 | 권장 | ✅/❌ | |
| 9 | 입출력 데이터 형식 | 필수 | ✅/❌ | |
| 10 | 재현 가능성 | 필수 | ✅/❌ | |

### Step 7: Restructuring Suggestions

불합격 항목에 대해 구체적 보완 방안 제시:
- 청구항 재구성 예시 (before/after)
- 명세서 추가 기재 항목
- 도면 추가 제안 (AI 파이프라인 도면, 데이터 흐름도 등)

### Step 8: Persist Output

Write to `outputs/patent-kr-ai/{date}/`:
- `ai-review-report-kr.md` — AI 발명 심사기준 준수 보고서
- `hw-sw-cooperation-check.md` — 하드웨어-소프트웨어 협동 점검
- `compliance-checklist.md` — 종합 체크리스트
- `restructuring-suggestions.md` — 보완 제안

## Anti-Patterns (금지 사항)

1. 모든 LLM/기초모델 사용 발명을 **"프롬프트 엔지니어링"**으로 일괄 판정하지 말 것 — **시스템 수준 구성**(라우팅, 스케줄링, 자원 배분, 장애 복구 등)을 반드시 확인한다.
2. HW-SW 협동 체크에서 **"프로세서" 단어 존재만**으로 통과 판정하지 말 것 — **구체적 정보처리 과정**이 하드웨어와 결합되어 기재되었는지 확인한다.
3. 공지 모델(BERT, GPT 등) 사용을 이유로 **자동으로 진보성 부정**하지 말 것 — **적용 방법·구성의 차별점**을 확인한다.
4. 재현성 판단에서 **비결정적(stochastic) 학습**의 고유한 특성을 무시하지 말 것 — **성능 범위·시드·반복 실험** 등 기재 여부를 확인한다.

## Worked Example: HW-SW 협동 분석 (테스트 발명)

**테스트 발명:** LLM Agent Orchestration Platform — 스킬 레지스트리 기반 의미 검색 라우팅, DAG 실행 순서, 자원 인지형 모델 선택.

**예시 판정 기록:**

> 프로세서 명시: ✅ ('프로세서에 의해 수행되는'), 메모리 명시: ✅ ('스킬 레지스트리에 저장된'), 구체적 처리: ✅ ('임베딩 유사도에 기초하여 검색', 'DAG 구성', '복잡도 신호 기반 모델 계층 선택'), 기술적 효과: ✅ ('체크포인트 기반 장애 복구로 시스템 안정성 향상') → **판정: 성립성 인정** (해당 출원 명세 기재와 일치할 때)

### Step 9: Pre-Delivery Check (전달 전 점검)

최종 산출 전에 다음을 **모두** 확인한다.

1. **체크리스트 10항목:** 상기 **종합 체크리스트 10개 항목**이 각각 평가되어 결과가 표에 채워졌는가?
2. **불합격 항목:** ❌ 항목마다 **before/after 청구항 예시** 또는 명세서 보강 문안 예시가 포함되었는가?
3. **일관성:** Step 0에서 확정한 **발명 유형 분류**와 Step 3 **청구항 구조 분석** 결과가 서로 모순되지 않는가?

## Output Artifacts

| Artifact | Path | Format |
|----------|------|--------|
| AI 검토 보고서 | `outputs/patent-kr-ai/{date}/ai-review-report-kr.md` | Markdown |
| HW-SW 협동 점검 | `outputs/patent-kr-ai/{date}/hw-sw-cooperation-check.md` | Markdown |
| 체크리스트 | `outputs/patent-kr-ai/{date}/compliance-checklist.md` | Markdown |
| 보완 제안 | `outputs/patent-kr-ai/{date}/restructuring-suggestions.md` | Markdown |

## Constraints

- 모든 보고서는 한국어로 작성
- KIPO 인공지능 분야 심사 가이드라인 기준 적용
- 법적 조언이 아닌 출원 전 리스크 평가
- 변리사 검토 필수 권고
- AI 기술의 급속한 발전으로 심사기준이 변경될 수 있음을 고지

## Gotchas

- KIPO AI 심사 가이드라인은 주기적으로 업데이트됨 — 최신 버전 확인 필요
- 미국(Alice/Mayo)과 한국의 AI 발명 심사 기준은 상이:
  한국은 HW-SW 협동에 초점, 미국은 abstract idea 회피에 초점
- 학습 데이터 자체에 대한 권리 주장은 저작권/데이터베이스권의 영역이지
  특허의 대상이 아님
- 강화학습(RL) 발명: 보상 함수, 상태 공간, 행동 공간의 구체적 정의 필수
- 전이학습(Transfer Learning): 소스 도메인과 타겟 도메인의 관계,
  파인튜닝 방법을 구체적으로 기재
- LLM/기초모델 기반 발명: 프롬프트 엔지니어링 자체는 발명으로 인정되기
  어려움 — 시스템 수준의 기술적 구성이 필요
