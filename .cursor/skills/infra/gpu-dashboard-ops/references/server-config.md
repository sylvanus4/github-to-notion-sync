# GPU Dashboard Server Configuration

## 프로젝트 위치

```
tools/gpu-dashboard/
├── server.js          # Express 서버 (메인 엔트리포인트)
├── package.json       # 의존성: express ^4.21.0, @playwright/test ^1.49.0
├── playwright.config.js
├── public/
│   ├── index.html     # SPA 프론트엔드 (i18n, 차트, 모달 포함)
│   └── locales/
│       ├── ko.json    # 한국어
│       └── en.json    # 영어
└── tests/
    └── gpu-dashboard.spec.js  # Playwright E2E 테스트
```

## 실행 명령

```bash
# TEST_MODE (mock 데이터, kubectl 불필요)
cd tools/gpu-dashboard && TEST_MODE=true node server.js

# LIVE 모드 (kubectl 필요, 현재 context의 클러스터에 연결)
cd tools/gpu-dashboard && node server.js

# E2E 테스트
cd tools/gpu-dashboard && npx playwright test
```

## 서버 동작 방식

- `TEST_MODE=true`: `getMockData()` 함수가 kubectl 명령을 가로채서 mock JSON 반환
- `TEST_MODE=false` (기본): `child_process.execSync`로 실제 `kubectl` 명령 실행
- kube-system 네임스페이스 보호: 삭제/수정 API에서 403 반환

## Mock 데이터 구성 (TEST_MODE)

- 노드 5대 (gpu-node-1~5), 각 GPU 1개
- GPU 파드 3개:
  - `ai-serving/qwen-embedding-6f8b4` (GPU 활성, 사용률 85%)
  - `dev/tas-dev-abc12` (GPU idle, 사용률 0%)
  - `default/nginx-xyz99` (Deployment 직접 소유, nvidia-smi 없음)
- Pending 파드 1개: `ml-team/training-job-7x2k`

## 포트 충돌 처리

```bash
# 포트 3000 사용 중인 프로세스 확인
lsof -i :3000

# 강제 종료
kill $(lsof -i :3000 -t)
```
