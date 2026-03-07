## Generate Visual Plan

Generate a visual HTML implementation plan — detailed feature specification with state machines, code snippets, and edge cases.

### Usage

```
/generate-visual-plan <feature or extension description>
```

### Workflow

1. **Data gathering** — Parse the feature request, read the relevant codebase, understand extension points, check for prior art
2. **Design** — Work through state design, API design, integration design, and edge cases
3. **Verification checkpoint** — Produce a structured fact sheet: every state variable, function/API signature, file modification, edge case, and assumption. Verify each against the code
4. **Generate HTML** — Create the page with these sections:
   - Header (feature name, description, scope)
   - The Problem (before/after comparison panels)
   - State Machine (Mermaid flowchart with zoom controls)
   - State Variables (card grid with code blocks)
   - Modified Functions (file path + key snippets + explanation)
   - Commands / API (table with parameters and behavior)
   - Edge Cases (table with scenarios and expected behaviors)
   - Test Requirements (grouped by unit/integration/edge case)
   - File References (file-to-change mapping)
   - Implementation Notes (callout boxes for compatibility, warnings, performance)
5. **Deliver** — Write to `~/.agent/diagrams/` with descriptive filename, open in browser

### Execution

Read and follow the `visual-explainer` skill (`.cursor/skills/visual-explainer/SKILL.md`) for workflow, CSS patterns, templates, and quality checks. Use editorial or blueprint aesthetic.

### Examples

New feature plan:
```
/generate-visual-plan Add WebSocket support for real-time notifications
```

Extension design:
```
/generate-visual-plan Extend auth middleware with RBAC permissions
```
