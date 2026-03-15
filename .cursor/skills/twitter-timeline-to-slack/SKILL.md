---
name: twitter-timeline-to-slack
description: >-
  Fetch the latest tweets from a Twitter/X user's profile, store locally with
  deduplication, classify each tweet by topic, and post to the appropriate Slack
  channel using the x-to-slack pipeline with rate limiting. Supports batch
  processing and resumable posting. Use when the user asks to "fetch tweets
  from timeline", "post timeline to slack", "twitter timeline", "scrape tweets",
  "twitter-timeline-to-slack", or wants to batch-process a user's tweets to
  Slack. Do NOT use for posting a single tweet URL (use x-to-slack). Do NOT use
  for general Slack messaging (use kwp-slack-slack-messaging). Do NOT use for
  Twitter scraping without Slack posting (use scrapling or agent-browser).
  Korean triggers: "타임라인", "트위터 타임라인", "트윗 일괄", "트윗 스크래핑".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
---
# Twitter Timeline to Slack Pipeline

Fetch a user's latest tweets, classify by topic, and post each to the appropriate Slack channel via the x-to-slack skill.

## Input

The user provides:
1. **Twitter screen name** -- e.g. `hjguyhan` or `@hjguyhan`
2. **Options** (optional):
   - `--limit N` -- max tweets to post (default: all unposted)
   - `--dry-run` -- classify without posting
   - `--fetch-only` -- fetch and store only, no posting

## Prerequisites

- `TWITTER_COOKIE` must be set in `.env` (Twitter session cookie for Syndication API)
- Channel DB must exist at `outputs/twitter/slack-channels.json`

## Workflow

### Phase 1: Fetch Tweets

Run the fetch script to collect tweets:

```bash
cd scripts/twitter && node fetch_timeline.js hjguyhan
```

This uses twittxr (Twitter Syndication API wrapper) to fetch up to 100 tweets. Falls back to FxTwitter API for individual tweet enrichment.

### Phase 2: Classify and Route

For each tweet, the classifier analyzes text content against keyword rules and routes to the best Slack channel. See [references/classification-rules.md](references/classification-rules.md) for the full rule set.

| Category | Target Channel |
|----------|----------------|
| AI Coding | `#ai-coding-radar` |
| Prompt Engineering | `#prompt` |
| Research | `#deep-research` |
| Press/News | `#press` |
| Stock/Finance | `#효정-주식` |
| Ideas | `#idea` |
| Insights | `#효정-insight` |
| Tasks | `#효정-할일` |
| Default | `#random` |

### Phase 3: Post via x-to-slack

For each unposted tweet:
1. Fetch enriched data via FxTwitter API
2. Run WebSearch for context (2-3 queries per tweet)
3. Post 3-message Slack thread to the classified channel
4. Update local DB with posting status
5. Wait 10-15 seconds before next post (rate limiting)

### Phase 4: Local Storage

Tweets are stored with deduplication at `outputs/twitter/{screen_name}/tweets.json`. Each tweet tracks: `id`, `url`, `text`, `created_at`, `posted_to_slack`, `slack_channel`, `classified_topic`.

Daily snapshots are archived to `outputs/twitter/{screen_name}/archive/YYYY-MM-DD.json`.

## Running the Pipeline

```bash
cd scripts/twitter

# Full pipeline: fetch + classify + post
node run_pipeline.js

# Fetch only (no Slack posting)
node run_pipeline.js --fetch-only

# Post 5 tweets max
node run_pipeline.js --limit 5

# Dry run (classify but don't post)
node run_pipeline.js --dry-run
```

## Examples

### Example 1: First run

User says: "hjguyhan 타임라인 트윗 100개 슬랙에 올려줘"

Actions:
1. Run `node scripts/twitter/run_pipeline.js`
2. Fetches ~100 tweets from @hjguyhan
3. Classifies each tweet → routes to appropriate channel
4. Posts each via x-to-slack with 12s delay
5. Saves DB with posting status

### Example 2: Re-run with dedup

User says: "twitter-timeline-to-slack 다시 실행해줘"

Actions:
1. Run pipeline again
2. Fetches latest tweets → only new ones added (existing IDs skipped)
3. Only unposted tweets are processed
4. Previously posted tweets are not re-posted

## Error Handling

- **TWITTER_COOKIE missing**: Error message with instructions to set the cookie
- **twittxr API failure**: Log error, continue with existing tweets in DB
- **FxTwitter fetch failure**: Use raw tweet data from twittxr as fallback
- **Slack channel not found**: Skip tweet, log warning
- **Rate limit**: Configurable via `TWEET_POST_DELAY_MS` env var (default: 12000ms)

## Composed Skills

This skill orchestrates:
- **x-to-slack** -- Core tweet → Slack posting pipeline
- **scrapling** or **agent-browser** -- Fallback for tweet fetching if twittxr fails

## File Structure

```
scripts/twitter/
  fetch_timeline.js       # Tweet fetcher (twittxr + FxTwitter fallback)
  classify_tweet.js       # Topic classifier with keyword rules
  run_pipeline.js         # Main orchestration script
  package.json            # Dependencies

outputs/twitter/
  slack-channels.json     # Channel ID registry
  {screen_name}/
    tweets.json           # Main tweet DB with posting status
    archive/              # Daily snapshots
```
