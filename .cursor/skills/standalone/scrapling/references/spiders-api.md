# Spiders API

## Table of Contents

- [Spider Class](#spider-class)
- [Request Object](#request-object)
- [Response Object](#response-object)
- [SessionManager](#sessionmanager)
- [CrawlResult & CrawlStats](#crawlresult--crawlstats)
- [Pause / Resume](#pause--resume)
- [Streaming](#streaming)

---

## Spider Class

Scrapy-like async spider with concurrent crawling, multi-session support, and pause/resume.

```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
    name = "my_spider"                       # required
    start_urls = ["https://example.com/"]    # initial URLs
    concurrent_requests = 10                 # max concurrent
    download_delay = 0.5                     # seconds between requests

    async def parse(self, response: Response):
        for item in response.css('.item'):
            yield {"title": item.css('h2::text').get()}

        next_link = response.css('.next a')
        if next_link:
            yield response.follow(next_link[0].attrib['href'])

result = MySpider().start()
```

### Class Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | str | — | Spider name (required) |
| `start_urls` | list[str] | [] | Initial URLs to crawl |
| `allowed_domains` | set[str] | set() | Restrict crawling to these domains |
| `concurrent_requests` | int | 4 | Max concurrent requests |
| `concurrent_requests_per_domain` | int | 0 | Per-domain concurrency (0 = unlimited) |
| `download_delay` | float | 0.0 | Delay between requests (seconds) |
| `max_blocked_retries` | int | 3 | Retries for blocked requests |
| `fp_include_kwargs` | bool | False | Include kwargs in request fingerprint |
| `fp_keep_fragments` | bool | False | Keep URL fragments in fingerprint |
| `fp_include_headers` | bool | False | Include headers in fingerprint |
| `logging_level` | int | DEBUG | Python logging level |
| `log_file` | str/None | None | Log to file |

### Constructor

```python
spider = MySpider(
    crawldir="./crawl_data",   # enable pause/resume (None = disabled)
    interval=300.0,            # checkpoint interval in seconds
)
```

### Overridable Methods

```python
class MySpider(Spider):
    def configure_sessions(self, manager: SessionManager):
        """Register session backends."""
        manager.add("default", FetcherSession(), default=True)
        manager.add("stealth", StealthySession(solve_cloudflare=True))

    async def parse(self, response: Response):
        """Process each response. Yield dicts (items) or Requests."""
        yield {"data": response.css('h1::text').get()}

    def start_requests(self):
        """Override to customize initial requests (default: start_urls)."""
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    async def on_start(self, resuming: bool):
        """Called before crawl starts. resuming=True if resuming from checkpoint."""
        pass

    async def on_close(self):
        """Called after crawl finishes."""
        pass

    async def on_error(self, request, error):
        """Called on per-request error."""
        self.logger.error(f"Error on {request.url}: {error}")

    def on_scraped_item(self, item):
        """Per-item hook. Return None to drop the item."""
        return item

    def is_blocked(self, response):
        """Detect blocked responses. Default: 401, 403, 407, 429, 444, 5xx."""
        return response.status in (401, 403, 407, 429, 444) or response.status >= 500

    def retry_blocked_request(self, request, response):
        """Prepare retry for blocked request. Return modified Request."""
        return request
```

### Execution

```python
# Blocking start
result = MySpider().start(use_uvloop=False)

# Graceful stop
spider = MySpider()
spider.start()   # press Ctrl+C to pause
spider.pause()   # programmatic pause
```

---

## Request Object

```python
from scrapling.spiders import Request

req = Request(
    url="https://example.com/page",
    sid="stealth",                    # session ID (empty = default)
    callback=self.parse_detail,       # handler (None = self.parse)
    priority=10,                      # higher = processed first
    dont_filter=False,                # True = skip dedup
    meta={"category": "books"},       # custom metadata
    **kwargs,                         # passed to session.fetch()
)
```

Properties: `url`, `sid`, `callback`, `priority`, `dont_filter`, `meta`, `domain` (cached).

Methods: `copy()`, `update_fingerprint(include_kwargs, include_headers, keep_fragments)`.

### response.follow()

Create a follow-up Request from a response:

```python
async def parse(self, response: Response):
    yield response.follow(
        url="/next-page",              # relative or absolute
        sid="",                        # inherit from current if empty
        callback=self.parse_next,      # None = self.parse
        priority=None,                 # None = inherit
        dont_filter=False,
        meta=None,
        referer_flow=True,             # set Referer header
        **kwargs,
    )
```

---

## Response Object

Spider `Response` extends `Selector` with request context:

| Property | Type | Description |
|----------|------|-------------|
| `url` | str | Final URL |
| `status` | int | HTTP status code |
| `reason` | str | HTTP reason |
| `cookies` | tuple/dict | Response cookies |
| `headers` | dict | Response headers |
| `request_headers` | dict | Sent headers |
| `body` | bytes | Raw body |
| `meta` | dict | Metadata from Request.meta |
| `request` | Request | Original Request object |

All Selector methods work: `.css()`, `.xpath()`, `.find_all()`, `.find_by_text()`, etc.

---

## SessionManager

Register and manage multiple session backends in a spider:

```python
def configure_sessions(self, manager: SessionManager):
    from scrapling.fetchers import FetcherSession, AsyncStealthySession

    manager.add("fast", FetcherSession(impersonate="chrome"), default=True)
    manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)
```

### Methods

| Method | Description |
|--------|-------------|
| `add(sid, session, default=False, lazy=False)` | Register a session. `lazy=True` defers initialization |
| `remove(sid)` | Remove a session |
| `pop(sid)` | Remove and return a session |
| `get(sid)` | Get a session by ID |

Properties: `default_session_id`, `session_ids`.

Route requests to specific sessions:

```python
async def parse(self, response: Response):
    yield Request("https://protected.com", sid="stealth")
    yield Request("https://fast-site.com", sid="fast")
```

---

## CrawlResult & CrawlStats

### CrawlResult

```python
result = MySpider().start()

result.stats       # CrawlStats object
result.items       # ItemList — scraped items
result.paused      # bool — was crawl paused?
result.completed   # bool — opposite of paused
```

### ItemList

```python
result.items.to_json("output.json", indent=True)   # JSON export
result.items.to_jsonl("output.jsonl")               # JSON Lines export
len(result.items)                                    # item count
```

### CrawlStats

| Field | Type | Description |
|-------|------|-------------|
| `requests_count` | int | Total requests made |
| `concurrent_requests` | int | Configured concurrency |
| `failed_requests_count` | int | Failed requests |
| `offsite_requests_count` | int | Filtered offsite requests |
| `response_bytes` | int | Total bytes received |
| `items_scraped` | int | Items yielded |
| `items_dropped` | int | Items dropped by `on_scraped_item` |
| `blocked_requests_count` | int | Blocked requests detected |
| `elapsed_seconds` | float | Total crawl time |
| `requests_per_second` | float | Throughput |

Also: `custom_stats`, `response_status_count`, `domains_response_bytes`.

---

## Pause / Resume

Enable checkpoint-based persistence by passing `crawldir`:

```python
spider = QuotesSpider(crawldir="./crawl_data")
result = spider.start()  # Ctrl+C to pause gracefully
```

Later, restart with the same `crawldir` to resume:

```python
spider = QuotesSpider(crawldir="./crawl_data")
result = spider.start()  # resumes from checkpoint
```

`interval` (default 300s) controls how often checkpoints are saved.

---

## Streaming

Stream items as they arrive instead of waiting for the full crawl:

```python
import asyncio
from scrapling.spiders import Spider, Response

class MySpider(Spider):
    name = "streamer"
    start_urls = ["https://example.com/"]

    async def parse(self, response: Response):
        for item in response.css('.item'):
            yield {"title": item.css('h2::text').get()}

async def main():
    spider = MySpider()
    async for item in spider.stream():
        print(item)               # process each item immediately
        print(spider.stats)       # live stats during crawl

asyncio.run(main())
```
