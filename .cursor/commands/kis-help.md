---
description: "KIS plugin help — command listing, agent overview, common workflows, and error code reference"
---

# KIS Help

## Your Task

User input: $ARGUMENTS

If `$ARGUMENTS` is provided, filter the content below by that keyword and show matching sections.
If no arguments, greet with "안녕하세요! 한국투자증권 KIS OpenAPI 플러그인입니다. 무엇을 도와드릴까요?" and show the command overview.

---

## 커맨드 목록

| 커맨드 | 설명 | 예시 |
|--------|------|------|
| `/kis-auth` | 인증 상태 확인·모의/실전 인증·WebSocket 인증·전환 | `/kis-auth vps` `/kis-auth prod` `/kis-auth switch` |
| `/kis-my-status` | 잔고·보유종목·코스피/코스닥 지수 조회 | `/kis-my-status` `/kis-my-status 잔고` `/kis-my-status 전체` |
| `/kis-setup` | 환경 진단 + 단계별 수정 | `/kis-setup` `/kis-setup check` |
| `/kis-help` | 이 도움말. 키워드 검색 가능 | `/kis-help EGW00201` `/kis-help 주문` |

---

## 에이전트 목록

에이전트는 트리거 문구를 입력하면 자동 실행된다.

| 트리거 문구 | 에이전트 | 단계 | 주요 기능 |
|------------|----------|------|----------|
| "전략 만들어줘", "YAML 전략", "지표 조합" | **kis-strategy-builder** | Step 1 | 10개 프리셋 또는 커스텀 `.kis.yaml` 생성 |
| "백테스트 해줘", "성과 분석", "수익률 확인" | **kis-backtester** | Step 2 | 과거 성과 검증, 파라미터 최적화, HTML 리포트 |
| "신호 확인", "실행해줘", "매수 신호 있어?" | **kis-order-executor** | Step 3 | 신호 생성(BUY/SELL/HOLD) → 모의/실전 주문 |
| "다 해줘", "풀파이프라인", "전략부터 주문까지" | **kis-team** | Step 1→2→3 | 3단계 전체 자동 오케스트레이션 |

---

## 자주 쓰는 흐름

```
# 처음 시작
/kis-auth vps          → 모의투자 인증
/kis-my-status         → 잔고 확인

# 전략 설계 → 검증 → 실행
"RSI 전략 만들어줘"       → kis-strategy-builder
"백테스트 해줘"           → kis-backtester
"삼성전자 신호 확인해줘"   → kis-order-executor

# 한 번에 다
"전략부터 주문까지 다 해줘" → kis-team
```

---

## 오류코드 참조

### EGW 서버 (REST API Gateway)

| 코드 | 메시지 | 대응 |
|------|--------|------|
| EGW00001 | 일시적 오류 | 재시도 |
| EGW00002 | 서버 에러 | 재시도 |
| EGW00003 | 접근 거부 | AppKey/Secret 확인 |
| EGW00103 | 유효하지 않은 AppKey | `/kis-auth` 재인증 |
| EGW00105 | 유효하지 않은 AppSecret | `/kis-auth` 재인증 |
| EGW00201 | **초당 거래건수 초과** | 요청 간격 늘리기 (Rate Limit) |
| EGW00206 | **API 사용 권한 없음** | KIS OpenAPI 신청 필요 |
| EGW00207 | IP 주소 오류 | 허용 IP 등록 확인 |
| EGW00213 | 모의투자 TR 불일치 | TR_ID를 V로 시작하도록 변경 |

### OPSQ 서버 (OPS Queue)

| 코드 | 메시지 | 대응 |
|------|--------|------|
| OPSQ1002 | 세션 연결 오류 | `/kis-auth` 재인증 |
| OPSQ2000 | 계좌번호 유효성 오류 | 계좌번호 확인 |
| OPSQ9997 | JSON 파싱 오류 | JSON 형식 확인 |

### OPSP 서버 (WebSocket 구독)

| 코드 | 메시지 | 대응 |
|------|--------|------|
| OPSP0000 | 구독 성공 | 정상 |
| OPSP0008 | **최대 구독 초과** | 기존 구독 해제 후 재시도 |
| OPSP8996 | **appkey 이미 사용 중** | 기존 WebSocket 연결 종료 후 재연결 |
| OPSP9994 | 유효하지 않은 appkey | `/kis-auth ws` 재인증 |

### 자주 발생하는 오류 빠른 참조

| 상황 | 코드 | 해결책 |
|------|------|--------|
| API 너무 빠르게 호출 | EGW00201 | 초당 1건 이하로 제한 |
| 토큰 만료 | EGW00103/105 | `/kis-auth vps` 또는 `/kis-auth prod` 재인증 |
| 모의투자인데 TR_ID가 T로 시작 | EGW00213 | TR_ID를 V로 시작하도록 변경 |
| WebSocket 중복 연결 | OPSP8996 | 기존 연결 종료 후 재연결 |
| 세션 끊김 | OPSQ1002 | `/kis-auth` 재인증 |

## Constraints

- Present all content in Korean
- When filtering by keyword, show only matching rows/sections
- Reference `/kis-auth` (not `/auth`) for this project's command naming
