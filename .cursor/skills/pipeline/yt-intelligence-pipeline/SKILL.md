---
name: yt-intelligence-pipeline
description: >-
  Parallel YouTube intelligence pipeline orchestrator: extract transcript via
  defuddle, generate detailed Korean analysis (3000-5000 words), then fan out
  3 parallel subagents for dual-audience NLM slides (expert + elementary),
  Notion publishing, and multi-platform content repurposing simultaneously,
  with consolidated 3-message Slack thread distribution. Requires Slack MCP,
  NotebookLM MCP, Notion MCP, and gws CLI. Outputs persist to
  outputs/yt-intel/{date}/{slug}/. Use when the user asks to "analyze YouTube
  video", "YouTube intelligence", "유튜브 분석 파이프라인", "유튜브 정리",
  "YouTube pipeline", "yt-intel", or wants comprehensive YouTube video
  analysis with slides + Notion + Slack delivery.
  Do NOT use for simple transcript extraction only (use defuddle).
  Do NOT use for slides-only without full pipeline (use nlm-dual-slides).
  Do NOT use for Notion upload only (use md-to-notion).
  Do NOT use for an existing analysis markdown that just needs slides and
  Slack (invoke nlm-dual-slides and Slack MCP directly).
tags:
  - pipeline
  - youtube
  - parallel
  - intelligence
  - slides
  - notion
  - slack
triggers:
  - "analyze YouTube video"
  - "YouTube intelligence"
  - "YouTube pipeline"
  - "yt-intel"
  - "유튜브 분석"
  - "유튜브 정리"
  - "유튜브 파이프라인"
  - "유튜브 인텔리전스"
---

# YouTube Intelligence Pipeline

## Role

You are a **pipeline orchestrator** that takes a YouTube URL, extracts the transcript, generates a detailed Korean analysis, dispatches 3 parallel subagents (slides, Notion, repurposing), and delivers a consolidated intelligence thread to Slack.

## Overview

End-to-end pipeline that takes a YouTube URL (and optional user context), extracts the transcript, generates a detailed Korean analysis, then fans out 3 parallel agents for slide generation, Notion publishing, and content repurposing -- finishing with a consolidated Slack thread.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| YouTube URL | Yes | Any `youtube.com` or `youtu.be` link |
| User context | No | Bullet points, notes, or supplementary information to merge with transcript |
| Slack channel | No | Defaults to `#deep-research-trending` (`C0AN34G4QHK`) |
| Output slug | No | Directory name for outputs; auto-derived from video title if omitted |

## Output Artifacts

| Artifact | Path | Description |
|----------|------|-------------|
| Transcript | `outputs/yt-intel/{date}/{slug}/transcript.md` | Raw defuddle transcript with timestamps |
| Full analysis | `outputs/yt-intel/{date}/{slug}/analysis.md` | Detailed Korean analysis (3000-5000 words) |
| Executive summary | `outputs/yt-intel/{date}/{slug}/summary.md` | Compressed bullet brief (~500 words) |
| Repurposed content | `outputs/yt-intel/{date}/{slug}/repurposed.md` | Twitter thread, LinkedIn post, newsletter |
| Expert slides | `outputs/presentations/{slug}-Expert-{date}.pdf` | Expert-level NLM slide deck |
| Elementary slides | `outputs/presentations/{slug}-Elementary-{date}.pdf` | Elementary-level NLM slide deck |
| Notion pages | (online) | Analysis + summary sub-pages |
| Slack thread | (online) | 3-message intelligence thread |

## Architecture

```
Phase 1 (Sequential) ─── Phase 2 (Sequential) ─── Phase 3 (Parallel) ─── Phase 4 (Sequential)
    Extract                    Analyze                  Fan-Out                 Distribute

  YouTube URL           Merge transcript            ┌─ Agent A: nlm-dual-slides
      │                 + user context              │
      ▼                      │                      │─ Agent B: md-to-notion        ──▶ Slack
   defuddle ──▶ transcript ──▶ LLM analysis ──────┤                                   Thread
                              │                     │─ Agent C: content-repurposing
                              ▼                     └
                    long-form-compressor
                     (executive summary)
```

---

## Phase 1: Transcript Extraction

**Skill:** `defuddle`

1. Call `curl -s "https://defuddle.md/{youtube_url_without_protocol}"` to extract the transcript
2. Parse the returned markdown: YAML frontmatter (title, author, channel) + timestamped transcript body
3. Save to `outputs/yt-intel/{date}/{slug}/transcript.md`
4. Extract the video title for use as the slug (if not provided)

**Failure mode:** If defuddle returns empty or error, fall back to `WebFetch` on the YouTube URL and extract available metadata.

---

## Phase 2: Deep Analysis

### Step 2a: Merge Sources

Combine the transcript from Phase 1 with any user-supplied context into a single source document. Place user context under a `## User-Supplied Context` heading.

### Step 2b: Generate Detailed Korean Analysis

Using the system prompt from `references/analysis-prompt.md`, generate a comprehensive Korean analysis markdown (~3000-5000 words) covering:

- **Video Summary:** Key claims and evidence from the video
- **Technical Deep-Dive:** Architecture, algorithms, implementation details
- **Market & Industry Implications:** Business impact, competitive dynamics
- **Counter-Arguments (Karpathy Opposite Direction Test):** Limitations, risks, alternative interpretations
- **Actionable Takeaways:** Concrete next steps for investors, engineers, and decision-makers

Save to `outputs/yt-intel/{date}/{slug}/analysis.md`

### Step 2c: Compress to Executive Summary

Invoke `long-form-compressor` skill concepts: compress the analysis to a ~500-word bullet brief with the 5 most critical points. Save to `outputs/yt-intel/{date}/{slug}/summary.md`

---

## Phase 3: Parallel Fan-Out (3 Subagents)

Launch 3 independent subagents via the Task tool simultaneously. Each receives the analysis markdown as input.

### Agent A: Slide Generation (nlm-dual-slides pattern)

1. Split analysis by `##` section headings
2. Rewrite each section into Expert (EN+KO) and Elementary (EN+KO) versions
3. Create 2 NotebookLM notebooks, upload source sections, generate slide decks
4. Download PDFs to `outputs/presentations/{slug}-Expert-{date}.pdf` and `outputs/presentations/{slug}-Elementary-{date}.pdf`
5. Upload both to Google Drive via `gws drive +upload`
6. **Return:** Expert Drive URL, Elementary Drive URL, local PDF paths

### Agent B: Notion Publishing (md-to-notion)

1. Read the analysis markdown
2. Convert pipe tables to Notion-compatible HTML tables
3. Create a Notion sub-page (under default parent) with the full analysis
4. Create a second sub-page with the executive summary
5. **Return:** Notion page URL, page title

### Agent C: Content Repurposing (content-repurposing-engine)

1. Read the analysis markdown
2. Generate platform-specific content:
   - Twitter thread (5-7 tweets with hooks)
   - LinkedIn post (professional tone, 1300 chars)
   - Newsletter section (email-ready paragraph)
3. Save to `outputs/yt-intel/{date}/{slug}/repurposed.md`
4. **Return:** File path, content preview (first tweet + LinkedIn opener)

---

## Phase 4: Slack Distribution

**Channel:** `#deep-research-trending` (ID: `C0AN34G4QHK`)

Post a 3-message Korean intelligence thread using templates from `references/message-templates.md`.

### Message 1 (Main Post)
- Video title + YouTube link
- Korean executive summary (3-5 bullets from Phase 2c)
- Links: Notion page, Expert slides (Drive), Elementary slides (Drive)

### Message 2 (Thread Reply - Detailed Analysis)
- Key technical findings (3-4 sections)
- Market implications
- Counter-arguments and limitations

### Message 3 (Thread Reply - Content Kit)
- Twitter thread draft
- LinkedIn post draft
- Repurposing notes

Use `slack_send_message` MCP tool with `message` parameter. Post Message 1 first, then use `thread_ts` from the response for Messages 2 and 3.

---

## Error Handling

| Phase | Failure | Recovery |
|-------|---------|----------|
| 1 | defuddle returns empty | Retry once; if still empty, use WebFetch + manual transcript extraction |
| 2 | LLM analysis too short (<1000 words) | Re-run with explicit length instruction |
| 3A | NLM slide generation fails | Skip slides, note in Slack thread; proceed with other agents |
| 3B | Notion API error | Save analysis locally; post file path in Slack instead of Notion link |
| 3C | Repurposing produces empty | Generate minimal Twitter thread from executive summary |
| 4 | Slack post fails | Retry with simplified mrkdwn; if persistent, save thread content to local file |

---

## Skill Dependencies

| Skill | Phase | Role |
|-------|-------|------|
| `defuddle` | 1 | YouTube transcript extraction |
| `long-form-compressor` | 2c | Analysis compression to executive summary |
| `nlm-dual-slides` | 3A | Dual-audience NotebookLM slide generation |
| `md-to-notion` | 3B | Notion page publishing |
| `content-repurposing-engine` | 3C | Multi-platform content generation |
| Slack MCP (`slack_send_message`) | 4 | Slack distribution |
| `gws-drive` | 3A | Google Drive slide upload |
