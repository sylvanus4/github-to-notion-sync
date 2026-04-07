# Agent-Reach Platform Commands Reference

## Zero-Config Channels (ready after install)

### GitHub

```bash
# Search repos
gh search repos "query" --sort stars --limit 10

# View repo
gh repo view owner/repo

# Search code
gh search code "pattern" --repo owner/repo

# Search issues
gh search issues "query" --repo owner/repo --limit 10

# Read issue
gh issue view 123 --repo owner/repo
```

### YouTube

```bash
# Extract subtitles (no video download)
yt-dlp --write-sub --write-auto-sub --sub-lang en,ko --skip-download -o "/tmp/%(id)s" "URL"

# Get video info as JSON
yt-dlp --dump-json "URL"

# List available subtitles
yt-dlp --list-subs "URL"
```

### Reddit

```bash
# Search posts
rdt search "query" --limit 10

# Read post + comments
rdt read POST_ID

# Browse subreddit
rdt sub SUBREDDIT --limit 10
```

### General Web (Jina Reader)

```bash
# Read any webpage as clean markdown
curl -s "https://r.jina.ai/URL"

# With custom user agent
curl -s -H "User-Agent: agent-reach/1.0" "https://r.jina.ai/URL"
```

### RSS/Atom Feeds

```bash
# Read RSS feed
curl -s "FEED_URL"

# Parse with formatting
agent-reach format rss "FEED_URL"
```

### V2EX

```bash
# Hot topics
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"

# Latest topics
curl -s "https://www.v2ex.com/api/topics/latest.json" -H "User-Agent: agent-reach/1.0"

# Node topics
curl -s "https://www.v2ex.com/api/nodes/show.json?name=python" -H "User-Agent: agent-reach/1.0"
```

### Bilibili

```bash
# Extract subtitles
yt-dlp --write-sub --skip-download -o "/tmp/%(id)s" "https://www.bilibili.com/video/BV..."

# Get video info
yt-dlp --dump-json "https://www.bilibili.com/video/BV..."

# Search (via Bilibili API)
curl -s "https://api.bilibili.com/x/web-interface/search/all/v2?keyword=query"
```

## Cookie-Required Channels

### Twitter/X (requires TWITTER_COOKIE)

```bash
# Search tweets
twitter search "query" --limit 10
twitter search "query" --filter="#hashtag" --limit 20

# Read specific tweet
twitter read TWEET_ID

# Read user timeline
twitter timeline USERNAME --limit 20
```

### Xiaohongshu (requires XHS_COOKIE)

```bash
# Read note
xhs-cli read "https://www.xiaohongshu.com/explore/..."

# Search notes
xhs-cli search "query" --limit 10
```

### Weibo (requires WEIBO_COOKIE)

```bash
# Read post
weibo read POST_ID

# Search
weibo search "query" --limit 10

# Hot search
weibo hot
```

## MCP-Based Channels

### Exa Search (requires mcporter + Exa config)

```bash
# Web search
mcporter call 'exa.web_search_exa(query: "query", numResults: 5)'

# Search with content
mcporter call 'exa.web_search_exa(query: "query", numResults: 5, text: true)'

# Find similar pages
mcporter call 'exa.find_similar(url: "https://example.com", numResults: 5)'
```

## Output Formatting

```bash
# Format output for readability
agent-reach format {platform} {raw_output}

# Supported formats: json, markdown, plain
agent-reach format --output markdown {data}
```

## Health Check

```bash
# Check all channels
agent-reach doctor

# Check specific channel
agent-reach doctor --channel twitter
```
