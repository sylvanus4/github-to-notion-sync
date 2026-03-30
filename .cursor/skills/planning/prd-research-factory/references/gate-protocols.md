# Human Review Gate Protocols

PRD Research Factory 파이프라인의 3개 검수 게이트 상세 프로토콜.

## Gate Overview

```
Gate 1 (소스 검증)   : Phase 1 완료 후 — 미팅 콘텐츠가 실제와 일치하는지 확인
Gate 2 (팩트 검증)   : Phase 5 완료 후 — PRD 초안 + Fidelity Report 검토
Gate 3 (최종 승인)   : Phase 6 완료 후 — 최종 PRD 업로드 승인
```

## Gate 1: Source Verification

### Purpose
미팅 콘텐츠 인입 직후, 소스 자료의 정확성을 확인.

### Activation
- `--trust-level low`: 활성화 (기본)
- `--trust-level medium`: 자동 통과
- `--trust-level high`: 자동 통과

### Protocol

1. 소스 유형 감지 결과 표시
2. 콘텐츠 요약 (3-5개 핵심 포인트) 제시
3. AI 요약 감지 시 경고 표시
4. 사용자 응답 대기:
   - **계속**: 현재 콘텐츠로 진행
   - **수정**: 사용자가 수정 사항 제공 → 반영 후 진행
   - **중단**: 파이프라인 중단, 현재까지 결과 저장

### Display Template
```
=== Gate 1: 소스 검증 ===
소스 유형: [detected type]
신뢰도: [High/Medium/Low]

📋 콘텐츠 요약:
1. [핵심 포인트 1]
2. [핵심 포인트 2]
3. [핵심 포인트 3]

⚠️ 주의: [AI 요약 기반 소스 경고, 해당 시]

이 내용이 실제 회의 내용과 일치합니까? (계속/수정/중단)
```

## Gate 2: Fact Verification

### Purpose
PRD 초안 생성 후, Fidelity Report와 함께 왜곡 여부를 검토.

### Activation
- `--trust-level low`: 활성화
- `--trust-level medium`: 활성화
- `--trust-level high`: confidence < 70 섹션이 있을 때만 활성화

### Protocol

1. PRD 초안 전체 신뢰도 점수 표시
2. Fidelity Report 요약 (Missing/Hallucinated/Distorted 수)
3. Confidence < 70 섹션 하이라이트
4. 사용자 응답 대기:
   - **계속**: 현재 PRD로 다음 단계 진행
   - **수정**: 사용자가 수정 사항 제공 → 해당 섹션만 재생성 → Fidelity 재검사
   - **중단**: 파이프라인 중단, 초안과 Fidelity Report 저장

### Display Template
```
=== Gate 2: 팩트 검증 ===
PRD 초안이 생성되었습니다.

📊 신뢰도 요약:
- 전체 신뢰도: [score]/100
- 소스 확인률: [XX]%

⚠️ 검증 필요 섹션:
- [섹션명]: [score]/100 — [이유]

📋 Fidelity Report:
- 누락 항목: [N]개
- 소스 근거 없는 항목: [K]개
- 왜곡 감지: [J]개

수정할 내용이 있으시면 알려주세요. (계속/수정/중단)
```

## Gate 3: Final Approval

### Purpose
최종 PRD를 Notion에 업로드하기 전 최종 검토.

### Activation
- `--trust-level low`: 항상 활성화
- `--trust-level medium`: 항상 활성화
- `--trust-level high`: confidence < 70 섹션이 있을 때만 활성화

### Protocol

1. doc-quality-gate 점수 표시
2. 최종 신뢰도 점수 표시
3. 생성된 파일 목록 표시
4. 사용자 응답 대기:
   - **업로드**: Notion 업로드 + 로컬 저장
   - **수정**: 사용자가 최종 수정 → 재검사
   - **로컬만**: Notion 업로드 건너뛰기, 로컬 파일만 유지

### Display Template
```
=== Gate 3: 최종 승인 ===
PRD 최종본이 준비되었습니다.

📊 품질 검사 결과:
- doc-quality-gate 점수: [score]/100
- 전체 신뢰도: [score]/100
- 검증 필요 섹션: [count]개

📁 생성된 파일:
- output/prd/{date}/prd-final.md
- output/prd/{date}/fidelity-report.md
- output/prd/{date}/research-context.md

Notion에 업로드하시겠습니까? (업로드/수정/로컬만)
```

## Trust Level Summary

| Trust Level | Gate 1 | Gate 2 | Gate 3 | 권장 소스 |
|-------------|--------|--------|--------|-----------|
| `low` (기본) | 활성 | 활성 | 활성 | AI 요약, 불확실한 소스 |
| `medium` | 자동통과 | 활성 | 활성 | 수기 회의록, 혼합 소스 |
| `high` | 자동통과 | 조건부 | 조건부 | 원본 트랜스크립트 |
