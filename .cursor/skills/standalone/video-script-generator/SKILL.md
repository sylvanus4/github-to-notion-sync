---
name: video-script-generator
description: >-
  Generate structured video scripts with hooks, content sections, pacing marks,
  B-roll cues, and CTAs — optimized for YouTube, YouTube Shorts, TikTok,
  Instagram Reels, and educational content. Includes timing estimates, visual
  direction notes, and platform-specific formatting. Use when the user asks to
  "write a video script", "YouTube script", "Shorts script", "TikTok script",
  "Reels script", "video content", "영상 스크립트", "유튜브 대본", "숏폼
  스크립트", "비디오 대본", "영상 기획", or wants a ready-to-film script for
  any video platform. Do NOT use for presentation slide scripts (use
  presentation-strategist). Do NOT use for NLM video narration (use nlm-video).
  Do NOT use for podcast-to-Shorts conversion (use marketing-podcast-ops). Do
  NOT use for stock content multi-channel drafts (use stock-content-printer). Do
  NOT use for video editing/post-production plans (use video-editing-planner).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "generation"
---

# Video Script Generator

Create platform-optimized video scripts with hooks, pacing, visual cues, and CTAs — ready for production.

## When to Use

- Creating a YouTube video from a topic, outline, or existing content
- Writing short-form scripts (Shorts, TikTok, Reels) with tight timing
- Generating educational or explainer video scripts
- Adapting written content (article, report, paper) into video format
- Planning a video series with consistent structure

## Workflow

### Step 1: Gather Brief

Collect from the user:

| Input | Description | Required |
|-------|-------------|----------|
| **Topic** | What the video is about | Yes |
| **Platform** | YouTube, Shorts, TikTok, Reels, Educational, Custom | Yes |
| **Duration** | Target length in seconds or minutes | Yes |
| **Audience** | Who watches this (developers, investors, general, etc.) | Yes |
| **Tone** | Educational, entertaining, motivational, analytical | No (inferred) |
| **Source material** | Existing content to adapt | No |
| **Speaker** | On-camera, voiceover, or text-on-screen | No (default: voiceover) |

### Step 2: Platform Format Selection

| Platform | Duration | Structure | Key Rules |
|----------|----------|-----------|-----------|
| **YouTube** | 8-15 min | Hook → Intro → 3-5 Sections → CTA → Outro | First 30s = retention gate |
| **YouTube Shorts** | 30-60s | Hook → 1 Point → Payoff | Hook in first 2s, vertical framing |
| **TikTok** | 15-60s | Hook → Build → Reveal | Pattern interrupt in first 1s, loop-friendly ending |
| **Instagram Reels** | 15-90s | Hook → Value → CTA | Visual-first, text overlay cues |
| **Educational** | 5-20 min | Empowerment Promise → Problem → Explanation → Example → Contribution Summary | Pacing marks every 2-3 min; open with what the viewer will gain (Winston), close with what was shown |
| **Custom** | Any | User-defined | Follow user specs |

### Step 3: Script Generation

Generate the script with these components for each section:

```
## [Section Name] — [Start Time] to [End Time] (~[Duration]s)

### Script (what the speaker says)
[Exact spoken words. Write conversationally — how people talk, not how they write.]

### Visual Direction
[What appears on screen: B-roll description, text overlays, graphics, transitions]

### Pacing Notes
[Speed: fast/medium/slow. Energy: high/building/calm. Pauses: where and why.]
```

**Hook Construction (mandatory first section):**

| Platform | Hook Window | Hook Pattern |
|----------|------------|--------------|
| YouTube | 0-30s | Empowerment Promise ("By the end of this video, you'll…") → Surprising stat → Preview of value (Winston: state what the audience gains) |
| Shorts | 0-2s | Visual pattern interrupt → Bold claim |
| TikTok | 0-1s | "Stop scrolling" move → Immediate curiosity gap |
| Reels | 0-3s | Visual hook → Text overlay statement |
| Educational | 0-15s | Empowerment Promise → Real-world problem → "By the end of this video, you'll…" (Winston: the audience must know what they gain within the first 15 seconds) |

### Step 4: Timing Validation

Calculate total script duration using:
- Speaking pace: ~150 words/minute for normal, ~130 for educational, ~170 for energetic
- Add time for: visual-only segments, pauses, transitions, B-roll inserts

Verify total fits within the target duration ±10%. Adjust if needed.

### Step 5: Output

```markdown
# Video Script: [Title]

## Metadata
- **Platform**: [platform]
- **Target Duration**: [duration]
- **Estimated Duration**: [calculated duration]
- **Word Count**: [total spoken words]
- **Audience**: [audience]
- **Tone**: [tone]

---

## Section 1: Hook — 0:00 to 0:30 (~30s)

### Script
[spoken words]

### Visual Direction
[what appears on screen]

### Pacing Notes
[speed, energy, pauses]

---

## Section 2: [Topic] — 0:30 to 2:00 (~90s)

### Script
[spoken words]

### Visual Direction
[what appears on screen]

### Pacing Notes
[speed, energy, pauses]

---

## [Additional sections...]

---

## Winston Narrative Threading (Educational / YouTube ≥ 5 min)
- **Circle & Star**: The core message must appear ≥ 3 times — Hook (promise), midpoint (reinforce), and closing (restate). Mark the single most critical moment as ★ Star.
- **Near Miss**: When explaining a concept, include a "This is X, but NOT Y" example to sharpen understanding.
- **Contribution Ending**: Close by stating what the viewer has learned or can now do — not just "thanks for watching."

---

## Section N: CTA & Outro — [time] to [end]

### Script
[spoken words — include specific CTA: subscribe, link, comment prompt; state what was shown (Winston Contribution Ending)]

### Visual Direction
[end screen elements, subscribe animation, link overlay]

---

## Production Notes
- **B-roll needed**: [list of B-roll shots to capture or source]
- **Graphics needed**: [list of custom graphics, charts, or animations]
- **Music suggestions**: [mood/genre for background music]
- **Thumbnail concept**: [1-sentence thumbnail idea]
```

## Examples

### Example 1: YouTube explainer

User: "Write a 10-minute YouTube script about why AI agents will replace SaaS"

Generate: Hook (surprising stat about SaaS disruption) → Context (current SaaS landscape) → 3 Reasons (with evidence per reason) → Counterarguments → Prediction → CTA (subscribe + comment). Include B-roll cues for each section (screen recordings, comparison graphics, talking head transitions).

### Example 2: TikTok short

User: "TikTok script about the 3-second rule in presentations"

Generate: 0-1s visual hook (dramatic slide transition) → 1-5s bold claim ("Most presentations lose the audience in 3 seconds") → 5-40s three rapid-fire tips with text overlays → 40-50s before/after example → 50-55s CTA. Total: ~55 seconds.

### Example 3: Educational series

User: "영상 스크립트 시리즈: Python 기초 3편 - 리스트와 딕셔너리"

Generate: Hook (real-world problem solved by lists) → Concept intro → Live coding walkthrough with pause marks → Common mistakes section → Practice exercise prompt → Next episode teaser. Include screen recording cues and code overlay specifications.

## Error Handling

| Scenario | Action |
|----------|--------|
| No platform specified | Ask: "Which platform is this for? (YouTube, Shorts, TikTok, Reels, Educational)" |
| Duration unrealistic for content depth | Warn: "[Topic] needs ~[N] minutes to cover properly. Adjust scope or duration?" |
| Source material is too thin for target duration | Suggest additional angles, examples, or segments to fill the time |
| User wants multiple platforms from one topic | Generate separate scripts per platform, each optimized for its format |
| Script exceeds target duration by >20% | Cut the lowest-impact section and note what was removed |
| Educational script lacks Circle & Star | Add core message callbacks at Hook, midpoint, and closing (Winston: repeat to build understanding) |
| Concept explanation is abstract | Add a Near Miss example: "This is X, but NOT Y" to sharpen the distinction (Winston) |

## Composability

- **hook-generator** — Generate alternative hooks to A/B test
- **content-repurposing-engine** — Source content for script adaptation
- **video-editing-planner** — Hand off the script for post-production planning
- **caption-subtitle-formatter** — Generate subtitles from the final script
- **anthropic-pptx** — Create supporting slides for educational videos
- **presentation-strategist** — Design the narrative arc before scripting
- **winston-speaking-coach** — Run a full Winston coaching session to refine the script's Empowerment Promise, Circle & Star threading, and Near Miss examples before recording

## Winston Framework Integration

Video scripts for Educational and YouTube (≥ 5 min) formats incorporate Patrick Winston's "How to Speak" principles:

| Principle | Application |
|-----------|-------------|
| **Empowerment Promise** | Hook section opens with what the viewer will gain |
| **Circle & Star** | Core message repeated ≥ 3 times (hook, midpoint, closing); one ★ Star moment marked |
| **Near Miss** | Concept explanations include "X but not Y" contrasts |
| **Contribution Ending** | CTA/Outro states what was shown — not just "thanks for watching" |
| **Storytelling → Analytical Thinking** | Educational scripts follow observation → hypothesis → test → learning |

For short-form (Shorts, TikTok, Reels ≤ 60s), only the Empowerment Promise is applied due to time constraints.
