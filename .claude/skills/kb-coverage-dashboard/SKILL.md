---
name: kb-coverage-dashboard
description: >-
  Generate a single aggregated KB health dashboard across all topics with
  RED/YELLOW/GREEN status indicators. Combines freshness scoring, broken
  wikilink detection, evidence density, connection coverage, article count,
  and staleness distribution into a unified report. Provides per-topic health
  cards and an overall KB health score. Use when the user asks to "KB
  dashboard", "KB health overview", "coverage dashboard", "topic health
  summary", "KB 대시보드", "KB 건강 현황", "토픽 건강 요약", "커버리지 대시보드",
  "kb-coverage-dashboard", "KB status report", "all topics health", "전체 토픽
  상태", "KB 종합 현황", "knowledge base health", "KB 헬스 체크", or wants a
  comprehensive view of the entire knowledge base system health. Do NOT use
  for linting a single topic (use kb-lint). Do NOT use for compiling wiki
  content (use kb-compile). Do NOT use for discovering missing connections
  (use wiki-connection-discoverer). Do NOT use for daily intelligence reports
  (use kb-daily-report).
---

# KB Coverage Dashboard

Generate a single aggregated health dashboard across all Knowledge Base topics
with RED/YELLOW/GREEN status indicators and an overall health score.

## When to Use

- Periodic (weekly/monthly) KB health check across all topics
- After large-scale ingestion or compilation runs
- Before presenting KB status to stakeholders
- Identifying which topics need immediate attention
- User says "KB dashboard", "KB 대시보드", "전체 토픽 상태"

## Do NOT Use

- Linting a single topic → `kb-lint`
- Compiling wiki content → `kb-compile`
- Discovering missing connections → `wiki-connection-discoverer`
- Daily intelligence reports → `kb-daily-report`

## Architecture

```
KB Coverage Dashboard
├── Enumerate all topics under knowledge-bases/
├── Per-topic health assessment
│   ├── Article metrics
│   │   ├── Total article count (concepts + references)
│   │   ├── Articles with frontmatter completeness
│   │   └── Average word count
│   ├── Freshness metrics
│   │   ├── Median article age (days since ingested/compiled)
│   │   ├── Stale article ratio (>90 days)
│   │   ├── Most recent article date
│   │   └── Unified freshness score (0-100, per kb-lint Check 5)
│   ├── Link health
│   │   ├── Broken wikilinks count
│   │   ├── Orphan articles (no incoming links)
│   │   ├── Dead-end articles (no outgoing links)
│   │   └── Link density (links per article)
│   ├── Evidence metrics
│   │   ├── Average evidence entries per article
│   │   ├── Articles with zero evidence
│   │   ├── Evidence diversity score (per kb-compile)
│   │   └── Source variety (unique source domains)
│   ├── Connection metrics
│   │   ├── Connection document count
│   │   ├── Articles with connections vs without
│   │   ├── Connection density (connections / articles)
│   │   └── Cross-topic connection count
│   └── Compute topic health score and status
├── Aggregate dashboard
│   ├── Overall KB health score (weighted average)
│   ├── Topic status distribution (RED/YELLOW/GREEN counts)
│   ├── Worst-performing topics (bottom 5)
│   ├── Best-performing topics (top 5)
│   ├── Trend comparison (vs previous dashboard if exists)
│   └── Actionable recommendations
└── Save to knowledge-bases/_dashboard/dashboard-{date}.md
```

## Health Status Thresholds

| Status | Color | Health Score | Meaning |
|---|---|---|---|
| Healthy | 🟢 GREEN | 70-100 | Topic is well-maintained, fresh, linked |
| Attention | 🟡 YELLOW | 40-69 | Some issues — aging content, broken links, or sparse evidence |
| Critical | 🔴 RED | 0-39 | Significant problems — stale, disconnected, or severely under-documented |

## Health Score Calculation

Per-topic health score (0-100) is a weighted composite:

| Dimension | Weight | Score Basis |
|---|---|---|
| Freshness | 30% | Unified freshness score from kb-lint (0-100) |
| Evidence quality | 25% | Evidence density + diversity score |
| Link health | 20% | (1 - broken_link_ratio) × 100 |
| Connection coverage | 15% | Connection density relative to article count |
| Completeness | 10% | Frontmatter completeness + average word count adequacy |

```
topic_health = (freshness × 0.30) + (evidence × 0.25) + (links × 0.20)
             + (connections × 0.15) + (completeness × 0.10)
```

Overall KB health = weighted average of all topic scores, weighted by article count.

## Execution Flow

### Step 1: Enumerate Topics

1. List all directories under `knowledge-bases/` excluding `_` prefixed dirs
2. For each topic, verify `wiki/` directory exists
3. Record topic name and path

### Step 2: Per-Topic Assessment

For each topic, compute metrics across 5 dimensions:

#### 2a: Article Metrics

```yaml
articles:
  concepts_count: {N}
  references_count: {N}
  connections_count: {N}
  total: {N}
  avg_word_count: {N}
  frontmatter_complete: {N}/{total}  # has title, tags, ingested
```

#### 2b: Freshness Metrics

```yaml
freshness:
  newest_article_date: "{YYYY-MM-DD}"
  oldest_article_date: "{YYYY-MM-DD}"
  median_age_days: {N}
  stale_count: {N}  # >90 days since ingested
  stale_ratio: {0.0-1.0}
  unified_score: {0-100}  # per kb-lint unified freshness formula
```

#### 2c: Link Health

```yaml
links:
  total_wikilinks: {N}
  broken_wikilinks: {N}
  broken_ratio: {0.0-1.0}
  orphan_articles: {N}  # no incoming links
  dead_end_articles: {N}  # no outgoing links
  links_per_article: {N.N}
```

#### 2d: Evidence Metrics

```yaml
evidence:
  articles_with_evidence: {N}
  articles_without_evidence: {N}
  avg_evidence_entries: {N.N}
  evidence_diversity_avg: {0.0-1.0}  # per kb-compile diversity scoring
  unique_source_domains: {N}
```

#### 2e: Connection Metrics

```yaml
connections:
  total_connection_docs: {N}
  articles_with_connections: {N}
  articles_without_connections: {N}
  connection_density: {0.0-1.0}
  cross_topic_connections: {N}
```

### Step 3: Compute Health Scores

For each topic, apply the weighted formula to produce a 0-100 score and
assign RED/YELLOW/GREEN status.

### Step 4: Aggregate Dashboard

```yaml
overall:
  total_topics: {N}
  total_articles: {N}
  overall_health_score: {0-100}
  status_distribution:
    green: {N}
    yellow: {N}
    red: {N}
```

### Step 5: Generate Dashboard Document

```markdown
---
title: "KB Coverage Dashboard — {date}"
total_topics: {N}
total_articles: {N}
overall_health: {score}
overall_status: "{GREEN/YELLOW/RED}"
green_count: {N}
yellow_count: {N}
red_count: {N}
dashboard_date: "{YYYY-MM-DD}"
---

# KB Coverage Dashboard — {date}

## Overall Health

**Score:** {score}/100 {status_emoji}
**Topics:** {N} total ({green} 🟢 / {yellow} 🟡 / {red} 🔴)
**Articles:** {N} total across all topics

## Status Distribution

```
🟢 GREEN  ({N} topics): ████████████░░░░ {%}%
🟡 YELLOW ({N} topics): ████░░░░░░░░░░░░ {%}%
🔴 RED    ({N} topics): ██░░░░░░░░░░░░░░ {%}%
```

## Critical Topics (🔴 RED)

| Topic | Score | Articles | Stale % | Broken Links | Evidence Gap | Action Needed |
|---|---|---|---|---|---|---|
| {topic} | {score} | {N} | {%} | {N} | {%} | {recommendation} |

## Attention Topics (🟡 YELLOW)

| Topic | Score | Top Issue | Quick Win |
|---|---|---|---|
| {topic} | {score} | {issue} | {action} |

## Healthy Topics (🟢 GREEN)

| Topic | Score | Articles | Last Updated |
|---|---|---|---|
| {topic} | {score} | {N} | {date} |

## Top 5 Best

| Rank | Topic | Score | Strength |
|---|---|---|---|
| 1 | {topic} | {score} | {why it scores well} |

## Bottom 5 Worst

| Rank | Topic | Score | Primary Issue |
|---|---|---|---|
| 1 | {topic} | {score} | {main problem} |

## Dimension Breakdown (All Topics)

### Freshness

| Topic | Newest | Median Age | Stale % | Freshness Score |
|---|---|---|---|---|
| {topic} | {date} | {days} | {%} | {score}/100 |

### Evidence Quality

| Topic | Avg Entries | Zero Evidence | Diversity | Sources |
|---|---|---|---|---|
| {topic} | {N.N} | {N} | {score} | {N} |

### Link Health

| Topic | Total Links | Broken | Orphans | Dead-ends | Density |
|---|---|---|---|---|---|
| {topic} | {N} | {N} | {N} | {N} | {N.N} |

### Connection Coverage

| Topic | Connections | Density | Cross-topic | Unconnected Articles |
|---|---|---|---|---|
| {topic} | {N} | {score} | {N} | {N} |

### Completeness

| Topic | Frontmatter Complete | Avg Word Count | Adequacy |
|---|---|---|---|
| {topic} | {%} | {N} | {score} |

## Trend (vs Previous Dashboard)

{If a prior dashboard exists, show delta:}

| Metric | Previous | Current | Delta |
|---|---|---|---|
| Overall score | {N} | {N} | {+/-N} |
| GREEN topics | {N} | {N} | {+/-N} |
| RED topics | {N} | {N} | {+/-N} |
| Total articles | {N} | {N} | {+/-N} |

## Recommendations

### Immediate Actions (This Week)

1. {Highest-impact recommendation for RED topics}
2. {Second recommendation}
3. {Third recommendation}

### Short-term (This Month)

1. {Recommendation for YELLOW topics}
2. {Evidence gap closure}

### Ongoing

1. {Maintenance recommendation}
2. {Connection building}
```

### Step 6: Save Output

1. Create `knowledge-bases/_dashboard/` directory if it doesn't exist
2. Save to `knowledge-bases/_dashboard/dashboard-{YYYY-MM-DD}.md`
3. Prior dashboards are preserved for trend analysis

## Output Format

| Artifact | Location | Description |
|---|---|---|
| Dashboard report | `_dashboard/dashboard-{date}.md` | Full dashboard with frontmatter |
| Optional HTML | stdout via `visual-explainer` | Interactive visual dashboard |

## Composability

- **kb-lint**: Freshness scores, broken link counts, evidence validation feed directly into dashboard metrics
- **kb-compile**: Evidence diversity scores from compile step are consumed by the dashboard
- **wiki-connection-discoverer**: Connection metrics from discovery runs feed connection coverage dimension
- **kb-daily-report**: KB Health Snapshot section is a lightweight daily version of this dashboard
- **visual-explainer**: Optional HTML rendering for interactive dashboard visualization
- **kb-orchestrator**: Can trigger dashboard generation as part of the `status` or `enhance` mode

## Constraints

- Topics without a `wiki/` directory are skipped with a warning
- Topics with zero articles are included but scored 0 (RED)
- Prior dashboards are never overwritten; each run creates a new dated file
- The `_dashboard/` directory is shared across all topics
- Health score formula weights are fixed in this version; future versions may support configurable weights
- Trend comparison only works when a prior dashboard exists in `_dashboard/`
- All narrative sections are in Korean; metric labels and topic names remain in English

## Examples

### Example 1: Full KB dashboard

**Trigger:** User says: "KB 대시보드 생성해줘"

**Actions:** (1) Enumerate all topics under `knowledge-bases/`. (2) Compute per-topic health scores across 5 dimensions. (3) Aggregate into overall KB health score. (4) Generate dashboard report with RED/YELLOW/GREEN status. (5) Save to `knowledge-bases/_dashboard/dashboard-{date}.md`.

**Result:** Dated dashboard markdown with per-topic cards and overall score.

### Example 2: Trend comparison

**Trigger:** User says: "KB health compared to last month"

**Actions:** (1) Generate current dashboard. (2) Load previous dashboard from `_dashboard/`. (3) Compute deltas for all metrics. (4) Highlight improving and declining topics.

**Result:** Current dashboard plus trend section; if no prior file, note baseline (see Error Handling).

## Error Handling

| Error | Action |
|-------|--------|
| `knowledge-bases/` directory not found | Report error: "KB root directory not found at expected path" |
| Topic has `wiki/` but zero articles | Include in dashboard with score 0 and RED status |
| `_dashboard/` directory doesn't exist | Create it automatically |
| Previous dashboard not found for trend comparison | Skip trend section and note "baseline established" |
| Metrics computation fails for a topic | Report partial results for that topic and continue |

## Gotchas

- **Symptom:** Overall score looks fine while small topics are broken. **Root cause:** Overall score weighted by article count; one large topic dominates. **Correct approach:** Always read per-topic cards; flag small-topic RED even when aggregate is GREEN.
- **Symptom:** "Stale" freshness on still-accurate pages. **Root cause:** Freshness is time-based, not truth-based. **Correct approach:** Present dashboard as maintenance signal, not a verdict on factual correctness.
- **Symptom:** Low coverage despite rich `raw/`. **Root cause:** Dashboard reflects `wiki/` only, not uncompiled raw. **Correct approach:** Mention compile backlog in recommendations when `raw/` exists without matching wiki depth.

## Output Discipline

- Do not generate visual embellishments (charts, graphs) inline — defer to `visual-explainer` for HTML rendering.
- Do not editorialize beyond the health score bands — "RED" means "below threshold", not "bad team".
- Dashboard should be reproducible — same input produces same output.

## Honest Reporting

- Report all topics including those with perfect scores — do not filter to "only problems".
- When overall health is RED, lead with this finding rather than burying it under per-topic details.
- If the health score improved but a critical topic degraded, highlight the degradation prominently.
