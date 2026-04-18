# Architecture Diagram Patterns Reference

Progressive-disclosure catalog for the architecture-diagram skill. Load this file only when selecting a visual style or layout pattern.

## Visual Styles

12 pre-defined accent color palettes. Each style sets accent colors for headers, borders, and highlights within the dark theme foundation (`#020617` background, `#0f172a` cards).

| # | Style | Accent | Header BG | Border | Use Case |
|---|---|---|---|---|---|
| 1 | Steel Blue | `#3b82f6` | `#1e3a5f` | `#2563eb` | General-purpose, corporate |
| 2 | Emerald | `#10b981` | `#064e3b` | `#059669` | Backend services, APIs |
| 3 | Violet | `#8b5cf6` | `#4c1d95` | `#7c3aed` | Data layer, ML pipelines |
| 4 | Amber | `#f59e0b` | `#78350f` | `#d97706` | Infrastructure, cloud |
| 5 | Rose | `#f43f5e` | `#881337` | `#e11d48` | Security, auth flows |
| 6 | Cyan | `#06b6d4` | `#083344` | `#0891b2` | Frontend, client apps |
| 7 | Orange | `#f97316` | `#7c2d12` | `#ea580c` | Event systems, messaging |
| 8 | Teal | `#14b8a6` | `#134e4a` | `#0d9488` | Monitoring, observability |
| 9 | Indigo | `#6366f1` | `#312e81` | `#4f46e5` | Platform services |
| 10 | Lime | `#84cc16` | `#365314` | `#65a30d` | CI/CD, automation |
| 11 | Pink | `#ec4899` | `#831843` | `#db2777` | User-facing, design |
| 12 | Slate Dark | `#64748b` | `#1e293b` | `#475569` | Minimal, documentation |

### Style Application

Apply a style by setting the accent color on the header bar and card title dots. The semantic component colors (cyan for frontend, emerald for backend, etc.) remain unchanged regardless of the chosen style.

```css
/* Example: Emerald style header */
.header h1 { color: #10b981; }
.card { border-color: #064e3b; }
.card-dot { background: #10b981; }
```

## Layout Patterns

12 spatial arrangements for positioning SVG components within the diagram canvas.

### 1. Three-Column

Three vertical lanes: left (frontend/clients), center (backend/services), right (data/storage). Best for standard web application stacks.

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Client  │  │ Service │  │   DB    │
│  Layer  │  │  Layer  │  │  Layer  │
└─────────┘  └─────────┘  └─────────┘
  x: 50-300   x: 400-700   x: 800-1050
```

SVG X ranges: left column 50-300, center 400-700, right 800-1050. Standard column width: 200px.

### 2. Pipeline (Left-to-Right)

Horizontal flow from source to sink. Best for ETL pipelines, CI/CD stages, request processing chains.

```
┌───────┐ → ┌───────┐ → ┌───────┐ → ┌───────┐
│ Ingest│   │Process│   │ Store │   │ Serve │
└───────┘   └───────┘   └───────┘   └───────┘
```

Equal spacing between stages. Arrow Y centered on component midpoint.

### 3. Hub-and-Spoke

Central service with radial connections to dependent components. Best for API gateways, message brokers, orchestrators.

```
           ┌───────┐
           │  Svc  │
           └───┬───┘
      ┌────────┼────────┐
  ┌───┴──┐ ┌──┴───┐ ┌──┴───┐
  │ Dep1 │ │ Dep2 │ │ Dep3 │
  └──────┘ └──────┘ └──────┘
```

Center hub at `(550, 200)`. Spokes distributed evenly on a circular arc below (radius ~200px).

### 4. Dashboard

Grid of equal-sized cards showing system status or component overview. 2x3 or 3x3 grid. Best for system health dashboards, service inventories.

```
┌──────┐ ┌──────┐ ┌──────┐
│  A   │ │  B   │ │  C   │
└──────┘ └──────┘ └──────┘
┌──────┐ ┌──────┐ ┌──────┐
│  D   │ │  E   │ │  F   │
└──────┘ └──────┘ └──────┘
```

Grid cell: 300x120px with 20px gap. Start at `(50, 60)`.

### 5. Nested Containers

Boundary boxes containing component groups (clusters, VPCs, namespaces). Best for K8s multi-cluster, cloud regions, security zones.

```
┌─ Cluster A ──────────────────┐
│ ┌──────┐ ┌──────┐ ┌──────┐  │
│ │ Pod1 │ │ Pod2 │ │ Pod3 │  │
│ └──────┘ └──────┘ └──────┘  │
└──────────────────────────────┘
```

Outer boundary: dashed stroke, `rx="12"`, 30px padding from inner components. Use amber for infra boundaries, rose for security boundaries.

### 6. Layered (Top-to-Bottom)

Horizontal layers stacked vertically: User -> Application -> Service -> Data -> Infrastructure. Best for enterprise architecture, N-tier systems.

```
┌────────────────────────────────┐  Layer 1: User
├────────────────────────────────┤  Layer 2: App
├────────────────────────────────┤  Layer 3: Service
├────────────────────────────────┤  Layer 4: Data
└────────────────────────────────┘  Layer 5: Infra
```

Each layer spans the full SVG width. Layer height: 100-140px. Vertical arrows between layers.

### 7. Swimlane

Vertical or horizontal lanes per team/domain/service boundary. Components placed within their lane. Best for cross-team workflows, domain-driven design.

```
│ Team A  │ Team B  │ Team C  │
│┌──────┐ │┌──────┐ │┌──────┐ │
││ Svc1 │ ││ Svc2 │ ││ Svc3 │ │
│└──┬───┘ │└──┬───┘ │└──────┘ │
│   └─────┼───┘     │         │
```

Lane width: `(viewBoxWidth - 60) / numLanes`. Lane separators: vertical lines, stroke `#1e293b`.

### 8. Ring / Circular

Components arranged in a circle with connections crossing the center. Best for mesh networks, peer-to-peer systems, microservice meshes.

Center: `(550, 350)`, radius 200px. Component angle: `360° / n` per component.

### 9. Hierarchical Tree

Top-down tree with parent-child relationships. Best for org charts, dependency trees, module hierarchies.

```
          ┌─────┐
          │Root │
        ┌─┴──┬──┴─┐
     ┌──┴─┐┌─┴──┐┌┴──┐
     │ A  ││ B  ││ C │
     └────┘└────┘└───┘
```

Level spacing: 120px vertical. Sibling spacing: 20px horizontal. Center-align children under parent.

### 10. Side Panel

Main diagram area (70% width) with a side panel (30% width) for metadata, legend, or auxiliary components. Best for detailed architecture with configuration panels.

```
┌──────────────────┐ ┌────────┐
│                  │ │ Config │
│   Main Diagram   │ │ Panel  │
│                  │ │        │
└──────────────────┘ └────────┘
```

Main area: x 30-740. Side panel: x 780-1070. Divider: vertical line at x=760.

### 11. Before/After Split

Two side-by-side diagrams comparing current vs target state. Best for migration plans, refactoring proposals.

```
┌─ Current ──────┐  ┌─ Target ───────┐
│                │  │                │
│   Diagram A    │  │   Diagram B    │
│                │  │                │
└────────────────┘  └────────────────┘
```

Left panel: x 30-530. Right panel: x 570-1070. Center divider with label.

### 12. Timeline / Sequence

Vertical or horizontal timeline with events and state changes. Best for deployment sequences, incident timelines, data flow stages.

```
  T1          T2          T3          T4
  │           │           │           │
  ▼           ▼           ▼           ▼
┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐
│Step1│   │Step2│   │Step3│   │Step4│
└─────┘   └─────┘   └─────┘   └─────┘
```

Timeline axis: horizontal line at y=40, full width. Event markers at equal intervals. Component boxes below axis.

## SVG Layout Examples

### Multi-Cluster K8s with GPU Scheduling

Recommended layout: **Nested Containers** (Pattern 5) with two boundary groups.

```
viewBox: 0 0 1100 800

Control Plane (amber boundary): x=30 y=30 w=500 h=350
  - API Server (emerald):  x=60  y=70  w=140 h=60
  - Scheduler (emerald):   x=220 y=70  w=140 h=60
  - ArgoCD (amber):        x=380 y=70  w=130 h=60
  - etcd (violet):         x=60  y=170 w=140 h=60
  - Keycloak (rose):       x=220 y=170 w=140 h=60
  - NATS (orange):         x=380 y=170 w=130 h=60

Worker Cluster (amber boundary): x=570 y=30 w=500 h=350
  - Kueue (amber):         x=600 y=70  w=140 h=60
  - vLLM (violet):         x=760 y=70  w=140 h=60
  - GPU Node (amber):      x=600 y=170 w=140 h=60
  - Fine-tune (violet):    x=760 y=170 w=140 h=60

Frontend (cyan): x=300 y=440 w=200 h=60
PostgreSQL (violet): x=60 y=440 w=160 h=60
Redis (violet): x=600 y=440 w=160 h=60

Arrows: Frontend -> API Server, API Server -> etcd, Scheduler -> Kueue, etc.
Legend: y=540 (below all boundaries)
```

### Microservice Pipeline

Recommended layout: **Pipeline** (Pattern 2) with message bus.

```
viewBox: 0 0 1100 500

Ingress (slate):    x=50  y=100 w=140 h=60
API GW (emerald):   x=250 y=100 w=140 h=60
Auth (rose):        x=450 y=100 w=140 h=60
Service (emerald):  x=650 y=100 w=140 h=60
DB (violet):        x=850 y=100 w=140 h=60

NATS bus (orange rect): x=50 y=210 w=940 h=20
  -> centered in gap between row 1 (y=160) and row 2 (y=270)

Worker 1 (emerald): x=250 y=270 w=140 h=60
Worker 2 (emerald): x=450 y=270 w=140 h=60
Cache (violet):     x=650 y=270 w=140 h=60

Arrows: horizontal between pipeline stages, vertical from bus to workers
Legend: y=400
```

### Hub-and-Spoke API Gateway

Recommended layout: **Hub-and-Spoke** (Pattern 3).

```
viewBox: 0 0 1100 700

API Gateway (emerald): x=450 y=100 w=200 h=70  (center hub)

Auth (rose):        x=100 y=300 w=160 h=60
User Svc (emerald): x=300 y=300 w=160 h=60
Order Svc (emerald):x=500 y=300 w=160 h=60
Payment (emerald):  x=700 y=300 w=160 h=60
Notify (orange):    x=900 y=300 w=160 h=60

DB cluster (violet boundary): x=200 y=440 w=700 h=120
  PostgreSQL:  x=230 y=470 w=140 h=60
  Redis:       x=430 y=470 w=140 h=60
  S3 (amber):  x=630 y=470 w=140 h=60

Arrows: Gateway -> each spoke service, each service -> DB cluster
Legend: y=620
```

## CSS Class Reference

These CSS classes are defined in `assets/template.html` and can be used when customizing the HTML wrapper around the SVG:

| Class | Purpose |
|---|---|
| `.header` | Top section with title and description |
| `.header h1` | Main diagram title (22px, white) |
| `.header p` | Subtitle text (12px, slate) |
| `.diagram-card` | Container for the SVG element |
| `.cards` | Three-column summary card grid |
| `.card` | Individual summary card |
| `.card-title` | Card header with pulsing dot |
| `.card-dot` | Animated status indicator dot |
| `.card-label` | Uppercase card section label |
| `.card-body` | Card content text |
| `.footer` | Bottom metadata bar |

## Sizing Guidelines

| Element | Recommended Size |
|---|---|
| Standard component box | 140 x 60 px |
| Wide component box | 200 x 60 px |
| Narrow component box | 120 x 60 px |
| Tall component box | 140 x 80 px |
| Minimum vertical gap | 40 px |
| Minimum horizontal gap | 20 px |
| Boundary padding (inner) | 30 px |
| Boundary corner radius | 12 px (cluster), 8 px (security) |
| Bus connector height | 20 px |
| Legend item spacing | 90 px horizontal |
| Default viewBox | 1100 x 700 |
| Extended viewBox (complex) | 1100 x 900 or 1100 x 1000 |
