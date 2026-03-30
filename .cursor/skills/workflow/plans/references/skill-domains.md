# Skill Domain Mapping

Reference table mapping task domains to available skills for Phase 2 skill matching. Each entry includes the skill path, type, and trigger keywords to help match sub-tasks.

## How to Use This File

For each sub-task from Phase 2 decomposition:
1. Identify which domain(s) the sub-task falls into
2. Check the skills listed for that domain
3. Verify the skill exists at its path before assigning
4. If no skill matches, assign to `generalPurpose` subagent

## Domain-to-Skill Mapping

### Code Quality and Review

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| simplify | `.cursor/skills/simplify/SKILL.md` | Orchestrator | code review, refactor, tech debt, code quality, clean up |
| deep-review | `.cursor/skills/deep-review/SKILL.md` | Orchestrator | full-stack review, multi-domain review, comprehensive review |
| backend-expert | `.cursor/skills/backend-expert/SKILL.md` | Review | API design, FastAPI, microservice, Pydantic, async |
| frontend-expert | `.cursor/skills/frontend-expert/SKILL.md` | Review | React, Vite, component architecture, bundle, frontend |
| refactor-simulator | `.cursor/skills/refactor-simulator/SKILL.md` | Review | blast radius, impact analysis, refactor simulator, what if I change, before refactoring |

### Testing

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| test-suite | `.cursor/skills/test-suite/SKILL.md` | Orchestrator | test coverage, generate tests, run tests, test audit |
| qa-test-expert | `.cursor/skills/qa-test-expert/SKILL.md` | Review | test strategy, test plan, coverage analysis |
| e2e-testing | `.cursor/skills/e2e-testing/SKILL.md` | Execution | Playwright, E2E test, browser test, end-to-end |

### Security and Compliance

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| security-expert | `.cursor/skills/security-expert/SKILL.md` | Review | threat model, OWASP, vulnerability, secret detection, PII |
| compliance-governance | `.cursor/skills/compliance-governance/SKILL.md` | Review | data governance, GDPR, SOC2, access control, audit logging |

### Performance

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| performance-profiler | `.cursor/skills/performance-profiler/SKILL.md` | Review | latency, p95, slow query, bundle size, SLO |

### UI / UX / Design

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| ui-suite | `.cursor/skills/ui-suite/SKILL.md` | Orchestrator | UI review, design audit, UX check, frontend quality |
| design-architect | `.cursor/skills/design-architect/SKILL.md` | Review | design audit, visual polish, premium design, Jobs/Ive |
| ux-expert | `.cursor/skills/ux-expert/SKILL.md` | Review | UX audit, heuristic evaluation, accessibility, WCAG |
| fsd-development | `.cursor/skills/fsd-development/SKILL.md` | Execution | FSD, feature-sliced, domain migration, entities |

### Database

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| db-expert | `.cursor/skills/db-expert/SKILL.md` | Review | PostgreSQL, schema, migration, query optimization, Redis |

### DevOps / Infrastructure

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| sre-devops-expert | `.cursor/skills/sre-devops-expert/SKILL.md` | Review | CI/CD, Helm, Kubernetes, Docker, runbook, SLO |
| ci-quality-gate | `.cursor/skills/ci-quality-gate/SKILL.md` | Execution | CI pipeline, lint, test, build, quality gate |
| local-dev-runner | `.cursor/skills/local-dev-runner/SKILL.md` | Execution | start dev, stop dev, local environment, dev stack |
| service-health-doctor | `.cursor/skills/service-health-doctor/SKILL.md` | Execution | service health, port conflict, restart, troubleshoot |

### Documentation

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| technical-writer | `.cursor/skills/technical-writer/SKILL.md` | Generation | ADR, API docs, changelog, operational guide |

### Git / PR / Release

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| domain-commit | `.cursor/skills/domain-commit/SKILL.md` | Execution | commit, pre-commit, split commits, domain commit |
| ship | `.cursor/skills/ship/SKILL.md` | Orchestrator | ship, pre-merge, review + commit + PR |
| pr-review-captain | `.cursor/skills/pr-review-captain/SKILL.md` | Review | PR summary, change risk, review checklist, release notes |
| github-workflow-automation | `.cursor/skills/github-workflow-automation/SKILL.md` | Execution | issue, branch, commit, push, PR, GitHub workflow |
| release-commander | `.cursor/skills/release-commander/SKILL.md` | Orchestrator | release, prepare release, release pipeline, full release check |

### Code History / Temporal Analysis

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| codebase-archaeologist | `.cursor/skills/codebase-archaeologist/SKILL.md` | Review | code ownership, bus factor, churn analysis, code history, dead code, risk heatmap |

### Debugging / Diagnosis

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| diagnose | `.cursor/skills/diagnose/SKILL.md` | Orchestrator | bug, debug, root cause, error, failing, diagnose |
| problem-definition | `.cursor/skills/problem-definition/SKILL.md` | Review | define problem, frame problem, root cause hypothesis |
| incident-to-improvement | `.cursor/skills/incident-to-improvement/SKILL.md` | Orchestrator | incident, post-mortem, outage, production issue, incident response lifecycle |

### Internationalization

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| i18n-sync | `.cursor/skills/i18n-sync/SKILL.md` | Execution | translation, i18n, locale, missing keys, sync translations |

### Dependencies

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| dependency-auditor | `.cursor/skills/dependency-auditor/SKILL.md` | Execution | dependency audit, CVE, update packages, vulnerability scan |

### Prompt Engineering

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| prompt-architect | `.cursor/skills/prompt-architect/SKILL.md` | Review | architect prompt, framework, CO-STAR, RISEN, prompt structure |
| prompt-transformer | `.cursor/skills/prompt-transformer/SKILL.md` | Execution | transform prompt, polish prompt, improve prompt quality |

### Product Management

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| pm-execution | `.cursor/skills/pm-execution/SKILL.md` | Generation | PRD, OKR, sprint plan, retrospective, release notes |
| pm-product-discovery | `.cursor/skills/pm-product-discovery/SKILL.md` | Generation | ideation, assumption testing, opportunity tree, interview |
| pm-product-strategy | `.cursor/skills/pm-product-strategy/SKILL.md` | Generation | product vision, lean canvas, SWOT, pricing strategy |
| pm-go-to-market | `.cursor/skills/pm-go-to-market/SKILL.md` | Generation | GTM, launch plan, ICP, growth loops, battlecard |
| pm-market-research | `.cursor/skills/pm-market-research/SKILL.md` | Generation | persona, segmentation, customer journey, TAM/SAM/SOM |
| pm-marketing-growth | `.cursor/skills/pm-marketing-growth/SKILL.md` | Generation | positioning, value proposition, North Star metric |

### Data Analysis

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| pm-data-analytics | `.cursor/skills/pm-data-analytics/SKILL.md` | Generation | SQL query, cohort analysis, A/B test, retention |

### Media / Content

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| transcribee | `.cursor/skills/transcribee/SKILL.md` | Execution | transcribe, video, audio, diarization, podcast |
| video-compress | `.cursor/skills/video-compress/SKILL.md` | Execution | compress video, ffmpeg, shrink video |
| visual-explainer | `.cursor/skills/visual-explainer/SKILL.md` | Generation | diagram, visualization, visual explanation, HTML page |
| demo-forge | `.cursor/skills/demo-forge/SKILL.md` | Generation | product demo, showcase changes, stakeholder demo, demo from diff |

### Communication / Integrations

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| x-to-slack | `.cursor/skills/x-to-slack/SKILL.md` | Execution | tweet, X/Twitter, Slack post |
| slack-agent | `.cursor/skills/slack-agent/SKILL.md` | Execution | Slack bot, Slack app, Bolt |
| notion-docs-sync | `.cursor/skills/notion-docs-sync/SKILL.md` | Execution | Notion sync, sync docs |

### Onboarding

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| onboarding-accelerator | `.cursor/skills/onboarding-accelerator/SKILL.md` | Orchestrator | onboarding, new developer, getting started kit, new team member |

### Orchestration

| Skill | Path | Type | Trigger Keywords |
|-------|------|------|-----------------|
| mission-control | `.cursor/skills/mission-control/SKILL.md` | Orchestrator | multi-skill, full audit, release prep, incident response |

## Fallback Rules

1. If no skill matches a sub-task, assign to `generalPurpose` subagent with a clear task description
2. If a skill path does not exist on disk, note it as "planned" and fall back to `generalPurpose`
3. If a sub-task spans multiple domains, assign the primary-domain skill and note secondary domains in the plan
4. KWP skills (`kwp-*`) are available for business domain tasks (sales, marketing, HR, legal, finance, operations, customer support) — match by domain prefix when relevant
