---
name: feynman-source-comparison
description: "Compare multiple sources on a topic and produce a grounded comparison matrix of agreements, disagreements, and confidence levels. Use when the user asks to 'compare papers', 'compare approaches', 'comparison matrix', 'compare tools', 'compare frameworks', 'cross-source analysis', 'agreement disagreement matrix', '논문 비교', '소스 비교', '도구 비교', '프레임워크 비교', '교차 분석', 'feynman-source-comparison', '/compare', 'compare claims across sources'. Do NOT use for paper-code consistency checks (use feynman-paper-audit). Do NOT use for single-paper peer review (use feynman-peer-review). Do NOT use for competitive product analysis (use kwp-product-management-competitive-analysis or kwp-marketing-competitive-analysis). Do NOT use for general web research without structured comparison (use parallel-web-search)."
---

# Source Comparison

Compare multiple sources (papers, tools, approaches, frameworks, benchmarks) on a topic and produce a source-grounded comparison matrix with agreement/disagreement analysis and confidence scoring.

## Prerequisites

- The user provides a comparison topic and optionally specific sources to compare.
- If sources are not specified, the skill discovers them during Phase 2.

## Workflow

### Phase 1: Plan

1. Derive a short slug from the comparison topic.
2. Outline the comparison plan:
   - Sources to compare (or discovery criteria if not specified)
   - Dimensions to evaluate (methodology, performance, scalability, cost, etc.)
   - Expected output structure
3. Save the plan to `outputs/feynman/<slug>-comparison-plan.md`.
4. Present to the user and **wait for confirmation**.

### Phase 2: Source Gathering (Subagent)

Spawn a `generalPurpose` subagent for broad comparison sets:

```
You are a research evidence agent. Your task:

1. Gather source material for comparing: <topic>
2. For each source:
   - Fetch the primary document (paper, docs, repo)
   - Extract key claims, metrics, methodologies
   - Note caveats, limitations, and conditions
3. Build a structured evidence file with per-source summaries
4. Save to `outputs/feynman/<slug>-sources.md`

Use both WebSearch and alphaxiv-paper-lookup (via alpha CLI if available) when comparing academic and practical sources.

Evidence quality rules:
- Prefer primary sources over secondary summaries
- Every claim needs a verifiable URL
- Distinguish self-reported metrics from independently verified ones
```

### Phase 3: Verification (Subagent)

Spawn a second `generalPurpose` subagent:

```
You are a verification agent. Read `outputs/feynman/<slug>-sources.md` and:

1. Verify all URLs resolve
2. Cross-check claims that appear in multiple sources
3. Add inline citations [1], [2] etc.
4. Flag contradictions between sources
5. Build the final comparison matrix
6. Save to `outputs/feynman/<slug>-comparison.md`
```

### Phase 4: Matrix Construction

The comparison matrix must include:

```markdown
## Comparison Matrix

| Dimension | Source A [1] | Source B [2] | Source C [3] | Agreement |
|-----------|-------------|-------------|-------------|-----------|
| Method | ... | ... | ... | AGREE / DISAGREE / PARTIAL |
| Performance | ... | ... | ... | ... |
| Scalability | ... | ... | ... | ... |
| Cost | ... | ... | ... | ... |
| Limitations | ... | ... | ... | ... |

## Agreement Analysis

### Strong Agreement
- Dimension X: All sources agree that...

### Disagreement
- Dimension Y: Source A claims X, while Source B claims Y. Likely explanation: ...

### Uncertain
- Dimension Z: Insufficient evidence to compare. Source A reports, others silent.

## Confidence Assessment

| Source | Evidence Type | Recency | Overall Confidence |
|--------|--------------|---------|-------------------|
| [1] | Primary research | 2025 | HIGH |
| [2] | Secondary review | 2024 | MEDIUM |
```

### Phase 5: Delivery

1. Present the comparison matrix summary
2. Highlight key disagreements and their implications
3. Provide a recommendation if the user asked for one
4. End with numbered `Sources` section

## Output Structure

```
outputs/feynman/
├── <slug>-comparison-plan.md  # Phase 1 plan
├── <slug>-sources.md          # Phase 2 raw sources
└── <slug>-comparison.md       # Phase 4 final matrix
```

## Visualization

When the comparison involves quantitative metrics, generate a Mermaid diagram or use visual-explainer for HTML visualization:
- Bar charts for performance comparisons
- Radar charts for multi-dimensional comparisons
- Flow diagrams for methodology/architecture comparisons

## Verification Before Completion

- [ ] Every cell in the comparison matrix cites a specific source
- [ ] Agreement/disagreement analysis covers all dimensions
- [ ] URLs in Sources section resolve
- [ ] Confidence assessment provided for each source
- [ ] Output files exist at documented paths
