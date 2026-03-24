# State specification template (implementation-ready)

Per screen or major component, list every user-visible state.

## Table template

```markdown
## 상태 정의서

### [화면명] 상태 목록

| 상태 | 진입 조건 | UI 표시 | 가능한 액션 |
|------|----------|---------|------------|
| 초기 (idle) | | | |
| 입력 중 (editing) | | | |
| 로딩 (loading) | | | |
| 성공 (success) | | | |
| 에러 (error) | | | |
| 빈 값 (empty) | | | |
| 비활성 (disabled) | | | |
```

## Figma cross-check (when design URL provided)

- Compare design variants vs this table; flag missing error/empty/loading states.
- Note token usage vs design system expectations.
