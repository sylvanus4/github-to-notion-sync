## Pick Command

Find the right slash command for any task. Indexes 624 commands across 42 categories and recommends the best match.

### Usage

```
/pick                                    # interactive — describe what you need
/pick "코드 리뷰하고 싶어"                   # intent-based command selection
/pick --browse                           # list all categories with counts
/pick --browse trading-finance           # list commands in a specific category
/pick --chain "분석하고 리포트 만들고 슬랙에 올려" # compose a multi-command workflow
```

### Workflow

1. **Load registry** — Read the command index from `command-registry.json`
2. **Detect mode** — Browse (explore categories), Pick (match intent, default), or Chain (compose workflow)
3. **Match** — Score commands by name, description, and argument relevance
4. **Recommend** — Primary pick + alternatives + anti-recommendations
5. **Disambiguate** — Clarify look-alike commands (e.g., `/simplify` vs `/deep-review`)

### Execution

Read and follow the `command-guide` skill (`.cursor/skills/automation/command-guide/SKILL.md`).

### Examples

Find the best command for code review:
```
/pick "코드 리뷰해줘"
```

Explore what trading commands are available:
```
/pick --browse trading-finance
```

Build a full shipping workflow:
```
/pick --chain "리뷰하고 커밋하고 PR까지"
```

Don't know the category — just describe the task:
```
/pick "어제 메일 정리하고 캘린더 확인"
```
