---
name: codebase-archaeologist
description: >-
  Analyze git history to create ownership maps, churn hotspot analysis,
  "bus factor" reports, pattern evolution timelines, and dead code detection
  through commit frequency decay. Adds the TIME dimension to code understanding.
  Use when the user asks "who owns this code", "code archaeology", "bus factor",
  "churn analysis", "what's the riskiest module", "dead code", "코드 히스토리",
  "코드 소유자", "위험 분석", "who should review this", or any question about
  code ownership, history, or temporal risk patterns.
  Do NOT use for static code review (use simplify or deep-review), debugging
  (use diagnose), or git commit/PR operations (use domain-commit or ship).
metadata:
  author: thaki
  version: 1.0.0
---

# Codebase Archaeologist — Temporal Code Analysis

Unearth the hidden history of your codebase. While code review tools see a snapshot, this skill sees the full timeline — who wrote what, what's decaying, what's risky, and what's been forgotten.

## Usage

```
/codebase-archaeologist                           # full project analysis
/codebase-archaeologist src/api/                  # scope to directory
/codebase-archaeologist --mode ownership          # ownership map only
/codebase-archaeologist --mode churn              # churn hotspots only
/codebase-archaeologist --mode bus-factor         # bus factor report only
/codebase-archaeologist --mode dead-code          # dead code candidates only
/codebase-archaeologist --mode risk               # composite risk heatmap
/codebase-archaeologist --since "6 months ago"    # custom time window
```

## Workflow

### Step 1: Determine Scope and Mode

Parse user input for:
- **Target path**: directory or file (default: entire repo)
- **Mode**: `ownership | churn | bus-factor | dead-code | risk | full` (default: `full`)
- **Time window**: `--since` value (default: 12 months). Accepts any git date format: `"6 months ago"`, `"2024-01-01"`, `"1 year ago"`

### Step 2: Collect Git History Data

Run these git commands to gather raw data:

```bash
# Commit frequency per file
git log --since="$SINCE" --format="%H %ae %aI" --name-only -- "$TARGET"

# Per-file author stats
git log --since="$SINCE" --format="%ae" -- "$FILE" | sort | uniq -c | sort -rn

# File-level change frequency (--name-only without format avoids empty-line issues)
git log --since="$SINCE" --name-only --pretty=format: -- "$TARGET" | grep -v '^$' | sort | uniq -c | sort -rn

# Last modified date per file
git log -1 --format="%aI" -- "$FILE"

# Total authors per file
git log --since="$SINCE" --format="%ae" -- "$FILE" | sort -u | wc -l
```

Parse the output into structured data for analysis.

### Step 3: Run Analysis (by mode)

#### 3a. Ownership Map (`--mode ownership`)

For each directory/module, determine:
- **Primary owner**: author with most commits
- **Contributors**: all authors with commit counts
- **Ownership concentration**: percentage of commits by top author

Present as a table:

```
Module              | Primary Owner    | Commits | Contributors | Concentration
--------------------|-----------------|---------|-------------|---------------
src/api/auth/       | dev-a@co.com    | 142     | 3           | 68%
src/components/ui/  | dev-b@co.com    | 89      | 5           | 41%
```

#### 3b. Churn Hotspots (`--mode churn`)

Rank files by commit frequency in the time window. High churn signals instability or active development.

```
Rank | File                        | Commits | Authors | Last Changed
-----|-----------------------------|---------|---------|--------------
1    | src/api/auth/handler.ts     | 47      | 3       | 2 days ago
2    | src/components/Chat.tsx     | 38      | 2       | 1 week ago
```

Flag files with high churn + low test coverage as stability risks.

#### 3c. Bus Factor (`--mode bus-factor`)

For each critical module, calculate: how many developers have meaningful knowledge?

- **Bus factor 1**: single author owns >80% of commits — critical risk
- **Bus factor 2**: two authors cover >80% — moderate risk
- **Bus factor 3+**: knowledge distributed — healthy

```
Module              | Bus Factor | Risk     | Top Authors
--------------------|-----------|----------|----------------------------
src/api/auth/       | 1         | CRITICAL | dev-a (92%)
src/lib/utils/      | 3         | LOW      | dev-a (40%), dev-b (30%), dev-c (20%)
```

#### 3d. Dead Code Candidates (`--mode dead-code`)

Find files that:
1. Have zero commits in the last N months
2. Are still imported/referenced by other files
3. May be candidates for removal or archival

```bash
# Files with no recent commits
git log --since="$SINCE" --name-only --pretty=format: | grep -v '^$' | sort -u > /tmp/active.txt
find "$TARGET" \( -name "*.ts" -o -name "*.tsx" -o -name "*.py" \) | sort > /tmp/all.txt
comm -23 /tmp/all.txt /tmp/active.txt
```

Cross-reference with import analysis (grep for `import` statements referencing these files) to classify:
- **Truly dead**: not imported anywhere — safe to remove
- **Stale but referenced**: imported but never modified — review needed
- **Config/fixture**: test fixtures, configs — likely intentional

#### 3e. Risk Heatmap (`--mode risk`)

Composite risk score per file/module combining:

```
risk_score = (churn_rate * 0.3) + (bus_factor_inverse * 0.3) + (staleness * 0.2) + (complexity_proxy * 0.2)
```

Where:
- `churn_rate`: normalized commit frequency (higher = more volatile)
- `bus_factor_inverse`: 1/bus_factor (higher = fewer people know it)
- `staleness`: months since last commit (higher = more neglected)
- `complexity_proxy`: file size in lines via `wc -l < "$FILE"` (rough approximation)

Present as a ranked list with risk levels: CRITICAL / HIGH / MEDIUM / LOW.

### Step 4: Generate Report

Combine all analyses into a structured report:

```
Codebase Archaeology Report
============================
Scope: [target path]
Period: [time window]
Total files analyzed: [N]
Total authors: [N]

[Mode-specific sections from Step 3]

Key Findings:
  1. [most critical finding]
  2. [second finding]
  3. [third finding]

Recommendations:
  1. [actionable recommendation]
  2. [actionable recommendation]
```

If `--mode full`, include all five analysis sections.

## Examples

### Example 1: Full project archaeology

User: `/codebase-archaeologist`

Output: Complete report with ownership map, churn hotspots, bus factor, dead code candidates, and risk heatmap for the entire repository over the last 12 months.

### Example 2: Targeted ownership check

User: "Who owns the auth module?"

Output: Ownership map for `src/api/auth/` showing primary owner, all contributors, and ownership concentration percentage.

### Example 3: Risk assessment before refactoring

User: "What's the riskiest part of the frontend?"

Output: Risk heatmap for `src/components/` and `src/pages/` showing files with high churn, low bus factor, and low test coverage.

## Error Handling

| Scenario | Action |
|----------|--------|
| Git history too shallow (CI clone) | Warn user; suggest `git fetch --unshallow` |
| No commits in time window | Expand window automatically; inform user |
| Target path doesn't exist | Report error with suggestion of similar paths |
| Binary files in results | Filter out non-source files automatically |
| Very large repo (10k+ files) | Limit to top-level directories first; drill down on request |

## Troubleshooting

- **"No commits found"**: Check `--since` window -- default is 12 months. Try `--since "3 years ago"` for older repos.
- **Shallow clone**: CI environments often clone with `--depth 1`. Run `git fetch --unshallow` to get full history.
- **Inaccurate ownership**: Bulk reformatting commits inflate author counts. Use `--no-merges` or filter commits touching >50 files.
- **Slow on large repos**: Scope to a specific directory (`/codebase-archaeologist src/api/`) instead of full project.
