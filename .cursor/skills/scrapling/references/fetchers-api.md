# Fetchers & Sessions API

## Table of Contents

- [Fetcher / AsyncFetcher](#fetcher--asyncfetcher)
- [StealthyFetcher](#stealthyfetcher)
- [DynamicFetcher](#dynamicfetcher)
- [Session Classes](#session-classes)
- [BaseFetcher Configuration](#basefetcher-configuration)
- [Response Object](#response-object)

---

## Fetcher / AsyncFetcher

Fast HTTP requests with TLS fingerprint impersonation via curl_cffi.

```python
from scrapling.fetchers import Fetcher, AsyncFetcher

# Sync
page = Fetcher.get(url, **kwargs)
page = Fetcher.post(url, data={...}, **kwargs)
page = Fetcher.put(url, **kwargs)
page = Fetcher.delete(url, **kwargs)

# Async
page = await AsyncFetcher.get(url, **kwargs)
```

Key kwargs: `impersonate` (e.g. `'chrome'`, `'firefox135'`), `stealthy_headers` (bool), `proxy`, `timeout`, `follow_redirects`, `verify`, `cookies`, `headers`.

---

## StealthyFetcher

Stealth browser with Cloudflare Turnstile/Interstitial bypass. Uses patchright (patched Playwright).

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch(url, **kwargs)
page = await StealthyFetcher.async_fetch(url, **kwargs)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | — | Target URL |
| `headless` | bool | True | Run browser headless |
| `solve_cloudflare` | bool | False | Auto-solve Cloudflare challenges |
| `network_idle` | bool | False | Wait for network idle (~500ms no requests) |
| `timeout` | int | 30000 | Page load timeout in ms |
| `wait` | int | 0 | Extra wait after load in ms |
| `disable_resources` | bool | False | Block fonts, images, stylesheets |
| `blocked_domains` | set | — | Domains to block (includes subdomains) |
| `useragent` | str | — | Custom User-Agent (auto-generated if omitted) |
| `cookies` | dict | — | Cookies to set |
| `proxy` | str/dict | — | `"http://host:port"` or `{"server": ..., "username": ..., "password": ...}` |
| `page_action` | callable | — | `async def action(page)` — automation after load |
| `wait_selector` | str | — | CSS selector to wait for before returning |
| `wait_selector_state` | str | "attached" | State: `"attached"`, `"visible"`, `"hidden"` |
| `init_script` | str | — | JS file path to inject on page creation |
| `locale` | str | system | Browser locale (e.g. `"en-GB"`) |
| `timezone_id` | str | system | Browser timezone |
| `real_chrome` | bool | False | Use system-installed Chrome |
| `hide_canvas` | bool | False | Canvas fingerprint noise |
| `block_webrtc` | bool | False | Block WebRTC (force proxy) |
| `allow_webgl` | bool | True | Enable WebGL |
| `load_dom` | bool | True | Wait for JS DOM execution |
| `cdp_url` | str | — | Connect to existing CDP session |
| `google_search` | bool | True | Simulate Google Search referer |
| `extra_headers` | dict | — | Additional HTTP headers |
| `user_data_dir` | str | temp | Browser profile directory |
| `extra_flags` | list | — | Additional browser flags |
| `selector_config` | dict | — | Passed to Selector constructor |
| `additional_args` | dict | — | Playwright browser context args (highest priority) |

---

## DynamicFetcher

Playwright-based dynamic page fetching. Alias: `PlayWrightFetcher`.

```python
from scrapling.fetchers import DynamicFetcher

page = DynamicFetcher.fetch(url, **kwargs)
page = await DynamicFetcher.async_fetch(url, **kwargs)
```

Supports the same parameters as StealthyFetcher **except**: `solve_cloudflare`, `hide_canvas`, `block_webrtc`, `allow_webgl`.

---

## Session Classes

Persistent sessions maintain cookies and state across requests.

| Class | Import | Pattern | Use Case |
|-------|--------|---------|----------|
| `FetcherSession` | `scrapling.fetchers` | sync context manager or standalone | HTTP with cookie persistence |
| `StealthySession` | `scrapling.fetchers` | sync context manager | Stealth browser with state |
| `AsyncStealthySession` | `scrapling.fetchers` | async context manager | Async stealth with tab pool |
| `DynamicSession` | `scrapling.fetchers` | sync context manager | Playwright with state |
| `AsyncDynamicSession` | `scrapling.fetchers` | async context manager | Async Playwright |

### FetcherSession

```python
from scrapling.fetchers import FetcherSession

# Sync context manager
with FetcherSession(impersonate='chrome') as session:
    page1 = session.get(url1, stealthy_headers=True)
    page2 = session.post(url2, data={...})

# Also works in async
async with FetcherSession(http3=True) as session:
    page = session.get(url)
```

Constructor kwargs: `impersonate`, `http3`, `proxy`, `timeout`, `follow_redirects`, `verify`.

### StealthySession / AsyncStealthySession

```python
from scrapling.fetchers import StealthySession, AsyncStealthySession

# Sync — single browser, sequential fetches
with StealthySession(headless=True, solve_cloudflare=True) as session:
    page = session.fetch(url)

# Async — browser tab pool for concurrent fetches
async with AsyncStealthySession(headless=True, max_pages=5) as session:
    tasks = [session.fetch(u) for u in urls]
    results = await asyncio.gather(*tasks)
    print(session.get_pool_stats())  # {"busy": 0, "free": 5, "error": 0}
```

Constructor takes same kwargs as StealthyFetcher (minus `url`). `max_pages` controls tab pool size for async.

### DynamicSession / AsyncDynamicSession

Same pattern as Stealth sessions but without anti-bot features.

```python
from scrapling.fetchers import DynamicSession, AsyncDynamicSession

with DynamicSession(headless=True, network_idle=True) as session:
    page = session.fetch(url, load_dom=False)

async with AsyncDynamicSession(max_pages=3) as session:
    results = await asyncio.gather(*[session.fetch(u) for u in urls])
```

---

## BaseFetcher Configuration

All fetcher classes inherit configurable class attributes:

```python
from scrapling.fetchers import StealthyFetcher

StealthyFetcher.adaptive = True           # enable adaptive element tracking
StealthyFetcher.huge_tree = True           # allow large DOM trees (default)
StealthyFetcher.keep_cdata = False         # keep CDATA sections
StealthyFetcher.keep_comments = False      # keep HTML comments

# Or configure multiple at once
StealthyFetcher.configure(adaptive=True, huge_tree=False)
StealthyFetcher.display_config()           # print current config
```

| Attribute | Default | Description |
|-----------|---------|-------------|
| `adaptive` | False | Enable adaptive element relocation |
| `huge_tree` | True | Allow large DOM trees |
| `storage` | SQLiteStorageSystem | Backend for adaptive data |
| `keep_cdata` | False | Preserve CDATA sections |
| `keep_comments` | False | Preserve HTML comments |
| `storage_args` | None | Storage configuration |
| `adaptive_domain` | "" | Domain scope for adaptive matching |

---

## Response Object

All fetchers return a `Response` that extends `Selector`:

| Property | Type | Description |
|----------|------|-------------|
| `url` | str | Final URL (after redirects) |
| `status` | int | HTTP status code |
| `reason` | str | HTTP reason phrase |
| `cookies` | tuple/dict | Response cookies |
| `headers` | dict | Response headers |
| `request_headers` | dict | Sent request headers |
| `body` | bytes | Raw response body |
| `meta` | dict | Custom metadata (spider use) |

### Selection Methods (inherited from Selector)

```python
page.css('.selector')                        # -> list of elements
page.css('.selector::text').get()            # -> first match text
page.css('.selector::text').getall()         # -> all match texts
page.css('.selector::attr(href)').getall()   # -> attribute values
page.xpath('//div[@class="x"]')             # -> XPath selection
page.find_all('div', class_='x')            # -> BS4-style
page.find_by_text('text', tag='div')         # -> text content search
page.find_by_regex(r'pattern', tag='span')   # -> regex search
```

### Navigation Methods

```python
el = page.css('.item')[0]
el.parent                    # parent element
el.children                  # child elements
el.next_sibling              # next sibling
el.previous_sibling          # previous sibling
el.find_similar()            # elements with similar structure
el.below_elements()          # elements below this one
el.generate_css_selector()   # auto-generate CSS selector
el.generate_xpath()          # auto-generate XPath
```

### Direct Parsing (no fetch)

```python
from scrapling.parser import Selector

page = Selector("<html><body><h1>Hello</h1></body></html>")
title = page.css('h1::text').get()  # "Hello"
```
