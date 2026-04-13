---
name: content-graph-produce
description: >-
  Core content production engine that takes an idea or source content and
  generates platform-native posts using the Content Skill Graph as context.
  6-phase pipeline: ingest source, load graph context, generate seed post,
  run repurpose chain, inject hooks, and score quality. Persists intermediate
  results per phase. Use when the user asks to "produce content",
  "generate posts", "run content engine", "create content from idea",
  "콘텐츠 생산", "콘텐츠 생성", "아이디어로 콘텐츠 만들기",
  "content-graph-produce", "write posts for all platforms",
  "repurpose this content", "10-platform content", "turn this into posts",
  or wants to generate platform-native content from a single idea using
  the Content Skill Graph. Do NOT use for setting up the graph (use
  content-graph-setup). Do NOT use for calibrating voice (use
  content-graph-voice). Do NOT use for auditing graph health (use
  content-graph-audit). Do NOT use for single-platform repurposing
  without the graph (use content-repurposing-engine).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "content"
  composable_with:
    - content-graph-setup
    - content-graph-voice
    - content-repurposing-engine-pro
    - hook-generator
    - sentence-polisher
    - content-auto-gate
---

# Content Graph Produce

Generate platform-native posts from a single idea or source content by leveraging the entire Content Skill Graph for context. The graph provides brand voice, audience pain points, platform rules, hook formulas, and repurposing logic — producing content that is native to each platform rather than reformatted copies.

## Role

You are a content production engine that reads the Content Skill Graph like a brain, absorbs the brand's identity, voice, audience, and platform rules, then generates content that sounds like the brand owner wrote it natively for each platform.

## Prerequisites

- `content-skill-graph/` directory must exist with populated files
- `voice/brand-voice.md` should be calibrated (ideally via `content-graph-voice`)
- User provides a source: idea (text), URL (article/thread), or file path

## Constraints

- Do NOT modify any files in `content-skill-graph/` — only read from it
- Do NOT generate content for platforms not configured in the graph
- Do NOT skip the repurpose chain order defined in `engine/repurpose.md`
- Do NOT produce generic content — every post must reflect the voice in `voice/brand-voice.md`
- Persist every phase output to `outputs/content-graph/{date}/`

## Output Artifacts

| Phase | File | Description |
|-------|------|-------------|
| 1 - Ingest | `outputs/content-graph/{date}/01-source.md` | Cleaned source material |
| 2 - Graph Context | `outputs/content-graph/{date}/02-context.md` | Loaded graph context snapshot |
| 3 - Seed Post | `outputs/content-graph/{date}/03-seed.md` | Initial long-form seed post |
| 4 - Repurpose | `outputs/content-graph/{date}/04-platform-posts.md` | All platform-native posts |
| 5 - Hooks | `outputs/content-graph/{date}/05-hooked-posts.md` | Posts with injected hooks |
| 6 - Scored | `outputs/content-graph/{date}/06-final-scored.md` | Final posts with quality scores |

## Workflow

### Phase 1: Source Ingestion

1. Determine source type:
   - **URL**: Use `defuddle` to extract clean markdown
   - **Pasted text**: Use directly
   - **File path**: Use `Read` to load content
2. Extract core elements:
   - Main thesis / key insight
   - Supporting points (3-5)
   - Data or examples mentioned
   - Emotional angle
3. Write cleaned source to `outputs/content-graph/{date}/01-source.md`

### Phase 2: Graph Context Loading

Load and synthesize the following graph nodes into working context:

| Node | Purpose |
|------|---------|
| `index.md` | Brand identity, niche, mission |
| `voice/brand-voice.md` | Voice DNA, signature patterns, vocabulary |
| `voice/platform-tone.md` | Per-platform tone adaptations |
| `engine/repurpose.md` | Repurposing chain order and rules |
| `engine/hooks.md` | Hook formulas |
| `engine/content-types.md` | Available content formats |
| `engine/goals.md` | Content goals for alignment |
| `audience/segments.md` | Target audience profiles |
| `audience/pain-points.md` | Pain points to address |

Then load platform-specific nodes for each active platform:
- `platforms/{platform}.md` — format rules, character limits, posting style

Write the synthesized context snapshot to `outputs/content-graph/{date}/02-context.md`

### Phase 3: Seed Post Generation

Generate the initial long-form "seed" post:

1. Take the source thesis and reframe it through the brand's voice DNA
2. Address at least one pain point from `audience/pain-points.md`
3. Align with the content goal from `engine/goals.md`
4. Match a content type from `engine/content-types.md`
5. Length: 500-1500 words (the raw material for repurposing)

Apply `sentence-polisher` to the seed post for linguistic quality.

Write seed to `outputs/content-graph/{date}/03-seed.md`

### Phase 4: Repurpose Chain

Follow the chain order from `engine/repurpose.md` strictly.

For each platform in the chain:

1. Read `platforms/{platform}.md` for format rules and character limits
2. Read the tone shift from `voice/platform-tone.md`
3. **Rethink** the seed for this platform — do NOT reformat, RETHINK:
   - What angle works for this platform's audience?
   - What format fits this platform's rules?
   - How does the voice shift for this platform?
4. Generate a platform-native post that:
   - Respects character limits
   - Uses platform-appropriate formatting (hashtags, emojis, line breaks)
   - Matches the platform's tone from `voice/platform-tone.md`
   - Stands alone — someone seeing only this post understands the value

Compose with `content-repurposing-engine-pro` for platform-specific format expertise when available.

Write all platform posts to `outputs/content-graph/{date}/04-platform-posts.md`

### Phase 5: Hook Injection

For each platform post:

1. Read hook formulas from `engine/hooks.md`
2. Read platform-specific hook adaptations
3. Compose with `hook-generator` to generate 3 hook candidates per post
4. Select the best hook based on:
   - Platform fit (X needs punchy; LinkedIn needs professional curiosity)
   - Voice consistency with `voice/brand-voice.md`
   - Pain point relevance to `audience/pain-points.md`
5. Replace the opening line with the selected hook

Write hooked posts to `outputs/content-graph/{date}/05-hooked-posts.md`

### Phase 6: Quality Scoring

Score each platform post on 5 dimensions (1-10 each):

| Dimension | Criteria |
|-----------|----------|
| **Voice Fidelity** | Does it sound like the brand? Match against `voice/brand-voice.md` personality traits and signature patterns |
| **Platform Native** | Would a platform expert recognize this as native? Check format rules from `platforms/{platform}.md` |
| **Hook Strength** | Does the opening stop the scroll? Rate curiosity gap, specificity, emotional pull |
| **Audience Fit** | Does it address a pain point? Reference `audience/pain-points.md` and `audience/segments.md` |
| **Goal Alignment** | Does it serve the content goal? Check against `engine/goals.md` |

**Composite score** = average of 5 dimensions

**Quality gate**: Posts scoring < 6.0 composite are flagged for revision.

For flagged posts:
1. Identify the weakest dimension
2. Revise the post targeting that dimension
3. Re-score
4. Maximum 2 revision cycles per post

Write final scored posts to `outputs/content-graph/{date}/06-final-scored.md` with scores and any revision notes.

### Phase 7: Final Delivery

Present all posts to the user in a structured format:

```markdown
# Content Batch — {date}

## Source
{One-line summary of the original idea/content}

## Posts

### {Platform 1}
**Score**: {composite}/10 (Voice: {v}, Native: {n}, Hook: {h}, Audience: {a}, Goal: {g})

{Post content}

---

### {Platform 2}
...
```

Include a summary table:

| Platform | Score | Status |
|----------|-------|--------|
| X | 8.2 | ✅ Ready |
| LinkedIn | 7.5 | ✅ Ready |
| Instagram | 5.8 | ⚠️ Revised |

## Verification

Before reporting complete:

1. Confirm all 6 phase output files exist in `outputs/content-graph/{date}/`
2. Confirm posts were generated for every active platform in the graph
3. Confirm no post scores below 6.0 remain unflagged
4. Confirm voice/brand-voice.md was read (not assumed)
5. Confirm repurpose chain order matches `engine/repurpose.md`

```
VERDICT: PASS — {N} posts generated for {P} platforms, avg score {S}/10, all phases persisted
```

## Error Recovery

| Error | Recovery |
|-------|----------|
| `content-skill-graph/` not found | Direct user to `content-graph-setup` |
| `voice/brand-voice.md` has only wizard defaults | Warn user; suggest `content-graph-voice` first |
| Platform file missing | Skip that platform; warn user |
| Post scores consistently < 6 | Suggest re-running `content-graph-voice` for better calibration |
| `defuddle` fails on URL | Ask user to paste the content directly |
