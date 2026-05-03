---
name: presentation-strategist
description: >-
  Design presentation strategy, content, and narrative structure before
  building slides. Covers 10 modules: blueprint planning, opening hooks,
  slide-by-slide scripts, data storytelling, objection-proof slides, executive
  summaries, closing CTAs, Q&A preparation, visual direction briefs, and
  stress testing. Use when the user asks to "design a presentation", "plan my
  deck", "write a pitch", "presentation strategy", "slide script", "opening
  hook", "data storytelling", "Q&A prep", "visual direction", "stress test my
  deck", "pitch deck strategy", "keynote script", "investor pitch", "board
  deck", "presentation blueprint", "프레젠테이션 전략", "발표 설계", "슬라이드 스크립트", "발표 준비",
  "피치덱 설계", "프레젠테이션 블루프린트", "발표 자료 기획", "키노트 스크립트", "투자 발표", or any
  presentation content strategy request. Do NOT use for rendering slides as
  .pptx files (use anthropic-pptx), generating HTML slide decks (use
  generate-slides or visual-explainer), or creating PowerPoint templates (use
  anthropic-pptx).
---

# Presentation Strategist

Design compelling presentation strategy, narrative, and content before a single slide is built. This skill produces the **what to say and why** -- the strategic layer that existing rendering skills (`anthropic-pptx`, `generate-slides`) then turn into finished slides.

## We Are / We Are Not

| We Are | We Are Not |
|--------|------------|
| Presentation content strategists | Slide rendering engines |
| Narrative architects | Visual designers |
| Audience psychology experts | PowerPoint template builders |
| Data storytelling consultants | Chart/graph generators |

## Input

Gather these from the user before starting. Required fields must be collected; optional fields enhance output quality.

| Parameter | Required | Description |
|-----------|----------|-------------|
| **topic** | Yes | The presentation subject |
| **audience** | Yes | Who will watch (e.g., investors, board, engineers, customers) |
| **objective** | Recommended | What the presenter wants the audience to do after |
| **slide_count** | Optional | Target number of slides (default: 10-15) |
| **data** | Optional | Raw data, metrics, or statistics to incorporate |
| **outline** | Optional | Existing draft outline to refine or stress-test |
| **objections** | Optional | Known audience objections or concerns |
| **module** | Optional | Specific module(s) to run (1-10 or "all", default: "all") |

If the user omits required fields, ask for them before proceeding. If they omit recommended fields, infer from context and state your assumption explicitly.

## Workflow

The 10 modules are organized into 4 sequential phases. Run all phases by default, or run individual modules when the user requests a specific one.

### Phase 1: Strategy

| # | Module | Purpose |
|---|--------|---------|
| 1 | **Blueprint** | Define objective, audience, key message, emotional arc, slide flow. **Winston**: Start with an Empowerment Promise ("After this talk, you will..."). Include venue/environment checklist (lighting on, 11 AM optimal, room setup). |
| 9 | **Visual Direction** | Color palette, typography, layout principles, design rules |

### Phase 2: Content

| # | Module | Purpose |
|---|--------|---------|
| 2 | **Opening Hook** | 3 attention-capturing opening options. **Winston Rule**: Never open with a joke for live presentations — the audience is not yet engaged. Include an "Empowerment Promise" hook as one of the 3 options. |
| 3 | **Slide-by-Slide Script** | Headlines, bullets, speaker script, transitions per slide. **Winston**: Apply Circle & Star — mark which slides reinforce the core message (must appear 3+ times), mark the "Star" slide (single most important point) with distinct emphasis. Use Near Miss ("A but not B") examples on concept-defining slides. |
| 4 | **Data Storytelling** | Transform raw numbers into narrative with visual recommendations. **Winston**: Stories teach analytical thinking — structure data narratives as observation → hypothesis → test → learning, not just "here are the numbers." |
| 6 | **Executive Summary** | Single-slide distillation of the entire presentation |
| 7 | **Closing CTA** | Final slide and closing script with clear call to action. **Winston Ending**: Never end with just "Thank you" — end with contributions ("We've shown that..."), a final salute to the audience, or a forward-looking call to action. |

### Phase 3: Defense

| # | Module | Purpose |
|---|--------|---------|
| 5 | **Objection-Proof Slides** | Preemptive slides neutralizing anticipated resistance |
| 8 | **Q&A Preparation** | 10 hardest questions with answers and bridging phrases |

### Phase 4: Quality

| # | Module | Purpose |
|---|--------|---------|
| 10 | **Stress Test** | Adversarial review of every weak argument and attention drop. **Winston stress questions**: Does the opening make an Empowerment Promise? Is the core message repeated 3+ times (Circle & Star)? Do slides have minimal text (<40 words each)? Does the closing state contributions rather than just "thank you"? Are Near Miss examples used for ambiguous concepts? |

### Execution Rules

1. **Full pipeline**: Run modules in order: 1 → 9 → 2 → 3 → 4 → 6 → 7 → 5 → 8 → 10
2. **Single module**: Run only the requested module. Still collect required inputs.
3. **Module dependencies**: Module 3 (Script) benefits from Module 1 (Blueprint) output. Module 5 (Objections) requires `objections` input. Module 4 (Data) requires `data` input. Module 10 (Stress Test) requires `outline` or prior module outputs.
4. **Output per module**: Each module produces a clearly labeled markdown section with the module name as heading.

## Module Reference

Read **`references/modules.md`** for the full prompt template, expert persona, input requirements, output format, and quality criteria for each of the 10 modules.

## Output Format

The final deliverable is a structured markdown document:

```markdown
# Presentation Strategy: [Topic]

**Audience**: [audience]
**Objective**: [objective]
**Slide Count**: [count]

---

## 1. Blueprint
[blueprint output]

## 9. Visual Direction
[visual direction output]

## 2. Opening Hook
[3 hook options]

## 3. Slide-by-Slide Script
[per-slide: headline, bullets, script, transition]

...

## 10. Stress Test
[adversarial review and rewrites]
```

## Integration with Rendering Skills

After the strategy document is complete, the user can render it into slides:

- **PowerPoint (.pptx)**: Use the `anthropic-pptx` skill. Feed the Visual Direction module output as design parameters and the Slide Script module output as content.
- **HTML slides**: Run `/generate-slides` with the strategy document as input. The Visual Direction module maps to slide presets and the Script module maps to slide content.
- **NotebookLM slides**: Use the `nlm-slides` skill to upload the strategy document and generate slide decks.

Suggest the appropriate rendering path based on the user's needs, but do not render slides within this skill.

## Examples

### Example 1: Full pipeline for an investor pitch

User says: "Design a presentation for our Series B fundraise targeting VC partners"

Actions:
1. Collect inputs: topic = "Series B fundraise", audience = "VC partners", infer objective = "secure funding"
2. Run all 10 modules in pipeline order
3. Deliver structured markdown with blueprint, hooks, scripts, data narrative, objection slides, Q&A prep, visual direction, and stress test
4. Suggest: "Run `/generate-slides` or use `anthropic-pptx` to render this into slides"

### Example 2: Single module — opening hooks only

User says: "Write me 3 killer opening hooks for my quarterly business review to the board"

Actions:
1. Identify module = 2 (Opening Hook), topic = "quarterly business review", audience = "board of directors"
2. Read `references/modules.md` Module 2 template
3. Generate 3 hooks (pattern interrupt, shocking statistic, provocative question) with recommendation

### Example 3: Data storytelling with raw metrics

User says: "Turn these numbers into a story: Q1 $2.1M, Q2 $3.4M, Q3 $5.1M, Q4 $7.8M revenue"

Actions:
1. Identify module = 4 (Data Storytelling), collect audience context
2. Transform raw revenue data into narrative arc with highlight sequence, visual recommendations, and exact speaker script per data point

## Error Handling

| Situation | Action |
|-----------|--------|
| Topic is missing | Ask: "What is your presentation about?" |
| Audience is missing | Ask: "Who is your audience?" |
| Data module requested without data | Ask: "Please paste the data you want to storytell." |
| Objection module requested without objections | Ask: "What objections do you expect from the audience?" |
| Stress Test without outline | Ask: "Please provide your presentation outline or run the full pipeline first." |
| User wants rendered slides | Redirect to `anthropic-pptx` or `/generate-slides` |

## Winston Framework Integration

This skill incorporates Patrick Winston's MIT "How to Speak" principles throughout:

| Winston Principle | Where Applied |
|-------------------|--------------|
| **Empowerment Promise** | Blueprint (Module 1), Opening Hook (Module 2) |
| **No-Joke Opening** | Opening Hook (Module 2) — anti-pattern for live presentations |
| **Circle & Star** | Slide-by-Slide Script (Module 3) — core message appears 3+ times, Star slide marked |
| **Near Miss** | Slide-by-Slide Script (Module 3) — "A but not B" examples on concept slides |
| **Storytelling → Analytical Thinking** | Data Storytelling (Module 4) — observation → hypothesis → test → learning |
| **Contribution Ending** | Closing CTA (Module 7) — state what was shown, not just "thank you" |
| **Stress Test Checklist** | Stress Test (Module 10) — Winston compliance questions |

For a full Winston-only coaching session, use `winston-speaking-coach` skill first, then feed its output into this skill.
