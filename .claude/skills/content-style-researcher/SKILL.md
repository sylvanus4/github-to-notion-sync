---
name: content-style-researcher
description: >-
  Learn a writer's unique style from existing content samples (blog posts,
  newsletters, tweets, articles), build a style profile (sentence patterns,
  vocabulary preferences, rhythm, tone markers, structural habits), then
  generate new long-form content that authentically mirrors that style with
  real citations and research. Distinct from content-repurposing-engine
  (reformatting existing content for platforms) and
  kwp-marketing-content-creation (channel-specific marketing copy) — this
  skill focuses on style cloning via pattern extraction from sample texts. Use
  when the user asks to "learn my writing style", "clone writing voice",
  "write like me", "content researcher", "style profile", "match my tone", "내
  글쓰기 스타일 학습", "글 스타일 클론", "내 톤으로 써줘", "스타일 프로필", "작문 패턴 분석", "글투 분석", "내 문체로
  블로그 써줘", or provides writing samples and wants new content generated in the
  same voice. Do NOT use for reformatting content across platforms (use
  content-repurposing-engine). Do NOT use for marketing copy without style
  learning (use kwp-marketing-content-creation). Do NOT use for brand voice
  guidelines from enterprise materials (use
  kwp-brand-voice-guideline-generation). Do NOT use for article editing
  without style cloning (use edit-article). Do NOT use for general
  prompt-to-content without sample-based style matching.
---

# Content Style Researcher

Learn a writer's style from samples, build a reusable style profile, and generate new content that authentically mirrors their voice with research-backed substance.

## When to Use

- You have 3+ writing samples and want Claude to match that style
- Building a ghostwriting pipeline for a specific author
- Creating content that should sound like a particular person or brand voice
- Generating blog posts, newsletters, or articles in a learned style
- Analyzing what makes a writer's voice distinctive

## When NOT to Use

- Reformatting existing content for different platforms (use `content-repurposing-engine`)
- Marketing copy without specific style samples (use `kwp-marketing-content-creation`)
- Enterprise brand voice from guidelines documents (use `kwp-brand-voice-guideline-generation`)
- Editing an article without style cloning intent (use `edit-article`)

## Workflow

### Phase 1: Collect Writing Samples

1. Gather 3-10 writing samples from the target author/voice
   - Accept: URLs (use defuddle to extract), pasted text, local files, tweet threads
   - Minimum: 3 samples (1,500+ words total)
   - Ideal: 5-10 samples across different topics (3,000-10,000 words)
2. Normalize all samples to clean markdown
3. Label each sample with source, date, and topic for reference

### Phase 2: Extract Style DNA

Analyze the collected samples across 8 dimensions:

#### 2.1 Sentence Architecture
- Average sentence length (words)
- Sentence length variance (do they mix short punchy with long flowing?)
- Opening patterns (do they lead with questions, declarations, stories, data?)
- Closing patterns (CTA, reflection, cliff-hanger, summary?)

#### 2.2 Vocabulary Fingerprint
- Signature words and phrases (used across multiple samples)
- Avoided words (common words they never use)
- Jargon level (0 = plain English, 5 = heavy domain terminology)
- Register (formal, conversational, academic, irreverent)

#### 2.3 Rhythm and Flow
- Paragraph length distribution
- Use of fragments vs complete sentences
- Transition patterns between ideas
- Cadence markers (repetition, parallelism, tricolon)

#### 2.4 Structural Habits
- How they open articles (hook type)
- Section organization (chronological, problem-solution, list, narrative)
- Use of headers, subheaders, bullets
- Typical article length and section count

#### 2.5 Rhetorical Devices
- Analogies and metaphors (frequency and type)
- Questions (rhetorical, Socratic, direct)
- Personal anecdotes (frequency, length, placement)
- Data/evidence usage (inline stats, case studies, citations)

#### 2.6 Tone Markers
- Humor level (0 = serious, 5 = comedy-driven)
- Confidence level (hedging vs assertive)
- Formality gradient per context
- Emotional range (analytical ↔ passionate)

#### 2.7 Formatting Preferences
- Bold, italic, code usage patterns
- List vs prose preference
- Link/citation style
- Image/visual reference frequency

#### 2.8 Distinctive Quirks
- Idiosyncratic punctuation (em dashes, ellipses, exclamation marks)
- Parenthetical asides frequency
- First person usage patterns
- Cultural references and allusions

Output: **Style Profile Document** — a structured markdown document capturing all 8 dimensions with examples extracted from the samples.

### Phase 3: Validate the Style Profile

1. Generate a short test paragraph (100-150 words) on a topic NOT covered in the samples
2. Present the test paragraph alongside a random sample from the original author
3. Ask: "Can you tell which one is the original?" — this is the Turing test for style cloning
4. If the style is distinguishable, identify which dimensions are off and adjust
5. Iterate until the test paragraph is indistinguishable in style (max 3 iterations)

### Phase 4: Research and Draft

When generating new content:

1. **Topic research**:
   - Use WebSearch to gather current facts, statistics, and perspectives
   - Collect 5-10 sources with real citations
   - Identify the unique angle the target writer would take on this topic
2. **Outline in their structure**:
   - Follow the structural habits from the Style Profile
   - Use their typical hook type for the opening
   - Match their section organization pattern
3. **Draft in their voice**:
   - Apply sentence architecture patterns
   - Use vocabulary fingerprint (include signature words, avoid their avoided words)
   - Match rhythm and cadence
   - Deploy their rhetorical devices at typical frequency
4. **Self-review against the Style Profile**:
   - Check each paragraph against the 8 dimensions
   - Flag any deviations and correct them

### Phase 5: Deliver and Archive

1. Output the final content in markdown
2. Include a **Style Compliance Report**:
   - Per-dimension match score (1-5)
   - Examples of style-matched elements highlighted
   - Any intentional deviations explained
3. Save the Style Profile to `outputs/style-profiles/{author-slug}.md` for reuse
4. The Style Profile can be loaded in future sessions without re-analyzing samples

## Gotchas

1. **Too few samples.** With only 1-2 samples, the profile captures topic-specific patterns rather than the writer's general style. Minimum 3 samples across different topics.
2. **Confusing format with style.** A writer may use bullets in newsletters but prose in blog posts. Separate content-type-specific formatting from their underlying voice.
3. **Over-indexing on vocabulary.** Using signature words too frequently sounds like parody. Match frequency, not just presence.
4. **Ignoring evolution.** A writer's style may have changed over time. Weight recent samples more heavily if spanning years.

## Verification

After generating content:
1. Re-read the output without the Style Profile — does it "feel" like the original author?
2. Check that signature phrases appear at roughly the same frequency as in the samples
3. Verify sentence length distribution matches the profile (±10%)
4. Confirm the structural pattern matches the author's typical article structure
5. Ensure all research citations are real and verifiable URLs

## Anti-Example

```
# BAD: Copying content, not style
"Here's the author's article with the topic swapped out"
→ Style cloning means writing NEW content in their voice, not paraphrasing.

# BAD: Over-using signature phrases
Original uses "here's the thing" once per 1000 words.
Clone uses it every paragraph.
→ Match frequency, not just presence. Parody ≠ style match.

# BAD: Ignoring structural patterns
Original always opens with a personal anecdote.
Clone opens with a statistic.
→ The opening pattern is part of the style DNA.
```

## Constraints

- Minimum 3 writing samples required before generating a Style Profile
- The Style Profile must cover all 8 dimensions — no skipping
- Generated content must include real, verifiable research citations
- Signature phrases must appear at the same approximate frequency as in samples (±20%)
- The Style Profile must be saved to `outputs/style-profiles/` for reuse
- Do NOT fabricate quotes or statistics — all data points must be from real sources
- Freedom level: **Structured** — follow the 5-phase workflow; the Style Profile dimensions are fixed but the specific patterns extracted are unique per author

## Output

1. Style Profile Document (8 dimensions with extracted examples)
2. Validation test paragraph with comparison
3. Generated content in the target style
4. Style Compliance Report (per-dimension match scores)
5. Archived Style Profile for future reuse
