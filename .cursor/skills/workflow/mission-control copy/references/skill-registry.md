## Skill Registry

### Execution Skills (modify code/state)

| Skill | Purpose | SKILL.md Path |
|-------|---------|---------------|
| domain-commit | Domain-split git commits | `.cursor/skills/domain-commit/SKILL.md` |
| local-dev-runner | Start/stop dev stack | `.cursor/skills/local-dev-runner/SKILL.md` |
| e2e-testing | Playwright E2E tests | `.cursor/skills/e2e-testing/SKILL.md` |
| ci-quality-gate | Local CI pipeline | `.cursor/skills/ci-quality-gate/SKILL.md` |
| service-health-doctor | Diagnose/fix services | `.cursor/skills/service-health-doctor/SKILL.md` |
| dependency-auditor | Audit/update deps | `.cursor/skills/dependency-auditor/SKILL.md` |
| i18n-sync | Translation sync | `.cursor/skills/i18n-sync/SKILL.md` |
| kwp-sync | Sync KWP plugins from GitHub | `.cursor/skills/kwp-sync/SKILL.md` |
| webapp-testing | Playwright web app testing | `.agents/skills/webapp-testing/SKILL.md` |

### Review Skills (read-only analysis)

| Skill | Purpose | SKILL.md Path |
|-------|---------|---------------|
| backend-expert | API/architecture review | `.cursor/skills/backend-expert/SKILL.md` |
| frontend-expert | React/Vite review | `.cursor/skills/frontend-expert/SKILL.md` |
| db-expert | Schema/migration review | `.cursor/skills/db-expert/SKILL.md` |
| security-expert | Threat model/OWASP | `.cursor/skills/security-expert/SKILL.md` |
| compliance-governance | Data governance | `.cursor/skills/compliance-governance/SKILL.md` |
| ux-expert | UX/accessibility audit | `.cursor/skills/ux-expert/SKILL.md` |
| sre-devops-expert | Infra/CI/CD review | `.cursor/skills/sre-devops-expert/SKILL.md` |
| qa-test-expert | Test strategy | `.cursor/skills/qa-test-expert/SKILL.md` |
| pr-review-captain | PR summary/risk | `.cursor/skills/pr-review-captain/SKILL.md` |
| performance-profiler | Latency/bundle analysis | `.cursor/skills/performance-profiler/SKILL.md` |

### Generation Skills (create artifacts)

| Skill | Purpose | SKILL.md Path |
|-------|---------|---------------|
| technical-writer | ADR/docs/changelog | `.cursor/skills/technical-writer/SKILL.md` |
| frontend-design | Build UIs | `.agents/skills/frontend-design/SKILL.md` |
| prompt-transformer | Transform prompts | `.cursor/skills/prompt-transformer/SKILL.md` |
| skill-optimizer | Audit/optimize SKILL.md files | `.cursor/skills/skill-optimizer/SKILL.md` |
| algorithmic-art | Generative art with p5.js | `.agents/skills/algorithmic-art/SKILL.md` |
| brand-guidelines | Anthropic brand styling | `.agents/skills/brand-guidelines/SKILL.md` |
| canvas-design | Static visual art (.png/.pdf) | `.agents/skills/canvas-design/SKILL.md` |
| doc-coauthoring | Collaborative doc writing | `.agents/skills/doc-coauthoring/SKILL.md` |
| docx | Word document creation/editing | `.agents/skills/docx/SKILL.md` |
| internal-comms | Internal communications | `.agents/skills/internal-comms/SKILL.md` |
| mcp-builder | MCP server development | `.agents/skills/mcp-builder/SKILL.md` |
| pdf | PDF processing/creation | `.agents/skills/pdf/SKILL.md` |
| pptx | Presentation creation/editing | `.agents/skills/pptx/SKILL.md` |
| skill-creator | Create new skills | `.agents/skills/skill-creator/SKILL.md` |
| slack-gif-creator | Animated GIFs for Slack | `.agents/skills/slack-gif-creator/SKILL.md` |
| theme-factory | Theme styling toolkit | `.agents/skills/theme-factory/SKILL.md` |
| web-artifacts-builder | Multi-component web apps | `.agents/skills/web-artifacts-builder/SKILL.md` |
| xlsx | Spreadsheet creation/editing | `.agents/skills/xlsx/SKILL.md` |

## Goal-to-Skill Mapping

When a goal arrives, match keywords to determine which skills to invoke:

| Goal Pattern | Primary Skills | Secondary Skills |
|-------------|---------------|-----------------|
| "full review" / "quality audit" / "check everything" | ci-quality-gate, security-expert | compliance-governance, qa-test-expert |
| "review this PR" / "code review" | pr-review-captain | security-expert, backend-expert, frontend-expert |
| "new feature" / "implement" | backend-expert, frontend-expert | qa-test-expert, e2e-testing, domain-commit |
| "release" / "prepare release" | pr-review-captain, technical-writer | sre-devops-expert, ci-quality-gate |
| "performance" / "slow" / "latency" | performance-profiler | db-expert, backend-expert |
| "service down" / "broken" / "incident" | service-health-doctor | sre-devops-expert, db-expert, backend-expert |
| "dependencies" / "update packages" / "CVE" | dependency-auditor | security-expert, ci-quality-gate |
| "translations" / "i18n" / "locale" | i18n-sync | frontend-expert |
| "deploy" / "infrastructure" / "helm" | sre-devops-expert | security-expert |
| "database" / "migration" / "schema" | db-expert | backend-expert |
| "UX" / "accessibility" / "design" | ux-expert | frontend-expert |
| "test" / "coverage" / "QA" | qa-test-expert | e2e-testing, ci-quality-gate |
| "optimize skills" / "audit skills" / "skill quality" | skill-optimizer | domain-commit |
| "create skill" / "new skill" / "skill template" | skill-creator | skill-optimizer |
| "Word doc" / "docx" / "report" / "memo" | docx | doc-coauthoring |
| "PDF" / "merge PDF" / "fill form" | pdf | docx |
| "slides" / "presentation" / "pptx" / "deck" | pptx | theme-factory |
| "spreadsheet" / "xlsx" / "csv" / "Excel" | xlsx | — |
| "MCP server" / "MCP tool" / "Model Context Protocol" | mcp-builder | backend-expert |
| "internal comms" / "status report" / "newsletter" | internal-comms | doc-coauthoring |
| "generative art" / "algorithmic art" / "p5.js" | algorithmic-art | canvas-design |
| "poster" / "visual art" / "print design" | canvas-design | theme-factory |
| "brand" / "brand colors" / "brand styling" | brand-guidelines | theme-factory |
| "theme" / "color palette" / "font pairing" | theme-factory | brand-guidelines |
| "GIF" / "animated GIF" / "Slack GIF" | slack-gif-creator | — |
| "web app" / "React app" / "shadcn" / "complex artifact" | web-artifacts-builder | frontend-design |
| "write docs" / "proposal" / "spec" / "co-author" | doc-coauthoring | technical-writer |
| "test web app" / "browser test" / "screenshot" | webapp-testing | e2e-testing |
| "sync KWP" / "update KWP" / "knowledge-work-plugins" | kwp-sync | skill-optimizer |
