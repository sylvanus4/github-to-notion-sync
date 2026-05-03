---
name: agency-roster
description: >-
  Manage and orchestrate 68 Agency AI specialist agents installed as Cursor
  skills. List agents by division, compose teams for scenarios, activate
  agents, and map overlaps with existing project skills. Use when the user
  asks to 'list agency agents', 'agency roster', 'agency team', 'activate
  agent', 'agency-roster', 'agency 목록', 'agency 팀', 'agent 활성화', or wants to
  use specialized AI personalities for tasks. Do NOT use for creating new
  skills (use create-skill) or optimizing existing skills (use
  skill-optimizer).
---

# Agency Roster

68 specialized AI agents from [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) installed as Cursor skills under `.cursor/skills/agency-*/SKILL.md`. Source commit: `2293264` (2026-03-09).

## How to Activate

Each agent is a skill in `.cursor/skills/agency-{name}/SKILL.md`.

**Single agent**: Read the skill and adopt its persona:
```
Read the agency-frontend-developer skill and use it to review this component.
```

**Multi-agent team**: Read multiple skills and assign roles:
```
Read the agency-frontend-developer and agency-ux-researcher skills, then review this page for both implementation quality and usability.
```

## Agent Roster by Division

### Engineering (10 agents)

| Skill Name | Agent | Specialty |
|-----------|-------|-----------|
| `agency-frontend-developer` | Frontend Developer | React/Vue/Angular, UI, performance optimization |
| `agency-backend-architect` | Backend Architect | API design, database architecture, scalability |
| `agency-mobile-app-builder` | Mobile App Builder | iOS/Android, React Native, Flutter |
| `agency-ai-engineer` | AI Engineer | ML models, deployment, AI integration |
| `agency-devops-automator` | DevOps Automator | CI/CD, infrastructure automation, cloud ops |
| `agency-rapid-prototyper` | Rapid Prototyper | Fast POC development, MVPs |
| `agency-senior-developer` | Senior Developer | Laravel/Livewire, advanced patterns |
| `agency-security-engineer` | Security Engineer | Threat modeling, secure code review |
| `agency-data-engineer` | Data Engineer | Pipelines, lakehouse, Spark, dbt, streaming |
| `agency-developer-advocate` | Developer Advocate | DevRel, DX, community building |

### Design (8 agents)

| Skill Name | Agent | Specialty |
|-----------|-------|-----------|
| `agency-ui-designer` | UI Designer | Visual design, component libraries, design systems |
| `agency-ux-researcher` | UX Researcher | User testing, behavior analysis |
| `agency-ux-architect` | UX Architect | Technical architecture, CSS systems |
| `agency-brand-guardian` | Brand Guardian | Brand identity, consistency, positioning |
| `agency-visual-storyteller` | Visual Storyteller | Visual narratives, multimedia content |
| `agency-whimsy-injector` | Whimsy Injector | Personality, delight, playful interactions |
| `agency-image-prompt-engineer` | Image Prompt Engineer | AI image generation prompts |
| `agency-inclusive-visuals-specialist` | Inclusive Visuals Specialist | Bias-free, culturally accurate image generation |

### Marketing (11 agents)

| Skill Name | Agent | Specialty |
|-----------|-------|-----------|
| `agency-growth-hacker` | Growth Hacker | User acquisition, viral loops, experiments |
| `agency-content-creator` | Content Creator | Multi-platform content, editorial calendars |
| `agency-twitter-engager` | Twitter Engager | Real-time engagement, thought leadership |
| `agency-tiktok-strategist` | TikTok Strategist | Viral content, algorithm optimization |
| `agency-instagram-curator` | Instagram Curator | Visual storytelling, community building |
| `agency-reddit-community-builder` | Reddit Community Builder | Authentic engagement, value-driven content |
| `agency-app-store-optimizer` | App Store Optimizer | ASO, conversion optimization |
| `agency-social-media-strategist` | Social Media Strategist | Cross-platform strategy, campaigns |
| `agency-xiaohongshu-specialist` | Xiaohongshu Specialist | Lifestyle content, trend-driven strategy |
| `agency-wechat-official-account-manager` | WeChat OA Manager | Subscriber engagement, content marketing |
| `agency-zhihu-strategist` | Zhihu Strategist | Thought leadership, knowledge-driven engagement |

### Product (3 agents)

| Skill Name | Agent | Specialty |
|-----------|-------|-----------|
| `agency-sprint-prioritizer` | Sprint Prioritizer | Agile planning, feature prioritization |
| `agency-trend-researcher` | Trend Researcher | Market intelligence, competitive analysis |
| `agency-feedback-synthesizer` | Feedback Synthesizer | User feedback analysis, insights extraction |

### Project Management (5 agents)

| Skill Name | Agent | Specialty |
|-----------|-------|-----------|
| `agency-studio-producer` | Studio Producer | Portfolio management, strategic alignment |
| `agency-project-shepherd` | Project Shepherd | Cross-functional coordination, timelines |
| `agency-studio-operations` | Studio Operations | Day-to-day efficiency, process optimization |
| `agency-experiment-tracker` | Experiment Tracker | A/B tests, hypothesis validation |
| `agency-senior-project-manager` | Senior Project Manager | Realistic scoping, spec-to-task conversion |

### Testing (8 agents)

| Skill Name | Agent | Specialty |
|-----------|-------|-----------|
| `agency-evidence-collector` | Evidence Collector | Screenshot-based QA, visual proof |
| `agency-reality-checker` | Reality Checker | Evidence-based certification, quality gates |
| `agency-test-results-analyzer` | Test Results Analyzer | Test evaluation, metrics analysis |
| `agency-performance-benchmarker` | Performance Benchmarker | Speed testing, load testing |
| `agency-api-tester` | API Tester | API validation, integration testing |
| `agency-tool-evaluator` | Tool Evaluator | Technology assessment, tool selection |
| `agency-workflow-optimizer` | Workflow Optimizer | Process analysis, workflow improvement |
| `agency-accessibility-auditor` | Accessibility Auditor | WCAG auditing, assistive technology testing |

### Support (6 agents)

| Skill Name | Agent | Specialty |
|-----------|-------|-----------|
| `agency-support-responder` | Support Responder | Customer service, issue resolution |
| `agency-analytics-reporter` | Analytics Reporter | Data analysis, dashboards, insights |
| `agency-finance-tracker` | Finance Tracker | Financial planning, budget management |
| `agency-infrastructure-maintainer` | Infrastructure Maintainer | System reliability, performance |
| `agency-legal-compliance-checker` | Legal Compliance Checker | Compliance, regulations, legal review |
| `agency-executive-summary-generator` | Executive Summary Generator | C-suite communication, strategic summaries |

### Spatial Computing (6 agents)

| Skill Name | Agent | Specialty |
|-----------|-------|-----------|
| `agency-xr-interface-architect` | XR Interface Architect | Spatial interaction design, immersive UX |
| `agency-macos-spatial-metal-engineer` | macOS Spatial/Metal Engineer | Swift, Metal, high-performance 3D |
| `agency-xr-immersive-developer` | XR Immersive Developer | WebXR, browser-based AR/VR |
| `agency-xr-cockpit-interaction-specialist` | XR Cockpit Interaction Specialist | Cockpit-based controls |
| `agency-visionos-spatial-engineer` | visionOS Spatial Engineer | Apple Vision Pro development |
| `agency-terminal-integration-specialist` | Terminal Integration Specialist | Terminal integration, SwiftTerm |

### Specialized (11 agents)

| Skill Name | Agent | Specialty |
|-----------|-------|-----------|
| `agency-agents-orchestrator` | Agents Orchestrator | Multi-agent coordination, workflow management |
| `agency-data-analytics-reporter` | Data Analytics Reporter | Business intelligence, data insights |
| `agency-lsp-index-engineer` | LSP/Index Engineer | Language Server Protocol, code intelligence |
| `agency-sales-data-extraction-agent` | Sales Data Extraction | Excel monitoring, sales metric extraction |
| `agency-data-consolidation-agent` | Data Consolidation | Sales data aggregation, dashboard reports |
| `agency-report-distribution-agent` | Report Distribution | Automated report delivery |
| `agency-agentic-identity-trust-architect` | Agentic Identity & Trust | Agent identity, authentication, audit trails |
| `agency-autonomous-optimization-architect` | Autonomous Optimization | Performance shadow-testing, cost guardrails |
| `agency-behavioral-nudge-engine` | Behavioral Nudge Engine | Adaptive interaction cadences, motivation |
| `agency-cultural-intelligence-strategist` | Cultural Intelligence | Global context, intersectional identity inclusion |
| `agency-technical-writer` | Technical Writer | Developer docs, API references, tutorials |

## Team Templates

### Startup MVP
1. `agency-frontend-developer` -- Build the React app
2. `agency-backend-architect` -- Design the API and database
3. `agency-growth-hacker` -- Plan user acquisition
4. `agency-rapid-prototyper` -- Fast iteration cycles
5. `agency-reality-checker` -- Quality before launch

### Marketing Campaign Launch
1. `agency-content-creator` -- Campaign content
2. `agency-twitter-engager` -- Twitter strategy
3. `agency-instagram-curator` -- Visual content
4. `agency-reddit-community-builder` -- Community engagement
5. `agency-analytics-reporter` -- Performance tracking

### Enterprise Feature Development
1. `agency-senior-project-manager` -- Scope and tasks
2. `agency-senior-developer` -- Complex implementation
3. `agency-ui-designer` -- Design system and components
4. `agency-experiment-tracker` -- A/B test planning
5. `agency-evidence-collector` -- Quality verification
6. `agency-reality-checker` -- Production readiness

### Full Product Discovery
1. `agency-trend-researcher` -- Market validation
2. `agency-backend-architect` -- Technical architecture
3. `agency-brand-guardian` -- Brand strategy
4. `agency-growth-hacker` -- Go-to-market
5. `agency-support-responder` -- Support systems
6. `agency-ux-researcher` -- UX research
7. `agency-project-shepherd` -- Project execution
8. `agency-xr-interface-architect` -- Spatial UI design

### Data Pipeline Build
1. `agency-data-engineer` -- Pipeline architecture
2. `agency-backend-architect` -- API layer
3. `agency-devops-automator` -- CI/CD and infra
4. `agency-performance-benchmarker` -- Load testing
5. `agency-security-engineer` -- Security review

### AI Feature Development
1. `agency-ai-engineer` -- ML model development
2. `agency-backend-architect` -- API integration
3. `agency-frontend-developer` -- UI for AI features
4. `agency-api-tester` -- API validation
5. `agency-data-engineer` -- Data pipeline

## Overlap Map with Existing Project Skills

Agency agents bring **personality-driven perspectives** that complement existing **process-driven project skills**. Use both for maximum coverage.

| Agency Agent | Existing Skill | When to Use Agency | When to Use Existing |
|-------------|---------------|-------------------|---------------------|
| `agency-frontend-developer` | `frontend-expert` | General React/Vue review, new projects | Project-specific React/Vite patterns |
| `agency-backend-architect` | `backend-expert` | General API/system design | FastAPI/Pydantic project patterns |
| `agency-security-engineer` | `security-expert` | Full threat model exercise | Project-specific STRIDE/OWASP checks |
| `agency-ui-designer` | `design-architect` | Visual design, component creation | 14-dimension Jobs/Ive audit |
| `agency-ux-researcher` | `ux-expert` | User testing, research planning | Heuristic evaluation, WCAG audit |
| `agency-devops-automator` | `sre-devops-expert` | General CI/CD automation | Project Helm/K8s/Docker configs |
| `agency-accessibility-auditor` | `kwp-design-accessibility-review` | Full WCAG audit with AT testing | Quick accessibility check |
| `agency-technical-writer` | `technical-writer` | General dev docs, tutorials | ADRs, changelogs, project docs |
| `agency-performance-benchmarker` | `performance-profiler` | Load/speed testing methodology | Project SLO/latency analysis |
| `agency-sprint-prioritizer` | `pm-execution` | Sprint planning personality | PRD/OKR/roadmap frameworks |
| `agency-data-analytics-reporter` | `kwp-data-data-visualization` | Dashboard creation, BI insights | Python chart creation |
| `agency-executive-summary-generator` | `kwp-product-management-stakeholder-comms` | McKinsey/BCG-style exec summaries | Product stakeholder updates |

## Maintenance

- **Source**: `msitarzewski/agency-agents` @ commit `2293264` (2026-03-09)
- **Location**: `.cursor/skills/agency-*/SKILL.md` (68 skills)
- **Update**: Re-clone source repo, run `scripts/convert-agency-rules-to-skills.py`, then `scripts/optimize-agency-skills.py`
- **Optimization**: All skills optimized to <500 lines via `optimize-agency-skills.py` (large code blocks extracted to `references/`)

## Examples

### Example 1: Activate agent
**User says:** "Activate the Roster agent" or "I need a roster perspective"
**Actions:** Agent persona is loaded and responds in character with domain expertise.
**Result:** Agent provides specialized guidance based on its core mission and expertise.

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Agent breaks character | Re-read the identity section and re-establish persona context |
| Output lacks domain depth | Request the agent to reference its core capabilities and provide detailed analysis |
| Conflicting with project skills | Use the project-specific skill instead; agency agents are for general domain expertise |
