---
description: End-to-end pipeline that takes a meeting URL or customer interview, auto-researches market context, then writes a complete PRD with competitive analysis and market sizing. Use when "PRD from meeting", "research PRD", "미팅 기반 PRD", "requirements to PRD". Do NOT use for simple PRD without research (use pm-execution), meeting digest only (use meeting-digest). Korean triggers: "미팅 기반 PRD", "리서치 PRD", "요구사항 PRD".
---

# PRD Research Factory

## Overview
Transforms meeting content or customer interviews into a full product requirements document. Automatically researches market context, competitive landscape, and market sizing, then composes a structured PRD with feature specs, acceptance criteria, and strategic rationale.

## Autonomy Level
**L2** — Human-in-loop for approval of research scope and final PRD; automation handles research and drafting.

## Pipeline Architecture
Sequential: meeting-digest → parallel-deep-research → pm-product-discovery → pm-market-research → pm-execution (PRD) → anthropic-docx → md-to-notion.

### Mermaid Diagram
```mermaid
flowchart LR
    A[Meeting URL / Interview] --> B[meeting-digest]
    B --> C[parallel-deep-research]
    C --> D[pm-product-discovery]
    D --> E[pm-market-research]
    E --> F[pm-execution PRD]
    F --> G[anthropic-docx]
    G --> H[md-to-notion]
```

## Trigger Conditions
- User shares meeting URL or interview transcript
- "PRD from meeting", "research PRD", "미팅 기반 PRD", "requirements to PRD"
- `/prd-research-factory` with meeting link

## Skill Chain
| Step | Skill | Purpose |
|------|-------|---------|
| 1 | meeting-digest | Extract requirements, context, stakeholders from meeting |
| 2 | parallel-deep-research | Market context, competitor moves, industry trends |
| 3 | pm-product-discovery | Opportunity Solution Tree, assumption testing |
| 4 | pm-market-research | TAM/SAM/SOM, personas, competitive analysis |
| 5 | pm-execution | Write structured PRD with user stories, acceptance criteria |
| 6 | kwp-product-management-feature-spec | Feature spec refinement |
| 7 | anthropic-docx | Generate formatted Word document |
| 8 | md-to-notion | Publish to Notion product space |

## Output Channels
- **Notion**: PRD page with sub-pages for research, specs, appendix
- **Local**: DOCX file in `output/` directory

## Configuration
- `NOTION_PRODUCT_PARENT_ID`: Parent page for PRD
- Meeting source: Notion URL, local file, or raw transcript

## Example Invocation
```
"Create a PRD from this meeting: [Notion URL]"
"미팅 기반으로 PRD 작성해줘"
"Research and write PRD for customer interview transcript"
```
