---
name: diagrams-generator
description: >-
  Generate professional cloud architecture diagrams as code using Python's
  diagrams library (mingrammer/diagrams). Produces PNG/SVG output from Python
  scripts with Graphviz rendering. Use when the user asks to "create
  architecture diagram", "generate infrastructure diagram", "draw system
  diagram", "diagram as code", "diagrams-generator", "cloud architecture
  diagram", "K8s architecture diagram", "Kubernetes diagram", "network
  topology diagram", "system architecture visualization", "generate PNG
  diagram from code", "아키텍처 다이어그램", "인프라 다이어그램", "시스템 다이어그램", "클라우드 아키텍처 그림",
  "컴포넌트 다이어그램", "네트워크 토폴로지", "인프라 시각화", "다이어그램 코드로 그려줘", "아키텍처 그림 만들어줘", "GPU
  아키텍처 다이어그램", or wants programmatic cloud/K8s/on-prem/GPU infrastructure
  diagrams rendered to image files. Do NOT use for Mermaid diagrams in
  markdown (use visual-explainer). Do NOT use for Figma design work (use
  figma-to-tds). Do NOT use for Draw.io XML diagrams (use
  alphaear-logic-visualizer). Do NOT use for interactive HTML visual pages
  (use md-to-visual-explainer). Do NOT use for slide deck creation (use
  anthropic-pptx or nlm-slides). Korean triggers: "아키텍처 다이어그램", "인프라 다이어그램",
  "시스템 다이어그램", "컴포넌트 다이어그램", "클라우드 아키텍처", "다이어그램 코드", "인프라 시각화".
disable-model-invocation: true
---

# Diagrams Generator

Generate professional cloud architecture diagrams using Python's `diagrams` library (mingrammer/diagrams). Produces high-quality PNG/SVG outputs from Python scripts with Graphviz rendering.

## Prerequisites

- Python 3.8+
- Graphviz (`brew install graphviz` on macOS)
- diagrams library (`pip3 install --break-system-packages diagrams`)

### Verify Prerequisites

```bash
dot -V && python3 -c "from diagrams import Diagram; print('OK')"
```

If either fails, install the missing dependency before proceeding.

## Workflow

### 1. Understand the Architecture

Before writing code, identify:

- **Layers**: What logical layers exist? (e.g., Client, Application, Data, Infrastructure)
- **Components**: What services/tools/systems are in each layer?
- **Connections**: How do components communicate? (sync, async, data flow)
- **Grouping**: Which components belong together as clusters?

### 2. Map Components to Icons

Use the diagrams library's built-in providers. Priority order for icon selection:

| Priority | Provider | Use When |
|---|---|---|
| 1 | `diagrams.k8s.*` | Kubernetes-native components (Pods, Deployments, Services, etc.) |
| 2 | `diagrams.onprem.*` | On-premises/self-hosted tools (PostgreSQL, Redis, Traefik, NATS, etc.) |
| 3 | `diagrams.aws.*` / `diagrams.gcp.*` / `diagrams.azure.*` | Cloud-provider-specific services |
| 4 | `diagrams.programming.*` | Language/framework-specific (React, Go, Python) |
| 5 | `diagrams.generic.*` | Generic icons when no specific match exists |
| 6 | `diagrams.custom.Custom()` | Custom SVG icons for unique components |

### Key Module Reference

```
diagrams.k8s.compute    → Deploy, Pod, Job, STS, RS, CronJob
diagrams.k8s.network    → Ingress, SVC, NetworkPolicy
diagrams.k8s.storage    → PV, PVC, SC
diagrams.k8s.infra      → Node, Master
diagrams.k8s.rbac       → ClusterRole, ClusterRoleBinding, Role
diagrams.k8s.controlplane → APIServer, Scheduler, ControllerManager

diagrams.onprem.database  → PostgreSQL, MySQL, MongoDB, Cassandra
diagrams.onprem.inmemory  → Redis, Memcached
diagrams.onprem.queue     → Nats, Kafka, RabbitMQ
diagrams.onprem.network   → Traefik, Nginx, HAProxy
diagrams.onprem.monitoring → Grafana, Prometheus, Datadog
diagrams.onprem.container  → Docker, Firecracker
diagrams.onprem.workflow   → Kubeflow, Airflow
diagrams.onprem.cd         → Spinnaker, ArgoCD
diagrams.onprem.vcs        → Github, Gitlab
diagrams.onprem.client     → User, Users
diagrams.onprem.security   → Vault

diagrams.programming.framework → React, Vue, Angular, Spring, Django, Flask
diagrams.programming.language  → Go, Python, Java, Rust, TypeScript

diagrams.generic.compute  → Rack
diagrams.generic.storage  → Storage
diagrams.generic.network  → Firewall, Switch, Router
```

### 3. Write the Diagram Script

Follow this template structure:

```python
"""
[Title] — [Subtitle]
[Brief description]
"""
from diagrams import Diagram, Cluster, Edge
# Import specific icons

OUTPUT = "output/path/to/diagram_name"

graph_attr = {
    "fontsize": "26",
    "fontname": "Helvetica Neue",
    "bgcolor": "#FAFBFC",
    "pad": "1.0",
    "splines": "spline",
    "nodesep": "1.0",
    "ranksep": "1.2",
}

with Diagram(
    "Title\nSubtitle",
    show=False,
    filename=OUTPUT,
    direction="TB",  # TB, LR, BT, RL
    graph_attr=graph_attr,
    outformat="png",
):
    # Define nodes, clusters, and edges
    pass
```

### 4. Styling Best Practices

#### Cluster Colors (layer-based palette)

| Layer | Background | Border Style |
|---|---|---|
| Client / Entry | `#E8F5E9` (light green) | rounded |
| Agent / Orchestration | `#E3F2FD` (light blue) | rounded, penwidth=2 |
| Platform / PaaS | `#FFF3E0` (light orange) | rounded |
| Infrastructure / IaaS | `#F3E5F5` (light purple) | rounded |
| Data / Storage | `#ECEFF1` (light gray) | rounded |
| Security / Auth | `#FFF9C4` (light yellow) | rounded |
| Observability | `#E0F2F1` (light teal) | rounded |

#### Edge Styling

```python
Edge(label="① Request", color="#2E7D32", style="bold")     # green for client flow
Edge(label="② Orchestrate", color="#1565C0", style="bold")  # blue for orchestration
Edge(label="③ Execute", color="#E65100", style="bold")      # orange for platform
Edge(label="④ GPU Compute", color="#6A1B9A", style="bold")  # purple for infra
Edge(color="#F9A825")                                        # yellow for auth
Edge(color="#00695C", style="dashed")                        # teal for monitoring
Edge(color="#666", style="dashed")                           # gray for data/storage
```

#### Direction Selection

- `TB` (Top-to-Bottom): Hierarchical layer views, stack diagrams
- `LR` (Left-to-Right): Process flows, data pipelines, deployment comparisons
- `BT` / `RL`: Rarely used, only for specific visual requirements

### 5. Multi-Version Strategy

For comprehensive architecture documentation, generate these standard versions:

| Version | Focus | Direction | Purpose |
|---|---|---|---|
| v1 | High-Level Architecture | TB | 4-layer overview, executive summary |
| v2 | Component Deep Dive (per layer) | TB | Detailed internals of one layer |
| v3 | Platform Services | TB | PaaS capabilities and workloads |
| v4 | Infrastructure Stack | TB | IaaS, GPU pools, storage, networking |
| v5 | Deployment Models | LR | Side-by-side deployment options |
| v6 | Data / Request Flow | LR | End-to-end request lifecycle |

### 6. Execute and Verify

```bash
python3 output/presentations/diagrams/v1_example.py
ls -la output/presentations/diagrams/*.png
open output/presentations/diagrams/v1_example.png  # macOS preview
```

### 7. Troubleshooting

| Error | Fix |
|---|---|
| `graphviz not found` | `brew install graphviz` |
| `No module named 'diagrams'` | `pip3 install --break-system-packages diagrams` |
| `cannot import name 'X' from 'diagrams.Y'` | Check the correct submodule — run `python3 -c "import diagrams.Y; print(dir(diagrams.Y))"` |
| Diagram too cluttered | Increase `nodesep` and `ranksep` in `graph_attr` |
| Labels overlapping | Use shorter labels or increase `pad` |

## Constraints

- NEVER use `show=True` — always `show=False` for headless generation
- ALWAYS set `filename=OUTPUT` with a clear output path
- ALWAYS use `outformat="png"` (or `"svg"` for vector output)
- Use `Rack` from `diagrams.generic.compute` as a fallback for components without specific icons
- Keep node labels concise: 2-3 lines max with `\n` line breaks
- For components not in the library, use `Custom()` with a local SVG icon file

## Custom Icon Pattern

When a component has no built-in icon (e.g., vLLM, Kueue, Slinky), use `Custom()` with a local SVG:

```python
from diagrams.custom import Custom

vllm = Custom("vLLM\nInference", "./icons/vllm.svg")
kueue = Custom("Kueue\nGPU Scheduler", "./icons/kueue.svg")
```

If no SVG is available, fall back to `Rack` from `diagrams.generic.compute` with a descriptive label.

## Batch Execution

Generate all versions at once:

```bash
for f in output/presentations/diagrams/v*.py; do python3 "$f"; done
ls -la output/presentations/diagrams/*.png
```

## Reference Implementation

See `output/presentations/diagrams/v1_high_level_architecture.py` through `v6_data_flow.py` for a complete 6-version ThakiCloud AI Platform architecture diagram set.
