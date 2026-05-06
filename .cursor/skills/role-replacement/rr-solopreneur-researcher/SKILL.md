---
name: rr-solopreneur-researcher
version: 1.0.0
description: >-
  Role Replacement Case Study: Solopreneur Research Assistant — autonomous market research,
  competitor analysis, and trend scouting pipeline that replaces a dedicated research hire.
  Thin harness composing parallel-web-search, kb-ingest, defuddle, alphaear-search, and
  feynman-source-comparison into a unified research role pipeline with KB-first persistence
  and structured insight extraction.
tags: [role-replacement, harness, research, solopreneur, market-research]
triggers:
  - rr-solopreneur-researcher
  - research agent
  - solopreneur research
  - 리서치 에이전트
  - 시장 조사 에이전트
  - 1인 기업 리서치
  - market research agent
  - competitor research agent
do_not_use:
  - Full academic paper review with PM analysis (use paper-review)
  - HuggingFace trending intelligence (use hf-trending-intelligence)
  - Daily stock analysis or trading signals (use today or daily-stock-check)
  - Single URL content extraction without research pipeline (use defuddle directly)
  - General KB query without new research intent (use kb-query)
composes:
  - parallel-web-search
  - kb-ingest
  - defuddle
  - alphaear-search
  - feynman-source-comparison
  - kb-compile
  - kb-query
  - evaluation-engine
  - long-form-compressor
---

# Role Replacement: Solopreneur Research Assistant

Thin harness that replaces a dedicated research hire for solo founders and small teams
by orchestrating existing research and knowledge skills into a 4-phase pipeline with
KB-first persistence and structured insight extraction.

## What This Replaces

| Human Researcher Task | Automated By | Skill |
|---|---|---|
| Market landscape scanning | Multi-provider parallel web search | `parallel-web-search` |
| Competitor product/pricing monitoring | Finance-specific search + web extraction | `alphaear-search` + `defuddle` |
| Trend report compilation | Cross-source comparison with evidence matrix | `feynman-source-comparison` |
| Research asset archival | Markdown-first KB ingestion with YAML frontmatter | `kb-ingest` |
| Insight synthesis | KB compilation with cross-references | `kb-compile` |
| Research quality scoring | Multi-dimension rubric evaluation | `evaluation-engine` |

## Prerequisites

- Web search available (WebSearch tool or parallel-web-search configured)
- Knowledge Base topic directory exists (e.g., `knowledge-bases/competitive-intel/`)
- No API keys required for core pipeline (web search uses built-in providers)

## Architecture

```
Phase 1: COLLECT (parallel)
  ├── parallel-web-search (3-5 queries, multi-provider)
  ├── alphaear-search (finance/industry-specific sources)
  └── defuddle (extract clean content from discovered URLs)

Phase 2: ANALYZE (sequential)
  ├── feynman-source-comparison (cross-source agreement/disagreement matrix)
  └── evaluation-engine (score research quality: coverage, freshness, depth)

Phase 3: PERSIST (sequential)
  ├── kb-ingest (save raw sources with YAML frontmatter to KB topic)
  └── kb-compile (update wiki with new findings, cross-references)

Phase 4: SYNTHESIZE (sequential)
  ├── long-form-compressor (executive summary from full findings)
  └── Output: structured Korean research brief
```

## Execution Modes

### Mode 1: Topic Research (default)
```
Input: "리서치 에이전트 실행: [TOPIC]"
Output: KB-persisted research + Korean executive brief
```

### Mode 2: Competitor Deep-Dive
```
Input: "경쟁사 분석: [COMPANY/PRODUCT]"
Output: Competitor profile with pricing, features, positioning, gaps
```

### Mode 3: Trend Scout
```
Input: "트렌드 스캐닝: [DOMAIN]"
Output: Emerging signals ranked by evidence strength
```

## Phase Details

### Phase 1: Collect

1. Parse user intent to extract research topic, scope, and depth
2. Generate 3-5 diverse search queries (Korean + English)
3. Fan-out:
   - `parallel-web-search`: broad market/industry queries
   - `alphaear-search`: finance/pricing/market-data queries
4. For top-10 URLs from search results, run `defuddle` to extract clean markdown
5. Persist raw extractions to `/tmp/research-{date}/` for Phase 2 input

### Phase 2: Analyze

1. Feed all collected sources to `feynman-source-comparison`
   - Identify agreements (consensus signals)
   - Flag disagreements (conflicting data points)
   - Score confidence per claim
2. Run `evaluation-engine` with research-quality rubric:
   - Coverage (0-10): breadth of sources
   - Freshness (0-10): recency of data
   - Depth (0-10): specificity of findings
   - Actionability (0-10): clarity of implications
3. If composite score < 6/10, loop back to Phase 1 with refined queries (max 1 retry)

### Phase 3: Persist

1. Select KB topic based on research domain:
   - Market/competitor → `competitive-intel`
   - Technology/trend → `intelligence` or relevant topic
   - Industry/pricing → `sales-playbook` or `finance-policies`
2. Run `kb-ingest` for each high-value source (score >= 7)
3. Run `kb-compile` to update wiki with new articles and cross-references

### Phase 4: Synthesize

1. Compile all findings into a structured research document
2. Run `long-form-compressor` for executive summary (bullet brief format)
3. Output format:

```markdown
## 리서치 결과: [TOPIC]

### 핵심 발견 (Executive Summary)
- [3-5 bullet points]

### 상세 분석
#### 시장 현황
#### 주요 플레이어
#### 트렌드 & 시그널
#### 기회 & 리스크

### 데이터 품질
- 소스 수: N개
- 신선도: YYYY-MM 기준
- 신뢰도 점수: X/10

### 다음 단계 제안
- [actionable next steps]
```

## Overlap & Differentiation

| Existing Agent | Overlap Area | Differentiation |
|---|---|---|
| `rr-market-research-analyst` | Market data, competitor analysis | This agent focuses on solopreneur-scale research without trading/quant context |
| `rr-knowledge-strategist` | KB persistence, wiki compilation | This agent is research-first; KS is consolidation-first |
| `rr-content-curator` | Web source collection | This agent analyzes and synthesizes; CC routes to Slack channels |

## Error Handling

- Search returns < 3 results → expand query scope, add alternative keywords
- defuddle fails on URL → skip and note in report, continue with other sources
- KB topic doesn't exist → create minimal topic structure before ingesting
- evaluation-engine score < 4 → abort with "insufficient data" report + suggested manual queries

## Invocation Examples

```
"리서치 에이전트: AI GPU 클라우드 시장 현황 2026"
"research agent: competitor analysis for serverless inference platforms"
"시장 조사 에이전트: 한국 MSP 시장 규모 및 주요 플레이어"
"solopreneur research: pricing strategies of vLLM hosting providers"
```
