# Decision Extraction (Step 3g)

After posting and updating the local DB, evaluate whether the tweet content
warrants a DECISION post using the `decision-router` skill rules.

Skip this step entirely if `skip-decisions` flag is set.

## Detection Criteria

- Tweet about a tool/technology with clear adoption-or-not signal for the platform → **team** scope, MEDIUM urgency → post to `#7층-리더방` (`C0A6Q7007N2`)
- Personal tool/workflow adoption signal → **personal** scope, LOW urgency → post to `#효정-의사결정` (`C0ANBST3KDE`)
- Market-moving news requiring portfolio adjustment → **personal** scope, HIGH urgency → post to `#효정-의사결정` (`C0ANBST3KDE`)
- Competitor announcement requiring strategic response → **team** scope, MEDIUM urgency → post to `#7층-리더방` (`C0A6Q7007N2`)

Check primarily Message 3 insights for actionable strategic implications. Only
post when the decision signal is clear and actionable — default to NOT posting.

## DECISION Post Template

```
*[DECISION]* {urgency_badge} | 출처: twitter-timeline-to-slack

*{Decision Title}*

*배경*
{1-3 sentence context from the tweet and research}

*판단 필요 사항*
{What needs to be decided}

*옵션*
A. {option A} — {pro/con}
B. {option B} — {pro/con}
C. 보류 / 추가 조사 필요

*추천*
{recommended option with rationale}

*긴급도*: {HIGH / MEDIUM / LOW}
*원본*: <{original_tweet_url}|{tweet summary}>
```

## Decision Channels

| Channel | ID | Scope |
|---|---|---|
| `효정-의사결정` | `C0ANBST3KDE` | Personal decisions (tool adoption, portfolio) |
| `7층-리더방` | `C0A6Q7007N2` | Team/CTO decisions (infra, strategy, competitive) |
