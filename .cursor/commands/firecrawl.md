## Firecrawl

Scrape structured data from complex or hostile websites that block naive scrapers — anti-bot bypass, JavaScript rendering, and large-scale crawling.

### Usage

```
/firecrawl "https://example.com/pricing"       # scrape a single page
/firecrawl --crawl "https://docs.example.com"  # crawl an entire site
/firecrawl --stealth "https://protected.site"   # bypass anti-bot protection
```

### Workflow

1. **Target** — Identify the URL(s) and desired data structure
2. **Strategy** — Choose extraction method: simple fetch, browser render, or stealth mode
3. **Extract** — Scrape content with anti-bot bypass and JavaScript rendering
4. **Structure** — Parse into clean markdown or structured JSON
5. **Output** — Save extracted data for downstream processing

### Execution

Read and follow the `scrapling` skill (`.cursor/skills/standalone/scrapling/SKILL.md`) for adaptive parsing with anti-bot bypass (Cloudflare Turnstile), concurrent spiders, and stealth fetching. For simpler URL-to-markdown extraction, use `defuddle` (`.cursor/skills/standalone/defuddle/SKILL.md`). For CLI-based browser automation, use `agent-browser` (`.cursor/skills/standalone/agent-browser/SKILL.md`).

### Examples

Scrape a pricing page:
```
/firecrawl "https://competitor.com/pricing"
```

Crawl documentation:
```
/firecrawl --crawl "https://docs.framework.io" --output docs-dump/
```
