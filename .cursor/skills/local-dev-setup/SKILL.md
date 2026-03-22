---
name: local-dev-setup
description: Go 백엔드 로컬 개발 환경을 자동 설정합니다. Docker DB/NATS 생성, 마이그레이션 적용, 시드 데이터, RSA 키 생성, 인프라 포트포워딩, .env 업데이트를 순차 수행합니다. 로컬 개발 환경, 로컬 셋업, backend 셋업, 환경 구성, 개발 환경 준비, 로컬 실행 요청 시 사용합니다. Do NOT use for 프론트엔드 개발 환경 설정이나 K8s 클러스터 배포.
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
| `missing` | `docker run -d --name ai-platform-nats -p 4222:4222 -p 6222:6222 -p 8222:8222 nats:2.10-alpine -js -p 4222 -m 8222` |
| `exited` | `docker start ai-platform-nats` |
| `running` | 스킵 |

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

.env가 이미 로컬 기본값(`localhost:5432`, `localhost:4222`)이므로 변경 불필요.
.env 파일이 없었다면 Step 2에서 이미 `cp tkai-backend.env .env` 완료.

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

서버 실행: cd ai-platform/backend/go && ./scripts/run-eda.sh
```

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
| S3 `InvalidAccessKeyId` (403) | .env의 `S3_ACCESS_KEY_ID`/`S3_SECRET_ACCESS_KEY`가 K8s 시크릿 값과 일치하는지 확인, Step 5b 재실행 |
