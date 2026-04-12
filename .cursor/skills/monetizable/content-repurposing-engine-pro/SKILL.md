---
name: content-repurposing-engine-pro
version: 1.0.0
description: >
  Transforms long-form content into 10 platform-specific formats with hook generation,
  quality scoring, batch mode, and visual dashboard. Extends content-repurposing-engine
  with density compression, per-platform hooks, length validation, and file-first output.
  Use when the user asks to "repurpose for all platforms", "10-platform content kit",
  "batch repurpose", "content-repurposing-engine-pro", "콘텐츠 킷 생성", "10채널 콘텐츠",
  "콘텐츠 일괄 변환", "멀티 플랫폼 콘텐츠 킷", or wants scored multi-platform content
  from a single source. Do NOT use for single-platform repurposing (use
  content-repurposing-engine). Do NOT use for podcast repurposing (use
  marketing-podcast-ops). Do NOT use for brand voice (use kwp-brand-voice). Do NOT use
  for slides only (use anthropic-pptx). Do NOT use for document rewriting (use
  prompt-transformer).
tags: [content, repurposing, multi-platform, monetizable, batch, scoring]
triggers:
  - "10-platform content kit"
  - "content kit from article"
  - "repurpose for all platforms"
  - "batch repurpose"
  - "content-repurposing-engine-pro"
  - "multi-platform content kit"
  - "scored content repurposing"
  - "콘텐츠 킷 생성"
  - "10채널 콘텐츠"
  - "콘텐츠 일괄 변환"
  - "플랫폼별 콘텐츠"
  - "멀티 플랫폼 콘텐츠 킷"
do_not_use:
  - "For single-platform repurposing without scoring (use content-repurposing-engine)"
  - "For podcast episode repurposing (use marketing-podcast-ops)"
  - "For brand voice enforcement (use kwp-brand-voice-brand-voice-enforcement)"
  - "For slide deck creation only (use anthropic-pptx)"
  - "For full document rewriting (use prompt-transformer)"
composes:
  - content-repurposing-engine
  - long-form-compressor
  - defuddle
  - hook-generator
  - sentence-polisher
  - visual-explainer
  - batch-agent-runner
metadata:
  author: "thaki"
  category: "monetizable"
  mrr_target: "$2K-$5K"
---

# Content Repurposing Engine Pro

Transform one piece of long-form content into 10 platform-optimized formats with hook generation, quality scoring, and a visual dashboard.

## When to Use

- A single article, report, or transcript needs distribution across 10 platforms
- The user needs a scored, quality-gated content kit (not just raw conversions)
- Batch processing of multiple source documents into content kits
- Content marketing teams need a repeatable one-to-many pipeline with artifact persistence

## Output Artifacts

| Phase | Stage Name         | Output File                                              |
| ----- | ------------------ | -------------------------------------------------------- |
| 1     | Ingest             | `outputs/content-repurposing-engine-pro/{date}/source-extract.md` |
| 2     | Compress           | `outputs/content-repurposing-engine-pro/{date}/density-levels.md` |
| 3     | Hooks              | `outputs/content-repurposing-engine-pro/{date}/hooks.md`          |
| 4     | Transform          | `outputs/content-repurposing-engine-pro/{date}/platforms/*.md`    |
| 5     | Quality            | `outputs/content-repurposing-engine-pro/{date}/quality-scores.md` |
| 6     | Deliver            | `outputs/content-repurposing-engine-pro/{date}/content-kit.md`    |
| 6     | Dashboard          | `outputs/content-repurposing-engine-pro/{date}/dashboard.html`    |
| 6     | Manifest           | `outputs/content-repurposing-engine-pro/{date}/manifest.json`     |

## Workflow

### Phase 1: Ingest Source Content

Accept source content in any form:
- **URL**: Extract via `defuddle` (strips noise, returns clean markdown)
- **File path**: Read directly
- **Pasted text**: Accept inline
- **Notion URL**: Fetch via Notion MCP

Extract these elements and save to `source-extract.md`:

| Element | Description |
|---------|-------------|
| Core thesis | Single main argument or insight (1 sentence) |
| Key points | 3-7 supporting points with evidence |
| Data/stats | Quantitative claims with sources |
| Quotes | Memorable phrases or expert quotes |
| Narrative arc | Problem → Insight → Implication |
| Target audience | Who the original content addresses |
| Word count | Source length for compression ratio calculation |

### Phase 2: Compress to Density Levels

Run `long-form-compressor` patterns to create 3 density levels. Save to `density-levels.md`:

| Level | Target | Use |
|-------|--------|-----|
| Full summary | 300-500 words | Blog, newsletter, podcast notes |
| 1-paragraph | 80-120 words | LinkedIn, email snippet |
| 1-sentence | 15-25 words | Twitter hook, Instagram opening |

### Phase 3: Generate Hooks

For each target platform, generate 2-3 hooks using `hook-generator` frameworks. Save to `hooks.md`:

| Framework | When to Use |
|-----------|-------------|
| Curiosity gap | Data-rich content with surprising findings |
| Data shock | Content with counterintuitive statistics |
| Contrarian claim | Content that challenges conventional wisdom |
| Story open | Content with a strong narrative example |
| Direct challenge | Content with an actionable recommendation |

Select the strongest hook per platform based on platform culture fit.

### Phase 4: Transform to 10 Platforms

Generate each platform output using `content-repurposing-engine` core logic, extended with platform-specific constraints. Save each to `platforms/{platform-name}.md`:

| # | Platform | Format | Constraints |
|---|----------|--------|-------------|
| 1 | Twitter/X thread | 5-7 tweets | 280 chars/tweet, hook in tweet 1, CTA in last |
| 2 | LinkedIn post | Long-form | 1200 chars max, professional tone, hook + story + CTA |
| 3 | Newsletter section | Article | 300 words, scannable headers, 1 CTA |
| 4 | Blog summary | Short post | 500 words, SEO-friendly title, meta description |
| 5 | Instagram caption | Visual-first | 2200 chars max, emoji-friendly, 5-10 hashtags |
| 6 | YouTube Shorts script | Video script | 60s, visual cues, spoken pacing marks |
| 7 | TikTok script | Video script | 30s, trend-hook opening, fast cuts |
| 8 | Email snippet | Outbound | 150 words, subject line, preview text, 1 link |
| 9 | Podcast show notes | Audio companion | 200 words, timestamps placeholder, key quotes |
| 10 | Slide deck outline | Presentation | 5 slides: hook, problem, insight, evidence, CTA |

For each output, apply `sentence-polisher` if the content is Korean.

### Phase 5: Quality Check

Score each platform output on 4 dimensions (1-10 scale). Save to `quality-scores.md`:

| Dimension | What It Measures |
|-----------|-----------------|
| Platform fit | Does format match platform norms? |
| Hook strength | Does the opening stop the scroll? |
| CTA presence | Is there a clear call to action? |
| Length compliance | Does it fit platform constraints? |

Flag any output scoring below 6 on any dimension for revision. Re-generate flagged outputs once.

### Phase 6: Deliver

1. Compile all platform outputs into `content-kit.md` (single file with all 10 outputs, separated by H2 headers)
2. Generate `dashboard.html` via `visual-explainer` showing:
   - Source summary
   - All 10 platform outputs in tabs or cards
   - Quality scores as a radar or bar chart
3. Write `manifest.json` with file paths, timestamps, quality scores, and source metadata
4. Optionally push `content-kit.md` to Notion via `md-to-notion`

## Batch Mode

When processing multiple source documents:
1. Accept a list of URLs or file paths
2. Process each through Phases 1-6 sequentially
3. Create a batch manifest at `outputs/content-repurposing-engine-pro/{date}/batch-manifest.json`

## Examples

### Example 1: Full 10-platform kit from a blog post

User says: "Repurpose this article for all platforms"

Actions:
1. Extract content from URL via defuddle
2. Generate 10 platform-specific versions with hooks and density compression
3. Score each output against platform-specific rubrics
4. Save all formats + dashboard to `outputs/content-repurposing-engine-pro/{date}/`

Result: 10 formatted content pieces, quality scorecard HTML, and manifest.json

### Example 2: Batch mode from a folder

User says: "Batch repurpose all articles in docs/blog/"

Actions:
1. Glob `docs/blog/*.md`, queue each through batch-agent-runner
2. Generate 10 platform kits per article in parallel
3. Aggregate scores into a batch summary dashboard

Result: Per-article output folders + batch-summary.html

## Error Handling

If Phase 4 fails for a specific platform, the remaining platforms continue. The failed platform is logged in `manifest.json` with `status: "failed"` and error details. Re-run from Phase 4 for the failed platform only.

## Gotchas

- Twitter thread numbering must use "1/" format, not "(1/7)"
- LinkedIn posts exceeding 1300 chars get truncated in feed preview; keep hook in first 210 chars
- Instagram hashtags count toward the 2200 char limit
- YouTube Shorts scripts must account for 2-3s of hook before content
- Podcast show notes need "[TIMESTAMP]" placeholders since actual timestamps depend on recording
