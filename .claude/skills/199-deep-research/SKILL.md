---
name: 199-deep-research
description: >-
  Enterprise-grade autonomous research engine producing citation-backed
  reports with source credibility scoring, multi-provider search, and
  automated validation. Supports industry research mode (TAM/SAM, competitive
  landscape), qualitative data coding (thematic analysis), product-spec
  linking (assumption mapping), and UltraDeep subagent fan-out. Based on
  199-biotechnologies/claude-deep-research-skill.
---

# 199 Deep Research Skill

Enterprise-grade autonomous research engine. Produces citation-backed reports with source credibility scoring, multi-provider search, and automated validation.

## Core Purpose

Execute comprehensive research using an 8-phase pipeline that produces professional reports with:
- Verified, triangulated claims with 3+ independent sources
- Source credibility scoring (domain authority, recency, expertise, bias)
- Anti-hallucination citation verification
- Progressive section-by-section report assembly (unlimited length)
- Auto-continuation for reports exceeding 18,000 words
- McKinsey-style HTML output with optional PDF generation

## Research Modes

| Mode | Phases | Duration | Sources | Words |
|------|--------|----------|---------|-------|
| Quick | 3 (Scope → Retrieve → Package) | 5-10 min | 10-15 | 2,000-5,000 |
| Standard | 6 (+ Plan, Triangulate, Synthesize) | 15-30 min | 15-25 | 5,000-10,000 |
| Deep | 8 (Full pipeline) | 30-60 min | 25-40 | 10,000-15,000 |
| UltraDeep | 8 (+ parallel subagent fan-out) | 60-120 min | 40-75 | 15,000-20,000 |

### Mode Modifiers

Modifiers can be combined with any mode:

| Modifier | Flag | Effect |
|---|---|---|
| Industry | `--mode industry` | Business-intelligence templates (TAM/SAM, competitive matrix, market map) |
| Qualitative | `--qualitative` | Thematic analysis with codebook generation for interview/survey data |
| Product-Spec | `--product-spec` | Appends product implications section (assumptions, opportunities, user stories) |

### Mode Selection Decision Tree

1. User says "quick overview" or "brief summary" → **Quick**
2. User says "research [topic]" (default) → **Standard**
3. User says "deep research" or "comprehensive analysis" → **Deep**
4. User says "exhaustive" or "thorough investigation" → **UltraDeep** (with parallel subagent fan-out)
5. Topic is market/company/industry → add `--mode industry` modifier
6. Source material includes interviews/surveys → add `--qualitative` modifier
7. Research is for product decisions → add `--product-spec` modifier

## 8-Phase Pipeline

### Phase 1: SCOPE
Define research boundaries and success criteria.
- Decompose question into 3-5 core components
- Identify 2-4 stakeholder perspectives
- Define in/out scope, success criteria, assumptions

### Phase 2: PLAN
Create intelligent research roadmap.
- Identify 5-10 primary sources, 5-10 secondary sources
- Map knowledge dependencies
- Create 10-15 search query variations
- Plan triangulation approach

### Phase 3: RETRIEVE
Systematically collect information.
- Execute minimum 10 WebSearch queries with iterative refinement
- WebFetch 5-10 most promising sources for deep extraction
- Spawn 2-3 parallel retrieval subagents via Task tool
- Target 15-30 distinct sources minimum
- Ensure source diversity (academic, industry, government, news)

### Phase 4: TRIANGULATE
Validate claims across multiple independent sources.
- Every core claim must have 3+ independent sources
- Flag single-source claims as "unverified"
- Document consensus vs debate areas
- Assess credibility (domain expertise, recency, bias)

### Phase 5: SYNTHESIZE (Outline Refinement)
Connect insights and generate novel understanding.
- Identify 5-10 patterns across sources
- Map concept relationships
- Generate 3-5 insights beyond source material
- Build argument structures with evidence hierarchies

### Phase 6: CRITIQUE
Red team analysis of research quality.
- Test logical consistency, citation completeness
- Identify gaps, biases, alternative interpretations
- Challenge assumptions with counterarguments
- Generate improvement priorities

### Phase 7: REFINE
Address gaps and strengthen weak areas.
- Conduct additional research for identified gaps
- Strengthen weak arguments with more evidence
- Add missing perspectives
- Resolve contradictions

### Phase 8: PACKAGE
Deliver professional, actionable report.
- Progressive section-by-section file assembly (≤2,000 words per write)
- Complete bibliography with ALL citations (no placeholders, no ranges)
- Run validation scripts
- Generate HTML/PDF if requested

## Execution Instructions

### Step 1: Read Reference Files
Before starting research, read the following reference documents from the skill directory:

```
.cursor/skills/199-deep-research/references/methodology.md
.cursor/skills/199-deep-research/references/quality-gates.md
.cursor/skills/199-deep-research/references/report-assembly.md
.cursor/skills/199-deep-research/references/html-generation.md
.cursor/skills/199-deep-research/references/continuation.md
```

### Step 2: Select Research Mode
Use the decision tree above based on user's request.

### Step 3: Execute Pipeline Phases
Run each phase sequentially. After RETRIEVE phase, use parallel subagents:

```
Task tool (subagent_type: "generalPurpose"):
  - Subagent 1: Academic & research sources
  - Subagent 2: Industry & news sources
  - Subagent 3: Government & documentation sources
```

### Step 4: Progressive Report Assembly
Write the report section-by-section to `~/Documents/[TopicName]_Research_[YYYYMMDD]/`:

1. Write Executive Summary → save to file
2. Write Introduction → append to file
3. Write each Finding → append to file (one at a time)
4. Write Synthesis → append to file
5. Write Limitations → append to file
6. Write Recommendations → append to file
7. Write Bibliography (ALL citations) → append to file
8. Write Methodology appendix → append to file

### Step 5: Validate Report
Run validation scripts from the skill's scripts directory:

```bash
python .cursor/skills/199-deep-research/scripts/validate_report.py --report [path]
python .cursor/skills/199-deep-research/scripts/verify_citations.py --report [path]
```

If validation fails, fix issues and re-validate (max 3 retries).

### Step 6: Generate HTML (Optional)
If user requests HTML or PDF output, use the HTML generation reference and template.

## Output Contract

### Required Report Sections
1. Executive Summary (200-400 words, 3-5 bullet findings)
2. Introduction (research question, scope, methodology, assumptions)
3. Main Analysis (4-8 detailed findings, each 300-2,000 words)
4. Synthesis & Insights (patterns, novel insights, implications)
5. Limitations & Caveats (counterevidence register, gaps, uncertainties)
6. Recommendations (immediate actions, next steps, further research)
7. Bibliography (COMPLETE — every [N] citation fully listed)
8. Appendix: Methodology (process, sources, verification, claims-evidence table)

### Quality Standards
- PRECISION: Exact numbers, specific data, no fluff
- ECONOMY: No unnecessary adjectives or embellishment
- CITATION: Every factual claim followed by [N] in same sentence
- NO FABRICATION: Admit uncertainty rather than hallucinate
- NO TRUNCATION: Every section complete, no "Content continues..."
- BIBLIOGRAPHY: No ranges [8-75], no "etc.", no placeholders

### File Formats
- Primary: Markdown (.md)
- Optional: HTML (.html) via McKinsey template
- Optional: PDF (.pdf) via WeasyPrint
- State: JSON (.json) for continuation support

## Anti-Hallucination Protocol

1. Every factual claim MUST cite a source: `"Mortality decreased 23% [1]"`
2. Distinguish fact from synthesis: label speculation with "This suggests..."
3. No vague attributions: never use "research suggests" or "experts believe"
4. Admit gaps: "No sources found for X" is better than a fabricated citation
5. Run `verify_citations.py` to catch DOI failures, URL dead links, suspicious title patterns

## Auto-Continuation Protocol

When a report exceeds 18,000 words, save continuation state:

```json
{
  "report_id": "unique_id",
  "sections_completed": ["executive_summary", "introduction", ...],
  "sections_remaining": ["finding_7", "synthesis", ...],
  "citations_used": [1, 2, 3, ...],
  "next_citation_number": 42,
  "research_context": { ... }
}
```

Spawn a continuation subagent via Task tool with full context preservation.

## Examples

### Example 1: Standard Research
```
User: "Research the current state of quantum computing for enterprise applications"
Agent: Runs Standard mode (6 phases), produces ~8,000 word report with 20+ sources
```

### Example 2: Deep Research
```
User: "Deep research on the impact of AI regulation in the EU vs US"
Agent: Runs Deep mode (8 phases), produces ~12,000 word report with 35+ sources, HTML output
```

### Example 3: Quick Overview
```
User: "Quick research on WebAssembly adoption trends"
Agent: Runs Quick mode (3 phases), produces ~3,000 word report with 12 sources
```

## Industry Research Mode

Activate with `--mode industry` for company/market-focused research. This mode replaces the default academic-oriented pipeline with business-intelligence templates.

### When to Use Industry Mode

- Company or market analysis (competitive landscape, market share, positioning)
- TAM/SAM/SOM sizing for a specific product or market segment
- Industry trend synthesis across multiple verticals
- Vendor evaluation and technology landscape mapping
- Go-to-market research for a new product or region

### Industry Mode Pipeline Modifications

| Phase | Standard Mode | Industry Mode |
|---|---|---|
| SCOPE | Academic research question decomposition | Market definition, segment boundaries, key players identification |
| PLAN | Academic + news + government sources | Industry reports, SEC filings, earnings calls, analyst notes, trade publications |
| RETRIEVE | Balanced source diversity | Weighted toward: Crunchbase, PitchBook, Statista, industry blogs, LinkedIn, G2/Capterra |
| SYNTHESIZE | Pattern identification | Competitive matrix, Porter's Five Forces, market map generation |
| PACKAGE | Academic report format | Business intelligence format with executive summary, market map, competitive matrix |

### Industry Mode Report Template

```markdown
# Market Intelligence Report — {topic}

## Executive Summary
[3-5 bullet market insights]

## Market Definition & Sizing
- TAM: [total addressable market with methodology]
- SAM: [serviceable addressable market]
- SOM: [serviceable obtainable market]
- Growth rate: [CAGR with source]

## Competitive Landscape
| Company | Position | Strengths | Weaknesses | Est. Revenue |
|---|---|---|---|---|
[top 5-10 players]

## Market Map
[Segment × capability matrix or Mermaid diagram]

## Trend Analysis
[3-5 macro trends with evidence and timeline]

## Strategic Implications
[Opportunities, threats, and recommended actions]

## Bibliography
[standard citation format]
```

## Qualitative Data Coding

When research involves interview transcripts, survey open-text, user feedback, or forum discussions, apply thematic analysis with codebook generation.

### Activation

Auto-activates when source material contains:
- Interview or survey transcript format (Q&A patterns, speaker labels)
- User feedback collections (app reviews, forum threads, support tickets)
- User explicitly requests `--qualitative` flag

### Coding Workflow

1. **Open coding**: Read through source material; generate initial codes (short labels) for recurring concepts
2. **Axial coding**: Group related codes into categories; identify relationships between categories
3. **Selective coding**: Identify core themes that unify the categories; build a thematic hierarchy

### Codebook Output

Append to the report as an appendix:

```markdown
## Appendix: Qualitative Codebook

### Theme 1: {theme_name}
- **Definition**: {what this theme captures}
- **Categories**:
  - {category_a}: {definition} — Sources: [N1], [N2]
  - {category_b}: {definition} — Sources: [N3]
- **Representative quotes**:
  - "{exact quote}" — Source [N1]
  - "{exact quote}" — Source [N3]
- **Frequency**: Mentioned in N of M sources

### Theme 2: ...
```

### Quality Criteria

- Each theme must be grounded in 3+ source passages
- Codes must be mutually exclusive at the category level
- Inter-coder reliability: when multiple subagents code, compare agreement rate (target >80%)
- Negative cases: explicitly note sources that contradict the theme

## Product-Spec Linking

New output section that maps research findings to actionable product requirements. Composes `pm-product-discovery` assumption format.

### Activation

- User includes `--product-spec` flag
- Research topic is product/feature-related (auto-detected from SCOPE phase)

### Output Format

Append after Recommendations section:

```markdown
## Product Implications

### Validated Assumptions
| ID | Assumption | Evidence | Confidence | Source |
|---|---|---|---|---|
| A1 | {assumption text} | {supporting evidence} | High/Medium/Low | [N] |

### New Opportunities
| ID | Opportunity | Market Signal | Effort Est. | Priority |
|---|---|---|---|---|
| O1 | {opportunity} | {what data suggests this} | S/M/L | P0/P1/P2 |

### Risk Register
| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | {risk description} | High/Medium/Low | High/Medium/Low | {suggested action} |

### Suggested User Stories
- As a {persona}, I want {capability} so that {outcome} — backed by finding [N]
- ...

### Next Steps for Product
1. {specific next step with owner suggestion}
2. {validation experiment to run}
3. {data to collect before deciding}
```

### Integration with pm-product-discovery

The Product Implications section uses the same assumption format as `pm-product-discovery`, enabling direct import into Opportunity Solution Trees and assumption testing workflows.

## UltraDeep Subagent Fan-Out

For `UltraDeep` mode, spawn parallel Researcher subagents per research question using Cursor's `Task` tool. Adapted from Anthropic's research-agent Lead Agent pattern.

### Architecture

```
Lead Agent (this skill)
├── SCOPE & PLAN phases (sequential, in main context)
├── RETRIEVE phase (parallel fan-out)
│   ├── Researcher Subagent 1: Research Question A
│   ├── Researcher Subagent 2: Research Question B
│   ├── Researcher Subagent 3: Research Question C
│   ├── Data Analyst Subagent: Quantitative data collection
│   └── Contrarian Subagent: Counter-evidence and alternative viewpoints
├── TRIANGULATE & SYNTHESIZE (sequential, merge results)
├── CRITIQUE (parallel)
│   ├── Red Team Subagent: Attack the synthesis
│   └── Gap Analyst Subagent: Identify missing perspectives
└── REFINE & PACKAGE (sequential)
```

### Subagent Dispatch Rules

- Max 4 concurrent subagents (Cursor Task tool constraint)
- Each subagent receives: research question, source type assignment, search query list, and output file path
- Each subagent returns: `{ status, file, summary, source_count, key_findings: string[] }`
- Lead Agent merges all subagent results before TRIANGULATE phase
- If any subagent fails, Lead Agent re-runs that question directly (no retry subagent)

### UltraDeep Subagent Prompt Template

```
You are a research subagent. Your single goal is: {research_question}

Source assignment: {source_types} (e.g., "academic papers, preprints, conference proceedings")

Search queries to execute:
1. {query_1}
2. {query_2}
3. {query_3}

Requirements:
- Execute ALL search queries via WebSearch
- WebFetch the top 3-5 most promising results
- Extract: key claims, supporting data, source credibility assessment
- Write findings to: {output_file_path}
- Return JSON: { status, file, summary, source_count, key_findings }

Do NOT synthesize across sources — the Lead Agent handles synthesis.
Do NOT write prose — write structured findings only.
```

### Merge Protocol

After all subagents complete:
1. Read all subagent output files
2. Deduplicate sources (by URL and title similarity)
3. Build a unified source registry with credibility scores
4. Proceed to TRIANGULATE with the merged dataset

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
