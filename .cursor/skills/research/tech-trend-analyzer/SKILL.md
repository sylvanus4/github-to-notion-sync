---
name: tech-trend-analyzer
description: >-
  Analyze technology trend content (tweets, articles, GitHub projects, demos)
  through a 4-phase pipeline: content extraction, structured 6-dimension analysis,
  optional deep-dive (first-principles / competitive comparison / role-perspective),
  and multi-channel distribution (KB, Slack, Notion).
  Use when the user asks to "analyze this tech trend", "tech trend analysis",
  "기술 트렌드 분석", "오픈소스 프로젝트 분석", "tech-trend-analyzer",
  "analyze this project", "evaluate this technology", "기술 평가",
  "/tech-trend", or shares a URL or content about a new technology, open-source
  project, or industry trend that needs structured evaluation.
  Do NOT use for daily stock analysis (use daily-stock-check).
  Do NOT use for academic paper review (use paper-review).
  Do NOT use for HuggingFace trending scan (use hf-trending-intelligence).
  Do NOT use for single tweet posting without analysis (use x-to-slack).
  Do NOT use for general web research without tech evaluation (use parallel-web-search).
metadata:
  author: thaki
  version: 1.0.0
  category: research
---

# Tech Trend Analyzer

Structured analysis pipeline for evaluating technology trends, open-source
projects, and industry shifts. Produces a scored assessment across 6 fixed
dimensions, stores results in a knowledge base, and distributes findings to
Slack and optionally Notion.

## Output Language

All outputs MUST be in Korean. Technical terms may remain in English.

## Prerequisites

- `defuddle` CLI or WebFetch for URL content extraction
- `SLACK_BOT_TOKEN` in `.env` for Slack posting
- Knowledge base directory `knowledge-bases/tech-trends/` initialized

## Composing Skills

| Skill | Phase | Purpose |
|-------|-------|---------|
| `defuddle` | 1 | URL content extraction |
| `parallel-web-search` | 1 | GitHub, demo, related article research |
| `first-principles-analysis` | 3 | Architecture decomposition (optional) |
| `feynman-source-comparison` | 3 | Competitive comparison table (optional) |
| `role-cto` / `role-dispatcher` | 3 | Strategic perspective analysis (optional) |
| `kb-ingest` | 4 | Knowledge base ingestion |
| `md-to-notion` | 4 | Notion publishing (optional) |
| `decision-router` | 4 | Action item routing |
| `content-repurposing-engine` | 4 | Multi-platform adaptation (optional) |

## Pipeline Overview

```
Phase 1: Content Extraction    → outputs/tech-trends/{date}/{slug}-extracted.md
Phase 2: Structured Analysis   → outputs/tech-trends/{date}/{slug}-analysis.md
Phase 3: Deep Dive (Optional)  → outputs/tech-trends/{date}/{slug}-deep-dive.md
                               → outputs/tech-trends/{date}/{slug}-comparison.md
Phase 4: Output & Distribution → Slack thread + KB entry + optional Notion page
```

## Output Artifacts

| Phase | Stage Name | Output File | Skip Flag |
|-------|------------|-------------|-----------|
| 1 | Content Extraction | `outputs/tech-trends/{date}/{slug}-extracted.md` | — |
| 2 | Structured Analysis | `outputs/tech-trends/{date}/{slug}-analysis.md` | — |
| 3a | First Principles | `outputs/tech-trends/{date}/{slug}-deep-dive.md` | `--skip-deep` |
| 3b | Competitive Comparison | `outputs/tech-trends/{date}/{slug}-comparison.md` | `--skip-deep` |
| 4 | KB Raw Entry | `knowledge-bases/tech-trends/raw/{slug}.md` | `--skip-kb` |

## Flags

| Flag | Effect |
|------|--------|
| `--deep` | Force deep-dive analysis regardless of relevance score |
| `--skip-kb` | Skip knowledge base ingestion |
| `--skip-slack` | Skip Slack posting |
| `--skip-notion` | Skip Notion publishing (default: skipped unless explicitly requested) |
| `--with-notion` | Enable Notion publishing |
| `--with-roles` | Trigger full role-dispatcher analysis |

---

## Phase 1: Content Extraction

### Step 1a: Input Type Detection

Determine input type:
- **URL** (x.com, twitter.com, github.com, any web URL): Use `defuddle` or FxTwitter API
- **Pasted text/content**: Use directly, skip extraction
- **Tweet URL**: Convert to FxTwitter API URL, extract tweet data

### Step 1b: Primary Content Extraction

For URLs:
1. Use `defuddle` (or `WebFetch` as fallback) to extract clean markdown
2. For tweet URLs: replace `x.com`/`twitter.com` with `api.fxtwitter.com`, fetch JSON, extract `tweet.text`, `tweet.author`, engagement metrics

For pasted content:
1. Use the text as-is
2. Extract any embedded URLs for additional research

### Step 1c: Supplementary Web Research

Run `parallel-web-search` (or multiple `WebSearch` calls) for:
1. The project's GitHub repository (stars, contributors, last commit, license)
2. Official demo or documentation site
3. Recent articles or discussions (Hacker News, Reddit, industry blogs)
4. Competitor or alternative solutions (at least 3)

Persist extracted content to `outputs/tech-trends/{date}/{slug}-extracted.md`.

---

## Phase 2: Structured Analysis

Analyze the extracted content across **6 fixed dimensions**. Read extracted
content from the Phase 1 output file.

### Dimension 1: Tech Stack Decomposition

| Aspect | Details |
|--------|---------|
| Core Languages | List primary languages and versions |
| Frameworks | Key frameworks and their roles |
| Architecture Pattern | ECS, MVC, microservices, monolith, etc. |
| Infrastructure | Cloud, browser, desktop, mobile |
| Build System | Monorepo structure, CI/CD, package management |
| Notable Innovations | Non-obvious technical decisions worth studying |

### Dimension 2: Market Context

| Aspect | Details |
|--------|---------|
| Problem Being Solved | What pain point does this address? |
| Existing Solutions | Incumbent tools and their pricing |
| Target Market | Who benefits most? |
| Business Model | Open-source, SaaS, freemium, enterprise |
| Market Size Indicators | Pricing of alternatives, number of potential users |
| Disruption Potential | Does this fundamentally change the economics? |

### Dimension 3: Competitive Landscape

Create a comparison table with at least 3 alternatives:

| Feature | Subject | Competitor A | Competitor B | Competitor C |
|---------|---------|--------------|--------------|--------------|
| License | | | | |
| Pricing | | | | |
| Platform | | | | |
| Key Strength | | | | |
| Key Weakness | | | | |
| Maturity | | | | |

### Dimension 4: ThakiCloud Relevance Score

Score 0-10 using weighted criteria:

| Criterion | Weight | Score (0-10) | Weighted |
|-----------|--------|--------------|----------|
| Tech Applicability | 40% | — | — |
| Market Trend Alignment | 30% | — | — |
| Strategic Implications | 30% | — | — |
| **Total** | **100%** | — | **X.X** |

**Scoring guidelines**:
- **Tech Applicability** (40%): Can the architecture, patterns, or specific
  technologies be directly applied to ThakiCloud products? Score 8+ only if
  a concrete integration scenario exists.
- **Market Trend Alignment** (30%): Does this validate or challenge ThakiCloud's
  market assumptions? Does it reveal a trend ThakiCloud should respond to?
- **Strategic Implications** (30%): Does this change competitive dynamics,
  open new opportunities, or create threats for ThakiCloud?

**Classification**:
- Score >= 8: **HIGH** — immediate action recommended
- Score 5-7: **MEDIUM** — monitor and revisit quarterly
- Score < 5: **LOW** — archive for reference

### Dimension 5: Risk and Limitations

Assess at least 4 risk factors:

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Technical maturity | HIGH/MED/LOW | HIGH/MED/LOW | — |
| Browser/platform support | | | |
| Community sustainability | | | |
| Performance at scale | | | |

### Dimension 6: Actionable Insights

Generate **specific, time-bound** action items. Each item MUST include:
- **What**: Concrete action (not "research further")
- **Who**: Responsible team or role
- **When**: Deadline (within 7 days for immediate, 30 days for medium-term)
- **Success Metric**: How to measure completion

Persist analysis to `outputs/tech-trends/{date}/{slug}-analysis.md`.

---

## Phase 3: Deep Dive (Optional)

Trigger conditions (any of these, or `--deep` flag):

### 3a: First-Principles Analysis (if relevance score >= 7)

Invoke `first-principles-analysis` on the subject technology:
- Strip inherited assumptions about the technology domain
- Identify bedrock truths about the underlying problem
- Reconstruct understanding from fundamentals

Save to `outputs/tech-trends/{date}/{slug}-deep-dive.md`.

### 3b: Competitive Source Comparison (if 3+ competitors identified)

Invoke `feynman-source-comparison` with the subject and top 3 competitors:
- Fixed dimensions: Architecture, Performance, Cost, Ecosystem, Limitations
- Agreement/Disagreement matrix
- Confidence levels per dimension

Save to `outputs/tech-trends/{date}/{slug}-comparison.md`.

### 3c: Role-Perspective Analysis (if `--with-roles` or relevance score >= 9)

Invoke `role-cto` for CTO-perspective analysis. If `--with-roles`, invoke
full `role-dispatcher` for 12-role analysis.

Save to `outputs/tech-trends/{date}/{slug}-roles.md`.

---

## Phase 4: Output and Distribution

Read all Phase 2 and Phase 3 output files to assemble final deliverables.

### Step 4a: Knowledge Base Ingestion (unless `--skip-kb`)

1. Ensure `knowledge-bases/tech-trends/` exists with `manifest.json`
2. Write raw source + analysis to `knowledge-bases/tech-trends/raw/{slug}.md`
   with YAML frontmatter:
   ```yaml
   ---
   title: "{Subject Name}"
   source_url: "{URL}"
   date_analyzed: "{YYYY-MM-DD}"
   relevance_score: X.X
   classification: "HIGH/MEDIUM/LOW"
   tags: [tag1, tag2, tag3]
   ---
   ```
3. Update `manifest.json` with the new entry

### Step 4b: Slack Distribution (unless `--skip-slack`)

Post a 3-part thread to `#deep-research-trending` (channel ID: `C0AN34G4QHK`):

**Message 1 (Header)**:
```
:mag: 기술 트렌드 분석: {Subject Name}
관련도: {score}/10 ({classification})
소스: {source_url}
```

**Message 2 (Analysis Summary)** — reply in thread:
```
:gear: 기술 스택: {key technologies}
:office: 시장 컨텍스트: {market summary}
:chart_with_upwards_trend: 경쟁 환경: {competitive position}
:warning: 리스크: {top 2 risks}
```

**Message 3 (Action Items)** — reply in thread:
```
:pushpin: 액션 아이템
1. {action 1} — {who} — {when}
2. {action 2} — {who} — {when}
3. {action 3} — {who} — {when}
```

### Step 4c: Notion Publishing (only with `--with-notion`)

Use `md-to-notion` to publish the full analysis report as a Notion page.

### Step 4d: Decision Router

Invoke `decision-router` to check if any action items qualify as decisions
requiring routing to `#효정-의사결정` or `#ai-리더방`.

---

## Error Recovery

- If Phase 1 fails (URL inaccessible): report error, suggest pasting content directly
- If Phase 2 fails: Phase 1 output at `outputs/tech-trends/{date}/{slug}-extracted.md` remains valid; fix and re-run Phase 2
- If Phase 3 fails: Phase 2 analysis is complete and usable; skip deep-dive and proceed to Phase 4
- If Slack posting fails: verify `SLACK_BOT_TOKEN`, check channel ID, retry once

## Gotchas

- FxTwitter API may rate-limit; fall back to `defuddle` for tweet URLs
- GitHub repo URLs need `github.com/{org}/{repo}` format for star/contributor lookup
- ThakiCloud relevance scoring: resist the temptation to score everything high — follow the guardrails in `tech-trend-guardrails.mdc`
- Slack channel `#deep-research-trending` is **private** — use the channel ID `C0AN34G4QHK` directly
- When running `parallel-web-search`, limit to 3-4 queries to avoid excessive token usage
