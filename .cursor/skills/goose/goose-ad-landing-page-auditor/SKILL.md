# Goose Ad-to-Landing Page Auditor

Audit the message match between ad copy and landing pages. Checks for headline consistency, CTA alignment, promise fulfillment, trust signals, and conversion friction. Produces a scorecard with specific fix recommendations for improving ad-to-page conversion rates.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/ad-to-landing-page-auditor.

## When to Use

- "Audit our ad-to-landing-page experience"
- "Check message match between our ads and landing pages"
- "광고-랜딩 페이지 일치도 감사", "전환 최적화 감사"
- "Why is our landing page conversion rate low?"

## Do NOT Use

- For full CRO audit without ad context (use marketing-conversion-ops)
- For designing new landing pages (use anthropic-frontend-design)
- For A/B test design on messaging (use goose-messaging-ab-tester)

## Methodology

### Dimension 1: Message Match (0-10)
- Headline continuity: does the landing page headline match the ad promise?
- Keyword scent: are the same terms used in both ad and page?
- Visual consistency: do imagery and tone match expectations set by ad?

### Dimension 2: Promise Fulfillment (0-10)
- Does the landing page deliver on what the ad promised?
- Is the promised offer/content/demo immediately visible?
- Are there unexpected barriers (registration walls, irrelevant content)?

### Dimension 3: CTA Alignment (0-10)
- Does the CTA match the ad's implied next step?
- Is there only one primary CTA? (choice paralysis check)
- Is the CTA above the fold?

### Dimension 4: Trust Signals (0-10)
- Social proof (logos, testimonials, reviews, case studies)
- Security indicators (SSL, privacy policy, trust badges)
- Specificity (concrete numbers vs vague claims)

### Dimension 5: Conversion Friction (0-10)
- Form length and required fields
- Page load speed
- Mobile optimization
- Distraction elements (navigation, competing CTAs)

### Scoring
- **9-10:** Excellent — optimize for marginal gains
- **7-8:** Good — 1-2 fixes could significantly improve conversion
- **5-6:** Needs work — message match or friction issues
- **Below 5:** Critical — likely losing significant conversion

## Output: Ad-to-Landing Page Scorecard with per-dimension scores and prioritized fix recommendations
