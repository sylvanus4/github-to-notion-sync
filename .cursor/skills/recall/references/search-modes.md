# Search Mode Reference

## Mode Comparison

| Mode | Speed | Best For | Command |
|------|-------|----------|---------|
| BM25 | ~0.1s | Exact terms, function names, error messages | `--mode bm25` |
| Semantic | ~2-5s | Conceptual queries, "how did we solve X?" | `--mode semantic` |
| Hybrid | ~3-6s | General purpose, best overall quality | `--mode hybrid` |
| Temporal | ~0.1s | Date-based session lookup | `--mode temporal` |

## When to Use Each Mode

### BM25 (Keyword Search)
- Searching for specific function names, class names, or error messages
- Looking up exact terms like "Guard Pipeline", "daily_stock_check"
- Fast iteration — use BM25 first, escalate to hybrid if results are poor
- 53x faster than hybrid (no embedding computation)

### Semantic (Embedding Search)
- Conceptual queries where exact words may not match
- "How did we handle authentication issues?"
- "What was the reasoning behind the database choice?"
- Cross-language queries (Korean query matching English content, or vice versa)

### Hybrid (RRF Fusion)
- Default mode — best overall result quality
- Combines keyword precision with semantic understanding
- Uses Reciprocal Rank Fusion (RRF) with k=60 constant
- Recommended when BM25 returns <3 results or low-confidence matches

### Temporal (Date Filter)
- "What did we work on yesterday?"
- "Show me all sessions from last week"
- "What happened on March 5?"
- Supports: `yesterday`, `today`, `last week`, `YYYY-MM-DD`

## Query Expansion Strategy

For topic searches, expand the user's query into 2-3 variants:

**User input**: "trading agent"
**Expanded queries**:
1. "trading agent" (original)
2. "autonomous trading system"
3. "OpenAlice Guard Pipeline Brain"

Run BM25 for each variant in parallel, merge and deduplicate results.

## Score Interpretation

| Score Range | Meaning |
|-------------|---------|
| BM25 > 5.0 | Strong keyword match |
| BM25 1.0-5.0 | Moderate match |
| BM25 < 1.0 | Weak / noisy match |
| Semantic > 0.7 | High conceptual similarity |
| Semantic 0.3-0.7 | Related content |
| Semantic < 0.3 | Likely irrelevant |
| Hybrid RRF > 0.03 | Top-tier combined result |

## CLI Examples

```bash
# Quick keyword search
python scripts/memory/search.py --mode bm25 "Guard Pipeline" --top 5 --verbose

# Conceptual search
python scripts/memory/search.py --mode semantic "how did we decide on the database architecture" --top 5

# Best quality search
python scripts/memory/search.py --mode hybrid "trading agent safety checks" --top 5 --verbose

# Date lookup
python scripts/memory/search.py --mode temporal --date yesterday --top 10

# JSON output for programmatic use
python scripts/memory/search.py --mode hybrid "CI/CD pipeline" --json
```
