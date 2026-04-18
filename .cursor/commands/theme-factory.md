## Theme Factory

Generate complete color palettes, themes, and design tokens from a text prompt. Apply to artifacts, slides, docs, or HTML.

### Usage

```
/theme-factory "calm fintech, trust, dark"     # generate theme from description
/theme-factory --preset corporate              # use a pre-set theme
/theme-factory --apply report.html             # apply theme to an artifact
```

### Workflow

1. **Interpret** — Parse brand description into color psychology and mood
2. **Generate** — Create a complete theme: primary, secondary, accent, neutral, semantic colors
3. **Token** — Output as CSS variables, Tailwind config, or design tokens
4. **Preview** — Render sample components with the generated theme
5. **Apply** — Optionally apply the theme to an existing artifact

### Execution

Read and follow the `anthropic-theme-factory` skill (`.cursor/skills/anthropic/anthropic-theme-factory/SKILL.md`) for 10 pre-set themes with colors/fonts and on-the-fly theme generation.

### Examples

Generate a fintech theme:
```
/theme-factory "professional fintech, blue-grey, dark mode accent"
```

Apply a preset:
```
/theme-factory --preset minimal --apply outputs/report.html
```
