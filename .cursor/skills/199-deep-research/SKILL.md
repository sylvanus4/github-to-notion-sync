---
name: 199-deep-research
version: 1.0.0
description: Enterprise-grade autonomous research engine producing citation-backed reports with source credibility scoring, multi-provider search, and automated validation. Based on 199-biotechnologies/claude-deep-research-skill.
triggers:
  - "deep research"
  - "199 deep research"
  - "comprehensive research report"
  - "research report with citations"
  - "exhaustive research"
  - "thorough investigation with bibliography"
  - "딥 리서치 보고서"
  - "인용 기반 리서치"
  - "심층 조사 보고서"
  - "199 리서치"
do_not_use:
  - For normal research/lookup requests (use parallel-web-search)
  - For daily stock analysis (use today)
  - For paper review (use paper-review)
  - For general web search (use WebSearch directly)
  - When user just needs quick answers without a formal report
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
| UltraDeep | 8 (+ extended iterations) | 60-120 min | 40-75 | 15,000-20,000 |

### Mode Selection Decision Tree

1. User says "quick overview" or "brief summary" → **Quick**
2. User says "research [topic]" (default) → **Standard**
3. User says "deep research" or "comprehensive analysis" → **Deep**
4. User says "exhaustive" or "thorough investigation" → **UltraDeep**

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
