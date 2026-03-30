# Edge case matrix template (implementation-ready)

Use for every feature in `mode: implementation-ready`. Expand rows per domain.

## Table template

```markdown
## Edge case 매트릭스

### [기능명] Edge Cases

| ID | 입력 조건 | 상태 | 예상 결과 | 우선순위 |
|----|----------|------|----------|---------|
| EC-001 | | | | P1 |
```

## Derivation checklist

- **입력**: 빈 값, 경계값, 형식 오류, 최대/최소, 특수문자, 악의적 입력
- **상태**: 로딩 중, 오프라인, 세션 만료, 동시성, 권한 변경
- **출력**: API 에러, 타임아웃, 부분 성공, 데이터 불일치
- **환경**: 저사양 기기, 느린 네트워크, 구형 브라우저, 다국어

Assign priority P1 (launch blocker) / P2 (near-term) / P3 (later).
