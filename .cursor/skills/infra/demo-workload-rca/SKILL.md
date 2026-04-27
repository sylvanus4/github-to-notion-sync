---
name: demo-workload-rca
description: >-
  Systematic RCA for AI Platform Demo Workload errors.
  Guides through K8s pod/deployment inspection, DB status queries,
  Helm release checks, and a decision tree mapping K8s states to root causes.
  Use when the user asks to "debug workload", "workload error",
  "workload failed", "workload RCA", "워크로드 에러", "워크로드 장애",
  "워크로드 원인 분석", "demo-workload-rca", "CrashLoopBackOff workload",
  "ImagePullBackOff workload", "OOMKilled workload", "워크로드 트러블슈팅",
  or encounters a failed/stuck workload in the AI Platform Demo environment.
  Do NOT use for Serverless/Endpoint errors (use demo-serverless-rca).
  Do NOT use for Pipeline Builder errors (use demo-pipeline-rca).
  Do NOT use for production environment troubleshooting.
metadata:
  author: "thaki"
  version: "2.0.0"
  category: "infra"
  platforms: [darwin]
---

# Demo Workload RCA

Workload 에러 발생 시 체계적으로 근본 원인을 분석하는 스킬입니다.

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
| tkai_agents | `PGPASSWORD=tkai_password psql -h localhost -p 15432 -U tkai_user -d tkai_agents` |

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

## Step 1 — DB에서 워크로드 상태 확인

```sql
SELECT id, name, status, status_message, exit_code,
       workload_type, k8s_deployment_name,
       created_at, started_at, finished_at, updated_at
FROM workloads
WHERE name = '{WORKLOAD_NAME}'
  AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 5;
```

> **주의**: `created_at`, `updated_at`, `started_at`, `finished_at` 컬럼은 **bigint (epoch milliseconds)** 타입입니다. `to_timestamp()` 사용 시 `/1000` 변환 필수.

`status_message` 값이 근본 원인의 핵심 단서입니다. Watcher가 K8s 상태를 감지하여 이 필드에 기록합니다.

### 주요 status 값

| status | 의미 |
|--------|------|
| `creating` | NATS 이벤트 처리 중, K8s 리소스 미생성 |
| `starting` | K8s Deployment 생성됨, Pod 대기 중 |
| `running` | Pod Ready, 정상 동작 |
| `restarting` | 사용자 요청 재시작 진행 중 |
| `failed` | Watcher가 장애 감지 |
| `stopped` | 정상 종료 (Job 완료 또는 사용자 중지) |

## Step 2 — K8s Pod 상태 확인

```bash
# 프로젝트 네임스페이스 확인
kubectl get ns | grep -i {PROJECT_NAME}

# Pod 상태 확인 (일반 워크로드)
kubectl get pods -n {NAMESPACE} -l app={DEPLOYMENT_NAME}

# Pod 상태 확인 (Helm 배포 워크로드 — is_special_image=true)
kubectl get pods -n {NAMESPACE} -l app.kubernetes.io/instance={HELM_RELEASE_NAME}

# Pod 상세 정보 (Events 섹션 확인)
kubectl describe pod {POD_NAME} -n {NAMESPACE}

# 이전 컨테이너 로그 (크래시된 경우)
kubectl logs {POD_NAME} -n {NAMESPACE} --previous

# 현재 컨테이너 로그
kubectl logs {POD_NAME} -n {NAMESPACE} --tail=100
```

## Step 3 — Helm Release 확인 (Special Image)

```bash
helm list -n {NAMESPACE} | grep {WORKLOAD_NAME}
helm status {HELM_RELEASE_NAME} -n {NAMESPACE}
helm history {HELM_RELEASE_NAME} -n {NAMESPACE}
```

## Step 4 — Decision Tree (status_message → Root Cause)

### 4.1 `creating` 상태에서 멈춘 경우

**Watcher 감지 조건**: `created_at` 기준 15분 초과 (`CreatingStuckThreshold`)

| status_message | 원인 | 조치 |
|---------------|------|------|
| `Workload stuck in creating state — NATS event may have been lost or runner crashed` | NATS 이벤트 유실 또는 Task Runner 장애 | Task Runner 로그 확인, NATS JetStream 상태 점검 |

```bash
# Task Runner 로그 확인
kubectl logs -n ai-platform -l app=ai-platform-backend-go --tail=200 | grep -i "workload\|nats\|error"

# NATS JetStream 상태
kubectl exec -n nats svc/nats -- nats stream ls
```

### 4.2 Container 관련 장애

**Watcher 감지**: `checkContainerFailures()` → `isTerminalWaitingReason()`

| status_message 패턴 | 원인 | 조치 |
|---------------------|------|------|
| `Container {name}: ImagePullBackOff` | 이미지 없음, 레지스트리 인증 실패 | 이미지 경로 확인, imagePullSecrets 점검 |
| `Container {name}: ErrImagePull` | 이미지 Pull 실패 (네트워크 또는 권한) | 레지스트리 접근 가능 여부 확인 |
| `Container {name}: InvalidImageName` | 이미지 이름 형식 오류 | 이미지 URL 형식 점검 |
| `Container {name}: CreateContainerConfigError` | ConfigMap/Secret 마운트 실패 | 참조된 ConfigMap/Secret 존재 여부 확인 |
| `Container {name}: CreateContainerError` | 컨테이너 생성 실패 | describe pod Events 확인 |
| `Container {name} crashed {N} times (last exit code: {code})` | RestartCount >= 5, 반복 크래시 | `--previous` 로그 확인, exit code 분석 |

```bash
# ImagePullBackOff 디버깅
kubectl get events -n {NAMESPACE} --field-selector reason=Failed | grep -i pull

# ConfigMap/Secret 존재 확인
kubectl get configmap,secret -n {NAMESPACE}
```

### 4.3 Pod 스케줄링 장애

**Watcher 감지**: `checkPendingPodIssues()` → PodScheduled 조건 확인

| status_message 패턴 | 원인 | 조치 |
|---------------------|------|------|
| `Pod unschedulable: Unschedulable - ...` | 노드 리소스 부족 | 노드 리소스 현황 확인 |
| `Pod unschedulable: InsufficientCPU` | CPU 부족 | 리소스 요청량 조정 또는 노드 스케일업 |
| `Pod unschedulable: InsufficientMemory` | 메모리 부족 | 리소스 요청량 조정 |
| `Pod unschedulable: InsufficientGPU` | GPU 부족 | GPU 노드 가용성 확인 |

```bash
# 노드 리소스 현황
kubectl top nodes
kubectl describe nodes | grep -A5 "Allocated resources"

# GPU 리소스 확인
kubectl get nodes -o custom-columns='NAME:.metadata.name,GPU:.status.allocatable.nvidia\.com/gpu'
```

> **Kyverno 정책 주의**: Demo 환경에서 standalone GPU Pod 생성이 `pod-gpu-validation` 정책에 의해 차단됩니다. GPU 워크로드 디버깅 시 반드시 Deployment/Job으로 생성해야 합니다.

### 4.4 PVC 바인딩 장애

**Watcher 동작**: PVC 관련 Unschedulable 에러는 `PVCBindingGracePeriod` (5분) 동안 유예. 초과 시 `failed` 처리.

```bash
# PVC 상태 확인
kubectl get pvc -n {NAMESPACE}

# StorageClass 확인
kubectl get storageclass

# PV 바인딩 상태
kubectl describe pvc {PVC_NAME} -n {NAMESPACE}
```

### 4.5 Deployment 장기 미가용

**Watcher 감지**: `checkDeploymentStuck()` — `started_at` (또는 `updated_at`) 기준 5분 초과 시 `failed`

| status_message 패턴 | 원인 | 조치 |
|---------------------|------|------|
| `Deployment unavailable for more than 5m0s` | ReadyReplicas = 0이 5분 지속 | Pod describe로 Events 확인 |
| `Deployment not found in Kubernetes` | Deployment 삭제됨 | Helm release 상태 확인, 재생성 필요 |

### 4.6 OOMKilled

```bash
# OOMKilled 확인 (jsonpath로 정확한 종료 사유 확인)
kubectl get pod {POD_NAME} -n {NAMESPACE} \
  -o jsonpath='{.status.containerStatuses[0].lastState.terminated}' | python3 -m json.tool

# OOM 이벤트 확인
kubectl get events -n {NAMESPACE} --field-selector reason=OOMKilling

# 리소스 사용량 확인
kubectl top pod -n {NAMESPACE}
```

> `exitCode: 137` + `reason: OOMKilled`가 확인되면 메모리 부족이 원인입니다.

**조치**: Helm values에서 `resources.limits.memory` 증가

### GPU 워크로드 메모리 참조 (S3 Model Streaming)

S3 Model Streaming (Runai Streamer)을 사용하는 VLLM 워크로드는 모델 가중치를 CPU 메모리에 버퍼링합니다.

| 모델 크기 | 최소 CPU 메모리 | 권장 CPU 메모리 |
|----------|----------------|----------------|
| 1-4B | 8Gi | 12Gi |
| 7-8B | 16Gi | 24Gi |
| 13B | 28Gi | 32Gi |
| 70B | 140Gi | 160Gi |

## Step 5 — Exit Code 분석

| Exit Code | 의미 | 일반적 원인 |
|-----------|------|-------------|
| 0 | 정상 종료 | Job 완료 |
| 1 | 일반 에러 | 애플리케이션 에러 |
| 126 | 실행 권한 없음 | 스크립트 권한 |
| 127 | 명령어 없음 | 바이너리/스크립트 경로 |
| 137 | SIGKILL (OOMKilled) | 메모리 초과 |
| 139 | SIGSEGV | Segmentation Fault |
| 143 | SIGTERM | 정상 종료 시그널 |

## Watcher Thresholds Reference

| 상수 | 값 | 용도 |
|------|------|------|
| `WorkloadWatchInterval` | 10초 | 상태 체크 주기 |
| `DeploymentUnavailableThreshold` | 5분 | ReadyReplicas=0 허용 시간 |
| `CreatingStuckThreshold` | 15분 | creating 상태 최대 허용 시간 |
| `PVCBindingGracePeriod` | 5분 | PVC Unschedulable 유예 시간 |
| `RestartCount >= 5` | - | 반복 크래시 판정 기준 |

## Source Code Reference

- Watcher: `ai-platform/backend/go/internal/runner/workload/status_watcher.go`
- K8s Client: `ai-platform/backend/go/internal/k8sclient/`
- Helm Charts: `ai-platform/backend/go/charts/container/templates/deployment.yaml`
