---
description: "Validate Helm charts with lint, template render, kubeconform schema check, and kube-score best practices"
---

## Helm Validate

Validate Helm charts through a 4-stage pipeline: lint → template render → schema validation → best-practice scoring.

### Usage

```
/helm-validate <chart-path>            # validate a specific chart
/helm-validate deploy/helm/            # validate all charts in directory
/helm-validate --values prod.yaml      # validate with specific values file
```

### Execution

Read and follow the skill at `.cursor/skills/helm-validator/SKILL.md`.

User input: $ARGUMENTS

1. Parse the chart path from arguments (default: scan for `Chart.yaml` files)
2. Run the 4-stage pipeline per the skill workflow
3. Present the consolidated report with pass/fail per stage
