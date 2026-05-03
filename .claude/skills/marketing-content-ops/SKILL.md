---
name: marketing-content-ops
description: >-
  Expert panel content scoring, quality gate, and editorial brain for
  marketing content. Assembles domain-specific expert panels, scores content
  against rubrics, and iterates to a 90-point quality threshold.
disable-model-invocation: true
---

# Marketing Content Ops

Expert panel content quality system. Assembles 7-10 domain-specific expert panels, scores content against multi-dimensional rubrics, and iterates up to 3 rounds to reach a 90-point quality threshold.

## Triggers

Use when the user asks to:

- "content quality score", "expert panel review", "content quality gate"
- "editorial brain", "content scoring", "quote mining"
- "콘텐츠 품질 평가", "전문가 패널 리뷰", "콘텐츠 점수"
- "content transform", "content rubric", "quality scoring loop"

## Do NOT Use

- For general content creation without quality scoring → use `kwp-marketing-content-creation`
- For brand voice enforcement → use `kwp-brand-voice-brand-voice-enforcement`
- For UX copy generation → use `ux-writing-agent`
- For document quality gate on PRDs/specs → use `doc-quality-gate`

## Prerequisites

- Python 3.10+
- `pip install anthropic openai tiktoken`

## Execution Steps

### Step 1: Intake

Receive content piece (draft, outline, or published) and determine domain (SEO, LinkedIn, newsletter, YouTube, etc.).

### Step 2: Panel Assembly

Select 7-10 experts from `experts/` directory matching the content domain. Available experts: humanizer, instagram, linkedin, newsletter, podcast-quotes, recruiting, seo-strategy, x-articles, youtube-shorts.

### Step 3: Rubric Selection

Choose scoring rubrics from `scoring-rubrics/` — content-quality, conversion-quality, evaluation-quality, strategic-quality, visual-quality.

### Step 4: Scoring Loop (max 3 rounds)

Each expert scores independently. Aggregate to composite score. If < 90, generate improvement brief and re-score. Continue until 90+ or 3 rounds exhausted.

### Step 5: Output

Deliver scored content with expert commentary, improvement suggestions, and final pass/fail status.

### Step 6: Pattern Learning

On approval/rejection, update `references/patterns.md` with learned patterns for future scoring calibration.

## Output

- Scored content with per-expert breakdowns
- Improvement briefs per round
- Final pass/fail with composite score
- Updated pattern library

## Examples

### Example 1: Score a blog post draft

User: "Score this blog post with the content quality rubric"

1. Receive draft, classify domain as "seo-strategy"
2. Assemble panel: seo-strategy, humanizer, newsletter experts
3. Score against content-quality + strategic-quality rubrics
4. Round 1 score: 78/100 → generate improvement brief → rewrite
5. Round 2 score: 92/100 → PASS

Result: Blog post approved with per-expert commentary and improvement log.

### Example 2: Mine quotes from a podcast transcript

User: "Extract the best quotes from this podcast episode for LinkedIn"

1. Run `scripts/quote-mining-engine.py --transcript episode.txt --platform linkedin`

Result: Ranked quotes with context, viral potential score, and suggested post formats.

## Error Handling

| Error | Action |
|-------|--------|
| ANTHROPIC_API_KEY not set | Required for expert panel scoring; set in `.env` |
| Expert file not found | Check `experts/` directory for available expert profiles |
| Score stuck below 90 after 3 rounds | Return FAIL with all round scores and improvement suggestions |
| Content too short for meaningful scoring | Minimum 200 words recommended; flag and ask user to expand |

## Composed Skills

- `kwp-marketing-content-creation` for initial content drafts
- `kwp-marketing-brand-voice` for brand consistency checks
