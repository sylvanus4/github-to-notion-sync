---
name: nlm-strategy-hub
description: >-
  End-to-end pipeline: run PM strategy frameworks (Lean Canvas, SWOT, Porter's
  Five Forces, market sizing, competitor analysis, personas), compile results
  into expert-level Korean documents, upload to NotebookLM with web research
  enrichment, and generate multi-format strategy outputs (slide deck, audio
  podcast, mind map, executive report).
  Use when the user asks to "create strategy hub", "build strategy notebook",
  "product strategy research", "전략 허브 생성", "전략 리서치", "NLM 전략",
  "strategy research hub", "strategy to slides and podcast",
  "comprehensive strategy analysis", "investor deck from strategy",
  or any request to run PM strategy analysis and produce NotebookLM outputs.
  Do NOT use for GTM launch materials -- use nlm-launch-kit.
  Do NOT use for product discovery and assumption testing -- use nlm-discovery-lab.
  Do NOT use for ad-hoc studio_create on existing notebooks -- use notebooklm-studio.
  Do NOT use for slides-only from local markdown -- use nlm-slides.
metadata:
  author: thaki
  version: 1.0.0
  category: orchestration
---

# NLM Strategy Hub: Product Strategy Research Hub Pipeline

End-to-end pipeline that transforms a product/company description into a comprehensive strategy knowledge base in NotebookLM — enriched with web research and delivered as multiple output formats for different audiences (board, team, investors).

## Prerequisites

- `notebooklm-mcp` MCP server registered and authenticated (see `notebooklm` skill)
- PM skills installed: `pm-product-strategy`, `pm-market-research`, `pm-marketing-growth`

## System Prompt

The strategy document rewrite system prompt is stored at `references/system-prompt.md` (relative to this skill). Read it before the Compile phase. It defines:

- Authoritative, data-backed strategy tone in Korean
- Section structure rules for strategy documents
- White background visual directive
- Quality gates for strategic content

## Pipeline

### Phase 1: Gather Input

Collect from the user:
- **Product/company description** (what it does, stage, key differentiators)
- **Target market** (industry, geography, segment)
- **Competitors** (2-3 named competitors, or ask the agent to discover them)
- **Analysis focus** (optional: emphasize pricing, market entry, defensibility, etc.)

### Phase 2: PM Strategy Analysis (pm-product-strategy)

Run these sub-skills sequentially, passing the product context as input:

1. **Lean Canvas** (`lean-canvas`): 9-section canvas — Problem, Solution, UVP, Unfair Advantage, Segments, Channels, Revenue, Cost, Metrics
2. **SWOT Analysis** (`swot-analysis`): Strengths, Weaknesses, Opportunities, Threats with strategic implications
3. **Porter's Five Forces** (`porters-five-forces`): Industry dynamics and competitive intensity
4. **Value Proposition** (`value-proposition`): JTBD-based articulation of why customers choose this product

### Phase 3: Market Research (pm-market-research)

Run these sub-skills using the product context and competitive information:

1. **Market Sizing** (`market-sizing`): TAM/SAM/SOM with top-down and bottom-up estimates
2. **Competitor Analysis** (`competitor-analysis`): 3-5 competitors with strengths, weaknesses, differentiation opportunities
3. **User Personas** (`user-personas`): 3 personas with JTBD, pains, gains

### Phase 4: Growth Metrics (pm-marketing-growth)

1. **North Star Metric** (`north-star-metric`): Business game classification, NSM definition, input metrics
2. **Positioning** (`positioning-ideas`): Differentiation statement and positioning strategy

### Phase 5: Compile Strategy Document (한국어)

Using the system prompt from `references/system-prompt.md`, compile all artifacts from Phases 2-4 into **한국어 전문가 전략 문서**:

- 전문가의 전략 분석 톤
- 각 프레임워크 결과를 핵심 시사점과 함께 구조화된 섹션으로 구성
- 핵심 데이터와 지표를 **굵게** 강조
- 프레임워크 간 연결 인사이트 포함 (예: SWOT 위협 → Porter's Five Forces 연계)
- 자연스러운 한국어 비즈니스 표현으로 전달

**Document structure:**
1. Executive Summary
2. Lean Canvas Overview
3. SWOT Analysis
4. Industry Dynamics (Porter's Five Forces)
5. Value Proposition
6. Market Sizing (TAM/SAM/SOM)
7. Competitive Landscape
8. Target Personas
9. North Star Metric & Growth Framework
10. Strategic Positioning
11. Key Risks & Recommendations

### Phase 6: NLM Research Enrichment

1. Create notebook:
```
notebook_create(title="<Product> - Strategy Hub")
```

2. Upload compiled documents:
```
source_add(notebook_id, source_type="text", title="전략 분석 (KO)", text=<korean_doc>, wait=True)
```

3. Run web research for enrichment:
```
research_start(notebook_id, query="<product> market analysis competitors trends", source="web", mode="fast")
```

4. Poll and import:
```
research_status(notebook_id, task_id)
research_import(notebook_id, task_id)
```

### Phase 7: Multi-Format Generation

Generate 4 artifact types from the enriched notebook:

1. **Slide Deck** — Board/investor presentation:
```
studio_create(notebook_id, artifact_type="slide_deck", confirm=True, language="ko")
```

2. **Audio Podcast** — Stakeholder strategy briefing:
```
studio_create(notebook_id, artifact_type="audio", audio_format="deep_dive", confirm=True, language="ko")
```

3. **Mind Map** — Strategy overview visualization:
```
studio_create(notebook_id, artifact_type="mind_map", confirm=True, language="ko")
```

4. **Executive Report** — Briefing document:
```
studio_create(notebook_id, artifact_type="report", report_format="Briefing Doc", confirm=True, language="ko")
```

Poll `studio_status(notebook_id)` every 30 seconds between each generation. Download all artifacts:

```
download_artifact(notebook_id, artifact_type="slide_deck", output_path="outputs/strategy-hubs/<product>-strategy-<date>/slides.pptx")
download_artifact(notebook_id, artifact_type="audio", output_path="outputs/strategy-hubs/<product>-strategy-<date>/podcast.mp3")
download_artifact(notebook_id, artifact_type="mind_map", output_path="outputs/strategy-hubs/<product>-strategy-<date>/mind-map.pdf")
download_artifact(notebook_id, artifact_type="report", output_path="outputs/strategy-hubs/<product>-strategy-<date>/executive-report.pdf")
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--lang ko` | 한국어 출력 (기본값) | 한국어 |
| `--skip-research` | Skip web research enrichment (Phase 6 research step) | Research enabled |
| `--artifacts "slides,audio"` | Generate only specified artifact types | All 4 artifacts |
| `--focus "pricing"` | Emphasize a specific strategic dimension | Balanced analysis |

## Output Convention

Files are saved to `outputs/strategy-hubs/`:

```
outputs/strategy-hubs/
  acme-saas-strategy-2026-03-08/
    slides.pptx
    podcast.mp3
    mind-map.pdf
    executive-report.pdf
```

## Example

```
/nlm-strategy-hub "Acme SaaS — B2B project management tool for mid-market companies. Competes with Asana, Monday.com, ClickUp. Series A stage, $5M ARR."
```

This will:
1. Collect product context for Acme SaaS
2. Run Lean Canvas, SWOT, Porter's Five Forces, Value Proposition
3. Run TAM/SAM/SOM, competitor analysis (Asana, Monday.com, ClickUp), 3 user personas
4. Define North Star metric and positioning
5. Compile into expert Korean strategy document
6. Create NotebookLM notebook, upload documents, run web research
7. Generate slide deck, audio podcast, mind map, executive report
8. Download all artifacts to `outputs/strategy-hubs/acme-saas-strategy-2026-03-08/`

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Shallow framework outputs | Provide more detailed product context and named competitors |
| Research returns irrelevant sources | Use `--skip-research` or refine the product description |
| Generation timeout | Generate artifacts one at a time; poll with longer intervals |
| Missing market data in sizing | Supplement with `--focus "market sizing"` or provide industry reports |
| Audio too generic | Ensure the compiled document has specific metrics and strategic implications |

## Related Skills

- **pm-product-strategy** -- individual strategy framework execution
- **pm-market-research** -- standalone market research sub-skills
- **pm-marketing-growth** -- North Star and positioning analysis
- **notebooklm** -- notebook/source CRUD
- **notebooklm-research** -- web/Drive research and import
- **notebooklm-studio** -- ad-hoc studio content generation
- **nlm-launch-kit** -- GTM launch materials pipeline
- **nlm-discovery-lab** -- product discovery and assumption testing pipeline
