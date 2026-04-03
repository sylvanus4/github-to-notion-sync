---
name: kb-index
description: >-
  Auto-maintain index files, summaries, and navigational metadata for an
  LLM Knowledge Base wiki. Rebuilds _index.md, _summary.md, _concept-map.md,
  and _glossary.md from current wiki contents. Ensures the LLM can efficiently
  navigate and answer questions against the KB without reading every article.
  Use when the user asks to "rebuild index", "refresh KB index",
  "kb index", "update wiki index", "regenerate summaries",
  or after manual edits to wiki articles.
  Do NOT use for compiling wiki from raw sources (use kb-compile).
  Do NOT use for ingesting new sources (use kb-ingest).
  Do NOT use for querying the KB (use kb-query).
  Korean triggers: "인덱스 갱신", "KB 인덱스", "위키 인덱스",
  "요약 재생성", "인덱스 리빌드".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
  tags: ["knowledge-base", "index", "navigation"]
---

# KB Index — Wiki Index Maintainer

Auto-maintain navigational index files that let an LLM efficiently find and reference articles in a Knowledge Base wiki. Scans all wiki articles, extracts metadata, and regenerates index files.

## Why This Matters

At ~400K words, an LLM cannot read the entire wiki for every query. Index files provide a lightweight map — the LLM reads the index first (~2-5K tokens), identifies relevant articles, then reads only those. This is the "poor man's RAG" that Karpathy describes.

## Prerequisites

- Wiki must exist at `knowledge-bases/{topic}/wiki/`
- At least some articles with YAML frontmatter

## Workflow

### Step 1: Scan Wiki Directory

List all `.md` files in `wiki/` and subdirectories, excluding files starting with `_` (index files themselves):

```bash
find knowledge-bases/{topic}/wiki -name "*.md" ! -name "_*" -type f | sort
```

### Step 2: Extract Metadata

For each article, read its YAML frontmatter to extract:
- `title`
- `category` (concepts, references, connections)
- `related` (list of related concepts)
- `sources` (list of raw source files)
- `word_count`
- `last_compiled`

If frontmatter is missing or incomplete, parse the file to estimate:
- Title from first `# ` heading
- Word count from body text
- Category from directory path

### Step 3: Regenerate `_index.md`

Build a comprehensive index organized by category:

```markdown
# {Topic} Knowledge Base Index

> {N} articles | ~{W}K total words | Last indexed: {date}

## Quick Navigation

- [Concepts](#concepts) ({N1} articles)
- [References](#references) ({N2} articles)
- [Connections](#connections) ({N3} articles)

## Concepts

| # | Article | Summary | Words | Related | Sources |
|---|---------|---------|-------|---------|---------|
| 1 | [[concept-name]] | Brief one-liner | 850 | 3 | 2 |
| 2 | ... | ... | ... | ... | ... |

## References

| # | Source | Key Concepts | Words | Date |
|---|--------|-------------|-------|------|
| 1 | [[source-notes]] | concept-1, concept-3 | 600 | 2026-01 |

## Connections

| # | Article | Bridging | Words |
|---|---------|----------|-------|
| 1 | [[a-vs-b]] | concept-a ↔ concept-b | 500 |

## Statistics

- Total articles: {N}
- Total words: ~{W}K
- Average article length: ~{avg} words
- Most connected concept: {name} ({N} links)
- Most cited source: {name} ({N} references)
```

### Step 4: Regenerate `_summary.md`

Read the top 5-10 most interconnected concept articles and synthesize a 500-1000 word executive summary of the entire KB.

### Step 5: Regenerate `_concept-map.md`

Build a Mermaid diagram from the `related` fields:

````markdown
# Concept Map

```mermaid
graph TD
    A["Concept 1"] --> B["Concept 2"]
    A --> C["Concept 3"]
    B --> D["Concept 4"]
    C --> D
    style A fill:#4CAF50,color:#fff
    style B fill:#2196F3,color:#fff
```

## Legend

- **Green nodes**: Hub concepts (3+ connections)
- **Blue nodes**: Standard concepts
- **Dashed lines**: Weak/speculative connections
````

### Step 6: Regenerate `_glossary.md`

Scan all articles for defined terms (bold terms, heading terms) and compile:

```markdown
# Glossary

| Term | Definition | Article |
|------|-----------|---------|
| Attention | Mechanism for weighing input relevance | [[attention-mechanism]] |
```

### Step 7: Update Manifest Stats

Update `manifest.json` with current stats from the index scan.

## Examples

### Example 1: Rebuild after manual edit

**User says:** "I edited a few wiki articles, rebuild the index"

**Actions:**
1. Scan all wiki articles
2. Regenerate all `_` prefixed files
3. Report changes (new articles found, removed articles, updated stats)

### Example 2: Full reindex

**User says:** "kb index transformer-architectures"

**Actions:**
1. Scan `knowledge-bases/transformer-architectures/wiki/`
2. Regenerate `_index.md`, `_summary.md`, `_concept-map.md`, `_glossary.md`
3. Update `manifest.json`

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| No wiki articles | Empty wiki/ directory | Prompt to run kb-compile first |
| Missing frontmatter | Articles lack YAML headers | Infer metadata from content, warn user |
| Broken links | `[[concept]]` points to nonexistent file | List broken links in report |
| Orphan articles | Articles not referenced by any other | List orphans in report |
