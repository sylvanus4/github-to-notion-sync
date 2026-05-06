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
| K8s generic failure (securityContext, resource limits, probe, RBAC, API drift) | kubeshark |

## K8s Failure Mode Escalation

플랫폼 컴포넌트별 RCA에서 근본 원인이 K8s 설정 오류(securityContext 누락, resource 미설정, probe 오설정, RBAC 과권한, deprecated API 등)로 식별되면 `kubeshark` 스킬의 6가지 failure mode 분류 체계를 참조하여 deep dive한다.

| FM# | Mode | 해당 상황 |
|-----|------|----------|
| FM1 | Insecure workload defaults | Pod가 root로 실행, PSS 위반으로 차단 |
| FM2 | Resource starvation | OOMKilled, CPU throttling, 스케줄링 실패 |
| FM3 | Network exposure | Pod 간 통신 불가, DNS 해석 실패 |
| FM4 | Privilege sprawl | ServiceAccount 권한 부족/과다 |
| FM5 | Fragile rollouts | Probe 오설정으로 cascading restart, 배포 실패 |
| FM6 | API drift | deprecated API로 매니페스트 적용 실패 |

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
