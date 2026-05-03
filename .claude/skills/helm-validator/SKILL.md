---
name: helm-validator
description: Validate Helm charts using helm lint, template rendering, kubeconform schema validation, and kube-score/Polaris policy checks.
disable-model-invocation: true
arguments: [chart_path]
---

Validate Helm chart at `$chart_path`.

## Validation Pipeline

1. **helm lint**: Syntax and structure validation
2. **helm template**: Render templates with default values, check for rendering errors
3. **kubeconform**: Validate rendered manifests against K8s JSON schemas
4. **kube-score / Polaris**: Policy checks (security, best practices, reliability)

## Output

```markdown
## Helm Validation Report: [chart_path]

### helm lint: [PASS/FAIL]
[Details]

### helm template: [PASS/FAIL]
[Rendering errors if any]

### kubeconform: [PASS/FAIL]
[Schema violations]

### Policy Checks: [PASS/FAIL]
[Security and best-practice findings]

## Overall: [PASS/FAIL]
[Fix suggestions for failures]
```

## Rules

- Run all 4 checks regardless of individual failures
- Report specific line numbers and fix suggestions
- Check for deprecated API versions
