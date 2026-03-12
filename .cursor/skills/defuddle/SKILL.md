---
name: defuddle
description: >-
  Extract clean markdown content from any web page URL using the Defuddle API,
  stripping ads, sidebars, navigation, and UI noise. Returns markdown with YAML
  frontmatter (title, author, published, domain, word_count). Use when the user
  asks to "read this page", "extract content from URL", "get markdown from
  website", "clean up this webpage", "defuddle", or when feeding web content to
  an LLM with minimal noise. Do NOT use for general web search (use WebSearch),
  API endpoint calls, browser automation (use agent-browser), or fetching
  structured JSON data from APIs. Korean triggers: "검색", "데이터", "API", "자동화".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# Defuddle — Web Page to Clean Markdown

Extract the main content from any web page as clean markdown via the Defuddle API. Strips ads, sidebars, headers, footers, and navigation clutter.

## Input

The user provides one or more URLs to extract content from.

## Workflow

### Step 1: Extract Content

Run via Shell:

```bash
curl -s "https://defuddle.md/{url_without_protocol}"
```

**CRITICAL**: The URL must omit the protocol prefix (`https://` or `http://`). Examples:

```bash
# Correct
curl -s "https://defuddle.md/example.com/article"

# Incorrect — do not include protocol
curl -s "https://defuddle.md/https://example.com/article"
```

The response is markdown with YAML frontmatter:

```markdown
---
title: "Article Title"
author: "Author Name"
published: 2025-10-20T00:00:00+00:00
source: "https://example.com/article"
domain: "example.com"
description: "Article description."
word_count: 1234
---

Article content in clean markdown...
```

### Step 2: Parse Metadata

Extract metadata from the YAML frontmatter block for downstream use:

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Page title |
| `author` | string | Author name |
| `published` | string | Publication date (ISO 8601) |
| `source` | string | Original URL |
| `domain` | string | Domain name |
| `description` | string | Page description/summary |
| `word_count` | number | Word count of extracted content |

### Step 3: Deliver Content

Based on the user's intent:

- **Display**: Show the markdown content directly to the user
- **Save**: Write to a file via `Write` tool
- **Summarize**: Feed the markdown to the LLM for analysis or summarization
- **Compare**: Extract multiple URLs and compare their content

## Advanced Usage

### Batch Extraction

For multiple URLs, run parallel Shell commands:

```bash
curl -s "https://defuddle.md/example.com/page1"
curl -s "https://defuddle.md/example.com/page2"
```

### Combining with Other Tools

- **Defuddle + Summarization**: Extract clean content, then summarize in the same turn
- **Defuddle + Translation**: Extract English content, translate to Korean
- **Defuddle + Comparison**: Extract two competing articles, compare key points

### When to Prefer Defuddle over WebFetch

| Scenario | Use |
|----------|-----|
| Page has heavy ads/sidebars/navigation | Defuddle |
| Need markdown with structured frontmatter | Defuddle |
| Simple page or API docs | WebFetch is sufficient |
| Need to interact with page elements | Use agent-browser instead |

## Examples

### Example 1: Read a blog post

User says: "Read this article and summarize it: https://stephango.com/file-over-app"

Actions:
1. Run `curl -s "https://defuddle.md/stephango.com/file-over-app"`
2. Parse frontmatter: title, author, word_count
3. Summarize the extracted markdown content for the user

Result: Clean article text without navigation/footer noise, summarized in Korean.

### Example 2: Extract and save documentation

User says: "Save the content from https://docs.example.com/guide as a markdown file"

Actions:
1. Run `curl -s "https://defuddle.md/docs.example.com/guide"`
2. Write the output to a local `.md` file using the Write tool

Result: Clean documentation saved as a local markdown file with frontmatter metadata.

### Example 3: Compare two pages

User says: "Compare the main points of these two articles"

Actions:
1. Run parallel `curl` commands for both URLs via Defuddle
2. Parse both responses
3. Compare key points side-by-side

Result: Structured comparison of both articles' content without UI noise.

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| Empty response | `curl` returns empty string | URL may be invalid or blocked; try `WebFetch` as fallback |
| Timeout | `curl` hangs beyond 30s | Add `--max-time 15` flag; report timeout to user |
| No main content found | Response has frontmatter but empty body | Site may use heavy JS rendering; suggest `agent-browser` instead |
| Rate limiting | HTTP 429 or delayed responses | Wait and retry; for batch operations, add 1s delay between requests |
| Invalid URL format | Error or unexpected output | Verify URL has no protocol prefix; strip `https://` before passing |
