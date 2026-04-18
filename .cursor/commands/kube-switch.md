---
description: "Switch K8s clusters, merge kubeconfigs, or manage cluster contexts via kube-cluster-switch skill"
---

# /kube-switch

Manage Kubernetes multi-cluster contexts for ThakiCloud infrastructure.

## Usage

```
/kube-switch                     # show current context and all available clusters
/kube-switch <cluster>           # switch to a cluster (dev, stage, b200, demo, master, kata)
/kube-switch add <config-path>   # merge a new kubeconfig file
/kube-switch remove <context>    # remove a cluster context
/kube-switch remerge             # re-merge all ~/.kube/tkai-*.config files
/kube-switch verify              # run verification checklist
```

## Skill

Read and follow `.cursor/skills/infra/kube-cluster-switch/SKILL.md`.
