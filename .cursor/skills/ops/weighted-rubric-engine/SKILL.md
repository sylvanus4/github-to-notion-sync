---
name: weighted-rubric-engine
description: >-
  Generalized weighted scoring rubric engine with configurable dimensions, weights,
  grade bands, and interpretation labels. Extends evaluation-engine with KB-domain
  rubric templates (doc-quality, market-health, signal-strength, role-relevance),
  interpretation bands with action guidance, and radar chart data output.
  Accepts rubric definitions as YAML/JSON, scores any entity against the rubric
  with per-dimension justification, and produces structured reports with composite
  score, grade, band interpretation, and visualization-ready data.
  Use when the user asks to "score with rubric", "weighted rubric", "rubric engine",
  "custom scoring rubric", "grade with dimensions", "evaluate with custom rubric",
  "가중 루브릭", "루브릭 평가", "차원별 점수", "맞춤 평가 루브릭", "루브릭 엔진",
  "weighted-rubric-engine", "apply rubric template", "루브릭 템플릿 적용",
  or wants to score entities against domain-specific weighted rubrics with
  interpretation bands beyond the standard A-F grading.
  Do NOT use for standard A-F entity evaluation without custom bands (use evaluation-engine).
  Do NOT use for LLM prompt evaluation (use evals-skills).
  Do NOT use for code review scoring (use deep-review).
  Do NOT use for AI report quality scoring (use ai-quality-evaluator).
user_invocable: true
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "ops"
  tags: ["rubric", "scoring", "evaluation", "weighted", "kb-domain", "configurable"]
---

# Weighted Rubric Engine

Score any entity against a configurable weighted rubric with custom dimensions,
grade bands, and interpretation labels. Produces structured reports with composite
scores, per-dimension justification, band interpretation, and radar chart data.

## When to Use

- Scoring KB wiki articles, documents, or reports against quality rubrics
- Evaluating market health, signal strength, or role relevance with custom bands
- Building domain-specific scoring frameworks beyond standard A-F grading
- Comparing entities using rubrics with interpretation guidance per band
- User says "rubric", "weighted score", "custom grading", "루브릭", "가중 평가"

## Do NOT Use

- Standard A-F entity evaluation without custom bands → `evaluation-engine`
- LLM prompt evaluation → `evals-skills`
- Code review scoring → `deep-review`
- AI report quality scoring → `ai-quality-evaluator`

## Architecture

```
Weighted Rubric Engine
├── Load rubric definition (inline YAML/JSON or template)
├── Validate rubric (weights sum to 1.0, bands are non-overlapping)
├── For each dimension:
│   ├── Gather evidence (KB search, file read, user input)
│   ├── Score against criteria with justification
│   └── Map to dimension-level band
├── Calculate weighted composite score
├── Map composite to interpretation band
├── Generate structured report with radar chart data
└── Output markdown + optional JSON for downstream consumption
```

## Rubric Definition Format

```yaml
rubric:
  name: document-quality
  version: 1
  description: KB wiki article quality assessment

  dimensions:
    - id: completeness
      name: Completeness
      weight: 0.25
      criteria:
        - All required sections present (Compiled Truth, Evidence Timeline)
        - Frontmatter fully populated
        - No placeholder or stub content
      scoring_guide:
        9-10: All sections present with depth
        7-8: Minor gaps in non-critical sections
        5-6: Missing 1-2 required sections
        3-4: Multiple sections missing or stub
        1-2: Skeleton only

    - id: evidence_quality
      name: Evidence Quality
      weight: 0.30
      criteria:
        - Evidence diversity score (source types, date spread)
        - Source citation completeness
        - Recency of evidence
      scoring_guide:
        9-10: 5+ diverse sources, all cited, within 30 days
        7-8: 3-4 sources, mostly cited, within 60 days
        5-6: 2-3 sources, some citations missing
        3-4: Single source or uncited claims
        1-2: No evidence or fabricated

    - id: synthesis
      name: Synthesis Quality
      weight: 0.25
      criteria:
        - Compiled Truth reflects all evidence
        - Contradictions acknowledged
        - Actionable insights derived
      scoring_guide:
        9-10: Comprehensive synthesis, contradictions noted, clear actions
        7-8: Good synthesis, minor gaps
        5-6: Adequate but surface-level
        3-4: Evidence listed without synthesis
        1-2: No synthesis attempted

    - id: connectivity
      name: Cross-Reference Quality
      weight: 0.20
      criteria:
        - Wikilinks to related concepts
        - Connection documents where appropriate
        - Backlinks from other articles
      scoring_guide:
        9-10: Rich wikilink network, connections documented
        7-8: Key cross-references present
        5-6: Some links but isolated
        3-4: Minimal cross-references
        1-2: No links to other articles

  bands:
    - id: excellent
      min: 8.5
      label: "Excellent"
      color: "#22c55e"
      interpretation: "Publication-ready. No revisions needed."
      action: "Archive as reference exemplar."
    - id: good
      min: 7.0
      label: "Good"
      color: "#84cc16"
      interpretation: "Solid quality. Minor improvements possible."
      action: "Flag low-scoring dimensions for next compile cycle."
    - id: adequate
      min: 5.5
      label: "Adequate"
      color: "#eab308"
      interpretation: "Meets minimum bar. Several areas need improvement."
      action: "Schedule targeted enhancement for weakest 2 dimensions."
    - id: needs_work
      min: 3.5
      label: "Needs Work"
      color: "#f97316"
      interpretation: "Below standard. Significant gaps present."
      action: "Recompile with additional sources. Do not cite externally."
    - id: poor
      min: 0.0
      label: "Poor"
      color: "#ef4444"
      interpretation: "Fundamentally incomplete or unreliable."
      action: "Re-ingest from scratch or mark for deletion review."
```

## Built-in Rubric Templates

| Template ID | Domain | Dimensions | Source Pattern |
|---|---|---|---|
| `doc-quality` | KB wiki article quality | completeness, evidence, synthesis, connectivity | `engineering-standards/wiki/concepts/document-quality-gate.md` |
| `market-health` | Market breadth composite | breadth, momentum, sentiment, volatility | `engineering-standards/wiki/concepts/market-breadth-composite-scoring.md` |
| `signal-strength` | Trading signal evolution | confidence, recency, confirmation, risk-reward | `engineering-standards/wiki/concepts/signal-evolution-state-machine.md` |
| `role-relevance` | Cross-role topic relevance | strategic_impact, operational_impact, urgency, scope | `research-intelligence/raw/role-*-analysis.md` |

Templates are loaded by name. Users can override any dimension or band.

## Execution Flow

### Step 1: Load Rubric

Accept rubric from one of:
1. Template name: `--rubric doc-quality`
2. Inline YAML/JSON in user message
3. File path: `--rubric-file config/rubrics/custom.yaml`

Validate:
- All dimension weights sum to 1.0 (tolerance: ±0.01)
- Bands are non-overlapping and cover 0.0-10.0
- Each dimension has at least 1 criterion

### Step 2: Gather Evidence

For each dimension, gather evidence based on the entity type:
- **KB articles**: Read article content, check frontmatter, count wikilinks
- **Market data**: Query recent price/volume data, breadth indicators
- **Signals**: Check signal age, confirmation count, decay state
- **Custom**: Use the evidence gathering strategy specified in the rubric

### Step 3: Score Each Dimension

For each dimension, produce:

```markdown
### {Dimension Name} — {Score}/10

**Criteria Evaluated:**
- {criterion 1}: {assessment}
- {criterion 2}: {assessment}

**Justification:** {1-2 sentences explaining the score}
**Band:** {dimension-level band label if applicable}
```

### Step 4: Compute Composite

```
composite = Σ (dimension_score × dimension_weight)
band = lookup(composite, rubric.bands)  # first band where composite >= min
```

### Step 5: Generate Report

```markdown
# Rubric Evaluation: {Entity Name}

**Date:** {YYYY-MM-DD}
**Rubric:** {name} v{version}
**Composite Score:** {X.XX} / 10
**Band:** {band.label} — {band.interpretation}
**Recommended Action:** {band.action}

## Score Summary

| Dimension | Weight | Score | Weighted |
|---|---|---|---|
| {name} | {weight} | {score}/10 | {weighted} |
| ... | ... | ... | ... |
| **Composite** | **1.00** | | **{composite}** |

## Radar Chart Data

```json
{
  "labels": ["Completeness", "Evidence", "Synthesis", "Connectivity"],
  "values": [8.0, 7.5, 6.0, 9.0],
  "max": 10
}
```

## Detailed Dimension Analysis

{Per-dimension blocks from Step 3}

## Improvement Priorities

1. {Weakest dimension}: {specific improvement suggestion}
2. {Second weakest}: {suggestion}
```

### Step 6: Multi-Entity Comparison (Optional)

When scoring multiple entities:
1. Run Steps 1-5 for each entity
2. Build comparison matrix with per-dimension and composite scores
3. Rank by composite
4. Highlight dimensions where entities diverge most

## Output Formats

| Format | Use Case |
|---|---|
| Markdown report | Default, human-readable |
| JSON (structured) | Downstream pipeline consumption, dashboard integration |
| Radar chart data | Visualization via `visual-explainer` |

## Composability

- **evaluation-engine**: Weighted-rubric-engine extends evaluation-engine's A-F model with configurable bands and interpretation labels
- **kb-lint**: Rubric scores can feed into kb-lint's health checks
- **kb-daily-report**: Rubric results can be included in daily intelligence reports
- **visual-explainer**: Radar chart data renders as interactive HTML

## Constraints

- Dimension weights MUST sum to 1.0
- Bands MUST be non-overlapping and monotonically decreasing (highest `min` first)
- Every score MUST include evidence citations
- Never modify rubric definition mid-evaluation
- Archive all evaluation results for trend analysis

## Examples

### Example 1: Score a competitor

- **Trigger:** User says: "Score AWS against our cloud platform rubric"
- **Actions:** Load the cloud-platform rubric template; score AWS across dimensions (scalability, pricing, UX, support, ecosystem); apply weight-adjusted composite; emit band classification.
- **Result:** Graded scorecard with per-dimension justification, radar chart data, and band interpretation.

### Example 2: Custom rubric creation

- **Trigger:** User says: "Create a rubric for evaluating KB article quality"
- **Actions:** Define dimensions (evidence density, freshness, cross-referencing, readability, completeness); assign weights (30/25/20/15/10); set bands A–D; save definition as YAML.
- **Result:** Reusable rubric file ready for `weighted-rubric-engine` runs.

## Error Handling

| Error | Action |
|-------|--------|
| Rubric YAML weights not summing to 100% | Normalize weights automatically and warn |
| Dimension score outside 0–100 range | Clamp to range and flag as anomaly |
| Missing required dimension in input | Score as 0 with explicit "NOT SCORED" label |
| Band definitions overlap | Report conflict and use first-match |
| Empty entity input | Return error: "No entity data provided for scoring" |

## Gotchas

- **Symptom:** Weights show 99% or 101% after edits. **Root cause:** Rounding in hand-authored YAML. **Correct approach:** Let the engine normalize; verify intentional precision vs. mistake in source rubric.
- **Symptom:** "D" band entity seems stronger on one axis than an "A" entity. **Root cause:** Composite score masks per-dimension spread. **Correct approach:** Always review the full dimension breakdown before decisions.
- **Symptom:** Radar chart looks wrong for a custom rubric. **Root cause:** Dimensions use different scales but were plotted raw. **Correct approach:** Normalize each dimension to 0–100 before emitting visualization JSON.

## Output Discipline

- Do not add interpretive narrative beyond the rubric's `interpretation` field; that field is the single source of truth for band meaning.
- Do not introduce dimensions absent from the rubric definition.
- Report composite scores to one decimal place; do not round composites for cosmetic band upgrades.

## Honest Reporting

- Report exact scores at band boundaries; do not round up to inflate a band.
- If all entities land in one band, state that plainly instead of spreading scores artificially.
- When data is insufficient for a dimension, mark "N/A" rather than estimating.
