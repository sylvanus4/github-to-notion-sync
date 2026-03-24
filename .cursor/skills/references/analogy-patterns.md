# Analogy Patterns

Reusable analogies for explaining technical concepts to non-technical audiences.

## API & Networking

| Technical Concept | Analogy | Context |
|-------------------|---------|---------|
| API | 식당 주문 창구 — 메뉴(요청)를 주면 음식(응답)이 나옴 | General |
| REST API | 우체국 — 주소(URL)에 편지(데이터)를 보내고 답장을 받음 | General |
| Endpoint | 메뉴판의 개별 메뉴 — 각각 다른 기능을 수행 | API context |
| Request/Response | 질문과 답변 — 특정 형식으로 물어봐야 정확한 답이 옴 | API context |
| Authentication | 건물 출입증 — 신원 확인 후 접근 허용 | Security |
| Authorization | 층별 접근 권한 — 출입증이 있어도 모든 층에 갈 수 있는 건 아님 | Security |
| Rate Limiting | 편의점 구매 수량 제한 — 한 번에 너무 많이 가져갈 수 없음 | Performance |
| Timeout | 전화 연결 대기 — 30초 이상 받지 않으면 끊김 | Performance |
| WebSocket | 전화 통화 — 한 번 연결하면 실시간으로 대화 가능 | Real-time |
| Webhook | 택배 알림 — 상태 변경 시 자동으로 알려줌 | Integration |

## Data & Storage

| Technical Concept | Analogy | Context |
|-------------------|---------|---------|
| Database | 거대한 엑셀 파일 — 표 형태로 데이터 저장 | General |
| Schema | 서류 양식 — 어떤 칸에 어떤 정보를 쓸지 정해진 규칙 | Data structure |
| Cache | 자주 보는 문서를 책상 위에 올려놓기 — 매번 서류함을 안 뒤져도 됨 | Performance |
| Migration | 이사 — 기존 데이터를 새 구조로 옮기는 작업 | Operations |
| Index | 책 뒷면의 색인 — 원하는 정보를 빠르게 찾기 위한 목록 | Performance |

## System Architecture

| Technical Concept | Analogy | Context |
|-------------------|---------|---------|
| Microservice | 전문 식당들이 모인 푸드코트 — 각 식당이 한 가지를 잘함 | Architecture |
| Load Balancer | 은행 번호표 시스템 — 고객을 여러 창구에 분배 | Performance |
| Queue | 대기줄 — 요청을 순서대로 처리 | Processing |
| CI/CD | 자동화된 공장 라인 — 코드 변경이 자동으로 검사되고 배포됨 | DevOps |

## Usage Guidelines

1. Pick analogies familiar to the target audience's daily work
2. Don't force analogies — if the concept is simple enough, explain directly
3. Acknowledge where the analogy breaks down
4. Use the same analogy consistently within one document
