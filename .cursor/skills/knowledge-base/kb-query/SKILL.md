---
name: kb-query
description: >-
  Ask complex questions against an LLM Knowledge Base wiki and get
  researched, citation-backed answers. The agent reads the index to
  identify relevant articles, deep-reads those articles, synthesizes
  an answer, and optionally files the result back into the wiki.
  Use when the user asks to "query the KB", "ask the knowledge base",
  "kb query", "research in KB", "what does the KB say about",
  "search my wiki", or wants answers derived from their curated sources.
  Do NOT use for web search (use WebSearch or parallel-web-search).
  Do NOT use for simple file reading (use Read tool directly).
  Do NOT use for adding new sources (use kb-ingest).
  Korean triggers: "KB 질문", "지식베이스 질문", "위키 검색",
  "KB 쿼리", "지식베이스에서 찾아줘".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "execution"
  tags: ["knowledge-base", "query", "q-and-a", "research"]
---

# KB Query — Knowledge Base Q&A

Research complex questions against your LLM-maintained wiki. The agent navigates the KB using index files, reads relevant articles, synthesizes answers with citations, and optionally archives results back into the wiki.

## Core Approach

This is "poor man's RAG" — no vector database needed. The LLM reads lightweight index files (~2-5K tokens) to identify relevant articles, then reads only those articles for depth. At scales up to ~100 articles and ~400K words, this approach works remarkably well.

## Prerequisites

- Wiki must exist at `knowledge-bases/{topic}/wiki/`
- Index files should be current (run kb-index if stale)

## Input

The user provides:

1. **Topic name** — which KB to query
2. **Question** — natural language question

Optional:
- `--no-file-back` — skip archiving the answer into the wiki (default: auto file-back is ON)
- `--deep` — read all potentially relevant articles, not just top matches
- `--with-sources` — include raw source excerpts in the answer

## Workflow

### Step 1: Read Index

Read `knowledge-bases/{topic}/wiki/_index.md` to get the full article inventory with summaries.

If `_index.md` doesn't exist or is stale, run kb-index first.

### Step 2: Identify Relevant Articles

Based on the question, identify the most relevant articles from the index:

1. Match question keywords against article titles and summaries
2. Follow `related` links to find connected articles
3. Check `_glossary.md` for term definitions
4. Rank articles by relevance

Typically 3-8 articles are sufficient for most queries.

### Step 3: Deep Read

Read the identified articles in full. For each article, note:
- Key facts relevant to the question
- Citations and source references
- Connections to other concepts
- Gaps or uncertainties

### Step 4: Synthesize Answer

Compose a comprehensive answer following this structure:

```markdown
## Answer

[Direct, clear answer to the question]

### Details

[Supporting analysis with specific references]

### Evidence

- From [[concept-1]]: "relevant excerpt or finding"
- From [[concept-2]]: "relevant excerpt or finding"

### Connections

[How different KB articles relate to this question]

### Limitations

[What the KB doesn't cover, uncertainties, potential gaps]

### Sources

- [[concept-1]] — primary source for [aspect]
- [[reference-notes-2]] — supporting data for [aspect]
```

### Step 5: File Back into Wiki (Auto)

By default, every query answer is automatically archived into the wiki. This implements the Karpathy feedback loop where explorations and queries "always add up" in the knowledge base. Use `--no-file-back` to skip this step.

Save the answer as a new article:

```
knowledge-bases/{topic}/wiki/queries/{question-slug}.md
```

With frontmatter:

```yaml
---
title: "Q: {question}"
category: "queries"
related: ["concept-1", "concept-2"]
date: "2026-04-03"
---
```

Then run kb-index to update the index with the new article.

### Step 6: Report

Present the answer to the user with:
- The synthesized answer
- List of articles consulted
- Confidence level (high/medium/low based on source coverage)
- Suggestions for follow-up queries

## Multi-Hop Queries

For complex questions requiring multi-step reasoning:

1. Decompose the question into sub-questions
2. Research each sub-question against the KB
3. Synthesize sub-answers into the final answer
4. Highlight where the chain of reasoning crosses concept boundaries

## Query Patterns

| Pattern | Example | Strategy |
|---------|---------|----------|
| Factual lookup | "What is X?" | Read glossary + concept article |
| Comparison | "How does X differ from Y?" | Read both concepts + connection articles |
| Synthesis | "What are the key themes?" | Read `_summary.md` + top concepts |
| Gap analysis | "What's missing in our understanding?" | Read `_summary.md` + lint report |
| Historical | "How has X evolved?" | Read chronological sources |
| Cross-cutting | "How do X, Y, Z interact?" | Read all three + connections |

## Examples

### Example 1: Simple concept query

**User says:** "What does the transformer KB say about positional encoding?"

**Actions:**
1. Read `_index.md` for the transformer KB
2. Find `[[positional-encoding]]` article
3. Read the article
4. Present a summary with citations

### Example 2: Complex synthesis query

**User says:** "Based on my ML KB, what are the 3 most promising research directions?"

**Actions:**
1. Read `_index.md` and `_summary.md`
2. Read top 10 concept articles by interconnectedness
3. Synthesize themes and identify frontier areas
4. Present ranked recommendations with evidence

### Example 3: File-back query

**User says:** "Query the diffusion KB: how do classifier-free and classifier guidance compare? File it back."

**Actions:**
1. Research the question against the KB
2. Write answer to `wiki/queries/classifier-free-vs-classifier-guidance.md`
3. Run kb-index to update
4. Report the filed location

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| No index file | `_index.md` missing | Run kb-index first |
| No relevant articles | Question doesn't match any KB content | Report "not covered" + suggest kb-ingest |
| Stale index | Index date much older than newest article | Run kb-index, then re-query |
| Contradictory sources | Different articles disagree | Present both views with citations |
