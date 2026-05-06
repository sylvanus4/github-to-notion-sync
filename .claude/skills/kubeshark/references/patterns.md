# KubeShark Patterns Reference

프로덕션 K8s 워크로드 패턴과 안티패턴. SKILL.md Step 3에서 생성/리팩토링 시 참조.

---

## Production Deployment Checklist

최소 요구사항 (모든 프로덕션 Deployment):

- [ ] replicas >= 2
- [ ] resource requests AND limits (모든 컨테이너)
- [ ] Pod-level securityContext (runAsNonRoot, fsGroup)
- [ ] Container-level securityContext (readOnlyRootFilesystem, drop ALL)
- [ ] livenessProbe + readinessProbe (별도 엔드포인트)
- [ ] startupProbe (초기화 30초+ 앱)
- [ ] topologySpreadConstraints 또는 podAntiAffinity
- [ ] PodDisruptionBudget companion
- [ ] preStop lifecycle hook
- [ ] Immutable image tag (digest 또는 SemVer, no `:latest`)
- [ ] 전용 ServiceAccount (default SA 사용 금지)

## Good Example: Production Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
  labels:
    app.kubernetes.io/name: api-server
    app.kubernetes.io/version: "1.2.3"
spec:
  replicas: 3
  selector:
    matchLabels:
      app.kubernetes.io/name: api-server
  template:
    metadata:
      labels:
        app.kubernetes.io/name: api-server
    spec:
      serviceAccountName: api-server-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 65534
        fsGroup: 65534
        seccompProfile:
          type: RuntimeDefault
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: kubernetes.io/hostname
          whenUnsatisfied: DoNotSchedule
          labelSelector:
            matchLabels:
              app.kubernetes.io/name: api-server
      containers:
        - name: api-server
          image: ghcr.io/thakicloud/api-server:v1.2.3
          ports:
            - containerPort: 8080
              protocol: TCP
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          startupProbe:
            httpGet:
              path: /healthz
              port: 8080
            failureThreshold: 30
            periodSeconds: 10
          lifecycle:
            preStop:
              exec:
                command: ["sh", "-c", "sleep 10"]
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      terminationGracePeriodSeconds: 60
      volumes:
        - name: tmp
          emptyDir: {}
```

## Bad Example: Common Anti-Patterns

```yaml
# WRONG: 거의 모든 실수를 포함한 예시
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  replicas: 1                          # 단일 replica -> 가용성 0
  selector:
    matchLabels:
      app: api-server
  template:
    metadata:
      labels:
        app: api-server
    spec:
      # serviceAccountName 누락 -> default SA 사용
      # securityContext 완전 누락 -> root 실행
      containers:
        - name: api-server
          image: api-server:latest      # mutable tag
          ports:
            - containerPort: 8080
          # resources 누락 -> BestEffort QoS
          # probes 누락 -> K8s가 건강 상태 모름
          # securityContext 누락
```

## Validation Pipeline

매니페스트 검증 3단계:

```bash
# 1. Client-side schema validation
kubeconform -strict -kubernetes-version 1.30.0 \
  -schema-location default \
  manifest.yaml

# 2. Policy check
kube-linter lint manifest.yaml \
  --config .kube-linter.yaml

# 3. Server-side dry-run
kubectl apply --dry-run=server -f manifest.yaml
```

## Do/Don't Quick Reference

| Do | Don't |
|----|-------|
| `runAsNonRoot: true` | root로 실행 |
| `readOnlyRootFilesystem: true` | writable root |
| `capabilities.drop: ["ALL"]` | capabilities 미설정 |
| `image: app:v1.2.3` | `image: app:latest` |
| 전용 ServiceAccount | default SA |
| ClusterIP Service | NodePort (프로덕션) |
| livenessProbe: `/healthz` | livenessProbe: DB 연결 체크 |
| `maxUnavailable: 0` | `maxUnavailable: 25%` (zero-downtime 필요 시) |
| Secret 파일 마운트 | Secret env var 주입 |
| NetworkPolicy deny-all base | NetworkPolicy 없음 |
| PDB companion | PDB 없이 Deployment |
| `preStop: sleep 10` | preStop 없이 배포 |
