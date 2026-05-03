---
name: infographic
description: >-
  Create data-rich infographic visualizations using a simple YAML-like syntax
  with pre-designed templates. Supports KPI cards, timelines, roadmaps,
  step-by-step processes, A vs B comparisons, SWOT analysis, funnels, org
  trees, pie charts, bar charts, and more. Use when the user asks to "create
  infographic", "KPI dashboard", "timeline infographic", "roadmap
  visualization", "comparison chart", "SWOT diagram", "funnel chart", "process
  infographic", "인포그래픽", "KPI 카드", "타임라인", "로드맵", "비교 차트", "SWOT", "퍼널 차트",
  "프로세스 인포그래픽", or needs visual data presentations beyond standard diagrams.
  Do NOT use for technical architecture (use architecture-diagram skill). Do
  NOT use for code structure (use class-diagram skill). Do NOT use for process
  flows with decision logic (use flowchart skill). Do NOT use for cloud
  deployment topology (use deployment-diagram skill). Do NOT use for BPMN
  workflows (use workflow-diagram skill).
---

# Infographic Generator

**Quick Start:** Choose template -> Define data items -> Set theme -> Output inside ` ```infographic ` code fence.

## Critical Rules

### Rule 1: Infographic Code Fence
Always output inside ` ```infographic ` fenced code blocks. The syntax is a simple YAML-like format.

### Rule 2: Basic Structure
```
infographic <template-name>
data
  <field>: <value>
  items
    - <field>: <value>
      <field>: <value>
    - <field>: <value>
theme: <theme-name>
```

### Rule 3: Template Selection
Choose the template that best fits the data type:

| Template | Best For |
|---|---|
| `kpi-cards` | Metrics dashboards, key numbers |
| `timeline` | Historical events, project milestones |
| `roadmap` | Product roadmap, feature planning |
| `steps` | Process guides, how-to instructions |
| `comparison` | A vs B product/feature comparison |
| `swot` | Strategic analysis |
| `funnel` | Sales/conversion pipeline |
| `org-tree` | Organization charts, hierarchies |
| `pie-chart` | Distribution, market share |
| `bar-chart` | Categorical comparisons, rankings |
| `number-counter` | Single highlighted metrics |
| `checklist` | Task lists, feature lists |
| `quote-cards` | Testimonials, key quotes |
| `feature-grid` | Feature matrices |
| `stat-cards` | Statistics with descriptions |

### Rule 4: Themes
Available themes: `modern`, `corporate`, `playful`, `dark`, `minimal`, `nature`, `tech`, `warm`, `ocean`, `sunset`

### Rule 5: Icon Resources
- **iconify**: Use icon names like `mdi:chart-bar`, `fa:users`, `carbon:analytics`
- **unDraw**: Use illustration names for larger visuals

## Template: KPI Cards

```infographic
infographic kpi-cards
data
  title: Q4 2024 Performance
  subtitle: Key Business Metrics
  items
    - label: Monthly Revenue
      value: $2.4M
      change: +18%
      trend: up
      icon: mdi:currency-usd
    - label: Active Users
      value: 45,200
      change: +12%
      trend: up
      icon: mdi:account-group
    - label: Churn Rate
      value: 2.1%
      change: -0.5%
      trend: down
      icon: mdi:account-remove
    - label: NPS Score
      value: 72
      change: +8
      trend: up
      icon: mdi:star
    - label: Avg Response Time
      value: 1.2s
      change: -30%
      trend: down
      icon: mdi:speedometer
    - label: Uptime
      value: 99.97%
      change: +0.02%
      trend: up
      icon: mdi:server
theme: modern
```

## Template: Timeline

```infographic
infographic timeline
data
  title: Product Evolution
  items
    - date: 2023 Q1
      title: Alpha Launch
      description: Internal testing with 50 users
      icon: mdi:rocket-launch
      color: blue
    - date: 2023 Q3
      title: Public Beta
      description: Open beta with 1,000 users
      icon: mdi:beta
      color: green
    - date: 2024 Q1
      title: GA Release
      description: General availability with enterprise features
      icon: mdi:check-decagram
      color: purple
    - date: 2024 Q3
      title: Series A
      description: Raised $15M for expansion
      icon: mdi:cash-multiple
      color: orange
    - date: 2025 Q1
      title: Global Expansion
      description: Launched in 12 new markets
      icon: mdi:earth
      color: teal
theme: corporate
```

## Template: Roadmap

```infographic
infographic roadmap
data
  title: 2025 Product Roadmap
  tracks
    - name: Platform
      items
        - title: Multi-tenant Architecture
          quarter: Q1
          status: done
        - title: Kubernetes Migration
          quarter: Q2
          status: in-progress
        - title: Edge Computing Support
          quarter: Q3
          status: planned
    - name: AI Features
      items
        - title: RAG Pipeline
          quarter: Q1
          status: done
        - title: Agent Framework
          quarter: Q2
          status: in-progress
        - title: Fine-tuning Platform
          quarter: Q4
          status: planned
    - name: Enterprise
      items
        - title: SSO / SAML
          quarter: Q1
          status: done
        - title: Audit Logging
          quarter: Q2
          status: done
        - title: Compliance Dashboard
          quarter: Q3
          status: planned
theme: tech
```

## Template: Steps (Process Guide)

```infographic
infographic steps
data
  title: CI/CD Pipeline Setup Guide
  items
    - step: 1
      title: Configure Repository
      description: Set up branch protection rules, add .github/workflows directory
      icon: mdi:source-branch
    - step: 2
      title: Write Tests
      description: Unit tests, integration tests, and E2E test suites
      icon: mdi:test-tube
    - step: 3
      title: Build Pipeline
      description: Docker image build, security scanning, artifact publishing
      icon: mdi:hammer-wrench
    - step: 4
      title: Deploy to Staging
      description: Automated deployment with smoke tests and canary analysis
      icon: mdi:cloud-upload
    - step: 5
      title: Production Release
      description: Blue-green deployment with rollback capability
      icon: mdi:rocket-launch
theme: modern
```

## Template: A vs B Comparison

```infographic
infographic comparison
data
  title: Monolith vs Microservices
  optionA:
    name: Monolith
    icon: mdi:cube
    color: blue
  optionB:
    name: Microservices
    icon: mdi:cube-unfolded
    color: green
  criteria
    - name: Deployment Speed
      a: Slow (full redeploy)
      b: Fast (independent services)
      winner: b
    - name: Complexity
      a: Low (single codebase)
      b: High (distributed system)
      winner: a
    - name: Scalability
      a: Vertical only
      b: Horizontal per service
      winner: b
    - name: Team Independence
      a: Coupled
      b: Autonomous teams
      winner: b
    - name: Initial Setup
      a: Quick
      b: Significant overhead
      winner: a
    - name: Debugging
      a: Easy (single process)
      b: Complex (distributed tracing)
      winner: a
theme: minimal
```

## Template: SWOT Analysis

```infographic
infographic swot
data
  title: AI Platform Strategic Analysis
  strengths
    - GPU orchestration expertise
    - Multi-cloud Kubernetes native
    - Integrated fine-tuning pipeline
    - Enterprise security compliance
  weaknesses
    - Limited brand awareness
    - Small partner ecosystem
    - Documentation gaps
    - No free tier
  opportunities
    - Enterprise AI adoption wave
    - On-premise AI demand
    - Vertical SaaS for healthcare/finance
    - NPU/XPU cost reduction
  threats
    - Hyperscaler bundling (AWS/Azure/GCP)
    - Open-source alternatives
    - Rapid technology obsolescence
    - GPU supply constraints
theme: corporate
```

## Template: Funnel

```infographic
infographic funnel
data
  title: Sales Pipeline
  items
    - stage: Awareness
      value: 10,000
      label: Website Visitors
      icon: mdi:eye
    - stage: Interest
      value: 2,500
      label: Free Trial Signups
      icon: mdi:hand-wave
    - stage: Evaluation
      value: 800
      label: Active Evaluators
      icon: mdi:magnify
    - stage: Decision
      value: 200
      label: Sales Qualified
      icon: mdi:handshake
    - stage: Purchase
      value: 50
      label: Paying Customers
      icon: mdi:check-circle
theme: modern
```

## Template: Pie Chart

```infographic
infographic pie-chart
data
  title: Cloud Market Share 2025
  items
    - label: AWS
      value: 31
      color: orange
    - label: Azure
      value: 25
      color: blue
    - label: GCP
      value: 11
      color: red
    - label: Alibaba
      value: 5
      color: yellow
    - label: Others
      value: 28
      color: gray
theme: modern
```

## Template: Bar Chart

```infographic
infographic bar-chart
data
  title: Monthly Active Users by Region
  xLabel: Region
  yLabel: Users (thousands)
  items
    - label: North America
      value: 125
      color: blue
    - label: Europe
      value: 98
      color: green
    - label: Asia Pacific
      value: 156
      color: red
    - label: Latin America
      value: 42
      color: orange
    - label: Middle East
      value: 28
      color: purple
theme: modern
```

## Best Practices

1. **Choose the right template** -- match data type to template; don't force data into wrong shapes
2. **Keep data concise** -- 4-8 items per infographic is ideal; more than 12 becomes cluttered
3. **Use meaningful icons** -- iconify icons add visual context; choose icons that reinforce the message
4. **Theme consistency** -- use the same theme across related infographics for visual cohesion
5. **Label everything** -- every metric needs a clear label, unit, and context (change %, trend direction)
6. **Tell a story** -- arrange items in logical order (chronological, most-to-least, process flow)
7. **Output format** -- always output inside ` ```infographic ` fenced code blocks
