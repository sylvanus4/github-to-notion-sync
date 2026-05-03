---
name: doc-lifecycle-auditor
description: >-
  Audit document lifecycle ground rules compliance across Notion and GitHub
  repos: check metadata presence, ownership assignment, path conventions, SSoT
  branch setup, architecture docs, deletion of orphaned docs, and common
  format adoption. Based on the "Document Lifecycle Ground Rules Setup
  Meeting" decisions. Korean triggers: "문서 생애주기 점검", "문서 관리 점검", "그라운드 룰 점검",
  "문서 오너쉽 점검", "문서 메타데이터 점검", "docs path 컨벤션 점검", "문서 삭제 점검", "문서 라이프사이클 감사".
  English triggers: "doc lifecycle audit", "document governance check",
  "doc-lifecycle-auditor", "ground rule compliance", "document ownership
  audit". Do NOT use for document quality scoring (use doc-quality-gate). Do
  NOT use for cross-domain sync checking (use cross-domain-sync-checker). Do
  NOT use for PRD content review (use doc-quality-gate or spec-quality-gate).
---

# Document Lifecycle Auditor

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Purpose

Audit compliance with the **Document Lifecycle Ground Rules** established in the
setup meeting. Checks whether agreed-upon governance practices have been
implemented across Notion workspaces and GitHub repositories.

This is NOT a document quality scorer — it checks **governance infrastructure**:
metadata fields, ownership, path conventions, SSoT branch setup, architecture
docs existence, deletion progress, and common format templates.

## Ground Rules Reference

The audit checks against the following agreed rules from the meeting.
See [references/ground-rules.md](references/ground-rules.md) for the canonical list.

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--scope` | No | `full` \| `notion` \| `github` \| `summary`. Default: `full` |
| `--repos` | No | Comma-separated GitHub repo paths or slugs to audit. Default: detect from workspace |
| `--notion-root` | No | Notion page ID or URL for the ai-platform root. Default: auto-discover |
| `--notify` | No | Slack channel for summary posting |
| `--output` | No | Report file path. Default: `output/doc-lifecycle-audit/{date}-audit-report.md` |

## Audit Checklist (7 Categories, 20 Items)

### Category 1: Common Ground Rules

| # | Check Item | How to Verify | Pass Criteria |
|---|-----------|---------------|---------------|
| 1.1 | Notion vs GitHub role separation defined | Search for a written policy or README section explaining which docs go where | Document exists stating separation rules |
| 1.2 | Weekly Friday 10:00-10:30 doc management slot | Check team calendar or Notion/Slack for recurring event | Recurring calendar event or documented schedule exists |
| 1.3 | Ownership assignment meetings held | Check Notion/Slack for meeting records about doc ownership review | At least 1 ownership review meeting logged |
| 1.4 | Notification bot configured | Check Slack for active notification bot (assigned to 이상민) | Bot exists and posts notifications |
| 1.5 | All documents have designated owners | Sample Notion pages and GitHub docs for ownership fields | >= 80% of sampled docs have an owner |
| 1.6 | Orphaned/unnecessary docs deleted | Check for deletion activity in Notion audit log or git history | Evidence of deletion rounds performed |

### Category 2: Notion Metadata

| # | Check Item | How to Verify | Pass Criteria |
|---|-----------|---------------|---------------|
| 2.1 | Lifecycle metadata fields present | Sample Notion pages for basic metadata (status, owner, created, updated) | >= 70% of sampled pages have metadata |
| 2.2 | Reference format followed | Compare against reference page structure | Metadata fields present (exact format not required per agreement) |
| 2.3 | Single ai-platform path used | Check Notion workspace for duplicate ai-platform paths | Only one ai-platform root path exists |

### Category 3: Notion Architecture Docs

| # | Check Item | How to Verify | Pass Criteria |
|---|-----------|---------------|---------------|
| 3.1 | Architecture docs exist in Notion | Search Notion for architecture documentation | At least 1 architecture doc per active domain |
| 3.2 | Domain-owner architecture diagrams shared | Check for architecture pages created by domain owners | At least 1 domain has architecture shared |

### Category 4: GitHub Docs Path Convention

| # | Check Item | How to Verify | Pass Criteria |
|---|-----------|---------------|---------------|
| 4.1 | Frontend: project-style at root | Check frontend repos for docs structure | Frontend docs at project root level |
| 4.2 | Backend: docs inside project | Check backend repos for `docs/` directory | Backend repos have `docs/` directory |
| 4.3 | Path convention documented | Search for README or CONTRIBUTING section about docs paths | Written convention exists |

### Category 5: GitHub README & Structure

| # | Check Item | How to Verify | Pass Criteria |
|---|-----------|---------------|---------------|
| 5.1 | Directory structure in README | Check README files for structural documentation | README describes project structure |
| 5.2 | SSoT branch designated | Check repo settings or docs for designated SSoT branch | SSoT branch (dev/main/head) documented |

### Category 6: Deletion & Cleanup

| # | Check Item | How to Verify | Pass Criteria |
|---|-----------|---------------|---------------|
| 6.1 | Initial deletion round completed | Check git history or Notion for bulk cleanup evidence | At least 1 cleanup round logged |
| 6.2 | Deletion criteria established | Search for documented deletion criteria per owner | Written criteria exist or owners confirmed |

### Category 7: Future Action Items (Tracking)

| # | Check Item | How to Verify | Pass Criteria |
|---|-----------|---------------|---------------|
| 7.1 | Common format templates available | Search for PRD/One-pager/ADR templates in Notion or repo | Templates exist (even draft) |
| 7.2 | LLM benchmark discussion scheduled | Check calendar or backlog for planned discussion | Tracked as future item |

## Workflow

### Phase 1: Discovery

1. Identify target repos from workspace or `--repos` parameter
2. Discover Notion ai-platform root page
3. Build inventory of docs to sample

### Phase 2: Notion Audit

For Notion scope (`--scope full` or `--scope notion`):

1. **Metadata scan**: Sample 10-20 Notion pages under ai-platform root.
   For each page, check for presence of:
   - Owner/담당자 field
   - Status field (draft/review/published/archived)
   - Created date
   - Last updated date
2. **Path audit**: Verify single ai-platform root path exists
3. **Architecture docs**: Search for architecture-related pages per domain
4. **Ownership coverage**: Count pages with vs without designated owners

Use Notion MCP tools (`notion_search`, `notion_retrieve_page`) for scanning.

### Phase 3: GitHub Audit

For GitHub scope (`--scope full` or `--scope github`):

1. **Path convention check**:
   - For frontend repos: verify docs at root level
   - For backend repos: verify `docs/` directory exists
2. **README structure check**: Read README for directory structure documentation
3. **SSoT branch**: Check branch naming and documentation
4. **Deletion evidence**: Scan git log for bulk doc cleanup commits
5. **Convention docs**: Search CONTRIBUTING.md or README for docs path rules

Use GitHub MCP or local filesystem + `gh` CLI.

### Phase 4: Common Items Audit

1. **Calendar/schedule**: Search for Friday doc management recurring event
2. **Bot setup**: Check Slack for notification bot
3. **Meeting records**: Search for ownership review meeting notes
4. **Templates**: Search for PRD/ADR/One-pager templates

### Phase 5: Scoring & Report

#### Scoring

Each check item is scored:

| Status | Score | Meaning |
|--------|-------|---------|
| PASS | 1.0 | Fully implemented |
| PARTIAL | 0.5 | Started but incomplete |
| FAIL | 0.0 | Not yet implemented |
| N/A | — | Not applicable to this repo/scope |
| SKIP | — | Could not verify (access issue) |

**Category score** = average of item scores within category (excluding N/A and SKIP).

**Overall compliance** = weighted average of category scores:

| Category | Weight |
|----------|--------|
| 1. Common Ground Rules | 25% |
| 2. Notion Metadata | 15% |
| 3. Notion Architecture | 10% |
| 4. GitHub Docs Path | 15% |
| 5. GitHub README/Structure | 15% |
| 6. Deletion & Cleanup | 10% |
| 7. Future Action Items | 10% |

#### Compliance grades

| Grade | Range | Meaning |
|-------|-------|---------|
| A | 80-100% | Ground rules well-established |
| B | 60-79% | Good progress, gaps remain |
| C | 40-59% | Significant work needed |
| D | 0-39% | Early stage, most items pending |

### Phase 6: Output

Generate Korean report with these sections:

1. **요약**: Overall compliance score, grade, date, scope
2. **카테고리별 결과**: Score per category with item-level details
3. **미완료 항목**: Prioritized list of FAIL/PARTIAL items with recommended actions
4. **완료 항목**: List of PASS items (evidence of progress)
5. **다음 단계**: Recommended priority order for remaining work
6. **변경 이력**: Comparison with previous audit if exists

### Phase 7: Distribution (Optional)

- **Notion**: Publish report via `md-to-notion` if requested
- **Slack**: Post summary to specified channel with details in thread

## Skill Chain

| Step | Skill / Tool | Purpose |
|------|-------------|---------|
| 1 | Notion MCP | Scan workspace pages for metadata and structure |
| 2 | GitHub MCP / `gh` CLI | Scan repos for path conventions and README |
| 3 | Slack MCP | Check for bot setup; post results |
| 4 | (self) | Score and report |
| 5 | `md-to-notion` | Publish report (optional) |
| 6 | Slack MCP | Notify team (optional) |

## Comparison with Related Skills

| Skill | Difference |
|-------|-----------|
| `doc-quality-gate` | Scores individual document content quality; this skill audits governance infrastructure |
| `cross-domain-sync-checker` | Checks sync between PRD/design/code/policy; this skill checks organizational compliance |
| `feature-coverage-matrix` | Tracks feature implementation across pipeline stages; this skill tracks governance setup |
| `release-readiness-gate` | Pre-release go/no-go; this skill is ongoing governance health check |

## Error Handling

| Situation | Action |
|-----------|--------|
| Notion MCP unavailable | Skip Notion checks; mark as SKIP; recommend manual review |
| GitHub repo not found | Skip that repo; report which repos were checked |
| No previous audit exists | Skip comparison; establish baseline |
| Permission denied on pages | Mark affected items as SKIP with reason |
| Too many Notion pages (>100) | Sample random 20; note sampling in report |

## Examples

### Example 1: Full audit

```
User: "문서 생애주기 그라운드 룰 점검해줘"
```

Actions: Scan Notion ai-platform → Scan all repos → Check common items →
Score 20 items → Generate Korean report → Post to Slack.

### Example 2: GitHub only

```
User: "깃헙 문서 컨벤션 지켜지고 있는지 확인해줘"
```

Actions: `--scope github` → Check path conventions, README, SSoT branch →
Report on categories 4-5.

### Example 3: Progress tracking

```
User: "지난주 대비 문서 관리 진행 상황 확인"
```

Actions: Full audit → Compare with previous `output/doc-lifecycle-audit/` report →
Highlight changes in compliance scores.
