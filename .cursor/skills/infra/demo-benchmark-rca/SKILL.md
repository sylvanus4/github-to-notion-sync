---
name: demo-benchmark-rca
description: >-
  Systematic RCA for AI Platform Demo Benchmark errors.
  Guides through DB status queries, K8s Job/Pod inspection, Kueue Workload checks,
  PVC verification, failure classification, and a decision tree mapping error patterns to root causes.
  Use when the user asks to "debug benchmark", "benchmark error", "benchmark failed",
  "benchmark RCA", "벤치마크 에러", "벤치마크 장애", "벤치마크 원인 분석",
  "demo-benchmark-rca", "lm-eval error", "벤치마크 트러블슈팅",
  "benchmark stuck", "benchmark creating timeout",
  or encounters a failed/stuck benchmark in the AI Platform Demo environment.
  Do NOT use for Workload errors (use demo-workload-rca).
  Do NOT use for Serverless/Endpoint errors (use demo-serverless-rca).
  Do NOT use for Pipeline Builder errors (use demo-pipeline-rca).
  Do NOT use for Tabular/ML Studio errors (use demo-tabular-rca).
  Do NOT use for Text Generation errors (use demo-text-generation-rca).
  Do NOT use for production environment troubleshooting.
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "infra"
  platforms: [darwin]
---

# Demo Benchmark RCA

Benchmark 에러 발생 시 체계적으로 근본 원인을 분석하는 스킬입니다.
Benchmark는 `lm-eval` 기반 언어 모델 평가를 K8s Job으로 실행합니다.

## Pre-flight (한 번에 실행)

```bash
# 1. VPN 연결 확인
ping -c1 demo-k8s-api-endpoint

# 2. Demo 클러스터 컨텍스트
kubectx demo

# 3. DB 포트포워드 (ai_platform_db)
kubectl port-forward -n postgresql svc/cnpg-cluster-rw 5432:5432 &
```

## Step 1: DB 상태 확인

### 1.1 실패/정체 벤치마크 조회

```sql
SELECT id, project_id, status, error_message,
       pod_name, k8s_namespace, k8s_job_name,
       benchmark_type, model_name,
       to_timestamp(created_at) as created_time,
       to_timestamp(updated_at) as updated_time,
       NOW() - to_timestamp(updated_at) as stuck_duration
FROM benchmark_runs
WHERE status IN ('failed', 'creating', 'running')
ORDER BY updated_at DESC
LIMIT 20;
```

| 컬럼 | 설명 |
|------|------|
| `id` | 벤치마크 고유 ID |
| `project_id` | 프로젝트 ID (네임스페이스 결정) |
| `status` | `pending` / `creating` / `running` / `completed` / `failed` |
| `error_message` | Watcher/Handler가 설정한 실패 원인 |
| `pod_name` | K8s Job Pod 이름 |
| `k8s_namespace` | K8s 네임스페이스 |
| `k8s_job_name` | K8s Job 이름 |
| `benchmark_type` | 벤치마크 유형 |
| `model_name` | 평가 대상 모델 |
| `created_at` | 생성 시각 (epoch seconds) |
| `updated_at` | 마지막 업데이트 시각 (epoch seconds) |

### 1.2 상태 분포 확인

```sql
SELECT status, COUNT(*) as cnt
FROM benchmark_runs
GROUP BY status
ORDER BY cnt DESC;
```

### 1.3 특정 벤치마크 상세 조회

```sql
SELECT id, project_id, status, error_message,
       pod_name, k8s_namespace, k8s_job_name,
       benchmark_type, model_name,
       gpu_count, gpu_type,
       to_timestamp(created_at) as created_time,
       to_timestamp(updated_at) as updated_time
FROM benchmark_runs
WHERE id = '{BENCHMARK_ID}';
```

## Step 2: K8s Job 상태 확인

```bash
# 벤치마크의 K8s Job 조회 (label selector)
kubectl get jobs -n {NAMESPACE} -l benchmark-id={BENCHMARK_ID}

# Job 상세 (Events, Conditions 확인)
kubectl describe job {JOB_NAME} -n {NAMESPACE}

# Job의 Pod 목록
kubectl get pods -n {NAMESPACE} -l benchmark-id={BENCHMARK_ID}

# Pod 로그 (lm-eval 출력)
kubectl logs {POD_NAME} -n {NAMESPACE} --tail=200

# 이전 로그 (크래시된 경우)
kubectl logs {POD_NAME} -n {NAMESPACE} --previous

# Pod 상세 (OOMKilled, Evicted 등 확인)
kubectl describe pod {POD_NAME} -n {NAMESPACE}
```

### 2.1 Pod 상태별 확인 포인트

| Pod Status | 확인 사항 |
|------------|-----------|
| `Pending` | 리소스 부족, GPU 할당 대기, PVC 바인딩 대기 |
| `Running` → 장시간 | lm-eval 실행 중이거나 hang 상태 |
| `Failed` | Exit code, OOMKilled, Evicted 확인 |
| `Succeeded` | 정상 완료 (results PVC에 결과 저장) |
| `Unknown` | 노드 통신 장애 |

### 2.2 Kueue Workload 확인 (Kueue 활성화 시)

```bash
# Kueue Workload 조회
kubectl get workloads -n {NAMESPACE} -l benchmark-id={BENCHMARK_ID}

# Workload 상세 (admission, conditions 확인)
kubectl describe workload {WORKLOAD_NAME} -n {NAMESPACE}
```

**Kueue 상태 해석:**

| Kueue State | 의미 | 조치 |
|-------------|------|------|
| `Pending` | 큐에서 리소스 대기 중 | GPU 가용성 확인, `BenchmarkCreatingTimeout` 억제됨 (최대 24시간) |
| `QuotaReserved` | 쿼타 예약됨, 아직 미실행 | 곧 실행 예정, `BenchmarkCreatingTimeout` 억제됨 |
| `Suspended` | 일시 중단됨 | Kueue가 중단 결정, 관리자 확인 필요 |
| `Evicted` | Kueue에 의해 축출됨 | 우선순위가 높은 작업에 밀림, 재제출 고려 |
| `Admitted` | 승인 완료, 실행 중 | 정상 상태 |

> **참고**: Kueue가 활성화된 경우, `Pending` 또는 `QuotaReserved` 상태에서는 `BenchmarkCreatingTimeout`이 억제됩니다. 대신 `KueueMaxQueueDuration` (24시간)이 적용됩니다.

## Step 3: PVC 확인

Benchmark는 두 가지 PVC를 사용합니다:

```bash
# HF Cache PVC (모델 캐시)
kubectl get pvc -n {NAMESPACE} -l benchmark-pvc-type=hf-cache,project-id={PROJECT_ID}

# Results PVC (결과 저장)
kubectl get pvc -n {NAMESPACE} -l benchmark-pvc-type=results,project-id={PROJECT_ID}

# PVC 상세 확인
kubectl describe pvc {PVC_NAME} -n {NAMESPACE}
```

| PVC 유형 | 용도 | 기본 크기 |
|----------|------|-----------|
| `hf-cache` | HuggingFace 모델 캐시 (`BENCHMARK_HF_CACHE_SIZE`) | config 참조 |
| `results` | lm-eval 결과 파일 (`BENCHMARK_RESULTS_SIZE`) | config 참조 |

**PVC 문제 패턴:**

| 증상 | 원인 | 조치 |
|------|------|------|
| `Pending` 상태 | StorageClass 미존재 또는 프로비저닝 실패 | `kubectl get sc`, CSI 드라이버 확인 |
| `Bound` but Job fails | 용량 부족 | PVC 크기 증가 |
| PVC 없음 | `BENCHMARK_AUTO_CREATE_PVC=false`이고 사전 생성 안됨 | config 확인 |

## Step 4: Failure Decision Tree

### `error_message` 패턴별 근본 원인

```
error_message 확인
├── "benchmark creating timeout" 포함
│   ├── Kueue 활성화?
│   │   ├── Yes → Kueue Workload 상태 확인 (Step 2.2)
│   │   │   ├── Pending/QuotaReserved 24시간 초과 → GPU 리소스 부족, 큐 관리자 확인
│   │   │   ├── Evicted → 우선순위 밀림, 재제출
│   │   │   └── Suspended → 관리자 개입 필요
│   │   └── No → BenchmarkCreatingTimeout (10분) 초과
│   │       ├── Pod Pending → GPU 리소스 부족
│   │       ├── PVC Pending → StorageClass/CSI 문제
│   │       └── ImagePull 실패 → 이미지 레지스트리 확인
│   └── 조치: Job describe, Pod events 확인
│
├── "job not found" / "benchmark job missing" 포함
│   ├── Kueue eviction으로 Job 삭제됨
│   ├── 수동으로 Job 삭제됨
│   └── 조치: `kubectl get jobs -n {NS}` 확인, Kueue events 조회
│
├── "Evicted" 포함
│   ├── 노드 리소스 pressure로 축출
│   ├── Kueue preemption에 의한 축출
│   └── 조치: 노드 상태 확인 `kubectl describe node`, 리소스 요청 조정
│
├── "Preempted" 포함
│   ├── 메시지: "Kueue에서 우선순위가 높은 작업에 의해 벤치마크가 선점되었습니다"
│   ├── Kueue priority class 확인
│   └── 조치: 우선순위 조정 또는 재제출
│
├── "OOMKilled" 포함
│   ├── 메시지: "Benchmark container가 메모리 부족(OOM)으로 종료되었습니다"
│   ├── 모델 크기 대비 메모리 할당 부족
│   └── 조치: memory limit 증가, 더 작은 배치 사이즈 사용
│
├── "namespace" 관련 에러
│   ├── 프로젝트 네임스페이스 미존재
│   └── 조치: 네임스페이스 생성 확인, 프로젝트 설정 점검
│
├── "running without K8s Job" / stuck running
│   ├── Watcher가 K8s에서 Job을 찾지 못함
│   ├── Job이 수동 삭제되었거나 GC됨
│   └── 조치: DB 상태와 K8s 실제 상태 비교
│
├── error_message 비어있고 status = 'failed'
│   ├── Handler 레벨 에러 (PVC 생성 실패, Job 생성 실패)
│   ├── Task Runner 로그 확인 필요
│   └── 조치: Task Runner 로그에서 benchmark_id로 grep
│
└── error_message 비어있고 status = 'creating' 장시간
    ├── NATS 이벤트 미수신 (benchmark.created)
    ├── Handler 처리 중 panic
    └── 조치: NATS stream 확인, Task Runner 로그 확인
```

## Step 5: Benchmark Status Lifecycle

```
pending ──(NATS: benchmark.created)──> creating
                                          │
                    ┌─────────────────────┤
                    │                     │
              PVC 생성 실패          PVC 생성 성공
              → failed               Job 생성
                                          │
                                    ┌─────┤
                                    │     │
                              Job 실패  Job 성공
                              → failed  → running
                                          │
                                    ┌─────┤
                                    │     │
                              Pod 실패  Pod 완료
                              → failed  → completed
```

## Step 6: NATS 이벤트 흐름

### 이벤트 유형

| Subject | 트리거 | Handler |
|---------|--------|---------|
| `benchmark.created` | 벤치마크 생성 API | `HandleBenchmarkCreated` — 네임스페이스 확인, PVC 생성, K8s Job 제출 |
| `benchmark.deleted` | 벤치마크 삭제 API | `HandleBenchmarkDeleted` — K8s Job 정리, 스토리지 정리 |

### NATS 디버깅

```bash
# Task Runner 로그에서 benchmark 이벤트 처리 확인
kubectl logs -n {TASK_RUNNER_NS} deploy/task-runner --tail=500 | grep -i "benchmark"

# 특정 벤치마크 이벤트 추적
kubectl logs -n {TASK_RUNNER_NS} deploy/task-runner --tail=500 | grep "{BENCHMARK_ID}"
```

## Step 7: Common Failure Matrix

| 증상 | 가능한 원인 | 확인 명령 | 해결 방법 |
|------|-------------|-----------|-----------|
| `creating` 10분+ 정체 | GPU 부족, PVC Pending | `kubectl get pods,pvc -n {NS}` | 리소스 확인, PVC 상태 확인 |
| `creating` 24시간+ (Kueue) | Kueue 큐 대기 시간 초과 | `kubectl get workloads -n {NS}` | GPU 가용성 확인, priority 조정 |
| `running` but Job 없음 | Job 수동 삭제 또는 GC | `kubectl get jobs -n {NS}` | DB 상태 수동 업데이트 |
| `failed` — OOMKilled | 모델 크기 > 메모리 | `kubectl describe pod` | memory limit 증가 |
| `failed` — Evicted | 노드 pressure | `kubectl describe node` | 다른 노드로 스케줄링 |
| `failed` — Preempted | Kueue 우선순위 | `kubectl get workloads` | priority class 조정 |
| `failed` — namespace | 네임스페이스 미존재 | `kubectl get ns` | 프로젝트 설정 확인 |
| `failed` — image pull | 이미지 레지스트리 접근 | `kubectl describe pod` | 이미지/시크릿 확인 |
| `failed` — PVC 생성 | StorageClass 없음 | `kubectl get sc` | StorageClass 생성 |
| `pending` 장시간 | NATS 이벤트 미전달 | Task Runner 로그 | NATS stream 확인 |

## Step 8: lm-eval 관련 디버깅

Benchmark는 `lm-eval` 프레임워크를 사용하여 언어 모델을 평가합니다.

### 8.1 lm-eval 실행 스크립트 구조

Job은 내부적으로 다음과 같은 스크립트를 실행합니다:

```bash
# 각 태스크별 lm_eval 명령 생성 (job_builder.go 참조)
lm_eval --model {model_type} \
        --model_args {model_args} \
        --tasks {task_name} \
        --num_fewshot {num_fewshot} \
        --output_path {results_dir}/{task_name} \
        --batch_size {batch_size} \
        [--limit {test_limit}] \
        [--log_samples] \
        [--gen_kwargs {gen_kwargs}] \
        [{extra_flags}]
```

### 8.2 lm-eval 에러 패턴

| 에러 패턴 | 원인 | 조치 |
|-----------|------|------|
| `model not found` | 모델 경로/이름 오류 | HF cache PVC에 모델 존재 확인 |
| `task not found` | 태스크 이름 오류 | lm-eval 지원 태스크 목록 확인 |
| `CUDA out of memory` | GPU 메모리 부족 | batch_size 감소, GPU 타입 변경 |
| `Connection error` | 모델 다운로드 실패 | HF 네트워크 접근 확인 |
| `results parsing failed` | 결과 JSON 파싱 오류 | 결과 PVC에서 파일 직접 확인 |

### 8.3 결과 확인

```bash
# Results PVC 내용 확인 (Job 완료 후)
kubectl exec -n {NAMESPACE} {POD_NAME} -- ls -la {BENCHMARK_RESULTS_DIRECTORY}

# 결과 JSON 확인
kubectl exec -n {NAMESPACE} {POD_NAME} -- cat {BENCHMARK_RESULTS_DIRECTORY}/{TASK_NAME}/results.json
```

## Step 9: Task Runner 로그 분석

```bash
# Task Runner 로그에서 벤치마크 관련 에러 확인
kubectl logs -n {TASK_RUNNER_NS} deploy/task-runner --tail=1000 | grep -E "(benchmark|BENCHMARK)" | tail -50

# 특정 벤치마크 ID로 필터링
kubectl logs -n {TASK_RUNNER_NS} deploy/task-runner --tail=2000 | grep "{BENCHMARK_ID}"

# Watcher 관련 로그
kubectl logs -n {TASK_RUNNER_NS} deploy/task-runner --tail=1000 | grep -i "benchmark.*watcher"

# Handler 에러
kubectl logs -n {TASK_RUNNER_NS} deploy/task-runner --tail=1000 | grep -i "HandleBenchmark"
```

## Watcher Thresholds Reference

| 파라미터 | 기본값 | 소스 | 설명 |
|----------|--------|------|------|
| `DefaultBenchmarkWatchInterval` | 10s | `watcher.go` 상수 | Watcher 폴링 간격 |
| `BenchmarkCreatingTimeout` | 10분 | `watcher.go` 상수 | `creating` 상태 최대 허용 시간 |
| `BenchmarkRunningTimeout` | 24시간 | `watcher.go` 상수 | `running` 상태 최대 허용 시간 |
| `KueueMaxQueueDuration` | 24시간 | `watcher_kueue.go` 상수 | Kueue 큐 대기 최대 시간 (creating timeout 억제) |
| `BENCHMARK_HEALTH_CHECK_INTERVAL` | 30s | `taskrunner.go` env | Health check 간격 |
| `BENCHMARK_NAMESPACE` | config | `taskrunner.go` env | 벤치마크 전용 네임스페이스 |
| `BENCHMARK_IMAGE` | config | `taskrunner.go` env | lm-eval 실행 컨테이너 이미지 |
| `BENCHMARK_KUEUE_QUEUE_NAME` | config | `taskrunner.go` env | Kueue 로컬 큐 이름 |
| `BENCHMARK_KUEUE_PRIORITY_CLASS` | config | `taskrunner.go` env | Kueue 우선순위 클래스 |
| `BENCHMARK_AUTO_CREATE_PVC` | config | `taskrunner.go` env | PVC 자동 생성 여부 |
| `BENCHMARK_STORAGE_CLASS` | config | `taskrunner.go` env | PVC StorageClass |
| `BENCHMARK_HF_CACHE_SIZE` | config | `taskrunner.go` env | HF 캐시 PVC 크기 |
| `BENCHMARK_RESULTS_SIZE` | config | `taskrunner.go` env | 결과 PVC 크기 |
| `BENCHMARK_TEST_LIMIT` | config | `taskrunner.go` env | 테스트 제한 (디버깅용) |

## Source Code Change Analysis

최근 코드 변경이 벤치마크 장애의 원인일 수 있습니다:

```bash
# Benchmark runner 최근 변경사항
git log --oneline -20 -- ai-platform/backend/go/internal/runner/benchmark/

# 특정 파일 변경 이력
git log --oneline -10 -- ai-platform/backend/go/internal/runner/benchmark/watcher.go
git log --oneline -10 -- ai-platform/backend/go/internal/runner/benchmark/handlers.go
git log --oneline -10 -- ai-platform/backend/go/internal/runner/benchmark/job_builder.go
git log --oneline -10 -- ai-platform/backend/go/internal/runner/benchmark/failure_classifier.go

# Kueue 통합 변경사항
git log --oneline -10 -- ai-platform/backend/go/internal/runner/benchmark/watcher_kueue.go
git log --oneline -10 -- ai-platform/backend/go/internal/runner/benchmark/watcher_kueue_event.go

# 공통 runner 변경사항 (benchmark에 영향 가능)
git log --oneline -10 -- ai-platform/backend/go/internal/runner/common/
```

## Source Code Reference

| 파일 | 역할 |
|------|------|
| `runner/benchmark/watcher.go` | `StartBenchmarkWatcher` — DB 폴링, Job 상태 동기화, timeout 감지, stuck 복구 |
| `runner/benchmark/handlers.go` | `HandleBenchmarkCreated` — 네임스페이스 확인, PVC 생성, Job 제출; `HandleBenchmarkDeleted` — 정리 |
| `runner/benchmark/db.go` | DB 상태 업데이트 (`creating`, `running`, `failed`), PVC 관리 (`ensureBenchmarkPVCs`) |
| `runner/benchmark/failure_classifier.go` | Pod 실패 분류 — Evicted/Preempted/OOMKilled 벤치마크 메시지 변환 |
| `runner/benchmark/job_builder.go` | K8s Job 스펙 생성, `lm-eval` 스크립트 빌드, `validateExtraFlags` 보안 검증 |
| `runner/benchmark/watcher_kueue.go` | Kueue 통합 — timeout 억제, 상태 enrichment, eviction 처리 |
| `runner/benchmark/watcher_kueue_event.go` | Kueue 중단 이벤트 emit (`KueueInterruptionQueueTimeout/Suspended/Evicted/JobMissing`) |
| `config/taskrunner.go` | `BENCHMARK_*` 환경 변수 설정 |
