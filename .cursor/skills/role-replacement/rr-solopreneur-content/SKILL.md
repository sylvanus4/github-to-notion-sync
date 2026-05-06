---
name: rr-solopreneur-content
version: 1.0.0
description: >-
  Role Replacement Case Study: Solopreneur Content Producer — autonomous content
  planning, writing, editing, and multi-channel distribution pipeline that replaces
  a dedicated content hire. Thin harness composing content-graph-produce,
  content-repurposing-engine, hook-generator, edit-article, and kwp-marketing-content-creation
  into a unified content role pipeline with Evaluator-Optimizer quality loop and
  platform-native formatting.
tags: [role-replacement, harness, content, solopreneur, marketing]
triggers:
  - rr-solopreneur-content
  - content agent
  - solopreneur content
  - 콘텐츠 에이전트
  - 콘텐츠 제작 에이전트
  - 1인 기업 콘텐츠
  - content production agent
  - multi-channel content agent
do_not_use:
  - Podcast-to-content repurposing with episode structure (use marketing-podcast-ops)
  - Brand voice guideline generation from scratch (use kwp-brand-voice-guideline-generation)
  - Slide deck or presentation creation (use anthropic-pptx or presentation-strategist)
  - Full book-length document editing (use anthropic-docx)
  - Social media scheduling or posting (handle via platform tools)
composes:
  - content-graph-produce
  - content-repurposing-engine
  - hook-generator
  - edit-article
  - kwp-marketing-content-creation
  - content-style-researcher
  - long-form-compressor
  - evaluation-engine
  - sentence-polisher
---

# Role Replacement: Solopreneur Content Producer

Thin harness that replaces a dedicated content hire for solo founders and small teams
by orchestrating existing content and marketing skills into a 4-phase pipeline with
an Evaluator-Optimizer quality loop and multi-channel distribution.

## What This Replaces

| Human Content Role Task | Automated By | Skill |
|---|---|---|
| Content calendar & topic ideation | Knowledge-graph-driven topic generation | `content-graph-produce` |
| Long-form article writing | Channel-specific content drafting | `kwp-marketing-content-creation` |
| Hook/headline creation | Framework-based hook generation (5 proven patterns) | `hook-generator` |
| Article editing & restructuring | Section-level editing with flow improvement | `edit-article` |
| Multi-platform adaptation | 10-platform reformatting with density compression | `content-repurposing-engine` |
| Style consistency enforcement | Sample-based voice DNA extraction and application | `content-style-researcher` |
| Grammar & tone polishing | Bilingual sentence-level quality pass | `sentence-polisher` |

## Prerequisites

- Content Skill Graph initialized (see `content-graph-setup`) OR provide topic + target audience inline
- No API keys required for core pipeline (all LLM-based)
- Optional: brand voice profile at `content-graph/voice/brand-voice.md` for style enforcement

## Architecture

```
Phase 1: PLAN (sequential)
  ├── Parse user intent (topic, audience, platforms, tone)
  ├── content-graph-produce Phase 1-2 (load graph context, generate seed)
  └── hook-generator (3-5 hook candidates per platform)

Phase 2: DRAFT (sequential)
  ├── kwp-marketing-content-creation (long-form primary draft)
  ├── content-style-researcher (apply voice DNA if samples provided)
  └── Output: raw long-form draft

Phase 3: EDIT (Evaluator-Optimizer loop, max 2 iterations)
  ├── evaluation-engine (score: clarity, engagement, accuracy, tone, CTA strength)
  ├── IF score < 7/10:
  │   ├── edit-article (restructure, cut filler, sharpen arguments)
  │   ├── sentence-polisher (grammar, honorifics, flow)
  │   └── Re-evaluate
  └── ELSE: approve draft

Phase 4: DISTRIBUTE (parallel)
  ├── content-repurposing-engine (adapt to 5-10 platforms)
  ├── long-form-compressor (executive summary / TL;DR version)
  └── Output: platform-native content kit
```

## Execution Modes

### Mode 1: Full Pipeline (default)
```
Input: "콘텐츠 에이전트: [TOPIC] 주제로 블로그 + SNS 콘텐츠 만들어줘"
Output: Long-form article + 5-10 platform adaptations + hooks
```

### Mode 2: Edit & Distribute (existing draft)
```
Input: "콘텐츠 에이전트: 이 글 편집하고 멀티채널로 배포해줘" + [draft text]
Output: Polished article + platform-native adaptations
```

### Mode 3: Repurpose Only
```
Input: "콘텐츠 에이전트: 이 글 10채널로 변환해줘" + [finished article]
Output: Platform-specific content kit (Twitter thread, LinkedIn, newsletter, etc.)
```

## Phase Details

### Phase 1: Plan

1. Parse user request to extract:
   - Core topic / thesis
   - Target audience (ICP)
   - Target platforms (default: blog + Twitter + LinkedIn + newsletter)
   - Desired tone (professional, casual, provocative, educational)
   - Length constraints per platform
2. If Content Skill Graph exists (`content-graph/`), run `content-graph-produce` Phases 1-2:
   - Load graph context (brand voice, platform rules, hook formulas)
   - Generate seed content angle
3. Run `hook-generator` with topic + platform list:
   - Produce 3-5 hook candidates using proven frameworks
   - Select best hook per platform based on scroll-stopping score

### Phase 2: Draft

1. Run `kwp-marketing-content-creation` with:
   - Topic, audience, tone from Phase 1
   - Selected hook as opening
   - Channel: primary platform (usually blog/article)
2. If brand voice samples exist, run `content-style-researcher`:
   - Extract voice DNA from samples
   - Apply to draft (vocabulary, rhythm, tone markers)
3. Output: raw long-form draft (1000-3000 words depending on request)

### Phase 3: Edit (Evaluator-Optimizer)

1. Run `evaluation-engine` with content-quality rubric:
   - Clarity (0-10): is the argument easy to follow?
   - Engagement (0-10): does the reader want to keep reading?
   - Accuracy (0-10): are claims supported?
   - Tone (0-10): does it match the requested voice?
   - CTA Strength (0-10): is the call-to-action compelling?
2. If composite score < 7/10:
   - Run `edit-article` (restructure sections, cut filler, sharpen)
   - Run `sentence-polisher` (grammar, flow, Korean honorific level)
   - Re-evaluate (max 2 iterations)
3. If score >= 7/10: approve and proceed to Phase 4

### Phase 4: Distribute

1. Run `content-repurposing-engine` with approved draft:
   - Twitter thread (hook + 5-7 tweets)
   - LinkedIn post (professional adaptation)
   - Newsletter section (email-friendly format)
   - Blog post (SEO-optimized with headers)
   - Instagram caption (visual-first, hashtag-ready)
   - Additional platforms as specified
2. Run `long-form-compressor` for TL;DR summary
3. Output format:

```markdown
## 콘텐츠 킷: [TOPIC]

### 원본 (Blog/Article)
[full edited article]

### 품질 점수
- Clarity: X/10 | Engagement: X/10 | Tone: X/10
- 종합: X/10 (PASS/RETRY)

### 플랫폼별 콘텐츠
#### Twitter Thread
[thread content]

#### LinkedIn Post
[linkedin content]

#### Newsletter
[newsletter section]

#### Instagram Caption
[caption + hashtags]

### TL;DR
[3-sentence summary]
```

## Overlap & Differentiation

| Existing Agent | Overlap Area | Differentiation |
|---|---|---|
| `rr-content-curator` | Multi-source content routing to Slack | This agent CREATES content; CC curates/routes existing content |
| `rr-knowledge-strategist` | KB-based content compilation | This agent produces audience-facing content; KS produces internal intelligence |
| Content Production Agent Team | Full editorial pipeline | This agent is a thin single-harness; the team uses 6 separate agent skills |

## Error Handling

- No topic provided → ask user for topic, audience, platform preferences
- evaluation-engine score < 4 after 2 edits → output draft with quality warning + manual review flag
- content-repurposing-engine fails on a platform → skip platform, note in output
- Brand voice samples not found → proceed without style enforcement, note in output

## Invocation Examples

```
"콘텐츠 에이전트: AI GPU 클라우드 비용 최적화 주제로 블로그 + 트위터 쓰레드 만들어줘"
"content agent: write a LinkedIn thought-leadership post about serverless inference"
"콘텐츠 제작 에이전트: 이 리서치 결과를 10채널 콘텐츠로 변환해줘"
"1인 기업 콘텐츠: 이번주 뉴스레터 주제 생성 + 초안 작성"
```
