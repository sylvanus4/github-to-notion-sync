---
name: patent-kr-drafting
description: >-
  Draft Korean patent application documents: claims (청구항), detailed
  description (발명의 설명), abstract (요약서), and drawings description (도면의
  간단한 설명). Uses support-basis anchored drafting style per Korean Patent Act
  Article 42 and KIPO Examination Guidelines. Every claim element must trace to
  a specific specification paragraph and drawing reference. Produces primary
  output in Korean with English reference translation. Supports AI/SW invention
  format per KIPO AI examination guidelines. Use when the user asks to "한국
  특허 출원", "청구항 작성", "Korean patent draft", "KIPO filing", "명세서
  작성", or "특허 명세서". Do NOT use for US patent drafting (use
  patent-us-drafting). Do NOT use for reviewing existing applications (use
  patent-kr-review). Do NOT use for office action responses (use
  patent-kr-oa-response). Korean triggers: "한국 특허 출원", "청구항 작성",
  "명세서 작성", "특허 초안", "KIPO 출원".
metadata:
  version: "1.1.0"
  category: "drafting"
  author: "thaki"
---

# Korean Patent Drafting — 청구항 및 명세서 작성

## Role

Expert Korean patent drafter (변리사급 초안 작성) who produces prosecution-ready
patent application documents following Korean Patent Act Article 42, KIPO
Examination Guidelines, and Korean patent office formatting standards.
Emphasizes support-basis anchored drafting where every claim element has a
direct traceable link to the specification and drawings.

## Prerequisites

- Invention description (from patent-scanner output or user input)
- Prior art search results (from patent-search, optional but recommended)
- Patent diagrams (from patent-diagrams, optional)
- Write tool for persisting output to `outputs/patent-kr/{date}/`

## Workflow

### Step 0: Input Validation

Step 1 이전에 다음 입력을 확보·검증한다:

1. **발명 설명**: 최소 **100자** 이상의 기술 내용, **또는** `patent-scanner` 출력 전문 (제공 시 발명의 요지·구성요소·효과를 스캐너 출력에서 직접 추출).
2. **선행기술 대비 차별점**: 선행 대비 신규성·진보성이 드러나는 요지 (patent-search 결과 인용 가능).
3. **AI/SW 발명 해당 여부**: 소프트웨어/AI 중심이면 이후 단계에서 HW-SW 협동 기재 및 방법·장치 균형을 강제한다.
4. **도면 자료**: `patent-diagrams` 산출물 **또는** 사용자가 제공한 도면/블록도 설명 (없으면 명세서 기재 전 도면 작성·보완 필요 여부를 사용자에게 확인).

**입력이 영어로만** 제공된 경우: 본 스킬은 **한국어 명세·청구항**을 생성하지만, 사용자에게 **기술용어·고유명사**는 출원 전 변리사 검토가 필요함을 명시한다.

발명 설명이 막연하면 **(가)** 해결 과제, **(나)** 해결 수단, **(다)** 선행과의 차이를 추가로 질문한 뒤 초안 작성을 진행한다. `patent-scanner` 출력이 있으면 이를 우선 근거로 삼는다.

### Step 1: Invention Analysis

Extract from user input:
1. 해결하고자 하는 기술적 과제 (technical problem)
2. 기술적 해결수단 (technical solution)
3. 선행기술 대비 차별점 (prior art differentiation)
4. 상업적 실시예 (commercial embodiments)
5. AI/SW 발명 해당 여부 (AI/SW invention classification)

### Step 2: Support Basis Matrix

Before drafting claims, build a support-basis matrix:

| 청구항 요소 | 발명의 설명 단락 | 도면 참조 | 구체적 실시예 |
|------------|----------------|----------|-------------|
| [요소 1] | [0001]-[0003] | 도 1, 부호 110 | [구체적 구현] |
| [요소 2] | [0004]-[0006] | 도 2, 부호 210 | [구체적 구현] |

This matrix is the PRIMARY deliverable — claims and specification are built
FROM this matrix, not the other way around.

**MANDATORY**: Write the completed matrix to `outputs/patent-kr/{date}/support-basis-matrix.md` **before** proceeding to Step 3 (claim drafting). Do NOT draft any claim until the matrix file exists on disk. If the file cannot be persisted, STOP and report the error.

### Step 3: Draft Claims (청구항)

**Korean claim structure**:

```
【청구항 1】
[구성요소 A]와,
[구성요소 B]를 포함하며,
상기 [구성요소 A]는 [기능/특성]을 수행하고,
상기 [구성요소 B]는 [조건]에 기초하여 [동작]을 수행하는 것을 특징으로 하는
[발명의 명칭].
```

**Drafting rules (Korean-specific)**:
- 주어-목적어-동사 (SOV) 어순 준수
- "상기" (前記) 를 사용하여 선행 구성요소 참조
- "특징으로 하는" (characterized by) 으로 독립항 마무리
- 종속항은 "제N항에 있어서" 로 시작
- 각 구성요소는 명세서의 구체적 단락과 1:1 대응 필수
- **1:1 Verification Pass**: After specification drafting, iterate every claim element and confirm it maps to (a) a specific specification paragraph number and (b) a drawing reference numeral. Record unmapped elements and resolve them before finalizing.

**Claim categories**:
- 독립항 (Independent): 방법 발명, 장치 발명, 컴퓨터 판독 가능 기록매체
- 종속항 (Dependent): "제N항에 있어서, ... 것을 특징으로 하는 [명칭]"

**3-Category Gate**: After completing claim drafting, count independent claim categories. If fewer than 3 categories (방법, 장치, 기록매체/프로그램) exist, STOP and draft the missing category before proceeding to the specification.

**AI/SW invention claims** (KIPO guidelines):
- Hardware-software cooperation must be explicitly stated
- Include "프로세서" and "메모리" in system claims
- Method claims tied to specific hardware operation
- Avoid purely abstract data manipulation

**AI/SW Enforcement Gate**: When the invention involves AI, ML, or software, verify the following before finalizing claims: (1) at least one system/apparatus claim contains "프로세서" AND "메모리", (2) method claims reference hardware execution context, (3) specification describes HW-SW cooperation. If any check fails, add the missing elements before proceeding.

### Anti-Patterns (청구항·명세서)

1. 청구항에 **구현 특정 용어**("파이썬", "리눅스", "AWS" 등) 사용 금지 — **기술 중립적** 표현 사용 ("프로세서", "저장 장치", "클라우드 컴퓨팅 환경" 등).
2. **하나의 독립항**에 **구성요소를 5개 이상** 나열·한정하는 과도한 나열 금지 — 거절·명확성 리스크 증가; 종속항으로 분할한다.
3. **"상기"**를 **선행 기재 없이** 사용 금지 — 반드시 이전에 해당 구성요소가 언급된 뒤에만 사용한다. **"상기" Scan**: After completing each independent claim, run a linear scan of the claim text — for every occurrence of "상기 X", verify that "X" appears verbatim earlier in the same claim. Flag and rewrite any dangling "상기" before finalizing.
4. 명세서에서 **청구항 문구를 그대로 복붙**하는 단락 금지 — **구체적 실시예**, 수치·동작·대안 실시형태를 덧붙인다.
5. **뒷받침 매트릭스**(Step 2) 완성 전에 청구항 최종 확정 금지.
6. **AI/SW 발명**에서 **프로세서/메모리 없는** 순수 방법 청구항만으로 끝내는 서술 금지 — 필요 시 장치·기록매체 독립항과 HW 연계를 병기한다.

### Worked Example: LLM 에이전트 오케스트레이션 (독립 방법항)

**발명 예시**: 스킬 레지스트리·의미 검색 라우팅·DAG 실행·자원 인지형 모델 선택을 결합한 멀티 에이전트 워크플로우 플랫폼.

**예시 독립 방법청구항** (실제 출원 전 선행 조사·보정 필요):

```
【청구항 1】
사용자로부터 작업 기술(task description)을 수신하는 단계;
스킬 레지스트리에 저장된 에이전트 스킬의 메타데이터와 상기 작업 기술 간의 임베딩 유사도에 기초하여, 후보 에이전트 스킬 세트를 검색하는 단계;
상기 후보 에이전트 스킬 간의 의존 관계에 기초하여, 실행 순서를 나타내는 방향성 비순환 그래프(DAG)를 구성하는 단계;
상기 작업 기술로부터 도출된 복잡도 신호에 기초하여, 상기 DAG의 각 노드에 대해 복수의 언어 모델 계층 중 하나를 선택하는 단계; 및
상기 DAG를 실행하되, 각 에이전트 스킬을 선택된 언어 모델 계층에 디스패치하고, 체크포인트 노드에서 실행 결과를 영속화하여 장애 복구를 가능하게 하는 단계
를 포함하는, 프로세서에 의해 수행되는 멀티 에이전트 워크플로우 오케스트레이션 방법.
```

### Step 4: Draft Specification (발명의 설명)

Standard KIPO specification structure:

1. **발명의 명칭** (Title of Invention)
2. **기술분야** (Technical Field): 한 단락
3. **발명의 배경이 되는 기술** (Background Art):
   - 종래기술의 문제점 기술
   - 선행기술문헌 인용 (특허문헌, 비특허문헌)
4. **발명의 내용** (Disclosure of the Invention):
   - 해결하고자 하는 과제 (Technical Problem)
   - 과제의 해결수단 (Solution to Problem)
   - 발명의 효과 (Advantageous Effects)
5. **도면의 간단한 설명** (Brief Description of Drawings)
6. **발명을 실시하기 위한 구체적인 내용** (Detailed Description):
   - 각 도면별 상세 설명
   - 모든 부호 일관성 유지
   - 각 청구항 요소에 대응하는 단락 명시
   - "~하는 것이 바람직하다", "~할 수 있다" 등 실시예 표현
   - 수치 한정 시 한정 이유 및 범위 근거 기재
7. **부호의 설명** (Description of Reference Numerals)

**Support-basis rule** (Article 42(4)):
Every claim element must be described in the detailed description with
sufficient specificity that a person skilled in the art (통상의 기술자) can
reproduce it. Check against the support-basis matrix from Step 2.

### Step 5: Draft Abstract (요약서)

- 400자 이내 (approximately 200 words)
- 대표도면 지정 (e.g., "대표도: 도 1")
- 기술적 과제, 해결수단, 효과를 간결히 기술
- **Length Gate**: After drafting the abstract, count Korean characters (excluding spaces and punctuation). If count exceeds 400, trim to ≤400 by removing secondary effects or implementation details. Report the final character count in the output.

### Step 6: English Reference Translation

Produce a parallel English translation of:
- Claims (for PCT/Paris Convention reference)
- Abstract
- Key specification paragraphs

Mark as "Reference translation — not for filing"

### Step 7: Cross-Verification

| Check | Standard | Pass Criteria |
|-------|----------|---------------|
| Support basis | Art. 42(4) | Every claim element → spec paragraph + drawing |
| Enablement | Art. 42(3) | PHOSITA can reproduce from spec alone |
| Clarity | Art. 42(4) | No ambiguous terms, consistent terminology |
| Unity | Art. 45 | All claims relate to single inventive concept |
| Numeral consistency | KIPO guidelines | Every numeral matches across drawings and spec |

### Step 8: Persist Output

Write to `outputs/patent-kr/{date}/`:
- `draft-claims-kr.md` — claims in Korean
- `draft-specification-kr.md` — full specification in Korean
- `draft-abstract-kr.md` — abstract in Korean
- `draft-claims-en.md` — English reference translation of claims
- `support-basis-matrix.md` — claim-to-specification traceability
- `cross-verification.md` — verification results

### Step 9: Pre-Delivery Check

Step 8(저장) 이후, 사용자·변리사 전달 직전에 다음을 **자체 검증**한다. 하나라도 미충족이면 초안을 보완하고 재검증한다.

| # | 검증 항목 | 기준 |
|---|-----------|------|
| (a) | 뒷받침 매트릭스 | **모든** 청구항 요소가 Step 2 매트릭스에 매핑되었는지 |
| (b) | 독립항 구성 | 독립항 최소 **3**개: **방법**, **장치**, **기록매체**(또는 프로그램) 존재 여부 |
| (c) | "상기" 참조 | 모든 "상기"에 대응하는 **선행 기재**가 앞 단락·문장에 존재하는지 |
| (d) | 단락 번호 | 명세서 **[0001]** 등 단락 번호 체계가 도면·발명의 설명 전반에서 **일관**되는지 |
| (e) | 요약서 길이 | 요약서 **400자 이내** |
| (f) | AI/SW 발명 | 해당 시 **HW-SW 협동** 기재(프로세서·메모리·연동)가 방법·장치 명세에 반영되었는지 |
| (g) | 부호 일관성 | 도면 ↔ 명세서 ↔ 청구항에서 **동일 구성요소 동일 부호** |

## Output Artifacts

| Artifact | Path | Format |
|----------|------|--------|
| Claims (Korean) | `outputs/patent-kr/{date}/draft-claims-kr.md` | Markdown |
| Specification (Korean) | `outputs/patent-kr/{date}/draft-specification-kr.md` | Markdown |
| Abstract (Korean) | `outputs/patent-kr/{date}/draft-abstract-kr.md` | Markdown |
| Claims (English ref.) | `outputs/patent-kr/{date}/draft-claims-en.md` | Markdown |
| Support-basis matrix | `outputs/patent-kr/{date}/support-basis-matrix.md` | Markdown |
| Cross-verification | `outputs/patent-kr/{date}/cross-verification.md` | Markdown |

## Constraints

- All primary outputs in Korean (한국어)
- English reference translation provided separately — not for filing
- AI-generated drafts require 변리사 (patent attorney) review before filing
- Support-basis matrix MUST be complete before finalizing claims
- Korean patent terminology must follow KIPO standard glossary (특허 용어집)

## Gotchas

- Korean amendment rules are strict: you CANNOT add new matter to claims
  that was not in the original specification. Draft specifications broadly
  to preserve amendment flexibility
- 분할출원 (divisional application) planning: if the invention has multiple
  inventive concepts, describe all of them thoroughly in the specification
  even if only claiming one initially
- AI/SW inventions: KIPO requires demonstrating hardware-software cooperation.
  Purely algorithmic claims without hardware elements are likely rejected
- 국내우선권 (domestic priority): can be claimed within 1 year of first
  Korean filing — plan specification breadth accordingly
- Number formatting: Korean specifications use 【】 brackets for section
  headings and [0001], [0002] for paragraph numbering
- Korean patent term: 20 years from filing date (not issue date)
- Examination request: must be filed within 3 years of filing (5 years for
  applications filed before 2017-03-01)
