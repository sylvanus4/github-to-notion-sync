# Fidelity Report Template

PRD 생성 시 원본 미팅 콘텐츠와 생성된 PRD를 대조하는 왜곡 모니터링 리포트.

## Report Structure

```markdown
# Fidelity Report

## 문서 메타데이터
- 생성일: YYYY-MM-DD
- 소스 미팅: [meeting title]
- 소스 유형: [source tag]
- PRD 파일: [path]

## Summary
- 전체 팩트 수: N
- 소스 확인 가능: M (XX%)
- 소스 근거 없음: K (XX%) ⚠️
- 왜곡 감지: J (XX%)

## Missing (회의에 있었지만 PRD에 빠진 항목)
| 미팅 내용 | 소스 위치 | 중요도 | 비고 |
|-----------|-----------|--------|------|
| [topic discussed] | L12-L15 | High | 요구사항 관련 |

## Hallucinated (PRD에 있지만 회의에 없는 항목)
| PRD 주장 | PRD 섹션 | 신뢰도 | 제거 권장 |
|----------|----------|--------|-----------|
| [claim in PRD] | 5.1 기능 요구사항 | 32 | Yes |

## Distorted (의미가 변형된 항목)
| 원본 표현 | PRD 표현 | 소스 위치 | 차이점 |
|-----------|----------|-----------|--------|
| "검토 후 결정" | "합의됨" | L45 | 결정 상태 과장 |
```

## Confidence Scoring Rules

### Fact-Level Confidence (0-100)

| Score | Category | Criteria |
|-------|----------|----------|
| 90-100 | Direct Quote | 식별된 발언자의 원문에서 직접 인용 가능 |
| 70-89 | Contextual | 명확한 토론 맥락에서 의역 가능. 원문에 명시적 언급은 없지만 논리적으로 도출 |
| 50-69 | Inferred | 주변 논의에서 추론. 명시적 진술 없음 |
| 0-49 | Unsourced | 소스 자료에서 근거 찾을 수 없음. `[소스 근거 없음]` 표기 |

### Section-Level Confidence

```
Section confidence = Σ(fact_confidence × fact_weight) / Σ(fact_weight)
```

Weight multipliers by fact category:
- Requirements: 1.5x (가장 중요)
- Decisions: 1.3x
- Constraints: 1.0x
- Assumptions: 0.8x (추론 기반이므로 가중치 낮음)

### Source Traceability Table (부록 C)

PRD의 모든 핵심 주장을 소스까지 역추적하는 표:

| PRD 섹션 | 주장 | 소스 위치 | 발언자 | 신뢰도 |
|----------|------|-----------|--------|--------|
| 2. 문제 정의 | 기존 인증 시스템 지연 | L12-L15 | 김개발 | 92 |
| 5.1 기능 요구사항 | OAuth 2.0 도입 | L23-L25 | 김개발 | 95 |
| 7. 타임라인 | Q3 출시 목표 | L45 | 박PM | 78 |

## AI Summary Detection Indicators

소스 콘텐츠가 AI 생성 요약인지 판별하는 지표:

| Indicator | Weight | Description |
|-----------|--------|-------------|
| No speaker names | High | 발언자 이름 없이 "논의됨", "합의됨" 등 수동태 사용 |
| No timestamps | Medium | 시간 순서 정보 없음 |
| Uniform formatting | Medium | 모든 항목이 동일한 불릿 포인트 구조 |
| No hesitations | Low | "음...", "그러니까" 등 구어체 표현 없음 |
| Perfect grammar | Low | 문법적으로 완벽한 문장 (실제 회의에서는 드묾) |
| Summary markers | High | "Summary by Notion AI", "AI가 요약함" 등 명시적 표기 |

3개 이상 High/Medium 지표 해당 시 → `[AI 요약 기반 - 검증 필요]` 태그 부착.

## Drift Log Entry Format

Notion 왜곡 모니터링 로그 페이지에 추가되는 행:

| 날짜 | 미팅 제목 | 소스 유형 | 전체 신뢰도 | 소스 확인률 | 왜곡 수 | 누락 수 | PRD 링크 |
|------|-----------|-----------|------------|------------|--------|--------|----------|
