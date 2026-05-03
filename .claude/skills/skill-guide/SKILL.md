---
name: skill-guide
description: Interactive skill discovery — scan local skills library, match user intent to available skills, suggest skill chains, and provide invocation patterns.
arguments: [intent]
---

Find the best skill(s) for: `$intent`.

## Discovery Process

1. **Scan**: Index all skills in `.cursor/skills/` and `.claude/skills/`
2. **Match**: Score each skill's description/triggers against user intent
3. **Rank**: Present top 5 matches with relevance scores
4. **Chain**: Suggest multi-skill workflows if applicable
5. **Invoke**: Provide copy-paste invocation pattern

## Output

```markdown
## Skill Recommendations for: [intent]

### Best Match
**[skill-name]** (Score: X/10)
- Description: ...
- Invocation: `/skill-name <args>`

### Alternatives
1. [skill-name-2] (Score: X/10)
2. [skill-name-3] (Score: X/10)

### Suggested Chain
1. First run /skill-a
2. Then /skill-b with output from step 1
3. Finally /skill-c
```

## Rules

- Search both Cursor skills and Claude Code skills
- Prefer exact matches over fuzzy
- Suggest chains when intent spans multiple domains
- Include Korean trigger words when available
