# Evolution Workflow 상세

autoskill-evolve 파이프라인의 각 단계별 상세 가이드.

## 목차

1. [트랜스크립트 분석 전략](#트랜스크립트-분석-전략)
2. [후보 추출 형식](#후보-추출-형식)
3. [유사도 비교 방법](#유사도-비교-방법)
4. [병합 전략](#병합-전략)
5. [진화 이력 추적](#진화-이력-추적)
6. [보안 검증 상세](#보안-검증-상세)

---

## 트랜스크립트 분석 전략

### 사용자 턴 분류

트랜스크립트의 각 사용자 턴을 다음으로 분류:

| 분류 | 설명 | 스킬 후보 가능성 |
|------|------|-----------------|
| **명령형** | "~해줘", "~만들어줘" | 높음 — 반복되면 스킬 |
| **질문형** | "~어떻게 해?", "~뭐야?" | 중간 — 도메인 지식 스킬 |
| **수정형** | "아니, ~로 바꿔줘" | 낮음 — 기존 스킬 개선 힌트 |
| **확인형** | "맞아", "좋아" | 없음 |

### 패턴 인식 기준

다음 조건을 충족하면 스킬 후보로 판별:

1. **반복성**: 2개 이상 세션에서 유사한 요청 패턴
2. **복잡성**: 3단계 이상의 도구 호출 시퀀스
3. **도메인 전문성**: 특정 도메인 지식이 필요한 작업
4. **구조적 출력**: 일관된 형식의 출력물을 요구

---

## 후보 추출 형식

```yaml
candidate:
  name: "[kebab-case-name]"
  confidence: 0.75
  source_transcript: "[uuid]"
  source_turns: [3, 5, 7]
  description: |
    [WHAT] ...
    [WHEN] ...
    [Do NOT] ...
  core_instructions:
    - "[핵심 지시사항 1]"
    - "[핵심 지시사항 2]"
  triggers:
    korean: ["트리거1", "트리거2"]
    english: ["trigger1", "trigger2"]
  estimated_pattern: "Pipeline | Generator | Reviewer | Tool Wrapper | Inversion"
```

---

## 유사도 비교 방법

### 텍스트 유사도

기존 스킬의 description과 후보의 description을 비교:

1. 트리거 문구 중복도 (50% 이상 중복 시 high similarity)
2. 핵심 지시사항 의미적 유사도
3. 입출력 형식 유사도

### 판정 매트릭스

| 유사도 | 후보 가치 | 결정 |
|--------|----------|------|
| < 0.3 | 무관 | **add** (신규 영역) |
| 0.3 - 0.7 | 추가 가치 있음 | **add** (보완적) |
| 0.7 - 0.9 | 추가 가치 있음 | **merge** (기존 확장) |
| 0.7 - 0.9 | 추가 가치 없음 | **discard** (중복) |
| >= 0.9 | 무관 | **discard** (거의 동일) |

---

## 병합 전략

### 병합 대상 결정

기존 스킬에 후보를 병합할 때:

1. **description 확장**: 새 트리거 문구 추가
2. **워크플로우 보완**: 누락된 단계나 예외 처리 추가
3. **예제 추가**: 새 사용 시나리오 추가
4. **에러 핸들링 보강**: 발견된 에러 케이스 추가

### 버전 범프 규칙

| 변경 범위 | 버전 변화 |
|-----------|----------|
| description 트리거만 추가 | patch (1.0.0 → 1.0.1) |
| 워크플로우 단계 추가 | minor (1.0.0 → 1.1.0) |
| 핵심 동작 변경 | major (1.0.0 → 2.0.0) |

---

## 진화 이력 추적

### 상태 파일 스키마

`.cursor/hooks/state/autoskill-evolution.json`:

```json
{
  "last_processed": "ISO-8601 timestamp",
  "processed_transcripts": ["uuid1", "uuid2"],
  "evolution_count": 42,
  "skills_created": 12,
  "skills_merged": 28,
  "skills_discarded": 15,
  "history": [
    {
      "date": "2026-03-24",
      "transcripts": 5,
      "candidates": 3,
      "added": 1,
      "merged": 1,
      "discarded": 1
    }
  ]
}
```

### 리포트 아카이브

리포트는 `outputs/autoskill-reports/`에 날짜별로 보관:

```
outputs/autoskill-reports/
├── 2026-03-24-evolution.md
├── 2026-03-17-evolution.md
└── 2026-03-10-evolution.md
```

---

## 보안 검증 상세

### 검사 패턴

| 패턴 | 예시 | 판정 |
|------|------|------|
| 시스템 명령 실행 | `rm -rf`, `sudo`, `chmod 777` | BLOCKED |
| 환경 변수 접근 | `process.env.SECRET`, `$API_KEY` | BLOCKED |
| 외부 URL fetch | `curl`, `wget` (의도하지 않은) | WARNING |
| 파일 시스템 광범위 접근 | `/**`, `/etc/`, `/root/` | WARNING |
| 일반 도구 호출 | `Read`, `Write`, `Shell` (범위 내) | SAFE |

### BLOCKED 시 처리

1. 후보 폐기
2. 리포트에 차단 사유 기록
3. 원본 트랜스크립트 UUID 기록 (추후 검토용)
