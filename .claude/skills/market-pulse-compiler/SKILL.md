---
name: market-pulse-compiler
description: >-
  Compile time-windowed market intelligence from KB wiki articles into
  structured "Market Pulse" documents. Scans competitive-intel,
  sales-playbook, and product-strategy wikis for articles ingested within a
  configurable time window (default: 7 days), extracts themes, vendor
  snapshots, and cross-cutting patterns, and produces a dated Market Pulse
  report with Evidence Timeline. Use when the user asks to "compile market
  pulse", "weekly market intelligence", "market pulse report", "time-windowed
  market scan", "vendor snapshot", "market theme extraction", "마켓 펄스", "시장
  인텔리전스 컴파일", "주간 시장 보고", "벤더 스냅샷", "시장 테마 추출", "market-pulse-compiler",
  "weekly competitive scan", "market intelligence compilation", "경쟁 동향 정리",
  "시장 펄스 리포트", or wants a structured, periodic market intelligence digest from
  KB data. Do NOT use for real-time news aggregation (use alphaear-news). Do
  NOT use for competitor archetype classification (use
  competitive-archetype-matrix). Do NOT use for cross-topic concept synthesis
  without time window (use kb-cross-topic-synthesizer). Do NOT use for stock
  market analysis (use daily-stock-check).
---

# Market Pulse Compiler

Compile time-windowed market intelligence from KB wiki articles into structured
"Market Pulse" reports with theme extraction and vendor snapshots.

## When to Use

- Weekly or periodic market intelligence compilation from KB data
- Extracting competitive themes from recently ingested wiki articles
- Generating vendor snapshot summaries from competitive-intel KB
- Building Evidence Timeline of market moves within a time window
- User says "market pulse", "마켓 펄스", "주간 시장 보고"

## Do NOT Use

- Real-time news aggregation → `alphaear-news`
- Competitor archetype classification → `competitive-archetype-matrix`
- Cross-topic synthesis without time window → `kb-cross-topic-synthesizer`
- Stock market analysis → `daily-stock-check`

## Architecture

```
Market Pulse Compiler
├── Configure time window (default: 7 days)
├── Scan KB wikis for recently ingested/updated articles
│   ├── competitive-intel/wiki/ (competitor moves, pricing, products)
│   ├── sales-playbook/wiki/ (deal intelligence, win/loss signals)
│   └── product-strategy/wiki/ (market positioning, feature gaps)
├── Extract market signals from each article
│   ├── Vendor/company mentions with action verbs
│   ├── Pricing changes or announcements
│   ├── Product launches or feature updates
│   ├── Partnership or M&A activity
│   ├── Market share shifts or analyst estimates
│   └── Regulatory or policy changes
├── Cluster signals into themes
│   ├── Group related signals by topic (pricing, product, partnerships)
│   ├── Identify cross-cutting themes spanning multiple vendors
│   └── Score theme strength by signal count and source diversity
├── Build vendor snapshots
│   ├── Per-vendor summary of recent activity
│   ├── Signal trend (accelerating, steady, decelerating)
│   └── Relevance to our positioning
├── Compile Evidence Timeline
│   ├── Chronological signal log with dates and sources
│   ├── Theme emergence and evolution tracking
│   └── Gap periods (quiet vendors or topics)
├── Generate Market Pulse document
│   ├── Executive summary with top 3 themes
│   ├── Theme-by-theme analysis
│   ├── Vendor snapshot cards
│   ├── Evidence Timeline table
│   ├── "So What?" implications section
│   └── Recommended actions
└── Save to knowledge-bases/_market-pulse/pulse-{date}.md
```

## Execution Flow

### Step 1: Configure Time Window

Accept parameters:
- `--window`: Number of days to look back (default: 7)
- `--topics`: Override topic list (default: `competitive-intel`, `sales-playbook`, `product-strategy`)
- `--vendors`: Optional vendor filter list

### Step 2: Scan for Recent Articles

For each target topic, find articles matching the time window:

1. Read all files under `{topic}/wiki/concepts/` and `{topic}/wiki/references/`
2. Check frontmatter `ingested` or `compiled_date` field
3. Include articles where date falls within the window
4. Also check `{topic}/raw/` for recently ingested source material

### Step 3: Extract Market Signals

For each qualifying article, extract structured signals:

```yaml
signals:
  - vendor: "AWS"
    action: "launched"
    subject: "GPU instance price cut 20%"
    date: "2024-03-15"
    source_article: "competitive-intel/wiki/concepts/aws-pricing-q1-2024.md"
    signal_type: "pricing"
    relevance: "high"

  - vendor: "GCP"
    action: "announced"
    subject: "TPU v5p general availability"
    date: "2024-03-18"
    source_article: "competitive-intel/wiki/concepts/gcp-tpu-v5p.md"
    signal_type: "product"
    relevance: "medium"
```

Signal types: `pricing`, `product`, `partnership`, `regulatory`, `market_share`, `talent`, `strategy`

### Step 4: Cluster into Themes

Group signals by semantic similarity and type:

```yaml
themes:
  - name: "GPU Price War Intensifying"
    strength: 8  # signal count
    diversity: 3  # unique vendors
    signals: [signal_refs...]
    trend: "accelerating"

  - name: "Inference-First Architecture Shift"
    strength: 5
    diversity: 4
    signals: [signal_refs...]
    trend: "emerging"
```

### Step 5: Build Vendor Snapshots

For each vendor with 2+ signals in the window:

```markdown
### {Vendor Name}

**Activity level:** {High/Medium/Low} ({N} signals)
**Primary moves:** {1-2 sentence summary}
**Trend:** {Accelerating/Steady/Decelerating/New entrant}
**Relevance to us:** {Direct competitor/Adjacent/Ecosystem partner/Peripheral}

| Date | Signal | Type | Source |
|---|---|---|---|
| {date} | {signal summary} | {type} | {article link} |
```

### Step 6: Compile Evidence Timeline

Build a chronological timeline of all signals:

```markdown
## Evidence Timeline

| Date | Vendor | Signal | Theme | Type | Source |
|---|---|---|---|---|---|
| 2024-03-15 | AWS | GPU price cut 20% | GPU Price War | pricing | [link] |
| 2024-03-16 | Azure | Spot instance expansion | GPU Price War | pricing | [link] |
| 2024-03-18 | GCP | TPU v5p GA | Inference Shift | product | [link] |
```

### Step 7: Generate Market Pulse Document

```markdown
---
title: "Market Pulse: {start_date} — {end_date}"
window_days: {N}
topics_scanned: [{topics}]
articles_analyzed: {N}
signals_extracted: {N}
themes_identified: {N}
vendors_tracked: {N}
compiled_date: {YYYY-MM-DD}
---

# Market Pulse: {start_date} — {end_date}

## Executive Summary

**Top 3 themes this period:**

1. 🔥 **{Theme 1}** — {one-line summary} ({N} signals, {trend})
2. 📈 **{Theme 2}** — {one-line summary} ({N} signals, {trend})
3. 🆕 **{Theme 3}** — {one-line summary} ({N} signals, {trend})

**Signal volume:** {N} signals from {N} vendors across {N} articles
**Coverage:** {topics scanned}

## Theme Analysis

### Theme 1: {Name}

**Strength:** {score}/10 | **Trend:** {direction} | **Sources:** {N} articles

{Narrative analysis of the theme with evidence citations}

**Key signals:**
{Bulleted list of signals driving this theme}

### Theme 2: {Name}
{...}

## Vendor Snapshots

{Per-vendor cards from Step 5}

## Evidence Timeline

{Chronological table from Step 6}

## So What? — Implications for Us

{Analysis of what these market moves mean for our positioning, pricing,
product roadmap, and sales strategy. Actionable takeaways.}

## Recommended Actions

| Priority | Action | Owner (Role) | Deadline | Related Theme |
|---|---|---|---|---|
| P1 | {action} | {role} | {date} | {theme} |
| P2 | {action} | {role} | {date} | {theme} |

## Coverage Notes

**Topics with no recent signals:** {list of quiet topics}
**Vendors with no recent signals:** {list of quiet vendors — may indicate gap}
**Articles excluded (outside window):** {count}

## Source Articles

{Numbered list of all articles contributing to this pulse}
```

### Step 8: Save Output

1. Create `knowledge-bases/_market-pulse/` directory if it doesn't exist
2. Save to `knowledge-bases/_market-pulse/pulse-{YYYY-MM-DD}.md`
3. Prior pulse documents are preserved for trend-over-trend comparison

## Output Format

| Artifact | Location | Description |
|---|---|---|
| Market Pulse report | `_market-pulse/pulse-{date}.md` | Full pulse with frontmatter |
| Signal data | stdout or inline | Extracted signal list for downstream consumption |

## Composability

- **kb-search**: Discovers articles within time window
- **kb-query**: Deep-reads articles for signal extraction
- **competitive-archetype-matrix**: Vendor snapshots can feed archetype updates
- **kb-daily-report**: Market Pulse can integrate into the daily intelligence report
- **kb-cross-topic-synthesizer**: Shares cross-topic methodology; pulse adds time dimension
- **anthropic-docx**: Optional DOCX rendering for board distribution

## Constraints

- Minimum time window: 1 day; maximum: 90 days
- Only articles with parseable `ingested` or `compiled_date` frontmatter are included
- Signal extraction is best-effort — complex implicit signals may be missed
- Prior pulse documents are never overwritten; each run creates a new dated file
- The `_market-pulse/` directory is shared across all topics
- All narrative prose is in Korean; vendor names, product names remain in original language

## Examples

### Example 1: Weekly market pulse

**Trigger:** User says: "Generate this week's market pulse"

**Actions:** (1) Scan competitive-intel, sales-playbook, product-strategy wikis for articles from the last 7 days. (2) Extract themes (pricing changes, new features, market moves). (3) Build vendor snapshots with evidence. (4) Identify cross-cutting patterns. (5) Save to `knowledge-bases/_market-pulse/pulse-{date}.md`.

**Result:** Dated pulse file with themes, vendor snapshots, evidence timeline, and coverage notes.

### Example 2: Custom time window

**Trigger:** User says: "지난 30일 시장 동향 컴파일"

**Actions:** (1) Set time window to 30 days. (2) Scan all market-relevant KB topics. (3) Generate extended pulse with monthly trend analysis.

**Result:** Longer-window pulse with proportionally summarized content (respect word cap in Output Discipline).

## Error Handling

| Error | Action |
|-------|--------|
| No articles found within time window | Widen window by 2x and retry; if still empty, report "no recent market data" |
| Single vendor dominates all findings | Note the imbalance and suggest broadening data collection |
| `_market-pulse/` directory doesn't exist | Create it automatically |
| Duplicate articles across topics | Deduplicate by URL/title before theme extraction |

## Gotchas

- **Symptom:** Missing recent articles in the pulse. **Root cause:** `ingested` (or equivalent) frontmatter missing; those articles are excluded. **Correct approach:** Note coverage limits in Honest Reporting; fix metadata at source when possible.
- **Symptom:** Overstated "trends" from thin evidence. **Root cause:** Theme extraction from only 2-3 articles. **Correct approach:** Require at least 3 independent sources before labeling something a theme (see Output Discipline).
- **Symptom:** One-sided vendor narrative. **Root cause:** Reliance on competitor press releases without labeling. **Correct approach:** Flag source type in the evidence trail.

## Output Discipline

- Do not extrapolate trends from fewer than 3 data points.
- Do not include vendor assessments without linked evidence from KB articles.
- Pulse reports should not exceed 3,000 words — summarize aggressively for longer time windows.

## Honest Reporting

- Report data coverage gaps explicitly — e.g. "3 of 7 tracked vendors had no new data this period".
- When a theme contradicts a previous pulse, reference the prior pulse and explain the reversal.
- If market activity was genuinely quiet, produce a short pulse rather than inflating minor events.
