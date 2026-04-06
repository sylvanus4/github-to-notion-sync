---
name: patent-kr-review
description: >-
  Review Korean patent application drafts for compliance with Korean Patent
  Act: Article 29 (novelty, inventive step/진보성), Article 42 (specification
  requirements — written description/기재불비, support basis/뒷받침 요건,
  enablement, clarity), and Article 45 (unity of invention). Produces
  severity-ranked Korean-language issue report with specific fix suggestions.
  Use when the user asks to "한국 특허 검토", "명세서 검토", "기재불비 점검",
  "진보성 분석", "Korean patent review", "KIPO compliance check", or
  "뒷받침 요건 확인". Do NOT use for US patent review (use patent-us-review).
  Do NOT use for AI/SW-specific examination guidelines review (use
  patent-kr-ai-invention). Do NOT use for drafting (use patent-kr-drafting).
  Korean triggers: "한국 특허 검토", "명세서 검토", "기재불비", "진보성 분석",
  "뒷받침 요건".
metadata:
  version: "1.0.0"
  category: "review"
  author: "thaki"
---

# Korean Patent Review — 특허법 준수 분석

## Role

한국 특허청(KIPO) 심사관 관점에서 특허 출원 초안을 분석하여 거절 리스크를
사전 식별하고, 특허법 제29조(신규성/진보성), 제42조(명세서 기재요건), 제45조
(발명의 단일성) 준수 여부를 검토하는 전문가 수준의 리뷰어.

## Prerequisites

- Korean patent draft (from patent-kr-drafting or user input)
- Prior art references (from patent-search, optional)
- Write tool for persisting results to `outputs/patent-kr-review/{date}/`

## Workflow

### Step 0: 입력 검증 (Input Validation)

분석 전에 다음을 확인한다. 미충족 시 중단하거나 보고서 상단에 한계를 명시한다.

| 항목 | 규칙 |
|------|------|
| **(a) 완전한 청구항 세트** | **모든 청구항**이 제공되어야 한다. 일부 청구항만 있는 경우 **작업 중단** 또는 완본 요청 후 진행. |
| **(b) 발명의 설명 (명세서)** | 명세서 전문 또는 청구항 지지에 필요한 최소 범위의 명세서 텍스트 필수. |
| **(c) 도면 자료** | 가능하면 도면 목록/도면을 확보한다. |

**명세서가 없는 경우:** 뒷받침 요건(제42조 제4항 제1호), 실시가능 요건 등 **명세서 기반 분석이 불가능하거나 매우 제한적**임을 **경고**하고, 사용자 확인 하에 요약 분석만 수행한다.

**도면이 없는 경우:** 명세서·도면·청구항 간 **부호 일관성 점검이 제한적**임을 보고서에 **고지**한다.

### Step 1: 청구항 파싱

각 청구항을 구조화된 요소로 분해:
- 청구항 번호, 유형 (독립항/종속항), 카테고리 (방법/장치/기록매체)
- 전제부, 구성요소 목록
- 종속항 참조 관계

### Step 2: 제29조 제1항 — 신규성

각 독립항에 대해:
- 선행기술 1건과 모든 요소 대비
- 가장 가까운 단일 선행기술 식별
- 신규성 상실 요소 vs 차별 요소 구분

| 청구항 | 가장 가까운 선행기술 | 일치 요소 | 차별 요소 | 판정 |
|--------|-------------------|----------|----------|------|
| 1 | [문헌번호] | [목록] | [목록] | 신규성 인정/부정 |

### Step 3: 제29조 제2항 — 진보성 (Inventive Step)

KIPO의 진보성 판단 기준 적용:

1. **청구발명의 인정**: 청구항의 기술적 의의 파악
2. **선행기술 선정**: 기술분야 관련성 기반
3. **차이점 확인**: 청구발명과 선행기술의 구성 차이
4. **진보성 판단**:
   - 차이점의 기술적 의의가 있는가?
   - 통상의 기술자가 선행기술로부터 용이하게 발명할 수 있는가?
   - 선행기술의 결합 동기(motivation)가 존재하는가?
   - 현저한 효과(unexpected effect)가 있는가?

| 청구항 | 선행기술 조합 | 차이점 | 결합 동기 | 효과 | 판정 |
|--------|-------------|--------|----------|------|------|
| 1 | [문헌 A + B] | [내용] | [유/무] | [유/무] | 인정/부정 |

### Step 4: 제42조 제3항 — 실시가능 요건

통상의 기술자(PHOSITA)가 명세서 기재만으로 발명을 실시할 수 있는지:
- 각 청구항 요소에 대한 실시 방법 기재 여부
- 구체적 수치/파라미터 기재 여부 (필요시)
- 실시예의 충분성

### Step 5: 제42조 제4항 제1호 — 뒷받침 요건 (Support Basis)

**가장 중요한 검토 항목** — 한국 심사실무에서 가장 빈번한 거절 사유:

각 청구항 요소에 대해:
- 발명의 설명에 대응하는 구체적 단락 존재 여부
- 도면에 대응하는 부호 존재 여부
- 청구항이 발명의 설명보다 과도하게 넓은 범위를 청구하지 않는지

| 청구항 요소 | 명세서 근거 단락 | 도면 부호 | 뒷받침 여부 | 보완 제안 |
|------------|----------------|----------|-----------|----------|
| [요소 1] | [단락] or ❌ | [부호] or ❌ | ✅/❌ | [제안] |

### Step 6: 제42조 제4항 제2호 — 명확성 요건

- 용어의 일관성 (동일 구성요소 → 동일 용어)
- "상기" 참조의 선행기재 존재 여부
- 불명확한 정도 표현 ("대략", "약" 등) 기준 유무
- 기능적 표현의 적절성

### Step 7: 제45조 — 발명의 단일성

- 모든 청구항이 단일 발명 개념에 속하는지
- 특별한 기술적 특징(special technical feature) 공유 여부
- 분할출원 필요성 판단

### Step 8: 교차 점검

- 부호 일관성 (명세서 ↔ 도면 ↔ 청구항)
- 용어 일관성
- 종속항 참조 오류
- 요약서 적합성

### Step 9: 검토 보고서 생성

심각도별 이슈 목록 (한국어):

| # | 심각도 | 조항 | 청구항 | 이슈 | 보완 제안 |
|---|--------|------|--------|------|----------|
| 1 | 🔴 필수 보완 | 42(4)①호 | 3 | 뒷받침 부족 | [구체적 보완안] |
| 2 | 🟠 권고 보완 | 29(2) | 1 | 진보성 취약 | [구체적 보완안] |
| 3 | 🟡 참고 | 42(4)②호 | 5 | 용어 불일치 | [구체적 보완안] |

심각도:
- **🔴 필수 보완**: 거절 확실 — 출원 전 반드시 수정
- **🟠 권고 보완**: 거절 가능성 높음 — 수정 강력 권고
- **🟡 참고**: 경미한 리스크 — 선택적 수정
- **🟢 양호**: 문제 없음

### Step 10: Persist Output

Write to `outputs/patent-kr-review/{date}/`:
- `review-report-kr.md` — 심각도별 이슈 보고서 (한국어)
- `support-basis-check.md` — 뒷받침 요건 매트릭스
- `inventive-step-analysis.md` — 진보성 분석
- `review-summary.json` — 구조화된 요약

## Anti-Patterns (금지 사항)

1. 모든 기능적 표현을 **불명확**으로 판정하지 말 것 — 통상의 기술자가 이해할 수 있는 수준이면 충분할 수 있다.
2. **"필수 보완"** 심각도를 **구체적 조항 근거 없이** 부여하지 말 것.
3. 진보성 판단에서 **후견적 고찰(hindsight bias)**에 기대어 선행기술을 맞추지 말 것 — **선행기술만**으로 용이성·결합을 판단한다.
4. 뒷받침 요건 검토 시 **특정 단락만** 보고 "부족"으로 끝내지 말 것 — **명세서 전체 맥락**을 고려한다.
5. **종속항 참조 오류** 검출 없이 보고서를 완성하지 말 것 — 참조 체인을 반드시 점검한다.

## Worked Example: 뒷받침 요건 분석 항목 (예시)

**청구항 요소:** "DAG 구성"

**분석 기록 예시:**

> 청구항 요소: 'DAG 구성' → 명세서 **[0042]-[0045]**에 '에이전트 스킬 간의 의존 관계를 분석하여 방향성 비순환 그래프를 구성하는 방법'이 기재됨, **도 3 부호 130** 참조 → **뒷받침: 충분**

(실제 검토 시 단락·도면 번호는 해당 출원 문헌에 맞게 대체한다.)

### Step 11: Pre-Delivery Check (전달 전 점검)

최종 산출물 전에 다음을 **모두** 확인한다.

1. **뒷받침 매트릭스:** 모든 청구항(또는 청구항의 모든 구성요소 항목)이 뒷받침 매트릭스에 포함되어 있는가?
2. **필수 보완:** "🔴 필수 보완"으로 분류된 모든 항목에 **구체적 조항 근거** 및 **보완안**이 있는가? (근거 없는 "필수 보완" 라벨 금지)
3. **진보성:** 진보성 분석에 **인용문헌 조합**, **결합 동기** 유무 또는 부재 이유가 서술되어 있는가?
4. **부호 일관성:** 도면이 있는 경우 부호 일관성 점검 **결과**가 보고서에 포함되어 있는가? 도면이 없으면 "제한적" 고지가 되어 있는가?

## Output Artifacts

| Artifact | Path | Format |
|----------|------|--------|
| 검토 보고서 | `outputs/patent-kr-review/{date}/review-report-kr.md` | Markdown |
| 뒷받침 점검 | `outputs/patent-kr-review/{date}/support-basis-check.md` | Markdown |
| 진보성 분석 | `outputs/patent-kr-review/{date}/inventive-step-analysis.md` | Markdown |
| 구조화 요약 | `outputs/patent-kr-review/{date}/review-summary.json` | JSON |

## Constraints

- 모든 보고서는 한국어로 작성
- 출원 전 리스크 평가이며 법적 조언이 아님
- 변리사 검토 필수 권고
- 공개된 선행기술만 기반으로 분석

## Gotchas

- 뒷받침 요건(제42조 제4항 제1호)은 한국 심사에서 가장 빈번한 거절 사유 —
  미국보다 엄격한 기준 적용
- 진보성 판단에서 "후견적 고찰" (hindsight bias) 주의
- 보정(amendment) 범위가 미국보다 엄격: 최초 출원 명세서에 기재된 사항
  범위 내에서만 보정 가능 (new matter 절대 불가)
- 분할출원은 원출원 계속 중에만 가능
- 수치 한정 발명: 수치 범위의 임계적 의의 입증 필요
