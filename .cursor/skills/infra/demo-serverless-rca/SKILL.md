---
name: demo-serverless-rca
description: >-
  Systematic RCA for AI Platform Demo Serverless (Endpoint) errors.
  Guides through the 4-step endpoint readiness check (mirrors watcher_sync.go),
  KEDA HSO troubleshooting, crash loop detection, timeout analysis, and
  warmup verification for VLLM endpoints.
  Use when the user asks to "debug endpoint", "endpoint error",
  "endpoint failed", "serverless error", "serverless RCA",
  "엔드포인트 에러", "서버리스 장애", "엔드포인트 원인 분석",
  "demo-serverless-rca", "CrashLoopBackOff endpoint", "endpoint timeout",
  "HSO error", "KEDA error", "서버리스 트러블슈팅", "엔드포인트 트러블슈팅",
  or encounters a failed/stuck endpoint in the AI Platform Demo environment.
  Do NOT use for Workload errors (use demo-workload-rca).
  Do NOT use for Pipeline Builder errors (use demo-pipeline-rca).
  Do NOT use for production environment troubleshooting.
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "infra"
  platforms: [darwin]
---

# Demo Serverless (Endpoint) RCA

Serverless Endpoint 에러 발생 시 체계적으로 근본 원인을 분석하는 스킬입니다.

Endpoint Watcher는 `creating` 상태의 엔드포인트를 모니터링하며 4단계 순차 검증을 수행합니다:
1. **Deployment Ready 확인** → available로 전환
2. **Absolute Timeout** → created_at 기준 최대 생성 시간 초과
3. **Relative Timeout** → creating_started_at 기준 타임아웃 초과
4. **CrashLoop 감지** → 2분 대기 후, 연속 2회 확인 시 failed

## Prerequisites

- Demo 클러스터 컨텍스트 활성화 (`kubectx tkai-demo`)
- DB 포트포워딩 활성 (`demo-db-connect` 스킬 참조)
- VPN 연결 필수

## Step 1 — DB에서 엔드포인트 상태 확인

```sql
SELECT id, name, status, status_message, namespace,
       k8s_deployment_name, workload_type, model,
       min_replica, helm_release_name,
       creating_started_at, created_at, updated_at
FROM endpoints
WHERE name = '{ENDPOINT_NAME}'
  AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 5;
```

### 주요 status 값

| status | 의미 |
|--------|------|
| `pending` | 생성 요청 수신, 처리 전 |
| `creating` | Helm 설치 완료, Deployment/HSO 생성됨, Pod 대기 중 |
| `available` | Pod Ready, 서비스 가능 |
| `failed` | Watcher가 장애 감지 (timeout/crash) |
| `updating` | 설정 변경 반영 중 |

## Step 2 — K8s 리소스 상태 확인

### 2.1 Deployment 상태

```bash
# Deployment 확인
kubectl get deploy -n {NAMESPACE} -l app.kubernetes.io/instance={DEPLOYMENT_NAME}

# Pod 상태
kubectl get pods -n {NAMESPACE} -l app.kubernetes.io/instance={DEPLOYMENT_NAME}

# Pod 상세 (Events 섹션 필수 확인)
kubectl describe pod {POD_NAME} -n {NAMESPACE}
```

### 2.2 KEDA HTTPScaledObject (HSO) 상태

```bash
# HSO 리소스 확인
kubectl get httpscaledobject -n {NAMESPACE}

# HSO 상세
kubectl describe httpscaledobject {NAME} -n {NAMESPACE}

# KEDA Operator 로그 (스케일링 문제 시)
kubectl logs -n keda -l app=keda-operator --tail=100
```

### 2.3 Helm Release 확인

```bash
helm list -n {NAMESPACE} | grep {ENDPOINT_NAME}
helm status {HELM_RELEASE_NAME} -n {NAMESPACE}
helm history {HELM_RELEASE_NAME} -n {NAMESPACE}
```

## Step 2.4 — StorageClass 존재 여부 검증 (PVC 바인딩 실패 시)

Pod Events에 `FailedScheduling` + `persistentvolumeclaim ... not found` 또는 PVC가 `Pending` 상태인 경우,
PVC가 참조하는 StorageClass가 클러스터에 실제 존재하는지 확인합니다.

```bash
# 1. 엔드포인트 관련 PVC 조회
kubectl get pvc -n {NAMESPACE} | grep {ENDPOINT_NAME}

# 2. PVC가 참조하는 StorageClass 확인
kubectl get pvc {PVC_NAME} -n {NAMESPACE} -o jsonpath='{.spec.storageClassName}'

# 3. 해당 StorageClass가 클러스터에 존재하는지 확인
kubectl get storageclass {STORAGE_CLASS_NAME}

# 4. 사용 가능한 전체 StorageClass 목록
kubectl get storageclass
```

| 진단 결과 | 원인 | 조치 |
|-----------|------|------|
| StorageClass 미존재 (`NotFound`) | PVC가 삭제되었거나 이름이 변경된 StorageClass 참조 | 사용 가능한 StorageClass로 변경 (`tkai-nfs-agent`, `tkai-nfs-agent-individual`, `csi-rbd-sc` 등) |
| StorageClass 존재 + PVC `Pending` | Provisioner 장애 또는 용량 부족 | NFS provisioner Pod 상태 확인, 스토리지 용량 점검 |
| PVC `Bound` + Pod 여전히 실패 | PVC 외 다른 원인 | Step 3 CrashLoop / Step 4 VLLM 워밍업 확인으로 진행 |

## Step 3 — 4-Step Watcher 로직 기반 분석

Endpoint Watcher(`watcher_sync.go`)의 `checkAndUpdateEndpointStatus` 로직을 따릅니다.

### 3.1 Deployment Ready 확인

```bash
kubectl get deploy {DEPLOYMENT_NAME} -n {NAMESPACE} -o jsonpath='{.status.readyReplicas}'
```

**ReadyReplicas > 0** 이면 정상 → `available`로 전환됩니다.
Ready가 아니면 아래 3단계 장애 판정이 진행됩니다.

### 3.2 Absolute Timeout 확인

`created_at` 기준으로 `MaxEndpointCreationAge`를 초과하면 무조건 `failed` 처리됩니다.

```sql
-- 절대 타임아웃 초과 여부 확인
SELECT id, name,
       to_timestamp(created_at) as created_time,
       NOW() - to_timestamp(created_at) as age
FROM endpoints
WHERE name = '{ENDPOINT_NAME}'
  AND status = 'creating';
```

| status_message | 원인 | 조치 |
|---------------|------|------|
| `endpoint exceeded maximum creation age (absolute timeout)` | 엔드포인트 생성 후 최대 허용 시간 초과 | 이미지 크기, 모델 다운로드 시간, 네트워크 확인 |

### 3.3 Relative Timeout 확인

`creating_started_at` (없으면 `updated_at`) 기준으로, `workload_config.base_model_id`에 따라 동적으로 결정된 타임아웃 초과 시 `failed`.

| status_message | 원인 | 조치 |
|---------------|------|------|
| `endpoint did not become ready within timeout` | 모델 로딩/워밍업 시간 초과 | 모델 크기 대비 리소스 적절성 확인, GPU 가용성 점검 |

### 3.4 CrashLoop 감지

**조건**: `creating_started_at` 기준 2분(`CrashLoopMinWait`) 경과 후 검사 시작, 연속 2회(`CrashLoopConfirmCount`) 감지 시 `failed`.

Watcher는 `IsPodCrashLooping()`을 호출하여 다음 상태를 감지합니다:

| 컨테이너 상태 | 감지 조건 |
|--------------|----------|
| `CrashLoopBackOff` | Waiting.Reason |
| `ImagePullBackOff` / `ErrImagePull` | Waiting.Reason |
| `CreateContainerConfigError` | Waiting.Reason |
| `RunContainerError` | Waiting.Reason |
| `OOMKilled` | Terminated.Reason |
| `Error` (restarts >= 3) | Terminated.Reason + RestartCount |
| High restart count (>= 5) | RestartCount only |

```bash
# 크래시 로그 확인
kubectl logs {POD_NAME} -n {NAMESPACE} --previous

# Init 컨테이너 로그 (init 컨테이너 크래시 시)
kubectl logs {POD_NAME} -n {NAMESPACE} -c {INIT_CONTAINER_NAME} --previous
```

| status_message 패턴 | 원인 | 조치 |
|---------------------|------|------|
| `pod crash detected: CrashLoopBackOff` | 컨테이너 반복 크래시 | 이전 로그 확인, 리소스/설정 점검 |
| `pod crash detected: OOMKilled` | 메모리 초과 | resources.limits.memory 증가 |
| `pod crash detected: ImagePullBackOff` | 이미지 Pull 실패 | 이미지 경로, 레지스트리 인증 확인 |
| `pod crash detected: CreateContainerConfigError: ...` | ConfigMap/Secret 누락 | 참조 리소스 존재 확인 |
| `pod crash detected: Error (restarts: N)` | 반복 에러 종료 | 애플리케이션 로그 분석 |

## Step 4 — VLLM 워밍업 확인 (모델 서빙 엔드포인트)

VLLM 기반 엔드포인트는 모델 로딩 및 워밍업에 시간이 소요됩니다.

```bash
# VLLM 로그에서 워밍업 진행 상황 확인
kubectl logs {POD_NAME} -n {NAMESPACE} | grep -i "loading\|warmup\|ready\|model"

# GPU 메모리 사용량
kubectl exec {POD_NAME} -n {NAMESPACE} -- nvidia-smi
```

**일반적인 VLLM 장애 원인**:
- GPU 메모리 부족 → `OOMKilled` 또는 CUDA OOM 에러
- 모델 다운로드 실패 → HuggingFace 토큰/네트워크 문제
- 잘못된 모델 ID → 404 에러

## Step 5 — Resource Cleanup 확인

Watcher는 `failed` 처리 시 K8s 리소스를 정리합니다 (`cleanupEndpointResources`):
- Helm release 삭제
- HSO 삭제
- HuggingFace Secret 삭제

정리가 실패한 경우 잔류 리소스가 남을 수 있습니다:

```bash
# 잔류 리소스 확인
helm list -n {NAMESPACE} --all | grep {ENDPOINT_NAME}
kubectl get httpscaledobject -n {NAMESPACE} | grep {ENDPOINT_NAME}
kubectl get secret -n {NAMESPACE} | grep hf-
```

## Watcher Thresholds Reference

| 상수 | 값 | 용도 |
|------|------|------|
| `EndpointWatchInterval` | 10초 | 상태 체크 주기 |
| `CrashLoopMinWait` | 2분 | CrashLoop 감지 시작 전 대기 시간 |
| `CrashLoopConfirmCount` | 2 | CrashLoop 연속 확인 횟수 |
| `MaxEndpointCreationAge` | 설정 의존 | 절대 타임아웃 (created_at 기준) |
| Relative Timeout | model_id 의존 | 상대 타임아웃 (creating_started_at 기준) |

## Source Code Reference

- Watcher Core: `ai-platform/backend/go/internal/runner/endpoint/watcher.go` (constants)
- Watcher Sync: `ai-platform/backend/go/internal/runner/endpoint/watcher_sync.go` (4-step check)
- Watcher Failure: `ai-platform/backend/go/internal/runner/endpoint/watcher_failure.go` (cleanup + DB update)
- CrashLoop Detection: `ai-platform/backend/go/internal/k8sclient/hso.go` (`IsPodCrashLooping`)
- Helm Charts: `ai-platform/backend/go/charts/container/templates/deployment.yaml`, `httpscaledobject.yaml`
