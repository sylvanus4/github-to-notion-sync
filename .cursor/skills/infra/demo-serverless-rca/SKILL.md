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
  version: "2.1.0"
  category: "infra"
  platforms: [darwin]
---

# Demo Serverless (Endpoint) RCA

Serverless Endpoint 에러 발생 시 체계적으로 근본 원인을 분석하는 스킬입니다.

Endpoint Watcher는 `creating` 상태의 엔드포인트를 모니터링하며 4단계 순차 검증을 수행합니다:
1. **Deployment Ready 확인** -> available로 전환
2. **Absolute Timeout** -> created_at 기준 최대 생성 시간 초과
3. **Relative Timeout** -> creating_started_at 기준 타임아웃 초과
4. **CrashLoop 감지** -> 2분 대기 후, 연속 2회 확인 시 failed

## Prerequisites -- Pre-flight (한 번에 실행)

VPN 연결 상태에서 아래 블록을 순서대로 실행합니다. 이미 활성 상태이면 해당 단계를 건너뜁니다.

```bash
# 1. 클러스터 컨텍스트 전환
kubectx tkai-demo

# 2. DB 포트포워딩 (백그라운드, 이미 열려 있으면 건너뜀)
lsof -i :15432 >/dev/null 2>&1 && echo "Port 15432 already forwarded" \
  || kubectl -n postgresql port-forward svc/postgresql 15432:5432 &
```

### DB 접속 Quick Reference

| DB | 커맨드 |
|----|--------|
| ai_platform_db | `PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db` |
| tkai_agents | `PGPASSWORD=tkai_password psql -h localhost -p 15432 -U tkai_user -d tkai_agents` |

### 사용자 프로젝트 네임스페이스 찾기

사용자 이메일로 프로젝트 네임스페이스를 조회합니다. Demo 환경의 네임스페이스 패턴: `project-{uuid}`

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

## Step 1 -- 원샷 진단 (DB + K8s 동시 수집)

단일 psql 호출로 엔드포인트 상태, 설정, 리소스를 한꺼번에 조회합니다.

```bash
PGPASSWORD=password psql -h localhost -p 15432 -U postgres -d ai_platform_db <<'SQL'
-- 1a. 엔드포인트 기본 상태
SELECT name, status, LEFT(status_message, 150) AS msg,
       gpu, workload_config::text,
       min_replica, max_replica,
       to_timestamp(creating_started_at/1000) AS creating_started,
       to_timestamp(created_at/1000) AS created,
       to_timestamp(updated_at/1000) AS updated
FROM endpoints
WHERE name LIKE '%{ENDPOINT_NAME}%'
  AND deleted_at IS NULL
ORDER BY created_at DESC LIMIT 5;

-- 1b. 해당 사용자의 전체 엔드포인트 현황 (비교 용도)
SELECT name, status, gpu, LEFT(status_message, 100) AS msg
FROM endpoints
WHERE namespace = '{NAMESPACE}'
  AND deleted_at IS NULL
ORDER BY updated_at DESC;
SQL
```

> **주의**: `created_at`, `updated_at`, `creating_started_at`은 **bigint (epoch milliseconds)** 타입입니다. `to_timestamp()` 사용 시 `/1000` 필수.

K8s 리소스도 한 번에 수집:

```bash
NS="{NAMESPACE}"
echo "=== Deployments ==="
kubectl get deploy -n $NS --no-headers
echo ""
echo "=== Pods ==="
kubectl get pods -n $NS -o wide --no-headers
echo ""
echo "=== HSO (KEDA) ==="
kubectl get httpscaledobject -n $NS --no-headers 2>/dev/null || echo "No HSO found"
echo ""
echo "=== Recent Events (Warning only) ==="
kubectl get events -n $NS --sort-by='.lastTimestamp' --field-selector type=Warning 2>/dev/null | tail -20
echo ""
echo "=== GPU Node Availability ==="
kubectl get nodes -o custom-columns='NAME:.metadata.name,GPU_ALLOC:.status.allocatable.nvidia\.com/gpu,GPU_CAP:.status.capacity.nvidia\.com/gpu' | grep -v '<none>'
```

### 주요 status 값

| status | 의미 |
|--------|------|
| `pending` | 생성 요청 수신, 처리 전 |
| `creating` | Helm 설치 완료, Deployment/HSO 생성됨, Pod 대기 중 |
| `available` | Pod Ready, 서비스 가능 |
| `failed` | Watcher가 장애 감지 (timeout/crash) |
| `updating` | 설정 변경 반영 중 |

### endpoints 테이블 주요 컬럼 참조

| 컬럼 | 타입 | 설명 |
|------|------|------|
| `gpu` | int | GPU 개수 |
| `min_replica` / `max_replica` | int | KEDA 스케일링 범위 |
| `workload_config` | jsonb | `{"model_path": "s3://..."}` 또는 `{"model_path": "/nfs/..."}` |
| `namespace` | text | K8s 네임스페이스 (project-{uuid}) |
| `k8s_deployment_name` | text | Helm release 기반 Deployment 이름 |
| `status_message` | text | Watcher가 기록한 장애 원인 |

## Step 2 -- Pod 상세 분석

Step 1에서 문제 Pod를 식별한 후, 해당 Pod에 대해 심층 분석합니다.

```bash
NS="{NAMESPACE}"
POD="{POD_NAME}"

echo "=== Pod Describe (Events) ==="
kubectl describe pod $POD -n $NS | grep -A 30 "^Events:"

echo ""
echo "=== Container Status ==="
kubectl get pod $POD -n $NS -o jsonpath='{range .status.containerStatuses[*]}
  name={.name}
  ready={.ready}
  restartCount={.restartCount}
  state={.state}
  lastState={.lastState}
{end}'

echo ""
echo "=== Previous Logs (crash) ==="
kubectl logs $POD -n $NS --previous --tail=80 2>/dev/null || echo "No previous logs"

echo ""
echo "=== Current Logs (tail) ==="
kubectl logs $POD -n $NS --tail=80 2>/dev/null || echo "No current logs"
```

### KEDA HSO 상태 확인 (scale-to-zero 문제 시)

```bash
NS="{NAMESPACE}"
echo "=== HSO Status ==="
kubectl get httpscaledobject -n $NS -o jsonpath='{range .items[*]}
  name={.metadata.name}
  minReplica={.spec.replicas.min}
  maxReplica={.spec.replicas.max}
  paused={.metadata.annotations.autoscaling\.keda\.sh/paused-replicas}
  conditions={.status.conditions}
{end}'
```

#### KEDA scale-to-zero 디버깅 트릭

엔드포인트가 `Scaled to zero due to inactivity`로 Pod가 없을 때, 라이브 로그를 확인하려면 KEDA를 일시 정지합니다:

```bash
# 강제로 1 replica 유지 (디버깅 전용)
kubectl annotate httpscaledobject {HSO_NAME} -n {NAMESPACE} \
  autoscaling.keda.sh/paused-replicas="1" --overwrite

# 디버깅 완료 후 반드시 해제
kubectl annotate httpscaledobject {HSO_NAME} -n {NAMESPACE} \
  autoscaling.keda.sh/paused-replicas- --overwrite
```

### Helm Release 확인 (필요 시)

```bash
helm list -n {NAMESPACE} | grep {ENDPOINT_NAME}
helm status {HELM_RELEASE_NAME} -n {NAMESPACE}
```

## Step 2.5 -- StorageClass 존재 여부 검증 (PVC 바인딩 실패 시)

Pod Events에 `FailedScheduling` + PVC 관련 에러가 있는 경우에만 실행합니다.

```bash
kubectl get pvc -n {NAMESPACE} | grep {ENDPOINT_NAME}
kubectl get storageclass
```

| 진단 결과 | 원인 | 조치 |
|-----------|------|------|
| StorageClass 미존재 | 삭제/변경된 StorageClass 참조 | `tkai-nfs-agent`, `csi-rbd-sc` 등으로 변경 |
| PVC `Pending` | Provisioner 장애 또는 용량 부족 | NFS provisioner Pod 확인 |
| PVC `Bound` + Pod 실패 | PVC 외 원인 | Step 3으로 진행 |

## Step 3 -- Watcher 로직 기반 장애 분류

Endpoint Watcher(`watcher_sync.go`)의 `checkAndUpdateEndpointStatus` 로직을 따릅니다.

### 3.1 Deployment Ready 확인

```bash
kubectl get deploy {DEPLOYMENT_NAME} -n {NAMESPACE} -o jsonpath='{.status.readyReplicas}'
```

**ReadyReplicas > 0** 이면 정상. Ready가 아니면 아래 3단계 장애 판정이 진행됩니다.

### 3.2 Absolute Timeout 확인

`created_at` 기준으로 `MaxEndpointCreationAge`를 초과하면 무조건 `failed` 처리됩니다.

| status_message | 원인 | 조치 |
|---------------|------|------|
| `endpoint exceeded maximum creation age (absolute timeout)` | 최대 허용 시간 초과 | 이미지/모델 크기, 네트워크 확인 |

### 3.3 Relative Timeout 확인

| status_message | 원인 | 조치 |
|---------------|------|------|
| `endpoint did not become ready within timeout` | 모델 로딩 시간 초과 | 모델 크기 대비 리소스, GPU 가용성 점검 |

### 3.4 CrashLoop 감지

**조건**: `creating_started_at` 기준 2분(`CrashLoopMinWait`) 경과 후 검사 시작, 연속 2회(`CrashLoopConfirmCount`) 감지 시 `failed`.

Watcher `IsPodCrashLooping()` 감지 상태:

| 컨테이너 상태 | 감지 조건 |
|--------------|----------|
| `CrashLoopBackOff` | Waiting.Reason |
| `ImagePullBackOff` / `ErrImagePull` | Waiting.Reason |
| `CreateContainerConfigError` | Waiting.Reason |
| `RunContainerError` | Waiting.Reason |
| `OOMKilled` | Terminated.Reason |
| `Error` (restarts >= 3) | Terminated.Reason + RestartCount |
| High restart count (>= 5) | RestartCount only |

| status_message 패턴 | 원인 | 조치 |
|---------------------|------|------|
| `pod crash detected: CrashLoopBackOff` | 컨테이너 반복 크래시 | 이전 로그 확인, 리소스/설정 점검 |
| `pod crash detected: OOMKilled` | 메모리 초과 | resources.limits.memory 증가 (아래 VLLM 메모리 참조) |
| `pod crash detected: ImagePullBackOff` | 이미지 Pull 실패 | 이미지 경로, 레지스트리 인증 확인 |
| `pod crash detected: CreateContainerConfigError: ...` | ConfigMap/Secret 누락 | 참조 리소스 존재 확인 |
| `pod crash detected: Error (restarts: N)` | 반복 에러 종료 | 애플리케이션 로그 분석 |

#### OOMKilled 확인 방법

```bash
kubectl get pod {POD_NAME} -n {NAMESPACE} \
  -o jsonpath='{.status.containerStatuses[0].lastState.terminated}'
```

`reason: "OOMKilled"` + `exitCode: 137`이면 메모리 부족 확정.

## Step 4 -- VLLM 엔드포인트 심층 분석

### 4.1 VLLM 로그 확인

```bash
kubectl logs {POD_NAME} -n {NAMESPACE} --tail=150 2>/dev/null | \
  grep -iE "loading|warmup|ready|model|error|oom|buffer|streamer|startup"
```

### 4.2 S3 Model Streaming (Runai Streamer) 주의사항

`workload_config.model_path`가 `s3://`로 시작하면 Runai Model Streamer를 사용합니다.
`--load-format=runai_streamer` 인자가 자동 추가됩니다.

**핵심**: Runai Streamer는 모델 파일을 S3에서 직접 GPU로 스트리밍하는데, **CPU 메모리에 임시 버퍼**를 할당합니다.
이 버퍼 크기는 모델 safetensors 파일의 총 크기에 비례하며, container의 `memory limit`을 초과하면 **OOMKilled**됩니다.

```
로그 예시: [RunAI Streamer] CPU Buffer size: 7.5 GiB for files: ['model-00001-of-00003.safetensors', ...]
```

#### VLLM 모델별 최소 메모리 요구사항 (S3 Streaming)

| 모델 크기 | Safetensors 총 용량 | CPU 버퍼 | 최소 memory limit | 권장 memory limit |
|-----------|--------------------|---------|--------------------|-------------------|
| 0.5B-1B | ~1-2 GB | ~2 GiB | 4Gi | 6Gi |
| 3B-4B | ~7-8 GB | ~7.5 GiB | 10Gi | **12Gi** |
| 7B-8B | ~14-16 GB | ~15 GiB | 18Gi | 20Gi |
| 13B-14B | ~26-28 GB | ~28 GiB | 32Gi | 36Gi |
| 70B+ | ~130+ GB | TP 필요 | 모델별 계산 | 모델별 계산 |

> **현재 기본값 문제**: Helm chart 기본 memory limit은 `6Gi`입니다. 3B+ 모델의 S3 스트리밍에는 부족합니다.

#### S3 인증 확인 (NoCredentialsError)

S3 스트리밍 시 필요한 환경변수와 Secret:

```bash
# s3-credentials Secret 존재 확인
kubectl get secret s3-credentials -n {NAMESPACE} -o jsonpath='{.data}' | \
  python3 -c "import sys,json,base64; d=json.load(sys.stdin); print('\n'.join(f'{k}={base64.b64decode(v).decode()}' for k,v in d.items()))"
```

필수 키: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `S3_ENDPOINT_URL`
선택 키: `AWS_DEFAULT_REGION`, `RUNAI_STREAMER_S3_ENDPOINT` (= S3_ENDPOINT_URL과 동일 값)

### 4.3 NFS 모델 경로 (model_path가 /nfs/로 시작)

NFS 기반 모델은 S3 스트리밍 메모리 이슈가 없으나, PVC 마운트 실패 가능성이 있습니다.

### 4.4 일반적인 VLLM 장애 원인 요약

| 증상 | 원인 | 조치 |
|------|------|------|
| `OOMKilled` (exitCode 137) | S3 Streamer CPU 버퍼 > memory limit | memory limit 증가 (위 표 참조) |
| `NoCredentialsError` | S3 인증 Secret 누락/미마운트 | `s3-credentials` Secret 확인 |
| CUDA OOM | GPU VRAM 부족 | `gpu-memory-utilization` 조정, 모델 크기 확인 |
| `Port 8000 is already in use` | VLLM 멀티프로세스 포트 충돌 | 정상 동작 (자동으로 8001 사용) |
| HuggingFace 404 | 모델 ID 오류 | model_path 확인 |
| 로딩 진행 중 멈춤 | 대형 모델 로딩 시간 | Relative Timeout 설정 확인 |

## Step 5 -- Debug Deployment 생성 (선택)

Watcher가 이미 `failed` 처리한 후 라이브 로그를 보려면 별도 디버그 Deployment를 생성합니다.

> **Kyverno 정책 주의**: 독립 GPU Pod는 `vpol.validate.kyverno.svc-fail-finegrained-pod-gpu-validation` 정책에 의해 차단됩니다. 반드시 **Deployment**로 생성해야 합니다.

정상 동작하는 엔드포인트(예: `qwen3-0b`)의 Deployment를 참조하여 동일한 구조로 디버그 Deployment를 만듭니다:

```bash
# 참조용: 정상 동작 중인 엔드포인트의 리소스 설정 복사
kubectl get deploy {WORKING_ENDPOINT_DEPLOY} -n {NAMESPACE} \
  -o jsonpath='{.spec.template.spec.containers[0].resources}' | python3 -m json.tool

# 참조용: 환경변수 및 시크릿 마운트 확인
kubectl get deploy {WORKING_ENDPOINT_DEPLOY} -n {NAMESPACE} \
  -o jsonpath='{.spec.template.spec.containers[0].env}' | python3 -m json.tool
```

디버그 Deployment에는:
- 문제 모델의 `model_path`, GPU 수, `--load-format` 동일하게 설정
- S3 모델이면 `s3-credentials` Secret의 env 주입 필수
- **memory limit을 위 메모리 참조표 기준으로 충분히 설정**
- `nodeSelector: nvidia.com/gpu.present: "true"` 추가

디버깅 완료 후 반드시 정리:

```bash
kubectl delete deploy {DEBUG_DEPLOY_NAME} -n {NAMESPACE}
```

## Step 6 -- Resource Cleanup 확인

Watcher는 `failed` 처리 시 K8s 리소스를 정리합니다 (`cleanupEndpointResources`):
- Helm release 삭제
- HSO 삭제
- HuggingFace Secret 삭제

잔류 리소스 확인:

```bash
NS="{NAMESPACE}"
echo "=== Residual Helm ==="
helm list -n $NS --all | grep {ENDPOINT_NAME}
echo "=== Residual HSO ==="
kubectl get httpscaledobject -n $NS | grep {ENDPOINT_NAME}
echo "=== Residual HF Secret ==="
kubectl get secret -n $NS | grep hf-
```

## Step 7 — Source Code Change Analysis

RCA 분석 시 최근 소스코드 변경사항을 함께 확인하여 코드 변경이 장애의 원인인지 판단합니다.

### 7.1 최근 변경 이력 (Last 14 Days)

```bash
git -C ai-platform log --since="14 days ago" \
  --format="%h | %an | %ad | %s" --date=short -- \
  backend/go/internal/runner/endpoint/ \
  backend/go/internal/k8sclient/hso.go \
  backend/go/charts/container/
```

### 7.2 핵심 파일 소유자 및 최근 수정자 확인

```bash
# watcher_sync.go 최근 수정자
git -C ai-platform log --since="30 days ago" \
  --format="%an" -- backend/go/internal/runner/endpoint/watcher_sync.go \
  | sort | uniq -c | sort -rn

# 핵심 함수 변경 이력 (4-step readiness check 로직)
git -C ai-platform log --since="30 days ago" -p \
  -S "checkAndUpdateEndpointStatus" -- backend/go/internal/runner/endpoint/watcher_sync.go

# CrashLoop 감지 로직 변경 이력
git -C ai-platform log --since="30 days ago" -p \
  -S "IsPodCrashLooping" -- backend/go/internal/k8sclient/hso.go
```

### 7.3 장애 시점과 코드 변경 시점 상관관계

1. Step 1의 DB 쿼리에서 확인한 장애 발생 시각(`updated_at` 또는 `creating_started_at`)을 기준으로 합니다
2. 해당 시각 전후 커밋 확인:
   ```bash
   git -C ai-platform log --since="{ERROR_DATE} -3 days" \
     --until="{ERROR_DATE}" \
     --format="%h | %an | %ad | %s" --date=iso -- \
     backend/go/internal/runner/endpoint/ \
     backend/go/internal/k8sclient/hso.go \
     backend/go/charts/container/
   ```
3. 커밋 상세 확인:
   ```bash
   git -C ai-platform show {COMMIT_HASH} --stat
   ```

### 7.4 Helm Chart 변경 확인

```bash
git -C ai-platform log --since="14 days ago" \
  --format="%h | %an | %ad | %s" --date=short -- \
  backend/go/charts/container/
```

### 코드 변경 → 장애 상관관계 판단 기준

| 조건 | 판단 |
|------|------|
| 장애 발생 3일 이내에 관련 파일 커밋 있음 | **높은 상관관계** — 변경 내용 상세 리뷰 필요 |
| 장애 발생 7일 이내에 관련 파일 커밋 있음 | **중간 상관관계** — 변경 내용 확인 |
| 14일 이내 커밋 없음 | **낮은 상관관계** — 인프라/설정 원인 가능성 높음 |
| Helm chart 변경 있음 | **배포 설정 변경** — values 비교 필요 |

> 깊은 소유권 분석이 필요한 경우 `codebase-archaeologist` 스킬을 참고하세요.

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
- Resource Defaults: `ai-platform/backend/go/charts/container/values.yaml` (memory default: 512Mi)
