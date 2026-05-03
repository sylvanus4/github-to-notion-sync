---
name: kwp-sales-create-an-asset
description: >-
  Generate tailored sales assets (landing pages, decks, one-pagers, workflow
  demos) from your deal context. Describe your prospect, audience, and goal —
  get a polished, branded asset ready to share with customers. Do NOT use for
  tasks outside the sales domain. Korean triggers: "생성", "워크플로우".
---

# Create an Asset

Generate custom sales assets tailored to your prospect, audience, and goals. Supports interactive landing pages, presentation decks, executive one-pagers, and workflow/architecture demos.

---

## Triggers

Invoke this skill when:
- User says `/create-an-asset` or `/create-an-asset [CompanyName]`
- User asks to "create an asset", "build a demo", "make a landing page", "mock up a workflow"
- User needs a customer-facing deliverable for a sales conversation

---

## Overview

This skill creates professional sales assets by gathering context about:
- **(a) The Prospect** — company, contacts, conversations, pain points
- **(b) The Audience** — who's viewing, what they care about
- **(c) The Purpose** — goal of the asset, desired next action
- **(d) The Format** — landing page, deck, one-pager, or workflow demo

The skill then researches, structures, and builds a polished, branded asset ready to share with customers.

---

## Phase 0: Context Detection & Input Collection

### Step 0.1: Detect Seller Context

From the user's email domain, identify what company they work for.

**Actions:**
1. Extract domain from user's email
2. Search: `"[domain]" company products services site:linkedin.com OR site:crunchbase.com`
3. Determine seller context:

| Scenario | Action |
|----------|--------|
| **Single-product company** | Auto-populate seller context |
| **Multi-product company** | Ask: "Which product or solution is this asset for?" |
| **Consultant/agency/generic domain** | Ask: "What company or product are you representing?" |
| **Unknown/startup** | Ask: "Briefly, what are you selling?" |

**Store seller context:**
```yaml
seller:
  company: "[Company Name]"
  product: "[Product/Service]"
  value_props:
    - "[Key value prop 1]"
    - "[Key value prop 2]"
    - "[Key value prop 3]"
  differentiators:
    - "[Differentiator 1]"
    - "[Differentiator 2]"
  pricing_model: "[If publicly known]"
```

**Persist to knowledge base** for future sessions. On subsequent invocations, confirm: "I have your seller context from last time — still selling [Product] at [Company]?"

---

### Step 0.2: Collect Prospect Context (a)

**Ask the user:**

| Field | Prompt | Required |
|-------|--------|----------|
| **Company** | "Which company is this asset for?" | ✓ Yes |
| **Key contacts** | "Who are the key contacts? (names, roles)" | No |
| **Deal stage** | "What stage is this deal?" | ✓ Yes |
| **Pain points** | "What pain points or priorities have they shared?" | No |
| **Past materials** | "Upload any conversation materials (transcripts, emails, notes, call recordings)" | No |

**Deal stage options:**
- Intro / First meeting
- Discovery
- Evaluation / Technical review
- POC / Pilot
- Negotiation
- Close

---

### Step 0.3: Collect Audience Context (b)

**Ask the user:**

| Field | Prompt | Required |
|-------|--------|----------|
| **Audience type** | "Who's viewing this?" | ✓ Yes |
| **Specific roles** | "Any specific titles to tailor for? (e.g., CTO, VP Engineering, CFO)" | No |
| **Primary concern** | "What do they care most about?" | ✓ Yes |
| **Objections** | "Any concerns or objections to address?" | No |

**Audience type options:**
- Executive (C-suite, VPs)
- Technical (Architects, Engineers, Developers)
- Operations (Ops, IT, Procurement)
- Mixed / Cross-functional

**Primary concern options:**
- ROI / Business impact
- Technical depth / Architecture
- Strategic alignment
- Risk mitigation / Security
- Implementation / Timeline

---

### Step 0.4: Collect Purpose Context (c)

**Ask the user:**

| Field | Prompt | Required |
|-------|--------|----------|
| **Goal** | "What's the goal of this asset?" | ✓ Yes |
| **Desired action** | "What should the viewer do after seeing this?" | ✓ Yes |

**Goal options:**
- Intro / First impression
- Discovery follow-up
- Technical deep-dive
- Executive alignment / Business case
- POC proposal
- Deal close

---

### Step 0.5: Select Format (d)

**Ask the user:** "What format works best for this?"

| Format | Description | Best For |
|--------|-------------|----------|
| **Interactive landing page** | Multi-tab page with demos, metrics, calculators | Exec alignment, intros, value prop |
| **Deck-style** | Linear slides, presentation-ready | Formal meetings, large audiences |
| **One-pager** | Single-scroll executive summary | Leave-behinds, quick summaries |
| **Workflow / Architecture demo** | Interactive diagram with animated flow | Technical deep-dives, POC demos, integrations |

---

### Step 0.6: Format-Specific Inputs

#### If "Workflow / Architecture demo" selected:

**First, parse from user's description.** Look for:
- Systems and components mentioned
- Data flows described
- Human interaction points
- Example scenarios

**Then ask for any gaps:**

| If Missing... | Ask... |
|---------------|--------|
| Components unclear | "What systems or components are involved? (databases, APIs, AI, middleware, etc.)" |
| Flow unclear | "Walk me through the step-by-step flow" |
| Human touchpoints unclear | "Where does a human interact in this workflow?" |
| Scenario vague | "What's a concrete example scenario to demo?" |
| Integration specifics | "Any specific tools or platforms to highlight?" |

---

## Phase 1: Research (Adaptive)

### Assess Context Richness

| Level | Indicators | Research Depth |
|-------|------------|----------------|
| **Rich** | Transcripts uploaded, detailed pain points, clear requirements | Light — fill gaps only |
| **Moderate** | Some context, no transcripts | Medium — company + industry |
| **Sparse** | Just company name | Deep — full research pass |

### Always Research:

1. **Prospect basics**
   - Search: `"[Company]" annual report investor presentation 2025 2026`
   - Search: `"[Company]" CEO strategy priorities 2025 2026`
   - Extract: Revenue, employees, key metrics, strategic priorities

2. **Leadership**
   - Search: `"[Company]" CEO CTO CIO 2025`
   - Extract: Names, titles, recent quotes on strategy/technology

3. **Brand colors**
   - Search: `"[Company]" brand guidelines`
   - Or extract from company website
   - Store: Primary color, secondary color, accent

### If Moderate/Sparse Context, Also Research:

4. **Industry context**
   - Search: `"[Industry]" trends challenges 2025 2026`
   - Extract: Common pain points, market dynamics

5. **Technology landscape**
   - Search: `"[Company]" technology stack tools platforms`
   - Extract: Current solutions, potential integration points

6. **Competitive context**
   - Search: `"[Company]" vs [seller's competitors]`
   - Extract: Current solutions, switching signals

### If Transcripts/Materials Uploaded:

7. **Conversation analysis**
   - Extract: Stated pain points, decision criteria, objections, timeline
   - Identify: Key quotes to reference (use their exact language)
   - Note: Specific terminology, acronyms, internal project names

---

## Phase 2: Structure Decision

### Interactive Landing Page

| Purpose | Recommended Sections |
|---------|---------------------|
| **Intro** | Company Fit → Solution Overview → Key Use Cases → Why Us → Next Steps |
| **Discovery follow-up** | Their Priorities → How We Help → Relevant Examples → ROI Framework → Next Steps |
| **Technical deep-dive** | Architecture → Security & Compliance → Integration → Performance → Support |
| **Exec alignment** | Strategic Fit → Business Impact → ROI Calculator → Risk Mitigation → Partnership |
| **POC proposal** | Scope → Success Criteria → Timeline → Team → Investment → Next Steps |
| **Deal close** | Value Summary → Pricing → Implementation Plan → Terms → Sign-off |

**Audience adjustments:**
- **Executive**: Lead with business impact, ROI, strategic alignment
- **Technical**: Lead with architecture, security, integration depth
- **Operations**: Lead with workflow impact, change management, support
- **Mixed**: Balance strategic + tactical; use tabs to separate depth levels

---

### Deck-Style

Same sections as landing page, formatted as linear slides:

```
1. Title slide (Prospect + Seller logos, partnership framing)
2. Agenda
3-N. One section per slide (or 2-3 slides for dense sections)
N+1. Summary / Key takeaways
N+2. Next steps / CTA
N+3. Appendix (optional — detailed specs, pricing, etc.)
```

**Slide principles:**
- One key message per slide
- Visual > text-heavy
- Use prospect's metrics and language
- Include speaker notes

---

### One-Pager

Condense to single-scroll format:

```
┌─────────────────────────────────────┐
│ HERO: "[Prospect Goal] with [Product]" │
├─────────────────────────────────────┤
│ KEY POINT 1     │ KEY POINT 2     │ KEY POINT 3     │
│ [Icon + 2-3     │ [Icon + 2-3     │ [Icon + 2-3     │
│  sentences]     │  sentences]     │  sentences]     │
├─────────────────────────────────────┤
│ PROOF POINT: [Metric, quote, or case study] │
├─────────────────────────────────────┤
│ CTA: [Clear next action] │ [Contact info] │
└─────────────────────────────────────┘
```

---

### Workflow / Architecture Demo

**Structure based on complexity:**

| Complexity | Components | Structure |
|------------|------------|-----------|
| **Simple** | 3-5 | Single-view diagram with step annotations |
| **Medium** | 5-10 | Zoomable canvas with step-by-step walkthrough |
| **Complex** | 10+ | Multi-layer view (overview → detailed) with guided tour |

**Standard elements:**

1. **Title bar**: `[Scenario Name] — Powered by [Seller Product]`
2. **Component nodes**: Visual boxes/icons for each system
3. **Flow arrows**: Animated connections showing data movement
4. **Step panel**: Sidebar explaining current step in plain language
5. **Controls**: Play / Pause / Step Forward / Step Back / Reset
6. **Annotations**: Callouts for key decision points and value-adds
7. **Data preview**: Sample payloads or transformations at each step

---

## Phase 3: Content Generation

For detailed content templates (section templates, workflow demo content, component definitions, flow steps, scenario narratives), see [references/content-generation.md](references/content-generation.md).

Key principles: reference specific pain points, use prospect's language, map seller product to prospect needs, include proof points, feel tailored not templated.

---

## Phase 4: Visual Design

For full visual design specifications (color system, typography, visual elements, workflow demo styling, component icons, brand color fallbacks), see [references/visual-design.md](references/visual-design.md).

Key elements: prospect brand colors as primary, dark theme base, Inter typography, 12px border-radius cards, smooth 200-300ms transitions.

---

## Phase 5: Clarifying Questions (REQUIRED)

**Before building any asset, always ask clarifying questions.** This ensures alignment and prevents wasted effort.

### Step 5.1: Summarize Understanding

First, show the user what you understood:

```
"Here's what I'm planning to build:

**Asset**: [Format] for [Prospect Company]
**Audience**: [Audience type] — specifically [roles if known]
**Goal**: [Purpose] → driving toward [desired action]
**Key themes**: [2-3 main points to emphasize]

[For workflow demos, also show:]
**Components**: [List of systems]
**Flow**: [Step 1] → [Step 2] → [Step 3] → ...
```

### Step 5.2: Ask Standard Questions (ALL formats)

| Question | Why |
|----------|-----|
| "Does this match your vision?" | Confirm understanding |
| "What's the ONE thing this must nail to succeed?" | Focus on priority |
| "Tone preference? (Bold & confident / Consultative / Technical & precise)" | Style alignment |
| "Focused and concise, or comprehensive?" | Scope calibration |

### Step 5.3: Ask Format-Specific Questions

#### Interactive Landing Page:
- "Which sections matter most for this audience?"
- "Any specific demos or use cases to highlight?"
- "Should I include an ROI calculator?"
- "Any competitor positioning to address?"

#### Deck-Style:
- "How long is the presentation? (helps with slide count)"
- "Presenting live, or a leave-behind?"
- "Any specific flow or narrative arc in mind?"

#### One-Pager:
- "What's the single most important message?"
- "Any specific proof point or stat to feature?"
- "Will this be printed or digital?"

#### Workflow / Architecture Demo:
- "Let me confirm the components: [list]. Anything missing?"
- "Here's the flow I understood: [steps]. Correct?"
- "Should the demo show realistic sample data, or keep it abstract?"
- "Any integration details to highlight or downplay?"
- "Should viewers be able to click through steps, or auto-play?"

### Step 5.4: Confirm and Proceed

After user responds:

```
"Got it. I have what I need. Building your [format] now..."
```

Or, if still unclear:

```
"One more quick question: [specific follow-up]"
```

**Max 2 rounds of questions.** If still ambiguous, make a reasonable choice and note: "I went with X — easy to adjust if you prefer Y."

---

## Phase 6: Build & Deliver

### Build the Asset

Following all specifications above:
1. Generate structure based on Phase 2
2. Create content based on Phase 3
3. Apply visual design based on Phase 4
4. Ensure all interactive elements work
5. Test responsiveness (if applicable)

### Output Format

**All formats**: Self-contained HTML file
- All CSS inline or in `<style>` tags
- All JS inline or in `<script>` tags
- No external dependencies (except Google Fonts)
- Single file for easy sharing

**File naming**: `[ProspectName]-[format]-[date].html`
- Example: `CentricBrands-workflow-demo-2026-01-28.html`

### Delivery Message

For delivery message, see [references/code-block-1.md](references/code-block-1.md).


---

## Phase 7: Iteration Support

After delivery, be ready to iterate:

| User Request | Action |
|--------------|--------|
| "Change the colors" | Regenerate with new palette, keep content |
| "Add a section on X" | Insert new section, maintain flow |
| "Make it shorter" | Condense, prioritize key points |
| "The flow is wrong" | Rebuild architecture based on correction |
| "Use our brand instead" | Switch from prospect brand to seller brand |
| "Add more detail on step 3" | Expand that section specifically |
| "Can I get this as a PDF?" | Provide print-optimized version |

**Remember**: Default to prospect's brand colors, but seller can adjust to their own brand or a neutral palette after initial build.

---

## Quality Checklist

Before delivering, verify:

### Content
- [ ] Prospect company name spelled correctly throughout
- [ ] Leadership names are current (not outdated)
- [ ] Pain points accurately reflect input/transcripts
- [ ] Seller's product accurately represented
- [ ] No placeholder text remaining
- [ ] Proof points are accurate and sourced

### Visual
- [ ] Brand colors applied correctly
- [ ] All text readable (contrast)
- [ ] Animations smooth, not distracting
- [ ] Mobile responsive (if interactive page)
- [ ] Dark theme looks polished

### Functional
- [ ] All tabs/sections load correctly
- [ ] Interactive elements work (calculators, demos)
- [ ] Workflow steps animate properly (if applicable)
- [ ] Navigation is intuitive
- [ ] CTA is clear and clickable

### Professional
- [ ] Tone matches audience
- [ ] Appropriate level of detail for purpose
- [ ] No typos or grammatical errors
- [ ] Feels tailored, not templated

---

## Examples

- **Executive Landing Page**: Prospect (manufacturing, C-suite) -> multi-tab interactive page with Strategic Fit, Business Impact, ROI Calculator, Security & Trust, Next Steps.
- **Technical Workflow Demo**: Prospect (IT architects, POC) -> interactive canvas with 5 component nodes, step-by-step walkthrough with sample data, Play/Pause/Step/Reset controls.
- **Sales One-Pager**: Prospect (VP Engineering, first meeting leave-behind) -> Hero headline + 3 key points + proof stat + CTA.

---

## Appendix

Component icons and brand color fallbacks are in [references/visual-design.md](references/visual-design.md).
