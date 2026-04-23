# Goose Battlecard Generator

Research a specific competitor across their website, reviews, ads, social presence, and pricing — then produce a structured sales battlecard with positioning traps, objection handlers, landmine questions, and win/loss themes. Use when sales needs competitive ammo or when entering a new market with established incumbents.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/battlecard-generator.

## When to Use

- "Generate a competitive battlecard for [competitor]"
- "Build sales battlecard against [company]"
- "경쟁사 배틀카드 생성", "세일즈 배틀카드"
- "Competitive battlecard for the sales team"

## Do NOT Use

- For general competitive analysis without sales focus (use kwp-product-management-competitive-analysis)
- For GTM battlecard with market entry strategy (use pm-go-to-market)
- For Sun Tzu strategic framing (use sun-tzu-analyzer)

## Methodology

### Phase 1: Competitor Website Analysis
- Homepage messaging, positioning, key claims
- Pricing page: tiers, feature gates, price anchoring
- Case studies: customer types, outcomes, industries
- Product pages: features claimed, differentiators

### Phase 2: Review Intelligence
- G2, Capterra, Trustpilot reviews (pros, cons, recurring themes)
- Win themes: what customers love
- Loss themes: what customers complain about
- Feature gaps and wishlist patterns

### Phase 3: Ad & Social Intelligence
- Ad copy and landing pages (Google/Meta/LinkedIn)
- Social presence: content strategy, engagement
- Founder/executive public commentary

### Phase 4: Battlecard Assembly

## Output Format

```markdown
# Battlecard: [Your Product] vs [Competitor]
Generated: [Date]

## Quick Reference
| Dimension | Us | Them |
|-----------|-----|------|
| Pricing | | |
| Key Strength | | |
| Key Weakness | | |

## Positioning Traps
[Questions to ask that lead to your strengths]

## Objection Handlers
| Objection | Response | Proof Point |
|-----------|----------|-------------|

## Landmine Questions
[Questions for prospects to ask the competitor]

## Win/Loss Themes
**Why we win:** [patterns from wins]
**Why we lose:** [patterns from losses]
**At-risk deals:** [when to worry]

## Competitive Proof Points
[Customer quotes, metrics, case studies]
```
