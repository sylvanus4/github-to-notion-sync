# Scrapling Advanced Patterns Reference

## Proxy Rotation

### ProxyRotator

```python
from scrapling.fetchers import ProxyRotator, FetcherSession

rotator = ProxyRotator([
    "http://user:pass@proxy1:8080",
    "http://user:pass@proxy2:8080",
    "http://user:pass@proxy3:8080",
])

# With HTTP fetcher
with FetcherSession(proxy_rotator=rotator) as session:
    for url in urls:
        page = session.get(url)  # proxy cycles automatically
```

### Per-request Proxy Override

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get(url, proxy="http://specific-proxy:8080")
```

### Proxy in Spiders

```python
from scrapling.spiders import Spider, Request

class ProxiedSpider(Spider):
    name = "proxied"
    start_urls = ["https://example.com/"]

    def configure_sessions(self, manager):
        manager.add("default", FetcherSession(proxy_rotator=rotator))
```

## DNS Leak Prevention

Route DNS queries through Cloudflare's DNS-over-HTTPS to prevent DNS leaks when using proxies:

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch(url, dns_over_https=True)
```

## Domain & Ad Blocking

Block requests to specific domains or enable built-in ad blocking (~3,500 known ad/tracker domains) in browser-based fetchers:

```python
from scrapling.fetchers import DynamicFetcher

# Block specific domains
page = DynamicFetcher.fetch(url, block_domains=["ads.example.com", "tracker.io"])

# Enable built-in ad blocking
page = DynamicFetcher.fetch(url, block_ads=True)
```

## CLI (Command-Line Interface)

### Interactive Shell

```bash
# Launch IPython shell with Scrapling integration
scrapling shell
```

Features:
- Pre-imported Scrapling classes
- Shortcuts for common operations
- Convert curl requests to Scrapling code
- View results in browser

### Extract Command

Extract content directly from terminal without code:

```bash
# Extract body content as Markdown
scrapling extract get 'https://example.com' content.md

# Extract as plain text
scrapling extract get 'https://example.com' content.txt

# With CSS selector and impersonation
scrapling extract get 'https://example.com' content.txt \
  --css-selector '#fromSkipToProducts' \
  --impersonate 'chrome'

# Using DynamicFetcher (browser)
scrapling extract fetch 'https://example.com' content.md \
  --css-selector '#main' \
  --no-headless

# Using StealthyFetcher (anti-bot)
scrapling extract stealthy-fetch 'https://nopecha.com/demo/cloudflare' result.html \
  --css-selector '#padded_content a' \
  --solve-cloudflare
```

### Output Formats

| Extension | Content |
|-----------|---------|
| `.txt` | Plain text (text content only) |
| `.md` | Markdown representation |
| `.html` | Raw HTML |

### Extract Subcommands

| Subcommand | Fetcher Used |
|------------|-------------|
| `get` | `Fetcher` (HTTP only) |
| `fetch` | `DynamicFetcher` (Playwright) |
| `stealthy-fetch` | `StealthyFetcher` (anti-bot) |

## MCP Server (AI Integration)

Built-in Model Context Protocol server for AI-assisted web scraping:

```bash
# Install MCP dependencies
pip install "scrapling[ai]"

# Run MCP server (for Claude, Cursor, etc.)
scrapling mcp
```

### MCP Capabilities

- Extract targeted content before passing to AI (reduces token usage)
- Structured data extraction via natural language
- AI-guided selector generation
- Integrates with Claude Desktop, Cursor IDE

### Configuration (server.json)

The repository includes `server.json` for MCP server configuration compatible with Claude Desktop and other MCP clients.

## Docker

### Pull from DockerHub

```bash
docker pull pyd4vinci/scrapling
```

### Pull from GitHub Container Registry

```bash
docker pull ghcr.io/d4vinci/scrapling:latest
```

The Docker image includes:
- All Python dependencies
- All browser binaries (Chromium, Camoufox)
- System dependencies for browser rendering
- All optional extras (`scrapling[all]`)

### Usage

```bash
docker run -it pyd4vinci/scrapling python3 -c "
from scrapling.fetchers import StealthyFetcher
page = StealthyFetcher.fetch('https://example.com')
print(page.css('title::text').get())
"
```

## Installation Variants

```bash
# Parser only (minimal)
pip install scrapling

# With fetchers (HTTP + browser automation)
pip install "scrapling[fetchers]"
scrapling install           # download browser binaries
scrapling install --force   # force reinstall browsers

# With MCP server
pip install "scrapling[ai]"

# With interactive shell + extract CLI
pip install "scrapling[shell]"

# Everything
pip install "scrapling[all]"
```

### Programmatic Browser Install

```python
from scrapling.cli import install
install([], standalone_mode=False)           # normal
install(["--force"], standalone_mode=False)  # force reinstall
```

## Adaptive Parsing (Element Tracking)

### Save Element Fingerprint

```python
page = StealthyFetcher.fetch(url)
products = page.css('.product', auto_save=True)  # saves element fingerprint
```

### Relocate After Site Redesign

```python
# Later, when site structure changes:
page = StealthyFetcher.fetch(url)
products = page.css('.product', adaptive=True)  # uses saved fingerprint to relocate
```

### Global Adaptive Mode

```python
StealthyFetcher.adaptive = True
# All subsequent .css() calls automatically use adaptive mode
```

## Auto Selector Generation

Generate robust CSS/XPath selectors for any element:

```python
element = page.css('.product')[0]
print(element.generate_css_selector())   # auto-generated robust selector
print(element.generate_xpath())          # auto-generated XPath
```

## Find Similar Elements

```python
first_quote = page.css('.quote')[0]
similar = first_quote.find_similar()      # all structurally similar elements
below = first_quote.below_elements()      # elements below in DOM tree
```

## Requirements

- Python >= 3.10
- For fetchers: `pip install "scrapling[fetchers]"` + `scrapling install`
- For browser-based fetchers: system with display or headless-capable environment
