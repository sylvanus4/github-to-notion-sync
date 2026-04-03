---
name: hook-generator
description: >-
  Generate attention-grabbing hooks for multiple contexts: video intros (first
  1-3 seconds), social media posts, email subject lines, ad copy, article
  openings, presentation openers, and Slack announcements. Uses proven hook
  frameworks (curiosity gap, contrarian claim, data shock, story open, direct
  challenge) with platform-specific formatting. Use when the user asks to
  "generate hooks", "write a hook", "opening line", "attention grabber", "email
  subject line", "video intro", "후킹 문구", "첫 문장", "관심 끄는 문구",
  "오프닝 훅", "hook me", "catchy opener", "click-worthy headline", or wants
  the first line of any content to stop the scroll. Do NOT use for full
  presentation design (use presentation-strategist). Do NOT use for copywriting
  beyond hooks (use kwp-marketing-content-creation). Do NOT use for email body
  drafting (use gws-email-reply). Do NOT use for full video scripts (use
  video-script-generator). Do NOT use for brand voice enforcement (use
  kwp-brand-voice-brand-voice-enforcement).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "generation"
---

# Hook Generator

Generate platform-optimized attention hooks using proven psychological frameworks.

## When to Use

- Writing the first line of any content and need it to grab attention
- A/B testing subject lines, headlines, or video intros
- Social media posts need stronger opening lines
- Video content needs a scroll-stopping first 1-3 seconds
- Email campaigns need higher open rates via better subject lines
- Presentation needs a memorable opening

## Workflow

### Step 1: Gather Context

| Input | Description | Required |
|-------|-------------|----------|
| **Topic/Content** | What the hook is for | Yes |
| **Context** | Video intro, email subject, social post, article, ad, presentation, Slack | Yes |
| **Audience** | Who should be hooked (developers, executives, consumers, etc.) | Yes |
| **Desired emotion** | Curiosity, urgency, surprise, fear, excitement, authority | No (default: curiosity) |
| **Quantity** | How many hook variants to generate | No (default: 5) |

### Step 2: Select Hook Frameworks

Apply frameworks based on context and audience:

| Framework | Pattern | Best For |
|-----------|---------|----------|
| **Curiosity Gap** | "X happened, but nobody noticed Y" | Articles, videos, social |
| **Contrarian Claim** | "Everything you know about X is wrong" | Thought leadership, LinkedIn |
| **Data Shock** | "[Surprising stat] — and here's why it matters" | Business, tech, finance |
| **Story Open** | "Last Tuesday, I [specific moment]..." | Personal brand, newsletters |
| **Direct Challenge** | "You're probably making this mistake right now" | Educational, how-to |
| **Question Hook** | "What if [provocative scenario]?" | Videos, presentations |
| **Social Proof** | "[Authority/many people] discovered that..." | Sales, landing pages |
| **Benefit Lead** | "Here's how to [desirable outcome] in [time]" | How-to, tutorials |
| **Controversy** | "[Popular thing] is actually [opposite view]" | Social media, debates |
| **Scarcity/Urgency** | "Before [deadline/event], you need to know..." | Emails, ads, CTAs |

### Step 3: Generate Variants

For each hook, produce:

```markdown
### Hook [N] — [Framework Name]

**Hook**: [The actual hook text]
**Why it works**: [1-sentence explanation of the psychological mechanism]
**Best for**: [specific platform/context where this works best]
**Risk level**: Low / Medium / High (how polarizing or bold the claim is)
```

Generate the requested number of variants (default: 5), using at least 3 different frameworks.

### Step 4: Platform Formatting

Adapt hooks to platform constraints:

| Platform | Constraint | Formatting |
|----------|-----------|------------|
| **Video (YouTube)** | First 5-10 words on screen + spoken | Hook + immediate visual/text overlay |
| **Shorts/TikTok/Reels** | First 1-2 seconds | Text overlay hook + visual pattern interrupt |
| **Twitter/X** | First line before "Show more" (~40 chars) | Punchy, no fluff, emoji optional |
| **LinkedIn** | First 2 lines before "...see more" (~150 chars) | Professional curiosity gap |
| **Email Subject** | 40-60 chars, preview text support | Subject + preview text pair |
| **Article/Blog** | First paragraph / H1 | SEO-conscious, keyword-forward |
| **Presentation** | Single slide, spoken + displayed | Bold statement or question |
| **Ad Copy** | Headline + subhead | Benefit-forward, action-oriented |
| **Slack** | First line of message | Direct, scannable, emoji optional |

### Step 5: Output

```markdown
# Hooks for: [Topic]

**Context**: [platform/format]
**Audience**: [target audience]
**Frameworks used**: [list]

---

## Hook 1 — Curiosity Gap
**Hook**: [text]
**Why it works**: [explanation]
**Best for**: [platform]
**Risk**: Low

## Hook 2 — Data Shock
**Hook**: [text]
**Why it works**: [explanation]
**Best for**: [platform]
**Risk**: Medium

## Hook 3 — Contrarian Claim
**Hook**: [text]
**Why it works**: [explanation]
**Best for**: [platform]
**Risk**: High

## Hook 4 — [Framework]
...

## Hook 5 — [Framework]
...

---

## Recommendation
**Top pick**: Hook [N] — [reasoning based on audience and context]
**A/B test pair**: Hook [X] vs Hook [Y] — [why these are good to test against each other]
```

## Examples

### Example 1: YouTube video hooks

User: "Generate hooks for a YouTube video about why most startups fail at pricing"

**Hook 1 — Data Shock**: "82% of startups that fail cite 'pricing' as a top-3 reason. But it's not what you think."
**Hook 2 — Contrarian**: "The best pricing strategy? Don't have one. Here's why."
**Hook 3 — Story Open**: "We lost our biggest customer last month. Not because of our product — because of a $5/month price difference."

### Example 2: Email subject lines

User: "5 email subject lines for a SaaS product launch announcement"

**1 — Curiosity Gap**: "We just changed everything (and broke nothing)"
**2 — Benefit Lead**: "Ship 3x faster starting today"
**3 — Social Proof**: "[Company] just switched — here's why"
**4 — Scarcity**: "Early access ends Friday"
**5 — Question**: "What if your CI pipeline took 30 seconds?"

### Example 3: LinkedIn post hook

User: "LinkedIn 포스트 훅 만들어줘 - AI 에이전트가 주니어 개발자를 대체한다는 주제"

**Hook 1 — Contrarian**: "AI won't replace junior developers. It'll replace the seniors who refuse to use it."
**Hook 2 — Question**: "If an AI agent can write, test, and deploy code — what's left for a junior dev to learn?"
**Hook 3 — Data Shock**: "Junior developer job postings dropped 34% this year. But hiring for 'AI-augmented developers' tripled."

## Error Handling

| Scenario | Action |
|----------|--------|
| No topic provided | Ask: "What's the topic or content you need hooks for?" |
| No context/platform specified | Ask: "Where will this hook appear? (video, email, social, article, presentation)" |
| Topic is too generic | Ask for a specific angle or claim within the topic |
| User wants hooks in a specific language | Generate in the requested language; default to the topic's language |
| All generated hooks feel too similar | Apply at least 4 different frameworks and vary sentence structure |

## Composability

- **video-script-generator** — Use the winning hook as the video's opening
- **content-repurposing-engine** — Generate platform-specific hooks for repurposed content
- **scqa-writing-framework** — Use the hook as the Complication or Question element
- **presentation-strategist** — Use a hook as the opening slide concept
- **kwp-marketing-content-creation** — Pair hooks with full marketing copy
- **sentence-polisher** — Polish the final selected hook
