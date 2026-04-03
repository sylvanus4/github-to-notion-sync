## Long-Form Compressor

Condense long documents into user-specified formats (executive summary, bullet brief, one-page memo, tweet-length, custom word count) with configurable compression ratios.

### Usage

```
# Executive summary
/compress "docs/report.md" --format executive-summary

# Tweet-length summary
/compress "outputs/analysis-2026-04-03.json" --format tweet

# Custom word count
/compress "docs/paper-review.md" --target 500

# Bullet brief
/compress "이 문서 핵심만 뽑아줘" --format bullets
```

### Workflow

1. **Ingest** — Read document (file, URL, Notion, pasted text); measure word count
2. **Target** — Determine compression format and ratio
3. **Priorities** — Set preservation priority (data-first, decision-first, narrative-first, balanced)
4. **Compress** — Extract thesis, rank points, cut from bottom, eliminate redundancy
5. **Output** — Compressed content with source stats, ratio, and "What Was Cut" section

### Output

Compressed document at target length with compression ratio, preservation priority applied, and list of major omissions.

### Execution

Read and follow the `long-form-compressor` skill (`.cursor/skills/standalone/long-form-compressor/SKILL.md`).
