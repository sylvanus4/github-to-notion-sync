---
name: demo-devspace-rca
description: >-
  Systematic RCA for AI Platform Demo DevSpace errors. Guides through K8s
  Deployment/Pod/PVC inspection, DB status queries, enhanced pod health
  monitoring, and a decision tree mapping status_message patterns to root
  causes across creation, running, stopping, and deletion phases. Use when the
  user asks to "debug devspace", "devspace error", "devspace failed",
  "devspace RCA", "데브스페이스 에러", "데브스페이스 장애", "데브스페이스 원인 분석",
  "demo-devspace-rca", "CrashLoopBackOff devspace", "ImagePullBackOff
  devspace", "OOMKilled devspace", "devspace stuck creating", "devspace not
  starting", "데브스페이스 트러블슈팅", or encounters a failed/stuck DevSpace in the AI
  Platform Demo environment. Do NOT use for Workload errors (use
  demo-workload-rca). Do NOT use for Serverless/Endpoint errors (use
  demo-serverless-rca). Do NOT use for Pipeline Builder errors (use
  demo-pipeline-rca). Do NOT use for production environment troubleshooting.
---

# Demo DevSpace RCA

DevSpace 에러 발생 시 체계적으로 근본 원인을 분석하는 스킬입니다.

## Pre-flight (한 번에 실행)

VPN 연결 상태에서 아래 블록을 순서대로 실행합니다. 이미 활성 상태이면 건너뜁니다.

```bash
# 1. 클러스터 컨텍스트 전환
kubectx tkai-demo

# 2. DB 포트포워딩 (백그라운드, 이미 열려 있으면 건너뛰기)
lsof -i :15432 >/dev/null 2>&1 && echo "Port 15432 already forwarded" \
  || kubectl -n postgresql port-forward svc/postgresql 15432:5432 &
```

### DB 접속 Quick Reference

| DB | 커맨드 |
|----|--------|
| ai_platform_db | `PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db` |

### 사용자 프로젝트 네임스페이스 찾기

```sql
SELECT p.id, p.name, ns.name AS namespace
FROM projects p
  JOIN namespaces ns ON p.namespace_id = ns.id
  JOIN project_members pm ON pm.project_id = p.id
  JOIN users u ON u.id = pm.user_id
WHERE u.email = '{USER_EMAIL}'
  AND p.deleted_at IS NULL;
```

또는 kubectl로 직접 확인:

```bash
kubectl get ns | grep project-
```

## Step 1 — DB에서 DevSpace 상태 확인

```sql
SELECT id, name, status, status_message,
       namespace, deployment_name, pvc_name, ingress_url,
       to_timestamp(created_at) AS created_at,
       to_timestamp(updated_at) AS updated_at,
       to_timestamp(started_at) AS started_at,
       to_timestamp(stopped_at) AS stopped_at
FROM devspaces
WHERE name = '{DEVSPACE_NAME}'
  AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 5;
```

> **주의**: `created_at`, `updated_at`, `started_at`, `stopped_at` 컬럼은 **bigint (epoch seconds)** 타입입니다. `to_timestamp()` 변환 시 `/1000`이 필요 **없습니다** (Workload와 다름).

`status_message` 값이 근본 원인의 핵심 단서입니다. DevSpace Watcher가 K8s 상태를 감지하여 이 필드에 기록합니다.

### 주요 status 값

| status | 의미 |
|--------|------|
| `pending` | API에서 생성됨, NATS 이벤트 발행 대기 |
| `creating` | Handler가 PVC + Deployment 생성 완료, Watcher가 Pod Ready 대기 |
| `starting` | 사용자가 정지된 DevSpace 재시작, Deployment scale-up 진행 |
| `running` | Pod Ready, 정상 동작 (Ingress URL 할당됨) |
| `stopping` | 사용자 중지 요청, Deployment scale-down 진행 |
| `stopped` | 정상 중지 (replicas=0, Pod 종료 확인) |
| `failed` | Watcher가 장애 감지 (status_message에 원인 기록) |
| `deleting` | 삭제 진행 중 (K8s 리소스 제거 중) |
| `deleted` | 삭제 완료 (soft-delete via deleted_at) |

### 장애 DevSpace 일괄 조회

```sql
SELECT id, name, status, status_message, namespace,
       to_timestamp(created_at) AS created_at,
       to_timestamp(updated_at) AS updated_at
FROM devspaces
WHERE status IN ('failed', 'creating', 'stopping', 'deleting')
  AND deleted_at IS NULL
ORDER BY updated_at DESC
LIMIT 20;
```

## Step 2 — K8s 리소스 확인

### 2.1 Deployment 및 Pod 상태

```bash
# Deployment 확인
kubectl get deployment {DEPLOYMENT_NAME} -n {NAMESPACE}

# Pod 상태 확인 (DevSpace 라벨)
kubectl get pods -n {NAMESPACE} -l ai-platform.io/devspace-id={DEVSPACE_ID}

# 또는 app 라벨로 확인
kubectl get pods -n {NAMESPACE} -l app={DEVSPACE_NAME}

# Pod 상세 정보 (Events 섹션 확인)
kubectl describe pod {POD_NAME} -n {NAMESPACE}

# 이전 컨테이너 로그 (크래시된 경우)
kubectl logs {POD_NAME} -n {NAMESPACE} --previous

# 현재 컨테이너 로그
kubectl logs {POD_NAME} -n {NAMESPACE} --tail=100
```

### 2.2 PVC 상태

```bash
# PVC 확인
kubectl get pvc -n {NAMESPACE} -l ai-platform.io/devspace-id={DEVSPACE_ID}

# PVC 상세 (Bound/Pending 확인)
kubectl describe pvc {PVC_NAME} -n {NAMESPACE}

# StorageClass 확인
kubectl get storageclass
```

### 2.3 Service 및 Ingress 확인

```bash
# Service 확인
kubectl get svc -n {NAMESPACE} | grep {DEVSPACE_NAME}

# Ingress 확인
kubectl get ingress -n {NAMESPACE} | grep {DEVSPACE_NAME}
```

## Step 3 — Decision Tree (status_message → Root Cause)

### 3.1 `creating` 상태에서 멈춘 경우

**Watcher 감지 로직**: `syncDevSpaceStatuses()` → `checkAndUpdateDevSpaceStatus()`

#### Absolute Timeout (MaxCreationAge)

| status_message 패턴 | 원인 | 조치 |
|---------------------|------|------|
| `[timeout] DevSpace exceeded maximum creation age (30m0s)` | `created_at` 기준 30분 초과 | NATS 이벤트 유실 또는 K8s 리소스 생성 실패 확인 |

```bash
# Task Runner 로그 확인
kubectl logs -n ai-platform -l app=ai-platform-backend-go --tail=200 | grep -i "devspace\|nats\|error"

# NATS JetStream 상태
kubectl exec -n nats svc/nats -- nats stream ls
```

#### Relative Timeout (ReadyTimeout)

| status_message 패턴 | 원인 | 조치 |
|---------------------|------|------|
| `[timeout] DevSpace did not become ready within timeout (15m0s)` | `updated_at` 기준 15분 초과, Deployment ReadyReplicas=0 지속 | Pod describe Events 확인, 리소스 요청량 점검 |

#### Pod Health Failures (Enhanced Monitoring)

`checkPodHealthForCreating()` → `k8sClient.CheckDevSpacePodHealth()`

| status_message 패턴 | 원인 | 조치 |
|---------------------|------|------|
| `PVC pending for more than 5m` | PVC가 Bound되지 않음 (StorageClass 미존재, 용량 부족) | StorageClass 확인, PVC describe |
| `Image pull error persisted for more than 3m: ...` | ImagePullBackOff / ErrImagePull 3분 초과 | 이미지 경로 확인, imagePullSecrets 점검 |
| `Container restarted N times in Xm (threshold: 3 in 10m)` | 컨테이너 반복 크래시 | `--previous` 로그 확인 |
| `Container OOMKilled N times in Xm (threshold: 3 in 10m)` | 메모리 부족으로 반복 OOM Kill | resources.limits.memory 증가 |

```bash
# PVC 바인딩 상태
kubectl get pvc -n {NAMESPACE}
kubectl describe pvc {PVC_NAME} -n {NAMESPACE}

# ImagePullBackOff 디버깅
kubectl get events -n {NAMESPACE} --field-selector reason=Failed | grep -i pull

# OOMKilled 확인
kubectl get pod {POD_NAME} -n {NAMESPACE} \
  -o jsonpath='{.status.containerStatuses[0].lastState.terminated}' | python3 -m json.tool
```

#### CrashLoopBackOff (Legacy Detection)

| status_message 패턴 | 원인 | 조치 |
|---------------------|------|------|
| `[crash] Pod crash detected: ...` | CrashLoopMinWait (2분) 경과 후 CrashLoopBackOff 감지 | `--previous` 로그로 크래시 원인 확인 |

#### Handler-Level Failures (즉시 실패)

| status_message 패턴 | 원인 | 조치 |
|---------------------|------|------|
| `Project namespace {ns} not found` | 프로젝트 네임스페이스 미존재 | 프로젝트 생성 상태 확인 |
| `Failed to create PVC: ...` | PVC 생성 K8s API 에러 | StorageClass, 용량, 권한 확인 |
| `Failed to create Deployment: ...` | Deployment 생성 K8s API 에러 | 이미지, 리소스 요청량, RBAC 확인 |
| `Failed to verify namespace: ...` | 네임스페이스 조회 K8s API 에러 | K8s API 서버 상태 확인 |

### 3.2 `running` 상태에서 장애 감지

**Watcher 감지 로직**: `checkRunningDevSpacesHealth()` → Enhanced Pod Health Monitoring

| status_message 패턴 | 원인 | 조치 |
|---------------------|------|------|
| `Container restarted N times in Xm (threshold: 3 in 10m)` | 실행 중 반복 크래시 | 컨테이너 로그, exit code 분석 |
| `Container OOMKilled N times in Xm (threshold: 3 in 10m)` | 실행 중 반복 OOM Kill | 메모리 사용량 분석, 리소스 증가 |
| `Container is in CrashLoopBackOff` | CrashLoopBackOff 감지 | 크래시 원인 분석 |
| `Container exceeded N total restarts (limit: 10)` | 절대 재시작 횟수 초과 | 근본적 크래시 원인 해결 필요 |
| `[warning] Container restarted N times` | 경고 (실패 미전환), 재시작 발생 | 모니터링, 근본 원인 조사 |
| `[warning] Container OOMKilled N times` | 경고 (실패 미전환), OOM 발생 | 메모리 사용 패턴 분석 |

```bash
# 리소스 사용량 확인
kubectl top pod -n {NAMESPACE}

# OOM 이벤트 확인
kubectl get events -n {NAMESPACE} --field-selector reason=OOMKilling

# 컨테이너 상태 상세
kubectl get pod {POD_NAME} -n {NAMESPACE} -o jsonpath='{.status.containerStatuses}' | python3 -m json.tool
```

### 3.3 `stopping` 상태에서 멈춘 경우

**Watcher 감지 로직**: `checkStuckStoppingDevSpaces()` → `StuckStoppingTimeout` (5분) 초과

| status_message 패턴 | 원인 | 조치 |
|---------------------|------|------|
| `pod termination timeout` | Deployment replicas=0이지만 Pod가 종료되지 않음 | Pod describe, finalizer 확인 |
| `scale-down not attempted` | Deployment replicas > 0 (scale-down 미실행) | Handler 로그 확인, NATS 이벤트 확인 |

> **참고**: 정상 경로에서는 `HandleDevSpaceStopped`가 Deployment를 replicas=0으로 스케일 다운하고, Watcher가 Pod 종료를 확인 후 `stopped`로 전환합니다.

```bash
# Deployment replicas 확인
kubectl get deployment {DEPLOYMENT_NAME} -n {NAMESPACE} -o jsonpath='{.spec.replicas}'

# Pod 상태 확인 (종료 대기 중인 Pod)
kubectl get pods -n {NAMESPACE} -l app={DEVSPACE_NAME}

# Finalizer 확인
kubectl get pod {POD_NAME} -n {NAMESPACE} -o jsonpath='{.metadata.finalizers}'
```

### 3.4 `deleting` 상태에서 멈춘 경우

**Watcher 감지 로직**: `cleanupStuckDeletingDevSpaces()` → `DeletingStuckThreshold` (10분) 초과

| 상태 | 원인 | 조치 |
|------|------|------|
| `deleting` 10분 초과 | K8s 리소스 삭제 실패 (Deployment/Service/PVC finalizer) | 아래 리소스별 확인 |

```bash
# Deployment 존재 여부
kubectl get deployment {DEPLOYMENT_NAME} -n {NAMESPACE} 2>/dev/null && echo "EXISTS" || echo "DELETED"

# Service 존재 여부
kubectl get svc -n {NAMESPACE} | grep {DEVSPACE_NAME}

# PVC 존재 여부 (PVC에 finalizer가 있으면 Pod가 사용 중일 때 삭제 불가)
kubectl get pvc {PVC_NAME} -n {NAMESPACE} -o jsonpath='{.metadata.finalizers}'

# Stuck PVC 강제 삭제 (주의: 데이터 손실 가능)
# kubectl patch pvc {PVC_NAME} -n {NAMESPACE} -p '{"metadata":{"finalizers":null}}'
```

## Step 4 — Exit Code 분석

| Exit Code | 의미 | 일반적 원인 |
|-----------|------|-------------|
| 0 | 정상 종료 | 프로세스 완료 |
| 1 | 일반 에러 | 애플리케이션 에러 |
| 126 | 실행 권한 없음 | 스크립트 권한 |
| 127 | 명령어 없음 | 바이너리/스크립트 경로 |
| 137 | SIGKILL (OOMKilled) | 메모리 초과 |
| 139 | SIGSEGV | Segmentation Fault |
| 143 | SIGTERM | 정상 종료 시그널 |

## Watcher Thresholds Reference

| 환경변수 / 상수 | 기본값 | 용도 |
|-----------------|--------|------|
| `DEVSPACE_WATCHER_INTERVAL` | 10s | 상태 체크 주기 (WatchInterval) |
| `DEVSPACE_WATCHER_READY_TIMEOUT` | 15m | Deployment Ready 대기 시간 (relative, updated_at 기준) |
| `DEVSPACE_WATCHER_MAX_CREATION_AGE` | 30m | 절대 생성 대기 시간 (absolute, created_at 기준) |
| `DEVSPACE_WATCHER_CRASHLOOP_MIN_WAIT` | 2m | CrashLoopBackOff 감지 최소 대기 시간 |
| `DEVSPACE_WATCHER_DELETING_STUCK_THRESHOLD` | 10m | deleting 상태 stuck 판정 시간 |
| `DEVSPACE_WATCHER_STUCK_STOPPING_TIMEOUT` | 5m | stopping 상태 stuck 판정 시간 |
| `DEVSPACE_WATCHER_PVC_PENDING_TIMEOUT` | 5m | PVC Pending 허용 시간 |
| `DEVSPACE_WATCHER_IMAGE_PULL_TIMEOUT` | 3m | Image Pull 에러 허용 시간 |
| `DEVSPACE_WATCHER_MAX_RESTARTS_IN_WINDOW` | 3 | RestartWindow 내 최대 재시작 횟수 |
| `DEVSPACE_WATCHER_RESTART_WINDOW` | 10m | 재시작 카운트 윈도우 |
| `DEVSPACE_WATCHER_MAX_OOM_IN_WINDOW` | 3 | RestartWindow 내 최대 OOM 횟수 |
| `DEVSPACE_WATCHER_ENABLE_POD_HEALTH_MONITORING` | true | Enhanced Pod Health Monitoring 활성화 |
| `DEVSPACE_DEFAULT_START_TIMEOUT` | 120s | CPU DevSpace Handler Start Watcher 타임아웃 |
| `DEVSPACE_GPU_START_TIMEOUT` | 300s | GPU DevSpace Handler Start Watcher 타임아웃 |
| `DEVSPACE_MAX_RESTART_COUNT` | 5 | Start Watcher 최대 재시작 횟수 |

## NATS Events Reference

| 이벤트 | 트리거 | Handler | 동작 |
|--------|--------|---------|------|
| `devspace.created` | 사용자가 DevSpace 생성 | `HandleDevSpaceCreated` | PVC + Deployment 생성, status: pending → creating |
| `devspace.started` | 사용자가 정지된 DevSpace 시작 | `HandleDevSpaceStarted` | Deployment scale 0→1, Start Watcher 시작 |
| `devspace.stopped` | 사용자가 DevSpace 중지 | `HandleDevSpaceStopped` | Deployment scale 1→0, Watcher가 Pod 종료 확인 |
| `devspace.deleted` | 사용자가 DevSpace 삭제 | `HandleDevSpaceDeleted` | Deployment + Service + PVC 삭제, Delete Watcher 시작 |

## Step 5 — Source Code Change Analysis

RCA 분석 시 최근 소스코드 변경사항을 함께 확인하여 코드 변경이 장애의 원인인지 판단합니다.

### 5.1 최근 변경 이력 (Last 14 Days)

```bash
git -C ai-platform log --since="14 days ago" \
  --format="%h | %an | %ad | %s" --date=short -- \
  backend/go/internal/runner/devspace/
```

### 5.2 핵심 파일 최근 수정자 확인

```bash
# devspace_watcher.go 최근 수정자
git -C ai-platform log --since="30 days ago" \
  --format="%an" -- backend/go/internal/runner/devspace/devspace_watcher.go \
  | sort | uniq -c | sort -rn

# 핵심 함수 변경 이력 (Pod Health Check)
git -C ai-platform log --since="30 days ago" -p \
  -S "checkPodHealthForCreating" -- backend/go/internal/runner/devspace/devspace_watcher.go
```

### 5.3 장애 시점과 코드 변경 시점 상관관계

1. Step 1의 DB 쿼리에서 확인한 장애 발생 시각(`updated_at`)을 기준으로 합니다
2. 해당 시각 전후 커밋 확인:
   ```bash
   git -C ai-platform log --since="{ERROR_DATE} -3 days" \
     --until="{ERROR_DATE}" \
     --format="%h | %an | %ad | %s" --date=iso -- \
     backend/go/internal/runner/devspace/
   ```
3. 커밋 상세 확인:
   ```bash
   git -C ai-platform show {COMMIT_HASH} --stat
   ```

### 코드 변경 → 장애 상관관계 판단 기준

| 조건 | 판단 |
|------|------|
| 장애 발생 3일 이내에 관련 파일 커밋 있음 | **높은 상관관계** — 변경 내용 상세 리뷰 필요 |
| 장애 발생 7일 이내에 관련 파일 커밋 있음 | **중간 상관관계** — 변경 내용 확인 |
| 14일 이내 커밋 없음 | **낮은 상관관계** — 인프라/설정 원인 가능성 높음 |

## Source Code Reference

- Watcher: `ai-platform/backend/go/internal/runner/devspace/devspace_watcher.go`
- Handlers: `ai-platform/backend/go/internal/runner/devspace/handlers.go`
- Start Watcher: `ai-platform/backend/go/internal/runner/devspace/start_watcher.go`
- Delete Watcher: `ai-platform/backend/go/internal/runner/devspace/delete_watcher.go`
- K8s Client: `ai-platform/backend/go/internal/k8sclient/`

---

## Git 커밋 귀인 분석 (필수)

> **반드시 수행**: "언제 누가 어떤 작업을 했는데 문제가 발생한 것인지?" 질문에 답해야 합니다.

RCA 완료 후 근본 원인과 관련된 코드/설정 변경의 커밋 이력을 추적하여 인과 관계 타임라인을 작성합니다.

### 관련 파일 커밋 이력 조회

```bash
git -C ai-platform log --since="30 days ago" \
  --format="%h | %an | %ad | %s" --date=short -- \
  backend/go/internal/runner/devspace/

gh api repos/{OWNER}/{REPO}/commits?path={FILE_PATH}&per_page=10
```

### 커밋 귀인 타임라인 작성

| 순서 | 날짜 | 누가 | 어디서 | 무슨 작업 | 영향 |
|------|------|------|--------|-----------|------|
| 1 | YYYY-MM-DD | 작업자 | 파일/레포 | 변경 내용 | 영향 분석 |

**핵심 커밋**에는 SHA, Author, Date, Message, 파일, 변경 내용을 상세히 기록합니다.

### 인과 관계 요약

```
[시점1] 작업 A (작업자)
     ↓
[시점2] 작업 B (작업자)
     ↓
[시점3] ⚠️ 핵심 원인 커밋 (작업자)
     ↓
[실행 시] 에러 발생
```

### 핵심 판단

- **직접 원인**: 어떤 커밋이 근본 원인인지
- **전파 경로**: 어떻게 현재 환경에 전파되었는지
- **ThakiCloud 팀 책임**: 리뷰/검증 부재 여부

---

## 노션 업로드 (필수)

RCA 리포트 완료 후 반드시 아래 절차를 수행합니다:

1. RCA 전체 내용(에러 요약 + 근본 원인 + 커밋 귀인 타임라인 + 해결 방안 + 재발 방지)을
   `outputs/demo-rca/{date}/devspace-rca.md`에 저장
2. `md-to-notion` 스킬 또는 Notion MCP `notion-create-pages`로
   "AI Platform Demo 환경 RCA 리포트" (ID: `34e9eddc34e680f78eacfea0a60270b3`) 하위에 업로드
3. 생성된 노션 페이지 URL을 사용자에게 제공

> **참고**: pipe 테이블은 Notion에서 렌더링되지 않으므로 HTML `<table>` 태그로 변환하여 업로드합니다.
