---
name: agent-reach
description: >-
  Route-and-execute access to 17+ internet platforms via CLI tools installed
  by Agent-Reach. Zero API keys for core channels. Cookie-based auth for
  restricted platforms (Twitter/X, Xiaohongshu, Weibo). Serves as both a
  standalone content access tool and a fallback provider when other skills
  encounter
---

# Agent-Reach — Multi-Platform Content Router

Route-and-execute access to 17+ internet platforms via CLI tools installed by Agent-Reach. Zero API keys for core channels. Cookie-based auth for restricted platforms (Twitter/X, Xiaohongshu, Weibo). Serves as both a standalone content access tool and a fallback provider when other skills encounter 403s, paywalls, rate limits, or anti-bot measures.

## Triggers

Use when the user asks to "agent-reach", "read this URL without API", "bypass paywall", "cookie-based scrape", "read tweet without API", "search Reddit", "read Xiaohongshu", "read Bilibili comments", "search the web with Exa", "API 없이 읽어줘", "쿠키 기반 스크래핑", "트위터 읽기", "레딧 검색", "샤오홍슈", "빌리빌리", or any request to access content on a supported platform when primary methods have failed.

## Do NOT Use For

- Simple web fetch that defuddle already handles successfully
- GitHub API operations already covered by `gh` CLI (use `gh` directly)
- YouTube transcription already handled by `transcribee` (unless `transcribee` fails)
- Platforms not in the routing table below
- Live browser interaction or DOM manipulation (use `agent-browser` or `cursor-ide-browser`)

## Platform Routing Table

| Platform | Channel Status | Read Command | Search Command |
|----------|---------------|--------------|----------------|
| **GitHub** | ✅ Zero-config | `gh repo view {owner}/{repo}` | `gh search repos "query" --sort stars --limit 10` |
| **YouTube** | ✅ Zero-config | `yt-dlp --write-sub --skip-download -o "/tmp/%(id)s" "URL"` | N/A (use WebSearch) |
| **Reddit** | ✅ Zero-config | `rdt read {post_id}` | `rdt search "query" --limit 10` |
| **General Web** | ✅ Zero-config | `curl -s "https://r.jina.ai/{URL}"` | N/A |
| **RSS/Atom** | ✅ Zero-config | `curl -s "FEED_URL"` | N/A |
| **V2EX** | ✅ Zero-config | `curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"` | N/A |
| **Bilibili** | ✅ Zero-config | `yt-dlp --write-sub --skip-download "URL"` | Bilibili API |
| **Twitter/X** | ⚠️ Cookie required | `twitter read {tweet_id}` | `twitter search "query" --limit 10` |
| **Xiaohongshu** | ⚠️ Cookie required | `xhs-cli read {url}` | `xhs-cli search "query"` |
| **Weibo** | ⚠️ Cookie required | Weibo CLI | Weibo CLI |
| **Exa Search** | ⚠️ MCP config | N/A | `mcporter call 'exa.web_search_exa(query: "q", numResults: 5)'` |

## Workflow

### Step 0: Health Check (once per session)

```bash
agent-reach doctor
```

Cache the result. Only re-run if a channel command fails unexpectedly.

### Step 1: Classify Intent

Match the user's request or URL against the routing table:

- URL pattern → direct channel routing
- Search intent → platform-specific search command
- General web → Jina Reader fallback

**URL Pattern Matching:**

| URL Pattern | Channel |
|-------------|---------|
| `x.com/*`, `twitter.com/*` | Twitter CLI |
| `reddit.com/*` | `rdt read` |
| `youtube.com/*`, `youtu.be/*` | `yt-dlp` |
| `github.com/*` | `gh` CLI |
| `xiaohongshu.com/*`, `xhslink.com/*` | `xhs-cli` |
| `bilibili.com/*`, `b23.tv/*` | `yt-dlp` |
| `v2ex.com/*` | V2EX API |
| Other URLs | `curl -s "https://r.jina.ai/{URL}"` |

### Step 2: Execute Command

Run the matched command via Shell tool. Capture stdout.

### Step 3: Parse and Return

Return the extracted content as clean text/markdown. Strip ANSI codes if present.

## Fallback Contract

When invoked as a fallback by another skill, use this interface:

```
Intent: "read URL {url}" → URL-pattern-match → execute channel command
Intent: "search {platform} {query}" → platform search command
```

Return markdown content or an error message explaining which channel failed and why.

## Error Handling

| Symptom | Cause | Resolution |
|---------|-------|------------|
| `twitter: command not found` | twitter-cli not installed | Run `agent-reach install --channels=twitter --safe` |
| `Cookie expired` / 403 on Twitter | Session cookie stale | Re-extract cookie from browser: see `references/setup-guide.md` |
| `rdt: command not found` | rdt-cli not installed | `pipx install rdt-cli` |
| `yt-dlp` returns no subtitles | Video has no captions, or JS runtime missing | Check `yt-dlp --js-runtimes node` config |
| `mcporter: command not found` | mcporter not installed | `npm install -g mcporter` |
| Exa search returns nothing | MCP not configured | `mcporter config add exa https://mcp.exa.ai/mcp` |
| Channel consistently failing | Upstream tool broken | Run `agent-reach doctor`, check for updates: `agent-reach check-update` |
| All channels fail for a URL | Network/geo restriction | Fall back to `agent-browser` or `cursor-ide-browser` MCP for full browser rendering |

## Security Notes

- Cookie-based platforms (Twitter, Xiaohongshu, Weibo): use **secondary accounts** to avoid suspension
- Cookies stored locally in `~/.agent-reach/` — never committed to git
- `--safe` flag on install previews changes before applying
- No data leaves the local machine except the HTTP requests to target platforms

## References

- [Setup Guide](references/setup-guide.md) — Installation, cookies, proxy, troubleshooting
- [Platform Commands](references/platform-commands.md) — Full per-platform command reference
