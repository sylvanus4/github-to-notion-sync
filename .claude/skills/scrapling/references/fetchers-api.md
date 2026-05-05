# Scrapling Fetchers & Sessions API Reference

## Fetcher Classes Overview

| Class | Transport | Use Case |
|-------|-----------|----------|
| `Fetcher` | HTTP (curl_cffi) | Fast requests, TLS fingerprint impersonation |
| `AsyncFetcher` | HTTP async | Same as Fetcher, non-blocking |
| `DynamicFetcher` | Playwright Chromium | JS-rendered pages, full browser automation |
| `StealthyFetcher` | Camoufox (stealth browser) | Anti-bot bypass, Cloudflare Turnstile |

## Session Classes

| Class | Persistence | Pattern |
|-------|-------------|---------|
| `FetcherSession` | Cookies/state across requests | sync context manager (`with`) |
| `AsyncStealthySession` | Browser pool, async tabs | `async with`, multi-page concurrency |
| `AsyncDynamicSession` | Playwright browser reuse | `async with`, pool stats |
| `StealthySession` | Stealth browser reuse | sync `with` |
| `DynamicSession` | Playwright browser reuse | sync `with` |

## Fetcher (HTTP)

```python
from scrapling.fetchers import Fetcher, FetcherSession

# One-off request
page = Fetcher.get(url, stealthy_headers=True)

# With impersonation
page = Fetcher.get(url, impersonate='chrome')
page = Fetcher.get(url, impersonate='firefox135')
```

### Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | str | required | Target URL |
| `impersonate` | str | None | Browser TLS fingerprint to impersonate (e.g. 'chrome', 'firefox135') |
| `stealthy_headers` | bool | False | Use realistic browser headers |
| `http3` | bool | False | Enable HTTP/3 |
| `proxy` | str | None | Proxy URL `"http://user:pass@host:port"` |
| `timeout` | int | 30 | Request timeout in seconds |

### FetcherSession

```python
with FetcherSession(impersonate='chrome') as session:
    page1 = session.get('https://example.com/')
    page2 = session.get('https://example.com/page2')  # cookies persist

# Async-compatible (works in both sync/async contexts)
async with FetcherSession(http3=True) as session:
    page = session.get(url, impersonate='firefox135')
```

## StealthyFetcher (Anti-bot Bypass)

```python
from scrapling.fetchers import StealthyFetcher, StealthySession

# One-off (opens browser, fetches, closes)
page = StealthyFetcher.fetch(url, headless=True, network_idle=True)

# Enable adaptive parsing globally
StealthyFetcher.adaptive = True
page = StealthyFetcher.fetch(url, headless=True)

# Solve Cloudflare
page = StealthyFetcher.fetch(url, solve_cloudflare=True)
```

### Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | str | required | Target URL |
| `headless` | bool | True | Run browser in headless mode |
| `network_idle` | bool | False | Wait for network idle before parsing |
| `solve_cloudflare` | bool | False | Auto-solve Cloudflare Turnstile challenges |
| `google_search` | bool | True | Navigate as if from Google search (referer) |
| `timeout` | int | 30000 | Page load timeout in ms |
| `proxy` | str | None | Proxy URL |

### StealthySession / AsyncStealthySession

```python
# Sync
with StealthySession(headless=True, solve_cloudflare=True) as session:
    page = session.fetch(url, google_search=False)

# Async with tab pool
async with AsyncStealthySession(max_pages=2) as session:
    tasks = [session.fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(session.get_pool_stats())  # {busy: N, free: N, error: N}
```

## DynamicFetcher (Playwright)

```python
from scrapling.fetchers import DynamicFetcher, DynamicSession

# One-off
page = DynamicFetcher.fetch(url, headless=True)

# With options
page = DynamicFetcher.fetch(url,
    headless=True,
    disable_resources=False,
    network_idle=True
)
```

### Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | str | required | Target URL |
| `headless` | bool | True | Headless browser |
| `disable_resources` | bool | True | Block images/CSS/fonts for speed |
| `network_idle` | bool | False | Wait for network idle |
| `load_dom` | bool | True | Wait for DOM content loaded |
| `timeout` | int | 30000 | Page load timeout in ms |
| `proxy` | str | None | Proxy URL |

### DynamicSession / AsyncDynamicSession

```python
with DynamicSession(headless=True, disable_resources=False, network_idle=True) as session:
    page = session.fetch(url, load_dom=False)
    data = page.xpath('//span[@class="text"]/text()').getall()

async with AsyncDynamicSession(max_pages=3) as session:
    results = await asyncio.gather(*[session.fetch(u) for u in urls])
```

## Selection API (Response/Page Object)

All fetchers return a page object with:

```python
# CSS selectors (Scrapy pseudo-elements supported)
page.css('.product')                    # list of elements
page.css('.text::text').get()           # first match text
page.css('.text::text').getall()        # all matches
page.css('a::attr(href)').getall()     # attributes

# XPath
page.xpath('//div[@class="quote"]')
page.xpath('//span/text()').getall()

# BeautifulSoup-style
page.find_all('div', {'class': 'quote'})
page.find_all('div', class_='quote')
page.find_all(class_='quote')

# Text search
page.find_by_text('quote', tag='div')

# Adaptive parsing (survives site redesigns)
products = page.css('.product', auto_save=True)   # save fingerprint
products = page.css('.product', adaptive=True)     # relocate if changed
```

### Element Navigation

```python
element = page.css('.quote')[0]
element.next_sibling
element.parent
element.children
element.find_similar()        # find structurally similar elements
element.below_elements()      # elements below in DOM
```

### Chained Selectors

```python
page.css('.quote').css('.text::text').getall()
page.css('.quote')[0].css('.author::text').get()
```

## Standalone Parser

```python
from scrapling.parser import Selector

page = Selector("<html>...</html>")
# Same API as fetcher results
page.css('.class')
page.xpath('//div')
page.find_all('div', class_='x')
```

## Proxy Configuration

```python
# Per-request proxy
page = Fetcher.get(url, proxy="http://user:pass@host:port")

# ProxyRotator with sessions
from scrapling.fetchers import ProxyRotator

rotator = ProxyRotator([
    "http://proxy1:8080",
    "http://proxy2:8080",
    "http://proxy3:8080",
])

with FetcherSession(proxy_rotator=rotator) as session:
    # Proxies rotate automatically per request
    page = session.get(url)
```
