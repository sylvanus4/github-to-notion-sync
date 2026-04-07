---
name: content-repurposing-engine
description: >-
  Transform long-form content (articles, reports, papers, docs, transcripts)
  into platform-specific formats: Twitter threads, LinkedIn posts, newsletter
  sections, blog summaries, video script outlines, infographic briefs, and
  email snippets. Preserves core message while adapting tone, length, and
  structure per platform. Use when the user asks to "repurpose this content",
  "turn this article into tweets", "make a LinkedIn post from this report",
  "content repurposing", "콘텐츠 재활용", "리퍼포징", "글 변환", "다채널
  콘텐츠", "multi-platform content", "adapt for social media", or wants to
  extract multiple content pieces from a single source. Do NOT use for podcast
  episode repurposing (use marketing-podcast-ops). Do NOT use for brand voice
  enforcement (use kwp-brand-voice-brand-voice-enforcement). Do NOT use for
  slide creation (use anthropic-pptx). Do NOT use for full document rewriting
  (use prompt-transformer).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "generation"
---

# Content Repurposing Engine

Transform one piece of long-form content into multiple platform-optimized formats without losing the core message.

## When to Use

- An article, report, paper, or transcript needs to reach audiences across multiple platforms
- The user has written a detailed analysis and wants social media distribution
- A long document needs a short-form summary for different channels
- Content marketing requires one-to-many content transformation

## Workflow

### Step 1: Ingest Source Content

Accept the source content in any of these forms:
- Markdown file path (read and parse)
- Pasted text
- URL (extract via defuddle)
- Notion page URL (fetch via Notion MCP)

Extract these elements from the source:

| Element | Description |
|---------|-------------|
| **Core thesis** | The single main argument or insight (1 sentence) |
| **Key points** | 3-7 supporting points with evidence |
| **Data/stats** | Quantitative claims with sources |
| **Quotes** | Memorable phrases or expert quotes |
| **Narrative arc** | The story structure (problem → insight → implication) |
| **Target audience** | Who the original content was written for |

### Step 2: Select Target Platforms

Ask the user which platforms to target, or default to all:

| Platform | Format | Constraints |
|----------|--------|-------------|
| **Twitter/X Thread** | 5-15 tweets, 280 chars each | Hook in tweet 1, CTA in final tweet |
| **LinkedIn Post** | 1,300 chars max, professional tone | Hook line, blank line, value, CTA |
| **Newsletter Section** | 200-400 words, scannable | Subject line + preview text + body |
| **Blog Summary** | 300-600 words, SEO-friendly | H2 headings, meta description, keywords |
| **Video Script Outline** | 60-180 second script skeleton | Hook, 3 key points, CTA |
| **Infographic Brief** | Structured data for visual design | Title, 5-7 data points, flow/hierarchy |
| **Email Snippet** | 100-200 words, action-oriented | Subject line, 1 key insight, CTA |
| **Slack Summary** | 3-5 bullet points | TL;DR format for internal sharing |

### Step 3: Transform per Platform

For each selected platform, apply these transformation rules:

**Tone Adaptation**
| Platform | Tone | Person |
|----------|------|--------|
| Twitter | Punchy, conversational, contrarian | 1st or 2nd person |
| LinkedIn | Professional, insightful, humble-expert | 1st person |
| Newsletter | Warm, informative, trusted-advisor | 2nd person |
| Blog | Clear, authoritative, SEO-conscious | 3rd person |
| Video Script | Energetic, visual, direct | 2nd person |
| Email | Personal, concise, action-driven | 2nd person |

**Content Density**
| Platform | Words | Key Points |
|----------|-------|------------|
| Twitter thread | 1,000-2,000 total | All points, one per tweet |
| LinkedIn | 200-300 | Top 2-3 points |
| Newsletter | 200-400 | Top 3 points + context |
| Blog summary | 300-600 | All points, compressed |
| Video script | 150-400 | Top 3 points + hook |
| Email | 100-200 | Top 1 point + CTA |

### Step 4: Quality Checks

Before outputting, verify each piece against:

- [ ] Core thesis is preserved (not diluted or distorted)
- [ ] Platform constraints are met (character limits, formatting rules)
- [ ] No data or claims are unsupported by the source
- [ ] Tone matches the platform's convention
- [ ] Each piece can stand alone — a reader shouldn't need the source to understand it
- [ ] CTA or next-step is included where appropriate

### Step 5: Output

Return all transformed pieces in a single structured output:

```markdown
# Content Repurposing: [Source Title]

## Source Summary
- **Core thesis**: [1 sentence]
- **Key points**: [numbered list]
- **Source**: [file path or URL]

---

## Twitter/X Thread

**Tweet 1 (Hook)**:
[text]

**Tweet 2**:
[text]

...

**Tweet N (CTA)**:
[text]

---

## LinkedIn Post

[full post text]

---

## Newsletter Section

**Subject Line**: [subject]
**Preview Text**: [preview]

[body]

---

## [Additional platforms...]

---

## Repurposing Notes
- [Any adaptations, omissions, or creative liberties taken]
- [Data points that couldn't be verified and were excluded]
```

## Examples

### Example 1: Technical report to social media

User: "이 분석 리포트를 Twitter thread랑 LinkedIn 포스트로 만들어줘" + [report path]

Read the report, extract core thesis ("AI agent costs are dropping 10x/year"), key data points, and transform into a 10-tweet thread with data visualizations described and a LinkedIn post with professional framing.

### Example 2: Meeting notes to newsletter

User: "Turn these meeting notes into a newsletter section for the team"

Extract decisions, action items, and key insights from the meeting notes. Write a 300-word newsletter section with a subject line that highlights the most impactful decision.

### Example 3: Research paper to multi-platform

User: "Repurpose this paper review across all platforms"

Generate all 8 platform formats from the paper review, emphasizing different aspects per platform (Twitter: surprising findings, LinkedIn: industry implications, Blog: methodology breakdown, Email: one actionable takeaway).

## Error Handling

| Scenario | Action |
|----------|--------|
| Source content is too short (<200 words) | Warn that repurposing may produce repetitive content; suggest expanding the source first |
| Source has no clear thesis | Ask: "What's the main takeaway you want to communicate?" |
| User requests a platform not in the list | Generate content following the platform's known conventions, or ask for format details |
| Source contains sensitive/internal data | Flag and ask whether to redact before generating public-facing content |
| Multiple conflicting theses in source | Ask the user to select the primary thesis, or generate separate repurposing sets per thesis |

## Composability

- **reclip-media-downloader** — Download source video/audio from URLs for transcription-based repurposing
- **scqa-writing-framework** — Structure the source content before repurposing
- **hook-generator** — Generate stronger hooks for each platform
- **sentence-polisher** — Polish each output before publishing
- **kwp-brand-voice-brand-voice-enforcement** — Apply brand voice to all outputs
- **md-to-slack-canvas** — Publish the Slack summary as a Canvas
- **md-to-notion** — Archive the repurposed content set in Notion
- **agent-reach** — Fallback content extractor when defuddle/WebFetch fails on source URLs (403, paywall, anti-bot). Use agent-reach URL-pattern routing to access the content via the appropriate channel.
