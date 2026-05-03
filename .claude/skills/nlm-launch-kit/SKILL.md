---
name: nlm-launch-kit
description: >-
  End-to-end pipeline: run PM go-to-market frameworks (GTM strategy, ICP,
  battlecards, beachhead), execution docs (PRD, release notes, stakeholder
  map), and marketing assets (positioning, value props, naming), compile into
  expert-level Korean launch documents, upload to NotebookLM with competitive
  research, and generate 5 artifact types (slides, video, infographic,
  flashcards, quiz). Use when the user asks to "create launch kit", "build
  launch package", "GTM launch materials", "런치 키트 생성", "출시 자료", "NLM 런치킷",
  "launch kit from product brief", "go-to-market launch bundle", "sales
  enablement kit", "product launch deck and video", or any request to generate
  a complete product launch package via NotebookLM. Do NOT use for strategic
  analysis without launch focus -- use nlm-strategy-hub. Do NOT use for
  product discovery and assumptions -- use nlm-discovery-lab. Do NOT use for
  ad-hoc studio_create on existing notebooks -- use notebooklm-studio. Do NOT
  use for slides-only from local markdown -- use nlm-slides.
disable-model-invocation: true
---

# NLM Launch Kit: Go-to-Market Launch Kit Generator Pipeline

End-to-end pipeline that generates a complete product launch package — GTM strategy, sales enablement materials, customer-facing content, and internal alignment resources — all from a single product brief, packaged as a NotebookLM knowledge base with 5 output formats.

## Prerequisites

- `notebooklm-mcp` MCP server registered and authenticated (see `notebooklm` skill)
- PM skills installed: `pm-go-to-market`, `pm-execution`, `pm-marketing-growth`

## System Prompt

The launch document rewrite system prompt is stored at `references/system-prompt.md` (relative to this skill). Read it before the Compile phase. It defines:

- Persuasive, action-oriented launch tone in Korean
- Section structure rules for launch kit documents
- White background visual directive
- Quality gates for launch readiness content

## Pipeline

### Phase 1: Gather Input

Collect from the user:
- **Product/feature brief** (what is being launched, key capabilities)
- **Target audience** (who is this for — buyers, users, decision-makers)
- **Launch date** (timeline for launch activities)
- **Competitors** (who the sales team will be compared against)
- **Launch scope** (optional: new product, major feature, incremental update)

### Phase 2: GTM Strategy (pm-go-to-market)

Run these sub-skills sequentially:

1. **GTM Strategy** (`gtm-strategy`): Channels, messaging pillars, KPIs, 90-day launch roadmap
2. **Ideal Customer Profile** (`ideal-customer-profile`): Firmographics, behaviors, JTBD, pain points, disqualification criteria
3. **Competitive Battlecard** (`competitive-battlecard`): Head-to-head comparison, objection handling, competitive landmines
4. **Beachhead Segment** (`beachhead-segment`): Initial target segment for market entry

### Phase 3: Execution Docs (pm-execution)

Run these sub-skills with the product brief and GTM context:

1. **PRD Summary** (`create-prd`): 8-section product requirements document
2. **Release Notes** (`release-notes`): User-facing changelog and feature highlights
3. **Stakeholder Map** (`stakeholder-map`): Power/interest grid with communication plan

### Phase 4: Marketing Assets (pm-marketing-growth)

1. **Value Proposition Statements** (`value-prop-statements`): 3-5 messaging variants for different audiences
2. **Positioning** (`positioning-ideas`): Differentiation and positioning strategy
3. **Product Name Candidates** (`product-name`): 5 name candidates with rationale (if new product/feature)

### Phase 5: Compile Launch Kit Document (한국어)

Using the system prompt from `references/system-prompt.md`, compile all artifacts from Phases 2-4 into **한국어 전문가 런치 문서**:

- 설득력 있는 런치 문서 톤
- 대상 독자별 맞춤 구조 (영업, 마케팅, 경영진, 고객)
- 각 섹션에 명확한 액션 아이템 포함
- 경쟁 포지셔닝 자연스럽게 반영

**Document structure:**
1. Launch Overview & Timeline
2. Product Summary (from PRD)
3. Ideal Customer Profile
4. Beachhead Segment & Entry Strategy
5. Value Propositions (by audience)
6. Competitive Battlecard
7. GTM Strategy & Channels
8. Stakeholder Communication Plan
9. Release Notes (Customer-Facing)
10. Product Name Recommendation
11. Launch Readiness Checklist

### Phase 6: NLM Upload + Research

1. Create notebook:
```
notebook_create(title="<Product> - Launch Kit")
```

2. Upload compiled documents:
```
source_add(notebook_id, source_type="text", title="런치 키트 (KO)", text=<korean_doc>, wait=True)
```

3. Run competitive research:
```
research_start(notebook_id, query="<product category> competitive landscape market trends 2026", source="web", mode="fast")
```

4. Poll and import:
```
research_status(notebook_id, task_id)
research_import(notebook_id, task_id)
```

### Phase 7: Multi-Format Generation

Generate 5 artifact types from the enriched notebook:

1. **Slide Deck** — Launch presentation for all-hands / leadership:
```
studio_create(notebook_id, artifact_type="slide_deck", confirm=True, language="ko")
```

2. **Video Explainer** — Customer-facing product explainer:
```
studio_create(notebook_id, artifact_type="video", video_format="explainer", confirm=True, language="ko")
```

3. **Infographic** — One-pager for sales team / social media:
```
studio_create(notebook_id, artifact_type="infographic", confirm=True, language="ko")
```

4. **Flashcards** — Sales enablement training cards:
```
studio_create(notebook_id, artifact_type="flashcards", confirm=True, language="ko")
```

5. **Quiz** — Team readiness check before launch:
```
studio_create(notebook_id, artifact_type="quiz", question_count=10, confirm=True, language="ko")
```

Poll `studio_status(notebook_id)` every 30 seconds between each generation. Download all artifacts:

```
download_artifact(notebook_id, artifact_type="slide_deck", output_path="outputs/launch-kits/<product>-launch-<date>/launch-deck.pptx")
download_artifact(notebook_id, artifact_type="video", output_path="outputs/launch-kits/<product>-launch-<date>/explainer-video.mp4")
download_artifact(notebook_id, artifact_type="infographic", output_path="outputs/launch-kits/<product>-launch-<date>/one-pager.pdf")
download_artifact(notebook_id, artifact_type="flashcards", output_path="outputs/launch-kits/<product>-launch-<date>/sales-flashcards.pdf")
download_artifact(notebook_id, artifact_type="quiz", output_path="outputs/launch-kits/<product>-launch-<date>/readiness-quiz.pdf")
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--lang ko` | 한국어 출력 (기본값) | 한국어 |
| `--skip-research` | Skip competitive web research (Phase 6 research step) | Research enabled |
| `--artifacts "slides,video"` | Generate only specified artifact types | All 5 artifacts |
| `--scope "feature"` | Launch scope: `product`, `feature`, or `update` | `product` |
| `--skip-naming` | Skip product name generation | Naming enabled |

## Output Convention

Files are saved to `outputs/launch-kits/`:

```
outputs/launch-kits/
  acme-tasks-launch-2026-03-08/
    launch-deck.pptx
    explainer-video.mp4
    one-pager.pdf
    sales-flashcards.pdf
    readiness-quiz.pdf
```

## Example

```
/nlm-launch-kit "Acme Tasks — new AI-powered task prioritization feature for Acme PM tool. Target: engineering managers at mid-market SaaS companies. Competitors: Linear, Shortcut, Height. Launch date: April 15, 2026."
```

This will:
1. Collect product brief for Acme Tasks AI feature
2. Run GTM strategy, ICP, competitive battlecard vs Linear/Shortcut/Height, beachhead segment
3. Generate PRD summary, release notes, stakeholder map
4. Create value propositions, positioning, feature name candidates
5. Compile into expert Korean launch kit document
6. Create NotebookLM notebook, upload documents, run competitive research
7. Generate launch deck, explainer video, one-pager infographic, sales flashcards, readiness quiz
8. Download all artifacts to `outputs/launch-kits/acme-tasks-launch-2026-03-08/`

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Battlecard too generic | Provide specific competitor names and known differentiators |
| Video too long | Add `video_format="brief"` in the studio_create call |
| Quiz questions off-topic | Ensure the compiled document has clear product facts and competitive points |
| Flashcards lack depth | Strengthen the value proposition and battlecard sections in the compiled doc |
| Infographic too dense | Simplify the compiled document's key messages to 5-7 core points |

## Related Skills

- **pm-go-to-market** -- individual GTM framework execution
- **pm-execution** -- PRD, release notes, stakeholder management
- **pm-marketing-growth** -- positioning and value proposition analysis
- **notebooklm** -- notebook/source CRUD
- **notebooklm-research** -- web/Drive research and import
- **notebooklm-studio** -- ad-hoc studio content generation
- **nlm-strategy-hub** -- strategic analysis pipeline (pre-launch phase)
- **nlm-discovery-lab** -- product discovery and assumption testing pipeline
