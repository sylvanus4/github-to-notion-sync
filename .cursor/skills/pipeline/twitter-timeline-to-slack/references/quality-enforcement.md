# Quality Enforcement Reference

This document defines the mandatory quality standards for every Slack post
produced by the `twitter-timeline-to-slack` skill. Read this when quality
starts drifting mid-session or when processing multiple tweets.

## Why Quality Degrades

The #1 cause of quality degradation is **subagent delegation**. When the main
agent delegates tweet processing to Task tool subagents, those subagents:

1. Do not have the full message templates in their context
2. Do not run proper WebSearch (or run shallow single-query searches)
3. Produce 3-5 line summaries instead of structured, multi-section posts
4. Skip engagement stats formatting, author bio, and reference links
5. Produce generic Message 3 insights instead of topic-specific analysis

The #2 cause is **context window exhaustion** from processing too many tweets
in a single session (>5), causing the agent to abbreviate later tweets.

**Solution**: Process each tweet yourself (no Task tool), max 5 per invocation.

## Complete Quality Gate Checklist

Every posted Slack thread MUST pass ALL items below. Check after each tweet.

### Formatting (ALL Messages)

- [ ] NO decorative emojis anywhere (only ❤️ 🔁 👀 📎 1️⃣ 2️⃣ 3️⃣ + ONE topic emoji in Message 1 title allowed)
- [ ] ALL body text in Korean (English only for proper nouns, technical terms, URLs)
- [ ] Section headers use `*bold*` ONLY — no emojis before/after
- [ ] Only template-defined headers used (no invented headers)
- [ ] No decorative separators (═══, ───, ***)
- [ ] Media uploaded to Slack if tweet has photos/videos (HARD FAILURE if skipped)

### Message 1 (Title Post)

- [ ] Bold Korean title with topic emoji: `*{emoji} {Subject} — {Korean description}*`
- [ ] Empty line after title
- [ ] One-line Korean summary with key features, numbers, or core insight
- [ ] Source URL included
- [ ] NO `>>>` block quote marker (removed)
- [ ] `message_ts` captured for thread replies

### Media Upload

- [ ] If `has_media === true`: media upload attempted via `upload_media_to_slack.js`
- [ ] Upload failure logged but does NOT block Message 2/3

### Message 2 (Detailed Summary)

- [ ] **Author context**: `@handle (Name) — bio/context` (NOT just `@handle`)
- [ ] **Engagement stats**: `❤️ {likes} | 🔁 {retweets} | 👀 {views}` format
- [ ] **Date**: `작성일: {YYYY-MM-DD}`
- [ ] **핵심 내용**: 3+ sentences of substantive analysis with specific details
- [ ] **Quote tweet section** (if FxTwitter data shows a quote): author + summary
- [ ] **추가 조사 결과**: Findings from 2+ WebSearches with specific data points
      (dates, numbers, project names — not generic background)
- [ ] **참고 링크**: 2+ URLs from WebSearch results with descriptive titles
- [ ] **Character count**: Message 2 MUST be ≥ 800 characters

### Message 2 Thread Variant (when `is_thread === true`)

All items above PLUS:
- [ ] `📎 스레드: {N}개 트윗` metadata line
- [ ] `_(루트 트윗 기준)_` after engagement stats
- [ ] `*스레드 전문*` section with all tweets numbered (1️⃣, 2️⃣, ...)
- [ ] 핵심 내용 synthesizes the FULL thread, not just one tweet
- [ ] WebSearch covers topics from across the entire thread

### Message 3 (Insights)

- [ ] Topic-specific heading (e.g., `*AI 코딩 에이전트 인사이트*`, NOT `*인사이트*`)
- [ ] Analytical content tied to the specific topic (NOT generic filler)
- [ ] `*핵심 시사점*` with 3 concrete, specific bullet points
- [ ] `*Action Items*` with 3 actionable next steps
- [ ] **Character count**: Message 3 MUST be ≥ 400 characters

## Character Count Minimums

| Message | Minimum | Red Flag |
|---------|---------|----------|
| Message 2 | 800 chars | < 500 chars = almost certainly shallow |
| Message 3 | 400 chars | < 250 chars = almost certainly generic filler |

If a message falls below these minimums, go back and:
1. Re-run WebSearch with more specific queries
2. Expand the analysis with specific data points, dates, and numbers
3. Add more context from the author's background and the topic's implications

## Formatting Anti-Patterns (QUALITY FAILURE)

These formatting violations have been observed in degraded output. Each is a hard quality failure.

| Pattern | BAD (NEVER do this) | GOOD (ALWAYS do this) |
|---------|---------------------|----------------------|
| Emoji in header | `🔍 *핵심 내용*` | `*핵심 내용*` |
| English header | `💡 Key Insights` | `*핵심 내용*` |
| Decorative emoji | `🚀 Claude 4.5 출시` | `Claude 4.5 출시` |
| English body text | `This is a significant development for the AI industry.` | `AI 산업에 중대한 발전이다.` |
| Mixed language body | `이 모델은 very impressive한 성능을 보여준다.` | `이 모델은 매우 인상적인 성능을 보여준다.` |
| Decorative separators | `═══════════` or `───────` or `***` | (no separators) |
| Invented header | `*📊 Data Analysis*` | Use only template-defined headers |
| Oversized emoji icons | `🔍💡🚀📊🎯✅⚡🔗📌💰🏆` throughout | Only ❤️ 🔁 👀 📎 1️⃣ 2️⃣ 3️⃣ |

**Allowed emojis (exhaustive list)**: ❤️ 🔁 👀 📎 1️⃣ 2️⃣ 3️⃣ — engagement stats and thread numbering only. + ONE topic emoji per Message 1 title (`:robot_face:`, `:books:`, `:mag:`, `:newspaper:`, `:bulb:`, `:chart_with_upwards_trend:`, `:writing_hand:`, `:cloud:`, `:memo:`).

**English exceptions**: Proper nouns (Claude, NVIDIA, ThakiCloud), technical terms without Korean equivalent, URLs, code.

## BAD vs GOOD Output Comparison

### BAD Output (Subagent Quality — NEVER Acceptable)

```
원문 요약 (@username)
개발자가 X를 시도했다는 내용. 조회 약 4만.
```

```
리서치 컨텍스트
일반적인 배경 설명. 별도 검증 필요.
```

**What's wrong:**
- No structured sections (핵심 내용, 추가 조사 결과, 참고 링크)
- No author bio context — just `@username`
- No emoji-formatted engagement stats
- No WebSearch findings — just vague "일반적인 배경 설명"
- No reference URLs
- Total length: ~80 characters (minimum is 800)
- No Message 3 insights at all

### GOOD Output (Expected Quality — ALWAYS Produce This)

See **Example 2** in the main SKILL.md for the complete reference. Key traits:

- Author: `@altryne (Alex Volkov) — @thursdai_pod 호스트, @wandb AI Evangelist`
- Stats: `❤️ 2,240 | 🔁 106 | 👀 373K`
- 핵심 내용: Multi-sentence analysis with specific product names and numbers
- Quote tweet: Full attribution with specific metrics (`53% 단축`, `61% 감소`)
- 추가 조사 결과: 3 bullet points with specific findings from WebSearch
  (framework name, optimization techniques, scale numbers)
- 참고 링크: 3 URLs with descriptive link text
- Message 3: Topic-specific heading, 3 insight bullets, 3 action items
- Total length: ~1,500+ characters for Message 2, ~600+ for Message 3

## Shortcuts That Are NEVER Acceptable

| Shortcut | Why It's Wrong |
|----------|---------------|
| Skipping WebSearch entirely | Core requirement — provides context unavailable in tweet text |
| Single WebSearch query instead of 2-3 | Insufficient depth for meaningful 추가 조사 결과 |
| Using Task tool for tweet processing | Subagents lack templates, quality gates, and search depth |
| Generic Message 3 ("이 콘텐츠는 흥미롭습니다") | Must be topic-specific with concrete implications |
| Omitting engagement stats or author bio | Required structural elements — not optional |
| Processing >5 tweets without re-invocation | Context exhaustion degrades later tweets |
| Copying tweet text without Korean analysis | 핵심 내용 must ADD analytical value, not just translate |
| Skipping media upload when `has_media === true` | Quality gate requirement |
| Using `**double asterisks**` in Slack messages | Slack uses `*single asterisks*` for bold |
| Adding decorative emojis to section headers | Only ❤️ 🔁 👀 📎 1️⃣ 2️⃣ 3️⃣ are allowed — zero others |
| Writing body text in English or mixed Korean-English | All body text must be Korean; English only for proper nouns/terms/URLs |
| Adding decorative separators (═══, ───, ***) | No separators — use bold headers and whitespace for structure |
| Inventing new section headers | Use ONLY template-defined headers (핵심 내용, 추가 조사 결과, etc.) |

## Anti-Delegation Rationale

The `/x-to-slack` skill produces high-quality output because the main agent:
1. Has the full template structure in context
2. Runs 2-3 WebSearches and follows up on interesting findings
3. Formats engagement stats with proper emoji markers
4. Writes analytical Korean summaries, not literal translations
5. Produces topic-specific Message 3 insights with actionable items

When this same workflow is delegated to a subagent via the Task tool:
1. The subagent gets a compressed prompt lacking template details
2. WebSearch is either skipped or produces single shallow queries
3. Output collapses to 3-5 generic lines
4. No quality self-check occurs before the subagent returns

**The quality gap is not fixable by improving subagent prompts.** The
fundamental issue is that subagents operate in a compressed context window
without access to the quality gate, templates, and reference examples.
The only reliable solution is main-agent sequential processing with a
batch limit to prevent context exhaustion.
