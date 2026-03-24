# Skill Evolution Configuration

Cross-Team Automation 스킬의 진화(Evolution) 인프라 설정.
`skill-autoimprove` 실행 시 이 파일을 참조합니다.

## 진화 대상 스킬 레지스트리

| Skill | Version | Category | Eval Count | Baseline Target | Status |
|-------|---------|----------|------------|-----------------|--------|
| doc-quality-gate | 2.0.0 | quality | 7 | 80% | Unified (checker+gate+inspector) |
| policy-text-generator | 1.0.0 | execution | 5 | 85% | Initial |
| code-to-spec | 2.0.0 | analysis | 6 | 80% | Unified |
| code-spec-comparator | 1.0.0 | analysis | 4 | 80% | Initial |
| design-system-tracker | 2.0.0 | tracking | 4 | 80% | Unified (tracker+changelog+change-tracker) |
| spec-assembler | 1.0.0 | execution | 5 | 80% | Initial |
| tech-doc-translator | 2.0.0 | generation | 6 | 85% | Unified (translator+explainer+context-advisor) |

## 진화 파이프라인

```
Step 1: Audit        → skill-optimizer audit 모드로 구조 점검
Step 2: Baseline     → 각 스킬의 Eval Criteria로 현재 성능 측정
Step 3: Autoimprove  → skill-autoimprove 루프 실행 (one-mutation-at-a-time)
Step 4: Verify       → 개선된 스킬을 fresh inputs로 검증
Step 5: Version      → 개선 시 metadata.version 범프
```

## 최적화 체크리스트 (모든 스킬 공통)

### 구조 최적화 (Applied)

- [x] YAML frontmatter: name, description (>- format), metadata (author, version, category)
- [x] Description에 Use when / Do NOT use / Korean triggers 포함
- [x] Input 테이블: Parameter, Required, Description
- [x] Workflow: 번호 매겨진 Phase 구조
- [x] Output Contract (Quality Gate) 섹션
- [x] Skill Chain 테이블
- [x] Examples 섹션 (최소 3개)
- [x] Error Handling 테이블
- [x] Evolution 섹션 (Eval Criteria + Autoimprove Hook)

### 라우팅 최적화 (Applied)

- [x] 한국어 + 영어 트리거 동시 지정
- [x] Do NOT use로 오용 방지 경로 명시
- [x] 인접 스킬과의 경계 명확화 (최소 3개 Do NOT)
- [x] 스킬 체인 테이블로 후속 스킬 연결

### 품질 게이트 최적화 (Applied)

- [x] 모든 출력에 필수 포함 항목 명시 (Output Contract)
- [x] 검증 가능한 조건으로 품질 기준 정의
- [x] 실패 시 대응 방법 명시 (Error Handling)

### 진화 인프라 (Applied)

- [x] Binary Eval Criteria (Yes/No, 스케일 없음)
- [x] Autoimprove Hook (Test inputs, Baseline target, Mutation focus)
- [x] 버전 관리 (metadata.version)

## Autoimprove 실행 가이드

### 준비물

각 스킬의 `## Evolution` 섹션에 정의된:
1. **Eval Criteria** — Binary 평가 기준
2. **Test inputs** — 3종 테스트 입력
3. **Baseline target** — 목표 Pass rate
4. **Mutation focus** — 개선 방향

### 실행 명령

```
/skill-autoimprove --target .cursor/skills/<skill-name>/SKILL.md
```

### 권장 실행 순서

1. `doc-quality-gate` — 다른 스킬의 품질 검증에 사용되므로 최우선
2. `policy-text-generator` — 정책 정합성이 중요한 스킬
3. `code-to-spec` — 추출 정확도가 핵심
4. `spec-assembler` — 정보 보존율이 핵심
5. `tech-doc-translator` — 정확성 보존이 핵심
6. `design-system-tracker` — 변경 감지 정확도

### 진화 기록

진화 결과는 각 스킬 폴더의 `autoimprove-<skill-name>/` 디렉토리에 저장:
- `dashboard.html` — 실시간 대시보드
- `results.tsv` — 실험 결과 로그
- `changelog.md` — 뮤테이션 기록
- `SKILL.md.baseline` — 원본 백업

## 스킬 간 의존성 그래프

```
doc-quality-gate ←── policy-text-generator (점검 후 문구 생성)
        ↑                      ↑
        │                      │
spec-assembler ──────── code-to-spec (코드 소스 통합)
        ↑
        │
meeting-digest (회의록 소스)
        
design-system-tracker → doc-quality-gate (변경 후 문서 재점검)

tech-doc-translator ←── code-to-spec (역기획서 청중 변환)
```

## 버전 범프 규칙

- **Patch** (1.0.x): Eval Pass rate 5%+ 향상, 에러 핸들링 추가
- **Minor** (1.x.0): 새 Phase 추가, 새 Eval Criteria 추가, 레퍼런스 파일 대폭 확장
- **Major** (x.0.0): 워크플로우 구조 변경, 입출력 계약 변경
