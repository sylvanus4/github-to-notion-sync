---
name: portfolio-report-generator
description: >-
  Generate cross-project portfolio reports aggregating weekly status from all
  managed projects into an executive view with project health, blockers, and
  resource allocation. Use when the user asks to "portfolio report",
  "cross-project summary", "포트폴리오 리포트", "프로젝트 전체 현황",
  "portfolio-report-generator", or needs a unified view across multiple
  repositories. Do NOT use for single-project weekly reports (use
  weekly-status-report), daily activity digests (use github-sprint-digest),
  or release pipeline (use release-commander).
metadata:
  version: "1.0.0"
  category: "execution"
  author: "thaki"
---
# Portfolio Report Generator

Cross-project executive portfolio report: aggregate status from all managed projects into a unified health dashboard.

## When to Use

- Weekly executive reporting across all managed projects
- Sprint retrospectives spanning multiple repositories
- Resource allocation reviews
- Stakeholder presentations on overall program health

## Managed Projects

| Project | Repository | Type |
|---------|-----------|------|
| AI Platform WebUI | ThakiCloud/ai-platform-webui | Main platform |
| TKAI Deploy | ThakiCloud/tkai-deploy | Deployment tooling |
| TKAI Agents | ThakiCloud/tkai-agents | Agent framework |
| Business Automation | ThakiCloud/thaki-business-automation | Business team tools |
| Research | ThakiCloud/research | R&D projects |

## Workflow

### Step 1: Collect Per-Project Data

For each managed project, gather weekly metrics:

```bash
for repo in ai-platform-webui tkai-deploy tkai-agents thaki-business-automation research; do
  gh issue list --repo ThakiCloud/$repo --state all --json number,state,labels,closedAt \
    --search "updated:>=$(date -v-7d +%Y-%m-%d)"
  gh pr list --repo ThakiCloud/$repo --state all --json number,state,mergedAt \
    --search "updated:>=$(date -v-7d +%Y-%m-%d)"
done
```

### Step 2: Calculate Health Scores

Per-project health score (0-100) based on:

| Metric | Weight | Scoring |
|--------|--------|---------|
| Sprint completion | 30% | story points completed / planned |
| PR cycle time | 20% | < 24h = 100, < 48h = 70, > 72h = 30 |
| Issue resolution | 20% | closed / (opened + carried over) |
| Blocker count | 15% | 0 = 100, 1 = 70, 2+ = 30 |
| Test pass rate | 15% | From CI results |

Overall health: 90-100 = Green, 70-89 = Yellow, < 70 = Red.

### Step 3: Identify Cross-Project Dependencies

Detect cross-project blockers:
- Issues mentioning other project repos
- PRs with cross-repo dependencies
- Shared component version conflicts

### Step 4: Generate Portfolio Report

```markdown
# 포트폴리오 리포트 — <YYYY-MM-DD> ~ <YYYY-MM-DD>

## 전체 현황

| 프로젝트 | 건강도 | 스프린트 진행률 | 블로커 | PR 사이클 |
|---------|--------|--------------|--------|----------|
| AI Platform | 🟢 92 | 85% (17/20 SP) | 0 | 6h avg |
| TKAI Deploy | 🟡 75 | 70% (7/10 SP) | 1 | 18h avg |
| TKAI Agents | 🟢 88 | 90% (9/10 SP) | 0 | 8h avg |
| Business Auto | 🟢 95 | 100% (5/5 SP) | 0 | 4h avg |
| Research | 🟡 72 | 60% (3/5 SP) | 2 | 36h avg |

## 주요 성과
1. AI Platform: 사용자 인증 시스템 완료 (#38, #42, #45)
2. TKAI Agents: Agent SDK v2 릴리즈
3. Business Auto: 세일즈 파이프라인 자동화 배포

## 크로스-프로젝트 이슈
- ⚠️ TKAI Deploy #89 블록됨: AI Platform API v2 마이그레이션 대기
- ⚠️ Research #34: TKAI Agents SDK 의존성 업데이트 필요

## 리소스 현황
| 팀원 | 주 프로젝트 | 기여 프로젝트 | 이번 주 커밋 |
|------|-----------|-------------|------------|
| @dev1 | AI Platform | TKAI Deploy | 23 |
| @dev2 | TKAI Agents | Research | 18 |

## 다음 주 핵심 목표
1. AI Platform: API v2 마이그레이션 착수
2. TKAI Deploy: 블로커 해소 후 CD 파이프라인 완료
3. Research: 실험 결과 정리 및 논문 초안
```

### Step 5: Generate .docx

Use `anthropic-docx` to produce formatted executive document.

### Step 6: Distribute

- **Notion**: Publish to portfolio reports parent page via `md-to-notion`
- **Slack**: Post summary to `#효정-할일` with health scores
- **Google Drive**: Upload .docx via `gws-drive`

## Output

```
Portfolio Report Generated
==========================
Period: 2026-03-13 ~ 2026-03-19
Projects: 5

Health Summary:
  🟢 Green: 3 projects (AI Platform, TKAI Agents, Business Auto)
  🟡 Yellow: 2 projects (TKAI Deploy, Research)
  🔴 Red: 0 projects

Cross-project blockers: 2
Resource utilization: 85%

Outputs:
- DOCX: output/reports/portfolio-2026-W12.docx
- Notion: <page-url>
- Slack: Posted to #효정-할일
```

## Error Handling

| Error | Action |
|-------|--------|
| Project registry (managed projects list) not found | Use default registry from skill; warn user; allow override via config path |
| GitHub API rate limit for multi-repo fetch | Throttle requests; retry with backoff; report partial data if limit persists |
| DOCX generation fails (anthropic-docx error) | Fall back to markdown output; log error; save report as .md to output path |
| Notion upload fails (API error or auth) | Skip Notion step; complete DOCX and Slack; report Notion failure to user |
| No data for reporting period (all repos empty) | Generate report with "No activity" placeholders; note date range; suggest widening period |

## Examples

### Example 1: Weekly portfolio review
User says: "Generate portfolio report"
Actions:
1. Collect data from all 5 projects
2. Calculate health scores
3. Identify cross-project dependencies
4. Generate Korean report
5. Distribute to all channels
Result: Executive portfolio view across all projects

### Example 2: Specific project deep-dive
User says: "Why is TKAI Deploy yellow?"
Actions:
1. Pull detailed metrics for TKAI Deploy
2. Analyze specific blockers and delays
3. Show trend (was green last week)
4. Suggest remediation actions
Result: Project-specific drill-down with action items
