---
name: kwp-design-design-system-management
description: >-
  Manage design tokens, component libraries, and pattern documentation. Trigger
  with "design system", "component library", "design tokens", "style guide", or
  when the user asks about maintaining consistency across designs. Do NOT use
  for this project's design audit or React component review — prefer
  design-architect or frontend-expert skill. Korean triggers: "설계", "감사", "리뷰",
  "문서".
metadata:
  author: "anthropic-kwp"
  version: "1.0.0"
  category: "workflow"
---
# Design System Management

Help build, maintain, and evolve design systems.

## Components of a Design System

### Design Tokens
Atomic values that define the visual language:
- Colors (brand, semantic, neutral)
- Typography (scale, weights, line heights)
- Spacing (scale, component padding)
- Borders (radius, width)
- Shadows (elevation levels)
- Motion (durations, easings)

### Components
Reusable UI elements with defined:
- Variants (primary, secondary, ghost)
- States (default, hover, active, disabled, loading, error)
- Sizes (sm, md, lg)
- Behavior (interactions, animations)
- Accessibility (ARIA, keyboard)

### Patterns
Common UI solutions combining components:
- Forms (input groups, validation, submission)
- Navigation (sidebar, tabs, breadcrumbs)
- Data display (tables, cards, lists)
- Feedback (toasts, modals, inline messages)

## Principles

1. **Consistency over creativity** — The system exists so teams don't reinvent the wheel
2. **Flexibility within constraints** — Components should be composable, not rigid
3. **Document everything** — If it's not documented, it doesn't exist
4. **Version and migrate** — Breaking changes need migration paths

## Examples

### Example 1: Typical request

**User says:** "I need help with design design system management"

**Actions:**
1. Ask clarifying questions to understand context and constraints
2. Apply the domain methodology step by step
3. Deliver structured output with actionable recommendations

### Example 2: Follow-up refinement

**User says:** "Can you go deeper on the second point?"

**Actions:**
1. Re-read the relevant section of the methodology
2. Provide detailed analysis with supporting rationale
3. Suggest concrete next steps
## Error Handling

| Issue | Resolution |
|-------|-----------|
| Missing required context | Ask user for specific inputs before proceeding |
| Skill output doesn't match expectations | Re-read the workflow section; verify inputs are correct |
| Conflict with another skill's scope | Check the "Do NOT use" clauses and redirect to the appropriate skill |
