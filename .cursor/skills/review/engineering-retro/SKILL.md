---
name: engineering-retro
description: >-
  Time-based engineering retrospective analyzing commits, session patterns, PR
  sizes, test-to-code ratios, hotspot files, and per-contributor highlights
  over a configurable period. Produces a structured Korean report with
  actionable insights. Use when the user asks for "engineering retro",
  "retrospective", "sprint retro", "weekly retro", "엔지니어링 회고", "스프린트
  회고", "주간 회고", "개발 회고", "engineering-retro", or wants to reflect on
  engineering health over a time period. Do NOT use for code review (use
  deep-review), daily standup (use standup-digest), or weekly status report
  (use weekly-status-report).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# Engineering Retro — Time-Based Development Retrospective

Analyze engineering activity over a configurable period to produce actionable insights about code health, velocity, testing discipline, and contributor patterns.

## Usage

```
/engineering-retro                    # default: last 7 days
/engineering-retro 14d               # last 14 days
/engineering-retro 30d               # last 30 days
/engineering-retro 2026-03-01..now   # specific date range
```

## Workflow

### Step 1: Collect Raw Data

```bash
# Commits in period
git log --since="$START" --until="$END" --format="%H|%an|%ae|%ai|%s" --no-merges

# File change stats
git log --since="$START" --until="$END" --numstat --no-merges

# Lines added/removed per author
git log --since="$START" --until="$END" --shortstat --author="$AUTHOR" --no-merges
```

### Step 2: Detect Commit Sessions

Group commits into "coding sessions" using a 45-minute inactivity gap:

1. Sort commits chronologically per author
2. If gap between consecutive commits > 45 minutes, start a new session
3. Calculate: session count, average session duration, longest session
4. Flag marathon sessions (> 4 hours) as potential burnout signals

### Step 3: Analyze Code Health Metrics

| Metric | Calculation | Healthy Range |
|--------|-------------|---------------|
| Test-to-code ratio | Lines in test files / Lines in source files | >= 0.3 (30%) |
| Average PR size | Lines changed per commit or PR | < 300 lines |
| Hotspot files | Files modified in > 3 commits | Track top 5 |
| Churn rate | Lines modified in files < 7 days old | < 20% of total |
| Commit frequency | Commits per day per contributor | 3-15 |
| TODO/FIXME delta | New TODO/FIXME added - removed | Net <= 0 |

### Step 4: Per-Contributor Highlights

For each active contributor:

1. **Productivity**: Total commits, lines added/removed, files touched
2. **Session patterns**: Average session length, work time distribution
3. **Strengths**: Top domains (frontend/backend/test/docs) by commit count
4. **Growth points**: Areas with fewer commits or lower test ratios
5. **Praise**: Highlight best commit (largest test ratio, cleanest diff, most impactful fix)

### Step 5: Identify Patterns and Risks

- **Hotspot files**: Files with highest churn — candidates for refactoring
- **Bus factor**: Files only touched by 1 contributor — knowledge concentration risk
- **Test discipline**: Commits without corresponding test changes
- **Large commits**: Commits with > 500 lines changed — harder to review and bisect
- **Weekend/late-night work**: Commits outside business hours — burnout risk

### Step 6: Generate Report

```
Engineering Retrospective
=========================
Period: [start] → [end] ([N] days)
Contributors: [N]
Total Commits: [N] | Total Sessions: [N]

Health Metrics:
  Test-to-code ratio:   [X]% [↑/↓ vs previous period]
  Average commit size:  [N] lines [↑/↓]
  Hotspot count:        [N] files
  TODO/FIXME delta:     +[N] / -[N] = net [N]

Top Hotspot Files (most churn):
  1. [file] — [N] commits, [N] contributors
  2. [file] — [N] commits, [N] contributors

Bus Factor Risks:
  - [file]: only touched by @[author]
  - [file]: only touched by @[author]

Per-Contributor Summary:
  @[author1]:
    Commits: [N] | Lines: +[N] -[N] | Sessions: [N]
    Domains: backend (60%), test (25%), docs (15%)
    Best commit: [hash] — [description]
    Growth: Consider adding tests for [domain] changes

  @[author2]:
    ...

Velocity Trend:
  Week 1: [N] commits, [N] lines
  Week 2: [N] commits, [N] lines
  Trend: [↑ accelerating / → stable / ↓ decelerating]

Action Items:
  1. Refactor [hotspot file] — touched [N] times this period
  2. Add contributor to [bus-factor file] for knowledge sharing
  3. Improve test ratio for [domain] (currently [X]%, target >= 30%)
```

### Step 7: Archive Snapshot (Optional)

Save a JSON snapshot for trend tracking:

```bash
# Save to output/retros/
mkdir -p output/retros
# Write JSON with metrics for period comparison
```

## Examples

### Example 1: Weekly retrospective

User runs `/engineering-retro` at end of sprint.

Actions:
1. Collect last 7 days of git data
2. Detect 15 coding sessions across 3 contributors
3. Calculate: test ratio 35%, average commit 180 lines, 2 hotspot files
4. Generate per-contributor highlights with praise points
5. Report with 3 action items

### Example 2: Monthly health check

User runs `/engineering-retro 30d` for monthly review.

Actions:
1. Analyze 30 days across all contributors
2. Compare velocity across 4 weekly windows
3. Identify trend (accelerating/decelerating)
4. Generate comprehensive report with bus factor analysis

## Error Handling

| Scenario | Action |
|----------|--------|
| No commits in period | Suggest expanding the date range |
| Single contributor | Skip per-contributor comparison, focus on self-improvement |
| No test files detected | Flag as critical: "No test infrastructure found" |
| Git log fails | Check if current directory is a git repo |
