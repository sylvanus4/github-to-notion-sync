# Goose Messaging A/B Tester & Ad Creative Strategist

Design messaging experiments and ad creative strategies across search, social, and display. Generates variant copy (headlines, CTAs, value props, email subjects), RSA (Responsive Search Ad) 15-headline architectures, Performance Max asset group designs, Meta/TikTok creative frameworks, and provides test hypotheses with decision frameworks. Pure reasoning skill.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/messaging-ab-tester. Ad creative patterns merged from [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) paid-media/paid-media-creative-strategist.

## When to Use

- "Design A/B tests for our landing page headlines"
- "Create messaging variants for email subject lines"
- "메시징 A/B 테스트 설계", "카피 변형 테스트"
- "Which headline should we test?"
- "RSA headline strategy", "write 15 RSA headlines for this campaign"
- "Performance Max asset group creative", "PMax 에셋 그룹 설계"
- "Meta ad creative strategy", "TikTok ad creative concepts"
- "광고 크리에이티브 전략", "RSA 헤드라인 설계", "소셜 광고 크리에이티브"
- "Creative testing framework for paid media"
- "Ad creative audit", "creative fatigue diagnosis"

## Do NOT Use

- For A/B test statistical analysis (use pm-data-analytics)
- For full landing page CRO audit (use marketing-conversion-ops)
- For brand voice enforcement on copy (use kwp-brand-voice-brand-voice-enforcement)
- For PPC account structure and bidding strategy (use paid-media-ppc-strategist)
- For search query analysis (use paid-media-search-query-analyst)
- For full account audit (use paid-media-auditor)
- For paid social campaign architecture (use paid-media-paid-social-strategist)

## Methodology

### Phase 1: Hypothesis Formation
For each element to test:
- **Control:** current version (or best guess if no baseline)
- **Hypothesis:** "Changing [X] to [Y] will increase [metric] because [reason]"
- **Primary metric:** the one number that determines the winner

### Phase 2: Variant Generation
Generate 3-5 variants per test element:
- Each variant tests ONE variable (isolated change)
- Variants span a range: conservative tweak to bold departure
- Each variant has a tag: `descriptive`, `emotional`, `specific`, `contrarian`, `social-proof`

### Phase 3: Test Design
- **Audience split:** equal random split vs segment-targeted
- **Sample size:** minimum for statistical significance (rule of thumb: 1000 impressions per variant for ads, 500 opens per variant for email)
- **Duration:** minimum 7 days or 2 business cycles
- **Confidence threshold:** 95% default

### Phase 4: Decision Framework
- Winner: statistically significant improvement on primary metric
- No winner: extend test, try bolder variants, or accept current
- Surprising loser: investigate qualitative signals before discarding

## Ad Creative Patterns (Paid Media Extension)

### RSA (Responsive Search Ads)
- 15-headline architecture: 5 benefit-led, 3 feature-led, 3 CTA-led, 2 brand, 2 urgency/proof
- Description line strategy: 4 descriptions covering unique value, trust, action, differentiator
- Pin strategy: when to pin (brand safety) vs let Google optimize (performance)
- Ad strength diagnostic: path from "Poor" to "Excellent"

### Performance Max Asset Groups
- Asset group segmentation by product category, audience signal, or funnel stage
- Per-group: 5+ headlines, 5+ long headlines, 5+ descriptions, 15+ images, 5+ videos
- Signal design: custom segments, first-party lists, demographics, in-market interests
- Asset performance rating optimization: replace "Low" performers, amplify "Best"

### Meta/Instagram Creative
- Format selection: single image, carousel, video, collection, instant experience
- Hook-first creative: first 3 seconds must stop the scroll
- UGC-style vs polished production: when each wins
- Dynamic creative optimization (DCO) vs manual creative testing
- Creative concept frameworks: problem-agitate-solve, before/after, testimonial, demo

### TikTok/Short-form Creative
- Native-first: content must look organic, not like an ad
- Trend hijacking: leverage trending sounds, formats, transitions
- Hook patterns: text overlay hooks, visual hooks, audio hooks
- Creator partnership briefing: how to brief creators for ad content
- Creative refresh cadence: every 7-14 days (faster fatigue than Meta)

### Creative Testing Framework
- Concept test (big idea) vs element test (headline, image, CTA)
- Minimum 3 concepts per campaign per month
- Creative fatigue signals: CTR decline 20%+, frequency >4, CPM increase
- Kill criteria: if variant underperforms control by 15% after sufficient data, kill it

## Output

Test plan with hypotheses, variant copy, audience splits, sample size requirements, decision criteria. For ad creative requests, also include: platform-specific asset specifications, creative concept briefs, and testing priority.
