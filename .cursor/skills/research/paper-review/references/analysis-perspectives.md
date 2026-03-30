# Multi-Perspective Analysis Definitions

Each perspective agent receives:
1. The paper review markdown from Phase 2
2. The extracted paper content from Phase 1
3. The perspective-specific instructions below

Agents apply PM/research skill frameworks to the paper's proposed method,
system, or technology — treating the research contribution as if it were a
potential product, service, or technology to commercialize or adopt.

---

## Perspective 1: PM Strategy Analysis

**Skill**: `pm-product-strategy`
**Output file**: `{paper-id}-pm-strategy-{DATE}.md`
**Sub-skills to apply**: `swot-analysis`, `value-proposition`, `lean-canvas`

### Instructions for the Agent

Treat the paper's proposed method/system as a potential product or technology
platform. Apply the following frameworks:

#### 1. SWOT Analysis
- **Strengths**: Technical advantages demonstrated in the paper (performance,
  efficiency, scalability)
- **Weaknesses**: Limitations acknowledged in the paper + those identified in
  the review
- **Opportunities**: Market gaps this technology could fill, adjacent
  applications, industry trends favoring adoption
- **Threats**: Competing approaches, regulatory risks, adoption barriers,
  faster-moving competitors

#### 2. Value Proposition Canvas
- **Customer Jobs**: What tasks do target users (researchers, engineers,
  companies) need to accomplish?
- **Pains**: What problems exist with current solutions?
- **Gains**: What benefits does this paper's approach provide?
- **Products/Services**: What could be built on this research?
- **Pain Relievers**: How does this approach address existing pains?
- **Gain Creators**: What new value does it enable?

#### 3. Lean Canvas
Fill a lean canvas treating the research as a startup idea:
Problem, Solution, Key Metrics, Unique Value Proposition, Unfair Advantage,
Channels, Customer Segments, Cost Structure, Revenue Streams.

### Output Template

```markdown
# PM Strategy Analysis: {Paper Title}

## SWOT Analysis
### Strengths
### Weaknesses
### Opportunities
### Threats

## Value Proposition Canvas
### Customer Profile
### Value Map

## Lean Canvas
| Block | Content |
|-------|---------|
| Problem | |
| Solution | |
| ...     | |

## Strategic Implications
{2-3 paragraphs synthesizing the strategic outlook}
```

---

## Perspective 2: Market Research Analysis

**Skill**: `pm-market-research`
**Output file**: `{paper-id}-market-research-{DATE}.md`
**Sub-skills to apply**: `market-sizing`, `competitor-analysis`, `user-personas`

### Instructions for the Agent

Analyze the market landscape for the technology/method proposed in the paper.

#### 1. Market Sizing (TAM/SAM/SOM)
- **TAM**: Total addressable market for the problem domain
- **SAM**: Serviceable addressable market with this specific approach
- **SOM**: Realistic obtainable market in 1-3 years

#### 2. Competitive Landscape
- Identify 5-10 competing approaches (from Related Work section and beyond)
- Compare on: performance, cost, ease of adoption, maturity, ecosystem
- Create a competitive positioning map

#### 3. User Personas
- Create 2-3 user personas who would benefit from this technology
- Include: role, goals, pain points, technical proficiency, decision criteria

### Output Template

```markdown
# Market Research Analysis: {Paper Title}

## Market Sizing
### TAM
### SAM
### SOM

## Competitive Landscape
| Competitor | Approach | Performance | Maturity | Adoption Barrier |
|------------|----------|-------------|----------|-----------------|
| ...        | ...      | ...         | ...      | ...             |

## User Personas
### Persona 1: {Name/Role}
### Persona 2: {Name/Role}

## Market Opportunities & Risks
```

---

## Perspective 3: Product Discovery Analysis

**Skill**: `pm-product-discovery`
**Output file**: `{paper-id}-discovery-{DATE}.md`
**Sub-skills to apply**: `identify-assumptions-new`, `opportunity-solution-tree`,
`brainstorm-experiments-new`

### Instructions for the Agent

Apply product discovery frameworks to validate whether this research can
translate into a viable product or feature.

#### 1. Assumption Identification
- List the key assumptions the paper makes (technical, market, user)
- Classify each as: validated (by paper experiments), partially validated,
  unvalidated
- Prioritize by risk × impact

#### 2. Opportunity Solution Tree
- Root: The overarching opportunity this research addresses
- Opportunities: Specific sub-problems it could solve
- Solutions: Concrete product/feature ideas based on the paper
- Experiments: How to validate each solution

#### 3. Experiment Design
- For the top 3 riskiest assumptions, design validation experiments
- Include: hypothesis, method, success criteria, timeline, cost estimate

### Output Template

```markdown
# Product Discovery Analysis: {Paper Title}

## Key Assumptions
| # | Assumption | Type | Status | Risk | Impact |
|---|------------|------|--------|------|--------|
| 1 | ...        | ...  | ...    | ...  | ...    |

## Opportunity Solution Tree
### Root Opportunity
### Sub-Opportunities
### Solution Ideas
### Validation Experiments

## Experiment Designs
### Experiment 1: {Title}
### Experiment 2: {Title}
### Experiment 3: {Title}

## Discovery Summary
```

---

## Perspective 4: GTM Analysis

**Skill**: `pm-go-to-market`
**Output file**: `{paper-id}-gtm-{DATE}.md`
**Sub-skills to apply**: `gtm-strategy`, `ideal-customer-profile`, `beachhead-segment`

### Instructions for the Agent

Design a go-to-market strategy for commercializing this research.

#### 1. GTM Strategy
- Define the go-to-market motion (product-led, sales-led, community-led)
- Map the adoption journey from research to production deployment
- Identify key channels and partnerships

#### 2. Ideal Customer Profile (ICP)
- Industry verticals most likely to adopt
- Company size and technical maturity
- Decision maker roles and buying criteria
- Budget considerations

#### 3. Beachhead Segment
- Identify the single best initial market segment
- Justify with: urgency, willingness to pay, accessibility, strategic value
- Define the wedge strategy to expand from beachhead

### Output Template

```markdown
# GTM Analysis: {Paper Title}

## GTM Strategy
### Motion Type
### Adoption Journey
### Key Channels

## Ideal Customer Profile
### Industry Verticals
### Company Profile
### Decision Makers

## Beachhead Segment
### Target Segment
### Justification
### Expansion Strategy

## GTM Risks & Mitigations
```

---

## Perspective 5: Statistical / Methodology Review

**Skill**: `kwp-data-statistical-analysis`
**Output file**: `{paper-id}-statistics-{DATE}.md`

### Instructions for the Agent

Evaluate the rigor and validity of the paper's experimental methodology.

#### Areas to Assess

1. **Experimental Design**
   - Sample sizes and statistical power
   - Control conditions and baselines
   - Randomization and bias prevention

2. **Statistical Methods**
   - Appropriateness of chosen metrics
   - Significance testing (if present)
   - Confidence intervals and error bars
   - Multiple comparison corrections

3. **Reproducibility Assessment**
   - Hyperparameter reporting completeness
   - Random seed handling
   - Hardware/software version reporting
   - Dataset availability and preprocessing details

4. **Common Pitfalls Check**
   - Cherry-picking results
   - Survivorship bias
   - Data leakage between train/test
   - Overfitting to benchmarks

### Output Template

```markdown
# Statistical / Methodology Review: {Paper Title}

## Experimental Design Assessment
### Strengths
### Concerns

## Statistical Rigor
### Metrics Appropriateness
### Significance Testing
### Missing Statistical Analysis

## Reproducibility Score
| Criterion | Score (1-5) | Notes |
|-----------|-------------|-------|
| Code availability | | |
| Data availability | | |
| Hyperparameter disclosure | | |
| Compute requirements stated | | |
| Random seed handling | | |

## Potential Pitfalls Identified

## Methodology Recommendations
```

---

## Perspective 6: Execution Planning

**Skills**: `pm-execution` + `pm-marketing-growth`
**Output file**: `{paper-id}-execution-{DATE}.md`
**Sub-skills to apply**: `create-prd` (pm-execution), `positioning-ideas` +
`north-star-metric` (pm-marketing-growth)

### Instructions for the Agent

Create an execution plan for turning this research into a product or feature.

#### 1. Mini-PRD
- Problem statement (from paper)
- Proposed solution (simplified for product context)
- User stories (3-5 core scenarios)
- Success criteria and acceptance tests
- Technical requirements and constraints
- Timeline estimate (MVP → V1 → V2)

#### 2. Positioning
- 3 positioning statement candidates
- Differentiation pillars vs. existing solutions
- Messaging framework for different audiences

#### 3. North Star Metric
- Define the primary metric that captures this technology's core value
- Supporting metrics and leading indicators
- Anti-metrics (what not to optimize for)

### Output Template

```markdown
# Execution Planning: {Paper Title}

## Mini-PRD
### Problem Statement
### Proposed Solution
### User Stories
### Success Criteria
### Technical Requirements
### Timeline

## Positioning
### Statement 1
### Statement 2
### Statement 3
### Differentiation Pillars

## North Star Metric
### Primary Metric
### Supporting Metrics
### Anti-Metrics

## Implementation Roadmap
```

---

## Agent Prompt Template

When launching each perspective subagent, provide this context:

```
You are a {perspective_name} analyst. Analyze the following academic paper
from a {perspective_name} perspective.

## Paper Review (Korean)
{Phase 2 review markdown}

## Paper Content
{Phase 1 extracted content — trimmed to key sections if too long}

## Your Task
{Perspective-specific instructions from above}

## Output Requirements — MANDATORY

### Language
All output MUST be written entirely in Korean (한국어). Section headings,
analysis text, tables, and conclusions — everything in Korean. English is
only allowed for proper nouns and technical terminology that has no standard
Korean equivalent (e.g., SWOT, TAM/SAM/SOM, ICP).

### Depth
- Output must be at least 80 lines of substantive analysis.
- Do NOT produce placeholder or skeleton content. Every section must contain
  specific, evidence-backed analysis with concrete data from the paper.
- Cite specific paper sections, figures, tables, equations, and numbers.
- Apply frameworks with paper-specific data, not generic textbook examples.
- Include quantitative comparisons wherever possible.

### Saving — CRITICAL
You MUST use the Write tool to save your complete output to:
  outputs/papers/{paper-id}-{perspective}-{DATE}.md

This is NOT optional. If you do not save the file, the downstream pipeline
(DOCX consolidation, PPTX generation) will fail because the content will be
missing. Verify the file exists after writing.
```
