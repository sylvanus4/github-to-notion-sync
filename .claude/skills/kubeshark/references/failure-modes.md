# KubeShark Failure Mode Reference

6가지 K8s failure mode 상세 체크리스트. SKILL.md Step 2에서 참조.
출처: kubernetes-skill (MIT) + NSA/CISA K8s Hardening Guide + OWASP K8s Top 10 + CIS Benchmark.

---

## FM1: Insecure Workload Defaults

K8s 워크로드는 기본값이 위험하게 관대하다. 명시적 보안 설정 필수.

### 필수 securityContext (Pod-level)

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 65534
  fsGroup: 65534
  seccompProfile:
    type: RuntimeDefault
```

### 필수 securityContext (Container-level)

```yaml
securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: ["ALL"]
```

### LLM 흔한 실수

- `securityContext` 완전 누락 (가장 빈번)
- `runAsNonRoot: true` 설정하면서 `runAsUser` 미지정
- `readOnlyRootFilesystem` 누락 (writable root = 공격 표면)
- capabilities drop 없이 add만 사용

### PSS (Pod Security Standards) 레벨

| Level | 용도 | 강제 |
|-------|------|------|
| privileged | 시스템 컴포넌트 only | 제한 없음 |
| baseline | 최소 보안 | hostNetwork/hostPID/hostIPC 금지 |
| restricted | 프로덕션 워크로드 | 위 + runAsNonRoot + drop ALL + seccomp |

네임스페이스 레이블로 강제:
```yaml
labels:
  pod-security.kubernetes.io/enforce: restricted
  pod-security.kubernetes.io/warn: restricted
```

### TKAI 특이사항

- GPU 워크로드는 `privileged` PSS가 필요할 수 있음 (NVIDIA device plugin)
- `kai-scheduler` 사용 시 `schedulerName: kai-scheduler` 명시 필수

---

## FM2: Resource Starvation

requests/limits 미설정 = 프로덕션 인시던트 예고.

### QoS Classes

| Class | 조건 | 리스크 |
|-------|------|--------|
| Guaranteed | requests == limits (모든 컨테이너) | 가장 안전 |
| Burstable | requests < limits | OOM 우선 대상 |
| BestEffort | requests/limits 모두 미설정 | 가장 먼저 evict |

### 필수 설정

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

### LLM 흔한 실수

- requests/limits 완전 누락
- CPU limits 과도하게 높게 설정 (throttling 무시)
- Memory limits < requests (즉시 OOMKilled)
- Init container에 requests 미설정

### PodDisruptionBudget 필수

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 1  # 또는 maxUnavailable: 1
  selector:
    matchLabels:
      app: myapp
```

### TKAI GPU 리소스

```yaml
resources:
  requests:
    nvidia.com/gpu: "1"
  limits:
    nvidia.com/gpu: "1"
```

MIG 파티션: `nvidia.com/mig-1g.5gb: 1` 형식.

---

## FM3: Network Exposure

K8s 기본값: 모든 Pod가 모든 Pod에 모든 포트로 접근 가능.

### Deny-by-default NetworkPolicy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

### 허용 정책 (명시적 egress 포함)

```yaml
spec:
  podSelector:
    matchLabels:
      app: myapp
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - port: 8080
  egress:
    - to:
        - namespaceSelector: {}
      ports:
        - port: 53
          protocol: UDP
        - port: 53
          protocol: TCP
```

### LLM 흔한 실수

- NetworkPolicy 완전 누락
- Egress 정책 없이 ingress만 설정 (DNS port 53 누락 -> 이름 해석 실패)
- NodePort/LoadBalancer를 내부 서비스에 사용

### Service 타입 선택

| Type | 용도 | 프로덕션 |
|------|------|----------|
| ClusterIP | 내부 통신 | 기본값 |
| NodePort | 개발/테스트 | 프로덕션 금지 |
| LoadBalancer | 외부 노출 | Ingress 뒤에서만 |

---

## FM4: Privilege Sprawl

RBAC 최소 권한 원칙 위반 = 보안 사고 예고.

### 위험 패턴

```yaml
# NEVER: 와일드카드 RBAC
rules:
  - apiGroups: ["*"]
    resources: ["*"]
    verbs: ["*"]

# NEVER: cluster-admin binding to workload SA
subjects:
  - kind: ServiceAccount
    name: my-app
roleRef:
  kind: ClusterRole
  name: cluster-admin
```

### 안전 패턴

```yaml
# 네임스페이스 스코프 Role (ClusterRole 대신)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: myapp
  name: myapp-role
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list"]
```

### Secret 관리

- env var 주입 금지 -> 파일 마운트 사용
- 외부 secret store 연동 (ExternalSecret + Vault/AWS SM)

### LLM 흔한 실수

- default ServiceAccount 사용 (전용 SA 생성 필수)
- ClusterRole을 namespace-scope 작업에 사용
- Secret을 env var로 주입

---

## FM5: Fragile Rollouts

잘못된 rollout은 rollout 안 하는 것보다 나쁘다.

### Probe 규칙

| Probe | 용도 | 금지 사항 |
|-------|------|----------|
| livenessProbe | 컨테이너 재시작 판단 | 외부 의존성 체크 금지 (DB, API) |
| readinessProbe | 트래픽 수신 가능 판단 | 무거운 체크 금지 |
| startupProbe | 느린 시작 앱용 | failureThreshold 충분히 |

### Zero-downtime Deployment

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  template:
    spec:
      terminationGracePeriodSeconds: 60
      containers:
        - lifecycle:
            preStop:
              exec:
                command: ["sh", "-c", "sleep 10"]
```

### LLM 흔한 실수

- livenessProbe에서 DB 연결 체크 (-> cascading restart)
- `:latest` 태그 사용 (mutable -> 재현 불가)
- `preStop` hook 누락 (in-flight 요청 손실)
- readinessProbe 없이 livenessProbe만 설정

### TKAI Argo Rollouts

TKAI는 Argo Rollouts 사용. 기본 Deployment strategy 대신:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
spec:
  strategy:
    canary:
      steps:
        - setWeight: 20
        - pause: {duration: 5m}
        - setWeight: 50
        - pause: {duration: 5m}
```

---

## FM6: API Drift

deprecated/removed API 사용 = 업그레이드 시 장애.

### 주요 마이그레이션 (LLM이 자주 틀리는 것)

| Resource | Old API | Current API | Removed Since |
|----------|---------|-------------|---------------|
| Ingress | `extensions/v1beta1` | `networking.k8s.io/v1` | 1.22 |
| HPA | `autoscaling/v2beta1` | `autoscaling/v2` | 1.26 |
| PDB | `policy/v1beta1` | `policy/v1` | 1.25 |
| CronJob | `batch/v1beta1` | `batch/v1` | 1.25 |
| CSIDriver | `storage.k8s.io/v1beta1` | `storage.k8s.io/v1` | 1.22 |

### 검증 방법

```bash
# kubeconform으로 타겟 K8s 버전 검증
kubeconform -kubernetes-version 1.30.0 -strict manifest.yaml

# kubectl로 서버사이드 dry-run
kubectl apply --dry-run=server -f manifest.yaml
```

### LLM 흔한 실수

- `extensions/v1beta1` Ingress 생성 (가장 빈번)
- `autoscaling/v2beta1` HPA 사용
- Ingress에 `ingressClassName` 미지정 (1.18+ 필수)
- CronJob `batch/v1beta1` 사용
