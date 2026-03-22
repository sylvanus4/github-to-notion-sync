---
description: "Validate Kubernetes manifests with kubeconform schema check, KubeLinter best practices, and dry-run verification"
---

## K8s Validate

Validate Kubernetes manifests through a 3-stage pipeline: schema validation → linting → dry-run.

### Usage

```
/k8s-validate <manifest-path>               # validate specific manifests
/k8s-validate deploy/k8s/                   # validate all YAML in directory
/k8s-validate --skip-dry-run                # skip kubectl dry-run (no cluster needed)
/k8s-validate --k8s-version 1.29            # target specific K8s version
```

### Execution

Read and follow the skill at `.cursor/skills/k8s-manifest-validator/SKILL.md`.

User input: $ARGUMENTS

1. Parse the manifest path from arguments (default: scan for `*.yaml`/`*.yml` files)
2. Run the 3-stage pipeline per the skill workflow
3. Present the consolidated report with pass/fail per stage
