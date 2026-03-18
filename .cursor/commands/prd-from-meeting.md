---
description: Takes a Notion meeting URL, extracts requirements, researches market context, and produces a complete PRD.
argument-hint: "<notion-meeting-url>"
---

# /prd-from-meeting

Orchestrates a full PRD pipeline from a Notion meeting page: extract requirements, research competitive/market context, generate personas and OST, write the PRD, produce DOCX, publish to Notion, and post summary to Slack.

## What This Command Does

Takes a Notion meeting URL as input, extracts requirements and pain points from the meeting content, runs deep research for competitive and market context, generates user personas and Opportunity Solution Trees, and produces a complete Product Requirements Document. The output is published to Notion and summarized in Slack.

## Required Input

- **Notion meeting page URL** — A valid Notion page URL containing meeting notes, requirements, or discovery session content.

## Execution Steps

1. **Read meeting page from Notion** — Fetch the meeting content via Notion MCP or meeting-digest.
2. **Extract requirements and pain points** — Parse meeting notes for explicit requirements, user pain points, and success criteria.
3. **Run parallel-deep-research** — Research competitive landscape and market context for the product area.
4. **Generate user personas** — Invoke pm-market-research to create user personas from extracted requirements.
5. **Build OST** — Invoke pm-product-discovery to create Opportunity Solution Tree.
6. **Write PRD** — Invoke pm-execution to produce structured PRD with problem statement, user stories, requirements, and success metrics.
7. **Generate .docx** — Create professional DOCX via anthropic-docx.
8. **Publish to Notion** — Upload PRD markdown and DOCX metadata via md-to-notion.
9. **Post summary to Slack** — Post main summary to `#효정-할일` with thread replies for key sections.

## Output

- PRD markdown file (local)
- PRD DOCX file (local)
- Notion page(s) with PRD content
- Slack post with summary and links

## Skills Used

- meeting-digest: Extract and structure meeting content
- parallel-deep-research: Competitive and market context
- pm-product-discovery: Opportunity Solution Tree
- pm-market-research: User personas
- pm-execution: PRD writing
- anthropic-docx: DOCX generation
- md-to-notion: Notion publishing

## Example Usage

```
/prd-from-meeting https://notion.so/thakicloud/Discovery-Session-Q2-Product-abc123
/prd-from-meeting <notion-meeting-url>
```
