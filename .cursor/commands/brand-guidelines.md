## Brand Guidelines

Enforce brand colors, typography, and visual identity across all components and artifacts.

### Usage

```
/brand-guidelines                      # audit current brand compliance
/brand-guidelines --apply src/         # enforce brand on components
/brand-guidelines --generate           # generate brand guideline document
```

### Workflow

1. **Extract** — Identify current brand tokens: colors, fonts, spacing, logos
2. **Audit** — Check existing components against brand guidelines
3. **Flag** — Report deviations with specific locations and fixes
4. **Apply** — Update components to match brand system
5. **Document** — Generate brand guideline reference document

### Execution

Read and follow the `anthropic-brand-guidelines` skill (`.cursor/skills/anthropic/anthropic-brand-guidelines/SKILL.md`) for applying official brand colors and typography. For custom brand voice enforcement, combine with `kwp-brand-voice-brand-voice-enforcement` (`.cursor/skills/kwp/kwp-brand-voice-brand-voice-enforcement/SKILL.md`).

### Examples

Audit brand compliance:
```
/brand-guidelines
```

Generate guidelines document:
```
/brand-guidelines --generate
```
