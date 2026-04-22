## UI Enhance

Transform a rough UI description into a structured, Refined Swiss design-system-aligned implementation prompt with exact Tailwind tokens, component patterns, and anti-pattern guardrails.

### Usage

```
/ui-enhance "endpoint list page with status badges"
/ui-enhance "create model form with GPU selector"
/ui-enhance --with-states "training job detail page"
```

### Workflow

1. **Extract** — Parse user intent: component type, data model, actions, edge cases
2. **Inject** — Map every visual element to Refined Swiss design tokens from `design-system.mdc`
3. **Guard** — Verify zero anti-patterns (rounded-md, hard-coded colors, missing a11y, etc.)
4. **Output** — Structured prompt with Layout, Visual Spec, States, Interactions, Accessibility sections

### Execution

Read and follow the `refined-swiss-prompt-enhancer` skill (`.cursor/skills/frontend/refined-swiss-prompt-enhancer/SKILL.md`).

### Options

- `--with-states`: Include loading, empty, error, and permission-denied state specifications
- `--for-figma`: Output formatted for Figma-to-code pipeline input
- `--minimal`: Skip accessibility and interaction sections for quick drafts

### Examples

Enhance a table page description:
```
/ui-enhance "model list page with name, status, created date columns and pagination"
```

Enhance with full state coverage:
```
/ui-enhance --with-states "GPU cluster dashboard with utilization charts and node status cards"
```

Enhance for Figma pipeline:
```
/ui-enhance --for-figma "serverless endpoint creation wizard"
```
