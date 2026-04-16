## Architecture Diagram Generator

Create professional dark-themed architecture diagrams as standalone HTML files with inline SVG.

### Usage

```
/architecture-diagram {description}                          # auto-select layout
/architecture-diagram {description} --layout pipeline        # force layout pattern
/architecture-diagram {description} --style emerald          # force visual style
/architecture-diagram {description} --layout nested --style amber   # combine flags
/architecture-diagram {description} --project-context        # use project domain terms
```

### Flags

| Flag | Effect |
|------|--------|
| `--layout {pattern}` | Force a specific layout pattern (three-column, pipeline, hub-spoke, dashboard, nested, layered, swimlane, ring, tree, side-panel, before-after, timeline) |
| `--style {name}` | Force a visual accent style (steel-blue, emerald, violet, amber, rose, cyan, orange, teal, indigo, lime, pink, slate-dark) |
| `--project-context` | Pre-populate with project domain terms (React 19, Go/Fiber, K8s, Keycloak, NATS, PostgreSQL) |
| `--viewbox {WxH}` | Override default SVG viewBox dimensions (default: 1100x700) |

### Workflow

1. **Parse input** — Extract system description and flags
2. **Identify components** — List all components with their semantic types (frontend, backend, database, infra, security, messaging, external)
3. **Map relationships** — Determine arrows and connections between components
4. **Select layout** — Choose from 12 layout patterns in `references/patterns.md` (or use `--layout` flag)
5. **Generate SVG** — Copy `assets/template.html`, customize with components following design system rules (arrow z-order masking, spacing discipline, legend placement)
6. **Save output** — Write standalone `.html` file
7. **Verify** — Confirm arrow order, spacing, legend position, and color palette

### Execution

Read and follow the `architecture-diagram` skill (`.cursor/skills/diagrams/architecture-diagram/SKILL.md`).

### Examples

Multi-cluster K8s architecture:
```
/architecture-diagram K8s 멀티클러스터 아키텍처 (컨트롤 플레인 + GPU 워커) --layout nested --project-context
```

Microservice pipeline:
```
/architecture-diagram API Gateway → Auth → Service → DB pipeline with NATS event bus --layout pipeline
```

General system overview:
```
/architecture-diagram 3-tier web application with React frontend, Go API, PostgreSQL, and Redis cache
```

Hub-and-spoke API gateway:
```
/architecture-diagram Central API gateway connecting 5 microservices with shared database cluster --layout hub-spoke
```

Before/after migration comparison:
```
/architecture-diagram Monolith to microservice migration plan --layout before-after
```
