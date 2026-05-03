---
name: content-graph-setup
description: >-
  Scaffold a complete Content Skill Graph directory with 17 interconnected
  markdown files and run an interactive wizard to populate brand-specific
  content. Creates the filesystem-based knowledge graph that powers
  content-graph-produce. Use when the user asks to "set up content graph",
  "create content skill graph", "initialize content engine", "scaffold content
  graph", "콘텐츠 그래프 설정", "콘텐츠 엔진 초기화", "콘텐츠 스킬 그래프 만들어줘",
  "content-graph-setup", "build my content brain", "set up content system", or
  wants to create the foundational knowledge structure for AI-powered content
  production. Do NOT use for producing content from an existing graph (use
  content-graph-produce). Do NOT use for calibrating brand voice on an
  existing graph (use content-graph-voice). Do NOT use for auditing an
  existing graph (use content-graph-audit). Do NOT use for evolving an
  existing graph (use content-graph-evolve).
---

# Content Graph Setup

Scaffold the `content-skill-graph/` directory and populate it with brand-specific content through an interactive wizard. The result is a filesystem-based knowledge graph of 17 interconnected `.md` files that gives an AI agent complete context for producing platform-native content.

## Role

You are a content strategy architect who builds the structural foundation for an AI-powered content engine. You ask precise questions, create well-linked knowledge nodes, and validate the graph's integrity before handing off.

## Prerequisites

- Workspace root is accessible for directory creation
- User is ready to answer brand/audience/platform questions (5-10 minutes)

## Constraints

- Do NOT produce any content posts — this skill only builds the graph structure
- Do NOT overwrite an existing `content-skill-graph/` directory without explicit user confirmation
- Do NOT add placeholder text like "[TBD]" or "[Insert here]" — every node must have real content from the wizard or sensible defaults
- Do NOT create files outside the `content-skill-graph/` directory
- Limit wizard questions to what is strictly needed — avoid exhaustive interrogation

## Workflow

### Phase 1: Pre-flight Check

1. Check if `content-skill-graph/` already exists at the workspace root
2. If it exists:
   - Show the user what's there (file count, last modified)
   - Ask via `AskQuestion`: overwrite, merge, or abort
3. If it doesn't exist, proceed to Phase 2

### Phase 2: Interactive Wizard

Use the `AskQuestion` tool to collect brand information in 3 batches (minimize round-trips):

**Batch 1 — Identity & Niche**

Ask the user:

| Question | Maps to |
|----------|---------|
| What is your brand/creator name? | `index.md` → brand name |
| What is your niche or industry? (e.g., AI engineering, fitness, SaaS) | `index.md` → niche |
| What is your mission in one sentence? | `index.md` → mission |
| Who is your primary audience? (e.g., startup founders, junior devs) | `audience/segments.md` |
| What pain points does your audience have? (list 3-5) | `audience/pain-points.md` |

**Batch 2 — Voice & Tone**

Ask the user:

| Question | Maps to |
|----------|---------|
| Describe your brand voice in 3-5 adjectives (e.g., bold, technical, witty) | `voice/brand-voice.md` |
| Any words or phrases you always/never use? | `voice/brand-voice.md` → vocabulary |
| Which platforms do you actively use? (multi-select: X, LinkedIn, Instagram, TikTok, YouTube, Threads, Facebook, Newsletter) | `platforms/*.md` file creation |

**Batch 3 — Content Strategy**

Ask the user:

| Question | Maps to |
|----------|---------|
| What content types do you create? (e.g., tutorials, hot takes, case studies, threads) | `engine/content-types.md` |
| What is your primary content goal? (awareness / engagement / conversion / education) | `engine/goals.md` |
| How often do you publish? (daily / 3x week / weekly) | `engine/schedule.md` |

### Phase 3: Directory Scaffolding

Create the full directory structure:

```
content-skill-graph/
├── index.md                    # Brand identity hub
├── platforms/
│   ├── x.md                    # Twitter/X rules
│   ├── linkedin.md             # LinkedIn rules
│   ├── instagram.md            # Instagram rules
│   ├── tiktok.md               # TikTok rules
│   ├── youtube.md              # YouTube rules
│   ├── threads.md              # Threads rules
│   ├── facebook.md             # Facebook rules
│   └── newsletter.md           # Newsletter rules
├── voice/
│   ├── brand-voice.md          # Voice DNA
│   └── platform-tone.md        # Per-platform tone map
├── engine/
│   ├── repurpose.md            # Repurposing chain
│   ├── hooks.md                # Hook formulas
│   ├── content-types.md        # Content type catalog
│   ├── goals.md                # Content goals
│   └── schedule.md             # Publishing cadence
└── audience/
    ├── segments.md             # Audience segments
    └── pain-points.md          # Pain points catalog
```

Only create platform files for platforms the user selected in Batch 2. Skip unselected platforms.

### Phase 4: File Population

Populate each file using wizard responses. Every file must:

1. Start with an H1 heading matching the file's purpose
2. Include `[[wikilinks]]` to related nodes (minimum 2 per file)
3. Contain substantive content — not stubs

**File templates:**

**`index.md`**
```markdown
# {Brand Name} Content Skill Graph

## Identity
- **Niche**: {niche}
- **Mission**: {mission}
- **Voice**: See [[voice/brand-voice]]

## Quick Links
- [[audience/segments]] — Who we talk to
- [[voice/brand-voice]] — How we sound
- [[engine/repurpose]] — How we distribute
- [[engine/content-types]] — What we create

## Active Platforms
{list of selected platforms with [[platform links]]}
```

**`platforms/{platform}.md`** (generate per platform with platform-specific defaults)
```markdown
# {Platform Name}

## Format Rules
- **Character limit**: {platform-specific}
- **Best content types**: {platform-specific}
- **Posting frequency**: {from schedule}
- **Tone**: See [[voice/platform-tone]]

## Platform-Specific Guidelines
{Pre-populated with known best practices for each platform}

## Hook Style
See [[engine/hooks]] for platform-adapted hooks.

## Audience on This Platform
See [[audience/segments]] for segment behavior on {platform}.
```

**`voice/brand-voice.md`**
```markdown
# Brand Voice

## Voice DNA
- **Adjectives**: {from wizard}
- **Always use**: {from wizard}
- **Never use**: {from wizard}

## Voice Principles
{Generate 3-5 principles from the adjectives}

## Application
Apply this voice across all [[platforms/]] with tone adaptations per [[voice/platform-tone]].
```

**`voice/platform-tone.md`**
```markdown
# Platform Tone Map

| Platform | Tone Shift | Example |
|----------|-----------|---------|
{For each selected platform, describe how voice adapts}

Base voice: [[voice/brand-voice]]
```

**`engine/repurpose.md`**
```markdown
# Repurposing Chain

## Order
1. **Seed**: Long-form or core idea
2. **X/Twitter**: Distill to punchy thread
3. **LinkedIn**: Reframe for professional insight
4. **Newsletter**: Expand with depth
5. **Instagram**: Visual + caption
6. **TikTok/YouTube Shorts**: Script for video
7. **Threads/Facebook**: Community version

## Rules
- Never copy-paste between platforms
- Each version must be "platform-native" — rethought, not reformatted
- See [[voice/platform-tone]] for tone shifts per platform
- Reference [[audience/segments]] for platform-specific targeting
```

**`engine/hooks.md`**
```markdown
# Hook Formulas

## Universal Hooks
1. **Curiosity Gap**: "Most people think X. They're wrong."
2. **Contrarian Claim**: "Unpopular opinion: {statement}"
3. **Data Shock**: "{Surprising stat} — here's why it matters"
4. **Story Open**: "Last week I {experience} and learned..."
5. **Direct Challenge**: "Stop doing X. Start doing Y."

## Platform Adaptations
{Per-platform hook style notes, linking to [[platforms/*]]}
```

**`engine/content-types.md`**
```markdown
# Content Types

{For each type the user listed}
## {Type Name}
- **Purpose**: {inferred from type}
- **Best platforms**: {matched to selected platforms}
- **Structure**: {template structure}
- **Frequency**: See [[engine/schedule]]
```

**`engine/goals.md`**
```markdown
# Content Goals

## Primary Goal
{from wizard}

## Goal-to-Content Mapping
| Goal | Content Types | Platforms | Metrics |
|------|--------------|-----------|---------|
{Map the primary goal to content types and platforms}

## Alignment
All content must serve [[engine/goals]] while maintaining [[voice/brand-voice]].
```

**`engine/schedule.md`**
```markdown
# Publishing Schedule

## Cadence
{from wizard: daily / 3x week / weekly}

## Platform Schedule
| Day | Platform | Content Type |
|-----|----------|-------------|
{Generate a reasonable schedule based on cadence and selected platforms}

## Rules
- Repurpose chain order: [[engine/repurpose]]
- Content types: [[engine/content-types]]
```

**`audience/segments.md`**
```markdown
# Audience Segments

## Primary Segment
- **Who**: {from wizard}
- **Where they hang out**: {matched to selected platforms}
- **What they care about**: {inferred from pain points}

## Pain Points
See [[audience/pain-points]] for detailed pain point catalog.

## Platform Behavior
{Per-platform audience behavior notes}
```

**`audience/pain-points.md`**
```markdown
# Audience Pain Points

{For each pain point from wizard}
## {Pain Point}
- **Severity**: {High/Medium/Low — inferred}
- **Content angle**: {How to address this in content}
- **Best format**: {Which content types work best}
- **Relevant platforms**: {Which platforms reach people with this pain}

## Connection
These pain points drive [[engine/content-types]] and [[engine/goals]].
```

### Phase 5: Wikilink Validation

After all files are written:

1. Scan every `.md` file for `[[wikilink]]` patterns
2. For each wikilink, verify the target file exists in the directory
3. Report any broken links
4. If broken links found, fix them (create missing files or correct paths)
5. Count total nodes, total links, and average links per node

### Phase 6: Summary Report

Present a summary to the user:

```
✅ Content Skill Graph Created

📁 Directory: content-skill-graph/
📄 Files created: {count}
🔗 Wikilinks: {total links} across {node count} nodes
📊 Average links/node: {average}
🎯 Platforms configured: {list}

Next steps:
1. Run content-graph-voice to calibrate your brand voice with real samples
2. Run content-graph-produce to generate your first content batch
```

## Verification

Before reporting complete:

1. Confirm `content-skill-graph/` directory exists with expected file count
2. Confirm every file has an H1 heading and at least 2 wikilinks
3. Confirm no broken wikilinks remain
4. Confirm no placeholder text ("[TBD]", "[Insert here]", etc.)

```
VERDICT: PASS — All {N} files created, {L} wikilinks validated, 0 broken links
```

## Error Recovery

| Error | Recovery |
|-------|----------|
| User aborts wizard mid-way | Save partial responses, offer to resume |
| Directory already exists | Ask before overwrite; offer merge mode |
| Wikilink target missing | Auto-create minimal stub file with TODO marker |
