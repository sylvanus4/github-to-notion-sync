# Slack Message Templates

## Message 1: Main Intelligence Post

```
🎬 *{video_title}*
📺 {youtube_url}

*핵심 요약*
{executive_summary_bullets}

📎 *리소스*
• <{notion_url}|📄 Notion 전체 분석>
• <{expert_drive_url}|🎓 전문가용 슬라이드>
• <{elementary_drive_url}|📚 입문자용 슬라이드>
```

## Message 2: Detailed Analysis (Thread Reply)

```
🔬 *기술 심층 분석*

{technical_sections}

📊 *시장 영향*
{market_implications}

⚖️ *반대 논거 & 한계*
{counter_arguments}
```

## Message 3: Content Kit (Thread Reply)

```
📱 *콘텐츠 키트*

*🐦 트위터 스레드 초안*
{twitter_thread_preview}

*💼 링크드인 포스트 초안*
{linkedin_post_preview}

_전체 리퍼포징 파일: `{repurposed_file_path}`_
```

## Field Substitution Rules

| Field | Source | Fallback |
|-------|--------|----------|
| `{video_title}` | defuddle frontmatter `title` | YouTube page title via WebFetch |
| `{youtube_url}` | User-provided URL | — |
| `{executive_summary_bullets}` | Phase 2c summary.md | First 5 bullets from analysis.md |
| `{notion_url}` | Agent B return value | "Notion 업로드 보류 — 로컬 파일 참조" |
| `{expert_drive_url}` | Agent A return value | "슬라이드 생성 보류" |
| `{elementary_drive_url}` | Agent A return value | "슬라이드 생성 보류" |
| `{technical_sections}` | analysis.md §2 truncated to 2000 chars | summary.md technical bullets |
| `{market_implications}` | analysis.md §3 truncated to 1000 chars | "시장 분석 미포함" |
| `{counter_arguments}` | analysis.md §4 truncated to 800 chars | "반대 논거 미포함" |
| `{twitter_thread_preview}` | repurposed.md Twitter section (first 3 tweets) | "트위터 스레드 미생성" |
| `{linkedin_post_preview}` | repurposed.md LinkedIn section (first 300 chars) | "링크드인 포스트 미생성" |
| `{repurposed_file_path}` | Agent C return value | — |

## Slack mrkdwn Formatting Notes

- Use `*bold*` not `**bold**`
- Use `_italic_` not `*italic*`
- Bullet lists use `•` not `-`
- Links: `<url|display text>`
- Keep each message under 4000 characters (Slack limit)
- If a section exceeds limit, truncate with `…(전체 내용은 Notion 참조)`
