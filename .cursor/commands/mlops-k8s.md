---
description: "MLOps K8s cluster access, GPU/MIG pod deployment, GHCR image management, and resource availability checks"
---

## MLOps K8s Access

Manage TKAI Kubernetes cluster access, deploy GPU/MIG workloads, provision NFS storage, and handle GHCR container image workflows across 6 clusters.

### Usage

```
/mlops-k8s switch <cluster>           # switch to a TKAI cluster context (stage, dev, b200, demo, master, kata)
/mlops-k8s deploy-gpu                 # generate and apply a GPU pod spec
/mlops-k8s deploy-mig                 # generate and apply a MIG pod spec
/mlops-k8s create-pvc <name>          # create a PVC with NFS StorageClass
/mlops-k8s check-resources            # check GPU/MIG availability across nodes
/mlops-k8s ghcr-push <image>          # build and push an image to GHCR
/mlops-k8s ghcr-secret <namespace>    # create imagePullSecret for GHCR
/mlops-k8s generate-yaml              # interactive full pod YAML generator
/mlops-k8s                            # interactive mode (asks what you need)
```

### Execution

Read and follow the skill at `.cursor/skills/infra/mlops-k8s-access/SKILL.md`.

User input: $ARGUMENTS

1. Parse the subcommand and arguments
2. If no subcommand, run Step 0 (AskQuestion) from the skill to determine intent
3. Route to the matching workflow mode (Mode 1–8) in the skill
4. Execute the steps, generating YAML templates and running kubectl/docker commands
5. Verify the result (cluster connectivity, pod status, secret existence, image push success)
