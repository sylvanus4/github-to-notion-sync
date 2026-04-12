---
name: kb-cross-topic-synthesizer
description: >-
  Generate unified synthesis documents by identifying overlapping concepts across
  multiple KB topics. Reads wiki articles from 2+ topics, detects shared entities
  and themes via wikilink analysis and semantic matching, and produces a synthesis
  document that addresses different perspectives, consensus, contradictions, and
  gaps — filed into a designated cross-topic synthesis area.
  Use when the user asks to "synthesize across topics", "cross-topic synthesis",
  "combine KB topics", "find overlaps between topics", "unified wiki view",
  "크로스 토픽 합성", "토픽 간 합성", "위키 토픽 통합", "중복 개념 합성",
  "kb-cross-topic-synthesizer", "multi-topic synthesis", "topic overlap analysis",
  "cross-wiki synthesis", "토픽 교차 분석", "통합 문서 생성",
  or wants to create a unified view of a concept that spans multiple KB topics.
  Do NOT use for single-topic wiki compilation (use kb-compile).
  Do NOT use for searching within one topic (use kb-search).
  Do NOT use for competitive-specific cross-analysis (use competitive-archetype-matrix).
  Do NOT use for market-intelligence time-windowed compilation (use market-pulse-compiler).
user_invocable: true
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "knowledge-base"
  tags: ["cross-topic", "synthesis", "overlap", "multi-topic", "kb-domain", "connections"]
---

# KB Cross-Topic Synthesizer

Generate unified synthesis documents by identifying overlapping concepts across
multiple KB topics and reconciling different perspectives.

## When to Use

- Two or more KB topics contain articles about the same concept from different angles
- Need a unified view reconciling different-role perspectives on a shared entity
- Identifying consensus, contradictions, and coverage gaps across topics
- Building cross-topic connection documents with evidence synthesis
- User says "cross-topic", "synthesize topics", "토픽 간 합성", "통합 문서"

## Do NOT Use

- Single-topic compilation → `kb-compile`
- Search within one topic → `kb-search`
- Competitive-focused cross-analysis → `competitive-archetype-matrix`
- Time-windowed market intelligence → `market-pulse-compiler`

## Architecture

```
KB Cross-Topic Synthesizer
├── Input: 2+ topic names or "all" + concept keyword
├── Discover overlapping articles
│   ├── Wikilink cross-reference analysis
│   ├── Entity name matching across topics
│   ├── Semantic similarity of article titles
│   └── Shared `related` frontmatter entries
├── Cluster overlapping articles by concept
│   ├── Group articles addressing the same entity/theme
│   ├── Record source topic for each article
│   └── Note perspective differences (role-based framing)
├── For each concept cluster:
│   ├── Extract key claims from each topic's article
│   ├── Identify consensus (claims supported across topics)
│   ├── Identify contradictions (conflicting claims)
│   ├── Identify gaps (topics that should cover but don't)
│   └── Synthesize unified narrative with attribution
├── Generate synthesis document
│   ├── Cross-Topic Synthesis header with metadata
│   ├── Per-concept sections with consensus/contradiction/gap analysis
│   ├── Evidence table linking claims to source articles
│   └── Recommended actions (resolve contradictions, fill gaps)
└── Save to knowledge-bases/_cross-topic/synthesis-{concept}-{date}.md
```

## Execution Flow

### Step 1: Identify Target Topics

Accept input in one of these forms:
1. **Explicit topic list**: `["competitive-intel", "product-strategy", "sales-playbook"]`
2. **Concept keyword**: `"GPU pricing"` → search all topics for articles mentioning it
3. **All topics**: scan the full `knowledge-bases/` directory

### Step 2: Discover Overlapping Articles

For the target topics, find articles that overlap:

**Method A — Wikilink Cross-Reference:**
Scan all `wiki/` articles for `[[wikilinks]]` pointing to concepts in other topics.

**Method B — Entity Name Matching:**
Extract entity names (company names, product names, technical terms) from each article's
frontmatter `title` and `aliases`. Match across topics using exact and fuzzy matching.

**Method C — Semantic Title Similarity:**
Compare article titles across topics. Flag pairs with >0.7 similarity.

**Method D — Shared Related Entries:**
Compare `related` frontmatter arrays across articles. Shared entries indicate overlap.

### Step 3: Cluster by Concept

Group discovered overlapping articles into concept clusters:

```yaml
concept_clusters:
  - concept: "GPU Pricing Trends"
    articles:
      - topic: competitive-intel
        path: wiki/concepts/gpu-pricing-landscape.md
        perspective: "Competitor pricing strategies"
      - topic: finance-policies
        path: wiki/concepts/cloud-cost-optimization.md
        perspective: "Internal cost management"
      - topic: product-strategy
        path: wiki/concepts/pricing-tier-design.md
        perspective: "Our pricing decisions"
```

### Step 4: Analyze Each Cluster

For each concept cluster:

#### 4a: Extract Claims
Read each article and extract its key claims as structured entries:

```markdown
| Claim | Source Topic | Source Article | Evidence Type | Date |
|---|---|---|---|---|
| GPU prices declining 15% YoY | competitive-intel | gpu-pricing-landscape.md | Reported | 2024-03 |
| Our GPU costs stable due to contracts | finance-policies | cloud-cost-optimization.md | Inferred | 2024-02 |
```

#### 4b: Identify Consensus
Claims supported by 2+ topics with compatible evidence:

```markdown
**Consensus:** GPU compute costs are trending downward industry-wide.
- Supported by: competitive-intel (market data), finance-policies (vendor negotiations)
- Confidence: High (2 independent sources, consistent direction)
```

#### 4c: Identify Contradictions
Claims where topics present conflicting information:

```markdown
**Contradiction:** GPU availability timeline
- competitive-intel: "Shortage easing by Q3 2024"
- engineering-standards: "Internal capacity still constrained through 2025"
- Resolution needed: Different scope (industry vs. our specific contracts)
```

#### 4d: Identify Gaps
Topics that should cover the concept but don't:

```markdown
**Gap:** sales-playbook lacks GPU pricing comparison data
- Expected: Sales team needs competitive pricing for objection handling
- Recommendation: Create sales-playbook/wiki/concepts/competitive-gpu-pricing.md
```

### Step 5: Generate Synthesis Document

```markdown
---
title: "Cross-Topic Synthesis: {Concept Name}"
topics: [{topic1}, {topic2}, ...]
articles_analyzed: {N}
consensus_items: {N}
contradictions: {N}
gaps: {N}
synthesis_date: {YYYY-MM-DD}
---

# Cross-Topic Synthesis: {Concept Name}

## Overview

This synthesis reconciles perspectives on **{concept}** across {N} KB topics:
{topic list with article counts}.

## Consensus

{For each consensus item: unified claim + supporting evidence from each topic}

## Contradictions

{For each contradiction: conflicting claims + source analysis + resolution suggestion}

## Coverage Gaps

{For each gap: which topic is missing what, and why it matters}

## Unified Narrative

{Synthesized narrative integrating all perspectives, citing sources, acknowledging
uncertainty where contradictions exist}

## Evidence Table

| # | Claim | Topics | Type | Confidence | Sources |
|---|---|---|---|---|---|
| 1 | {claim} | {topics} | Consensus | High | {articles} |
| 2 | {claim} | {topics} | Contradiction | Low | {articles} |

## Recommended Actions

1. **Resolve:** {contradiction} — suggested owner: {role from _role-registry.json}
2. **Fill gap:** {gap description} — create article in {topic}
3. **Update:** {stale article} — evidence is {N} months old

## Source Articles

{Numbered list of all articles analyzed with topic and path}
```

### Step 6: Save Output

1. Create `knowledge-bases/_cross-topic/` directory if it doesn't exist
2. Save synthesis to `knowledge-bases/_cross-topic/synthesis-{concept-slug}-{date}.md`
3. Optionally create `connections/` documents in relevant topics linking to the synthesis

## Output Format

| Artifact | Location | Description |
|---|---|---|
| Synthesis document | `_cross-topic/synthesis-{concept}-{date}.md` | Full synthesis with frontmatter |
| Connection stubs | `{topic}/wiki/connections/` | Optional links from topic wikis to synthesis |
| Gap report | stdout | Summary of gaps and contradictions for immediate attention |

## Composability

- **kb-search**: Discovers articles across topics by keyword
- **kb-query**: Deep-reads specific articles for claim extraction
- **kb-lint**: Cross-topic gap detection feeds candidate clusters
- **wiki-connection-discoverer**: Shares overlap detection methodology
- **kb-daily-report**: Cross-topic synthesis findings can feed into daily intelligence
- **competitive-archetype-matrix**: Can consume synthesis output for competitive topics

## Constraints

- Minimum 2 topics required for synthesis — single-topic requests redirect to `kb-compile`
- Every claim in the synthesis MUST cite its source article(s)
- Contradictions are reported, not resolved — the skill flags them for human decision
- Prior synthesis documents are preserved — new runs create new dated files
- The `_cross-topic/` directory is shared across all topics
- Gap identification considers `_role-registry.json` to determine expected coverage

## Examples

### Example 1: Multi-topic synthesis

**Trigger:** User says: "Synthesize engineering-standards and product-strategy on API design"

**Actions:** (1) Search both topics for articles mentioning "API". (2) Identify shared concepts and different perspectives. (3) Detect consensus and contradictions. (4) Generate synthesis document with unified narrative. (5) Save to `knowledge-bases/_cross-topic/`.

**Result:** One dated synthesis file with consensus, contradictions, gaps, and cited sources.

### Example 2: All-topic synthesis

**Trigger:** User says: "KB 전체에서 'observability' 관련 내용 통합해줘"

**Actions:** (1) Scan all KB topics for "observability" mentions. (2) Cluster related articles across topics. (3) Synthesize into a single document with per-topic perspective sections.

**Result:** Cross-topic observability synthesis with explicit per-topic lenses and evidence.

## Error Handling

| Error | Action |
|-------|--------|
| Search returns zero matches across all topics | Report "no content found" and suggest alternative search terms |
| Only one topic has relevant content | Produce single-topic summary instead of cross-topic synthesis |
| Contradictory claims detected | Flag contradiction with source references; do not resolve — present both perspectives |
| Topic directory missing `wiki/` | Skip topic with warning and continue with remaining topics |

## Gotchas

- **Symptom:** Unfocused mega-documents after one run. **Root cause:** Synthesizing 5+ topics without scoping. **Correct approach:** Limit to 2-3 most relevant topics per run or require explicit topic list.
- **Symptom:** False "alignment" between topics. **Root cause:** Same word, different domain meaning (e.g. "model" in engineering vs finance). **Correct approach:** Verify semantic alignment before merging claims.
- **Symptom:** Spurious contradictions in the report. **Root cause:** Treating different scopes (strategy vs implementation depth) as conflicting claims. **Correct approach:** Only flag contradictions when claims actually disagree at the same scope; silence is not contradiction.

## Output Discipline

- Do not merge perspectives that genuinely conflict — present them as distinct viewpoints with evidence.
- Do not fabricate connections between topics that share only superficial terminology.
- Synthesis documents should be shorter than the sum of their source articles.

## Honest Reporting

- Report the number of source articles actually consulted, not the total in the KB.
- When synthesis reveals genuine knowledge gaps, flag them as "gap identified" rather than filling them with speculation.
- If one topic dominates the synthesis due to more content, disclose the imbalance.
