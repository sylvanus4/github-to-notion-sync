---
name: slack-post-template
description: Slack message format for Phase 6 distribution to #효정-할일.
---

# Slack Post Template

## Main Message (Channel Post)

Post to `#효정-할일` (`C0AA8NT4T8T`):

```
🔄 스프린트 회고 → GitHub 이슈 변환 완료

📋 {meeting_title}
📊 생성된 이슈: {created_count}개
⚡ 우선순위: P0({p0}) P1({p1}) P2({p2})
📎 프로젝트: <https://github.com/orgs/ThakiCloud/projects/5|ThakiCloud Project #5>
📝 총 스토리 포인트: {total_estimate}pt
```

## Thread Reply 1 — Issue List

```
📌 *생성된 이슈 목록*

{for each issue:}
• <{issue_url}|#{issue_number}>: {title} ({priority}, {size})
{end for}
```

## Thread Reply 2 — Quality Report

```
🔍 *품질 검사 결과*

• 총 항목: {total_items} | 통과: {passed} | 보완: {rewritten} | 병합: {merged}
• 평균 품질 점수: {average_score}/5.0
{if gap_warnings_count > 0:}
• ⚠️ 갭 경고: {gap_warnings_count}건 — 커버되지 않은 논의 주제 있음
{else:}
• ✅ 모든 논의 주제 커버 완료
{end if}
```

## Formatting Rules

1. Use Slack mrkdwn syntax (not markdown): `*bold*`, `_italic_`, `<url|text>`.
2. Do NOT use raw `---` horizontal rules (Slack block validation failure).
3. Keep each thread reply under 3000 characters.
4. Use bullet `•` (Unicode) instead of `-` for list items.
5. Thread replies use `slack_send_message` with `thread_ts` from the main message.
6. Channel ID `C0AA8NT4T8T` maps to `#효정-할일`.
