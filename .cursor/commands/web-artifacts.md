## Web Artifacts

Build interactive web applications — dashboards, calculators, tools — from natural language using React, Tailwind, and shadcn/ui.

### Usage

```
/web-artifacts "ROI calculator"                # build from description
/web-artifacts "kanban board"                  # interactive tool
/web-artifacts --complex "multi-tab dashboard" # complex state management
```

### Workflow

1. **Understand** — Parse requirements: data model, interactions, state
2. **Architecture** — Plan component hierarchy and state management
3. **Build** — Generate React + Tailwind + shadcn/ui code
4. **Polish** — Add animations, loading states, error handling
5. **Output** — Self-contained HTML artifact or component files

### Execution

Read and follow the `anthropic-web-artifacts-builder` skill (`.cursor/skills/anthropic/anthropic-web-artifacts-builder/SKILL.md`) for building complex HTML artifacts with React, Tailwind, and shadcn/ui.

### Examples

Build a calculator:
```
/web-artifacts "compound interest calculator with charts"
```

Build a dashboard:
```
/web-artifacts --complex "real-time metrics dashboard with filtering and export"
```
