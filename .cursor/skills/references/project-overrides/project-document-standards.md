# Project Document Standards — AI Stock Analytics

> Override for cloud-platform document standards.
> Source: `docs/policies/04-document-quality-standards.md` (POL-004)

## Quality Gate — 7 Dimensions

| # | Dimension | Weight | Description |
|---|-----------|--------|-------------|
| 1 | Completeness | 20% | All required sections present |
| 2 | State Coverage | 15% | All data states mapped (loading/empty/error/success/partial) |
| 3 | Exception Handling | 15% | Edge cases documented |
| 4 | Policy Compliance | 15% | Aligns with POL-001~006 |
| 5 | Terminology Consistency | 10% | No forbidden terms, consistent glossary |
| 6 | API Consistency | 15% | Endpoints match code |
| 7 | UI/Design References | 10% | Refers to design-system.mdc, not Figma |

## Grading

| Grade | Score | Action |
|-------|-------|--------|
| A | 90-100% | Approved |
| B | 75-89% | Minor fixes, proceed |
| C | 60-74% | Significant revision needed |
| D | <60% | Rewrite required |

## AI-Generated Report Standards

1. **Accuracy**: All prices, volumes, indicators must match DB data
2. **No Hallucination**: No fabricated ticker names, dates, or metrics
3. **Source Citation**: Cite data source (Yahoo Finance, DB query)
4. **Date Consistency**: Report date = analysis date in outputs
5. **Disclaimer**: Mandatory "정보 제공 목적" notice on trading signals
6. **Korean Primary**: Body in Korean; English for proper nouns and abbreviations only

## PRD Template Sections

1. 개요 (Overview)
2. 배경 및 목적 (Background & Purpose)
3. 사용자 시나리오 (User Scenarios)
4. 기능 요구사항 (Functional Requirements)
5. 비기능 요구사항 (Non-functional Requirements)
6. 상태 매트릭스 (State Matrix)
7. 예외 상황 (Exception Handling)
8. API 명세 (API Specification)
9. UI/UX 가이드 (UI/UX Guide — ref design-system.mdc)
10. 테스트 시나리오 (Test Scenarios)
