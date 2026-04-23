# Goose Voice of Customer Synthesizer

Pull customer language from reviews, testimonials, support tickets, and sales calls — then extract recurring phrases, emotional triggers, objection patterns, and "jobs to be done" language. Outputs a VoC dictionary that marketers can use to write copy that sounds like the customer, not the company.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/voice-of-customer-synthesizer.

## When to Use

- "Extract voice of customer from reviews"
- "Build a VoC dictionary from customer feedback"
- "고객 목소리 분석", "VoC 사전 생성"
- "What language do our customers use?"

## Do NOT Use

- For quantitative feedback analysis with RICE scoring (use customer-feedback-processor)
- For brand voice guideline generation (use kwp-brand-voice-guideline-generation)
- For customer sentiment scoring (use alphaear-sentiment)

## Methodology

### Phase 1: Source Collection
Gather customer language from:
- G2/Capterra/Trustpilot reviews
- Customer testimonials and case studies
- Support ticket language
- Sales call transcripts / Gong insights
- Social media mentions
- NPS/survey open-text responses

### Phase 2: Language Extraction
For each source, extract:
- **Recurring phrases** — exact words customers use repeatedly
- **Emotional triggers** — words expressing frustration, delight, surprise
- **Before/after language** — how they describe life before vs after your product
- **Objection language** — concerns, hesitations, deal-breakers
- **JTBD expressions** — "I was trying to...", "I needed to...", "I hired [product] to..."

### Phase 3: Pattern Clustering
Group extracted language into themes:
- Pain points (top 5 by frequency)
- Desired outcomes (top 5 by frequency)
- Product descriptors (how they describe you in their words)
- Competitor mentions (what they compare you to)

### Phase 4: VoC Dictionary

## Output Format

```markdown
# Voice of Customer Dictionary: [Product]

## Pain Language
| Theme | Customer Phrases | Frequency |
|-------|-----------------|-----------|

## Outcome Language
| Theme | Customer Phrases | Frequency |
|-------|-----------------|-----------|

## Product Descriptors
[How customers describe you in their own words]

## Objection Patterns
| Objection | Typical Phrasing | Frequency |

## JTBD Expressions
[Exact "I hired this to..." language]

## Copy Recommendations
[Specific suggestions for using VoC in headlines, CTAs, email, ads]
```
