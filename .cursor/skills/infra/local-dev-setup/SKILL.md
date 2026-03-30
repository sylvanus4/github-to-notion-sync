---
name: local-dev-setup
description: Go 백엔드 로컬 개발 환경을 자동 설정합니다. Docker DB/NATS 생성, 마이그레이션 적용, 시드 데이터, RSA 키 생성, 인프라 포트포워딩, .env 업데이트, Caddy HTTPS 리버스 프록시 설정을 순차 수행합니다. 로컬 개발 환경, 로컬 셋업, backend 셋업, 환경 구성, 개발 환경 준비, 로컬 실행 요청 시 사용합니다. Do NOT use for 프론트엔드 개발 환경 설정이나 K8s 클러스터 배포.
---

# Local Development Setup

Go 백엔드(`ai-platform/backend/go`) 로컬 개발 환경 자동 설정.

## Prerequisites

| 도구 | 필수 | 용도 |
|------|------|------|
| `docker` | 항상 | PostgreSQL, NATS 컨테이너 |
| `openssl` | 항상 | RSA 키 생성 |
| `make` | 항상 | 마이그레이션, 서버 실행 |
| `migrate` | 자동 설치 | DB 마이그레이션 CLI |
| `caddy` | 항상 (자동 설치) | HTTPS 리버스 프록시 (쿠키 기반 인증 테스트) |
| `kubectl` | full 모드만 | 포트포워딩 |

## Workflow Checklist

```
- [ ] Step 0: 사용자 입력 수집
- [ ] Step 1: Docker 컨테이너 (PostgreSQL + NATS)
- [ ] Step 2: DB 마이그레이션
- [ ] Step 3: 시드 데이터
- [ ] Step 4: RSA 키 생성
- [ ] Step 5: 포트포워딩 (full 모드)
- [ ] Step 5b: S3 크리덴셜 조회 (full 모드)
- [ ] Step 6: .env 업데이트
- [ ] Step 7: Caddy HTTPS 설정
```

---

## Step 0: 사용자 입력 수집

AskQuestion 2개로 셋업 모드를 결정합니다.

**Question 1 — 셋업 모드:**

| id | prompt | options |
|----|--------|---------|
| `setup-mode` | 셋업 모드를 선택하세요 | `local-only`: DB + NATS만 (K8s 불필요) / `full`: 원격 K8s 클러스터 연동 포함 |

**Question 2 — KUBECONFIG 경로 (full 모드만):**

| id | prompt | options |
|----|--------|---------|
| `kubeconfig` | KUBECONFIG 파일 경로 | `~/tkai-local.config` / `~/.kube/config` / `직접 입력` |

"직접 입력" 선택 시 자연어로 경로를 재질문합니다.

**Question 3 — K8s 네임스페이스 (full 모드만):**

| id | prompt | options |
|----|--------|---------|
| `namespace` | S3 크리덴셜을 가져올 K8s 네임스페이스 | `ai-platform-stage` / `ai-platform-prod` / `직접 입력` |

"직접 입력" 선택 시 자연어로 네임스페이스를 재질문합니다.

---

## Step 1: Docker 컨테이너

Working directory: 프로젝트 루트

### PostgreSQL

```bash
docker inspect -f '{{.State.Status}}' ai-platform-database 2>/dev/null || echo 'missing'
```

| 출력 | 액션 |
|------|------|
| `missing` | `docker run -d --name ai-platform-database -e POSTGRES_PASSWORD=password -e POSTGRES_DB=ai_platform_db -p 5432:5432 postgres:15-alpine` |
| `exited` | `docker start ai-platform-database` |
| `running` | 스킵 |

### NATS

```bash
docker inspect -f '{{.State.Status}}' ai-platform-nats 2>/dev/null || echo 'missing'
```

| 출력 | 액션 |
|------|------|
| `missing` | `docker run -d --name ai-platform-nats -p 4222:4222 -p 8222:8222 nats:2.10-alpine -js -p 4222 -m 8222` |
| `exited` | `docker start ai-platform-nats` |
| `running` | 스킵 |

> **참고:** 로컬 Docker NATS는 인증 없이 실행됩니다. K8s NATS는 멀티 어카운트 인증(`LOCAL`/`AGGREGATOR`/`SHARED`)을 사용하지만, local-only 모드에서는 단순화를 위해 인증을 생략합니다. 6222(클러스터 포트)는 단일 노드에서 불필요하므로 제외합니다.

컨테이너 시작 후 `sleep 3`으로 준비 대기.

---

## Step 2: DB 마이그레이션

Working directory: `ai-platform/backend/go`

### .env 파일 확인

```bash
# .env 없으면 기본 템플릿 복사
[ -f .env ] || cp tkai-backend.env .env
```

### 마이그레이션 실행

```bash
make migrate-install
make migrate-up
```

| 출력 | 의미 |
|------|------|
| `no change` | 이미 최신 — 정상 |
| `Dirty database version N` | `make migrate-force version=N` 후 재시도 필요 — 사용자에게 알림 |
| `error: ... connection refused` | DB 컨테이너 미실행 — Step 1 재확인 |

---

## Step 3: 시드 데이터

Working directory: `ai-platform/backend/go`

시드 파일은 `ON CONFLICT DO NOTHING` 방식 — 이미 존재하는 행은 스킵, 없는 행만 삽입.
반복 실행해도 기존 데이터를 삭제/변경하지 않습니다.

시드 파일 존재 여부 먼저 확인:

```bash
ls seeds/seed_all_data.sql 2>/dev/null
```

- **파일 있음:** docker exec로 직접 적용 (apply 스크립트의 interactive 프롬프트 회피)

```bash
docker exec -i ai-platform-database psql -U postgres -d ai_platform_db < seeds/seed_all_data.sql
```

- **파일 없음:** 이 단계를 스킵하고 사용자에게 알림

---

## Step 4: RSA 키 생성

Working directory: `ai-platform/backend/go`

4개 파일 존재 확인:

```bash
ls certs/auth_private_key.pem certs/auth_public_key.pem \
   certs/admin_auth_private_key.pem certs/admin_auth_public_key.pem 2>/dev/null
```

**모두 존재하면 스킵.** 하나라도 없으면 전체 재생성:

```bash
mkdir -p certs
openssl genpkey -algorithm RSA -out certs/auth_private_key.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in certs/auth_private_key.pem -out certs/auth_public_key.pem
openssl genpkey -algorithm RSA -out certs/admin_auth_private_key.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in certs/admin_auth_private_key.pem -out certs/admin_auth_public_key.pem
```

---

## Step 5: 포트포워딩 (full 모드 전용)

**local-only 모드면 이 단계를 완전히 스킵합니다.**

Working directory: `ai-platform/backend/go`

### 실행

KUBECONFIG 경로를 첫 번째 인자로 전달합니다.
TTY가 없는 환경(Cursor Agent)에서는 `IS_INTERACTIVE=false`로 자동 포트 선택됩니다.

```bash
# block_until_ms: 0 으로 백그라운드 실행
./scripts/port-forward-infra.sh "$KUBECONFIG_PATH"
```

### 출력 파싱

1. 터미널 파일을 5초 간격으로 폴링
2. `=== .env 설정 가이드 ===` 마커 탐색 (최대 120초)
3. 마커 ~ `=== Ctrl+C` 구간에서 `KEY="VALUE"` 패턴 추출
4. 주석 처리된 줄(`# KEY=""`)은 인프라 미발견이므로 무시

### 파싱 대상 .env 변수

| 카테고리 | 변수 |
|----------|------|
| NATS | `NATS_URL`, `NATS_SUBJECT_PREFIX`, `STREAM_NAME` |
| KEDA | `KEDA_INTERCEPTOR_URL`, `KEDA_INTERCEPTOR_HOST`, `KEDA_INTERCEPTOR_PORT` |
| VictoriaMetrics | `PROMETHEUS_URL` |
| Workload | `WORKLOAD_BASE_DOMAIN`, `AI_PLATFORM_RELEASE_NAME` |
| MLflow | `MLFLOW_TRACKING_URL` |
| KFP | `KFP_API_URL`, `KFP_NAMESPACE`, `KFP_DEX_USERNAME`, `KFP_DEX_PASSWORD`, `KFP_DEX_AUTH_TYPE`, `KFP_SKIP_TLS_VERIFY` |
| S3 | `S3_ENDPOINT_URL`, `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`, `S3_REGION`, `S3_BUCKET`, `S3_PREFIX`, `S3_CREDENTIALS_SECRET_NAME` |
| Kubernetes | `KUBECONFIG` |

---

## Step 5b: S3 크리덴셜 조회 (full 모드 전용)

**local-only 모드면 이 단계를 완전히 스킵합니다.**

K8s 시크릿에서 S3 크리덴셜을 직접 조회합니다. 포트포워딩 스크립트가 S3 값을 출력하지 않는 경우가 많으므로, 이 단계에서 시크릿을 직접 읽어 확보합니다.

### 1. 사전 검증

kubectl 접근 가능 여부와 네임스페이스 존재를 먼저 확인합니다.

```bash
export KUBECONFIG="$KUBECONFIG_PATH"

# 1-a. 클러스터 인증 확인
kubectl cluster-info --request-timeout=5s 2>&1
```

| 출력 | 액션 |
|------|------|
| `Kubernetes control plane is running at ...` | 정상 — 다음 단계 진행 |
| `error: ... certificate ...` / `Unauthorized` | 사용자에게 알림: "KUBECONFIG 인증 실패. 파일 경로와 토큰 만료 여부를 확인하세요." → S3 단계 스킵 |
| `connection refused` / timeout | 사용자에게 알림: "클러스터 접근 불가. VPN 연결 또는 클러스터 상태를 확인하세요." → S3 단계 스킵 |

```bash
# 1-b. 네임스페이스 존재 확인
kubectl get namespace "$NAMESPACE" --no-headers 2>&1
```

| 출력 | 액션 |
|------|------|
| `$NAMESPACE   Active` | 정상 — 다음 단계 진행 |
| `Error from server (NotFound)` | 사용자에게 알림: "네임스페이스 '$NAMESPACE'가 존재하지 않습니다." → 올바른 네임스페이스를 재질문 (AskQuestion) |

### 2. S3 시크릿 탐색 및 선택

```bash
kubectl get secrets -n "$NAMESPACE" -o name | grep -i s3
```

출력 예시: `secret/s3-credentials`, `secret/ai-platform-stage-backend-s3-secret` 등.

#### 선택 우선순위 (결정적 규칙)

매칭된 시크릿 목록에서 아래 우선순위로 `$S3_SECRET_NAME`을 결정합니다.

| 우선순위 | 패턴 | 예시 |
|----------|------|------|
| 1 (최우선) | 정확히 `s3-credentials` | `secret/s3-credentials` |
| 2 | `*-s3-secret` (접미사 매칭) | `secret/ai-platform-stage-backend-s3-secret` |
| 3 | 위 패턴에 해당하지 않는 첫 번째 매칭 | `secret/my-custom-s3-config` |

#### 결정 플로우

```
매칭 0건 → "S3 시크릿 없음" 안내, S3 설정 스킵 (아래 "매칭 없음" 참조)
매칭 1건 → 해당 시크릿을 $S3_SECRET_NAME으로 사용
매칭 2건+ → 우선순위 적용:
  ├─ 최우선 패턴 1건만 매칭 → 자동 선택
  └─ 동일 우선순위 2건+ → AskQuestion으로 사용자에게 선택 요청
```

**동일 우선순위 복수 매칭 시 AskQuestion:**

| id | prompt | options |
|----|--------|---------|
| `s3-secret` | 여러 S3 시크릿이 발견되었습니다. 사용할 시크릿을 선택하세요 | 매칭된 각 시크릿 이름을 옵션으로 나열 |

#### 매칭 없음 처리

사용자에게 다음 메시지를 출력하고 S3 크리덴셜 단계를 스킵합니다:

```
⚠️ 네임스페이스 '$NAMESPACE'에서 S3 관련 시크릿을 찾지 못했습니다.
   .env의 S3 설정을 수동으로 입력해주세요:
   - S3_ENDPOINT_URL, S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY, S3_REGION
```

### 3. S3 시크릿 디코딩

```bash
kubectl get secret "$S3_SECRET_NAME" -n "$NAMESPACE" \
  -o jsonpath='{.data}' | python3 -c "
import sys, json, base64
d = json.load(sys.stdin)
for k, v in sorted(d.items()):
    print(f'{k}={base64.b64decode(v).decode()}')
"
```

### 4. 파싱 대상 변수

| 시크릿 키 | .env 변수 | 비고 |
|-----------|-----------|------|
| `S3_ACCESS_KEY_ID` | `S3_ACCESS_KEY_ID` | 필수 |
| `S3_SECRET_ACCESS_KEY` | `S3_SECRET_ACCESS_KEY` | 필수 |
| `S3_ENDPOINT_URL` | `S3_ENDPOINT_URL` | 필수 |
| `S3_REGION` | `S3_REGION` | 있으면 적용 |

디코딩 결과에서 위 4개 변수를 추출하여 Step 6에서 .env에 반영합니다.
시크릿에 해당 키가 없으면 기존 .env 값을 유지합니다.

---

## Step 6: .env 업데이트

**파일:** `ai-platform/backend/go/.env`

### full 모드

Step 5(포트포워딩)와 Step 5b(S3 크리덴셜)에서 수집한 각 `KEY="VALUE"` 쌍에 대해 StrReplace 수행:

```
old_string: 기존 KEY="기존값"
new_string: KEY="새값"
```

적용 순서:
1. Step 5 포트포워딩에서 파싱한 인프라 변수 적용
2. Step 5b S3 시크릿에서 파싱한 크리덴셜 적용 (포트포워딩 값보다 우선)

주의사항:
- 주석 줄은 건드리지 않음
- 파싱에서 제외된 변수(인프라 미발견)는 기존 값 유지
- `KFP_DEX_PASSWORD` 등 민감 정보는 빈 문자열이면 기존 값 유지
- S3 크리덴셜은 K8s 시크릿 값이 있으면 반드시 덮어쓰기 (포트포워딩 출력보다 시크릿이 정확)

### local-only 모드

.env 파일이 없었다면 Step 2에서 이미 `cp tkai-backend.env .env` 완료.
로컬 Docker NATS는 인증 없이 실행되므로 `NATS_URL`을 수정해야 합니다:

`.env` 파일에서 `NATS_URL=`로 시작하는 줄을 찾아 **값이 무엇이든** 아래 값으로 교체합니다:

```
1. .env에서 NATS_URL="..." 줄 전체를 Read로 확인
2. StrReplace:
   old_string: NATS_URL="<현재 값 그대로>"   ← Read에서 확인한 실제 줄
   new_string: NATS_URL="nats://localhost:4222"
```

> **주의**: `tkai-backend.env` 템플릿의 기본값은 `NATS_URL="nats://<NATS_USERNAME>:<NATS_PASSWORD>@localhost:4222"`이지만, 이전에 full 모드 셋업이나 수동 편집으로 다른 값이 들어 있을 수 있습니다. 반드시 현재 .env의 실제 줄을 읽어서 old_string으로 사용하세요.

나머지 DB 관련 값(`localhost:5432`)은 기본값 그대로 유지합니다.

---

## Step 7: Caddy HTTPS 설정

`__Secure-` 쿠키 기반 인증은 HTTPS에서만 동작합니다. Caddy를 리버스 프록시로 사용하여 로컬에서 HTTPS를 제공합니다.

고정값:
- **도메인**: `tkai-api-local.thakicloud.net`
- **Caddyfile 위치**: 프로젝트 루트 (`ai-platform-webui/Caddyfile`)
- **참조 가이드**: `ai-platform/backend/go/docs/local/local_caddy_https_guide.md`

### 7-1. Caddy 설치 확인

```bash
which caddy 2>/dev/null
```

| 출력 | 액션 |
|------|------|
| 경로 출력 | 스킵 |
| 빈 출력 | `brew install caddy` |

### 7-2. hosts 파일 확인

```bash
grep -c 'tkai-api-local.thakicloud.net' /etc/hosts 2>/dev/null
```

| 출력 | 액션 |
|------|------|
| `1` 이상 | 스킵 |
| `0` | 사용자에게 수동 실행 안내 (sudo 필요): |

```
⚠️ hosts 파일에 도메인이 등록되어 있지 않습니다. 다음 명령어를 터미널에서 직접 실행해주세요:

echo '127.0.0.1 tkai-api-local.thakicloud.net' | sudo tee -a /etc/hosts
```

### 7-3. Caddy 루트 인증서 신뢰

Caddy CA 인증서가 시스템에 신뢰 등록되어 있는지 확인합니다.

```bash
security find-certificate -a -c "Caddy Local Authority" /Library/Keychains/System.keychain 2>/dev/null
```

| 출력 | 액션 |
|------|------|
| 인증서 정보 출력 | 스킵 |
| 빈 출력 / 에러 | 사용자에게 수동 실행 안내: |

```
⚠️ Caddy 루트 인증서가 신뢰 등록되어 있지 않습니다. 다음 명령어를 터미널에서 직접 실행해주세요 (최초 1회):

sudo caddy trust
```

### 7-4. Caddyfile 생성

Working directory: 프로젝트 루트 (`ai-platform-webui/`)

```bash
ls Caddyfile 2>/dev/null
```

| 출력 | 액션 |
|------|------|
| `Caddyfile` | 파일 내에 `tkai-api-local.thakicloud.net` 포함 여부 확인 → 있으면 스킵, 없으면 덮어쓰기 |
| 빈 출력 | 아래 내용으로 생성 |

Caddyfile 내용:

```
https://tkai-api-local.thakicloud.net {
	tls internal

	handle /api/* {
		reverse_proxy localhost:3000
	}

	handle /swagger/* {
		reverse_proxy localhost:3000
	}

	handle /healthz {
		reverse_proxy localhost:3000
	}

	handle {
		reverse_proxy localhost:5173
	}
}
```

### 7-5. 백엔드 .env 쿠키/CORS 설정

**파일:** `ai-platform/backend/go/.env`

다음 변수들을 StrReplace로 업데이트합니다. 기존 값이 무엇이든 아래 값으로 덮어씁니다.

| 변수 | 값 | 비고 |
|------|-----|------|
| `CORS_ALLOW_ORIGINS` | `"https://thakicloud.net"` | 정적 origin |
| `CORS_ALLOW_ORIGIN_PATTERNS` | `"*.thakicloud.net"` | 서브도메인 동적 매칭 |
| `CORS_ALLOW_CREDENTIALS` | `true` | 쿠키 전송 허용 |
| `COOKIE_SECURE_MODE` | `true` | `__Secure-` 접두사 + `Secure=true` |
| `AUTH_COOKIE_DOMAIN` | `.thakicloud.net` | 서브도메인 간 쿠키 공유 |

`CORS_ALLOW_ORIGIN_PATTERNS` 키가 .env에 존재하지 않으면 `CORS_ALLOW_CREDENTIALS` 줄 바로 위에 새 줄로 삽입합니다.
`COOKIE_SECURE_MODE`, `AUTH_COOKIE_DOMAIN` 키가 .env에 존재하지 않으면 CORS 블록 아래에 새 줄로 삽입합니다.

### 7-6. rspack allowedHosts 확인

**파일:** `ai-platform/frontend/rspack.config.mjs`

`devServer` 블록에 `allowedHosts`가 `.thakicloud.net`을 포함하는지 확인합니다.

```bash
grep -c 'thakicloud.net' ai-platform/frontend/rspack.config.mjs
```

| 출력 | 액션 |
|------|------|
| `1` 이상 | 스킵 |
| `0` | `devServer` 블록의 `host: '0.0.0.0'` 다음 줄에 `allowedHosts: ['localhost', '.thakicloud.net'],` 추가 |

---

## 완료 메시지

모든 단계 완료 후 사용자에게 요약 출력:

```
셋업 완료:
  ✓ PostgreSQL: localhost:5432 (ai_platform_db)
  ✓ NATS: localhost:4222
  ✓ 마이그레이션: 적용 완료
  ✓ 시드 데이터: 적용 완료
  ✓ RSA 키: certs/ 디렉토리
  ✓ 포트포워딩: 실행 중 (full 모드만)
  ✓ .env: 업데이트 완료
  ✓ Caddy: https://tkai-api-local.thakicloud.net → Backend(:3000) + Frontend(:5173)
  ✓ Cookie: __Secure- 모드 (COOKIE_SECURE_MODE=true)

실행 방법:
  1. 백엔드: cd ai-platform/backend/go && make run-server
  2. 프론트엔드: cd ai-platform/frontend && pnpm run dev
  3. Caddy: caddy run --config Caddyfile
  4. 브라우저: https://tkai-api-local.thakicloud.net
```

---

## NATS 아키텍처 참고

K8s 클러스터의 NATS는 **멀티 어카운트 + 3-node StatefulSet** 구조로 운영됩니다.

| 어카운트 | 사용자 | 용도 |
|----------|--------|------|
| `LOCAL` | `local` | 백엔드 서비스 (이벤트 발행/소비) |
| `AGGREGATOR` | `aggregator` | 스트림 수집/집계 |
| `SHARED` | `shared` | LOCAL/AGGREGATOR 스트림 import (교차 접근) |
| `$SYS` | `tkai` | NATS 시스템 모니터링 |

- **네임스페이스**: `nats` (전용), 시크릿(`nats-secret`)은 `ai-platform*` 네임스페이스에 위치
- **인증 정보**: K8s 시크릿 `nats-secret`에서 `NATS_USERNAME`/`NATS_PASSWORD` 키를 자동 조회 (`port-forward-infra.sh`가 처리, 스크립트 내부 셸 변수는 `NATS_USER`/`NATS_PASS`로 축약)
- **JetStream**: 전 어카운트 활성화, 50Gi 파일 스토리지
- **Leafnode**: `thakicloud.site:10701`로 cross-cluster 연결 (aggregator 어카운트)
- **nats-stream-sync**: LOCAL→SHARED/AGGREGATOR 스트림 동기화 워커

> full 모드에서 포트포워딩 시 백엔드는 `LOCAL` 어카운트로 접속합니다.
> `NATS_URL="nats://<NATS_USERNAME>:<NATS_PASSWORD>@localhost:{forwarded_port}"` — 실제 값은 `port-forward-infra.sh`(Step 5)의 `.env 설정 가이드` 출력을 사용하세요.

---

## 트러블슈팅

| 증상 | 해결 |
|------|------|
| `port 5432 already in use` | `docker stop ai-platform-database` 후 재시작, 또는 로컬 PostgreSQL 종료 |
| `Dirty database version N` | `make migrate-force version=N` 후 `make migrate-up` 재실행 |
| `KUBECONFIG 파일 없음` | 올바른 kubeconfig 경로 확인 |
| 포트포워딩 `.env 가이드`가 안 나옴 | kubectl 연결 확인, 클러스터 접근 가능 여부 점검 |
| `migrate: command not found` | `make migrate-install` 실행 |
| kubectl `Unauthorized` / 인증서 에러 | kubeconfig 토큰 만료 여부 확인, `kubectl config view`로 context 점검, 필요 시 토큰 재발급 |
| kubectl `connection refused` / timeout | VPN 연결 확인, 클러스터 API 서버 상태 점검 |
| 네임스페이스 `NotFound` | `kubectl get namespaces`로 사용 가능한 네임스페이스 목록 확인 후 재선택 |
| S3 시크릿 `grep` 결과 0건 | 네임스페이스 내 시크릿 전체 목록 확인: `kubectl get secrets -n $NAMESPACE` → 올바른 네임스페이스인지 재확인 |
| NATS `Authorization Violation` | `NATS_URL`에 인증 정보 확인: full 모드는 포트포워딩 스크립트가 출력한 `NATS_URL` 사용 (`nats://<user>:<pass>@localhost:{forwarded_port}`), local-only 모드는 `nats://localhost:4222` (인증 없음) |
| NATS `nats-secret` 미발견 | `nats` 네임스페이스에는 없고 `ai-platform*` 네임스페이스에 존재. Step 5의 `port-forward-infra.sh`가 `nats-secret`을 자동 탐색 (스크립트 내부에서 `nats` + `ai-platform*` 네임스페이스를 순회) |
| S3 `InvalidAccessKeyId` (403) | .env의 `S3_ACCESS_KEY_ID`/`S3_SECRET_ACCESS_KEY`가 K8s 시크릿 값과 일치하는지 확인, Step 5b 재실행 |
| 브라우저 403 (Caddy → 프론트엔드) | `rspack.config.mjs`의 `devServer.allowedHosts`에 `.thakicloud.net` 미등록 → Step 7-6 확인 |
| CORS 에러 (Caddy 경유) | 백엔드 `.env`의 `CORS_ALLOW_ORIGIN_PATTERNS`에 `*.thakicloud.net` 설정 확인 |
| 쿠키 미설정 (Caddy HTTPS) | `COOKIE_SECURE_MODE=true` 확인 + 백엔드 재시작 |
| `ERR_CERT_AUTHORITY_INVALID` | `sudo caddy trust` 실행 (최초 1회) |
| Caddy `EADDRINUSE :443` | `lsof -i :443 -t \| xargs kill -9` 또는 기존 Caddy 종료: `caddy stop` |
| API 요청이 `http://localhost:3000`으로 감 | 프론트엔드 `.env`의 `VITE_GO_BACKEND_URL`이 빈 문자열인지 확인 후 **프론트엔드 재시작** |
