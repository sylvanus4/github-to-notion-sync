# Content Skill Graph — Directory Template

Standard directory structure for a Content Skill Graph instance.

## Required Structure

```
content-skill-graph/
├── index.md                    # Brand identity, niche, mission, active platforms
├── audience/
│   ├── segments.md             # Target audience profiles with demographics and psychographics
│   └── pain-points.md          # Audience frustrations, fears, desires mapped to segments
├── voice/
│   ├── brand-voice.md          # Voice DNA: personality, vocabulary, patterns, always/never
│   └── platform-tone.md        # Per-platform tone shifts from the base voice
├── platforms/
│   ├── x.md                    # Twitter/X: 280 chars, thread rules, hashtag strategy
│   ├── linkedin.md             # LinkedIn: professional tone, 3000 chars, formatting
│   ├── instagram.md            # Instagram: caption + carousel, hashtag sets, CTA style
│   ├── tiktok.md               # TikTok: script format, hook-first, trending sounds
│   ├── youtube.md              # YouTube: description, timestamps, SEO tags
│   ├── threads.md              # Threads: conversational, 500 chars, no hashtags
│   ├── facebook.md             # Facebook: community tone, longer posts, share-worthy
│   └── newsletter.md           # Newsletter: subject line, preview text, sections
└── engine/
    ├── repurpose.md            # Repurposing chain order and transformation rules
    ├── hooks.md                # Hook formulas by type (curiosity, data, story, challenge)
    ├── content-types.md        # Available formats: thread, carousel, short-form, etc.
    ├── goals.md                # Content goals: awareness, trust, conversion, community
    └── schedule.md             # Posting cadence per platform (optional)
```

## Node Relationships (Wikilinks)

Every node connects to related nodes via `[[wikilinks]]`:

- `index.md` links to all top-level directories
- `audience/segments.md` ↔ `audience/pain-points.md` (segments reference pain points)
- `voice/brand-voice.md` ↔ `voice/platform-tone.md` (base voice → tone shifts)
- `platforms/*.md` → `voice/platform-tone.md` (each platform references its tone)
- `engine/repurpose.md` → `platforms/*.md` (chain references platform files)
- `engine/hooks.md` → `platforms/*.md` (hook adaptations per platform)
- `engine/goals.md` → `audience/segments.md` (goals target specific segments)

## Adding New Nodes

When adding a custom node:

1. Place it in the most relevant subdirectory
2. Add `[[wikilinks]]` to and from related existing nodes
3. Update `index.md` to reference the new node
4. Run `content-graph-audit` to verify integrity
