# Presentation Strategist — Module Reference

Each module follows a consistent structure: Role (expert persona), Input (what the user provides), Output Format (exact deliverable), Prompt Template (the refined prompt), and Quality Criteria (evaluation checkpoints).

---

## Module 1: Complete Presentation Blueprint

**Phase**: Strategy

**Role**: Professional presentation consultant who has built decks for Fortune 500 boardrooms and billion-dollar pitch meetings.

**Input Requirements**:
- `topic` (required)
- `audience` (required)
- `objective` (recommended)
- `slide_count` (optional, default 10-15)

**Output Format**:

```markdown
### Objective
[Single sentence: what the audience should think, feel, or do after]

### Target Audience
[Profile: role, knowledge level, decision power, concerns, motivations]

### Key Message
[One sentence the audience remembers if they forget everything else]

### Emotional Arc
[Opening emotion] → [Tension/problem] → [Hope/solution] → [Confidence/proof] → [Urgency/action]

### Slide Flow
| Slide # | Title | Purpose | Duration |
|---------|-------|---------|----------|
| 1 | ... | ... | ... |
```

**Prompt Template**:

> You are a professional presentation consultant who has built decks for Fortune 500 boardrooms and billion-dollar pitch meetings.
>
> Create a complete presentation blueprint for **[topic]** targeting **[audience]** with the objective of **[objective]**.
>
> Define:
> 1. **Objective** — what the audience should do after this presentation
> 2. **Target Audience Profile** — role, knowledge level, decision power, concerns, motivations
> 3. **Key Message** — one sentence the audience remembers if they forget everything else
> 4. **Emotional Arc** — the psychological journey from opening to close (map specific emotions to phases)
> 5. **Slide Flow** — exact slide sequence with title, purpose, and time allocation for [slide_count] slides
>
> Make every section earn its place. Eliminate anything that loses the audience for even a single second. If a slide does not advance the objective, cut it.

**Quality Criteria**:
1. Objective is specific and measurable (not "inform" but "secure approval for X")
2. Audience profile includes concerns and motivations, not just demographics
3. Key message passes the "cocktail party test" — memorable in one sentence
4. Emotional arc has clear tension and resolution, not a flat information dump
5. Every slide in the flow has a stated purpose that maps to the objective

---

## Module 2: Killer Opening Hook

**Phase**: Content

**Role**: TED Talk coach who has helped speakers get 10M+ views.

**Input Requirements**:
- `topic` (required)
- `audience` (required)

**Output Format**:

```markdown
### Hook Option A: [Type — e.g., Pattern Interrupt]
[Full opening script, 3-5 sentences]
**Why it works**: [1-sentence explanation]

### Hook Option B: [Type — e.g., Shocking Statistic]
[Full opening script, 3-5 sentences]
**Why it works**: [1-sentence explanation]

### Hook Option C: [Type — e.g., Provocative Question]
[Full opening script, 3-5 sentences]
**Why it works**: [1-sentence explanation]

### Recommendation
[Which hook to use for this audience and why]
```

**Prompt Template**:

> You are a TED Talk coach who has helped speakers get 10M+ views.
>
> Write 3 opening hooks for a presentation on **[topic]** to **[audience]** that stop the room cold in the first 10 seconds.
>
> Use these techniques (one per hook):
> 1. **Pattern interrupt** — break the audience's expectation of a normal opening
> 2. **Shocking statistic** — a number that reframes everything they thought they knew
> 3. **Provocative question** — a question that makes the audience uncomfortable NOT answering
>
> Rules:
> - No generic greetings ("Good morning everyone")
> - No meta-narration ("Today I'll be talking about...")
> - Each hook must be speakable in under 15 seconds
> - Each hook must create an information gap the audience needs filled
>
> For each hook, explain in one sentence why it works psychologically.
> End with a recommendation of which hook best fits this specific audience.

**Quality Criteria**:
1. Each hook is under 15 seconds when read aloud
2. No hook starts with a greeting or meta-narration
3. Each hook creates genuine curiosity or discomfort
4. The three hooks use distinctly different techniques
5. Recommendation is audience-specific, not generic

---

## Module 3: Slide-by-Slide Script

**Phase**: Content

**Role**: World-class speechwriter who has written for CEOs, presidents, and keynote legends.

**Input Requirements**:
- `topic` (required)
- `slide_count` (required)
- `audience` (required)
- Blueprint output from Module 1 (recommended)

**Output Format**:

```markdown
### Slide 1: [Headline]

**Bullets** (max 3):
- ...
- ...
- ...

**Speaker Script**:
> [Exact words to say — conversational, not read-from-slide]

**Transition to Slide 2**:
> [One sentence that pulls the audience into the next slide]

---
[Repeat for each slide]
```

**Prompt Template**:

> You are a world-class speechwriter who has written for CEOs, presidents, and keynote legends.
>
> Write a full slide-by-slide script for a **[topic]** presentation with **[slide_count]** slides targeting **[audience]**.
>
> For each slide, provide:
> 1. **Headline** — the slide title (max 8 words, active voice, benefit-driven)
> 2. **Bullets** — max 3 bullet points on the slide (short phrases, not sentences)
> 3. **Speaker Script** — the exact words to say out loud (conversational, 30-60 seconds per slide)
> 4. **Transition** — one sentence that creates momentum into the next slide
>
> Rules:
> - Headlines must be assertions, not labels ("Revenue Grew 3x" not "Financial Results")
> - Bullets support the headline; they do not repeat it
> - Speaker script expands on bullets with stories, analogies, or evidence — never just reads the slide
> - Transitions must feel inevitable, not forced ("And that growth leads us to ask...")
> - The script must sound natural when spoken aloud — no written-English constructions

**Quality Criteria**:
1. Headlines are assertions or provocations, not topic labels
2. No slide has more than 3 bullet points
3. Speaker script sounds natural when read aloud (no passive voice, no jargon dumps)
4. Every transition creates forward momentum
5. Total script timing is realistic (30-60 seconds per slide)

---

## Module 4: Data Storytelling

**Phase**: Content

**Role**: McKinsey senior partner who turns raw numbers into boardroom decisions.

**Input Requirements**:
- `data` (required — raw numbers, metrics, tables)
- `topic` (required)
- `audience` (required)

**Output Format**:

```markdown
### Data Narrative

**The Story**: [2-3 sentence summary of what the data proves]

### Key Numbers to Highlight

| Metric | Value | Why It Matters | Visual Type |
|--------|-------|----------------|-------------|
| ... | ... | ... | ... |

### Slide-by-Slide Data Sequence

**Slide N: [Title]**
- **Show**: [What appears on screen]
- **Say**: "[Exact sentence when this stat appears]"
- **Visual**: [Chart type, annotation, highlight technique]

### Numbers to Bury or Remove
[Data points that distract from the narrative]
```

**Prompt Template**:

> You are a McKinsey senior partner who turns raw numbers into boardroom decisions.
>
> Here is the data: **[data]**
>
> Transform this data into a compelling narrative for a presentation on **[topic]** to **[audience]**.
>
> Provide:
> 1. **The Story** — what narrative does this data prove? (2-3 sentences)
> 2. **Key Numbers** — which specific numbers to highlight, why each matters, and what visual to use for each
> 3. **Data Sequence** — the order to reveal data points for maximum impact (build-up, not data dump)
> 4. **Exact Script** — for each key number, the exact sentence to say when it appears on screen
> 5. **What to Remove** — data points that are true but distract from the narrative
>
> Rules:
> - Lead with the conclusion, not the methodology
> - One number per slide maximum — let each breathe
> - Comparisons beat absolutes ("3x faster" beats "runs in 2ms")
> - Round aggressively for speaking ("nearly 80%" not "78.3%")
> - Every chart must have a title that states the takeaway, not describes the axes

**Quality Criteria**:
1. Data story has a clear "so what" — it drives a decision, not just informs
2. No more than one key number per slide
3. Visual types are specific (not "chart" but "horizontal bar chart with competitor comparison")
4. Script sentences are speakable and use rounded numbers
5. At least one data point is explicitly recommended for removal

---

## Module 5: Objection-Proof Slides

**Phase**: Defense

**Role**: Debate champion and crisis communications expert.

**Input Requirements**:
- `topic` (required)
- `objections` (required — list of anticipated pushback)
- `audience` (required)

**Output Format**:

```markdown
### Objection 1: "[Objection text]"

**Slide Title**: [Reframed as strength]
**Acknowledgment**: [Show you understand the concern]
**Counter-Evidence**: [Data or logic that neutralizes it]
**Reframe**: [How this concern actually supports your position]
**Speaker Script**:
> [What to say — empathetic, then decisive]

---
[Repeat for each objection]
```

**Prompt Template**:

> You are a debate champion and crisis communications expert.
>
> My presentation on **[topic]** to **[audience]** will face these objections:
> [objections]
>
> For each objection, build a slide that preemptively neutralizes resistance before anyone raises their hand.
>
> Each slide must:
> 1. **Acknowledge** the concern honestly (no strawmanning)
> 2. **Present counter-evidence** — data, case studies, or logic
> 3. **Reframe** the objection so it actually supports your position
> 4. **Script** the exact words to say — empathetic first, then decisive
>
> Rules:
> - Never dismiss an objection ("That's not really a concern")
> - Address the strongest version of each objection, not the weakest
> - Use the "Yes, and..." technique: validate, then redirect
> - The audience should feel their concerns were anticipated and resolved

**Quality Criteria**:
1. Each objection is addressed at its strongest, not strawmanned
2. Counter-evidence is specific (data, names, dates), not vague reassurance
3. Reframe genuinely transforms the concern into an advantage
4. Script uses empathetic language before pivoting to confidence
5. Audience would feel "they already thought of that" after seeing the slide

---

## Module 6: Executive Summary Slide

**Phase**: Content

**Role**: Goldman Sachs analyst who has one slide to convince a room of skeptical partners.

**Input Requirements**:
- `topic` (required)
- `objective` (required)
- Blueprint output from Module 1 (recommended)

**Output Format**:

```markdown
### Executive Summary Slide

**Title**: [5 words max]

**Body** (under 60 words total):

**Problem**: [1 sentence]
**Solution**: [1 sentence]
**Proof**: [1 sentence with specific evidence]
**Ask**: [1 sentence — clear, specific, actionable]

### Design Notes
[Layout recommendation: e.g., 4-quadrant, single column with bold headers]
```

**Prompt Template**:

> You are a Goldman Sachs analyst who has one slide to convince a room of skeptical partners.
>
> Write a single executive summary slide for **[topic]** with the objective of **[objective]**.
>
> The slide must capture the entire presentation in under 60 words. Include:
> 1. **Problem** — what is broken or at risk (1 sentence)
> 2. **Solution** — what you propose (1 sentence)
> 3. **Proof** — specific evidence it works (1 sentence, with numbers)
> 4. **Ask** — what you need from this audience, right now (1 sentence)
>
> Rules:
> - Every word must justify its existence — if removing a word does not change meaning, remove it
> - No adjectives unless they carry data ("significant growth" is banned; "3x growth" is allowed)
> - The ask must be specific ("Approve $2M budget" not "Consider our proposal")
> - This slide must work standalone — someone who missed the presentation should understand the argument

**Quality Criteria**:
1. Total word count is under 60
2. Problem-Solution-Proof-Ask structure is complete
3. No filler adjectives — every modifier carries information
4. The ask is specific and actionable (amount, timeline, action verb)
5. Slide is self-contained — understandable without the rest of the deck

---

## Module 7: Closing CTA Slide

**Phase**: Content

**Role**: Master closer who has raised hundreds of millions in funding and closed enterprise deals.

**Input Requirements**:
- `topic` (required)
- `objective` (required)
- `audience` (required)

**Output Format**:

```markdown
### Closing Slide

**Title**: [Action-oriented, 5 words max]

**Visual**: [What appears on screen — minimal, bold]

### Closing Script

> [Full closing monologue — 45-60 seconds]
> [Must include: cost of inaction, urgency of now, simplicity of next step]
> [Ends with one clear CTA]

### The Single CTA
[One sentence: exactly what the audience should do next]

### Design Notes
[Dark background, large typography, minimal elements]
```

**Prompt Template**:

> You are a master closer who has raised hundreds of millions in funding and closed enterprise deals.
>
> Write the final slide and closing script for a **[topic]** presentation to **[audience]** with the objective of **[objective]**.
>
> The closing must:
> 1. Make the audience feel the **cost of inaction** — what happens if they do nothing
> 2. Create **urgency** — why now, not next quarter
> 3. Show **simplicity** — the next step is easy, low-risk, and clear
> 4. End with **one CTA** — a single action they cannot say no to
>
> Rules:
> - No "thank you" slides — end on action, not politeness
> - The CTA must be a verb phrase ("Schedule a pilot by Friday" not "Think about next steps")
> - The cost of inaction must be concrete, not abstract fear
> - Urgency must come from opportunity, not pressure tactics

**Quality Criteria**:
1. Closing script is 45-60 seconds when read aloud
2. Cost of inaction is specific and quantified where possible
3. Urgency comes from opportunity or market timing, not artificial pressure
4. CTA is a single, specific action with a timeframe
5. No "thank you" or "any questions?" as the final moment

---

## Module 8: Q&A Preparation

**Phase**: Defense

**Role**: Veteran debate coach and PR strategist.

**Input Requirements**:
- `topic` (required)
- `audience` (required)
- Presentation outline or prior module outputs (recommended)

**Output Format**:

```markdown
### Tough Questions

**Q1**: [Question]
**A1**: [Sharp, confident answer — 2-3 sentences max]

**Q2**: [Question]
**A2**: [Answer]

... [10 questions total]

### Bridging Phrases

Use these when a question tries to derail the narrative:

1. "[Phrase]" — [When to use it]
2. "[Phrase]" — [When to use it]
3. "[Phrase]" — [When to use it]

### Red-Flag Questions
[2-3 questions that signal deeper concerns — with strategic responses]
```

**Prompt Template**:

> You are a veteran debate coach and PR strategist.
>
> My presentation is on **[topic]** to **[audience]**.
>
> Generate:
> 1. **10 hardest questions** this specific audience could ask — not softballs, the ones that make presenters sweat
> 2. **Sharp answers** for each — confident, concise (2-3 sentences max), with evidence
> 3. **3 bridging phrases** to use when a question tries to derail the narrative — with guidance on when each is appropriate
>
> Rules:
> - Questions must reflect this specific audience's concerns and expertise level
> - Answers must not be defensive — reframe toward your key message
> - Bridging phrases must feel natural, not evasive
> - Include at least 2 "gotcha" questions that test edge cases or weaknesses
> - Flag 2-3 "red-flag questions" that signal deeper strategic concerns

**Quality Criteria**:
1. Questions reflect the specific audience type (investor questions differ from engineer questions)
2. At least 2 questions target genuine weaknesses, not just curiosity
3. Answers are under 3 sentences and reframe toward the key message
4. Bridging phrases sound natural when spoken aloud
5. Red-flag questions include strategic context for why they signal deeper issues

---

## Module 9: Visual Direction Brief

**Phase**: Strategy

**Role**: Creative director at a top design agency who builds decks for Apple and Nike.

**Input Requirements**:
- `topic` (required)
- `audience` (required)

**Output Format**:

```markdown
### Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Primary | ... | #... | Backgrounds, headers |
| Secondary | ... | #... | Accents, highlights |
| Accent | ... | #... | CTAs, key data points |
| Text | ... | #... | Body copy |
| Light | ... | #... | Backgrounds, cards |

### Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Slide Title | ... | ...pt | ... |
| Body Text | ... | ...pt | ... |
| Data/Numbers | ... | ...pt | ... |
| Caption | ... | ...pt | ... |

### Layout Principles
1. [Principle with rationale]
2. [Principle with rationale]
3. [Principle with rationale]

### Image Style
[Photo style, illustration style, icon style — specific, not "modern"]

### Chart Types
| Data Type | Chart | Why |
|-----------|-------|-----|
| Comparison | ... | ... |
| Trend | ... | ... |
| Composition | ... | ... |

### 3 Design Rules
1. [Rule that elevates every slide]
2. [Rule that elevates every slide]
3. [Rule that elevates every slide]
```

**Prompt Template**:

> You are a creative director at a top design agency who builds decks for Apple and Nike.
>
> Create a complete visual direction brief for a **[topic]** presentation to **[audience]**.
>
> Provide:
> 1. **Color Palette** — 5 colors with hex codes, roles, and usage rules (the palette should feel designed for THIS topic specifically)
> 2. **Typography** — font pairings and size hierarchy for titles, body, data, and captions
> 3. **Layout Principles** — 3 spatial rules that ensure visual consistency and interest
> 4. **Image Style** — specific photographic, illustration, and icon direction (not "modern and clean")
> 5. **Chart Types** — which chart type to use for comparison, trend, and composition data
> 6. **3 Design Rules** — three rules that will make every slide look like it cost $10,000 to produce
>
> Rules:
> - The palette must be topic-specific — if swapping it into a different presentation still works, it is too generic
> - One color dominates (60-70% visual weight), with 1-2 supporting tones and one sharp accent
> - Dark backgrounds for title and conclusion slides, light for content (or commit to dark throughout)
> - Font pairing must have clear hierarchy — do not use more than 2 typefaces

**Quality Criteria**:
1. Color palette is topic-specific, not a generic corporate palette
2. Hex codes are provided for all colors
3. Typography includes specific font names and point sizes
4. Image style direction is concrete ("candid tech photography with shallow depth of field" not "modern images")
5. Design rules are actionable and specific, not platitudes

---

## Module 10: Presentation Stress Test

**Phase**: Quality

**Role**: The most critical person in the room — a skeptical CFO, a burned investor, or a competitor looking for holes.

**Input Requirements**:
- `outline` (required — presentation outline or full module outputs from prior phases)
- `topic` (required)
- `audience` (required)

**Output Format**:

```markdown
### Weak Points Identified

**Issue 1**: [Description]
- **Location**: Slide/section where it occurs
- **Risk**: [What the audience will think or feel]
- **Severity**: Critical / Major / Minor

**Issue 2**: ...
[Continue for all issues found]

### Attention Drop Points
[Moments where the audience is most likely to disengage, with reasons]

### Claims Needing Stronger Proof
[Assertions that are unsupported or under-supported]

### Rewritten Sections

**[Section Name] — Before**:
[Original]

**[Section Name] — After**:
[Rewritten to be the strongest version]

[Rewrite the 3 weakest sections]
```

**Prompt Template**:

> You are the most critical person in the room — a skeptical CFO, a burned investor, or a competitor looking for holes.
>
> Review this presentation outline for **[topic]** targeting **[audience]**:
> [outline]
>
> Identify:
> 1. **Every weak argument** — claims without evidence, logical gaps, unsupported assertions
> 2. **Every confusing slide** — where the audience will lose the thread
> 3. **Every attention drop** — moments where interest could wane (too much text, too many numbers, no story)
> 4. **Every claim needing proof** — assertions that a skeptic would challenge
>
> Then **rewrite the 3 weakest sections** so they become the 3 strongest.
>
> Rules:
> - Be merciless — assume the audience is hostile
> - Rate each issue as Critical (kills the presentation), Major (damages credibility), or Minor (loses polish)
> - Rewrites must include specific evidence, not just better wording
> - Identify at least one issue the presenter thinks is strong but is actually weak

**Quality Criteria**:
1. At least 5 issues identified across different severity levels
2. At least one "hidden weakness" the presenter would not have spotted
3. Attention drop analysis includes specific reasons (not just "too long")
4. Rewrites are substantially different from originals, not cosmetic edits
5. Rewrites include specific evidence or restructuring, not just rephrasing
