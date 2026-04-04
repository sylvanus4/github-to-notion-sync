---
name: kb-search
description: >-
  Search across Knowledge Base wiki articles using keyword matching,
  semantic search, and fuzzy search. Returns ranked results with
  context snippets. Designed as both a user-facing tool and an
  LLM tool for use in larger query pipelines.
  Use when the user asks to "search KB", "find in knowledge base",
  "kb search", "grep wiki", "look up in KB", or wants to locate
  specific information across wiki articles without full Q&A synthesis.
  Do NOT use for synthesized Q&A answers (use kb-query).
  Do NOT use for web search (use WebSearch).
  Do NOT use for codebase search (use Grep).
  Korean triggers: "KB 검색", "위키 검색", "지식베이스 검색",
  "KB에서 찾기", "위키에서 검색".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
  tags: ["knowledge-base", "search", "retrieval"]
---

# KB Search — Wiki Search Engine

Fast search across Knowledge Base wiki articles. Returns ranked results with context snippets. Serves as both a direct user tool and an LLM utility for larger query pipelines.

## Search Modes

| Mode | Speed | Best For |
|------|-------|----------|
| **keyword** | Fast | Exact terms, specific names, identifiers |
| **semantic** | Medium | Conceptual queries, "articles about X" |
| **fuzzy** | Medium | Approximate matches, typo tolerance |
| **heading** | Fast | Find articles by title/heading |

## Workflow

### Step 1: Parse Query

Determine the search mode:
- If query is a single term or exact phrase → `keyword`
- If query is a question or conceptual → `semantic`
- If query contains potential typos or partial terms → `fuzzy`
- If query starts with `title:` or `heading:` → `heading`

### Step 2: Execute Search

#### Keyword Search

Use Grep to find exact matches across wiki files:

```bash
rg -i --type md -C 2 "{query}" knowledge-bases/{topic}/wiki/
```

#### Semantic Search

1. Read `_index.md` to get article summaries
2. Score each article's summary against the query for semantic relevance
3. Read top-scoring articles and search within them
4. Return context-rich snippets

#### Heading Search

Search only headings and frontmatter titles:

```bash
rg "^#+\s.*{query}" knowledge-bases/{topic}/wiki/ --type md
rg "^title:.*{query}" knowledge-bases/{topic}/wiki/ --type md
```

#### Fuzzy Search

Use ripgrep with word boundaries and case insensitivity:

```bash
rg -i --type md "{query}" knowledge-bases/{topic}/wiki/
```

### Step 3: Rank Results

Score results by:
1. **Title match** (highest): Query appears in article title → 10 points
2. **Heading match**: Query appears in a heading → 7 points
3. **Definition match**: Query appears in first paragraph → 5 points
4. **Body match**: Query appears in article body → 3 points
5. **Frequency**: More occurrences → +1 per occurrence (cap 5)

### Step 4: Format Output

Present results as a ranked list:

```markdown
## Search Results for "{query}" in {topic} KB

**{N} results found** | Mode: {mode}

### 1. [[concept-name]] (Score: 15)
> ...context snippet with **highlighted** match...
**File:** wiki/concepts/concept-name.md | **Words:** 850

### 2. [[reference-notes]] (Score: 8)
> ...context snippet with **highlighted** match...
**File:** wiki/references/reference-notes.md | **Words:** 600

### 3. [[connection-article]] (Score: 5)
> ...context snippet with **highlighted** match...
**File:** wiki/connections/connection-article.md | **Words:** 400
```

## CLI-Style Interface

For LLM tool use in pipelines, the search can be invoked with structured output:

```json
{
  "query": "attention mechanism",
  "topic": "transformer-architectures",
  "mode": "semantic",
  "top_k": 5,
  "results": [
    {
      "file": "wiki/concepts/attention-mechanism.md",
      "title": "Attention Mechanism",
      "score": 15,
      "snippet": "The attention mechanism allows the model to..."
    }
  ]
}
```

## Examples

### Example 1: Keyword search

**User says:** "Search my ML KB for 'dropout'"

**Actions:**
1. Run keyword search: `rg -i "dropout" knowledge-bases/ml/wiki/ --type md -C 2`
2. Rank and present results

### Example 2: Semantic search

**User says:** "Find articles about preventing overfitting in my KB"

**Actions:**
1. Read index to get article summaries
2. Score summaries for relevance to "preventing overfitting"
3. Read top articles for context snippets
4. Present ranked results

### Example 3: Search as LLM tool

**Used by kb-query internally:**

1. kb-query calls kb-search with a specific sub-question
2. kb-search returns top 3 results with file paths
3. kb-query reads those files for full content
4. kb-query synthesizes the final answer

## Standalone CLI

`scripts/kb_search.py` provides a direct terminal search without the full orchestrator:

```bash
python scripts/kb_search.py "query"              # search all KBs
python scripts/kb_search.py "query" -t ai-knowledge-bases  # specific topic
python scripts/kb_search.py "query" --json        # JSON output for pipelines
python scripts/kb_search.py "query" -C 3          # with context lines
```

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| No matches | Zero results | Suggest alternative queries, check spelling |
| Too many matches | > 50 results | Narrow with more specific terms |
| No wiki | Wiki directory missing | Prompt to run kb-compile |
