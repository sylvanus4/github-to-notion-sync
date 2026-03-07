---
name: scrapling
description: >-
  Write Python web scraping scripts using the Scrapling framework — adaptive
  parsing, anti-bot bypass (Cloudflare Turnstile), concurrent spiders, and
  stealth fetching. Use when the user asks to "scrape a website", "bypass
  cloudflare", "crawl pages", "adaptive scraping", "stealth scraping",
  "anti-bot scraping", "web spider", "scrapling", "extract data from website
  with Python", or any Python-based web scraping task that benefits from
  TLS fingerprint impersonation, browser automation, or large-scale crawling.
  Do NOT use for interactive browser automation via CLI (use agent-browser),
  simple URL-to-markdown extraction (use defuddle or WebFetch), or Playwright
  E2E test suites (use e2e-testing).
metadata:
  author: thaki
  version: 1.0.0
---

# Scrapling — Adaptive Web Scraping Framework

Write Python scripts that scrape websites using [Scrapling](https://github.com/D4Vinci/Scrapling) (v0.4.1). Handles anti-bot bypass, adaptive element relocation, and concurrent crawling.

## Prerequisites

```bash
# Parser only (no browser)
pip install scrapling

# With fetchers (HTTP + browser automation)
pip install "scrapling[fetchers]"
scrapling install  # install browser binaries

# With MCP server
pip install "scrapling[ai]"

# Everything
pip install "scrapling[all]"
scrapling install
```

## Fetcher Decision Tree

Pick the right fetcher for the task:

| Need | Fetcher | Why |
|------|---------|-----|
| Fast HTTP, no JS rendering | `Fetcher` | curl_cffi with TLS fingerprint impersonation |
| JS-rendered pages (SPA, dynamic) | `DynamicFetcher` | Playwright Chromium, full DOM |
| Cloudflare / anti-bot protected | `StealthyFetcher` | Fingerprint spoofing + Turnstile solver |
| Multiple requests, keep cookies | `*Session` variant | Persistent cookies and state |
| Large-scale crawl (many pages) | `Spider` | Concurrent requests, pause/resume, export |

## Quick-Start Examples

### 1. Simple HTTP Scraping

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text').getall()
authors = page.css('.quote .author::text').getall()

for q, a in zip(quotes, authors):
    print(f"{q} — {a}")
```

### 2. Stealth Fetch (Cloudflare Bypass)

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch(
    'https://protected-site.com',
    headless=True,
    solve_cloudflare=True,
    network_idle=True,
)
data = page.css('#content').get()
```

### 3. Session-Based Scraping (Cookies Persist)

```python
from scrapling.fetchers import FetcherSession

with FetcherSession(impersonate='chrome') as session:
    login = session.post('https://example.com/login', data={'user': 'x', 'pass': 'y'})
    page = session.get('https://example.com/dashboard')
    items = page.css('.item::text').getall()
```

### 4. Spider (Concurrent Crawl)

```python
from scrapling.spiders import Spider, Response

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]
    concurrent_requests = 10

    async def parse(self, response: Response):
        for quote in response.css('.quote'):
            yield {
                "text": quote.css('.text::text').get(),
                "author": quote.css('.author::text').get(),
            }
        next_page = response.css('.next a')
        if next_page:
            yield response.follow(next_page[0].attrib['href'])

result = QuotesSpider().start()
print(f"Scraped {len(result.items)} items")
result.items.to_json("quotes.json")
```

### 5. Async Stealth Session

```python
import asyncio
from scrapling.fetchers import AsyncStealthySession

async def main():
    async with AsyncStealthySession(headless=True, max_pages=3) as session:
        tasks = [session.fetch(url) for url in urls]
        results = await asyncio.gather(*tasks)
        for r in results:
            print(r.css('h1::text').get())

asyncio.run(main())
```

## Selection API Cheat Sheet

All fetcher responses support these selection methods:

```python
page.css('.class')                         # CSS selector
page.css('.class::text').getall()          # extract text
page.css('.class::attr(href)').getall()    # extract attribute
page.xpath('//div[@class="quote"]')        # XPath
page.find_all('div', class_='quote')       # BS4-style
page.find_by_text('some text', tag='div')  # text search

# Navigation
el = page.css('.item')[0]
el.parent                                  # parent element
el.next_sibling                            # next sibling
el.find_similar()                          # similar elements
el.below_elements()                        # elements below
```

## Adaptive Parsing

Track elements across site redesigns:

```python
StealthyFetcher.adaptive = True

# First run — save element signatures
products = page.css('.product', auto_save=True)

# Later — site layout changed, relocate elements
products = page.css('.product', adaptive=True)
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: curl_cffi` | Missing fetcher deps | `pip install "scrapling[fetchers]"` |
| `BrowserNotInstalledError` | No browser binaries | `scrapling install` |
| `TimeoutError` on StealthyFetcher | Page too slow / blocked | Increase `timeout`, add `network_idle=True` |
| `ConnectionError` with proxy | Bad proxy | Check proxy format: `"http://user:pass@host:port"` |
| Empty results from `.css()` | Wrong selector or JS-rendered | Switch to `DynamicFetcher` or `StealthyFetcher` |

## Detailed API Reference

- **Fetchers & Sessions**: See [references/fetchers-api.md](references/fetchers-api.md) for all fetcher classes, session types, and full parameter tables
- **Spiders**: See [references/spiders-api.md](references/spiders-api.md) for Spider class, Request/Response, SessionManager, CrawlResult, streaming
- **Advanced Patterns**: See [references/advanced-patterns.md](references/advanced-patterns.md) for proxy rotation, CLI, MCP server, Docker, multi-session spiders
