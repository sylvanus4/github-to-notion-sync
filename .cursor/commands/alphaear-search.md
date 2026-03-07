---
description: "Finance-specific web search (Jina/DDG/Baidu) and local RAG search"
---

# AlphaEar Search

## Skill Reference

Read and follow the skill at `.cursor/skills/alphaear-search/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

- If `$ARGUMENTS` contains a query string, use it for search
- If `$ARGUMENTS` specifies an engine (jina, ddg, baidu, local), use that engine
- If `$ARGUMENTS` mentions "aggregate" or "multi", run `aggregate_search`
- If `$ARGUMENTS` mentions "local" or "rag", search the local daily_news DB
- If `$ARGUMENTS` is empty, ask user for a finance search query

### Step 2: Execute

Follow the workflow in the skill:

1. Check cache relevance using Smart Cache prompt
2. Run search with specified or default engine
3. Return formatted results

### Step 3: Report

Present results with:
- Search query and engine used
- Summarized findings
- Source URLs where available
