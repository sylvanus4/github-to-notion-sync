---
name: hf-papers
description: >-
  Discover daily and trending papers on Hugging Face Hub via the hf CLI. Use
  when the user asks to list today's papers, find trending AI research, browse
  daily papers by date, or track new publications on HF Hub. Do NOT use for
  full paper review with PM analysis (use paper-review), arXiv paper lookup
  (use alphaxiv-paper-lookup), related paper scouting (use
  related-papers-scout), or general web research (use parallel-web-search).
  Korean triggers: "오늘 논문", "트렌딩 논문", "HF 논문", "일일 논문".
---

# Hugging Face Papers

> **Prerequisites**: `hf` CLI installed and authenticated. See `hf-hub` skill.

## Quick Commands

### List Daily Papers

```bash
hf papers ls
hf papers ls --date today --sort trending --limit 20
hf papers ls --date 2026-03-17 --format json
hf papers ls -q  # paper IDs only
```

| Flag | Required | Description |
|------|----------|-------------|
| `--sort` | No | `publishedAt` (default), `trending` |
| `--date TEXT` | No | ISO date (`YYYY-MM-DD`) or `today` |
| `--limit INTEGER` | No | Number of results (default: 50) |
| `--format [table\|json]` | No | Output format |
| `-q, --quiet` | No | Print paper IDs only (one per line) |

## Common Patterns

```bash
# Today's trending papers
hf papers ls --sort trending --date today --limit 10

# Get paper IDs for piping to other tools
hf papers ls --date today -q | head -5

# JSON output for programmatic processing
hf papers ls --date today --sort trending --format json

# Papers from a specific date
hf papers ls --date 2026-03-15 --limit 30

# Combine with web search for deeper analysis
PAPER_IDS=$(hf papers ls --date today -q | head -3)
for id in $PAPER_IDS; do
  echo "Researching paper: $id"
done
```

## Agent Workflow Patterns

### Daily Paper Digest

1. Fetch trending papers: `hf papers ls --date today --sort trending --limit 10 --format json`
2. Extract titles and IDs from JSON
3. For each paper, search for associated models: `hf models ls --search PAPER_KEYWORD -q`
4. Compile digest with paper + model associations

### Paper-to-Model Discovery

1. List papers: `hf papers ls --date today --format json`
2. Extract keywords from titles
3. Cross-reference: `hf models ls --search KEYWORD --sort downloads -q`
4. Report which papers have practical model implementations

## Examples

### Example 1: Browse today's papers

**User says:** "Show me today's trending papers"

**Actions:**
1. Fetch: `hf papers ls --date today --sort trending --limit 10`
2. Present results with titles, IDs, and upvote counts
3. Offer to dive deeper into specific papers

### Example 2: Track papers over time

**User says:** "What were the hot papers last Monday?"

**Actions:**
1. Calculate date: last Monday = `2026-03-09`
2. Fetch: `hf papers ls --date 2026-03-09 --sort trending --limit 10`
3. Compare with today's papers for trend analysis

## Error Handling

| Issue | Resolution |
|-------|-----------|
| No papers for date | Verify date format (YYYY-MM-DD); daily papers may not be available for all dates |
| Authentication error | Run `hf auth login` — some paper metadata may require auth |
| Empty results | Try a different date or remove the date filter for latest papers |
