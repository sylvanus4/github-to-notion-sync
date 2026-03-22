---
description: "Detect infrastructure drift by comparing live cluster state against declared IaC — Helm releases, K8s resources, ConfigMaps"
---

## Infra Drift

Compare live infrastructure state against declared IaC to detect configuration drift.

### Usage

```
/infra-drift                                # check all namespaces
/infra-drift --namespace production         # check specific namespace
/infra-drift --context staging-cluster      # use specific kubeconfig context
/infra-drift --iac-path deploy/k8s/         # specify IaC source directory
```

### Execution

Read and follow the skill at `.cursor/skills/infra-drift-detector/SKILL.md`.

User input: $ARGUMENTS

1. Snapshot live cluster state (deployments, services, configmaps, secrets, HPA)
2. Load declared IaC from source directory
3. Diff live vs declared for each resource
4. Classify drift by severity (Critical / Warning / Info)
5. Generate drift report with remediation commands
