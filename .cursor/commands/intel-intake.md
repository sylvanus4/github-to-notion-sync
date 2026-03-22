---
description: "Process any URL (news, paper, tweet, blog) through the unified intelligence pipeline — extract, classify, enrich, and route to the appropriate Slack channel"
---

## Intel Intake

Single entry point for all intelligence sources. Drop any URL and get it classified, enriched, and routed.

### Usage

```
/intel-intake <url>                         # process a single URL
/intel-intake <url1> <url2> ...             # batch process multiple URLs
/intel-intake --dry-run <url>               # classify and preview without posting
```

### Execution

Read and follow the skill at `.cursor/skills/unified-intel-intake/SKILL.md`.

User input: $ARGUMENTS

1. Parse URL(s) from arguments
2. Auto-detect content type (news article, academic paper, tweet, blog post)
3. Extract content via defuddle or appropriate extractor
4. Classify into domain categories (AI/ML, Cloud, Finance, etc.)
5. Route to the appropriate Slack channel with enriched context
6. Log to daily intake manifest for knowledge aggregation
