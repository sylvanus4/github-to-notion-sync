---
name: nlm-discovery-lab
description: >-
  End-to-end pipeline: run PM product discovery frameworks (OST, assumptions,
  interview scripts, experiments), user research (personas, journey maps,
  segmentation), and data frameworks (metrics, cohort, A/B test), compile into
  expert-level EN + KO discovery documents, upload to NotebookLM with competitive
  research, and generate 5 learning assets (quiz, debate podcast, slides, study
  guide, data table).
  Use when the user asks to "run discovery lab", "product discovery notebook",
  "디스커버리 랩", "assumption testing", or run product discovery and produce
  NotebookLM outputs.
  Do NOT use for strategic planning without discovery focus -- use nlm-strategy-hub.
  Do NOT use for GTM launch materials -- use nlm-launch-kit.
  Do NOT use for ad-hoc studio_create on existing notebooks -- use notebooklm-studio.
  Do NOT use for slides-only from local markdown -- use nlm-slides.
metadata:
  author: thaki
  version: 1.0.0
  category: orchestration
---

# NLM Discovery Lab: Product Discovery Lab Pipeline

End-to-end pipeline that runs a complete product discovery cycle — from opportunity identification through assumption testing to experiment design — then packages everything into a NotebookLM-powered learning environment for the product trio (PM + Designer + Engineer) to align on findings.

## Prerequisites

- `notebooklm-mcp` MCP server registered and authenticated (see `notebooklm` skill)
- PM skills installed: `pm-product-discovery`, `pm-market-research`, `pm-data-analytics`

## System Prompt

The discovery document rewrite system prompt is stored at `references/system-prompt.md` (relative to this skill). Read it before the Compile phase. It defines:

- Hypothesis-driven, exploratory tone for each language
- Section structure rules for discovery documents
- White background visual directive
- Quality gates for discovery rigor

## Pipeline

### Phase 1: Gather Input

Collect from the user:
- **Desired outcome** (the product/business outcome to improve, e.g., "increase trial-to-paid conversion")
- **Opportunity area** (the problem space or user pain point to explore)
- **Product context** (existing product vs new product, current state)
- **Known constraints** (timeline, resources, technical limitations)
- **Existing data** (optional: interview transcripts, analytics, feature requests)

### Phase 2: Discovery Ideation (pm-product-discovery)

Run these sub-skills sequentially, using the outcome and opportunity as input:

1. **Opportunity Solution Tree** (`opportunity-solution-tree`): Outcome -> opportunities -> solutions -> experiments (4-level tree)
2. **Assumption Identification** (`identify-assumptions-existing`): Classify assumptions into Value, Usability, Viability, Feasibility risks
3. **Interview Script** (`interview-script`): JTBD + Mom Test interview guide with note-taking template
4. **Experiment Brainstorm** (`brainstorm-experiments-existing`): Pretotype and MVP experiment designs for top assumptions

### Phase 3: User Research (pm-market-research)

Run these sub-skills to build empathy maps and journey understanding:

1. **User Personas** (`user-personas`): 3 personas with JTBD, pains, gains, and behavioral patterns
2. **Customer Journey Map** (`customer-journey-map`): Awareness -> consideration -> decision -> onboarding -> advocacy with touchpoints and emotions
3. **User Segmentation** (`user-segmentation`): 3+ behavioral/needs-based segments with sizing

### Phase 4: Data Framework (pm-data-analytics)

Design the measurement framework for discovery experiments:

1. **Metrics Dashboard** (`metrics-dashboard`): KPIs, North Star candidates, dashboard layout design
2. **Cohort Analysis Template** (`cohort-analysis`): Retention and feature adoption cohort framework for the opportunity area
3. **A/B Test Framework** (`ab-test-analysis`): Sample size, duration, and success criteria for top 2-3 experiments from Phase 2

### Phase 5: Compile Discovery Document (EN + KO)

Using the system prompt from `references/system-prompt.md`, compile all artifacts from Phases 2-4 into **two discovery documents**:

**English version:**
- Hypothesis-driven, evidence-aware discovery narrative
- Each framework result framed as "What we believe" -> "What we need to learn" -> "How we'll test it"
- Assumptions explicitly labeled with confidence levels and risk categories
- Cross-references between personas and journey stages

**Korean version:**
- 가설 중심의 탐색적 발견 서술
- 각 프레임워크 결과를 "우리가 믿는 것" -> "검증이 필요한 것" -> "테스트 방법" 프레임으로 구성
- 가정에 신뢰도 수준과 리스크 범주 명시
- 페르소나와 여정 단계 간 교차 참조

**Document structure:**
1. Discovery Brief (outcome, opportunity, constraints)
2. Opportunity Solution Tree
3. Assumption Map (classified by risk type)
4. Interview Script & Research Plan
5. Experiment Designs (top 3)
6. User Personas
7. Customer Journey Map
8. User Segmentation
9. Metrics Dashboard Design
10. Cohort Analysis Framework
11. A/B Test Specifications
12. Open Questions & Next Steps

### Phase 6: NLM Research + Upload

1. Create notebook:
```
notebook_create(title="<Opportunity> - Discovery Lab")
```

2. Upload compiled documents:
```
source_add(notebook_id, source_type="text", title="Discovery Lab (EN)", text=<english_doc>, wait=True)
source_add(notebook_id, source_type="text", title="디스커버리 랩 (KO)", text=<korean_doc>, wait=True)
```

3. Upload existing data if provided (interview transcripts, analytics exports):
```
source_add(notebook_id, source_type="file", file_path="<path_to_data>", wait=True)
```

4. Run web research for competitive validation and prior art:
```
research_start(notebook_id, query="<opportunity area> user research best practices competitive solutions", source="web", mode="fast")
```

5. Poll and import:
```
research_status(notebook_id, task_id)
research_import(notebook_id, task_id)
```

6. Optionally share notebook with the product trio:
```
notebook_share_invite(notebook_id, email="<designer@company.com>", role="writer")
notebook_share_invite(notebook_id, email="<engineer@company.com>", role="writer")
```

### Phase 7: Interactive Learning Assets

Generate 5 artifact types designed for team alignment and learning:

1. **Team Alignment Quiz** — "Do we agree on the problem?":
```
studio_create(notebook_id, artifact_type="quiz", question_count=15, difficulty="medium", confirm=True)
```

2. **Assumption Debate Podcast** — Two-sided debate on key assumptions:
```
studio_create(notebook_id, artifact_type="audio", audio_format="debate", confirm=True)
```

3. **Discovery Review Slides** — Stakeholder presentation of findings:
```
studio_create(notebook_id, artifact_type="slide_deck", confirm=True)
```

4. **Study Guide** — Deep-dive reference for the product trio:
```
studio_create(notebook_id, artifact_type="report", report_format="Study Guide", confirm=True)
```

5. **Assumption Tracking Table** — Structured data table for ongoing tracking:
```
studio_create(notebook_id, artifact_type="data_table", description="Assumption tracking matrix: assumption, risk type (Value/Usability/Viability/Feasibility), confidence level, experiment, status, evidence, next action", confirm=True)
```

Poll `studio_status(notebook_id)` every 30 seconds between each generation. Download all artifacts:

```
download_artifact(notebook_id, artifact_type="quiz", output_path="outputs/discovery-labs/<opportunity>-discovery-<date>/alignment-quiz.pdf")
download_artifact(notebook_id, artifact_type="audio", output_path="outputs/discovery-labs/<opportunity>-discovery-<date>/assumption-debate.mp3")
download_artifact(notebook_id, artifact_type="slide_deck", output_path="outputs/discovery-labs/<opportunity>-discovery-<date>/discovery-review.pptx")
download_artifact(notebook_id, artifact_type="report", output_path="outputs/discovery-labs/<opportunity>-discovery-<date>/study-guide.pdf")
download_artifact(notebook_id, artifact_type="data_table", output_path="outputs/discovery-labs/<opportunity>-discovery-<date>/assumption-tracker.csv")
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--lang en` | Generate English version only | Both EN + KO |
| `--lang ko` | Generate Korean version only | Both EN + KO |
| `--skip-research` | Skip web research enrichment | Research enabled |
| `--artifacts "quiz,slides"` | Generate only specified artifact types | All 5 artifacts |
| `--context "new"` | Product context: `existing` or `new` product | `existing` |
| `--share "email1,email2"` | Share notebook with team members after creation | No sharing |
| `--data "path/to/file"` | Upload additional data files (transcripts, analytics) | No extra data |

## Output Convention

Files are saved to `outputs/discovery-labs/`:

```
outputs/discovery-labs/
  trial-conversion-discovery-2026-03-08/
    alignment-quiz.pdf
    assumption-debate.mp3
    discovery-review.pptx
    study-guide.pdf
    assumption-tracker.csv
```

## Example

```
/nlm-discovery-lab "Increase trial-to-paid conversion rate from 8% to 15% for Acme PM tool. Current users drop off during onboarding (day 2-3). We believe the value moment is not reached fast enough. Existing product, mid-market B2B SaaS."
```

This will:
1. Collect outcome (trial-to-paid 8% -> 15%), opportunity (onboarding drop-off), product context (existing B2B SaaS)
2. Build Opportunity Solution Tree from onboarding conversion outcome
3. Identify assumptions (Value: is the value moment right? Usability: is onboarding too complex? etc.)
4. Generate JTBD + Mom Test interview script for churned trial users
5. Design 3 experiments (e.g., guided setup wizard, value-moment shortcut, progressive disclosure)
6. Create 3 personas (power user, evaluator, reluctant adopter), journey map, segmentation
7. Design metrics dashboard, cohort analysis for trial-to-paid by signup week, A/B test specs
8. Compile into expert EN + KO discovery documents
9. Create NotebookLM notebook, upload documents, run web research
10. Generate quiz, debate podcast, slides, study guide, assumption tracker
11. Download all artifacts to `outputs/discovery-labs/trial-conversion-discovery-2026-03-08/`

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| OST too shallow | Provide more specific outcome metrics and known constraints |
| Assumptions too vague | Add existing user data or interview transcripts via `--data` |
| Quiz questions miss key assumptions | Strengthen the assumption map section in the compiled document |
| Debate podcast one-sided | Ensure assumptions have genuine uncertainty — clearly stated for/against |
| Data table missing columns | Provide a more detailed description in the `data_table` studio_create call |
| Personas feel generic | Supplement with real user data via `--data` flag |

## Related Skills

- **pm-product-discovery** -- individual discovery framework execution
- **pm-market-research** -- standalone user research sub-skills
- **pm-data-analytics** -- SQL, cohort, and A/B test analysis
- **notebooklm** -- notebook/source CRUD
- **notebooklm-research** -- web/Drive research and import
- **notebooklm-studio** -- ad-hoc studio content generation
- **nlm-strategy-hub** -- strategic analysis pipeline (post-discovery phase)
- **nlm-launch-kit** -- GTM launch materials pipeline (post-strategy phase)
