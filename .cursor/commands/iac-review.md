---
description: "Unified IaC review — auto-detect and validate Helm, Terraform, and Kubernetes manifests with parallel subagents"
---

## IaC Review

Unified Infrastructure-as-Code review that auto-detects IaC types and dispatches to specialized validators in parallel.

### Usage

```
/iac-review                                 # scan current project for all IaC
/iac-review <directory>                     # scan specific directory
/iac-review --pr                            # post findings as PR review comments
/iac-review --type helm,k8s                 # review only specific IaC types
```

### Execution

Read and follow the skill at `.cursor/skills/iac-review-agent/SKILL.md`.

User input: $ARGUMENTS

1. Scan for IaC files (Chart.yaml, *.tf, Deployment/Service YAML)
2. Dispatch to helm-validator, terraform-reviewer, k8s-manifest-validator in parallel
3. Aggregate results into unified report
4. Optionally post as PR review comments (with `--pr`)
