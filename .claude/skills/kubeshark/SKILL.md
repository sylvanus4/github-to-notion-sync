---
name: kubeshark
description: >-
  Failure-mode-first Kubernetes diagnostic workflow. Prevents K8s
  misconfigurations by diagnosing 6 critical failure modes before manifest
  generation or during RCA. Use when "K8s 보안 점검", "매니페스트 리뷰",
  "K8s failure mode", "kubeshark", "쿠버네티스 진단", "K8s 설정 오류",
  "securityContext 누락", "리소스 설정 점검", "K8s best practice 검증",
  or any Kubernetes security/reliability diagnostic task.
  Do NOT use for manifest generation (use k8s-deployment-creator).
  Do NOT use for manifest CI validation (use k8s-manifest-validator).
  Do NOT use for GitOps/CI/CD patterns (use k8s-gitops-cicd).
  Do NOT use for Demo env RCA (use demo-rca-orchestrator).
---

# KubeShark: K8s Failure-Mode Diagnostic Workflow

LLM이 K8s 매니페스트에서 자주 놓치는 6가지 치명적 실패 모드를 체계적으로 진단하고 수정한다.
출처: [LukasNiessen/kubernetes-skill](https://github.com/LukasNiessen/kubernetes-skill) (MIT), ThakiCloud 환경에 적응.

## TKAI Platform Context

- Clusters: k0s-based (stage, dev, b200, demo, master, kata)
- GPU: NVIDIA A100, B200 (MIG support)
- Scheduler: `kai-scheduler` (GPU workloads)
- Autoscaling: KEDA HTTPScaledObject (not HPA)
- Progressive delivery: Argo Rollouts (canary/blue-green)
- Job scheduling: Kueue with priority-class labels
- Registry: `ghcr.io/thakicloud/`

## 7-Step Workflow

### Step 1: Capture Context

문서화 필수 항목 (매니페스트 작성/리뷰 전):

| Item | Example |
|------|---------|
| Cluster version | k0s v1.30 |
| Namespace | `project-{uuid}` |
| Workload type | Deployment / StatefulSet / Job / CronJob |
| Deployment method | Helm / Kustomize / raw YAML |
| Policy enforcement | PSS labels on namespace |
| GPU requirement | A100 / B200 / MIG partition |

### Step 2: Diagnose Failure Mode

6가지 failure mode 중 해당 항목 식별. 상세 체크리스트: `references/failure-modes.md`

| # | Mode | 핵심 증상 |
|---|------|----------|
| FM1 | Insecure workload defaults | securityContext 누락, root 실행, PSS 위반 |
| FM2 | Resource starvation | requests/limits 누락, PDB 없음, OOMKilled |
| FM3 | Network exposure | NetworkPolicy 없음, NodePort 노출 |
| FM4 | Privilege sprawl | 와일드카드 RBAC, default SA 사용 |
| FM5 | Fragile rollouts | probe 오설정, mutable tag, preStop 누락 |
| FM6 | API drift | deprecated apiVersion, 스키마 불일치 |

### Step 3: Load References Selectively

필요한 failure mode 참조만 로드 (Conditional Reference Retrieval):

```
Read references/failure-modes.md  (항상)
Read references/patterns.md      (생성/리팩토링 시)
Read references/validation.md    (검증 시)
```

### Step 4: Propose Fixes with Risk Controls

각 수정 제안에 포함할 항목:
- **Mechanism**: 왜 이 설정이 필요한지
- **Residual risk**: 수정 후에도 남는 위험
- **Validation command**: `kubectl`, `kubeconform`, `kube-linter`
- **Rollback procedure**: 되돌리기 방법

### Step 5: Generate Artifacts

매니페스트 생성은 `k8s-deployment-creator`에 위임. KubeShark는 생성된 결과에 다음을 보장:
- securityContext (runAsNonRoot, readOnlyRootFilesystem, drop ALL)
- Resource requests AND limits
- PodDisruptionBudget companion
- Immutable image tags (no `:latest`)

### Step 6: Validate Before Deploy

검증은 `k8s-manifest-validator`에 위임하거나 직접:

```bash
# Schema validation
kubeconform -strict -kubernetes-version 1.30.0 manifest.yaml

# Policy check
kube-linter lint manifest.yaml

# Dry-run
kubectl apply --dry-run=server -f manifest.yaml
```

### Step 7: Output Contract

모든 응답에 포함:
1. **Assumptions**: 클러스터/환경 가정
2. **Failure modes diagnosed**: 식별된 FM 번호
3. **Remediation + tradeoffs**: 수정 방안과 트레이드오프
4. **Validation plan**: 검증 명령어
5. **Rollback notes**: 롤백 절차

## Composition

| Need | Delegate To |
|------|-------------|
| Manifest generation | `k8s-deployment-creator` |
| CI/CD validation pipeline | `k8s-manifest-validator` |
| GitOps deployment | `k8s-gitops-cicd` |
| MSP incident investigation | `k8s-incident-investigator` |
| Demo env RCA | `demo-rca-orchestrator` |
