# Scrapling Spiders API Reference

## Spider Class

```python
from scrapling.spiders import Spider, Request, Response

class MySpider(Spider):
    name = "my_spider"
    start_urls = ["https://example.com/"]
    concurrent_requests = 10

    async def parse(self, response: Response):
        for item in response.css('.product'):
            yield {"title": item.css('h2::text').get()}

        next_page = response.css('.next a')
        if next_page:
            yield response.follow(next_page[0].attrib['href'])
```

### Spider Configuration

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | str | required | Spider identifier |
| `start_urls` | list[str] | required | Initial URLs to crawl |
| `concurrent_requests` | int | 5 | Max concurrent requests |
| `download_delay` | float | 0 | Delay between requests (seconds) |
| `robots_txt_obey` | bool | False | Respect robots.txt directives |
| `crawldir` | str | None | Directory for pause/resume checkpoints |

### Starting a Spider

```python
# Basic start
result = MySpider().start()

# With checkpoint directory (enables pause/resume)
result = MySpider(crawldir="./crawl_data").start()

# Access results
print(f"Scraped {len(result.items)} items")
result.items.to_json("output.json")
result.items.to_jsonl("output.jsonl")
```

## Request Object

```python
from scrapling.spiders import Request

# Basic request
yield Request(url, callback=self.parse_detail)

# With session routing
yield Request(url, sid="stealth", callback=self.parse_protected)

# Follow helper (relative URL resolution)
yield response.follow(href)
yield response.follow(href, callback=self.parse_next)
```

| Param | Type | Description |
|-------|------|-------------|
| `url` | str | Target URL |
| `callback` | callable | Async parse method to handle response |
| `sid` | str | Session ID for multi-session spiders |
| `meta` | dict | Pass arbitrary data to callback |

## Response Object

The `Response` object passed to callbacks has the full Scrapling selection API:

```python
async def parse(self, response: Response):
    response.css('.class')
    response.xpath('//div')
    response.find_all('div', class_='x')
    response.find_by_text('text')
    response.url          # current URL
    response.status       # HTTP status code
    response.follow(url)  # resolve relative URL
```

## Multi-Session Spiders

Route requests to different fetcher backends within a single spider:

```python
from scrapling.spiders import Spider, Request, Response
from scrapling.fetchers import FetcherSession, AsyncStealthySession

class MultiSessionSpider(Spider):
    name = "multi"
    start_urls = ["https://example.com/"]

    def configure_sessions(self, manager):
        manager.add("fast", FetcherSession(impersonate="chrome"))
        manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)

    async def parse(self, response: Response):
        for link in response.css('a::attr(href)').getall():
            if "protected" in link:
                yield Request(link, sid="stealth")
            else:
                yield Request(link, sid="fast", callback=self.parse)
```

### SessionManager API

| Method | Description |
|--------|-------------|
| `manager.add(id, session, lazy=False)` | Register a session; `lazy=True` defers initialization |
| `sid="<id>"` in Request | Route to that session |

## Pause & Resume (Checkpoint-based)

```python
# Enable persistence
spider = QuotesSpider(crawldir="./crawl_data")
result = spider.start()

# Press Ctrl+C → graceful shutdown, state saved
# Re-run same command → resumes from last checkpoint
```

## Streaming Mode

Stream items as they arrive instead of waiting for crawl completion:

```python
spider = MySpider()

async for item in spider.stream():
    print(item)  # process each item immediately
    # Real-time stats available during stream
```

## CrawlResult

Returned by `spider.start()`:

| Property | Type | Description |
|----------|------|-------------|
| `result.items` | ItemCollection | All yielded dicts |
| `result.items.to_json(path)` | method | Export as JSON |
| `result.items.to_jsonl(path)` | method | Export as JSONL |
| `len(result.items)` | int | Item count |

## Blocked Request Detection

Spiders include automatic detection and retry of blocked requests. Customize logic with:

```python
class MySpider(Spider):
    def is_blocked(self, response: Response) -> bool:
        return response.status == 403 or 'captcha' in response.text
```

## Robots.txt Compliance

```python
class PoliteSpider(Spider):
    robots_txt_obey = True  # Respects Disallow, Crawl-delay, Request-rate
```

## Development Mode (Response Caching)

Cache responses on first run, replay on subsequent runs for faster iteration:

```python
class DevSpider(Spider):
    dev_mode = True  # Cache to disk, replay without hitting servers
```
