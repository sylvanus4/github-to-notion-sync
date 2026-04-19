---
name: rr-pm-scrum-master
version: 1.0.0
description: >-
  Role Replacement Case Study: PM / Scrum Master — unified sprint lifecycle from
  meeting analysis through retro-to-issues, with adversarial critique and GitHub
  Project integration. Thin harness composing meeting-digest, sprint-retro-to-issues,
  sprint-orchestrator, doc-quality-gate, commit-to-issue, and pm-execution into a
  single scrum-master role pipeline with MemKraft-powered decision memory, adversarial
  quality gates, and automated GitHub Project field management.
tags: [role-replacement, harness, pm, sprint, scrum]
triggers:
  - rr-pm-scrum-master
  - scrum master replacement
  - PM automation
  - sprint lifecycle automation
  - 스크럼 마스터 대체
  - PM 역할 자동화
  - 스프린트 라이프사이클
  - 회의에서 이슈까지
do_not_use:
  - Simple meeting notes without PM analysis (use pm-execution summarize-meeting)
  - General GitHub issue management without meeting context (use commit-to-issue)
  - PRD creation from scratch (use pm-execution create-prd)
  - Single-meeting digest without sprint lifecycle (use meeting-digest)
  - Sprint triage without retro pipeline (use sprint-orchestrator)
  - Code-level issue tracking from commits (use commit-to-issue)
composes:
  - meeting-digest
  - sprint-retro-to-issues
  - sprint-orchestrator
  - doc-quality-gate
  - commit-to-issue
  - pm-execution
  - memkraft
  - ai-context-router
  - github-sprint-digest
---

# Role Replacement: PM / Scrum Master

## What This Skill Replaces

A human PM / Scrum Master who:
- Attends every sprint meeting, retro, and planning session
- Takes structured notes with action items and owners
- Converts retro findings into GitHub issues with proper fields
- Triages incoming issues overnight and assigns priority/owners
- Tracks sprint velocity, completion rates, and blockers
- Maintains the GitHub Project board as single source of truth
- Follows up on overdue action items and escalates blockers
- Remembers past sprint patterns and applies lessons learned

This thin harness orchestrates 6 existing skills into a unified sprint lifecycle
pipeline that runs daily, covering meeting → analysis → issues → triage → tracking.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   rr-pm-scrum-master                        │
│                  (Thin Harness Orchestrator)                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 0: MemKraft Context Pre-load                         │
│  ├── ai-context-router → sprint patterns, team velocity,    │
│  │                        past retro decisions               │
│  │                                                          │
│  Phase 1: Meeting Intake & Analysis                         │
│  ├── meeting-digest → multi-perspective PM analysis         │
│  │   ├── Notion fetch + transcript ingestion                │
│  │   ├── Meeting type classification (sprint/retro/ops)     │
│  │   ├── Parallel PM sub-skill analysis                     │
│  │   ├── Korean summary + action items generation           │
│  │   └── Notion upload + optional Slack/PPTX                │
│  │                                                          │
│  Phase 2: Retro-to-Issues Pipeline                          │
│  ├── sprint-retro-to-issues → structured issue creation     │
│  │   ├── Extract structured action items with owners        │
│  │   ├── Adversarial quality critique (5 dimensions)        │
│  │   ├── Gap detection vs retro topics                      │
│  │   ├── GitHub issue creation with Project #5 fields       │
│  │   └── Korean Slack summary with issue links              │
│  │                                                          │
│  Phase 3: Sprint Board Triage                               │
│  ├── sprint-orchestrator → overnight issue classification   │
│  │   ├── Type classification (bug/feature/enhancement)      │
│  │   ├── Priority assignment (P0-P3)                        │
│  │   ├── Assignee suggestion from CODEOWNERS + blame        │
│  │   ├── GitHub Project field updates                       │
│  │   └── Triage summary to Slack                            │
│  │                                                          │
│  Phase 4: Sprint Health Report                              │
│  ├── github-sprint-digest → development activity summary    │
│  │   ├── Overnight GitHub activity per user                 │
│  │   ├── PR/issue/review/comment aggregation                │
│  │   └── Korean digest to Notion + Slack                    │
│  │                                                          │
│  Phase 5: Quality Gate on Sprint Artifacts                  │
│  ├── doc-quality-gate → 7-dimension document scoring        │
│  │   ├── Score retro report on completeness/consistency     │
│  │   ├── Validate action items coverage vs discussion       │
│  │   └── A-D grade with pass/fail threshold                 │
│  │                                                          │
│  Phase 6: MemKraft Write-back & Sprint Digest               │
│  ├── memkraft → HOT tier: sprint decisions, velocity        │
│  ├── Slack #효정-할일 → consolidated sprint briefing        │
│  └── decision-router → decision items to #효정-의사결정      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

| Requirement | Check Command | Required By |
|-------------|--------------|-------------|
| `gh` CLI authenticated | `gh auth status` | Phases 2, 3, 4 |
| Notion MCP server | `CallMcpTool(notion, mcp_auth)` | Phase 1 |
| Slack MCP server | Slack tool availability | Phases 1, 2, 3, 6 |
| GitHub Project #5 access | `gh project view 5 --owner ThakiCloud` | Phase 2 |
| MemKraft directories | `ls memory/topics/` | Phases 0, 6 |
| `gbrain` CLI (optional) | `which gbrain` | Phase 1 (entity extraction) |

## Pipeline Output Protocol

All phases persist structured output to disk following the file-first principle.

### Output Directory

```
outputs/rr-pm-scrum-master/{date}/
├── manifest.json
├── phase-0-context.json
├── phase-1-meeting/              # meeting-digest output dir
│   ├── manifest.json
│   ├── phase-1-ingest.json
│   ├── phase-2-classify.json
│   ├── phase-3-pm-analysis.json
│   ├── phase-4-generate.json
│   ├── phase-5-deliver.json
│   ├── summary.md
│   └── action-items.md
├── phase-2-retro-issues/         # sprint-retro-to-issues output dir
│   ├── manifest.json
│   ├── phase-1-collect.json
│   ├── phase-3-extract.json
│   ├── phase-4-critique.json
│   ├── phase-5-issues.json
│   ├── report.md
│   └── action-items.md
├── phase-3-triage.json
├── phase-4-sprint-digest.json
├── phase-5-quality-gate.json
└── phase-6-writeback.json
```

### `manifest.json` Schema

```json
{
  "pipeline": "rr-pm-scrum-master",
  "date": "YYYY-MM-DD",
  "started_at": "ISO-8601",
  "completed_at": null,
  "phases": [],
  "overall_status": "running",
  "warnings": [],
  "input": {
    "notion_url": "optional meeting URL",
    "mode": "full | meeting-only | triage-only | retro-only"
  }
}
```

### Subagent Return Contract

Any Task/subagent invoked MUST return only:

```json
{
  "status": "success | skipped | failed",
  "file": "path to written artifact or null",
  "summary": "one short paragraph"
}
```

The parent reads content from `file`, never from the subagent's chat transcript.

## Execution Modes

| Mode | Phases | Trigger |
|------|--------|---------|
| `full` | 0 → 1 → 2 → 3 → 4 → 5 → 6 | Default: Notion retro URL provided |
| `meeting-only` | 0 → 1 → 5 → 6 | `--mode meeting-only`: any meeting without retro context |
| `retro-only` | 0 → 2 → 5 → 6 | `--mode retro-only`: retro already ingested, skip meeting-digest |
| `triage-only` | 0 → 3 → 4 → 6 | `--mode triage-only`: overnight triage without meeting |

## Phase 0: MemKraft Context Pre-load

**Goal**: Load sprint-relevant context from personal memory before any analysis.

### Steps

1. Query `ai-context-router` for sprint context:
   - Past sprint velocity and completion rates
   - Recurring blockers and their resolutions
   - Team member strengths and assignment patterns
   - Prior retro decisions and whether they were implemented
   - Active sprint goals and OKR alignment

2. Query for meeting-specific context (if Notion URL provided):
   - Previous meetings with same participants
   - Unresolved action items from prior sessions
   - Related decisions from `#효정-의사결정`

3. Write context to `phase-0-context.json`:
   ```json
   {
     "phase": 0,
     "label": "context",
     "status": "success",
     "sprint_velocity": {"last_3": [12, 15, 14], "trend": "stable"},
     "recurring_blockers": ["CI flakiness", "cross-team API deps"],
     "unresolved_actions": [{"from": "2026-04-08", "item": "..."}],
     "team_patterns": {"frontend": "혜림", "backend": "재훈님"},
     "prior_retro_decisions": [{"decision": "...", "implemented": true}]
   }
   ```

4. Update `manifest.json`.

### Error Recovery

If MemKraft is unavailable, proceed with empty context and add warning to manifest.

---

## Phase 1: Meeting Intake & Analysis

**Goal**: Run the full meeting-digest pipeline on the provided meeting content.

### Steps

1. Read `phase-0-context.json` for prior context.

2. Delegate to `meeting-digest` skill with the following parameters:
   - Input: Notion URL, file path, or raw transcript
   - Output directory: `outputs/rr-pm-scrum-master/{date}/phase-1-meeting/`
   - Flags: `--slack-channel C0AA8NT4T8T` (if Slack posting desired)
   - Context injection: Pass MemKraft context as supplementary input so the analysis
     can reference past decisions and unresolved items.

3. The meeting-digest pipeline runs its internal 6 phases:
   - Phase 1: Ingest (Notion fetch + normalize)
   - Phase 2: Classify (detect meeting type: sprint/retro/discovery/strategy/operational)
   - Phase 3: PM Analysis (parallel subagents for multi-perspective analysis)
   - Phase 4: Generate (Korean summary.md + action-items.md)
   - Phase 5: Deliver (Notion upload, optional Slack/PPTX)
   - Phase 6: gbrain entity extraction (non-blocking)

4. Verify meeting-digest manifest shows `overall_status: "success"`.

5. Read the generated `summary.md` and `action-items.md` to determine if meeting
   type is `sprint` or contains retro content → decide whether to proceed to Phase 2.

6. Update parent `manifest.json` with Phase 1 results.

### Decision Gate

| Meeting Type | Next Phase |
|-------------|------------|
| `sprint` with retro content | → Phase 2 (retro-to-issues) |
| `sprint` without retro | → Phase 3 (triage only) |
| `operational` / `strategy` / `discovery` | → Phase 5 (quality gate on digest) |

### Skip Condition

If `--mode triage-only`, skip Phase 1 entirely.

---

## Phase 2: Retro-to-Issues Pipeline

**Goal**: Convert sprint retrospective findings into tracked GitHub issues.

### Steps

1. Read Phase 1 outputs (specifically `phase-3-pm-analysis.json` and `action-items.md`).

2. Delegate to `sprint-retro-to-issues` skill:
   - Input: The Notion URL (for direct collection) or Phase 1 collected content
   - Output directory: `outputs/rr-pm-scrum-master/{date}/phase-2-retro-issues/`
   - MemKraft context injection: Pass `phase-0-context.json` data so the extraction
     can flag items that duplicate unresolved actions from prior sprints

3. The retro-to-issues pipeline runs its internal 6 phases:
   - Phase 1: Collect (Notion fetch — may reuse Phase 1 data if same source)
   - Phase 2: Analyze (multi-perspective PM analysis)
   - Phase 3: Extract (structured action items with owners, sizes, priorities)
   - Phase 4: Critique (5-dimension adversarial quality gate)
   - Phase 5: Create Issues (GitHub issues + Project #5 field setup)
   - Phase 6: Report (Korean summary + Slack posting)

4. **MemKraft-enhanced critique** (added by this harness):
   - Cross-reference extracted items against `phase-0-context.json.unresolved_actions`
   - Flag items that are repeat appearances from prior retros (pattern detection)
   - Boost priority for items that appeared 2+ times without resolution
   - Add historical context to issue descriptions: "이 항목은 N번째 스프린트 회고에서
     반복 등장합니다. 이전 결정: {prior_decision}"

5. Verify retro-to-issues manifest shows `overall_status: "success"`.

6. Update parent `manifest.json` with Phase 2 results.

### Skip Condition

If `--mode meeting-only` or `--mode triage-only`, skip Phase 2.
If Phase 1 classified meeting as non-sprint, skip Phase 2.

---

## Phase 3: Sprint Board Triage

**Goal**: Auto-classify and prioritize incoming issues/PRs on the project board.

### Steps

1. Delegate to `sprint-orchestrator` skill:
   - Scope: All untriaged issues/PRs since last run
   - Target: ThakiCloud repositories (ai-platform-strategy primary)
   - Output: `phase-3-triage.json`

2. The sprint-orchestrator runs:
   - Fetch new items via `gh issue list` / `gh pr list`
   - Classify by type (bug/feature/enhancement/chore/security)
   - Assign priority (P0-P3)
   - Suggest assignees from CODEOWNERS + git blame + workload balance
   - Update GitHub Project fields (Status, Priority, Size, Sprint, Estimate)
   - Post triage summary to Slack

3. **MemKraft-enhanced assignment** (added by this harness):
   - Use `phase-0-context.json.team_patterns` for assignment suggestions
   - Cross-reference with ongoing sprint velocity data
   - Avoid overloading team members who are already at capacity

4. Write triage summary to `phase-3-triage.json`:
   ```json
   {
     "phase": 3,
     "label": "triage",
     "status": "success",
     "items_triaged": 12,
     "by_priority": {"P0": 1, "P1": 3, "P2": 5, "P3": 3},
     "auto_assigned": 8,
     "needs_manual": 4
   }
   ```

5. Update parent `manifest.json`.

### Skip Condition

If `--mode meeting-only` or `--mode retro-only`, skip Phase 3.

---

## Phase 4: Sprint Health Digest

**Goal**: Aggregate overnight development activity into a sprint health report.

### Steps

1. Delegate to `github-sprint-digest` skill:
   - Scope: All managed repositories
   - Users: Team members from Owner-to-GitHub Mapping
   - Output: Notion sub-pages + Slack digest

2. Capture results in `phase-4-sprint-digest.json`:
   ```json
   {
     "phase": 4,
     "label": "sprint-digest",
     "status": "success",
     "commits": 23,
     "prs_merged": 5,
     "prs_open": 3,
     "reviews_completed": 8,
     "active_contributors": 6
   }
   ```

3. Update parent `manifest.json`.

### Skip Condition

If `--mode meeting-only` or `--mode retro-only`, skip Phase 4.

---

## Phase 5: Quality Gate on Sprint Artifacts

**Goal**: Validate the quality of generated meeting summaries and retro reports.

### Steps

1. Identify artifacts to validate:
   - If Phase 1 ran: validate `summary.md` and `action-items.md`
   - If Phase 2 ran: validate `report.md` and the generated issues

2. Delegate to `doc-quality-gate` skill for each document:
   - Score on 7 dimensions: required sections, state coverage, edge cases,
     policy alignment, terminology consistency, API alignment, design references
   - Threshold: B grade (70+ score) = PASS

3. Write quality results to `phase-5-quality-gate.json`:
   ```json
   {
     "phase": 5,
     "label": "quality-gate",
     "status": "success",
     "documents_scored": 2,
     "results": [
       {"document": "summary.md", "score": 82, "grade": "B", "verdict": "PASS"},
       {"document": "report.md", "score": 91, "grade": "A", "verdict": "PASS"}
     ],
     "issues_found": ["Missing stakeholder section in summary"],
     "overall_verdict": "PASS"
   }
   ```

4. If any document scores below B (FAIL):
   - Log specific issues in warnings
   - Do NOT block the pipeline — these are advisory
   - Include improvement suggestions in the Phase 6 Slack digest

5. Update parent `manifest.json`.

---

## Phase 6: MemKraft Write-back & Sprint Digest

**Goal**: Persist sprint decisions to memory and post consolidated briefing.

### Steps

1. **MemKraft HOT tier write-back**:
   - Sprint decisions made during the meeting
   - New team velocity data point
   - Issue creation outcomes (count, priorities, assignees)
   - Quality gate scores for trend tracking
   - Recurring items flagged in Phase 2 critique

2. **MemKraft WARM tier** (if patterns detected):
   - Team member assignment effectiveness (who completes which types)
   - Retro item completion rates by category
   - Sprint planning accuracy (estimated vs actual)

3. **Consolidated Slack Briefing** to `#효정-할일` (`C0AA8NT4T8T`):

   **Main message**:
   ```
   📋 스프린트 라이프사이클 — {date} 완료

   🔄 모드: {mode}
   📊 Phase 결과:
   • 회의 분석: {meeting type} — {action_item_count}개 액션 아이템
   • 이슈 생성: {issue_count}개 (P0: {n}, P1: {n}, P2: {n})
   • 트리아지: {triaged_count}개 분류 완료
   • 품질 게이트: {grade} ({score}/100)
   ```

   **Thread reply 1** — Issues created:
   ```
   📌 생성된 이슈:
   • #{issue_number}: {title} (P{n}, {size}) → @{assignee}
   • ...

   🔄 반복 항목 (이전 회고에서도 등장):
   • #{issue_number}: {title} — {n}번째 등장
   ```

   **Thread reply 2** — Sprint health:
   ```
   🏃 스프린트 건강:
   • 커밋: {n}개 | PR 머지: {n}개 | 리뷰: {n}개
   • 활성 기여자: {n}명
   • 속도 추세: {trend} (최근 3스프린트: {velocity_array})
   ```

4. **Decision routing**: If any P0 items were created or velocity dropped >20%,
   route to `#효정-의사결정` via `decision-router`.

5. Write `phase-6-writeback.json` and update `manifest.json` with `completed_at`
   and `overall_status`.

---

## Memory Configuration

### HOT Tier (session-critical, auto-loaded by Phase 0)

| Key | Content | Source |
|-----|---------|--------|
| `sprint.current_velocity` | Story points completed this sprint | Phase 4 digest |
| `sprint.active_blockers` | Current blockers with owners | Phase 3 triage |
| `sprint.last_retro_decisions` | Decisions from most recent retro | Phase 2 critique |
| `sprint.recurring_items` | Items appearing 2+ times in retros | Phase 2 critique |
| `sprint.team_capacity` | Per-member current workload | Phase 3 triage |

### WARM Tier (cross-session patterns, decayed weekly)

| Key | Content | Source |
|-----|---------|--------|
| `sprint.velocity_history` | Last 10 sprint velocity data points | Phase 4 over time |
| `sprint.retro_completion_rate` | % of retro items completed by next retro | Phase 2 tracking |
| `sprint.assignment_effectiveness` | Which assignees complete which issue types | Phase 3 + outcomes |
| `sprint.quality_trend` | Doc quality gate scores over time | Phase 5 over time |
| `sprint.planning_accuracy` | Estimated vs actual story points | Phase 4 vs plan |

### Knowledge Tier (persistent KB)

| Topic | Content | Source |
|-------|---------|--------|
| `engineering-standards` | Sprint process policies and conventions | Team agreements |
| `product-strategy` | Current OKRs and sprint goals | PM documentation |

---

## Error Recovery

| Phase | Failure | Recovery |
|-------|---------|----------|
| Phase 0 (Context) | MemKraft unavailable | Proceed with empty context; add warning |
| Phase 1 (Meeting) | Notion MCP auth fails | Check credentials; abort if unreachable |
| Phase 1 (Meeting) | Empty transcript | Continue with summary content only |
| Phase 2 (Retro) | GitHub auth fails | Check `gh auth status`; abort Phase 2, continue to Phase 3 |
| Phase 2 (Retro) | Project field setting fails | Issue is created; log warning for manual field setup |
| Phase 3 (Triage) | No new items | Post empty triage summary; continue normally |
| Phase 4 (Digest) | GitHub API rate limit | Wait and retry with exponential backoff (max 3 attempts) |
| Phase 5 (Quality) | Score below threshold | Log advisory warning; do not block pipeline |
| Phase 6 (Write-back) | Slack post fails | Save briefing to local file; retry once |

---

## Security & Governance Rules

1. **No auto-assignment of P0 items** — P0 items are flagged for human review
   in the Slack digest; assignment is suggested, not forced.
2. **Issue creation is auditable** — every created issue links back to the retro
   discussion via `source_quote` in the issue body.
3. **Project field IDs are org-specific** — IDs in Phase 2 are for ThakiCloud
   Project #5 only; verify before running on other projects.
4. **Sprint iteration IDs rotate** — always query dynamically, never hardcode.
5. **No PII in issue bodies** — meeting content is summarized, not verbatim.
   Personal notes from retro tables are paraphrased into actionable items.

---

## Honest Reporting

- Report outcomes faithfully — never claim all phases passed when any failed
- Never suppress errors, partial results, or skipped phases
- Surface unexpected findings even if they complicate the narrative
- If a phase produces no actionable output, say so explicitly

## Coordinator Synthesis

- Do not reconstruct phase outputs from chat context — always read from persisted files
- Each phase dispatch includes a purpose statement explaining the expected transformation
- File paths and line numbers must be specific, not inferred
- Never delegate with vague instructions like "analyze this" — provide concrete specs

## Subagent Contract

Every subagent dispatch MUST include:
1. **Purpose statement** — one sentence explaining why this subagent exists
2. **Absolute file paths** — all input/output paths as absolute paths
3. **Return contract** — subagent must return JSON: `{"status": "ok|error", "file": "<output_path>", "summary": "<1-line>"}`
4. Load-bearing outputs must be written to disk, not passed via chat context

## Operational Runbook

### Daily Morning Run (Recommended)

```
1. morning-ship completes git sync
2. rr-pm-scrum-master --mode triage-only
   → Phase 0: Load sprint context
   → Phase 3: Triage overnight issues
   → Phase 4: Sprint health digest
   → Phase 6: Post briefing to Slack
```

### After Sprint Retro Meeting

```
1. Receive Notion retro URL from meeting
2. rr-pm-scrum-master {notion-url}
   → Phase 0: Load sprint context + prior retro decisions
   → Phase 1: Full meeting analysis with PM sub-skills
   → Phase 2: Extract items, critique, create GitHub issues
   → Phase 5: Quality gate on generated documents
   → Phase 6: Write sprint decisions to MemKraft, post digest
```

### After Any Sprint Meeting (non-retro)

```
1. Receive Notion meeting URL
2. rr-pm-scrum-master --mode meeting-only {notion-url}
   → Phase 0: Load context
   → Phase 1: Meeting analysis + Notion upload
   → Phase 5: Quality gate
   → Phase 6: Write-back + Slack digest
```

---

## Comparison: Human vs Automated Scrum Master

| Dimension | Human PM | rr-pm-scrum-master |
|-----------|----------|-------------------|
| Meeting notes | Manual, inconsistent format | Structured Korean output with PM frameworks |
| Retro → Issues | Manual copy-paste, 30-60 min | Automated with 5-dimension critique, 5 min |
| Issue fields | Often incomplete (missing size/estimate) | ALL 5 fields set on every issue |
| Overnight triage | Next morning, delayed | Automated classification + assignment |
| Pattern detection | Relies on memory | MemKraft tracks recurring items across sprints |
| Quality consistency | Varies by workload | doc-quality-gate enforces minimum B grade |
| Sprint velocity | Manual spreadsheet tracking | Auto-computed from GitHub activity data |
| Decision memory | Notes lost between sprints | MemKraft HOT/WARM tiers persist cross-sprint |
| Stakeholder visibility | Weekly email summary | Real-time Slack threads with issue links |
| Cost | $80K-120K/year salary | Compute cost ~$2-5/run (LLM + MCP calls) |

---

## Examples

### Example 1: Full Sprint Retro Lifecycle

User says: `rr-pm-scrum-master https://notion.so/thakicloud/Sprint-Retro-26-04-S3...`

Actions:
1. Phase 0: Load sprint velocity (avg 14 SP), 2 unresolved items from S2, team patterns
2. Phase 1: meeting-digest classifies as `sprint` retro, runs PM analysis with
   retrospective + test-scenarios sub-skills, generates 12-page Korean summary
3. Phase 2: sprint-retro-to-issues extracts 8 action items, critique flags 1 as
   duplicate of S2 unresolved item (boosted to P1), creates 7 issues on Project #5
4. Phase 5: doc-quality-gate scores summary at 88/100 (A), action items at 79/100 (B)
5. Phase 6: Posts digest with 7 issue links, flags 1 recurring item, velocity trend stable

### Example 2: Morning Triage Only

User says: `rr-pm-scrum-master --mode triage-only`

Actions:
1. Phase 0: Load current sprint capacity and assignment patterns
2. Phase 3: sprint-orchestrator finds 5 new issues, classifies and assigns
3. Phase 4: github-sprint-digest shows 3 PRs merged overnight, 2 reviews pending
4. Phase 6: Posts morning briefing with triage results and sprint health

### Example 3: Non-Retro Sprint Meeting

User says: `rr-pm-scrum-master --mode meeting-only https://notion.so/thakicloud/Sprint-Planning-26-04-S4...`

Actions:
1. Phase 0: Load context
2. Phase 1: meeting-digest classifies as `sprint` (planning), runs core summary +
   sprint-plan PM analysis, generates action items with sprint goal alignment
3. Phase 5: Quality gate validates planning document
4. Phase 6: Posts planning summary, writes sprint goals to MemKraft HOT tier
