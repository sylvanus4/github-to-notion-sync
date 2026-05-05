# Session Management Best Practice

## Scope Discipline
- 한 세션 = 1 major deliverable. 별개 도메인은 `/clear` 후 분리.
- 관련 인프라끼리는 묶을 수 있음 (MCP + env), 무관한 작업은 분리 (infra vs. pipeline)
- 4개 이상 무관한 task 감지 시 Claude가 우선순위 확인 후 순차 처리 제안

## Context Window Hygiene
- Context 사용률 40% 이하 유지 (경험 많으면 30%)
- 60% 초과 시 세션 종료/교체 검토
- Auto-compact 전에 `/compact [focus hint]` 수동 실행 권장

## Session Control
- `/context`: 컨텍스트 사용량 + 부풀림 원인 진단. 새 세션 시작 시, 느려진다 싶을 때 먼저 실행
- `/clear`: 50% 도달 시 즉시 실행. 새 task 시작 또는 도메인 전환 시
- `/compact [hint]`: 같은 task 연속 시
- `/rewind` (Esc-Esc): 실패한 접근 즉시 되돌리기 -- 잘못된 context 누적 방지
- `/rename` + `/resume`: 멀티 세션 관리
- 세션 시작 전 prompt를 먼저 정리 -- 의도 없이 세션 열고 바로 /exit 패턴 방지

## Quality Amplifiers
- Plan Mode에서 시작 (Shift+Tab x2) -- 복잡한 task
- `ultrathink` 키워드 -- extended thinking 최대 활성화
- Claude에게 검증 방법 제공 시 품질 2-3x 향상
- "grill me on these changes" -- 검증 강제 패턴
