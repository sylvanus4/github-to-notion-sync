# Reddit Public JSON API Reference

This skill uses Reddit's public `.json` endpoints — no OAuth, no API key, no Reddit account needed.

## How It Works

Append `.json` to any Reddit URL to get a JSON response:

```
https://www.reddit.com/r/{subreddit}/hot.json?limit=10
https://www.reddit.com/r/{subreddit}/top.json?t=week&limit=10
```

## Endpoints Used

### Listing Posts

```
GET https://www.reddit.com/r/{subreddit}/{sort}.json
```

| Parameter | Values | Description |
|-----------|--------|-------------|
| `{sort}` | `hot`, `top`, `new`, `rising` | Sort order |
| `limit` | 1-100 | Posts per request |
| `t` | `hour`, `day`, `week`, `month`, `year`, `all` | Time filter (for `top` sort only) |
| `after` | string | Pagination cursor |

### Post Comments

```
GET https://www.reddit.com/r/{subreddit}/comments/{post_id}.json
```

Returns an array of two listings: `[post_data, comments_data]`.

## Response Structure

### Post Object (simplified)

```json
{
  "data": {
    "children": [
      {
        "data": {
          "id": "abc123",
          "title": "Post title",
          "selftext": "Body text",
          "author": "username",
          "score": 1234,
          "num_comments": 56,
          "subreddit": "korea",
          "created_utc": 1700000000,
          "permalink": "/r/korea/comments/abc123/post_title/"
        }
      }
    ]
  }
}
```

### Comment Object (simplified)

```json
{
  "data": {
    "id": "xyz789",
    "body": "Comment text",
    "author": "commenter",
    "score": 42,
    "depth": 0
  }
}
```

## Rate Limiting

Reddit's public endpoint enforces rate limits:
- ~30 requests per minute per IP without auth
- Returns HTTP 429 with `Retry-After` header when exceeded

### Mitigation

1. The scraper adds a 2-second delay between requests
2. User-Agent header is randomized from a pool of browser strings
3. Cached posts can be reused via `--skip-scrape`
4. If persistently blocked, use `agent-reach` skill's `rdt read "reddit.com/r/{subreddit}"` as a fallback

## Important Notes

- NSFW subreddits require authentication — not supported by this skill
- The `.json` endpoint may serve stale data (cached ~1-2 minutes by Reddit)
- Some posts with deleted content return `[removed]` as the body text
- Reddit may geo-block certain IPs; a VPN may be needed in some regions
