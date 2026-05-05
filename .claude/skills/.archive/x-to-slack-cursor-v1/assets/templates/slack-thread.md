# X-to-Slack Thread Template

Three-message thread structure for posting tweet intelligence to Slack.

> **FORMATTING CONSTRAINTS (MANDATORY — violation = quality failure)**
> - NO decorative emojis in headers or body. ALLOWED: ❤️ 🔁 👀 📎 1️⃣ 2️⃣ 3️⃣ (engagement/thread numbering only) + ONE topic emoji per Message 1 title line.
> - ALL body text in Korean (English only for proper nouns, technical terms, URLs, code).
> - Section headers = `*bold text*` only, no emojis before/after.
> - Use ONLY headers defined in templates below. Do NOT invent new ones.
> - No decorative separators (═══, ───, ***).
> - Media upload MANDATORY if tweet has photos/videos — use `scripts/slack_upload_file.py` (NOT URL unfurling).

## Message 1: Title (Channel Post)

Message 1 is EXACTLY 2 lines — a Korean headline and the URL. Nothing else.

```
{Korean headline — one sentence summarizing the core insight or news, NO emojis, NO bold}
{source URL}
```

Capture `message_ts` from the response for thread replies and media uploads.

### Media Upload (after Message 1)

If the tweet has photos or videos, upload them to the thread immediately after Message 1:

```bash
# Single media
python3 scripts/slack_upload_file.py \
    --url "{media_url}" --channel {channel_id} --thread-ts "{message_ts}"

# Multiple media (batch)
python3 scripts/slack_upload_file.py \
    --urls "{url_1}" "{url_2}" --channel {channel_id} --thread-ts "{message_ts}"
```

Media URLs come from FxTwitter: `tweet.media.photos[].url` or `tweet.media.videos[].url`.

### Message 1 Strict Rules

**MUST contain ONLY:** one Korean headline sentence + source URL (2 lines total).

**MUST NOT contain (QUALITY FAILURE if present):**
- Author info (@username, name, bio, follower count)
- Engagement stats (likes, retweets, views, bookmarks)
- "원문 보기" link text
- Flag emojis (🇮🇹 🇺🇸 🇰🇷 etc.)
- Decorative emojis (🧠 👤 🔗 📝 🔍 💡 🚀 📊 🎯 ✅ ⚡ 📌 💰 🏆)
- Topic emojis in the text
- Bold or italic formatting (`*text*` or `_text_`)
- Multiple description lines
- Bullet points or section headers

**GOOD example:**
```
Claude Code + Obsidian으로 세컨드 브레인 구축하는 완전 가이드 — Karpathy LLM Wiki 기반 지식 관리 시스템
https://x.com/defileo/status/2042241063612502162
```

**BAD example (HARD FAILURE):**
```
🧠 Claude Code + Obsidian = 세컨드 브레인 구축 완전 가이드
👤 @defileo | DeFi & AI 인사이트 크리에이터 (팔로워 41.7K)
🔗 원문 보기
🇮🇹 👀 365만 | ❤️ 5,331 | 🔄 429 | 📝 26,583
```

## Message 2: Detailed Summary (Thread Reply)

```
*Tweet 요약*
- 작성자: @{screen_name} ({name}) — {author bio/description}
- 반응: ❤️ {likes} | 🔁 {retweets} | 👀 {views}
- 작성일: {created_at}

*핵심 내용*
{Tweet 내용을 한국어로 요약 정리. 원문이 영어인 경우 번역 포함.}

{인용 트윗이 있는 경우:}
*인용 트윗 (@{quote.author.screen_name})*
{quote.text 요약}

*추가 조사 결과*
{WebSearch로 수집한 관련 정보를 bullet point로 정리}
- {관련 배경 정보}
- {최근 동향}
- {영향 및 의미}

*참고 링크*
- {검색에서 발견한 관련 URL들}
```

## Message 3: AI GPU Cloud Insights (Thread Reply)

```
*AI GPU Cloud 서비스 인사이트*

{이 트윗 주제가 AI GPU Cloud / AI 플랫폼 서비스에 어떤 의미를 가지는지 분석}

*핵심 시사점*
- {GPU 클라우드 인프라 관점에서의 인사이트}
- {AI 플랫폼 서비스에 미칠 영향}
- {팀이 취해야 할 액션 또는 고려사항}

*적용 가능성*
{구체적으로 우리 서비스에 어떻게 적용하거나 대응할 수 있는지}
```

## Formatting Rules

- `*bold*` (single asterisk only, never `**`)
- `_italic_` (underscore)
- `<url|text>` for links
- No `## headers` — use `*bold text*` on its own line
- Write content in Korean
- Limit each message to under 4000 characters

### Anti-Patterns (QUALITY FAILURE)

| BAD | GOOD |
|-----|------|
| `🔍 *핵심 내용*` | `*핵심 내용*` |
| `💡 Key Insights` | `*핵심 내용*` |
| `🚀 *AI GPU Cloud 서비스 인사이트*` | `*AI GPU Cloud 서비스 인사이트*` |
| English body text | Korean body text (English only for proper nouns, terms, URLs) |
| `═══════════` separators | (no separators) |
| Inventing headers like `*📊 Data Analysis*` | Use only template-defined headers |
