---
name: figma-dev-pipeline
description: Bidirectional Figma-to-code and code-to-Figma pipeline with Code Connect, design token extraction, and 5-stage workflow.
disable-model-invocation: true
arguments: [figma_url]
---

Orchestrate the Figma development pipeline for `$figma_url`.

## Pipeline Stages

### Figma → Code
1. **Design Extraction**: Get design context, screenshots, tokens from Figma MCP
2. **Spec Generation**: Create component spec with props, variants, states
3. **Code Scaffolding**: Generate React/TypeScript component skeleton
4. **Implementation Guide**: Map Figma tokens to TDS design tokens
5. **Verification**: Compare rendered output against Figma design

### Code → Figma
1. **Code Analysis**: Read existing component implementation
2. **Design System Search**: Find matching DS components via search_design_system
3. **Screen Building**: Use use_figma to build screen from DS components
4. **Layout Matching**: Align layout to code implementation
5. **Verification**: Compare Figma result against live UI

## Code Connect Integration

- Map Figma components to codebase components via Code Connect files
- Track coverage of mapped vs unmapped components
- Use search_design_system for published DS token/component lookup

## Rules

- Always check for existing TDS components before creating new ones
- Map Figma tokens to project's CSS custom properties
- Preserve auto-layout and responsive constraints
