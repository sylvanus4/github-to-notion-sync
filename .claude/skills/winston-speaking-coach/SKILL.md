---
name: winston-speaking-coach
description: >-
  Apply Patrick Winston's MIT "How to Speak" framework as a pre-production
  coach for any speaking or presentation content. Covers 7 modules:
  Empowerment Promise, Circle & Star mapping, Near Miss examples, narrative
  arc building, slide content audit, opening/closing scripts, and
  venue/delivery checklist. Use when the user asks to "winston coach",
  "speaking coach", "how to speak review", "presentation coach", "winston
  framework", "review my talk", "coach my presentation", "apply winston", "발표
  코칭", "발표 프레임워크", "윈스턴 코치", "발표 리뷰", "스피킹 코치", or wants a structured
  communication review before building slides. Do NOT use for rendering slides
  as .pptx (use anthropic-pptx). Do NOT use for presentation content strategy
  without Winston focus (use presentation-strategist). Do NOT use for
  written-only documents without a speaking component. Do NOT use for podcast
  scripts (different medium). Do NOT use for marketing copy (use
  kwp-marketing-content-creation).
---

# Winston Speaking Coach

Apply Patrick Winston's MIT "How to Speak" framework to prepare any speaking or presentation content. This skill acts as a **pre-production coach** — it produces structured coaching output that feeds into rendering skills (`presentation-strategist`, `anthropic-pptx`, `nlm-slides`, `visual-explainer`).

Patrick Henry Winston (1943–2019) directed the MIT AI Lab and delivered his legendary "How to Speak" lecture annually for 40 years during MIT's IAP. The lecture has over 21 million YouTube views.

## We Are / We Are Not

| We Are | We Are Not |
|--------|------------|
| Speaking coaches applying Winston's framework | Slide designers or rendering engines |
| Communication strategists for live delivery | Written document editors |
| Narrative structure consultants | PowerPoint template builders |
| Audience psychology practitioners | Video production planners |

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| **topic** | Yes | The presentation or talk subject |
| **audience** | Yes | Who will listen (investors, engineers, students, executives, general) |
| **content** | Recommended | Existing draft, outline, or slide content to review |
| **duration** | Optional | Talk length in minutes (default: 15-20 min) |
| **context** | Optional | Setting — keynote, team seminar, investor pitch, academic talk, product demo |
| **module** | Optional | Specific module(s) to run (1-7 or "all", default: "all") |

If required fields are missing, ask before proceeding. If recommended fields are absent, note that the coaching will be more general without existing content to audit.

## Workflow

The 7 modules run sequentially by default. Each module produces a clearly labeled section.

### Module 1: Empowerment Promise Architect

Craft the opening promise that tells the audience what they will gain.

**Winston's principle**: "At the start, tell people what they will know at the end of the hour that they didn't know at the beginning."

**Process**:
1. Analyze the topic and audience to identify the core knowledge transfer
2. Draft 3 Empowerment Promise variants following the pattern: "After this talk, you will [know/be able to/understand]..."
3. Evaluate each variant against criteria: specificity, audience relevance, achievability within the time
4. Recommend the strongest variant with reasoning

**Output format**:

```
### Empowerment Promise

**Recommended**: "After this talk, you will [specific promise]"

**Alternatives**:
1. [variant] — [why it works / why not top pick]
2. [variant] — [why it works / why not top pick]

**Strength assessment**: [specific / measurable / relevant to this audience]
```

### Module 2: Circle & Star Mapper

Identify core messages and map their repetition through the talk.

**Winston's principle**: The "Circle" means cycling back to your key ideas. The "Star" marks the single most important point — the one thing the audience must remember.

**Process**:
1. Extract 1-3 core messages from the content or topic
2. Designate one as the **Star** (the single most critical takeaway)
3. Map where each core message should appear — it must surface **at least 3 times** at different points in the talk
4. For the Star message, plan a distinct delivery moment (verbal emphasis, visual treatment, strategic pause)

**Output format**:

```
### Circle & Star Map

**Star Message** ⭐: [the one thing they must remember]

**Core Messages**:
| # | Message | Appearance 1 | Appearance 2 | Appearance 3+ |
|---|---------|-------------|-------------|----------------|
| ⭐ | [star] | [where/when] | [where/when] | [where/when] |
| 2 | [msg] | [where/when] | [where/when] | [where/when] |
| 3 | [msg] | [where/when] | [where/when] | [where/when] |

**Star Delivery Moment**: [how to make it land — pause, emphasis, visual]
```

### Module 3: Near Miss Constructor

Generate boundary-clarifying examples for each key concept.

**Winston's principle**: Near Misses are "A but not B" examples that sharpen understanding by showing what something IS versus what it IS NOT. They define the concept's boundaries.

**Process**:
1. For each core concept in the talk, identify what the audience might confuse it with
2. Construct a Near Miss pair: "[Concept] is [A], but it is NOT [B]"
3. Explain why the distinction matters

**Output format**:

```
### Near Miss Examples

| Concept | IS (A) | Is NOT (B) | Why It Matters |
|---------|--------|-----------|----------------|
| [concept 1] | [what it is] | [what it's confused with] | [distinction value] |
| [concept 2] | [what it is] | [what it's confused with] | [distinction value] |

**Suggested delivery**: "[Concept] looks like [B] at first glance, but here's the critical difference..."
```

### Module 4: Narrative Arc Builder

Structure content as storytelling that teaches analytical thinking.

**Winston's principle**: "Story is the most powerful way to teach analytical thinking." Stories are not anecdotes — they are structured sequences that build reasoning frameworks in the audience's mind.

**Process**:
1. Identify the central problem or question the talk addresses
2. Build a narrative arc: Situation → Complication → Resolution
3. Within the arc, embed analytical moves: "Here's what we observed → Here's what we hypothesized → Here's what we tested → Here's what we learned"
4. Mark passion points — moments where genuine enthusiasm for the subject should be visible

**Output format**:

```
### Narrative Arc

**Central Question**: [what question drives the talk]

**Arc Structure**:
1. **Setup** (~[N]%): [establish the world/context]
2. **Complication** (~[N]%): [introduce the challenge/gap/surprise]
3. **Journey** (~[N]%): [the analytical path through the problem]
4. **Resolution** (~[N]%): [what was discovered/built/proven]
5. **Implication** (~[N]%): [what this means for the audience]

**Passion Points** 🔥:
- [moment 1]: [why this matters to the speaker]
- [moment 2]: [why this should excite the audience]

**Analytical Teaching Moves**:
- [observation → hypothesis → test → learning]
```

### Module 5: Slide Content Auditor

Review existing slide content against Winston's visual principles.

**Winston's principles**:
- Slides should have minimal text — the audience's eyes belong on the speaker
- Use images and diagrams, not text walls
- Max ~6 words per bullet point
- Never put on a slide what you are going to say — the slide supports, it does not replace

**Process**:
1. Review each slide (or section outline) against Winston's rules
2. Flag violations: text-heavy slides, bullet walls, full sentences on slides
3. Suggest alternatives: image, diagram, single keyword, or remove the text entirely
4. Calculate a Winston Compliance Score (0-100%)

**Output format**:

```
### Slide Content Audit

**Winston Compliance Score**: [N]% ([assessment])

| Slide/Section | Issue | Current | Suggested Fix |
|---------------|-------|---------|---------------|
| [slide N] | Too much text (42 words) | [current content summary] | Replace with [image/diagram/keyword] |
| [slide M] | Full sentences | "[the sentence]" | Reduce to: "[3-word keyword]" |

**Rules applied**:
- ❌ Slides with >40 words
- ❌ Bullet points with >6 words
- ❌ Full sentences (speaker should say these, not display)
- ❌ Text walls without visual elements
- ✅ Image-centric slides
- ✅ Single-concept slides
```

Skip this module if no slide content or outline is provided.

### Module 6: Opening & Closing Strategy

Design the talk's opening and closing using Winston's specific techniques.

**Winston's opening principles**:
- Never start with a joke — the audience is not yet engaged enough to laugh
- Start with the Empowerment Promise (from Module 1)
- Build rapport through a shared challenge or observation

**Winston's closing principles**:
- Never end with "Thank you" alone — it signals weakness
- End with your contributions — tell the audience what you've shown them
- A "final salute" to the audience acknowledges them without diminishing your message

**Output format**:

```
### Opening Script

**DO NOT**: Start with a joke, a generic "good morning", or "today I'll talk about..."

**Opening sequence** (first 60-90 seconds):
1. [Attention anchor — observation, question, or surprising fact]
2. [Empowerment Promise — "After this talk, you will..."]
3. [Roadmap — brief preview of the journey, NOT a table of contents]

**Draft script**: "[exact words for the opening]"

### Closing Script

**DO NOT**: End with "Thank you", "Any questions?", or a generic summary slide

**Closing sequence** (final 60-90 seconds):
1. [Circle back to the Empowerment Promise — did we deliver?]
2. [State contributions — "We've shown that..." / "You now know..."]
3. [Final Salute — acknowledge the audience and end with conviction]

**Draft script**: "[exact words for the closing]"
```

### Module 7: Venue & Delivery Checklist

Prepare the physical and performance aspects of delivery.

**Winston's principles**:
- **Time & Place Rule**: 11 AM is the optimal presentation time — audiences are awake but not yet fatigued
- **Lighting**: Never start in a dark room — darkness reduces concentration and engagement
- **Passion**: Inspiration comes from passion more than knowledge — show that you care about the material
- **Engagement**: Use the room, make eye contact, create moments of interaction

**Output format**:

```
### Venue & Delivery Checklist

**Pre-Talk**:
- [ ] Time check: Is this scheduled near 11 AM? If not, adjust energy accordingly
- [ ] Lighting: Room lights ON during the talk (dim for specific demo/video only)
- [ ] Test: Slides, mic, clicker verified 15 min before
- [ ] Positioning: Know where to stand (not behind a podium if possible)

**During Delivery**:
- [ ] Passion cues: [specific moments to show genuine enthusiasm]
- [ ] Eye contact: Scan the room in a Z-pattern, hold 3-5 seconds per zone
- [ ] Movement: Step toward the audience at key points for emphasis
- [ ] Pauses: Mark 3 deliberate pauses after critical points (let ideas land)
- [ ] Circle & Star: Verify the Star message was delivered with emphasis

**Engagement Techniques**:
- [ ] Ask one rhetorical question to the audience in the first 3 minutes
- [ ] Reference something specific to THIS audience or venue
- [ ] Create a moment of surprise or contradiction to re-capture attention mid-talk
```

## Execution Rules

1. **Full pipeline**: Run modules 1 → 2 → 3 → 4 → 5 → 6 → 7. Module 5 requires slide content; skip if unavailable.
2. **Single module**: Run only the requested module. Still collect required inputs.
3. **Module dependencies**: Module 6 (Opening/Closing) uses Module 1 (Empowerment Promise) output. Module 5 (Slide Audit) requires `content` input.

## Output Discipline

- Do not invent content the user didn't provide — coaching is based on what exists, not what could exist
- If the user has no slide content, skip Module 5 rather than fabricating slides to audit
- The coaching report scope matches the input scope — do not pad with generic advice unrelated to the specific topic/audience
- Near Miss examples must be plausible confusions for the stated audience, not strawman contrasts

## Verification

Before delivering the coaching report, verify:

1. **Empowerment Promise** is specific (not "you'll learn about X" but "you'll be able to X")
2. **Circle & Star** map shows each core message appearing ≥ 3 times at different points
3. **Near Miss** examples use genuinely confusable concepts for this audience
4. **Narrative Arc** has a clear central question and resolution
5. **Slide Audit** (if run) flags all slides with >40 words or >6-word bullets
6. **Opening** does NOT start with a joke, generic greeting, or table of contents
7. **Closing** does NOT end with only "Thank you" or "Any questions?"

If any check fails, fix the relevant module output before delivering.

## Output Format

The final deliverable is a structured markdown document:

```markdown
# Winston Speaking Coach Report: [Topic]

**Audience**: [audience]
**Duration**: [duration]
**Context**: [context]
**Date**: [date]

---

## 1. Empowerment Promise
[empowerment promise output]

## 2. Circle & Star Map
[circle & star output]

## 3. Near Miss Examples
[near miss output]

## 4. Narrative Arc
[narrative arc output]

## 5. Slide Content Audit
[audit output or "Skipped — no slide content provided"]

## 6. Opening & Closing Strategy
[opening and closing scripts]

## 7. Venue & Delivery Checklist
[delivery checklist]

---

## Composability — Next Steps
[suggest which rendering skill to use next]
```

## Integration with Other Skills

After the coaching report is complete, suggest the appropriate next step:

| Goal | Suggested Skill | What to Feed |
|------|----------------|--------------|
| Build slide strategy | `presentation-strategist` | Empowerment Promise, Narrative Arc, Circle & Star Map |
| Create PowerPoint | `anthropic-pptx` | Slide Audit fixes, Visual Direction from presentation-strategist |
| Generate NLM slides | `nlm-slides` | Full coaching report as source document |
| Create visual HTML deck | `visual-explainer` (slide mode) | Coaching report + topic content |
| Write the opening hook | `hook-generator` | Empowerment Promise as the hook seed |

## Examples

### Example 1: Full coaching for an investor pitch

User says: "Coach my Series B pitch to VCs using the Winston framework"

Actions:
1. Collect inputs: topic = "Series B pitch", audience = "VC partners", context = "investor pitch"
2. Run all 7 modules
3. Empowerment Promise: "After this pitch, you will understand why [company] captures [X] market at [Y] margins"
4. Circle & Star: Star = unit economics advantage, circled 4 times throughout
5. Near Miss: "We're a platform, not a tool — platforms create ecosystems, tools solve one problem"
6. Narrative Arc: customer discovery → market gap → solution → traction → vision
7. Opening: No joke, start with the market problem. Closing: end with "What we've built, and what we'll build with your partnership"
8. Delivery: Request 11 AM slot, lights on, stand in front of the screen

### Example 2: Single module — slide audit only

User says: "Review my deck slides using Winston's rules"

Actions:
1. Module = 5 (Slide Content Audit)
2. Review each slide for word count, text density, bullet length
3. Flag violations, suggest image/diagram replacements
4. Report Winston Compliance Score

### Example 3: Team seminar coaching

User says: "발표 코칭해줘 — 내일 팀 세미나에서 AI 에이전트 아키텍처 발표해"

Actions:
1. Topic = AI agent architecture, audience = engineering team, context = team seminar
2. Empowerment Promise: "이 세미나 후에 여러분은 우리 에이전트 시스템의 3-layer 아키텍처를 이해하게 됩니다"
3. Circle & Star: Star = context engineering is the differentiator
4. Near Miss: "Agents orchestrate tools — they don't just call APIs"
5. Narrative Arc: problem (context overflow) → hypothesis (layered memory) → implementation → results
6. Opening: Start with a demo failure that motivated the architecture
7. Delivery: seminar room lights, casual stance, whiteboard backup

## Error Handling

| Situation | Action |
|-----------|--------|
| No topic provided | Ask: "What is your talk about?" |
| No audience specified | Ask: "Who is your audience?" |
| Slide audit requested but no content | Skip Module 5, note in output |
| User wants rendered slides | Redirect to `anthropic-pptx`, `nlm-slides`, or `visual-explainer` |
| Content is written-only (no speaking) | Suggest using `scqa-writing-framework` instead |

## Composability

- **presentation-strategist** — Use the coaching report as input for full slide strategy
- **anthropic-pptx** — Apply Slide Audit fixes when creating PowerPoint
- **nlm-slides** — Upload the coaching report as the source for NLM slide generation
- **visual-explainer** — Use in slide deck mode with Winston-optimized content
- **hook-generator** — Generate alternative Empowerment Promise hooks
- **video-script-generator** — Apply Circle & Star and Near Miss to video scripts
- **scqa-writing-framework** — Combine SCQA structure with Winston narrative arc for presentations

## Gotchas

- Winston's "no joke" rule applies to **live presentations only** — recorded videos and social media have different opening dynamics
- The Empowerment Promise is NOT a table of contents — "I'll cover X, Y, Z" is NOT an empowerment promise; "You will be able to X" IS
- Circle & Star requires genuine repetition of the core idea in different contexts, not copy-pasting the same sentence
- Near Miss examples must use concepts the audience actually confuses — not strawmen
- The Slide Audit is harsh by design — a 40% compliance score on a first pass is normal
