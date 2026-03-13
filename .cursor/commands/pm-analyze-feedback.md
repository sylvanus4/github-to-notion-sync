---
description: Analyze user feedback at scale — sentiment, themes, segment-level insights
argument-hint: "<feedback source: NPS, reviews, support tickets, surveys>"
---

# PM Analyze Feedback

Analyze user feedback at scale: sentiment analysis, theme extraction, and segment-level insights. Supports NPS, reviews, support tickets, and survey responses. Uses pm-market-research skill, sentiment-analysis sub-skill.

## Usage
```
/pm-analyze-feedback Analyze these NPS responses
/pm-analyze-feedback 이 NPS 응답 분석해줘
/pm-analyze-feedback Theme extraction from 500 support tickets
/pm-analyze-feedback 지원 티켓 500건 테마 분석
/pm-analyze-feedback Sentiment of App Store reviews
/pm-analyze-feedback 앱스토어 리뷰 감성 분석
```

## Workflow

### Step 1: Ingest Feedback
- Accept: NPS comments, app/store reviews, support tickets, survey open-ends
- Require: raw text + optional metadata (score, segment, date, product area)
- Handle large volumes: sample if >1000, or process in batches with summary

### Step 2: Sentiment Analysis
- Overall sentiment distribution: positive / neutral / negative
- Sentiment by segment (if metadata provided): e.g., by plan, cohort, product
- Identify sentiment drivers: which topics correlate with negative/positive

### Step 3: Theme Extraction
- Cluster similar feedback into themes (e.g., "pricing," "performance," "missing feature X")
- Frequency: how often each theme appears
- Severity or urgency: combine sentiment + volume for prioritization

### Step 4: Segment-Level Insights
- Compare themes and sentiment across segments (enterprise vs SMB, power vs casual users)
- Identify segment-specific pain points or delights
- Flag themes that span segments (common issues) vs segment-specific

### Step 5: Actionable Summary
- Top 5 themes ranked by impact (frequency × severity)
- Recommended actions: fix, communicate, investigate, deprioritize
- Highlight verbatim quotes for storytelling

## Notes
- For NPS: analyze both promoters and detractors; detractors often have richer feedback
- Support tickets: exclude auto-replies and internal notes
- Use consistent taxonomy for themes to enable trend analysis over time
