---
name: competitive-archetype-matrix
description: >-
  Classify competitors into strategic archetypes (Hyperscaler, Vertical AI,
  MLOps Platform, Agent Platform, OSS/DIY, etc.) and generate strength/weakness
  matrices with evidence citations from KB wiki articles. Reads competitive-intel,
  sales-playbook, and product-strategy wikis to extract competitor entities,
  assign archetypes, detect archetype drift when new evidence contradicts prior
  classification, and produce comparison tables (markdown + optional HTML via
  visual-explainer).
  Use when the user asks to "classify competitors", "archetype matrix",
  "competitive archetype", "competitor classification", "strength weakness matrix",
  "competitor positioning map", "경쟁사 아키타입", "경쟁사 분류", "강점 약점 매트릭스",
  "경쟁 포지셔닝", "아키타입 드리프트", "competitive-archetype-matrix",
  "generate battlecard from KB", "archetype comparison", "경쟁사 비교 매트릭스",
  or wants to systematically classify and compare competitors using KB evidence.
  Do NOT use for one-off competitive analysis without KB context (use
  kwp-product-management-competitive-analysis or kwp-sales-competitive-intelligence).
  Do NOT use for Sun Tzu strategic framing (use sun-tzu-analyzer).
  Do NOT use for GTM battlecard creation without KB wiki data (use pm-go-to-market).
  Do NOT use for cross-topic synthesis without competitive focus (use kb-cross-topic-synthesizer).
user_invocable: true
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "knowledge-base"
  tags: ["competitive-intel", "archetype", "matrix", "positioning", "kb-domain", "battlecard"]
---

# Competitive Archetype Matrix

Classify competitors into strategic archetypes and generate evidence-backed
strength/weakness matrices from KB wiki articles.

## When to Use

- Classifying competitors from competitive-intel, sales-playbook, product-strategy wikis
- Generating archetype-based strength/weakness matrices with KB evidence citations
- Detecting archetype drift when new intelligence contradicts prior classification
- Building comparison tables for sales enablement or strategy sessions
- User says "archetype", "competitor matrix", "경쟁사 분류", "아키타입"

## Do NOT Use

- One-off competitive analysis without KB wiki data → `kwp-product-management-competitive-analysis`
- Sun Tzu strategic framing → `sun-tzu-analyzer`
- GTM battlecard without KB context → `pm-go-to-market`
- General cross-topic synthesis → `kb-cross-topic-synthesizer`

## Architecture

```
Competitive Archetype Matrix
├── Scan KB wikis (competitive-intel, sales-playbook, product-strategy)
├── Extract competitor entities (names, products, signals)
├── Classify each into archetype
│   ├── Match against defined archetype taxonomy
│   ├── Score archetype fit with evidence
│   └── Detect multi-archetype overlap
├── Build strength/weakness matrix per archetype
│   ├── Gather evidence per dimension
│   ├── Cite source wiki article + section
│   └── Score relative positioning
├── Detect archetype drift
│   ├── Compare current classification to prior snapshot
│   ├── Flag contradictions or category shifts
│   └── Generate drift advisory
├── Generate comparison outputs
│   ├── Markdown matrix table
│   ├── Optional HTML via visual-explainer
│   └── Per-archetype battlecard summary
└── Archive to knowledge-bases/competitive-intel/outputs/
```

## Archetype Taxonomy

Default archetypes (extensible by user):

| Archetype | Description | Typical Players |
|---|---|---|
| **Hyperscaler** | Cloud-native AI infra bundled with IaaS | AWS, Azure, GCP |
| **Vertical AI** | Domain-specific AI solutions | Industry-focused startups |
| **MLOps Platform** | End-to-end ML lifecycle management | Weights & Biases, MLflow, Comet |
| **Agent Platform** | Autonomous agent building/orchestration | LangChain, CrewAI, AutoGen |
| **GPU Cloud** | Pure GPU compute rental | CoreWeave, Lambda, RunPod |
| **OSS/DIY** | Open-source self-hosted stacks | vLLM + Ray + K8s |
| **Horizontal SaaS** | Broad platform with AI add-ons | Salesforce Einstein, HubSpot AI |

Users can define custom archetypes inline or via YAML config.

## Execution Flow

### Step 1: Scan KB Wikis

Read wiki articles from these KB topics:
- `competitive-intel/wiki/concepts/competitive-positioning*.md`
- `competitive-intel/wiki/concepts/market-pulse-*.md`
- `sales-playbook/wiki/concepts/competitive-*.md`
- `product-strategy/wiki/concepts/competitive-*.md`

Use `kb-search` for keyword-based discovery across topics.

### Step 2: Extract Competitor Entities

For each relevant article:
1. Extract named entities (company names, product names, service names)
2. Capture associated signals: funding, product launches, partnerships, pricing changes
3. Record source article path and section for citation

### Step 3: Classify Into Archetypes

For each competitor entity:

```markdown
### {Competitor Name}

**Primary Archetype:** {archetype}
**Secondary Archetype:** {archetype or "None"}
**Confidence:** {High/Medium/Low}

**Classification Evidence:**
- {Source article}: "{relevant quote or summary}"
- {Source article}: "{relevant quote or summary}"

**Archetype Fit Signals:**
- {signal 1}
- {signal 2}
```

Classification rules:
- Assign primary archetype based on strongest evidence cluster
- Assign secondary if competitor spans two categories with substantial evidence
- Flag as "Emerging" if fewer than 3 evidence sources

### Step 4: Build Strength/Weakness Matrix

For each archetype group, evaluate across standard dimensions:

| Dimension | Description |
|---|---|
| **Compute Access** | GPU/TPU availability, pricing, scale |
| **Platform Breadth** | Range of services (training, inference, data, agents) |
| **Enterprise Readiness** | Security, compliance, SLA, support |
| **Developer Experience** | APIs, SDKs, documentation, community |
| **AI/ML Depth** | Model catalog, fine-tuning, AutoML capabilities |
| **Pricing Model** | Pay-as-you-go, committed, hybrid flexibility |
| **Ecosystem Lock-in** | Data gravity, migration difficulty, vendor dependency |

Output per archetype:

```markdown
## Archetype: {Name}

### Members
{Competitor list with primary/secondary classification}

### Strength/Weakness Matrix

| Dimension | Strength | Weakness | Evidence |
|---|---|---|---|
| Compute Access | {assessment} | {assessment} | {source article(s)} |
| Platform Breadth | {assessment} | {assessment} | {source article(s)} |
| ... | ... | ... | ... |

### Thaki Positioning Against This Archetype
- **Our advantage:** {based on product-strategy KB}
- **Our gap:** {honest assessment}
- **Recommended approach:** {engage/differentiate/avoid}
```

### Step 5: Detect Archetype Drift

Compare current classification against any prior `archetype-matrix-*.md` output:

1. Load most recent prior matrix from `competitive-intel/outputs/`
2. For each competitor, compare:
   - Primary archetype change → **DRIFT**
   - New secondary archetype → **EXPANSION**
   - Lost secondary archetype → **CONTRACTION**
   - Significant evidence shift without archetype change → **EVOLVING**
3. Generate drift report:

```markdown
## Archetype Drift Report

| Competitor | Previous | Current | Change Type | Trigger Evidence |
|---|---|---|---|---|
| {name} | {old archetype} | {new archetype} | DRIFT | {article that triggered change} |
```

### Step 6: Generate Outputs

1. **Markdown matrix**: Full report saved to `knowledge-bases/competitive-intel/outputs/archetype-matrix-{date}.md`
2. **Optional HTML**: If `--html` flag or user requests visual output, generate via `visual-explainer` with:
   - Color-coded archetype cards
   - Interactive comparison table
   - Drift timeline visualization
3. **Per-archetype battlecard summary**: One-page summaries suitable for sales enablement

## Output Format

```markdown
# Competitive Archetype Matrix — {DATE}

## Executive Summary
- **Competitors analyzed:** {N}
- **Archetypes represented:** {list}
- **Drift detected:** {count} competitors shifted

## Archetype Overview
{For each archetype: member list, key characteristics}

## Detailed Matrix
{Per-archetype strength/weakness tables from Step 4}

## Drift Report
{From Step 5, if prior data exists}

## Thaki Strategic Implications
- **Strongest positioning against:** {archetype}
- **Largest gap against:** {archetype}
- **Emerging threats:** {competitors with DRIFT or EXPANSION}

## Evidence Sources
{Numbered list of all KB articles cited}
```

## Composability

- **kb-query**: Reads competitive-intel, sales-playbook, product-strategy topics
- **kb-search**: Discovers competitor mentions across all topics
- **visual-explainer**: Renders HTML comparison tables and archetype maps
- **sun-tzu-analyzer**: Can overlay strategic terrain analysis on archetype output
- **kb-daily-report**: Drift alerts can feed into daily intelligence reports

## Constraints

- Every strength/weakness claim MUST cite a specific KB wiki article
- Never fabricate competitive intelligence — only use what exists in the KB
- Archetype taxonomy is extensible but the default set must always be available
- Prior matrix snapshots are never deleted — used for drift detection
- Output file naming: `archetype-matrix-{YYYY-MM-DD}.md`

## Examples

### Example 1: Generate archetype matrix

- **Trigger:** User says: "Classify our competitors into archetypes"
- **Actions:** Scan competitive-intel KB wiki for competitor profiles; classify each into an archetype; build strength/weakness matrix per archetype; write to `competitive-intel/outputs/`.
- **Result:** Dated markdown matrix with evidence-backed classifications.

### Example 2: Detect archetype drift

- **Trigger:** User says: "Has any competitor changed their strategy recently?"
- **Actions:** Compare current classification to the prior matrix; list shifts with evidence from recent KB articles; note strategic implications.
- **Result:** Drift report with triggers and citations, or baseline-only note if no prior snapshot exists.

## Error Handling

| Error | Action |
|-------|--------|
| competitive-intel KB has no competitor articles | Report "insufficient data" and suggest `kb-ingest` |
| Competitor has insufficient data for classification | Classify as "Unclassified" with confidence < 0.5 |
| Previous matrix not found for drift detection | Skip drift analysis; treat current run as baseline |
| Archetype taxonomy doesn't fit the industry | Suggest customizing the taxonomy and provide a template |

## Gotchas

- **Symptom:** Forced single label hides hybrid competitors. **Root cause:** One-hot archetype assignment ignores multi-vector strategy. **Correct approach:** Report primary and secondary archetypes with confidence scores.
- **Symptom:** Drift expected on first run. **Root cause:** Drift needs two timestamped matrices. **Correct approach:** First output is baseline only; explain that drift analysis starts on the next run.
- **Symptom:** Sudden reclassification after M&A news. **Root cause:** Event-driven articles overweight tactical noise vs. structural position. **Correct approach:** Weight durable structural signals higher than one-off partnership or acquisition headlines.

## Output Discipline

- Do not fabricate capabilities; every claim must cite a KB wiki article.
- Do not assign archetypes from reputation alone; require quoted or paraphrased wiki evidence.
- Matrix outputs must include source references for each classification decision.

## Honest Reporting

- Show confidence per assignment; low confidence means thin evidence, not a weak competitor.
- If the competitive-intel KB is sparse, state the limitation instead of a false-precision matrix.
- When two archetypes fit equally, report both rather than arbitrary tie-breaking.
