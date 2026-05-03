---
name: meeting-digest
description: Analyze meeting content from Notion, transcript, or file — produce structured Korean summaries with action items, upload to Notion, and optionally post to Slack.
disable-model-invocation: true
arguments: [source]
---

Analyze meeting content from `$source` and produce structured output.

## Input Types

- Notion page URL (preferred)
- Raw transcript text
- Local file path (.md, .txt)

## Analysis Pipeline

1. **Extract content**: Fetch from Notion, read file, or parse pasted transcript
2. **Multi-perspective PM analysis**: Apply PM sub-skills for comprehensive review
3. **Structured summary**: Korean summary with decisions, action items, announcements
4. **Notion upload**: Create two sub-pages (summary + action items) under meeting parent
5. **Slack post** (optional): Thread to #효정-할일

## Output Format

```markdown
## 회의 요약
- 일시:
- 참석자:
- 주요 안건:

## 핵심 결정 사항
1. [결정 내용] — 담당: [이름]

## 액션 아이템
- [ ] [항목] — 담당: [이름], 기한: [날짜]

## 주요 논의 내용
[상세 내용]
```

## Rules

- Always upload to Notion as sub-pages
- Action items must have owner and deadline
- Korean output unless explicitly told otherwise
