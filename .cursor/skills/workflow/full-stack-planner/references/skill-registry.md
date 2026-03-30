# Full-Stack Planner — Skill Registry

Categorized skill list for domain-based matching during plan generation. Skills are grouped by domain so each phase can select the most relevant ones.

> **Verification**: Before assigning a skill, confirm it exists at `.cursor/skills/{skill-name}/SKILL.md`. If not found, assign to `generalPurpose` subagent.

## Table of Contents

- [Context and Survey](#domain-context-and-survey)
- [Role-Based Analysis](#domain-role-based-analysis)
- [Product Management](#domain-product-management-and-research)
- [Backend Engineering](#domain-backend-engineering)
- [Frontend Engineering](#domain-frontend-engineering)
- [Security and Compliance](#domain-security-and-compliance)
- [Testing and Quality](#domain-testing-and-quality)
- [UX and Design](#domain-ux-and-design)
- [Code Review](#domain-code-review)
- [Documentation](#domain-documentation-and-generation)
- [Git and Shipping](#domain-git-and-shipping)
- [Orchestration](#domain-orchestration)
- [Finance and Trading](#domain-finance-and-trading)
- [Domain Matching Guide](#domain-matching-guide)

## Domain: Context and Survey

| Skill | Purpose |
|-------|---------|
| codebase-archaeologist | Git history, ownership maps, churn hotspots |
| recall | Cross-session context from long-term memory |
| refactor-simulator | Blast radius analysis for proposed changes |
| context-engineer | MEMORY.md lifecycle, knowledge graph updates |

## Domain: Role-Based Analysis

| Skill | Purpose |
|-------|---------|
| role-dispatcher | Dispatch topic to all 10 roles, collect results |
| role-ceo | Strategic impact, market positioning |
| role-cto | Architecture gaps, tech debt, security posture |
| role-pm | PRD gaps, sprint priorities, OKR alignment |
| role-developer | Implementation complexity, code quality |
| role-cso | Market sizing, competitive positioning, GTM |
| role-ux-designer | UX gaps, accessibility, design system |
| role-security-engineer | STRIDE threats, OWASP gaps, compliance |
| role-finance | ROI analysis, budget, audit compliance |
| role-sales | Sales enablement, competitive battlecards |
| role-hr | Team capacity, hiring, training needs |
| executive-briefing | Synthesize role analyses into CEO briefing |

## Domain: Product Management and Research

| Skill | Purpose |
|-------|---------|
| pm-market-research | Personas, segmentation, TAM/SAM/SOM |
| pm-product-discovery | Ideation, OSTs, assumption testing |
| pm-product-strategy | Vision, Lean Canvas, SWOT, Porter's Five Forces |
| pm-execution | PRDs, OKRs, sprint planning, user stories |
| pm-go-to-market | GTM strategy, ICP, growth loops |
| pm-data-analytics | SQL queries, cohort analysis, A/B tests |
| pm-marketing-growth | Positioning, North Star metrics, naming |
| pm-toolkit | Resume review, NDA, privacy policy |
| presentation-strategist | Presentation strategy and narrative design |

## Domain: Backend Engineering

| Skill | Purpose |
|-------|---------|
| backend-expert | FastAPI design, Pydantic models, async patterns |
| db-expert | PostgreSQL schemas, Alembic migrations, queries |
| system-thinker | End-to-end system design, data flows |
| sre-devops-expert | CI/CD, Helm, K8s, Docker, runbooks |

## Domain: Frontend Engineering

| Skill | Purpose |
|-------|---------|
| frontend-expert | React components, Vite, Core Web Vitals |
| fsd-development | FSD domain scaffolding and migration |
| design-architect | 4-phase design audit (Jobs/Ive philosophy) |
| overlay-layout-patterns | useOverlay hook modal/drawer patterns |

## Domain: Security and Compliance

| Skill | Purpose |
|-------|---------|
| security-expert | STRIDE, OWASP Top 10, secret detection |
| compliance-governance | Data classification, access control, GDPR |
| dependency-auditor | CVE scanning, safe patch updates |

## Domain: Testing and Quality

| Skill | Purpose |
|-------|---------|
| qa-test-expert | Test strategy, coverage, regression planning |
| test-suite | Full lifecycle: review, generate, run |
| e2e-testing | Playwright E2E test creation and execution |
| ci-quality-gate | Local CI pipeline (lint, test, build) |
| playwright-runner | Ad-hoc browser automation scripts |
| anthropic-webapp-testing | Web app testing with Playwright |
| ai-quality-evaluator | Score AI reports for accuracy |
| evals-skills | LLM evaluation pipeline orchestration |

## Domain: UX and Design

| Skill | Purpose |
|-------|---------|
| ux-expert | UX audits, heuristic evaluation, WCAG |
| ui-suite | 3-agent UI/UX review and fix pipeline |
| design-architect | Design audit with phased implementation |

## Domain: Code Review

| Skill | Purpose |
|-------|---------|
| deep-review | 4-agent parallel multi-domain review |
| simplify | Code quality, DRY, tech debt auto-fix |
| code-review-all | Adversarial 3-agent review with scoring |
| pr-review-captain | PR summary, risk assessment, release notes |
| workflow-eval-opt | Evaluator-optimizer quality loops |

## Domain: Documentation and Generation

| Skill | Purpose |
|-------|---------|
| technical-writer | ADRs, API docs, changelogs, guides |
| visual-explainer | Interactive HTML diagrams and visualizations |
| prompt-architect | Framework-based prompt design (8 frameworks) |
| prompt-transformer | Transform prompts to professional quality |
| anthropic-docx | Word document generation |
| anthropic-pptx | PowerPoint presentation generation |
| anthropic-pdf | PDF reading, creation, manipulation |

## Domain: Git and Shipping

| Skill | Purpose |
|-------|---------|
| domain-commit | Domain-split git commits with pre-commit |
| release-ship | Push + create PR pipeline |
| ship | Pre-merge pipeline: review, fix, commit, PR |
| release-commander | Full release lifecycle (10-skill pipeline) |
| commit-to-issue | Create GitHub issues from commits |

## Domain: Orchestration

| Skill | Purpose |
|-------|---------|
| mission-control | Multi-skill workflow orchestration |
| plans | Prompt optimization + skill-based planning |
| diagnose | 3-agent root cause analysis + auto-fix |
| ralph-loop | Continuous agent loop for batch tasks |

## Domain: Finance and Trading

| Skill | Purpose |
|-------|---------|
| daily-stock-check | Turtle/Bollinger analysis + Slack post |
| weekly-stock-update | Yahoo Finance price sync to DB |
| stock-csv-downloader | investing.com CSV download + DB import |
| today | Full daily pipeline (sync, screen, analyze, report) |
| alphaear-search | Finance-specific web/local search |
| alphaear-news | Multi-source finance news aggregation |
| alphaear-sentiment | Financial text sentiment analysis |
| alphaear-signal-tracker | Investment signal evolution tracking |
| alphaear-predictor | Market prediction with Kronos model |
| alphaear-reporter | Professional financial report generation |

## Domain: Internationalization

| Skill | Purpose |
|-------|---------|
| i18n-sync | Translation key sync across locale files |

## Domain Matching Guide

When assigning skills in Phase Decomposition:

1. Classify each sub-step by domain (use the headers above)
2. Select the most specific skill within that domain
3. If multiple skills match, prefer the one whose description most closely matches the sub-step
4. If no domain matches, use `generalPurpose` subagent
