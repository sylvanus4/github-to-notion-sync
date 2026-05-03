# Session Management Best Practice

## Context Window Hygiene
- Context 사용률 40% 이하 유지 (경험 많으면 30%)
- 60% 초과 시 세션 종료/교체 검토
- Auto-compact 전에 `/compact [focus hint]` 수동 실행 권장

## Session Control
- `/rewind` (Esc-Esc): 실패한 접근 즉시 되돌리기 -- 잘못된 context 누적 방지
- `/clear`: 새 task 시작 시
- `/compact [hint]`: 같은 task 연속 시
- `/rename` + `/resume`: 멀티 세션 관리

## Quality Amplifiers
- Plan Mode에서 시작 (Shift+Tab x2) -- 복잡한 task
- `ultrathink` 키워드 -- extended thinking 최대 활성화
- Claude에게 검증 방법 제공 시 품질 2-3x 향상
- "grill me on these changes" -- 검증 강제 패턴
