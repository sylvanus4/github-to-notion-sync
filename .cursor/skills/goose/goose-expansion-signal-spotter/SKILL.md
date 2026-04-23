# Goose Expansion Signal Spotter

Identify signals that indicate an existing customer is ready for upsell or expansion — usage pattern changes, team growth, new use cases, feature requests, and engagement spikes. Produces a scored list of expansion-ready accounts with recommended expansion plays. Pure reasoning skill.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/expansion-signal-spotter.

## When to Use

- "Which customers are ready for upsell?"
- "Detect expansion signals in our customer base"
- "확장 시그널 감지", "업셀 준비 고객 식별"
- "Build an expansion playbook"

## Do NOT Use

- For churn risk detection (use goose-churn-risk-detector)
- For new lead prospecting (use kwp-apollo-prospect)
- For pricing strategy (use pm-product-strategy)

## Methodology

### Signal Categories

#### Usage-Based Signals (highest predictive value)
- Approaching plan limits (seats, API calls, storage)
- New feature adoption spike
- Usage frequency increase
- Power user emergence in new departments
- API integration expansion

#### Organization Signals
- Company headcount growth (LinkedIn, press releases)
- New department/team adopting
- New geography/office
- Funding round or acquisition
- New executive hire in relevant function

#### Engagement Signals
- Support ticket increase (more engaged = more questions)
- Feature request pattern (wanting capabilities in next tier)
- Event attendance, webinar participation
- Case study or testimonial willingness
- Community activity increase

#### Competitive Signals
- Evaluating complementary tools (can you bundle?)
- Competitor mentioned in support (defend + expand)
- Industry peer adoption (social proof pressure)

### Scoring Model
Each signal scored on:
- **Strength** (1-5): how predictive of expansion
- **Recency** (1-5): how recent the signal
- **Accessibility** (1-5): can you detect it with existing data?
- **Expansion Score** = (Strength × Recency) + Accessibility bonus

### Expansion Plays
For each signal pattern, a recommended play:
- Trigger event → Outreach template → Recommended offer → Owner

## Output: Expansion Signal Framework with signal definitions, scoring model, and recommended plays per signal pattern
