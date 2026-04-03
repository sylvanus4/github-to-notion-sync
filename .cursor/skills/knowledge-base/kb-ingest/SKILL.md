---
name: kb-ingest
description: >-
  Ingest raw source material (web articles, PDFs, papers, repos, images,
  YouTube transcripts) into a local LLM Knowledge Base topic directory.
  Converts each source to clean markdown via defuddle/WebFetch, downloads
  associated images, and catalogs everything in raw/ with YAML frontmatter.
  Use when the user asks to "add to knowledge base", "ingest article",
  "kb ingest", "add source to KB", "clip this URL to KB", "index this
  paper into KB", "add raw data", or wants to collect source material
  for LLM-maintained wiki compilation.
  Do NOT use for compiling the wiki from raw data (use kb-compile).
  Do NOT use for querying the KB (use kb-query).
  Do NOT use for general web scraping without KB intent (use scrapling).
  Do NOT use for Cognee knowledge graph ingestion (use cognee).
  Korean triggers: "지식베이스 수집", "KB 인제스트", "원본 추가",
  "지식 베이스에 추가", "자료 수집".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
  tags: ["knowledge-base", "ingest", "data-collection"]
---

# KB Ingest — Source Material Collector

Ingest diverse source material into a structured LLM Knowledge Base. Converts web pages, PDFs, papers, repos, and videos into clean markdown with downloaded assets, ready for wiki compilation.

## Prerequisites

- **defuddle API** available (no install needed — uses `https://defuddle.md/`)
- **curl** available on PATH
- Knowledge base root directory: `knowledge-bases/` at project root

## Input

The user provides:

1. **Topic name** — the KB topic to ingest into (e.g. `transformer-architectures`)
2. **One or more sources** — URLs, local file paths, or text content

## Directory Structure

```
knowledge-bases/{topic}/
├── raw/                    # Ingested source documents
│   ├── {slug}.md           # Converted markdown with frontmatter
│   ├── {slug}.pdf          # Original binary files (kept as-is)
│   └── assets/             # Downloaded images and media
│       └── {slug}/         # Per-source asset directory
├── wiki/                   # (Managed by kb-compile)
├── outputs/                # (Managed by kb-output)
└── manifest.json           # KB metadata and source registry
```

## Workflow

### Step 1: Initialize KB Directory

If the topic directory doesn't exist, create it:

```bash
mkdir -p knowledge-bases/{topic}/raw/assets
mkdir -p knowledge-bases/{topic}/wiki
mkdir -p knowledge-bases/{topic}/outputs
```

If `manifest.json` doesn't exist, create it:

```json
{
  "topic": "{topic}",
  "created": "YYYY-MM-DD",
  "description": "",
  "sources": [],
  "stats": {
    "raw_count": 0,
    "wiki_articles": 0,
    "total_words": 0
  }
}
```

### Step 2: Classify Source Type

For each source, determine the type:

| Source Pattern | Type | Processing |
|----------------|------|------------|
| `https://...` web page | `web-article` | defuddle → markdown |
| `https://youtube.com/...` or `youtu.be/...` | `youtube` | defuddle → transcript markdown |
| `https://arxiv.org/abs/...` | `arxiv-paper` | defuddle + alphaxiv lookup |
| `https://github.com/...` | `github-repo` | WebFetch README + key files |
| Local `.pdf` file | `pdf` | Copy to raw/, extract text with anthropic-pdf |
| Local `.md` file | `markdown` | Copy to raw/ with frontmatter |
| Local image file | `image` | Copy to raw/assets/ |
| Raw text/paste | `text` | Save as markdown with frontmatter |

### Step 3: Extract Content

**For web articles:**

```bash
curl -s "https://defuddle.md/{url_without_protocol}" > knowledge-bases/{topic}/raw/{slug}.md
```

**For YouTube videos:**

```bash
curl -s "https://defuddle.md/youtube.com/watch?v={video_id}" > knowledge-bases/{topic}/raw/{slug}.md
```

**For arXiv papers:**

1. Extract content via defuddle
2. Optionally fetch structured overview from AlphaXiv:
   ```bash
   curl -s "https://defuddle.md/alphaxiv.org/abs/{paper_id}" > knowledge-bases/{topic}/raw/{slug}.md
   ```

**For GitHub repos:**

1. Fetch README via WebFetch
2. Save key files (if user specifies) to raw/

**For local files:**

1. Copy file to `raw/` directory
2. For PDFs, extract text content and save as companion `.md`

### Step 4: Download Associated Images

For web articles with images, download referenced images to `raw/assets/{slug}/`:

```bash
mkdir -p knowledge-bases/{topic}/raw/assets/{slug}
```

Parse the markdown for image references and download each:

```bash
curl -sL "{image_url}" -o "knowledge-bases/{topic}/raw/assets/{slug}/{filename}"
```

Update image references in the markdown to use relative paths:

```markdown
![alt](assets/{slug}/{filename})
```

### Step 5: Add Frontmatter

Ensure every raw markdown file has YAML frontmatter:

```yaml
---
title: "Article Title"
source: "https://original-url.com/article"
source_type: "web-article"
author: "Author Name"
date_published: "2026-01-15"
date_ingested: "2026-04-03"
tags: []
word_count: 1234
summary: ""
---
```

### Step 6: Update Manifest

Append a source entry to `manifest.json`:

```json
{
  "slug": "article-slug",
  "title": "Article Title",
  "source_url": "https://...",
  "source_type": "web-article",
  "date_ingested": "2026-04-03",
  "file": "raw/article-slug.md",
  "word_count": 1234
}
```

Update `stats.raw_count`.

### Step 7: Confirm and Report

Report to the user:

```
✓ Ingested: {title}
  Type: {source_type}
  Words: {word_count}
  File: knowledge-bases/{topic}/raw/{slug}.md
  Assets: {N} images downloaded
```

## Batch Ingestion

When multiple URLs are provided, process them sequentially, reporting progress:

```
[1/5] Ingesting: https://example.com/article-1 ... ✓
[2/5] Ingesting: https://example.com/article-2 ... ✓
...
```

## Slug Generation

Generate slugs from titles:
- Lowercase
- Replace spaces with hyphens
- Remove special characters except hyphens
- Truncate to 60 characters
- Ensure uniqueness by appending `-2`, `-3` etc. if needed

## Examples

### Example 1: Ingest a web article

**User says:** "Add this to my ML knowledge base: https://example.com/attention-is-all-you-need-explained"

**Actions:**
1. Create/verify `knowledge-bases/ml/raw/` directory
2. Run defuddle to extract markdown
3. Download images to `raw/assets/attention-is-all-you-need-explained/`
4. Add frontmatter
5. Update manifest

### Example 2: Batch ingest from a list

**User says:** "Ingest these 3 papers into the 'diffusion-models' KB: [url1, url2, url3]"

**Actions:**
1. Process each URL sequentially
2. Report progress per source
3. Update manifest with all 3 sources

### Example 3: Ingest a local PDF

**User says:** "Add this PDF to the robotics KB: ~/papers/sim-to-real.pdf"

**Actions:**
1. Copy PDF to `knowledge-bases/robotics/raw/sim-to-real.pdf`
2. Extract text via anthropic-pdf skill
3. Save extracted text as `knowledge-bases/robotics/raw/sim-to-real.md`
4. Add frontmatter
5. Update manifest

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| URL unreachable | defuddle returns empty/error | Log warning, skip source, continue batch |
| Image download fails | curl returns non-200 | Keep original URL reference, log warning |
| Duplicate source | Same URL already in manifest | Ask user: overwrite or skip |
| Invalid file path | Local file not found | Report error with path |
| Rate limiting | defuddle returns 429 | Wait 5 seconds, retry once |
