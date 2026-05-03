---
name: argocd-expert
description: ArgoCD Application management — sync, rollback, RBAC, health checks, secret management, and InitSetup state machine operations.
disable-model-invocation: true
---

Manage ArgoCD operations for the TKAI multi-cluster platform.

## Capabilities

1. **Application CRUD**: Create, update, delete ArgoCD Applications via K8s API or CLI
2. **Sync Operations**: Manual sync, auto-sync policies, sync waves, sync windows
3. **Rollback**: Rollback to previous revision with health verification
4. **RBAC**: AppProject-scoped RBAC configuration
5. **Secret Management**: sealed-secrets or external-secrets integration
6. **Health Assessment**: Application health, sync status, resource status
7. **InitSetup State Machine**: Manage cluster initialization states

## Project Context

- Charts at `ai-platform/backend/go/charts/`
- Go package at `ai-platform/tkai-multi-cluster/clustermanager/argocd/`
- Image tags: `dev-{TIMESTAMP}`, `rc-{TIMESTAMP}`, `vYYYY.MM.DD`

## Common Commands

```bash
argocd app sync <app-name>
argocd app get <app-name>
argocd app rollback <app-name> <revision>
argocd app diff <app-name>
```

## Rules

- Always check health status after sync operations
- Use server-side apply for Application resources
- Verify sync status before rollback
