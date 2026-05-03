---
name: demo-rca-orchestrator
description: Unified RCA entry point for AI Platform Demo environment — routes to component-specific RCA skills based on error context.
disable-model-invocation: true
arguments: [error_context]
---

Diagnose errors in the AI Platform Demo environment.

## Routing Table

| Error Context | Routes To |
|---------------|-----------|
| Workload errors (CrashLoopBackOff, OOMKilled) | demo-workload-rca |
| Endpoint/Serverless errors | demo-serverless-rca |
| Pipeline Builder errors (KFP) | demo-pipeline-rca |
| Text Generation errors | demo-text-generation-rca |
| DevSpace errors | demo-devspace-rca |
| Tabular/ML Studio errors | demo-tabular-rca |
| Benchmark errors (lm-eval) | demo-benchmark-rca |
| Volume/Storage errors | demo-volume-rca |
| Unknown | Run broad diagnostics across all components |

## Diagnostic Steps

1. **Classify error**: Determine affected component from error context
2. **DB check**: Query ai_platform_db for resource status
3. **K8s inspection**: Check pod/deployment/job status via kubectl
4. **Log analysis**: Retrieve relevant pod logs
5. **Root cause**: Map findings to known failure patterns
6. **Resolution**: Propose fix with rollback plan

## Demo Environment Access

- Cluster context: demo
- DB: ai_platform_db (CNPG cluster in postgresql namespace)
- Namespace: varies by component

## Rules

- This is for Demo environment ONLY, not production
- Read-only diagnostics — do not modify resources without approval
- Always include git log/blame for commit attribution in RCA reports
