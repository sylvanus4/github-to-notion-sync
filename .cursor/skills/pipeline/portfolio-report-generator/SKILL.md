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
  version: "1.1.0"
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
| AI Platform WebUI | ThakiCloud/ai-platform-strategy | Main platform |
| TKAI Deploy | ThakiCloud/tkai-deploy | Deployment tooling |
| TKAI Agents | ThakiCloud/tkai-agents | Agent framework |
| Business Automation | ThakiCloud/thaki-business-automation | Business team tools |
| Research | ThakiCloud/research | R&D projects |

## Configuration

- **`{date}`**: Run date for partitioning outputs (typically report end date or today in `YYYY-MM-DD`).
- **Output root**: `outputs/portfolio-report/{date}/` (create before Step 1).

## Pipeline Output Protocol (File-First)

All multi-phase work MUST persist to disk under `outputs/portfolio-report/{date}/`. Do not rely on in-context memory for handoffs between phases.

### Output layout

| Artifact | Path |
|----------|------|
| Per-phase JSON | `outputs/portfolio-report/{date}/phase-{N}-{label}.json` |
| Run manifest | `outputs/portfolio-report/{date}/manifest.json` |

- **Phase numbering**: N = 1 … 6 matching the workflow steps below (`collect`, `health-scores`, `dependencies`, `report`, `docx`, `distribute`).
- **`manifest.json`**: Single source of truth for which phases completed and where their files live. Append or patch after each phase’s persist step.

### Subagent return contract

When delegating to subagents, require return value **only**:

```json
{ "status": "complete|failed|skipped", "file": "<path to phase JSON>", "summary": "<one-line outcome>" }
```

No large payloads in chat—only paths and short summaries.

### Final aggregation rule

Phases that produce the **portfolio markdown body**, **.docx**, and **Slack/Notion/Drive distribution** MUST read inputs **only** from:

- `outputs/portfolio-report/{date}/manifest.json`
- Prior phase files: `phase-1-collect.json` … `phase-5-docx.json` (as required by the step)

Do **not** reconstruct prior phase results from conversation memory or unstored tool output.

### `manifest.json` schema

```json
{
  "$schema": "portfolio-report-manifest/1.0",
  "date": "YYYY-MM-DD",
  "created_at": "ISO-8601 timestamp",
  "updated_at": "ISO-8601 timestamp",
  "phases": [
    {
      "phase": 1,
      "label": "collect",
      "status": "pending|complete|failed|skipped",
      "file": "outputs/portfolio-report/{date}/phase-1-collect.json",
      "summary": "string",
      "updated_at": "ISO-8601 timestamp"
    }
  ]
}
```

- On initialization, write `phases` with all six entries in `pending` (or omit until first update).
- After each persist step, set that phase to `complete` (or `failed` / `skipped`) and refresh `updated_at`.

### Output Artifacts

| Phase | Label | Output file | Consumes |
| ----- | ----- | ----------- | -------- |
| 1 | collect | `phase-1-collect.json` | GitHub CLI raw per-repo metrics |
| 2 | health-scores | `phase-2-health-scores.json` | `phase-1-collect.json` |
| 3 | dependencies | `phase-3-dependencies.json` | `phase-1-collect.json`, `phase-2-health-scores.json` |
| 4 | report | `phase-4-report.json` (include `markdown_path` or `body` per implementation) | `phase-1-collect.json`, `phase-2-health-scores.json`, `phase-3-dependencies.json` |
| 5 | docx | `phase-5-docx.json` | `phase-4-report.json` |
| 6 | distribute | `phase-6-distribute.json` | `manifest.json`, `phase-5-docx.json`, `phase-4-report.json` |

## Workflow

### Initialization (before Step 1)

1. Resolve `{date}` for this run.
2. Create directory `outputs/portfolio-report/{date}/`.
3. Write initial `manifest.json` with `date`, `created_at`, `updated_at`, and six `phases` entries (labels: `collect`, `health-scores`, `dependencies`, `report`, `docx`, `distribute`; `status` may start as `pending`).

### Step 1: Collect Per-Project Data

For each managed project, gather weekly metrics:

```bash
for repo in ai-platform-strategy tkai-deploy tkai-agents thaki-business-automation research; do
  gh issue list --repo ThakiCloud/$repo --state all --json number,state,labels,closedAt \
    --search "updated:>=$(date -v-7d +%Y-%m-%d)"
  gh pr list --repo ThakiCloud/$repo --state all --json number,state,mergedAt \
    --search "updated:>=$(date -v-7d +%Y-%m-%d)"
done
```

**Persist & manifest**: Write aggregated collection payload to `outputs/portfolio-report/{date}/phase-1-collect.json`. Update `manifest.json`: phase 1 → `complete` (or `failed`), set `file` and `summary`, refresh `updated_at`.

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

**Inputs**: Read **only** from `outputs/portfolio-report/{date}/phase-1-collect.json` (and `manifest.json` for paths if needed).

**Persist & manifest**: Write scores and per-project breakdown to `outputs/portfolio-report/{date}/phase-2-health-scores.json`. Update `manifest.json` for phase 2.

### Step 3: Identify Cross-Project Dependencies

Detect cross-project blockers:
- Issues mentioning other project repos
- PRs with cross-repo dependencies
- Shared component version conflicts

**Inputs**: Read **only** from `outputs/portfolio-report/{date}/phase-1-collect.json` and `outputs/portfolio-report/{date}/phase-2-health-scores.json` on disk (not from prior chat context).

**Persist & manifest**: Write cross-project blocker list and dependency graph data to `outputs/portfolio-report/{date}/phase-3-dependencies.json`. Update `manifest.json` for phase 3.

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

**Inputs**: Assemble the Korean markdown report **only** from `outputs/portfolio-report/{date}/phase-1-collect.json`, `outputs/portfolio-report/{date}/phase-2-health-scores.json`, and `outputs/portfolio-report/{date}/phase-3-dependencies.json`. Optionally write the markdown body to `outputs/portfolio-report/{date}/report.md` and reference it from the phase JSON.

**Persist & manifest**: Write `phase-4-report.json` (must include enough pointers/content for docx: e.g. `markdown_path` or structured sections). Update `manifest.json` for phase 4.

### Step 5: Generate .docx

Use `anthropic-docx` to produce formatted executive document.

**Inputs**: Read **only** from `outputs/portfolio-report/{date}/phase-4-report.json` (and linked `report.md` if used)—not from unstored prior summaries.

**Persist & manifest**: Write `phase-5-docx.json` including absolute or repo-relative path to the generated `.docx`. Update `manifest.json` for phase 5.

### Step 6: Distribute

- **Notion**: Publish to portfolio reports parent page via `md-to-notion`
- **Slack**: Post summary to `#효정-할일` with health scores
- **Google Drive**: Upload .docx via `gws-drive`

**Inputs**: Load channel copy and links **only** from `outputs/portfolio-report/{date}/manifest.json`, `outputs/portfolio-report/{date}/phase-4-report.json` (summary text if needed), and `outputs/portfolio-report/{date}/phase-5-docx.json` (artifact paths). Do not rebuild the executive summary from memory without reading these files.

**Persist & manifest**: Write `phase-6-distribute.json` with Notion URL, Slack message id or timestamp, Drive file id/path as applicable. Mark phase 6 `complete` in `manifest.json` and set final `updated_at`.

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
- Run directory: `outputs/portfolio-report/{date}/` (phase JSON + manifest.json)
- DOCX: path recorded in `phase-5-docx.json` (e.g. `output/reports/portfolio-2026-W12.docx` or under the same date folder per project convention)
- Notion: <page-url> (from `phase-6-distribute.json`)
- Slack: Posted to #효정-할일 (confirmed in `phase-6-distribute.json`)
```

## Error Handling

| Error | Action |
|-------|--------|
| Project registry (managed projects list) not found | Use default registry from skill; warn user; allow override via config path |
| GitHub API rate limit for multi-repo fetch | Throttle requests; retry with backoff; report partial data if limit persists |
| DOCX generation fails (anthropic-docx error) | Fall back to markdown output; log error; save report as .md to output path |
| Notion upload fails (API error or auth) | Skip Notion step; complete DOCX and Slack; report Notion failure to user |
| No data for reporting period (all repos empty) | Generate report with "No activity" placeholders; note date range; suggest widening period |

### Recovery checkpoints

If a step fails, the last successfully written `phase-N-*.json` and `manifest.json` remain valid. Re-run from the failed phase after fixing the issue; do not discard earlier phase files.

## Examples

### Example 1: Weekly portfolio review
User says: "Generate portfolio report"
Actions:
1. Initialize `outputs/portfolio-report/{date}/` and `manifest.json`
2. Collect data from all 5 projects → `phase-1-collect.json`
3. Calculate health scores from file → `phase-2-health-scores.json`
4. Cross-project dependencies from files → `phase-3-dependencies.json`
5. Generate Korean report from phase 1–3 JSON only → `phase-4-report.json`
6. DOCX from `phase-4-report.json` → `phase-5-docx.json`
7. Distribute using manifest + phase 4/5 files → `phase-6-distribute.json`
Result: Executive portfolio view across all projects; full audit trail on disk

### Example 2: Specific project deep-dive
User says: "Why is TKAI Deploy yellow?"
Actions:
1. Pull detailed metrics for TKAI Deploy
2. Analyze specific blockers and delays
3. Show trend (was green last week)
4. Suggest remediation actions
Result: Project-specific drill-down with action items


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
