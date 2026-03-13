---
description: Run a full product discovery cycle — ideation, assumption mapping, prioritization, experiment design
argument-hint: "<product or feature idea>"
---

# Full Product Discovery Cycle

Execute a structured product discovery process from divergent thinking to focused validation. This command chains multiple pm-product-discovery sub-skills into an end-to-end workflow.

## Usage
```
/pm-discover Smart notification system for project management
/pm-discover New product: AI writing assistant for non-native speakers
/pm-discover 프로젝트 관리 도구의 스마트 알림 시스템
```

## Workflow

### Step 1: Determine Discovery Context
Identify whether this is **existing product** (continuous discovery with real users) or **new product** (early-stage discovery without validated demand).

Ask the user:
- What are you exploring? (product idea, feature area, opportunity space)
- What do you already know? (prior research, customer feedback, data)
- What decision will this discovery inform? (build/kill, prioritization, pivot)

### Step 2: Brainstorm Ideas (Divergent Phase)
Read and apply the pm-product-discovery skill, invoking **brainstorm-ideas-existing** or **brainstorm-ideas-new** sub-skill:
- Generate ideas from PM, Designer, and Engineer perspectives
- Present top 10 ideas with brief rationale
- Ask user to select 3-5 ideas to proceed or accept all

**Checkpoint**: "Here are 10 ideas. Which ones should we validate? Pick 3-5 or proceed with all."

### Step 3: Identify Assumptions (Critical Thinking Phase)
For each selected idea, invoke **identify-assumptions-existing** or **identify-assumptions-new** sub-skill:
- Surface assumptions across risk categories: Value, Usability, Feasibility, Viability, GTM (new products only)
- Build a master list of assumptions across all ideas

### Step 4: Prioritize Assumptions (Focus Phase)
Invoke **prioritize-assumptions** sub-skill:
- Map assumptions on an Impact x Risk matrix
- Identify "leap of faith" assumptions — high impact, high uncertainty
- Rank assumptions by testing priority

**Checkpoint**: "Here are the riskiest assumptions. Which ones feel most critical to validate first?"

### Step 5: Design Experiments (Validation Phase)
For top-priority assumptions, invoke **brainstorm-experiments-existing** or **brainstorm-experiments-new** sub-skill:
- Design 1-2 experiments per key assumption
- Existing products: A/B tests, fake doors, prototypes, user testing, data analysis
- New products: XYZ hypotheses, pretotypes, landing pages, concierge MVPs
- Include success criteria, timeline, and effort for each

### Step 6: Compile Discovery Plan
Assemble everything into a discovery plan document and save as markdown.

### Step 7: Suggest Next Steps
- "Shall I **write a PRD** for the top idea?"
- "Shall I **design an interview script** to complement the experiments?"
- "Shall I **set up metrics** to track experiment outcomes?"
