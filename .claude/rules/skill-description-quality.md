# Skill Description Quality

When creating or editing SKILL.md frontmatter, enforce these patterns:

## Required Fields

```yaml
description: >-
  [What it does - one sentence, third person].
  Use when [trigger phrases in English and Korean].
  Do NOT use for [anti-patterns] (use [correct-skill]).
```

## Checklist

- Trigger phrases: include both English and Korean keywords
- Anti-triggers: name adjacent skills that handle similar requests
- Max 1024 chars
- First sentence = capability
- "Use when" = discovery triggers
- "Do NOT use for" = disambiguation from related skills

## Hard vs Soft Dependencies

- Hard: skill cannot function without config -> add explicit setup or gate
- Soft: skill improves with config -> mention in prose, don't gate

## Progressive Disclosure

- SKILL.md under 100 lines -> everything inline
- Over 100 lines -> split to REFERENCE.md, EXAMPLES.md
- Over 500 lines -> mandatory split
