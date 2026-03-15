# Category Mapping Rules

Maps skill names to their target guide files using prefix matching and keyword rules.
Rules are evaluated top-to-bottom; first match wins.

## Prefix Rules

| Prefix / Pattern | Target Guide File | Category |
|------------------|-------------------|----------|
| `agency-*` | `27-agency-specialists.md` | Agency 전문가 |
| `alphaear-*` | `18-alphaear-financial-analysis.md` | AlphaEar 금융 분석 |
| `anthropic-*` | `17-anthropic-toolkit.md` | Anthropic 툴킷 |
| `autoskill-*` | `29-autoskill-system.md` | AutoSkill 시스템 |
| `ecc-*` | `26-ecc-skills.md` | ECC 스킬 |
| `gws-*` | `16-gws-google-workspace.md` | Google Workspace |
| `hf-*` | `25-huggingface-ml.md` | HuggingFace ML |
| `kwp-*` | See KWP sub-rules below | KWP 도메인 스킬 |
| `nlm-*` | `20-notebooklm.md` | NotebookLM |
| `paperclip-*` | `21-paperclip-agents.md` | Paperclip 에이전트 |
| `pm-*` | `10-product-management.md` | 프로덕트 매니지먼트 |
| `role-*` | `28-role-based-analysis.md` | 역할 기반 분석 |
| `sp-*` | `22-sp-development-workflow.md` | SP 개발 워크플로우 |
| `tab-*` | `30-tab-stock-pipeline-api.md` | TAB 파이프라인 API |
| `trading-*` | `24-trading-strategies.md` | 트레이딩 전략 |
| `workflow-*` | `23-workflow-patterns.md` | 워크플로우 패턴 |

## KWP Sub-Rules

| KWP Prefix | Target Guide File |
|------------|-------------------|
| `kwp-apollo-*` | `kwp-apollo.md` |
| `kwp-bio-research-*` | `kwp-bio-research.md` |
| `kwp-brand-voice-*` | `kwp-brand-voice.md` |
| `kwp-common-room-*` | `kwp-common-room.md` |
| `kwp-cowork-*` | `kwp-productivity-collaboration.md` |
| `kwp-customer-support-*` | `kwp-customer-support.md` |
| `kwp-data-*` | `kwp-data.md` |
| `kwp-design-*` | `kwp-design.md` |
| `kwp-engineering-*` | `kwp-engineering.md` |
| `kwp-enterprise-search-*` | `kwp-enterprise-search.md` |
| `kwp-finance-*` | `kwp-finance.md` |
| `kwp-human-resources-*` | `kwp-human-resources.md` |
| `kwp-legal-*` | `kwp-legal.md` |
| `kwp-marketing-*` | `kwp-marketing.md` |
| `kwp-operations-*` | `kwp-operations.md` |
| `kwp-product-management-*` | `kwp-product-management.md` |
| `kwp-productivity-*` | `kwp-productivity-collaboration.md` |
| `kwp-sales-*` | `kwp-sales.md` |
| `kwp-slack-*` | `kwp-productivity-collaboration.md` |
| `kwp-sync` | `kwp-productivity-collaboration.md` |

## Keyword Rules (for skills without a matching prefix)

These rules apply when no prefix rule matches. Check skill name or description for keywords.

| Keywords in Name/Description | Target Guide File | Category |
|------------------------------|-------------------|----------|
| `review`, `simplify`, `diagnose`, `refactor`, `codebase`, `problem-definition` | `01-code-review-pipeline.md` | 코드 리뷰 파이프라인 |
| `backend`, `frontend`, `db-expert` | `02-development-experts.md` | 개발 전문가 |
| `fsd`, `overlay`, `layout` | `03-frontend-patterns.md` | 프론트엔드 패턴 |
| `test`, `qa`, `e2e`, `ci-quality` | `04-testing.md` | 테스팅 |
| `devops`, `infra`, `local-dev`, `service-health`, `sre`, `incident` | `05-devops-infrastructure.md` | DevOps & 인프라 |
| `security`, `compliance`, `dependency-auditor`, `semantic-guard` | `06-security-compliance.md` | 보안 & 컴플라이언스 |
| `commit`, `git`, `pr-review`, `release`, `ship`, `eod`, `morning`, `sod` | `07-git-github.md` | Git & GitHub |
| `design`, `ux-expert`, `ui-suite`, `visual` | `08-design-ux.md` | 디자인 & UX |
| `docs`, `technical-writer`, `notion`, `paper`, `meeting`, `onboarding`, `alphaxiv` | `09-documentation.md` | 문서화 & 지식 |
| `prompt`, `eval`, `skill-optimizer`, `plans`, `presentation`, `ai-quality`, `skill-seekers`, `full-stack-planner` | `11-ai-prompt-skills.md` | AI & 프롬프트 |
| `mission-control`, `critical-review`, `skill-composer`, `workflow-miner`, `intent-alignment` | `12-orchestration.md` | 오케스트레이션 |
| `i18n`, `performance-profiler` | `13-i18n-performance.md` | 국제화 & 성능 |
| `notebooklm` | `20-notebooklm.md` | NotebookLM |
| `stock`, `daily-stock`, `weekly-stock`, `stock-csv`, `today`, `ai-workflow` | `19-stock-analytics-pipeline.md` | 주식 분석 파이프라인 |
| `executive-briefing` | `28-role-based-analysis.md` | 역할 기반 분석 |
| `google-daily`, `calendar`, `gmail` | `16-gws-google-workspace.md` | Google Workspace |

## Fallback: Utilities

If no prefix or keyword rule matches, the skill goes to `14-utilities.md` (유틸리티).

## New Category Threshold

If 3+ undocumented skills share a common prefix not in the mapping above, propose creating a new guide file instead of dumping into utilities. Ask the user to confirm the new category name.
