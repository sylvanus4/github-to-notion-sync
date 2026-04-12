# Skill Registry

## Available Skills (Implemented)

These skills exist in the repository and can be delegated to:

### Orchestrator Skills

| Skill | Purpose | SKILL.md Path | Type |
|-------|---------|---------------|------|
| mission-control | Orchestrate multi-skill workflows | `.cursor/skills/mission-control/SKILL.md` | Orchestrator |
| deep-review | Multi-domain full-stack review (4 agents) | `.cursor/skills/deep-review/SKILL.md` | Orchestrator |
| diagnose | Root cause analysis (3 agents) + auto-fix | `.cursor/skills/diagnose/SKILL.md` | Orchestrator |
| ship | Pre-merge pipeline: review → fix → commit → PR | `.cursor/skills/ship/SKILL.md` | Orchestrator |
| simplify | Code review + auto-fix (4 agents) | `.cursor/skills/simplify/SKILL.md` | Orchestrator |
| test-suite | Test full-lifecycle: review → generate → run | `.cursor/skills/test-suite/SKILL.md` | Orchestrator |
| ui-suite | UI/UX full-lifecycle review and fix | `.cursor/skills/ui-suite/SKILL.md` | Orchestrator |
| plans | Prompt optimization + skill-based execution planning | `.cursor/skills/plans/SKILL.md` | Orchestrator |
| ralph-loop | Continuous AI agent loop for long-running tasks | `.cursor/skills/ralph-loop/SKILL.md` | Orchestrator |

### Execution Skills

| Skill | Purpose | SKILL.md Path | Type |
|-------|---------|---------------|------|
| domain-commit | Domain-split git commits | `.cursor/skills/domain-commit/SKILL.md` | Execution |
| commit-to-issue | Create GitHub issues from commits | `.cursor/skills/commit-to-issue/SKILL.md` | Execution |
| github-workflow-automation | Full GitHub workflow automation | `.cursor/skills/github-workflow-automation/SKILL.md` | Execution |
| cursor-sync | Sync .cursor/ assets across projects | `.cursor/skills/cursor-sync/SKILL.md` | Execution |
| cursor-automations | Create/manage Cursor cloud agents | `.cursor/skills/cursor-automations/SKILL.md` | Execution |
| local-dev-runner | Start/stop dev stack | `.cursor/skills/local-dev-runner/SKILL.md` | Execution |
| e2e-testing | Playwright E2E tests | `.cursor/skills/e2e-testing/SKILL.md` | Execution |
| ci-quality-gate | Local CI pipeline (lint, test, build) | `.cursor/skills/ci-quality-gate/SKILL.md` | Execution |
| service-health-doctor | Diagnose/fix services | `.cursor/skills/service-health-doctor/SKILL.md` | Execution |
| dependency-auditor | Audit/update dependencies | `.cursor/skills/dependency-auditor/SKILL.md` | Execution |
| i18n-sync | Translation synchronization | `.cursor/skills/i18n-sync/SKILL.md` | Execution |
| transcribee | Transcribe video/audio with diarization | `.cursor/skills/transcribee/SKILL.md` | Execution |
| video-compress | ffmpeg video compression | `.cursor/skills/video-compress/SKILL.md` | Execution |
| x-to-slack | Tweet intelligence to Slack | `.cursor/skills/x-to-slack/SKILL.md` | Execution |
| slack-agent | Build/deploy Slack bots | `.cursor/skills/slack-agent/SKILL.md` | Execution |
| agent-browser | Headless browser automation via CLI | `.cursor/skills/agent-browser/SKILL.md` | Execution |
| defuddle | Extract clean markdown from web pages | `.cursor/skills/defuddle/SKILL.md` | Execution |
| daiso-mcp | Korean retail store/inventory search | `.cursor/skills/daiso-mcp/SKILL.md` | Execution |
| public-apis | Search 1,400+ free public APIs | `.cursor/skills/public-apis/SKILL.md` | Execution |
| scrapling | Python web scraping with anti-bot bypass | `.cursor/skills/scrapling/SKILL.md` | Execution |
| notion-docs-sync | Sync markdown docs to Notion | `.cursor/skills/notion/notion-docs-sync/SKILL.md` | Execution |

### Review Skills

| Skill | Purpose | SKILL.md Path | Type |
|-------|---------|---------------|------|
| backend-expert | API/architecture review | `.cursor/skills/backend-expert/SKILL.md` | Review |
| frontend-expert | React/Vite review | `.cursor/skills/frontend-expert/SKILL.md` | Review |
| db-expert | Schema/migration review | `.cursor/skills/db-expert/SKILL.md` | Review |
| security-expert | Threat model/OWASP | `.cursor/skills/security-expert/SKILL.md` | Review |
| compliance-governance | Data governance | `.cursor/skills/compliance-governance/SKILL.md` | Review |
| ux-expert | UX/accessibility audit | `.cursor/skills/ux-expert/SKILL.md` | Review |
| sre-devops-expert | Infra/CI/CD review | `.cursor/skills/sre-devops-expert/SKILL.md` | Review |
| qa-test-expert | Test strategy | `.cursor/skills/qa-test-expert/SKILL.md` | Review |
| pr-review-captain | PR summary/risk assessment | `.cursor/skills/pr-review-captain/SKILL.md` | Review |
| performance-profiler | Latency/bundle analysis | `.cursor/skills/performance-profiler/SKILL.md` | Review |
| design-architect | 4-phase design audit (Jobs/Ive philosophy) | `.cursor/skills/design-architect/SKILL.md` | Review |
| skill-optimizer | Audit/evaluate/benchmark skills | `.cursor/skills/skill-optimizer/SKILL.md` | Review |
| problem-definition | 5D problem definition framework (PDD) | `.cursor/skills/problem-definition/SKILL.md` | Review |

### Generation Skills

| Skill | Purpose | SKILL.md Path | Type |
|-------|---------|---------------|------|
| technical-writer | ADR/docs/changelog | `.cursor/skills/technical-writer/SKILL.md` | Generation |
| visual-explainer | Generate visual HTML explanations | `.cursor/skills/visual-explainer/SKILL.md` | Generation |
| prompt-transformer | Transform prompts to professional quality | `.cursor/skills/prompt-transformer/SKILL.md` | Generation |
| prompt-architect | Framework-based prompt design (8 frameworks) | `.cursor/skills/prompt-architect/SKILL.md` | Generation |
| evals-skills | LLM evaluation pipeline orchestration | `.cursor/skills/evals-skills/SKILL.md` | Evaluation |
| docs-tutor | Interactive quiz tutor for StudyVault | `.cursor/skills/docs-tutor/SKILL.md` | Generation |
| docs-tutor-setup | Generate StudyVault from docs | `.cursor/skills/docs-tutor-setup/SKILL.md` | Generation |

### Frontend Pattern Skills

| Skill | Purpose | SKILL.md Path | Type |
|-------|---------|---------------|------|
| fsd-development | FSD domain generation/migration | `.cursor/skills/fsd-development/SKILL.md` | Execution |
| overlay-layout-patterns | useOverlay hook overlay patterns | `.cursor/skills/overlay-layout-patterns/SKILL.md` | Reference |

### Product Management Skills

| Skill | Purpose | SKILL.md Path | Type |
|-------|---------|---------------|------|
| pm-data-analytics | SQL, cohort analysis, A/B test | `.cursor/skills/pm-data-analytics/SKILL.md` | Execution |
| pm-execution | PRDs, OKRs, sprint planning | `.cursor/skills/pm-execution/SKILL.md` | Execution |
| pm-go-to-market | GTM strategy, ICP, growth loops | `.cursor/skills/pm-go-to-market/SKILL.md` | Execution |
| pm-market-research | Personas, segmentation, TAM/SAM/SOM | `.cursor/skills/pm-market-research/SKILL.md` | Execution |
| pm-marketing-growth | Positioning, North Star metrics | `.cursor/skills/pm-marketing-growth/SKILL.md` | Execution |
| pm-product-discovery | Ideation, OSTs, experiment design | `.cursor/skills/pm-product-discovery/SKILL.md` | Execution |
| pm-product-strategy | Vision, strategy canvas, Lean Canvas | `.cursor/skills/pm-product-strategy/SKILL.md` | Execution |
| pm-toolkit | Resume review, NDA, privacy policy | `.cursor/skills/pm-toolkit/SKILL.md` | Execution |

### Google Workspace Skills

| Skill | Purpose | SKILL.md Path | Type |
|-------|---------|---------------|------|
| gws-workspace | Install/auth/configure gws CLI | `.cursor/skills/gws-workspace/SKILL.md` | Execution |
| gws-calendar | Calendar agenda, events, freebusy | `.cursor/skills/gws-calendar/SKILL.md` | Execution |
| gws-chat | Google Chat messages and spaces | `.cursor/skills/gws-chat/SKILL.md` | Execution |
| gws-docs | Google Docs CRUD | `.cursor/skills/gws-docs/SKILL.md` | Execution |
| gws-drive | Drive files, permissions, folders | `.cursor/skills/gws-drive/SKILL.md` | Execution |
| gws-gmail | Gmail send, triage, watch, labels | `.cursor/skills/gws-gmail/SKILL.md` | Execution |
| gws-sheets | Sheets read, append, create | `.cursor/skills/gws-sheets/SKILL.md` | Execution |
| gws-workflows | Cross-service productivity workflows | `.cursor/skills/gws-workflows/SKILL.md` | Execution |
| gws-recipe-audit-sharing | Audit externally shared Drive files | `.cursor/skills/gws-recipe-audit-sharing/SKILL.md` | Execution |
| gws-recipe-doc-from-template | Create Doc from template | `.cursor/skills/gws-recipe-doc-from-template/SKILL.md` | Execution |
| gws-recipe-events-from-sheet | Create Calendar events from Sheets | `.cursor/skills/gws-recipe-events-from-sheet/SKILL.md` | Execution |
| gws-recipe-personalized-emails | Mail merge from Sheets to Gmail | `.cursor/skills/gws-recipe-personalized-emails/SKILL.md` | Execution |
| gws-recipe-save-email-to-doc | Archive Gmail to Docs | `.cursor/skills/gws-recipe-save-email-to-doc/SKILL.md` | Execution |
