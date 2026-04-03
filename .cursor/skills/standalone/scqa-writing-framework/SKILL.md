---
name: scqa-writing-framework
description: >-
  Apply the SCQA (Situation-Complication-Question-Answer) framework to structure
  any topic into a persuasive narrative for articles, threads, memos,
  presentations, and reports. Supports multi-section documents with nested SCQA
  and audience-adaptive tone. Use when the user asks to "write with SCQA",
  "SCQA framework", "structure this as SCQA", "SCQA로 써줘", "SCQA 구조",
  "situation complication question answer", "McKinsey structure", "pyramid
  principle", "narrative structure", or wants a clear problem-solution narrative
  for any content. Do NOT use for executive summaries (use
  agency-executive-summary-generator). Do NOT use for stakeholder comms (use
  kwp-product-management-stakeholder-comms). Do NOT use for internal comms with
  company formats (use anthropic-internal-comms). Do NOT use for brand voice
  enforcement (use kwp-brand-voice-brand-voice-enforcement).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "generation"
---

# SCQA Writing Framework

Structure any content using the Situation-Complication-Question-Answer framework to produce clear, persuasive narratives that guide readers from context to conclusion.

## When to Use

- Structuring a blog post, article, or thought piece around a central argument
- Writing a memo, proposal, or recommendation that needs to convince stakeholders
- Creating a Twitter/LinkedIn thread with narrative tension
- Organizing a presentation or speech around a problem-solution arc
- Drafting product announcements, strategy docs, or analysis reports
- Any content where the reader needs to understand WHY before WHAT

## Workflow

### Step 1: Gather Context

Collect the following from the user or source material:

| Input | Description | Required |
|-------|-------------|----------|
| **Topic** | The subject to write about | Yes |
| **Audience** | Who will read this (executives, engineers, public, investors) | Yes |
| **Format** | Article, thread, memo, presentation, report | Yes |
| **Tone** | Formal, conversational, technical, persuasive | No (inferred from audience) |
| **Length** | Target word count or section count | No (default: medium) |
| **Source material** | Existing docs, data, or notes to incorporate | No |

If any required input is missing, ask the user before proceeding.

### Step 2: SCQA Decomposition

Break the topic into the four SCQA components:

**S — Situation** (What everyone agrees on)
- Establish shared context the audience already accepts as true
- Use concrete facts, data points, or widely-known trends
- Length: 1-3 sentences for short-form, 1-2 paragraphs for long-form
- Tone: neutral, factual, non-controversial

**C — Complication** (What changed or went wrong)
- Introduce the tension, problem, gap, or disruption
- This is the narrative engine — make the reader feel the problem
- Use contrast against the Situation: "However...", "But...", "The problem is..."
- Length: match or exceed Situation length — the complication carries emotional weight

**Q — Question** (What the reader now wants answered)
- Crystallize the complication into a single question the reader can't ignore
- The question should feel inevitable given S and C
- Can be explicit ("So how do we...?") or implicit (the structure creates the question)
- For thread/social formats, this often becomes the hook

**A — Answer** (Your insight, solution, or recommendation)
- Deliver the resolution with evidence, reasoning, or data
- Structure as: claim → evidence → implication
- For long-form: the Answer can contain multiple sub-points, each with its own mini-SCQA
- End with a clear takeaway, CTA, or forward-looking statement

### Step 3: Format Adaptation

Adapt the SCQA structure to the target format:

| Format | Adaptation |
|--------|-----------|
| **Article/Blog** | S = opening paragraphs, C = "the problem" section, Q = transition, A = body + conclusion |
| **Twitter Thread** | Tweet 1 = S+C hook, Tweet 2-3 = Q expansion, Tweets 4-N = A with evidence, Final = CTA |
| **LinkedIn Post** | S = first line hook (C embedded), blank line, Q implied, A = value section, CTA |
| **Memo/Proposal** | S = Background, C = Problem Statement, Q = Decision Required, A = Recommendation |
| **Presentation** | S = slide 1-2, C = slide 3-4 (build tension), Q = pivot slide, A = remaining slides |
| **Report** | S = Executive Summary context, C = Key Findings, Q = Implications, A = Recommendations |

### Step 4: Write and Polish

1. Draft each SCQA section following the format adaptation
2. Verify narrative flow: S→C should create tension, C→Q should feel inevitable, Q→A should satisfy
3. Check that the Situation uses no jargon the audience wouldn't know
4. Verify the Complication has emotional or intellectual weight — if it feels flat, sharpen it
5. Confirm the Answer directly addresses the Question — no tangents

### Step 5: Nested SCQA (for long-form only)

For documents with multiple sections, apply SCQA at two levels:

- **Document-level SCQA**: The overall narrative arc
- **Section-level SCQA**: Each major section can have its own mini-SCQA that contributes to the document-level Answer

```
Document SCQA:
  S: [overall context]
  C: [overall problem]
  Q: [overall question]
  A: composed of:
    Section 1: mini-SCQA → sub-answer 1
    Section 2: mini-SCQA → sub-answer 2
    Section 3: mini-SCQA → sub-answer 3
    Synthesis: how sub-answers combine into the full Answer
```

## Output Format

```markdown
# [Title]

## SCQA Blueprint (for reference — remove before publishing)

- **Situation**: [1-sentence summary]
- **Complication**: [1-sentence summary]
- **Question**: [the core question]
- **Answer**: [1-sentence thesis]

---

## [Content in target format]

[Full content following the SCQA structure adapted to the chosen format]
```

## Examples

### Example 1: Blog article

User: "SCQA로 'AI 에이전트가 SaaS를 대체한다'는 주제로 블로그 글 써줘"

**S**: SaaS has been the dominant software delivery model for 20 years — subscription-based, browser-delivered, continuously updated.

**C**: AI agents can now perform the tasks that SaaS tools were built to assist with — scheduling, data entry, report generation — without requiring a user interface at all.

**Q**: If AI agents can do the work directly, what happens to the SaaS model built around human-operated interfaces?

**A**: SaaS won't disappear, but the value layer shifts from "tool the human uses" to "API the agent calls." Companies that expose agent-friendly APIs will thrive; those locked into GUI-only workflows will shrink.

### Example 2: Twitter thread

User: "Write a thread about why most A/B tests fail using SCQA"

**Tweet 1 (S+C hook)**: Most companies run A/B tests religiously. But 80% of their "winning" variants don't actually move the needle in production. Here's why 🧵

**Tweet 2-3 (Q)**: The question isn't whether A/B testing works — it does. The question is: why do statistically significant results fail to replicate?

**Tweets 4-7 (A)**: [Evidence-backed answer covering sample size, novelty effects, interaction effects, with data]

**Tweet 8 (CTA)**: Before you ship your next "winner," run this 3-point checklist: [actionable takeaway]

### Example 3: Internal memo

User: "Structure a memo recommending we switch from Jira to Linear"

**S (Background)**: Our engineering team has used Jira for project tracking since 2019, with 14 active projects and 200+ issues per sprint.

**C (Problem)**: Jira's configuration complexity has led to 3+ hours/week of admin overhead per team lead, custom field sprawl (47 unused fields), and consistent complaints in retro surveys (cited in 8 of last 12 retros).

**Q (Decision Required)**: Should we migrate to Linear to reduce project management overhead while maintaining our workflow requirements?

**A (Recommendation)**: Yes. Linear covers 95% of our workflow needs with zero-config defaults, and a 2-week parallel trial with Team Alpha showed 40% reduction in admin time. Migration plan attached.

## Error Handling

| Scenario | Action |
|----------|--------|
| User provides no topic | Ask: "What topic do you want to structure with SCQA?" |
| Topic is too broad | Ask the user to narrow to one claim, recommendation, or argument |
| No clear complication exists | Probe: "What's the tension, gap, or problem in this space?" |
| User wants pure information without persuasion | SCQA may not be the right framework — suggest a structured outline instead |
| Source material contradicts the SCQA thesis | Flag the contradiction; ask the user whether to adjust the thesis or acknowledge the counterpoint |

## Composability

SCQA output feeds into other skills:
- **presentation-strategist** — Use the SCQA blueprint as the presentation structure
- **content-repurposing-engine** — Repurpose the SCQA article into platform-specific formats
- **hook-generator** — Generate hooks from the Complication and Question
- **anthropic-pptx** — Turn the SCQA structure into slides
- **md-to-notion** — Publish the final content to Notion
