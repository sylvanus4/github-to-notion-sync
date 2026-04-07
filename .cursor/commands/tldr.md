---
description: "Condense any long text, URL, or file into a concise summary preserving only the key points"
argument-hint: "<text, URL, or file path to summarize>"
---

# TL;DR — Too Long; Didn't Read

Compress verbose content into its essential points. Accepts pasted text, URLs, or file paths.

## Usage

```
/tldr [paste long text here]
/tldr https://example.com/long-article
/tldr outputs/papers/2604.03128/review-2604.03128-2026-04-07.md
/tldr --one-liner What is the key takeaway from this 50-page report?
/tldr --tweet Summarize this paper for Twitter
/tldr --paragraph 이 문서의 핵심을 한 문단으로 요약해줘
```

## Your Task

User input: $ARGUMENTS

### Mode Selection

Parse `$ARGUMENTS` for output format flags:

- **No flags / `--bullets`** — 3-5 bullet points (default)
- `--one-liner` — Single sentence summary
- `--tweet` — Under 280 characters, punchy and shareable
- `--paragraph` — One dense paragraph (max 100 words)
- `--structured` — Sections: Key Point, Supporting Evidence, So What?, What's Missing

### Workflow

1. **Detect input type**
   - Raw text pasted → use directly
   - URL → extract content via `defuddle` skill (`.cursor/skills/standalone/defuddle/SKILL.md`)
   - File path → read the file
2. **Identify core claims** — Find the 3-5 most important assertions or findings
3. **Rank by importance** — Order claims by impact and novelty, not by document order
4. **Compress** — Write each point in one concise sentence; eliminate hedging, filler, and repetition
5. **Add verdict** — Append a one-line "Bottom line:" assessment
6. **Format** — Apply the selected output format

### Output Format (default `--bullets`)

```
## TL;DR

- [Key point 1]
- [Key point 2]
- [Key point 3]

**Bottom line:** [One-sentence verdict]
```

### Constraints

- Never add information not present in the source
- Preserve the author's intent — do not editorialize beyond the verdict line
- If the source is under 200 words, respond with "This is already short enough" and quote the original
- For URLs, cite the source title and URL at the top

### Execution

For long documents (>5000 words), reference the `long-form-compressor` skill (`.cursor/skills/standalone/long-form-compressor/SKILL.md`) for compression-ratio-aware summarization. For URLs, use the `defuddle` skill for clean content extraction.
