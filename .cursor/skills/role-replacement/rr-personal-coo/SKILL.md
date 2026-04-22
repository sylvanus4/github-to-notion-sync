---
name: rr-personal-coo
version: 1.0.0
description: >-
  Role Replacement Case Study: Personal COO / 6-Axis Orchestrator — meta-orchestrator
  replacing a dedicated Chief Operating Officer who manually coordinates personal
  productivity (calendar/email), recruitment (job pipeline/interviews), investment
  intelligence (trading/portfolio), continuous learning (papers/KB), side project
  management (multi-repo sprints), and cross-axis executive synthesis (OKR/synergies).
  Thin harness composing axis-dispatcher, axis-life, axis-recruitment, axis-investment,
  axis-learning, axis-sidepm, and axis-gm into a unified COO role pipeline with
  MemKraft-powered executive memory, cross-axis synergy detection, progressive
  automation levels, and consolidated Slack distribution.
tags: [role-replacement, harness, personal, orchestrator, axis, coo, meta]
triggers:
  - rr-personal-coo
  - personal COO replacement
  - 6-axis orchestrator
  - personal operations officer
  - life management automation
  - full axis pipeline
  - 개인 COO 대체
  - 6축 오케스트레이터
  - 개인 운영 자동화
  - 전체 축 파이프라인
  - 일상 운영 총괄
do_not_use:
  - Running individual axes (invoke the specific axis-* skill)
  - Daily pipeline orchestration directly (use daily-am-orchestrator or daily-pm-orchestrator)
  - Single-project coding tasks (use the specific review/frontend/backend skill)
  - Running the today pipeline directly (use today)
  - Google Workspace operations only (use gws-* skills)
  - Single-paper review (use paper-review)
  - Broker operations only (use toss-ops-orchestrator or kis-team)
composes:
  - axis-dispatcher
  - axis-life
  - axis-recruitment
  - axis-investment
  - axis-learning
  - axis-sidepm
  - axis-gm
  - memkraft
  - ai-context-router
  - decision-router
  - visual-explainer
---

# Role Replacement: Personal COO / 6-Axis Orchestrator

## Role Being Replaced

A **Personal Chief Operating Officer** — the human who manually:

1. **Starts the day** by checking calendar, triaging email, planning errands (Axis 6: Life)
2. **Monitors job pipeline** — tracks applications, prepares for interviews, researches target companies (Axis 1: Recruitment)
3. **Runs investment analysis** — syncs market data, screens stocks, evaluates trades, manages broker portfolio (Axis 2: Investment)
4. **Curates learning** — reviews papers, maintains knowledge bases, tracks AI research trends (Axis 3: Learning)
5. **Manages side projects** — syncs repos, triages issues, ships code, runs CI (Axis 5: Side PM)
6. **Synthesizes everything** — detects cross-domain synergies, tracks OKR progress, makes executive decisions (Axis 4: GM)

This skill replaces the manual coordination overhead of running 6 parallel life domains by orchestrating all 6 axis skills through a single dispatcher with MemKraft-powered executive memory, cross-axis synergy detection, and progressive automation.

## Architecture

```
rr-personal-coo (this skill)
└── axis-dispatcher (meta-orchestrator)
    ├── [Phase 0] axis-life (Axis 6)
    │   └── google-daily → calendar-daily-briefing, gmail-daily-triage
    │   └── gws-* skills, daiso-mcp, obsidian-*
    ├── [Phase 1 — Parallel, max 4 concurrent]
    │   ├── axis-recruitment (Axis 1)
    │   │   └── portal-scanner, parallel-deep-research, interview-prep
    │   ├── axis-investment (Axis 2)
    │   │   └── today → toss-ops-orchestrator → content-repurposing-engine
    │   ├── axis-learning (Axis 3)
    │   │   └── hf-trending-intelligence → paper-review → kb-orchestrator
    │   └── axis-sidepm (Axis 5)
    │       └── sod-ship → sprint-orchestrator → ci-quality-gate
    └── [Phase 2] axis-gm (Axis 4)
        └── cross-axis-scan → synergy-detection → decision-queue → briefing
```

## MemKraft Executive Memory Configuration

### Pre-Load (before dispatch)

Query `ai-context-router` with provenance separation:

```
PERSONAL (MemKraft HOT):
  - Yesterday's cross-axis health scores
  - Pending decisions from decision queue
  - Active synergies being tracked
  - Automation level overrides
  - Recent circuit breaker activations

PERSONAL (MemKraft WARM):
  - Weekly OKR progress snapshot
  - Per-axis performance trends (last 7 days)
  - Recurring synergy patterns
  - User preference overrides (e.g., "skip recruitment axis on weekends")

KNOWLEDGE (LLM Wiki):
  - 6-axis architecture documentation
  - Synergy detection rules (8 rules)
  - Automation level definitions (Level 0/1/2)
  - Error severity classification (S1-S4)
  - Failure alerting protocol
```

### Write-Back (after dispatch completes)

```
MemKraft HOT:
  - Today's cross-axis health scores
  - New synergies detected
  - Decisions routed and their channels
  - Phase guard reuse count
  - Axis failures and recovery actions

MemKraft WARM (weekly):
  - OKR progress delta
  - Automation level review candidates
  - Circuit breaker status changes
  - Cross-axis performance correlation
```

## Execution — Morning Routine (~07:00 Weekdays)

### Pre-Flight

1. **MemKraft Context Pre-Load** — query executive memory for yesterday's state
2. **Dispatch Guard Check** — if `outputs/axis/dispatch/{date}/dispatch-manifest.json` exists
   and `--force` is not set, warn user and ask confirmation before re-running
3. **Automation Levels Load** — read `outputs/axis/automation-levels.json` for per-axis config
4. **Weekend Check** — on Saturday/Sunday, run reduced set (skip recruitment, investment markets closed)

### Phase 0 — Life First (Sequential)

Dispatch `axis-life` morning routine via subagent:

```
Subagent prompt: "Run axis-life morning routine for {date}. Return:
{ status, summary_file, calendar_events, email_action_count, errands_due, errors }"
```

- Calendar data informs other axes (interviews affect recruitment, meetings affect sidepm)
- Email triage may surface items for other axes
- Must complete before Phase 1

### Phase 1 — Independent Axes (Parallel, max 4 concurrent)

Launch 4 subagents simultaneously:

**Axis 1 — Recruitment**:
```
Subagent prompt: "Run axis-recruitment morning routine for {date}. Return:
{ status, pipeline_by_stage, interviews_today, new_opportunities_count, errors }"
```

**Axis 2 — Investment**:
```
Subagent prompt: "Run axis-investment morning routine for {date}. Return:
{ status, top_signals, portfolio_health, strategy_card_count, errors }"
```

**Axis 3 — Learning**:
```
Subagent prompt: "Run axis-learning morning routine for {date}. Return:
{ status, trending_papers_count, queue_items_due, kb_routing_count, errors }"
```

**Axis 5 — Side PM**:
```
Subagent prompt: "Run axis-sidepm morning routine for {date}. Return:
{ status, dirty_repos, open_prs, ci_failures, sprint_items_assigned, errors }"
```

Collect all 4 results. Each subagent returns independently — one failure does not block others.

### Phase 2 — GM Aggregation (Sequential)

Dispatch `axis-gm` morning routine after all Phase 1 subagents complete:

```
Subagent prompt: "Run axis-gm morning routine for {date}. Read outputs from
all axes at outputs/axis/*/. Detect synergies using the 8 cross-axis rules.
Compile consolidated briefing. Return:
{ status, synergies_detected, decisions_pending, overall_health, errors }"
```

The GM axis:
- Reads all Phase 0 + Phase 1 output files
- Runs 8 synergy detection rules (company overlap, topic-project alignment,
  calendar-deadline conflict, news-investment signal, interview prep boost,
  side project → recruitment demo, email → multi-axis routing, market event → calendar block)
- Uses 3-tier fuzzy matching (exact → alias → semantic) with entity alias registry
- Classifies pending decisions via `decision-router`
- Produces the consolidated morning digest

### Phase 3 — Distribution

1. **Slack Briefing** — post to `#효정-할일` as structured thread:
   - Main: 6-axis status grid (axis → GREEN/YELLOW/RED emoji)
   - Reply 1: Top priorities across axes
   - Reply 2: Cross-axis synergies detected
   - Reply 3: Decisions pending (linked to `#효정-의사결정`)
   - Reply 4: Errors/warnings (if any)

2. **Decision Routing** — route decision items:
   - Personal decisions → `#효정-의사결정`
   - Team/CTO decisions → `#ai-리더방`

3. **Dispatch Manifest** — write to `outputs/axis/dispatch/{date}/dispatch-morning.json`

4. **MemKraft Write-Back** — persist today's executive state

## Execution — Evening Routine (~17:00 Weekdays)

### Phase 0 — Life Evening (Sequential)

Dispatch `axis-life` evening (tomorrow prep, email follow-up).

### Phase 1 — Parallel Evening Operations (max 4 concurrent)

- **Axis 2**: EOD market summary, strategy card accuracy review
- **Axis 5**: Code shipping (`eod-ship`), cursor sync
- **Axis 3**: Paper queue processing (max 2/day), KB compile if new sources
- **Axis 1**: Application follow-up check, pipeline status updates

### Phase 2 — GM Evening (Sequential)

- Daily digest compilation
- Axis health scoring (0-100 per axis)
- Write dispatch-evening manifest

### Phase 3 — Evening Distribution

- EOD Slack summary to `#효정-할일`
- Decision items pending from today
- MemKraft write-back with evening state

## Execution — Weekly Routine (Friday PM, after Evening)

### Phase W1 — Parallel Weekly Aggregation

- **Axis 3**: Weekly learning progress, KB health report
- **Axis 5**: Weekly portfolio status report, release ops check
- **Axis 1**: Weekly pipeline summary

### Phase W2 — GM Weekly Synthesis

- OKR progress compilation across all axes
- Axis self-improvement recommendations via `intent-alignment-tracker`
- Automation level review candidates (axes performing consistently at
  Level N may be recommended for Level N+1)
- Executive weekly briefing

### Phase W3 — Weekly Distribution

- Weekly Slack summary to `#효정-할일`
- Optional Notion page via `md-to-notion`
- Optional HTML dashboard via `visual-explainer` (6-axis radar chart,
  activity timeline, decision network graph)
- MemKraft WARM write-back with weekly trends

## Cross-Axis Synergy Detection (GM Phase 2)

The 8 synergy rules that differentiate this from siloed axis execution:

| Rule | Cross-Axis Link | Example |
|------|----------------|---------|
| R001 | Recruitment ↔ Investment | Company in job pipeline also appears in stock watchlist |
| R002 | Learning ↔ Side PM | Paper topic aligns with active side project |
| R003 | Life ↔ Recruitment/Side PM | Calendar conflict between interview and sprint deadline |
| R004 | Learning ↔ Investment | Trending AI paper impacts tracked stock sector |
| R005 | Recruitment ↔ Learning | Interview at ML company → queue related papers |
| R006 | Side PM ↔ Recruitment | Side project demo quality → portfolio for applications |
| R007 | Life → All | Email contains items for multiple axes |
| R008 | Investment ↔ Life | Market event (Fed meeting) → block calendar for monitoring |

Each detected synergy is scored (0-10) and tracked in `outputs/axis/gm/{date}/synergies.json`.
High-scoring synergies (>7) are promoted to the consolidated briefing.

## Progressive Automation Levels

Tracked per-axis in `outputs/axis/automation-levels.json`:

| Level | Behavior | Safety |
|-------|----------|--------|
| 0 — Report Only | Generate briefings and status reports; no actions taken | Default for all axes |
| 1 — Suggest + Confirm | Suggest actions with human approval gate before execution | Requires 2 weeks at Level 0 with <2 S2+ errors |
| 2 — Act + Notify | Execute pre-approved actions autonomously; notify after | Requires 4 weeks at Level 1 with <1 S2+ error |

**Safety constraints (NEVER auto-execute regardless of level):**
- Email sending and meeting scheduling (Axis 6)
- Job applications and outreach emails (Axis 1)
- Trade execution and order placement (Axis 2)
- PR creation and force push (Axis 5)
- KB compilation (Axis 3, expensive operation)

**Level upgrade process:**
1. GM axis flags candidate during weekly review (Phase W2)
2. Recommendation posted to `#효정-의사결정`
3. User explicitly approves upgrade
4. Updated in `automation-levels.json` with `last_reviewed` timestamp

## Phase Guard Protocol (COO Level)

Before dispatching any routine, check the dispatch manifest:

| Routine | Guard File | Skip Condition |
|---------|-----------|----------------|
| Morning | `outputs/axis/dispatch/{date}/dispatch-morning.json` | File exists |
| Evening | `outputs/axis/dispatch/{date}/dispatch-evening.json` | File exists |
| Weekly | `outputs/axis/dispatch/{date}/dispatch-weekly.json` | File exists |

Individual axes implement their own Phase Guards (documented in each axis SKILL.md).
The COO-level guard prevents re-running the entire dispatch when individual
sub-pipelines were already invoked.

Pass `--force` to bypass all guards at every level.
When a phase is skipped (at dispatch or axis level), log `REUSED` in the manifest.

## Composed Skills Reference

### Dispatcher Layer
| Skill | Role in Pipeline |
|-------|-----------------|
| `axis-dispatcher` | Core meta-orchestrator with dependency ordering and failure isolation |
| `memkraft` | Executive memory pre-load and write-back |
| `ai-context-router` | Provenance-separated context retrieval (personal vs official) |
| `decision-router` | Personal vs team decision channel classification |
| `visual-explainer` | HTML dashboard generation for weekly reviews |

### Axis Skills (delegated via axis-dispatcher)
| Skill | Axis | Domain |
|-------|------|--------|
| `axis-life` | 6 | Calendar, email, errands, wellness |
| `axis-recruitment` | 1 | Job pipeline, interviews, career |
| `axis-investment` | 2 | Market data, trading, broker, content |
| `axis-learning` | 3 | Papers, KB, AI radar, study |
| `axis-sidepm` | 5 | Multi-repo git, sprints, CI, releases |
| `axis-gm` | 4 | Cross-axis synthesis, OKR, decisions |

### Transitive Dependencies (invoked by axis skills)
Each axis composes 10-50+ skills internally. Key transitive dependencies:

- **Axis 6**: `google-daily`, `gws-*` (14), `gmail-daily-triage`, `calendar-daily-briefing`,
  `smart-meeting-scheduler`, `daiso-mcp`, `obsidian-*` (8)
- **Axis 1**: `portal-scanner`, `parallel-deep-research`, `kwp-human-resources-interview-prep`,
  `pm-toolkit`, `evaluation-engine`, `gws-email-reply`
- **Axis 2**: `today` (full pipeline), `toss-ops-orchestrator` (8 sub-skills),
  `trading-agent-desk`, `daily-strategy-engine`, `ai-quality-evaluator`,
  `content-repurposing-engine`, `alphaear-orchestrator` (8 sub-skills)
- **Axis 3**: `hf-trending-intelligence`, `paper-review`, `kb-orchestrator` (9 sub-skills),
  `paper-lifecycle-orchestrator`, `cognee`, `nlm-*` slides skills
- **Axis 5**: `sod-ship`, `eod-ship`, `cursor-sync`, `sprint-orchestrator`,
  `ci-quality-gate`, `deep-review`, `release-ops-orchestrator`
- **Axis 4**: `role-dispatcher` (12 roles), `executive-briefing`,
  `decision-tracker`, `intent-alignment-tracker`

## Output Artifacts

### Per-Dispatch
| File | Description |
|------|-------------|
| `outputs/axis/dispatch/{date}/dispatch-morning.json` | Morning dispatch manifest |
| `outputs/axis/dispatch/{date}/dispatch-evening.json` | Evening dispatch manifest |
| `outputs/axis/dispatch/{date}/dispatch-weekly.json` | Weekly dispatch manifest |

### Per-Axis (delegated)
Each axis writes to `outputs/axis/{axis-name}/{date}/` — see individual axis SKILL.md files.

### Persistent State
| File | Purpose |
|------|---------|
| `outputs/axis/automation-levels.json` | Per-axis automation level config |
| `outputs/axis/gm/entity-aliases.json` | Fuzzy matching entity alias registry |
| `outputs/axis/life/errands-queue.json` | Cross-day errand tracker |
| `outputs/axis/recruitment/job-pipeline.json` | Job application tracker |
| `outputs/axis/learning/learning-queue.json` | Learning item queue |
| `outputs/axis/learning/topics-config.json` | Tracked research topics |
| `outputs/axis/recruitment/criteria-config.json` | Job fit scoring criteria |

## Slack Channels

| Channel | Purpose |
|---------|---------|
| `#효정-할일` | Consolidated briefings, axis alerts, errand reminders |
| `#효정-의사결정` | Personal decisions, automation level upgrades, critical failures |
| `#ai-리더방` | Team/CTO decisions (via decision-router) |
| `#h-report` | Trading signals and daily report (via today pipeline) |
| `#deep-research-trending` | AI research radar posts (via axis-learning) |

## Error Handling

### Per-Axis Failure Isolation

Each axis runs in its own subagent. One axis failing does NOT prevent others:

1. Failed axis posts immediately to `#효정-할일`: `⚠️ Axis {N} ({name}) failed: {error_summary}`
2. Failure recorded in dispatch manifest
3. Remaining axes continue execution
4. GM axis marks failed axis as "NO DATA" in cross-axis scan and continues

### Escalation Rules

- 3+ axes degraded (S2+) in single routine → escalate to `#효정-의사결정`
- 2+ axes critical (S1) → escalate to `#효정-의사결정`
- Single S1 failure → alert in `#효정-할일`, included in briefing

### Circuit Breaker

If an axis reports S1 severity for 3 consecutive days:
1. Automatically set its automation level to 0 in `automation-levels.json`
2. Post persistent alert to `#효정-의사결정`
3. Skip the axis in subsequent dispatches until manually re-enabled

### Retry Policy

No automatic retries at dispatcher level. Individual axes handle internal retries.
User can re-run a specific axis via `/axis-{name}` command.

## Gaps Addressed by This Skill

| Gap | How Addressed |
|-----|--------------|
| No unified coordination across 6 life domains | Single dispatcher with dependency-aware ordering |
| Cross-axis synergies go undetected | 8 synergy detection rules with fuzzy entity matching |
| Automation levels not tracked or reviewed | Progressive 3-tier automation with weekly review |
| No executive memory across dispatch cycles | MemKraft HOT/WARM integration for state continuity |
| Decision routing scattered across skills | Centralized decision queue with channel classification |
| No circuit breaker for persistently failing axes | 3-day S1 consecutive failure → auto-disable |
| Weekend routines run unnecessary axes | Auto-detection of day-of-week with reduced-set weekend mode |
| Dispatch re-runs waste API calls and duplicate Slack posts | 3-level Phase Guard (dispatch + axis + sub-pipeline) |
| No cross-axis performance trends | Weekly GM health scoring with intent-alignment-tracker |
| Dashboard for holistic life view missing | On-demand HTML dashboard via visual-explainer (radar chart) |

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

## Examples

**Standard morning dispatch:**
User: "rr-personal-coo" or "6축 오케스트레이터"
→ Runs morning routine: Axis 6 (life) → parallel [Axis 1,2,3,5] → Axis 4 (GM synthesis) → Slack briefing

**Friday weekly review:**
User: "rr-personal-coo" on Friday PM
→ Adds weekly reporting, portfolio review, and Dream Cycle to the standard evening routine

## Operational Runbook

### First Run Setup

```bash
mkdir -p outputs/axis/dispatch
mkdir -p outputs/axis/{life,recruitment,investment,learning,sidepm,gm}

# Initialize automation levels (all at Level 0)
cat > outputs/axis/automation-levels.json << 'EOF'
{
  "axis-life": { "level": 0, "last_reviewed": "2026-04-15" },
  "axis-recruitment": { "level": 0, "last_reviewed": "2026-04-15" },
  "axis-investment": { "level": 0, "last_reviewed": "2026-04-15" },
  "axis-learning": { "level": 0, "last_reviewed": "2026-04-15" },
  "axis-sidepm": { "level": 0, "last_reviewed": "2026-04-15" },
  "axis-gm": { "level": 0, "last_reviewed": "2026-04-15" }
}
EOF

# Initialize entity alias registry
echo '{}' > outputs/axis/gm/entity-aliases.json

# Initialize persistent queues
echo '[]' > outputs/axis/life/errands-queue.json
echo '[]' > outputs/axis/recruitment/job-pipeline.json
echo '[]' > outputs/axis/learning/learning-queue.json
```

### Daily Verification

```bash
# Check if morning dispatch ran
ls outputs/axis/dispatch/$(date +%Y-%m-%d)/dispatch-morning.json

# Check per-axis health
cat outputs/axis/gm/$(date +%Y-%m-%d)/axis-health.json | python -m json.tool

# Check for errors across axes
for axis in life recruitment investment learning sidepm gm; do
  echo "=== $axis ==="
  cat outputs/axis/$axis/$(date +%Y-%m-%d)/errors.json 2>/dev/null || echo "No errors"
done
```

### Force Re-Run

```bash
# Re-run full morning dispatch
# Invoke rr-personal-coo with --force flag

# Re-run single axis
# Invoke axis-{name} directly
```

### Troubleshooting

| Symptom | Check | Fix |
|---------|-------|-----|
| Axis marked NO DATA | `outputs/axis/{axis}/{date}/` directory empty | Re-run individual axis |
| Duplicate Slack posts | Phase Guard files missing | Verify `outputs/` directory permissions |
| Synergy detection misses | Entity alias registry incomplete | Update `entity-aliases.json` with new mappings |
| Automation level stuck at 0 | Check `last_reviewed` date > 2 weeks | Run weekly review to evaluate upgrade |
| Circuit breaker activated | Check `errors.json` for 3 consecutive S1 days | Fix root cause, re-enable in `automation-levels.json` |
| Weekend over-execution | Day-of-week check not applied | Verify weekend check logic in pre-flight |

### Cursor Automation Cron Setup

```yaml
automations:
  - name: "Personal COO — Morning"
    trigger:
      type: cron
      schedule: "0 7 * * 1-5"
    action:
      skill: rr-personal-coo
      args: { routine: "morning" }

  - name: "Personal COO — Evening"
    trigger:
      type: cron
      schedule: "0 17 * * 1-5"
    action:
      skill: rr-personal-coo
      args: { routine: "evening" }

  - name: "Personal COO — Weekly"
    trigger:
      type: cron
      schedule: "0 17 * * 5"
      after: "Personal COO — Evening"
    action:
      skill: rr-personal-coo
      args: { routine: "weekly" }
```
