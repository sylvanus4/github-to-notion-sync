# Slack Thread Format

## Main Message

```
:satellite: *HF Topic Radar — {DATE}*

Scanned *{TOPIC_COUNT}* topics across models, spaces, and papers.

:fire: *{HOT_COUNT}* HOT items | :sunny: *{WARM_COUNT}* WARM items

*Top highlights:*
{TOPIC_1}: {TOP_ITEM_1} ({SCORE})
{TOPIC_2}: {TOP_ITEM_2} ({SCORE})
{TOPIC_3}: {TOP_ITEM_3} ({SCORE})
```

## Thread Reply — Per Topic

One thread reply per topic with non-empty results:

```
:mag: *{TOPIC_NAME}* — {HOT_COUNT} HOT, {WARM_COUNT} WARM

:fire: *HOT*
1. `{item_id}` ({type}) — score {SCORE}
   {KEY_METRIC} | linked: {LINKED_ITEMS}
   _{INSIGHT}_

2. ...

:sunny: *WARM*
1. `{item_id}` ({type}) — score {SCORE}
   {KEY_METRIC}

_Full report: `output/hf-intelligence/{DATE}-topic-radar.md`_
```

## Thread Reply — Cross-Topic & Insights

```
:link: *Cross-Topic Convergence*
{Items appearing in 2+ topics with explanation}

:bulb: *Actionable Insights*
1. {Recommendation}
2. {Recommendation}
```

## Formatting Rules

- Use `:fire:` for HOT, `:sunny:` for WARM, `:snowflake:` for COOL
- Item IDs in backtick code format
- Scores to 2 decimal places
- Type in parentheses: `(model)`, `(space)`, `(paper)`
- Keep each thread reply under 3000 characters
- If a topic has > 10 items, show top 5 HOT + top 3 WARM only
