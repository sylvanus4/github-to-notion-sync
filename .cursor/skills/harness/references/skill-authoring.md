# Skill Authoring & Testing Guide (Cursor)

## 스킬 파일 구조

```
skill-name/
├── SKILL.md          (필수, <500줄)
│   ├── YAML frontmatter (name, description 필수)
│   └── Markdown 본문
└── references/       (선택, 필요 시 Read로 로딩)
    ├── scripts/      반복/결정적 작업용 코드
    ├── docs/         조건부 로딩 참조 문서
    └── assets/       출력에 사용되는 파일
```

## 작성 원칙

### 1. Why-First (이유 중심)

```markdown
# ❌ 규칙 나열
- ALWAYS use TypeScript
- NEVER use any type
- ALWAYS add error handling

# ✅ 이유 전달
TypeScript를 사용하는 이유는 빌드 타임 에러 방지와 IDE 자동완성이
런타임 디버깅보다 효율적이기 때문이다. any 타입은 이 이점을 무효화한다.

에러 핸들링이 필수인 이유는 에이전트가 실패 시 무한 재시도 대신
명확한 실패 보고를 해야 사용자 시간을 절약하기 때문이다.
```

LLM은 **이유**를 이해하면 명시하지 않은 엣지 케이스에서도 올바른 판단을 내린다. 규칙 목록은 열거되지 않은 상황에서 무력해진다.

### 2. Lean (간결)

SKILL.md 본문 500줄 이내:

| 구분 | SKILL.md에 포함 | references/에 분리 |
|---|---|---|
| 핵심 워크플로우 | ✅ | |
| 판단 기준/원칙 | ✅ | |
| 상세 가이드 | | ✅ |
| 예시 코드 | 1–2개 인라인 | 나머지 분리 |
| 긴 체크리스트 | 요약만 | 전체 분리 |
| 스크립트 | | ✅ |

### 3. 일반화 (Generalization)

```markdown
# ❌ 특정 예시 맞춤 규칙
"매출 관련 입력이면 항상 sales 테이블을 JOIN한다"

# ✅ 원리 기반
"도메인 특화 분석이 필요한 경우, 사용자 입력에서 도메인 키워드를
추출하고 해당 데이터 소스를 우선 탐색한다. 키워드가 불명확하면
가장 관련성 높은 2–3개 소스를 병렬 탐색한다."
```

### 4. 명령형 (Imperative Tone)

```markdown
# ❌ 서술형
"이 스킬은 코드 리뷰를 수행하는 기능을 제공합니다."

# ✅ 명령형
"변경된 파일을 읽고, 보안/성능/유지보수 관점에서 리뷰하라.
이슈를 severity 순으로 정렬하여 보고하라."
```

### 5. Progressive Disclosure (점진적 로딩)

3단계로 정보를 노출한다:

1. **Metadata (description)** — 트리거 판단용. 항상 로딩.
2. **SKILL.md 본문** — 스킬 실행 시 로딩. 핵심 워크플로우와 원칙.
3. **references/** — 필요 시 Read 도구로 로딩. 상세 가이드, 스크립트.

### 6. Script Bundling (스크립트 번들링)

에이전트가 반복 작성하는 코드는 `references/scripts/`에 미리 포함:

```
references/scripts/
├── validate-output.py     # 출력 형식 검증
├── merge-results.sh       # 병렬 결과 병합
└── generate-report.py     # 보고서 생성
```

스크립트를 포함해야 하는 신호:
- 3회 이상 반복되는 코드 패턴
- 결정적(deterministic) 작업 (검증, 변환, 포맷팅)
- 에이전트마다 약간씩 달라져 일관성이 깨지는 작업

---

## Description 작성 — "Pushy" 원칙

description은 스킬의 **유일한** 트리거 메커니즘이다. 적극적으로 작성한다:

### 구조

```
"{핵심 역할 한 문장}. Use when the user asks to {동사1}, {동사2}, ...,
{한국어 트리거1}, {한국어 트리거2}, ..., or {넓은 범위 트리거}.
Do NOT use for {경계 스킬1} (use {대안1}). Do NOT use for {경계 스킬2} (use {대안2})."
```

### 핵심 규칙

| 규칙 | 이유 |
|---|---|
| 모든 관련 동사 나열 | 사용자는 다양한 표현 사용 |
| Korean + English 트리거 | 다국어 사용자 대응 |
| Do NOT use 명시 | 경계 스킬과 명확 구분 |
| 1% 확률도 포착 | 트리거 실패 > 불필요한 트리거 |
| 구체적 대안 명시 | `(use {skill-name})` 형태 |

### 예시

```
"Design and generate coordinated multi-agent skill architectures for
any domain. Use when the user asks to 'build a harness', 'design agent team',
'multi-agent workflow', '하네스 구성', '에이전트 팀 설계', or wants to
create a coordinated multi-agent system. Do NOT use for single-skill
creation (use create-skill). Do NOT use for running existing skills
(invoke directly)."
```

---

## 테스트 방법론

### 1. With-skill vs Without-skill 비교

스킬의 부가가치를 검증하는 가장 기본적인 방법:

| 항목 | With-skill | Without-skill |
|---|---|---|
| 프롬프트 | 동일 | 동일 |
| 스킬 | 활성화 | 비활성화 |
| 평가 | 구조화된 기준 | 동일 기준 |

차이가 미미하면 스킬의 가치가 부족한 것 — 재설계 또는 폐기.

### 2. Assertion 기반 정량 평가

출력에 대한 구체적 assertion으로 채점:

```json
{
  "assertions": [
    { "type": "contains", "value": "## 보안 분석", "weight": 2 },
    { "type": "format", "value": "markdown_with_headers", "weight": 1 },
    { "type": "length_min", "value": 500, "weight": 1 },
    { "type": "no_contains", "value": "TODO", "weight": 3 }
  ]
}
```

### 3. 트리거 검증

Should-trigger와 Should-NOT-trigger 쿼리로 description 품질을 측정:

**Should-trigger (8–10개):**
- 공식적: "에이전트 팀 아키텍처를 설계해줘"
- 캐주얼: "멀티에이전트 하네스 만들어줘"
- 암시적: "이 프로젝트에 맞는 에이전트 구조 잡아줘"
- 영어: "design agent team for this domain"
- 한국어: "하네스 구성해줘"

**Should-NOT-trigger (8–10개):**
- 경계: "이 스킬 최적화해줘" (skill-optimizer 영역)
- 경계: "단일 스킬 하나 만들어줘" (create-skill 영역)
- 무관: "주식 분석해줘"
- 무관: "버그 수정해줘"

### 4. 드라이런 테스트

실제 오케스트레이터를 2–3개 프롬프트로 실행:

1. Phase 순서 논리성 검토
2. 데이터 전달 경로 검증 (파일이 실제 생성되는가)
3. 에러 시나리오 확인 (에이전트 실패 시 폴백)
4. 최종 산출물 완결성 확인

### 5. 반복 개선 프로세스

```
초안 작성 → 테스트 실행 → 평가 → 개선
    ↑                              ↓
    └──────────────────────────────┘

평가 결과 기반 우선순위:
1. 트리거 실패 → description 보강
2. 워크플로우 빈 구간 → Phase 보완
3. 출력 품질 부족 → 원칙/프로토콜 강화
4. 불필요한 트리거 → Do NOT use 추가
```

---

## 테스트 데이터 스키마

### eval_metadata.json

```json
{
  "skill_name": "harness",
  "test_id": "harness-fanout-001",
  "prompt": "코드 리뷰 에이전트 팀을 설계해줘",
  "expected_pattern": "fan-out/fan-in",
  "expected_agents": ["security-reviewer", "performance-reviewer", "style-reviewer"],
  "timestamp": "2026-03-29T10:00:00Z"
}
```

### grading.json

```json
{
  "test_id": "harness-fanout-001",
  "assertions": {
    "pattern_correct": { "passed": true, "weight": 3 },
    "agents_generated": { "passed": true, "weight": 2 },
    "orchestrator_exists": { "passed": true, "weight": 2 },
    "no_trigger_conflict": { "passed": false, "weight": 3, "note": "security-reviewer conflicts with security-expert" }
  },
  "total_score": 7,
  "max_score": 10,
  "grade": "B"
}
```

### timing.json

```json
{
  "test_id": "harness-fanout-001",
  "phases": {
    "domain_analysis": 12.3,
    "team_design": 8.7,
    "skill_generation": 45.2,
    "orchestration": 15.1,
    "validation": 22.8
  },
  "total_seconds": 104.1,
  "token_estimate": 28500
}
```
