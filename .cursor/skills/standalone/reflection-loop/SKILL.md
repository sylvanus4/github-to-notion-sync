---
name: reflection-loop
description: >-
  Domain-agnostic post-task/post-day reflection that reviews completed work,
  cross-references session patterns, generates lessons, and routes actionable
  items to the appropriate destinations (skills → autoskill-extractor, facts →
  memkraft-ingest, lessons → tasks/lessons.md). Supports manual invocation
  (/reflect), automatic invocation by daily-pm-orchestrator (Phase 0), and
  per-domain adapters for trading, engineering, and PM reflection.
  Use when the user asks to "reflect", "run reflection", "daily reflection",
  "session reflection", "일일 회고", "리플렉션", "회고 실행", "오늘 돌아보기",
  "reflection-loop", or when invoked by daily-pm-orchestrator Phase 0.
  Do NOT use for engineering-only retrospectives with git metrics (use
  engineering-retro). Do NOT use for sprint retrospective-to-issue pipelines
  (use sprint-retro-to-issues). Do NOT use for inline post-task reflection
  during active work (follow post-task-reflection.mdc rule directly).
triggers:
  - reflect
  - run reflection
  - daily reflection
  - session reflection
  - 리플렉션
  - 일일 회고
  - 회고 실행
  - 오늘 돌아보기
  - reflection-loop
tags: [reflection, learning, memory, self-improvement, orchestration]
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "standalone"
---

# Reflection Loop — Domain-Agnostic Post-Work Reflection

Structured reflection that reviews completed work, detects reusable patterns,
and routes discoveries to the correct knowledge stores. Operates at a higher
level than the inline `post-task-reflection.mdc` rule (which fires per-task);
this skill synthesizes across an entire day or session.

## Modes

| Mode | Trigger | Scope |
|---|---|---|
| Manual | `/reflect` or "run reflection" | Current session or today |
| Automated | `daily-pm-orchestrator` Phase 0 | Full day's work |
| Domain | `/reflect --domain trading` | Domain-specific adapter |

## Workflow

### Step 1: Gather Completed Work

Collect all completed tasks and artifacts from today's work.

**Sources** (check in order, skip if empty):

1. `tasks/todo.md` — completed items with today's date stamp
2. `outputs/daily-pm/{date}/` — pipeline phase outputs (if running as Phase 0)
3. `outputs/today/{date}/` — morning pipeline outputs
4. `memory/sessions/` — today's session files (match by date prefix `YYYY-MM-DD`)
5. Git log — today's commits: `git log --since="midnight" --oneline`

**Output**: A structured list of completed items with source attribution.

### Step 2: Cross-Reference Patterns

Search for recurring patterns across recent sessions.

```bash
python scripts/memory/search.py "<top 3 keywords from Step 1>" --mode hybrid --limit 10
```

Look for:
- **Repeated workflows**: same sequence of tools/skills used 3+ times across sessions
- **Recurring corrections**: user corrections that appear in `tasks/lessons.md` repeatedly
- **Skill gaps**: tasks that required excessive tool calls (>15) suggesting a missing skill
- **Decision patterns**: similar decisions made in different contexts

### Step 3: Domain Adapter (Optional)

If `--domain` is specified or the day's work is dominated by one domain (>60% of tasks),
apply the domain-specific reflection lens.

#### Trading Adapter

Compare today's trading decisions against actual market outcomes:

- Read `outputs/today/{date}/` for screener/analysis outputs
- Read `outputs/toss/` for portfolio snapshots and P&L
- **Key question**: Did the signals from the pipeline align with actual price movements?
- **Metrics**: signal accuracy rate, missed opportunities, false positives
- Route trading lessons to `knowledge-bases/trading-daily/` via `kb-ingest`

#### Engineering Adapter

Compare engineering estimates against actuals:

- Read today's git commits and PR data
- Cross-reference with sprint estimates from GitHub issues
- **Key question**: Were complexity estimates accurate? Which files had unexpected churn?
- **Metrics**: estimate accuracy, hotspot files, test coverage delta
- Route engineering lessons to `tasks/lessons.md`

#### PM Adapter

Compare PM assumptions against observed outcomes:

- Read today's meeting digests and PRD updates
- Cross-reference with feature adoption metrics if available
- **Key question**: Were user/stakeholder assumptions validated or invalidated?
- **Metrics**: assumption hit rate, scope change frequency, stakeholder feedback alignment
- Route PM insights to `memory/topics/preferences.md`

### Step 4: Generate Recommendations

Synthesize findings into three categories:

#### 4a. Skill Candidates

Apply the 3-gate filter from `hermes-inline-learning.mdc`:

1. **Non-Googleable**: required project-specific knowledge
2. **Codebase-specific**: tied to this project's conventions
3. **Hard-won**: required real debugging effort or multi-step reasoning

- All 3 gates pass → invoke `autoskill-extractor` with the pattern description
- Gates 1-2 pass, gate 3 fails → log as a memory entry via `memkraft-ingest`

#### 4b. Memory Updates

- New workspace facts → `AGENTS.md` Learned Workspace Facts (via `memkraft-ingest`)
- New user preferences → `AGENTS.md` Learned User Preferences
- Confirm security scan passes before any memory write (ref: `done-checklist.mdc`)

#### 4c. Lessons

- Mistakes or dead-ends → append to `tasks/lessons.md` with pattern + prevention rule
- If same pattern appears 3+ times → promote to a `.cursor/rules/` rule

### Step 5: Persist Reflection Output

Write the reflection report to `outputs/reflection/{date}/reflection-{timestamp}.json`:

```json
{
  "date": "YYYY-MM-DD",
  "mode": "manual|automated|domain",
  "domain": null,
  "tasks_reviewed": 12,
  "patterns_detected": [
    {
      "type": "recurring_workflow|skill_gap|decision_pattern",
      "description": "...",
      "frequency": 3,
      "action": "extract_skill|memory_update|lesson|none"
    }
  ],
  "skill_candidates": [],
  "memory_updates": [],
  "lessons": [],
  "summary": "one-line Korean summary"
}
```

### Step 6: Report

Produce a concise Korean summary suitable for:
- **If manual**: direct output to the user
- **If automated (Phase 0)**: write to `outputs/daily-pm/{date}/phase-0-reflection.json`
  and return the subagent contract:
  ```json
  {
    "status": "completed",
    "file": "outputs/daily-pm/{date}/phase-0-reflection.json",
    "summary": "one-line summary"
  }
  ```

## Integration

| Component | Relationship |
|---|---|
| `post-task-reflection.mdc` | Inline per-task reflection; this skill synthesizes across a full day/session |
| `daily-pm-orchestrator` | Invokes this skill as Phase 0 before knowledge consolidation |
| `hermes-inline-learning.mdc` | Shares the 3-gate filter for skill candidate evaluation |
| `autoskill-extractor` | Receives skill candidates from Step 4a |
| `memkraft-ingest` | Receives memory updates from Step 4b |
| `tasks/lessons.md` | Receives lesson captures from Step 4c |
| `engineering-retro` | Domain-specific: engineering adapter references similar analysis |
| `trading-agent-desk` | Domain-specific: trading adapter complements post-decision reflection |
| `session_lineage.py` | Session cross-referencing uses lineage data when available |

## Output Directory

```
outputs/reflection/{date}/
├── reflection-{timestamp}.json    # Structured reflection data
└── manifest.json                  # Links to actionable outputs
```

## Skip Conditions

- Day had fewer than 3 completed tasks → skip (insufficient data for pattern detection)
- User explicitly says "skip reflection" or passes `--skip-phase 0`
- Running in `--only-phase N` mode where N ≠ 0
