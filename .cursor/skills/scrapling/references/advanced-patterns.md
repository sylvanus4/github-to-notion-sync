# Advanced Patterns

## Table of Contents

- [Proxy Rotation](#proxy-rotation)
- [Adaptive Parsing](#adaptive-parsing)
- [Multi-Session Spiders](#multi-session-spiders)
- [CLI Commands](#cli-commands)
- [MCP Server](#mcp-server)
- [Docker](#docker)

---

## Proxy Rotation

Built-in proxy rotation across all session types.

### ProxyRotator

```python
from scrapling.engines.toolbelt import ProxyRotator, cyclic_rotation, is_proxy_error

proxies = [
    "http://proxy1:8080",
    "http://user:pass@proxy2:8080",
    {"server": "http://proxy3:8080", "username": "user", "password": "pass"},
]

rotator = ProxyRotator(proxies, strategy=cyclic_rotation)
proxy = rotator.get_proxy()  # thread-safe, returns next proxy
len(rotator)                 # number of proxies
```

### Custom Rotation Strategy

```python
import random

def random_rotation(proxies, current_index):
    idx = random.randint(0, len(proxies) - 1)
    return proxies[idx], idx

rotator = ProxyRotator(proxies, strategy=random_rotation)
```

### Using with Sessions

```python
from scrapling.fetchers import FetcherSession

with FetcherSession(impersonate='chrome') as session:
    for url in urls:
        proxy = rotator.get_proxy()
        page = session.get(url, proxy=proxy)
```

### Error Detection

```python
from scrapling.engines.toolbelt import is_proxy_error

try:
    page = Fetcher.get(url, proxy=proxy)
except Exception as e:
    if is_proxy_error(e):
        proxy = rotator.get_proxy()  # switch to next proxy
        page = Fetcher.get(url, proxy=proxy)
```

`is_proxy_error` detects: `net::err_proxy`, `connection refused`, `connection reset`, `tunnel failed`, etc.

---

## Adaptive Parsing

Relocate elements after website layout changes using intelligent similarity algorithms.

### Setup

```python
from scrapling.fetchers import Fetcher

Fetcher.adaptive = True  # enable globally
```

### Workflow

```python
# Step 1: First scrape — save element signatures
page = Fetcher.get('https://example.com')
products = page.css('.product-card', auto_save=True)

# Step 2: Later — site redesigned, elements moved
page = Fetcher.get('https://example.com')
products = page.css('.product-card', adaptive=True)  # finds relocated elements
```

### Find Similar Elements

```python
page = Fetcher.get(url)
first_product = page.css('.product')[0]

similar = first_product.find_similar()  # all structurally similar elements
below = first_product.below_elements()  # elements positioned below
```

### Auto Selector Generation

```python
el = page.css('.product')[0]
css = el.generate_css_selector()    # robust CSS selector
xpath = el.generate_xpath()         # robust XPath
```

---

## Multi-Session Spiders

Route requests through different session backends in a single spider:

```python
from scrapling.spiders import Spider, Request, Response
from scrapling.fetchers import FetcherSession, AsyncStealthySession

class HybridSpider(Spider):
    name = "hybrid"
    start_urls = ["https://example.com/"]

    def configure_sessions(self, manager):
        manager.add("fast", FetcherSession(impersonate="chrome"), default=True)
        manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)

    async def parse(self, response: Response):
        for link in response.css('a::attr(href)').getall():
            if "protected" in link:
                yield Request(link, sid="stealth", callback=self.parse_protected)
            else:
                yield Request(link, sid="fast")

    async def parse_protected(self, response: Response):
        yield {"data": response.css('#content').get()}
```

`lazy=True` defers browser initialization until the session is first used.

---

## CLI Commands

### Interactive Shell

```bash
scrapling shell                           # launch IPython shell with Scrapling
scrapling shell -c "Fetcher.get('...')"   # one-off command
scrapling shell -L info                   # set log level
```

### Extract Content

Output format depends on file extension: `.html` (raw HTML), `.md` (Markdown), `.txt` (plain text).

```bash
# HTTP fetchers
scrapling extract get 'https://example.com' output.md
scrapling extract get 'https://example.com' output.txt --css-selector '#content' --impersonate chrome
scrapling extract post 'https://api.com' output.json --headers 'Content-Type: application/json'

# Browser fetchers
scrapling extract fetch 'https://spa.com' output.md --no-headless
scrapling extract stealthy-fetch 'https://cf-site.com' output.html --solve-cloudflare --css-selector '#main'
```

#### Extract Options

| Flag | Description |
|------|-------------|
| `-s`, `--css-selector` | Extract matching elements only |
| `--impersonate` | Browser TLS fingerprint (e.g. `chrome`, `chrome,firefox`) |
| `--proxy` | Proxy URL |
| `--timeout` | Timeout in seconds (default 30) |
| `--cookies` | Cookies string |
| `-H`, `--headers` | Custom headers (repeatable) |
| `--stealthy-headers` / `--no-stealthy-headers` | Use stealth headers |
| `--follow-redirects` / `--no-follow-redirects` | Follow HTTP redirects |
| `--verify` / `--no-verify` | TLS verification |
| `--no-headless` | Show browser window |
| `--solve-cloudflare` | Auto-solve Cloudflare (stealthy-fetch only) |

---

## MCP Server

AI-assisted scraping via Model Context Protocol. Extracts targeted content before passing to AI to reduce token usage.

### Start Server

```bash
# stdio transport (for Claude Desktop, Cursor)
scrapling mcp

# HTTP transport
scrapling mcp --http --host 0.0.0.0 --port 8000
```

### MCP Tools Available

| Tool | Description |
|------|-------------|
| `get` | HTTP GET with browser impersonation |
| `bulk_get` | Async multi-URL GET |
| `fetch` | Dynamic content via Chromium |
| `bulk_fetch` | Async multi-URL dynamic fetch |
| `stealthy_fetch` | Stealth fetch with Cloudflare bypass |
| `bulk_stealthy_fetch` | Async multi-URL stealth fetch |

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "ScraplingServer": {
      "command": "scrapling",
      "args": ["mcp"]
    }
  }
}
```

### Cursor MCP Configuration

Add to Cursor MCP settings:

```json
{
  "mcpServers": {
    "scrapling": {
      "command": "scrapling",
      "args": ["mcp"]
    }
  }
}
```

---

## Docker

Pre-built image with all extras and browsers:

```bash
# From Docker Hub
docker pull pyd4vinci/scrapling

# From GitHub Container Registry
docker pull ghcr.io/d4vinci/scrapling:latest

# Run interactively
docker run -it pyd4vinci/scrapling python -c "
from scrapling.fetchers import Fetcher
page = Fetcher.get('https://example.com')
print(page.css('h1::text').get())
"
```
