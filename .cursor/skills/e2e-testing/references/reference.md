# E2E Testing Reference

기존 E2E 테스트 파일별 패턴과 프로젝트 아키텍처 상세 참조.

## Existing Test Files

### auth.spec.ts
- 로그인/로그아웃, 리다이렉트, 에러 표시, 헤더 사용자명 검증
- `ensureLoggedOut()` 패턴: localStorage clear → reload
- CSS selector로 input 접근: `input[type="email"]`, `input[type="password"]`

### call-flow.spec.ts
- 통화 시작/종료, 타이머 표시, 트랜스크립트/추천 패널 대기 메시지
- Role 기반 selector: `getByRole("button", { name: /start call/i })`
- URL 패턴 매칭: `/call/.*\/summary/`

### chatbot.spec.ts
- FAB 클릭 → 패널 열기, 메시지 전송, 응답 대기, 패널 닫기
- `data-testid` 집중 사용: `chatbot-fab`, `chatbot-panel`, `chatbot-input`, `chatbot-send`, `chatbot-close`
- CSS 애니메이션 처리: `toHaveCSS("opacity", "0")`

### dashboard.spec.ts
- 메트릭 카드 검증, 시스템 상태 표시
- `getByText` 기반 정적 텍스트 확인
- `{ exact: true }` 옵션으로 부분 매치 방지

### summary.spec.ts
- API mock 패턴 (`page.route`)으로 summary-crm 서비스 의존 제거
- 통화 시작→종료→요약 페이지 전체 플로우
- textarea 편집 및 discard 네비게이션

### file-upload.spec.ts
- `setInputFiles()` mock 버퍼 패턴
- `data-testid`: `audio-drop-zone`, `audio-file-input`

### i18n.spec.ts
- 다국어 전환 테스트
- localStorage language 설정 변경

### help-tooltips.spec.ts
- 도움말 팝업 표시/숨기기
- `data-testid`: `help-trigger-{key}`, `help-popup-{key}`

## Known data-testid Values

| testid | Component | Location |
|--------|-----------|----------|
| `chatbot-fab` | 챗봇 FAB 버튼 | 전역 |
| `chatbot-panel` | 챗봇 패널 | 전역 |
| `chatbot-input` | 챗봇 입력 필드 | 챗봇 패널 |
| `chatbot-send` | 챗봇 전송 버튼 | 챗봇 패널 |
| `chatbot-close` | 챗봇 닫기 버튼 | 챗봇 패널 |
| `audio-drop-zone` | 오디오 드롭존 | 통화 화면 |
| `audio-file-input` | 오디오 파일 입력 | 통화 화면 |
| `help-trigger-{key}` | 도움말 트리거 | 각 Feature |
| `help-popup-{key}` | 도움말 팝업 | 각 Feature |

## Backend Services Architecture

E2E 테스트 시 관련 서비스 참조:

| Service | Port | E2E 관련도 |
|---------|------|-----------|
| frontend | 5173 | 테스트 대상 |
| call-manager (Go) | 8010 | 통화 API (`/api` 프록시) |
| admin (Python) | 8018 | 인증/관리자 API (`/api/v1/auth`, `/api/v1/tenants`) |
| summary-crm | 8016 | 통화 요약 (mock 권장) |
| stt-pipeline | 8011 | 음성→텍스트 |
| rag-engine | 8013 | 지식 검색 |
| knowledge-manager | 8015 | 지식 관리 |

### Vite Proxy 설정
- `/api` → call-manager (8010)
- `/ws` → call-manager (8010) WebSocket
- `/api/v1/auth`, `/api/v1/tenants`, `/api/v1/audit-logs`, `/api/v1/health`, `/api/v1/users`, `/api/v1/config`, `/api/v1/licenses`, `/api/v1/api-keys` → admin (8018)

## Test Credentials (Seeded)

| Role | Email | Password |
|------|-------|----------|
| Agent (기본) | `minjun@demo.example` | `changeme123` |

> Admin 사용자 정보는 `make db-seed` 실행 결과 확인.

## Feature Flags

E2E에 영향을 줄 수 있는 Feature Flag:

- `FF_STT_ENABLED` — STT 기능 활성화
- `FF_RECOMMENDATIONS_ENABLED` — 추천 기능 활성화
- `FF_SUMMARY_ENABLED` — 요약 기능 활성화
- `FF_RAG_ENABLED` — RAG 검색 활성화
- `FF_PILOT_ONLY` — 파일럿 모드 제한

## Troubleshooting

### Rate Limiting
global-setup.ts가 Redis rate-limit 키를 자동 플러시하지만, 수동 초기화 필요 시:

```bash
docker exec aa-redis redis-cli EVAL \
  "local keys = redis.call('KEYS','ratelimit:*'); if #keys > 0 then return redis.call('DEL',unpack(keys)) else return 0 end" 0
```

### Seed Data 재설정
```bash
make db-seed
```

### 서비스 상태 확인
```bash
docker compose -f docker-compose.yml -f docker-compose.services.yml ps
```

### Playwright 브라우저 설치
```bash
cd frontend && npx playwright install chromium
```
