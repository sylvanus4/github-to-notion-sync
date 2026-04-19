---
name: kube-cluster-switch
description: >-
  Automate Kubernetes multi-cluster kubeconfig management for ThakiCloud infrastructure.
  Use when the user asks to "switch cluster", "merge kubeconfig", "add new cluster",
  "kube switch", "kube-cluster-switch", "kubecm merge", "클러스터 전환",
  "kubeconfig 병합", "K8s 클러스터", "새 클러스터 추가", or needs to manage
  kubectl contexts across dev, stage, b200, demo, master, and kata clusters.
  Do NOT use for Helm chart validation (use helm-validator).
  Do NOT use for K8s manifest validation (use k8s-manifest-validator).
  Do NOT use for infrastructure drift detection (use infra-drift-detector).
  Do NOT use for CI/CD pipeline review (use sre-devops-expert).
  Do NOT use for kubectl command execution beyond context switching.
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "infra"
  platforms: [darwin]
---

# Kube Cluster Switch

## Constraints

- **Freedom level: Low** — kubeconfig mutations affect cluster access; follow exact step sequences
- Do NOT modify kubeconfig files manually — always use `kubecm` commands
- Always backup `~/.kube/config` before any merge or re-merge operation
- Do NOT execute `kubectl` workload commands (apply, delete, scale) — this skill is context-switching only
- VPN connection is required for all ThakiCloud clusters

## Tools

| Tool     | Install                    | Purpose                    |
|----------|----------------------------|----------------------------|
| kubectl  | `brew install kubectl`     | K8s CLI                    |
| kubecm   | `brew install kubecm`      | Kubeconfig merge/manage    |
| kubectx  | `brew install kubectx`     | Context & namespace switch |

Verify: `kubectl version --client && kubecm version && kubectx --help`

## Cluster Registry

| Alias       | Context Name  | Server                                    | Notes           |
|-------------|---------------|--------------------------------------------|-----------------|
| `kdev`      | tkai-dev      | https://tkai.build-kube.thakicloud.site:6443 | Development     |
| `kstage`    | tkai-stage    | https://10.7.60.153:6443                   | Staging / OKS   |
| `kb200`     | tkai-b200     | https://10.7.60.214:6443                   | B200 GPU        |
| `kdemo`     | tkai-demo     | https://10.7.80.20:6443                    | Demo            |
| `kmaster`   | tkai-master   | https://10.7.81.20:6443                    | Master / Prod   |
| `kkata`     | tkai-kata     | https://10.7.60.20:6443                    | Kata Containers |

Config files stored at `~/.kube/tkai-{name}.config`.

## Workflow Modes

### Mode 1: Status Check

```bash
kubecm list          # show all contexts with current selection
kubectx              # list context names only
kubectx -c           # show current context
kubens               # list namespaces in current context
```

### Mode 2: Switch Context

```bash
kubectx tkai-dev     # switch to dev cluster
kubens thaki-system  # switch namespace within current context
```

Shell aliases (defined in `~/.zshrc`):

| Alias      | Command                        | Effect                         |
|------------|--------------------------------|--------------------------------|
| `kdev`     | `kubectx tkai-dev`             | Switch active context to dev   |
| `kstage`   | `kubectx tkai-stage`           | Switch to staging              |
| `kb200`    | `kubectx tkai-b200`            | Switch to B200 GPU             |
| `kdemo`    | `kubectx tkai-demo`            | Switch to demo                 |
| `kmaster`  | `kubectx tkai-master`          | Switch to master               |
| `kkata`    | `kubectx tkai-kata`            | Switch to kata                 |
| `kc-dev`   | `kubectl --context=tkai-dev`   | Run kubectl without switching  |
| `kc-stage` | `kubectl --context=tkai-stage` | Run kubectl without switching  |
| `kx`       | `kubectx`                      | Short for kubectx              |
| `kns`      | `kubens`                       | Short for kubens               |
| `kls`      | `kubecm list`                  | Short for kubecm list          |

### Mode 3: Add New Cluster

1. Place the new kubeconfig file in `~/.kube/`:
   ```bash
   cp /path/to/new-cluster.config ~/.kube/
   ```

2. Backup current merged config:
   ```bash
   cp ~/.kube/config ~/.kube/config.backup.$(date +%Y%m%d)
   ```

3. Merge with kubecm:
   ```bash
   kubecm add -f ~/.kube/new-cluster.config --context-name <desired-name> --cover
   ```

4. If kubecm generates a composite name, rename it:
   ```bash
   kubecm rename "<generated-name>" "<desired-name>" -s
   ```

5. Verify:
   ```bash
   kubecm list
   kubectx <desired-name>
   kubectl get nodes
   ```

6. Add alias to `~/.zshrc`:
   ```bash
   alias k<short>="kubectx <desired-name>"
   alias kc-<short>="kubectl --context=<desired-name>"
   ```

7. Update the Cluster Registry table in this skill.

### Mode 4: Remove Cluster

```bash
kubecm delete <context-name>
kubecm list   # verify removal
```

Then remove the corresponding alias from `~/.zshrc`.

### Mode 5: Re-merge All

When kubeconfig files are updated (e.g., certificate rotation):

```bash
cp ~/.kube/config ~/.kube/config.backup.$(date +%Y%m%d)
rm ~/.kube/config

for f in ~/.kube/tkai-*.config; do
  name=$(basename "$f" .config)
  kubecm add -f "$f" --context-name "$name" --cover
done

kubecm list
```

Rename any composite context names as needed with `kubecm rename`.

## Verification Checklist

- [ ] `kubecm list` shows all 6 contexts with clean names
- [ ] `kubectx tkai-dev && kubectl get nodes` succeeds
- [ ] `kubectx tkai-stage && kubectl get nodes` succeeds
- [ ] Shell aliases (`kdev`, `kstage`, etc.) work after `source ~/.zshrc`
- [ ] `kubecm completion zsh` loads without errors

## Output Format

- Status reports: text table via `kubecm list`
- Context switch confirmation: single line showing the new active context
- Verification: checklist items with PASS/FAIL per cluster

## Troubleshooting

| Symptom                           | Fix                                                    |
|-----------------------------------|--------------------------------------------------------|
| `kubecm add` creates long names   | Use `kubecm rename "<old>" "<new>" -s` after merge     |
| Certificate expired               | Re-download kubeconfig and re-merge (Mode 5)           |
| Context not found                 | Check `kubecm list`; file may not have been merged     |
| Alias not working                 | Run `source ~/.zshrc` or open a new terminal           |
| Permission denied on cluster      | Verify VPN connection and kubeconfig credentials       |

## File Layout

```
~/.kube/
├── config                  # kubecm-merged master config
├── config.backup.YYYYMMDD  # backup before last merge
├── tkai-dev.config
├── tkai-stage.config
├── tkai-b200.config
├── tkai-demo.config
├── tkai-master.config
└── tkai-kata.config
```
