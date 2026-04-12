---
name: architecture-diagram
description: Create layered architecture diagrams using HTML/CSS templates with color-coded layers and grid layouts. Supports 12 visual styles and 12 layout patterns including three-column, pipeline, dashboard, and nested containers. Best for visualizing system layers (User/Application/Data/Infrastructure), microservices architecture, and enterprise application design. Use when the user asks to "create architecture diagram", "draw system architecture", "visualize layers", "architecture overview", "system design diagram", "layered diagram", "microservice architecture", "아키텍처 다이어그램", "시스템 아키텍처", "레이어 다이어그램", or needs a visual representation of system components organized by architectural layers. Do NOT use for simple flowcharts (use flowchart skill). Do NOT use for data visualization charts (use infographic skill). Do NOT use for cloud provider deployment topology with service icons (use deployment-diagram skill). Do NOT use for UML class or sequence diagrams (use class-diagram or the appropriate UML skill). Do NOT use for Python diagrams-as-code PNG/SVG image generation (use diagrams-generator skill).
---

# Architecture Diagram Generator

**Quick Start:** Choose layout (single/two/three-column) -> Pick visual style -> Define layers with components -> Wrap as direct HTML in Markdown.

## Critical Rules

### Rule 1: Direct HTML Embedding
Write architecture diagrams as direct HTML in Markdown. **NEVER** use code blocks (` ```html `). The HTML must be embedded directly without fencing.

### Rule 2: No Empty Lines in HTML Structure
Do NOT add empty lines within the HTML architecture diagram structure. Keep the entire HTML block continuous to prevent parsing errors.

### Rule 3: Incremental Creation
Build diagrams step by step:
1. Create the overall framework (wrapper, sidebars, main) and define CSS styles
2. Add layer containers with titles
3. Fill in components layer by layer
4. Add details and highlights

### Rule 4: Flexible Layout Structure
Choose layout based on complexity:
- **Single Column**: Main content only (simple architectures)
- **Two Column**: Main + one sidebar (monitoring or security emphasis)
- **Three Column**: Full layout with both sidebars (complex systems)

### Rule 5: Layer-Based Organization
Each layer needs:
- Clear semantic meaning (User, Application, AI/Logic, Data, Infrastructure)
- Consistent color coding via CSS classes
- Grid-based layout for components (`.arch-grid-2` through `.arch-grid-6`)
- Appropriate nesting for sub-components

### Rule 6: Color Semantics
Use consistent semantic meaning for layers:
- **User Layer** (`.user`) -- interfaces and clients
- **Application Layer** (`.application`) -- business logic and APIs
- **AI/Logic Layer** (`.ai`) -- intelligence, rules, processing engines
- **Data Layer** (`.data`) -- databases, caches, storage
- **Infrastructure Layer** (`.infra`) -- containers, networking, DevOps
- **External Services** (`.external`) -- third-party APIs (dashed border)

## Visual Styles

Choose a style that matches the project tone:

| # | Style | Suitable For |
|---|---|---|
| 1 | Steel Blue | Consulting, banking, government, RFP proposals |
| 2 | Ember Warm | Retail, education, lifestyle brands |
| 3 | Neon Dark | Tech talks, gaming, cybersecurity dashboards |
| 4 | Stark Block | Creative studios, indie devs, tech blogs |
| 5 | Ocean Teal | Travel, logistics, green tech |
| 6 | Dusk Glow | Social media, entertainment, martech |
| 7 | Rose Bloom | Fashion, luxury, premium memberships |
| 8 | Sage Forest | Healthcare, agritech, clean energy |
| 9 | Frost Clean | Design tools, developer docs, API references |
| 10 | Indigo Deep | Enterprise white papers, internal platforms |
| 11 | Pastel Mix | SaaS products, startups, product docs |
| 12 | Slate Dark | Enterprise dark mode, developer dashboards |

## Layout Patterns

| # | Layout | Best For |
|---|---|---|
| 1 | Three-Column | Complex systems with monitoring + security sidebars |
| 2 | Single Stack | Simple services, microservice detail views |
| 3 | Left Sidebar | DevOps-centric views with operations emphasis |
| 4 | Right Sidebar | Governance-focused views with security emphasis |
| 5 | Pipeline | Data pipelines, CI/CD flows, ETL processes |
| 6 | Two-Column Split | Before/after comparisons, migration architecture |
| 7 | Dashboard | System overviews with KPIs, executive summaries |
| 8 | Grid Catalog | Service catalogs, equal-weight microservices |
| 9 | Banner + Center | Gateway-centric architectures |
| 10 | Nested Containers | Cloud deployments, VPC/network topology |
| 11 | Layer Layouts | Per-layer patterns: grid, sub-group, product group, KPI |
| 12 | Connectors | SVG overlay connectors between components |

## Common CSS Classes

- `.arch-wrapper` -- flex container for sidebar + main layout
- `.arch-sidebar` -- fixed-width sidebar column
- `.arch-main` -- flexible main content area
- `.arch-layer` -- layer container (add: `.user`, `.application`, `.ai`, `.data`, `.infra`, `.external`)
- `.arch-box` -- component box; `.arch-box.highlight` for key items; `.arch-box.tech` for smaller tech items
- `.arch-grid-2` through `.arch-grid-6` -- grid column layouts
- `.arch-sidebar-panel` -- sidebar panel container
- `.arch-sidebar-item` -- sidebar item; `.arch-sidebar-item.metric` for highlighted metrics

## Template: Three-Column Architecture

```html
<style scoped>
.arch-wrapper { display: flex; gap: 16px; font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-size: 13px; }
.arch-sidebar { width: 180px; flex-shrink: 0; display: flex; flex-direction: column; gap: 12px; }
.arch-main { flex: 1; display: flex; flex-direction: column; gap: 12px; }
.arch-layer { border-radius: 12px; padding: 14px; }
.arch-layer-title { font-weight: 700; font-size: 13px; margin-bottom: 10px; }
.arch-grid { display: grid; gap: 8px; }
.arch-grid-2 { grid-template-columns: repeat(2, 1fr); }
.arch-grid-3 { grid-template-columns: repeat(3, 1fr); }
.arch-grid-4 { grid-template-columns: repeat(4, 1fr); }
.arch-box { border-radius: 8px; padding: 10px; text-align: center; font-size: 12px; border: 1px solid rgba(0,0,0,0.08); }
.arch-box small { display: block; margin-top: 4px; opacity: 0.7; font-size: 10px; }
.arch-box.highlight { font-weight: 700; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.arch-sidebar-panel { border-radius: 10px; padding: 12px; }
.arch-sidebar-title { font-weight: 700; font-size: 11px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
.arch-sidebar-item { font-size: 11px; padding: 6px 8px; margin-bottom: 4px; border-radius: 6px; background: rgba(255,255,255,0.5); }
/* Semantic layer colors */
.arch-layer.user { background: #dbeafe; }
.arch-layer.application { background: #dcfce7; }
.arch-layer.ai { background: #fef3c7; }
.arch-layer.data { background: #fce7f3; }
.arch-layer.infra { background: #f3e8ff; }
.arch-layer.external { background: #f1f5f9; border: 2px dashed #94a3b8; }
</style>
<div class="arch-wrapper">
<div class="arch-sidebar">
  <div class="arch-sidebar-panel" style="background:#f0fdf4;">
    <div class="arch-sidebar-title">Monitoring</div>
    <div class="arch-sidebar-item">Prometheus</div>
    <div class="arch-sidebar-item">Grafana</div>
    <div class="arch-sidebar-item">Alertmanager</div>
  </div>
</div>
<div class="arch-main">
  <div class="arch-layer user">
    <div class="arch-layer-title">User Layer</div>
    <div class="arch-grid arch-grid-3">
      <div class="arch-box highlight">Web App<br><small>React</small></div>
      <div class="arch-box">Mobile App<br><small>React Native</small></div>
      <div class="arch-box">Admin Portal<br><small>Next.js</small></div>
    </div>
  </div>
  <div class="arch-layer application">
    <div class="arch-layer-title">Application Layer</div>
    <div class="arch-grid arch-grid-4">
      <div class="arch-box">API Gateway<br><small>Kong</small></div>
      <div class="arch-box">Auth Service<br><small>Keycloak</small></div>
      <div class="arch-box">Core Service<br><small>Go/Fiber</small></div>
      <div class="arch-box">Worker<br><small>NATS</small></div>
    </div>
  </div>
  <div class="arch-layer data">
    <div class="arch-layer-title">Data Layer</div>
    <div class="arch-grid arch-grid-3">
      <div class="arch-box highlight">PostgreSQL<br><small>Primary DB</small></div>
      <div class="arch-box">Redis<br><small>Cache</small></div>
      <div class="arch-box">S3<br><small>Object Storage</small></div>
    </div>
  </div>
  <div class="arch-layer infra">
    <div class="arch-layer-title">Infrastructure Layer</div>
    <div class="arch-grid arch-grid-3">
      <div class="arch-box">Kubernetes<br><small>Orchestration</small></div>
      <div class="arch-box">ArgoCD<br><small>GitOps</small></div>
      <div class="arch-box">Helm<br><small>Packaging</small></div>
    </div>
  </div>
</div>
<div class="arch-sidebar">
  <div class="arch-sidebar-panel" style="background:#fef2f2;">
    <div class="arch-sidebar-title">Security</div>
    <div class="arch-sidebar-item">mTLS</div>
    <div class="arch-sidebar-item">RBAC</div>
    <div class="arch-sidebar-item">Vault</div>
  </div>
</div>
</div>
```

## Advanced Features

### Product Groups
```html
<div class="arch-product-group">
  <div class="arch-product">
    <div class="arch-product-title">Product A</div>
    <div class="arch-grid arch-grid-2">
      <div class="arch-box">Feature 1</div>
      <div class="arch-box highlight">Feature 2</div>
    </div>
  </div>
</div>
```

### SVG Connectors
Use an SVG overlay as the last child of a `position: relative` container. Always use `<path>` with `M`/`L` for strictly horizontal and vertical segments.

```html
<svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; overflow: visible;">
  <defs>
    <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6" fill="none" stroke="#94a3b8" stroke-width="1"/>
    </marker>
  </defs>
  <path d="M 200,72 L 200,90 L 400,90 L 400,108" class="arch-conn" marker-end="url(#arrowhead)"/>
</svg>
```

## Best Practices

1. **Direct embedding only** -- never use ` ```html ` code blocks
2. **No empty lines** -- keep the entire HTML block continuous
3. **Incremental development** -- framework first, then layers, then components
4. **Highlight key components** -- use `.highlight` for critical items
5. **Add tech details** -- include stack info in `<small>` tags
6. **Balance density** -- avoid overcrowding components with text
7. **Maintain color semantics** -- stick to established layer meanings
