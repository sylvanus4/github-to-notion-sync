---
name: long-form-compressor
description: >-
  Condense long documents into user-specified output formats (executive summary,
  bullet brief, one-page memo, tweet-length, custom word count) with
  configurable compression ratios and preservation priorities. Handles articles,
  reports, papers, transcripts, and multi-chapter documents. Use when the user
  asks to "summarize this", "compress this document", "make this shorter",
  "TL;DR", "executive summary", "one-page summary", "bullet point summary",
  "요약해줘", "짧게 줄여줘", "한 페이지로", "핵심만", "문서 압축", "긴 글
  요약", or wants a document condensed to a specific length. Do NOT use for
  agent context compression (use ce-context-compression or ecc-strategic-compact).
  Do NOT use for prompt optimization (use prompt-architect). Do NOT use for
  meeting digest (use meeting-digest). Do NOT use for content repurposing across
  platforms (use content-repurposing-engine).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "generation"
---

# Long-Form Compressor

Condense any long document into a shorter format while preserving what matters most to the reader.

## When to Use

- A 20-page report needs a 1-page executive summary
- A research paper needs a 3-bullet TL;DR
- A transcript needs key takeaways extracted
- A user wants a document at a specific word count (e.g., "make this 500 words")
- Meeting notes, articles, or specs need compression for different audiences

## Workflow

### Step 1: Ingest Document

Accept input as:
- File path (read the file)
- Pasted text
- URL (extract via defuddle)
- Notion page URL (fetch via Notion MCP)

Measure the source: word count, section count, and estimated reading time.

### Step 2: Determine Compression Target

Ask or infer the target format:

| Format | Target Length | Use Case |
|--------|-------------|----------|
| **Tweet** | ≤280 characters | Social sharing |
| **TL;DR** | 1-3 sentences | Slack, email preview |
| **Bullet Brief** | 5-10 bullets | Quick scan |
| **One-Page Memo** | 250-400 words | Decision-makers |
| **Executive Summary** | 500-800 words | Leadership review |
| **Half-Length** | 50% of original | General compression |
| **Custom** | User-specified word count | Any |

Calculate the compression ratio: `source_words / target_words`.

### Step 3: Set Preservation Priorities

Ask or infer what the user cares about preserving:

| Priority | What Gets Kept | What Gets Cut |
|----------|---------------|---------------|
| **Data-first** | Numbers, statistics, metrics, evidence | Narrative, context, transitions |
| **Decision-first** | Conclusions, recommendations, action items | Background, methodology, alternatives |
| **Narrative-first** | Story arc, key arguments, flow | Supporting details, caveats, appendices |
| **Balanced** (default) | Core thesis + top evidence + conclusions | Repetition, examples, tangential points |

### Step 4: Compression

Apply these rules in order:

1. **Extract core thesis** — Identify the single most important claim or conclusion
2. **Rank supporting points** — Order all supporting arguments by importance to the thesis
3. **Cut from the bottom** — Remove lowest-ranked points until target length is approached
4. **Eliminate redundancy** — Merge overlapping points; remove repeated evidence
5. **Compress language** — Replace verbose phrases with concise equivalents
6. **Preserve attribution** — Keep source citations for any data or quotes retained
7. **Verify fidelity** — Confirm the compressed version doesn't distort the original's meaning

**Compression strategies by ratio:**

| Ratio | Strategy |
|-------|----------|
| 2:1 (half) | Cut examples, reduce transitions, merge similar sections |
| 5:1 | Keep only thesis + top 3-5 supporting points + conclusion |
| 10:1 | Thesis + key evidence + single recommendation |
| 20:1+ | Core thesis only, possibly with one data point |

### Step 5: Output

```markdown
## Compressed: [Original Title]

**Source**: [file path, URL, or "pasted text"]
**Original**: ~[N] words | **Compressed**: ~[M] words | **Ratio**: [X]:1
**Preservation priority**: [Data/Decision/Narrative/Balanced]

---

[Compressed content in the target format]

---

## What Was Cut
- [Major section/point omitted and why]
- [Data points excluded]
- [Caveats or nuances simplified]
```

For **Bullet Brief** and **TL;DR** formats, skip the "What Was Cut" section.

## Examples

### Example 1: Report to executive summary

User: "이 20페이지 분석 리포트를 executive summary로 줄여줘"

Read the report (~5,000 words), apply Balanced preservation, produce an 800-word executive summary with key findings, data highlights, and recommendations. List the 3-4 major sections that were condensed.

### Example 2: Article to tweet

User: "Summarize this article in a tweet"

Extract the single most surprising or important claim from the article, compress to ≤280 characters with impact. Example: "New study: companies using AI agents ship 3x faster but spend 40% more on debugging — the speed-quality tradeoff is real."

### Example 3: Custom word count

User: "Make this 2,000-word doc exactly 500 words"

Apply a 4:1 compression. Keep thesis, top 3 supporting points, and conclusion. Cut all examples, reduce transitions to one sentence each, merge the two methodology paragraphs into one sentence.

### Example 4: Transcript to bullet brief

User: "Give me the key takeaways from this 1-hour transcript"

Extract 7-10 key points as bullets, organized by topic. Each bullet is a complete thought with any relevant data. Skip small talk, repetition, and tangential discussion.

## Error Handling

| Scenario | Action |
|----------|--------|
| Source is already shorter than target | Return the original with a note: "Source is already at or below target length" |
| Target length is unreasonably small for the content | Warn: "Compressing [N] words to [M] words (ratio [X]:1) will lose significant detail. Proceed?" |
| Source has no clear thesis or structure | Ask: "What's the main point you want preserved in the summary?" |
| Multiple independent topics in source | Offer to produce separate summaries per topic or one unified summary |
| Source contains tables/charts that don't compress well | Preserve table headers and key rows; note omitted data |

## Composability

- **content-repurposing-engine** — Compress first, then repurpose the summary across platforms
- **scqa-writing-framework** — Structure the summary using SCQA for persuasive compression
- **sentence-polisher** — Polish the compressed output
- **md-to-notion** — Publish the summary to Notion
- **anthropic-docx** — Export the executive summary as a Word document
