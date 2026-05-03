---
name: kb-collect-research
description: >-
  Daily collector for Research KB. Monitors HuggingFace trending papers, arXiv
  feeds for AI/ML/LLM topics, and research community signals. Feeds into
  existing research-focused KBs. Use when the user asks to "collect research
  data", "update research KB", "연구 KB 수집", "논문 수집", "kb-collect-research", or
  when invoked by kb-daily-build-orchestrator. Korean triggers: "연구 KB 수집",
  "논문 수집", "AI 리서치 수집".
---

# KB Collect Research — Daily Research Intelligence Collector

Automated daily collector for AI/ML research papers, HuggingFace trending content, and research community signals. Feeds into existing research-related KBs.

## Prerequisites

- WebSearch tool available
- `knowledge-bases/_config/social-feeds.yaml` — research Twitter accounts and arXiv RSS feeds

## Collection Window

> **NEWS_WINDOW_DAYS=3** — All external content searches (HF papers, arXiv feeds, community signals) use a 3-day rolling window. This ensures papers published on weekends or late evenings are not missed.

## Deduplication (collector-side)

Before writing any raw file, check existing files in the target `raw/` directory from the last 3 days:

1. **Scan** all `*.md` files in `knowledge-bases/{topic}/raw/` with dates within the last 3 days (based on filename `{date}-` prefix).
2. **Parse YAML frontmatter** of each file to extract `source` (URL or arXiv ID) and `title`.
3. **Skip** writing a new file if either condition matches:
   - Same `source` URL/arXiv ID already exists in any file from the last 3 days.
   - Same `title` (case-insensitive, trimmed) already exists in any file from the last 3 days.
4. **Track** the count of skipped items and report as `dedup_skipped` in the collector summary returned to the orchestrator.

> For arXiv papers: extract the paper ID from the URL (e.g., `2401.12345`) for more reliable dedup matching.

## Workflow

### Phase 1: HuggingFace Daily Papers

1. WebSearch for "huggingface papers" or use HF papers API (last 3 days).
2. Filter for papers relevant to: LLM, multi-agent, GPU optimization, inference.
3. Save top 5 paper summaries to `knowledge-bases/product-strategy/raw/{date}-hf-papers.md`.

### Phase 2: arXiv Feed Monitor

1. Check RSS feeds from `social-feeds.yaml` → `research.rss_feeds` (cs.AI, cs.CL, cs.LG).
2. Filter by relevance keywords: "agent", "LLM", "inference", "GPU", "kubernetes", "platform".
3. Save relevant paper summaries to `knowledge-bases/product-strategy/raw/{date}-arxiv-digest.md`.

### Phase 3: Research Community Signals

1. Monitor `social-feeds.yaml` → `research.twitter_accounts` via WebSearch.
2. Track `research.hashtags` for trending topics.
3. Compile into `knowledge-bases/product-strategy/raw/{date}-research-signals.md`.

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 1 | `knowledge-bases/product-strategy/raw/{date}-hf-papers.md` | HF paper digest |
| 2 | `knowledge-bases/product-strategy/raw/{date}-arxiv-digest.md` | arXiv digest |
| 3 | `knowledge-bases/product-strategy/raw/{date}-research-signals.md` | Community signals |

## Gotchas

- arXiv RSS can be large; filter aggressively by keyword before summarizing.
- HF daily papers endpoint may change; fall back to WebSearch.
- Paper summaries should be 3-5 sentences each, not full abstracts.
