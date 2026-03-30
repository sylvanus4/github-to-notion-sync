# FxTwitter API Reference

## Response Structure

```json
{
  "code": 200,
  "message": "OK",
  "tweet": {
    "id": "...",
    "url": "https://twitter.com/...",
    "text": "tweet content",
    "author": {
      "name": "Display Name",
      "screen_name": "handle",
      "avatar_url": "..."
    },
    "replies": 0,
    "retweets": 0,
    "likes": 0,
    "views": 0,
    "created_at": "...",
    "lang": "en",
    "media": { "photos": [], "videos": [] },
    "quote": null
  }
}
```

## Fields to Extract

| Field | Path | Usage |
|-------|------|-------|
| Tweet text | `tweet.text` | Main content for summary |
| Author name | `tweet.author.name` | Display name |
| Author handle | `tweet.author.screen_name` | @mention |
| Likes | `tweet.likes` | Engagement metrics |
| Retweets | `tweet.retweets` | Engagement metrics |
| Views | `tweet.views` | Engagement metrics |
| URL | `tweet.url` | Original tweet link |
| Quote tweet | `tweet.quote` | Quoted tweet object (same structure) |
| Media | `tweet.media` | Photos and videos arrays |
| Created at | `tweet.created_at` | Timestamp |

## Error Codes

| Code | Message | Meaning |
|------|---------|---------|
| 200 | OK | Success |
| 401 | PRIVATE_TWEET | Tweet is from a private account |
| 404 | NOT_FOUND | Tweet does not exist or was deleted |
| 500 | API_FAIL | FxTwitter service error |

## URL Conversion

| Original domain | API domain |
|---|---|
| `x.com` | `api.fxtwitter.com` |
| `twitter.com` | `api.fxtwitter.com` |

Example: `https://x.com/elonmusk/status/123` becomes `https://api.fxtwitter.com/elonmusk/status/123`
