# Repurpose Chain Specification

Defines the transformation chain that converts a single seed post into platform-native variants.

## Chain Structure

The repurpose chain is defined in `content-skill-graph/engine/repurpose.md` and follows a strict order. Each step transforms the seed (or a prior variant) into a new platform's format.

## Default Chain Order

```
Seed Post (long-form, platform-agnostic)
  ↓
1. LinkedIn — Professional narrative, 1000-3000 chars
  ↓
2. X/Twitter — Compressed thread, 280 chars/tweet × 3-10 tweets
  ↓
3. Instagram — Visual carousel captions + CTA
  ↓
4. Threads — Conversational, 500 chars, approachable tone
  ↓
5. TikTok — Script: hook (3s) + body (30-60s) + CTA
  ↓
6. YouTube — Description + timestamps + tags
  ↓
7. Facebook — Community-style, share-worthy, longer form
  ↓
8. Newsletter — Subject line + preview + curated section
```

## Transformation Rules

Each step applies platform-specific transformations:

| Step | Source | Key Transformations |
|------|--------|---------------------|
| LinkedIn | Seed | Add professional framing, "I" perspective, line breaks, CTA |
| X | Seed | Compress to thread, numbered tweets, remove fluff |
| Instagram | Seed | Extract key points for carousel slides, add emoji, hashtag set |
| Threads | LinkedIn | Soften tone, shorten, remove hashtags, add personality |
| TikTok | Seed | Extract 3-sec hook, convert to spoken script, add visual cues |
| YouTube | Seed | SEO title, description with timestamps, tags from keywords |
| Facebook | LinkedIn | Add community question, make share-worthy, soften CTA |
| Newsletter | Seed | Curate as section, add subject line + preview text |

## Voice Application

At each step, load:
1. `voice/brand-voice.md` — base voice DNA
2. `voice/platform-tone.md` — platform-specific tone shift
3. `platforms/{name}.md` — format constraints and rules

## Skip Logic

Not all platforms are always needed. Skip conditions:
- Platform not listed in `content-skill-graph/index.md` active platforms
- User explicitly excludes a platform during production
- Platform node file is missing (warn, do not fail)

## Quality Gate

After the chain completes, each variant is scored against:
- Voice Fidelity (vs brand voice + platform tone)
- Platform Native (follows format rules)
- Hook Strength (opening line quality)
- Audience Fit (matches target segment)
- Goal Alignment (supports stated content goal)

Variants scoring below 7.0 composite are flagged for revision.
