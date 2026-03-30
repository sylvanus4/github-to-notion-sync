# State & Edge Case Checklist

Auto-generation template for state coverage and edge case analysis in PRDs.

## Standard States

Every interactive feature should define behavior for these states:

| State | Description | Must Define |
|-------|-------------|-------------|
| **Default/Initial** | First load, before any user action | UI appearance, default values |
| **Loading** | Async operation in progress | Loading indicator, interaction blocking |
| **Empty** | No data available | Empty state message, CTA |
| **Partial** | Some data loaded, more available | Pagination/infinite scroll behavior |
| **Success** | Operation completed successfully | Confirmation, next steps |
| **Error (validation)** | User input invalid | Inline error messages, field highlighting |
| **Error (network)** | Network request failed | Retry option, offline message |
| **Error (server)** | Server returned error | Error message, support contact |
| **Error (auth)** | Authentication/authorization failed | Login redirect, permission message |
| **Timeout** | Operation exceeded time limit | Timeout message, retry option |
| **Permission denied** | User lacks required permissions | Access request flow |
| **Disabled** | Feature temporarily unavailable | Disabled state UI, reason |

## Standard Edge Cases

### Input Edge Cases

- [ ] 빈 값 제출
- [ ] 최소/최대 길이 경계값
- [ ] 특수문자 및 이모지 입력
- [ ] 매우 긴 텍스트 입력
- [ ] 복사-붙여넣기 대량 데이터
- [ ] XSS/SQL Injection 시도

### Concurrency Edge Cases

- [ ] 동시 요청 (같은 리소스에 복수 사용자)
- [ ] 동시 편집 (conflict resolution)
- [ ] 중복 제출 (더블 클릭)
- [ ] 요청 중 페이지 이탈

### Navigation Edge Cases

- [ ] 뒤로 가기 (브라우저 뒤로)
- [ ] 새로고침
- [ ] 딥링크 직접 접근
- [ ] 탭 전환 후 복귀
- [ ] 세션 만료 후 동작

### Data Edge Cases

- [ ] 대용량 데이터 (1000+ items)
- [ ] 데이터 없음 → 데이터 생성 전환
- [ ] 삭제된 데이터 참조
- [ ] 시간대(timezone) 차이
- [ ] 다국어/RTL 텍스트

## Auto-Generation Rules

When generating the checklist for a specific feature:

1. Include ALL standard states
2. Mark each as "Defined" or "Not Defined" based on source material
3. For undefined states, suggest default behavior based on common patterns
4. Add feature-specific edge cases beyond the standard list
5. Prioritize: states with user-visible impact first
