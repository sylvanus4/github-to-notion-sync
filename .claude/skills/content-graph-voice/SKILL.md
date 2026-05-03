---
name: content-graph-voice
description: >-
  Calibrate and maintain brand voice for the Content Skill Graph by analyzing
  real content samples, extracting voice DNA, mapping platform-specific tones,
  and validating with user feedback. Updates voice/brand-voice.md and
  voice/platform-tone.md. Use when the user asks to "calibrate voice", "update
  brand voice", "voice calibration", "tune my voice", "콘텐츠 보이스 설정", "브랜드 보이스
  분석", "톤 캘리브레이션", "content-graph-voice", "analyze my writing style", "extract
  my voice", "set up brand voice for content graph", or wants to refine the
  voice definition in an existing Content Skill Graph from real writing
  samples. Do NOT use for scaffolding a new graph from scratch (use
  content-graph-setup). Do NOT use for producing content (use
  content-graph-produce). Do NOT use for auditing graph health (use
  content-graph-audit). Do NOT use for generating brand guidelines without a
  content skill graph (use kwp-brand-voice-guideline-generation).
---

# Content Graph Voice

Analyze real content samples to extract, codify, and validate the user's brand voice. Updates `voice/brand-voice.md` and `voice/platform-tone.md` in the Content Skill Graph with empirically-derived voice DNA rather than self-reported adjectives.

## Role

You are a brand voice linguist who reverse-engineers writing style from real samples. You identify patterns in word choice, sentence structure, rhythm, and tone — then codify them into actionable guidelines an AI can follow consistently.

## Prerequisites

- `content-skill-graph/` directory must exist (created by `content-graph-setup`)
- User must provide 3-10 real content samples (URLs, pasted text, or file paths)

## Constraints

- Do NOT modify any files outside `content-skill-graph/voice/`
- Do NOT fabricate voice attributes — extract only from provided samples
- Do NOT produce content posts — this skill only calibrates the voice definition
- Do NOT delete existing voice files without user confirmation

## Workflow

### Phase 1: Graph Verification

1. Verify `content-skill-graph/` exists
2. Read `content-skill-graph/voice/brand-voice.md` (current state)
3. Read `content-skill-graph/voice/platform-tone.md` (current state)
4. If either file is missing, warn the user and offer to create from scratch or run `content-graph-setup` first

### Phase 2: Sample Collection

Ask the user for content samples using `AskQuestion`:

- "Provide 3-10 samples of your best content. These can be URLs, pasted text, or file paths. Mix of platforms is ideal."

For URLs, use `defuddle` to extract clean text content.
For file paths, use `Read` to load content.

Minimum 3 samples required. If fewer, ask for more.

### Phase 3: Voice Extraction

Analyze all samples collectively and extract:

**Voice DNA Profile**

| Dimension | Extraction Method |
|-----------|------------------|
| **Sentence length** | Measure average words/sentence across samples |
| **Vocabulary level** | Classify: casual / professional / technical / academic |
| **Tone markers** | Identify recurring emotional tones (confident, humble, urgent, etc.) |
| **Signature phrases** | Find repeated words, phrases, or patterns |
| **Structural patterns** | List patterns, bullets vs prose, question-first, etc. |
| **Personality traits** | 3-5 adjectives that describe the writing personality |
| **Forbidden patterns** | Identify what the author clearly avoids |

**Platform Tone Variations**

If samples span multiple platforms, identify how voice shifts:

| Platform | Tone Shift | Evidence |
|----------|-----------|----------|
| {platform} | {how voice changes} | {specific example from samples} |

### Phase 4: Voice Document Update

Update `content-skill-graph/voice/brand-voice.md` with extracted voice DNA:

```markdown
# Brand Voice

## Voice DNA (Calibrated from {N} samples on {date})

### Personality
- **Adjectives**: {extracted adjectives}
- **In one sentence**: {synthesized voice description}

### Linguistic Fingerprint
- **Sentence style**: {short/medium/long, simple/compound/complex}
- **Vocabulary**: {casual/professional/technical}
- **Rhythm**: {staccato/flowing/mixed}
- **POV**: {first person/second person/third person}

### Signature Patterns
{List of recurring patterns with examples}

### Always
{Behaviors consistently present in samples}

### Never
{Patterns consistently absent}

### Vocabulary
- **Favorite words**: {words that appear disproportionately}
- **Banned words**: {words never used or explicitly avoided}

## Calibration Source
- Samples analyzed: {N}
- Platforms covered: {list}
- Last calibrated: {date}

## Application
Apply this voice across all [[platforms/]] with tone adaptations per [[voice/platform-tone]].
```

Update `content-skill-graph/voice/platform-tone.md`:

```markdown
# Platform Tone Map

## Base Voice
See [[voice/brand-voice]] for the full voice DNA.

## Platform Adaptations

{For each platform in the graph}
### [[platforms/{platform}]]
- **Tone shift**: {how voice adapts}
- **Formality**: {scale 1-5}
- **Emoji usage**: {none/light/moderate/heavy}
- **Hashtag style**: {none/minimal/strategic}
- **Example**: "{Real example or adapted example}"
```

### Phase 5: Validation

Present the extracted voice profile to the user and ask for rating:

Use `AskQuestion` with:
- "Rate how accurately this voice profile captures YOUR writing style" (1-5 scale)
- "What's missing or wrong?" (free text)

If rating < 4:
1. Ask for specific corrections
2. Re-analyze with corrections applied
3. Update files
4. Re-validate

If rating >= 4:
- Finalize and confirm

### Phase 6: Compose with Brand Voice Enforcement

Optionally compose with `kwp-brand-voice-guideline-generation` if the user wants a formal brand guidelines document beyond the skill graph files.

### Phase 7: Summary

```
✅ Voice Calibration Complete

📝 Samples analyzed: {N}
🎯 Voice adjectives: {list}
📊 Platform tones mapped: {list}
⭐ User validation: {rating}/5

Updated files:
- content-skill-graph/voice/brand-voice.md
- content-skill-graph/voice/platform-tone.md

Next steps:
1. Run content-graph-produce to generate content using your calibrated voice
2. Run content-graph-audit to verify voice consistency across the graph
```

## Verification

Before reporting complete:

1. Confirm `voice/brand-voice.md` contains extracted voice DNA (not wizard defaults)
2. Confirm `voice/platform-tone.md` maps all platforms in the graph
3. Confirm user validation rating >= 4 (or corrections applied)
4. Confirm wikilinks in updated files resolve correctly

```
VERDICT: PASS — Voice calibrated from {N} samples, user rating {R}/5, {P} platforms mapped
```

## Error Recovery

| Error | Recovery |
|-------|----------|
| `content-skill-graph/` doesn't exist | Direct user to run `content-graph-setup` first |
| Fewer than 3 samples provided | Ask for more samples; explain minimum requirement |
| URL extraction fails | Ask user to paste the text directly |
| User rates < 3 | Ask specific questions about what's wrong; re-extract |
