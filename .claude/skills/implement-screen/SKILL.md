---
name: implement-screen
description: Master orchestrator — generate production FSD code from screen spec and Figma design.
disable-model-invocation: true
arguments: [screen_spec, figma_url]
---

Implement a production screen from specification and Figma design.

## Pipeline

1. **Parse spec**: Read screen description document (`$screen_spec`)
2. **Figma analysis**: Extract design tokens and components from `$figma_url` (if provided)
3. **Entity generation**: Create/update entity layer (types, API hooks)
4. **Feature generation**: Create mutation hooks and interactive components
5. **Widget composition**: Build composed UI sections
6. **Page assembly**: Create route-level page with layout
7. **i18n**: Add translation keys for all UI strings
8. **Validation**: Check FSD import rules, TypeScript compilation

## Output

- Complete FSD domain code across entities/features/widgets/pages
- Updated route configuration
- i18n key additions
- TypeScript-clean, lint-clean code

## Rules

- Follow TDS (@thakicloud/shared) component patterns
- Use React Query for data fetching
- Use Zod + React Hook Form for form validation
- Korean strings in i18n files, not hardcoded
- Do not duplicate existing shared components
