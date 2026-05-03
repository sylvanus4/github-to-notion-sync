---
name: skill-optimizer
description: Audit, evaluate, benchmark, and fitness-score existing SKILL.md files for quality assurance.
disable-model-invocation: true
arguments: [skill_path]
---

Audit the skill at `$skill_path`.

## Audit Dimensions

1. **Trigger Accuracy**: Does the description match actual use cases?
2. **Boundary Clarity**: Are DO/DO NOT use cases well-defined?
3. **Structure**: YAML frontmatter completeness, Markdown body quality
4. **Conciseness**: Is SKILL.md under 500 lines? Is there bloat?
5. **Overlap Detection**: Does it conflict with other installed skills?
6. **Output Quality**: Is the output format well-specified?
7. **Testability**: Can the skill be verified with a test invocation?

## Scoring

Each dimension scored 1-10 with one-line justification.
Composite score = weighted average (trigger accuracy: 2x weight).

## Output

```markdown
## Skill Audit: [skill_name]

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Trigger Accuracy | X/10 | ... |
| ... | ... | ... |

### Composite Score: X/10 (Grade: A-F)

### Recommendations
[Prioritized improvements]

### Overlap Warnings
[Skills with similar triggers]
```

## Rules

- Compare against all installed skills for overlap
- Flag skills with description > 200 words as verbose
- Check for `disable-model-invocation` on side-effect skills
