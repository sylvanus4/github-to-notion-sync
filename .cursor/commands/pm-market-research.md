## PM Market Research

Market research workflows: user personas, market segmentation, customer journey mapping, competitive analysis, sentiment analysis, and market sizing (TAM/SAM/SOM).

### Usage

```
<sub-skill> [context]
```

### Sub-Skills

| Sub-Skill | Shorthand | What it does |
|-----------|-----------|--------------|
| user-personas | `personas` | Build 3 personas with JTBD, pains, gains from research data |
| user-segmentation | `segments` | Segment users by behavior, JTBD, and needs |
| market-segments | `market-seg` | Identify 3-5 customer segments with demographics and product fit |
| customer-journey-map | `journey` | Map awareness-to-advocacy journey with touchpoints and pain points |
| competitor-analysis | `competitors` | Analyze 5 competitors: strengths, weaknesses, differentiation |
| sentiment-analysis | `sentiment` | Analyze feedback at scale: sentiment scores, themes, satisfaction |
| market-sizing | `sizing` | TAM/SAM/SOM with top-down and bottom-up approaches |

### Execution

Read and follow the `pm-market-research` skill (`.cursor/skills/pm-market-research/SKILL.md`) for the full workflow, sub-skill selection, and error handling.

### Examples

```bash
# Build personas from survey data
/pm-market-research personas -- create personas from these survey responses

# Map customer journey
/pm-market-research journey -- map the onboarding journey for our SaaS product

# Market sizing
/pm-market-research sizing -- size the market for AI writing tools in the US

# Competitive analysis
/pm-market-research competitors -- analyze top 5 competitors in our space

# Sentiment analysis
/pm-market-research sentiment -- analyze feedback from our NPS survey data
```
