# GPU Dashboard Ops

GPU Dashboard 서버를 체크, 실행, 재시작하는 운영 스킬.

**경로**: `tools/gpu-dashboard/`
**서버**: Node.js + Express (`server.js`)
**포트**: `PORT` 환경변수 또는 기본 `3000`

## Trigger

- "GPU 대시보드 시작", "GPU dashboard start", "대시보드 재시작", "대시보드 상태 확인"
- "gpu-dashboard-ops", "GPU 대시보드 체크", "대시보드 서버 실행"
- "TEST_MODE로 실행", "대시보드 테스트 모드"

## Constraints

- Do NOT use for K8s manifest validation (use helm-validator or k8s-manifest-validator).
- Do NOT use for GPU pod deployment (use mlops-k8s-access).
- Do NOT use for GPU resource inspection without the dashboard (use gpu-resource-inspector).

## Modes

| Mode | 설명 |
|------|------|
| `check` | 서버 프로세스 실행 여부 + 포트 응답 확인 |
| `start` | 서버 미실행 시 백그라운드로 시작 |
| `restart` | 기존 프로세스 종료 → 재시작 |
| `stop` | 실행 중인 서버 프로세스 종료 |
| `test` | Playwright E2E 테스트 실행 |

## Procedure

### Phase 1 — Health Check

```bash
# 1-a. 프로세스 확인
lsof -i :3000 -t 2>/dev/null

# 1-b. HTTP 응답 확인 (프로세스 존재 시)
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/cluster-summary
```

**판정 기준**:
- 프로세스 없음 → `STOPPED`
- 프로세스 있고 HTTP 200 → `HEALTHY`
- 프로세스 있고 HTTP 비정상 → `UNHEALTHY` (재시작 필요)

### Phase 2 — Start / Restart

```bash
# 작업 디렉토리 이동
cd tools/gpu-dashboard

# 의존성 확인 (node_modules 없으면 설치)
[ -d node_modules ] || npm install

# TEST_MODE 실행 (실제 K8s 클러스터 없이 mock 데이터)
TEST_MODE=true node server.js

# LIVE 모드 실행 (kubectl 필요, context: tkai-demo)
node server.js
```

**재시작 시**:
```bash
# 기존 프로세스 종료
kill $(lsof -i :3000 -t) 2>/dev/null
sleep 1

# 재시작
cd tools/gpu-dashboard
TEST_MODE=true node server.js
```

Shell 도구의 `block_until_ms: 0`으로 백그라운드 실행하고, 서버 시작 로그 확인:
- 정상: `GPU Dashboard running at http://localhost:3000`
- 모드 표시: `Mode: TEST (mock data)` 또는 `Mode: LIVE (kubectl)`

### Phase 3 — 검증

```bash
# API 응답 확인
curl -s http://localhost:3000/api/cluster-summary | head -c 200

# 브라우저 접속 안내
echo "http://localhost:3000"
```

### Phase 4 — E2E 테스트 (선택)

```bash
cd tools/gpu-dashboard
npx playwright test
```

## Environment Variables

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `PORT` | `3000` | 서버 포트 |
| `TEST_MODE` | `false` | `true` 시 mock 데이터 반환 (kubectl 불필요) |

## API Endpoints

| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/cluster-summary` | 클러스터 GPU 요약 |
| GET | `/api/gpu-pods` | GPU 파드 목록 |
| GET | `/api/gpu-utilization/:ns/:pod` | 파드 GPU 사용률 |
| GET | `/api/pending-pods` | Pending GPU 파드 |
| GET | `/api/waste-analysis` | GPU 낭비 분석 |
| POST | `/api/pods/:ns/:pod/delete` | 파드 삭제 |
| POST | `/api/deployments/:ns/:name/scale-zero` | Deployment 중지 |
| POST | `/api/deployments/:ns/:name/delete` | Deployment 삭제 |
| POST | `/api/deployments/:ns/:name/remove-gpu` | GPU 요청 제거 |

## Output

사용자에게 한국어로 결과 보고:
- 서버 상태 (HEALTHY / STOPPED / UNHEALTHY)
- 실행 모드 (TEST / LIVE)
- 접속 URL
- 에러 발생 시 로그 요약
