---
name: goose-review-intelligence-digest
description: >-
  Scrape and analyze G2, Capterra, Trustpilot, and app store reviews for any
  product (yours or a competitor's). Extract themes, sentiment distribution,
  feature requests, recurring complaints, and competitive switching signals.
  Outputs a structured review digest with actionable insights.
---

# Goose Review Intelligence Digest

Scrape and analyze G2, Capterra, Trustpilot, and app store reviews for any product (yours or a competitor's). Extract themes, sentiment distribution, feature requests, recurring complaints, and competitive switching signals. Outputs a structured review digest with actionable insights.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/review-intelligence-digest.

## When to Use

- "Analyze reviews for [product]"
- "What are customers saying about [competitor] on G2?"
- "리뷰 인텔리전스 분석", "G2/Capterra 리뷰 분석"
- "Review sentiment analysis for our product"

## Do NOT Use

- For voice-of-customer dictionary (use goose-voice-of-customer-synthesizer)
- For general customer feedback pipeline with RICE (use customer-feedback-processor)
- For financial sentiment analysis (use alphaear-sentiment)

## Methodology

### Phase 1: Review Collection
- Search G2, Capterra, Trustpilot for the target product
- Extract review text, rating, date, reviewer role/company size
- Aim for 50-100 recent reviews for statistical relevance

### Phase 2: Theme Extraction
Categorize each review into themes:
- **Praise themes** — what do happy customers love?
- **Complaint themes** — what do unhappy customers hate?
- **Feature requests** — what's missing that customers want?
- **Comparison mentions** — competitors named in reviews
- **Switching signals** — "we switched from..." or "considering switching to..."

### Phase 3: Sentiment Distribution
- Overall sentiment score (positive/neutral/negative ratio)
- Sentiment by theme (which areas are strong vs weak)
- Sentiment trend over time (improving or declining)
- Rating distribution (1-5 stars breakdown)

### Phase 4: Competitive Intelligence
- Which competitors are mentioned most?
- Why do customers switch TO this product?
- Why do customers switch FROM this product?
- Feature comparison through customer lens

## Output: Review Intelligence Digest with theme analysis, sentiment scores, feature request rankings, and competitive switching patterns
