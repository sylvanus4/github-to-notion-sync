---
name: sprint-retro-facilitator
description: >-
  Data-backed sprint retrospective facilitator that combines engineering
  metrics (via engineering-retro + github-sprint-digest) with structured
  facilitation frameworks, mood/sentiment tracking, SMART action items, and
  retro-over-retro trend analysis. Produces a comprehensive retro document
  with discussion prompts, data highlights, and tracked follow-ups.
---

# Sprint Retro Facilitator

Data-backed facilitation for sprint retrospectives with structured prompts, sentiment tracking, and SMART action item management.

## When to Use

- End-of-sprint retrospective that needs data backing (not just vibes)
- Team wants structured discussion prompts seeded with real metrics
- Action item follow-up from previous retros needs tracking
- Sentiment trend across multiple retros needs visualization
- Remote/async retro that benefits from a pre-built discussion guide

## Pipeline

```
Collect Data → Review Previous → Generate Prompts → Facilitate → Track Actions → Archive
```

### Phase 1: Pre-Retro Data Collection

Gather quantitative engineering data to ground the discussion in evidence.

**Data sources** (run in parallel via subagents):

| Source | Skill | Data Extracted |
|---|---|---|
| Git metrics | `engineering-retro` | Commits, PR sizes, test ratios, hotspots, session patterns, bus factor |
| GitHub activity | `github-sprint-digest` | Issues closed, PRs merged, review turnaround, blocked items, CI status |
| Sprint board | `jira-linear-adapter` (optional) | Story points completed vs planned, carry-over items, scope changes |

**Output**: `outputs/retros/{date}/phase-1-data.json` with merged metrics.

**Derived highlights** (auto-detected, used to seed discussion):
- **Wins**: PRs merged ahead of schedule, test ratio improvement, hotspot files stabilized
- **Anomalies**: Unusual churn in stable files, review turnaround spikes, CI failure rate increase
- **Risks**: Bus factor files, large uncommitted PRs, stale branches

### Phase 2: Previous Retro Review

Load the most recent retro archive (if exists) from `outputs/retros/`.

- **Action item follow-up**: Check each previous action item's status
  - Completed: celebrate
  - Still open: carry forward with escalation flag
  - Stale (>2 sprints): escalate or explicitly close with rationale
- **Sentiment trend**: Load previous sentiment scores for comparison
- **Pattern detection**: Flag recurring themes (same category appearing 3+ retros)

### Phase 3: Discussion Prompt Generation

Generate structured facilitation prompts organized by retrospective framework.

**Default framework: 4Ls** (Liked, Learned, Lacked, Longed For)

Each category gets 2-3 data-backed seed prompts:

```markdown
## Liked (What went well)
- 🎯 Test-to-code ratio improved from 28% to 35% this sprint
  → "What practices helped us write more tests?"
- 🚀 Average PR review turnaround dropped from 18h to 8h
  → "What changed in our review process?"

## Learned (New insights)
- 📊 3 hotspot files accounted for 40% of all changes
  → "What does this concentration tell us about our architecture?"

## Lacked (What was missing)
- ⚠️ 4 PRs were merged without test changes
  → "What prevented us from adding tests for these changes?"
- ⏰ 2 items carried over from the previous sprint
  → "Were these underestimated or deprioritized?"

## Longed For (What we wish we had)
- [Open-ended — no data-backed seed, left for team input]
```

**Alternative frameworks** (selectable via `--framework`):
- **Start-Stop-Continue**: Action-oriented, good for teams with clear process issues
- **Mad-Sad-Glad**: Emotion-focused, good for psychological safety emphasis
- **Sailboat**: Goal (island), wind (helpers), anchor (blockers), rocks (risks)
- **Custom**: User provides category names

### Phase 4: Facilitation Guide

Generate a facilitator's run-of-show document.

```markdown
# Sprint Retro — {sprint_name} ({date})

## Agenda (60 min)

| Time | Activity | Duration |
|---|---|---|
| 0:00 | Check-in & ground rules | 5 min |
| 0:05 | Previous action item review | 10 min |
| 0:15 | Data highlights walkthrough | 10 min |
| 0:25 | 4Ls discussion (each category) | 25 min |
| 0:50 | Action item generation (SMART) | 8 min |
| 0:58 | Closing & sentiment check | 2 min |

## Ground Rules
1. Vegas rule: what's said in retro stays in retro
2. Focus on systems, not individuals
3. One conversation at a time
4. Every voice matters — use round-robin for quiet members

## Data Highlights (present to team)
[charts from visual-explainer: velocity trend, test ratio, PR turnaround]

## Discussion Prompts
[from Phase 3]

## Previous Action Items
[from Phase 2, with status markers]
```

### Phase 5: Sentiment Tracking

After the retro discussion (or async input), collect team sentiment.

**Sentiment dimensions** (each scored 1-5):
- **Sprint satisfaction**: How satisfied are you with this sprint's outcomes?
- **Team collaboration**: How well did the team collaborate?
- **Process health**: How effective are our current processes?
- **Psychological safety**: How safe do you feel raising concerns?
- **Workload balance**: How manageable was your workload?

**Collection mode**:
- **Live**: Facilitator collects verbal scores during closing
- **Async**: Generate a simple form template (markdown checklist or linked survey)

**Trend visualization**: If 3+ retros exist, generate a line chart via `visual-explainer` showing dimension trends over time.

### Phase 6: Action Item Management

Convert discussion outcomes into tracked, SMART action items.

**SMART enforcement**:
- **Specific**: Action must describe a concrete change, not a vague goal
- **Measurable**: Include a success metric or completion criteria
- **Assignable**: Must have a named owner (not "the team")
- **Relevant**: Must connect to a discussed topic
- **Time-bound**: Must have a due date (default: next retro date)

**Examples**:
| ❌ Not SMART | ✅ SMART |
|---|---|
| "Write more tests" | "@kim: Add unit tests for user-auth module to reach 40% coverage by Apr 24" |
| "Improve code review" | "@lee: Create PR review checklist as .md and link in CONTRIBUTING.md by Apr 18" |
| "Better communication" | "@park: Post daily async standup in #dev-standup channel starting next sprint" |

**Tracking**: Route all action items to `meeting-action-tracker` for Notion task creation, Slack reminders, and escalation.

### Phase 7: Archive & Output

**File outputs** (under `outputs/retros/{date}/`):
- `retro-data.json` — Phase 1 merged metrics
- `retro-prompts.md` — Discussion prompts and facilitation guide
- `retro-summary.md` — Post-retro summary with decisions and action items
- `sentiment.json` — Sentiment scores (if collected)
- `retro-report.docx` — Formatted document via `anthropic-docx`

**Optional distribution**:
- `--notion`: Publish retro summary to Notion
- `--slack`: Post highlights + action items to team Slack channel

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `--sprint` | auto-detect | Sprint name or date range |
| `--framework` | 4Ls | Retro framework: 4Ls, start-stop-continue, mad-sad-glad, sailboat, custom |
| `--previous` | auto | Path to previous retro archive for trend comparison |
| `--skip-jira` | false | Skip Jira/Linear data collection |
| `--async` | false | Generate async retro template instead of live facilitation guide |
| `--sentiment` | true | Include sentiment tracking section |
| `--notion` | false | Publish to Notion |
| `--slack` | false | Post summary to Slack |

## Constraints

- Never attribute metrics to individuals in a negative framing — retros are about systems, not blame
- Sentiment data is anonymous by default; only aggregate scores are stored
- Action items without owners are flagged but not auto-assigned
- Previous retro data is read-only; never modify archived retro files
- If no previous retro exists, skip Phase 2 trend analysis gracefully
- Limit data highlights to 5-7 items to avoid information overload
