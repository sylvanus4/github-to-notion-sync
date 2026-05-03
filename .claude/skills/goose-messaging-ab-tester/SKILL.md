---
name: goose-messaging-ab-tester
description: >-
  Design messaging experiments by generating variant copy (headlines, CTAs,
  value props, email subjects), defining test hypotheses, specifying audience
  splits, and providing a decision framework for declaring winners. Pure
  reasoning skill — generates the experiment design, not the test
  infrastructure.
---

# Goose Messaging A/B Tester

Design messaging experiments by generating variant copy (headlines, CTAs, value props, email subjects), defining test hypotheses, specifying audience splits, and providing a decision framework for declaring winners. Pure reasoning skill — generates the experiment design, not the test infrastructure.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/messaging-ab-tester.

## When to Use

- "Design A/B tests for our landing page headlines"
- "Create messaging variants for email subject lines"
- "메시징 A/B 테스트 설계", "카피 변형 테스트"
- "Which headline should we test?"

## Do NOT Use

- For A/B test statistical analysis (use pm-data-analytics)
- For full landing page CRO audit (use marketing-conversion-ops)
- For brand voice enforcement on copy (use kwp-brand-voice-brand-voice-enforcement)

## Methodology

### Phase 1: Hypothesis Formation
For each element to test:
- **Control:** current version (or best guess if no baseline)
- **Hypothesis:** "Changing [X] to [Y] will increase [metric] because [reason]"
- **Primary metric:** the one number that determines the winner

### Phase 2: Variant Generation
Generate 3-5 variants per test element:
- Each variant tests ONE variable (isolated change)
- Variants span a range: conservative tweak → bold departure
- Each variant has a tag: `descriptive`, `emotional`, `specific`, `contrarian`, `social-proof`

### Phase 3: Test Design
- **Audience split:** equal random split vs segment-targeted
- **Sample size:** minimum for statistical significance (use rule of thumb: 1000 impressions per variant for ads, 500 opens per variant for email)
- **Duration:** minimum 7 days or 2 business cycles
- **Confidence threshold:** 95% default

### Phase 4: Decision Framework
- Winner: statistically significant improvement on primary metric
- No winner: extend test, try bolder variants, or accept current
- Surprising loser: investigate qualitative signals before discarding

## Output: Test plan with hypotheses, variant copy, audience splits, sample size requirements, and decision criteria
