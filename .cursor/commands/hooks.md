## Hook Generator

Generate attention-grabbing hooks for multiple contexts: video intros, social media posts, email subject lines, ad copy, article openings, and presentation openers.

### Usage

```
# Video hooks
/hooks "Why most startups fail at pricing" --context video --count 5

# Email subject lines
/hooks "SaaS product launch" --context email --count 5

# LinkedIn post opener
/hooks "AI 에이전트가 주니어 개발자를 대체한다" --context linkedin --count 3

# Multi-context
/hooks "Kubernetes adoption" --context video,email,linkedin
```

### Workflow

1. **Context** — Collect topic, platform/context, audience, desired emotion
2. **Frameworks** — Apply hook frameworks (Curiosity Gap, Contrarian, Data Shock, Story Open, Direct Challenge, Question, Social Proof, Benefit Lead, Controversy, Scarcity)
3. **Generate** — Produce N variants using 3+ different frameworks
4. **Format** — Adapt to platform constraints (character limits, visual cues)
5. **Recommend** — Pick top hook and suggest A/B test pair

### Output

Ranked hook variants with framework labels, psychological mechanism explanations, risk levels, and A/B test recommendations.

### Execution

Read and follow the `hook-generator` skill (`.cursor/skills/standalone/hook-generator/SKILL.md`).
