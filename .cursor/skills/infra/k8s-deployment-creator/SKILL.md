---
name: k8s-deployment-creator
description: >-
  Generate production-grade Kubernetes workload manifests for the TKAI AI
  Platform. Covers Deployments (with Argo Rollouts canary/blue-green
  support), StatefulSets, DaemonSets, Jobs/CronJobs, Services,
  Ingress/IngressRoute, PVCs, ConfigMaps, Secrets, KEDA HTTPScaledObjects,
  Pod Disruption Budgets, and GPU/MIG resource requests with
  kai-scheduler. Generates Helm chart templates following the project's
  chart patterns at ai-platform/backend/go/charts/{container,vllm}/. Use
  when the user asks to "create deployment", "generate K8s manifest",
  "write Helm template", "GPU pod spec", "inference deployment", "model
  serving manifest", "KEDA scaling", "canary deployment", "Argo Rollouts",
  "K8s 디플로이먼트 생성", "Helm 차트 작성", "GPU 파드 스펙",
  "추론 서비스 배포", "KEDA 스케일링", "카나리 배포", "모델 서빙",
  "k8s-deployment-creator", or any Kubernetes workload manifest
  generation task. Do NOT use for validating existing manifests (use
  k8s-manifest-validator). Do NOT use for GitOps deployment patterns (use
  argocd-gitops-patterns). Do NOT use for Helm chart linting (use
  helm-validator). Do NOT use for CI/CD pipeline design (use
  sre-devops-expert).
metadata:
  version: "1.1.0"
  category: "infra"
  author: "thaki"
---

# K8s Deployment Creator

You are a Kubernetes workload generator for the TKAI AI Platform.

## Project Context

- Helm charts: `ai-platform/backend/go/charts/{container,vllm}/`
- Clusters: k0s-based, 6 TKAI clusters (stage, dev, b200, demo, master, kata)
- Container runtime: containerd
- GPU types: NVIDIA A100, B200 with MIG support
- **Custom scheduler: `kai-scheduler`** for GPU workloads
- **Autoscaling: KEDA HTTPScaledObject** (not HPA)
- **Progressive delivery: Argo Rollouts** (canary/blue-green)
- **Job scheduling: Kueue** with priority-class labels
- Registry: GHCR (`ghcr.io/thakicloud/`)
- Image tag flow: `dev-*` → `rc-*` → `vYYYY.MM.DD`

## Core Templates

### Standard Go Microservice (container chart pattern)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
  labels:
    app.kubernetes.io/name: {{ .Release.Name }}
    app.kubernetes.io/instance: {{ .Release.Name }}
spec:
  {{- if not .Values.keda.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {{ .Release.Name }}
    spec:
      serviceAccountName: {{ .Release.Name }}
      containers:
        - name: {{ .Release.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 15
            periodSeconds: 20
          readinessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          envFrom:
            - configMapRef:
                name: {{ .Release.Name }}-config
            - secretRef:
                name: {{ .Release.Name }}-secret
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

### GPU Inference Service (vLLM chart pattern)

The vLLM Helm chart at `charts/vllm/` is the most complex template in the project:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
  labels:
    {{- include "vllm.labels" . | nindent 4 }}
    {{- if .Values.kueue.enabled }}
    kueue.x-k8s.io/priority-class: {{ .Values.kueue.priorityClass }}
    {{- end }}
spec:
  {{- if not .Values.keda.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "vllm.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "vllm.labels" . | nindent 8 }}
    spec:
      {{- if .Values.schedulerName }}
      schedulerName: {{ .Values.schedulerName }}   # kai-scheduler
      {{- end }}
      serviceAccountName: {{ .Release.Name }}
      {{- if .Values.initContainer.enabled }}
      initContainers:
        - name: model-bootstrap
          image: "{{ .Values.initContainer.image }}"
          command:
            - /bin/sh
            - -c
            - |
              # NFS lock handling: wait for any existing lock
              LOCK_FILE="{{ .Values.initContainer.modelPath }}/.download.lock"
              CACHE_DIR="{{ .Values.initContainer.modelPath }}/cache-$(hostname)"
              
              if [ -f "$LOCK_FILE" ]; then
                echo "Another pod is downloading. Waiting..."
                while [ -f "$LOCK_FILE" ]; do sleep 5; done
              fi
              
              # Pod-unique cache directory to avoid cross-pod conflicts
              mkdir -p "$CACHE_DIR"
              
              # Download model via huggingface-cli or s3
              {{- if .Values.s3ModelStreaming.enabled }}
              runai-model-streamer download \
                --source {{ .Values.s3ModelStreaming.source }} \
                --dest "$CACHE_DIR"
              {{- else }}
              touch "$LOCK_FILE"
              huggingface-cli download {{ .Values.model.name }} --cache-dir "$CACHE_DIR"
              rm -f "$LOCK_FILE"
              {{- end }}
          volumeMounts:
            - name: model-storage
              mountPath: {{ .Values.initContainer.modelPath }}
          securityContext:
            runAsUser: 1000
            runAsGroup: 2000
      {{- end }}
      containers:
        - name: vllm
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - name: http
              containerPort: {{ .Values.service.port | default 8000 }}
          args:
            - --model={{ .Values.model.name }}
            - --tensor-parallel-size={{ .Values.model.tensorParallelSize | default 1 }}
            - --gpu-memory-utilization={{ .Values.model.gpuMemoryUtilization | default "0.9" }}
            - --max-model-len={{ .Values.model.maxModelLen | default 4096 }}
            {{- if .Values.s3ModelStreaming.enabled }}
            - --load-format=runai_streamer
            {{- end }}
            {{- range .Values.extraArgs }}
            - {{ . }}
            {{- end }}
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 240
            periodSeconds: 30
            failureThreshold: 10
          readinessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 60
            periodSeconds: 10
          startupProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
            failureThreshold: 60
          resources:
            limits:
              nvidia.com/gpu: {{ .Values.resources.limits.gpu | default 1 }}
              memory: {{ .Values.resources.limits.memory }}
            requests:
              nvidia.com/gpu: {{ .Values.resources.requests.gpu | default 1 }}
              memory: {{ .Values.resources.requests.memory }}
              cpu: {{ .Values.resources.requests.cpu }}
          securityContext:
            runAsUser: 1000
            fsGroup: 2000
            readOnlyRootFilesystem: false
          volumeMounts:
            - name: model-storage
              mountPath: {{ .Values.initContainer.modelPath }}
            - name: shm
              mountPath: /dev/shm
      volumes:
        - name: model-storage
          persistentVolumeClaim:
            claimName: {{ .Values.persistence.existingClaim | default (printf "%s-model" .Release.Name) }}
        - name: shm
          emptyDir:
            medium: Memory
            sizeLimit: {{ .Values.shmSize | default "16Gi" }}
```

### KEDA HTTPScaledObject (replaces HPA)

The project uses KEDA for HTTP-based autoscaling rather than the Kubernetes HPA:

```yaml
{{- if .Values.keda.enabled }}
apiVersion: http.keda.sh/v1alpha1
kind: HTTPScaledObject
metadata:
  name: {{ .Release.Name }}
spec:
  hosts:
    - {{ .Values.keda.host }}
  pathPrefixes:
    - /
  scaleTargetRef:
    name: {{ .Release.Name }}
    kind: Deployment
    apiVersion: apps/v1
  replicas:
    min: {{ .Values.keda.minReplicas | default 1 }}
    max: {{ .Values.keda.maxReplicas | default 10 }}
  scalingMetric:
    requestRate:
      targetValue: {{ .Values.keda.targetRequestRate | default 100 }}
      granularity: "1s"
      window: "1m"
{{- end }}
```

### Argo Rollouts (Canary / Blue-Green)

```yaml
{{- if .Values.rollout.enabled }}
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: {{ .Release.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  strategy:
    {{- if eq .Values.rollout.strategy "canary" }}
    canary:
      steps:
        - setWeight: 20
        - pause: { duration: 30s }
        - setWeight: 50
        - pause: { duration: 60s }
        - setWeight: 80
        - pause: { duration: 60s }
      canaryService: {{ .Release.Name }}-canary
      stableService: {{ .Release.Name }}-stable
    {{- else if eq .Values.rollout.strategy "blueGreen" }}
    blueGreen:
      activeService: {{ .Release.Name }}-active
      previewService: {{ .Release.Name }}-preview
      autoPromotionEnabled: false
    {{- end }}
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ .Release.Name }}
  template:
    # ... same as Deployment template spec
{{- end }}
```

### Job / CronJob with Kueue

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ .Release.Name }}-batch
  labels:
    kueue.x-k8s.io/priority-class: {{ .Values.kueue.priorityClass | default "default" }}
spec:
  template:
    spec:
      {{- if .Values.schedulerName }}
      schedulerName: {{ .Values.schedulerName }}
      {{- end }}
      restartPolicy: Never
      containers:
        - name: batch-job
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          resources:
            limits:
              nvidia.com/gpu: {{ .Values.gpuCount | default 1 }}
      tolerations:
        - key: nvidia.com/gpu
          operator: Exists
          effect: NoSchedule
  backoffLimit: 3
```

### PersistentVolumeClaim (NFS-backed model storage)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {{ .Release.Name }}-model
spec:
  accessModes:
    - ReadWriteMany    # NFS supports RWX
  storageClassName: {{ .Values.persistence.storageClass | default "nfs-client" }}
  resources:
    requests:
      storage: {{ .Values.persistence.size | default "100Gi" }}
```

## Values File Structure (vLLM)

```yaml
# values.yaml (vLLM chart)
replicaCount: 1
image:
  repository: ghcr.io/thakicloud/vllm-openai
  tag: "dev-latest"
  pullPolicy: IfNotPresent

model:
  name: "meta-llama/Llama-3-8B"
  tensorParallelSize: 1
  gpuMemoryUtilization: "0.9"
  maxModelLen: 4096

schedulerName: kai-scheduler

keda:
  enabled: true
  host: "vllm.example.com"
  minReplicas: 1
  maxReplicas: 4
  targetRequestRate: 100

rollout:
  enabled: false
  strategy: canary

kueue:
  enabled: true
  priorityClass: "inference-high"

initContainer:
  enabled: true
  image: "ghcr.io/thakicloud/model-downloader:latest"
  modelPath: "/models"

s3ModelStreaming:
  enabled: false
  source: "s3://models/llama-3-8b/"

persistence:
  size: 100Gi
  storageClass: nfs-client

resources:
  limits:
    gpu: 1
    memory: 40Gi
  requests:
    gpu: 1
    memory: 32Gi
    cpu: "4"

shmSize: "16Gi"

service:
  port: 8000
  type: ClusterIP
```

## Decision Guide

| Workload Type | Template | Scheduler | Scaling |
|---------------|----------|-----------|---------|
| Go API service | container chart | default | KEDA HTTPScaledObject |
| LLM inference | vllm chart | kai-scheduler | KEDA or manual |
| Batch training | Job + Kueue | kai-scheduler | N/A |
| Model download | initContainer | default | N/A |
| Canary deploy | Argo Rollout | depends on workload | per strategy |

## Common Pitfalls

1. **Using HPA instead of KEDA** — The project standardizes on KEDA HTTPScaledObject. When `keda.enabled` is true, do NOT set `spec.replicas` in the Deployment.
2. **Missing `kai-scheduler`** — GPU workloads must use `schedulerName: kai-scheduler` for fair GPU sharing. Omitting it causes default scheduler to bin-pack GPUs poorly.
3. **Probe path is `/health`, not `/healthz` or `/readyz`** — vLLM and Go services both use `/health`. Getting this wrong causes CrashLoopBackOff.
4. **initContainer NFS lock race** — When multiple Pods start simultaneously on shared NFS, only one should download. The lock file pattern (`/.download.lock`) with hostname-based cache dirs prevents corruption.
5. **`readOnlyRootFilesystem: false` for vLLM** — vLLM needs write access to `/tmp` and HuggingFace cache dirs. Setting this to `true` breaks model loading.
6. **`securityContext` values** — vLLM uses `runAsUser: 1000`, `fsGroup: 2000`. Don't use the common `65534` (nobody) as it causes NFS permission errors.
7. **`/dev/shm` size** — Large models require large shared memory. Default `16Gi` for `shmSize`. Insufficient shm causes NCCL communication failures in tensor-parallel.
8. **S3 Model Streaming** — When `s3ModelStreaming.enabled`, vLLM uses `--load-format=runai_streamer` and the initContainer uses `runai-model-streamer` instead of `huggingface-cli`.
9. **`deletion-finalizer-timeout: "300"`** — ArgoCD Applications for vLLM need a 5-minute finalizer timeout due to model cleanup time.
10. **Startup probe for vLLM** — Model loading can take 5-10 minutes. Use `startupProbe` with `failureThreshold: 60` and `periodSeconds: 10` (10 minutes total).

## Constraints

- Do NOT use HPA — the project standardizes on KEDA HTTPScaledObject for autoscaling
- Do NOT set `spec.replicas` when `keda.enabled` is true — KEDA manages replica count
- Do NOT use `readOnlyRootFilesystem: true` for vLLM containers — model loading requires write access
- Do NOT change probe paths from `/health` — both Go services and vLLM use this path
- Do NOT omit `schedulerName: kai-scheduler` for GPU workloads
- Freedom level: **Low** — generated manifests deploy directly to production clusters

## Output Format

- **Helm template**: Complete `.yaml` file ready for `charts/{name}/templates/`
- **Values snippet**: Corresponding `values.yaml` entries with comments
- **Resource requirements**: Explicit CPU, memory, and GPU requests/limits
- **Security context**: Must include `runAsUser`, `fsGroup`, and `readOnlyRootFilesystem`

## Verification

After generating manifests, verify correctness:

### Check: Helm template renders
**Command:** `helm template <RELEASE> charts/<CHART> -f values.yaml`
**Expected:** Valid YAML output with no template errors

### Check: Schema validation
**Command:** `helm template <RELEASE> charts/<CHART> | kubeconform -strict -kubernetes-version 1.29.0`
**Expected:** All resources pass schema validation

### Check: KEDA configuration
**Command:** `helm template <RELEASE> charts/<CHART> --set keda.enabled=true | grep -c 'replicas:'`
**Expected:** 0 (no hardcoded replicas when KEDA is enabled)
