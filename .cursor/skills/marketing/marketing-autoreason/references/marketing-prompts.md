# Marketing extensions to core autoreason prompts

Apply these bullets **in addition** to `automation/autoreason/references/prompts.md`.

## Critic addendum

Append to critic system prompt:

```
Marketing-specific rules:
- Call out "category boilerplate" that any vendor in this space could say.
- If knowledge_context includes past subject lines or CTR/open-rate bands, compare tone/pattern to winners vs losers when relevant.
- Do not invent benchmarks. If no stats exist, say "no performance data supplied" once and proceed with qualitative critique.
```

## Author B addendum

```
Marketing-specific rules:
- Lead with the strongest differentiated claim allowed by knowledge_context.
- If the format is headlines/subjects, stay within character limits in task_spec.
- Avoid fake urgency unless task_spec allows it.
```

## Synthesizer addendum

```
Marketing-specific rules:
- Prefer one primary CTA or value hook; demote secondary ideas to supporting bullets.
- If evidence supports a metric, surface it once in the most natural place; never stack redundant stats.
```

## Judge addendum

```
Marketing-specific rules:
- Penalize unsubstantiated numeric superiority claims.
- Reward alignment with brand voice constraints when they appear in the task_spec or rubric.
```
