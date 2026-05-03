---
name: fsd-development
description: Create new FSD domains or migrate legacy code following the AI Platform Frontend's FSD variant structure.
disable-model-invocation: true
arguments: [domain_name]
---

Scaffold or migrate frontend code following the FSD (Feature-Sliced Design) variant.

## FSD Layer Structure

```
src/
├── entities/<domain>/          # Domain models, types, API hooks
│   ├── api/                    # React Query hooks + API calls
│   ├── model/                  # Types, schemas, constants
│   └── ui/                     # Presentational components
├── features/<domain>/          # User interactions, mutations
│   ├── api/                    # Mutation hooks
│   ├── model/                  # Feature-specific types
│   └── ui/                     # Interactive components
├── widgets/<domain>/           # Composed UI blocks
├── pages/<domain>/             # Route-level pages
└── shared/                     # Design system, utils, hooks
```

## Operations

### New Domain (`$domain_name`)
1. Create entity layer: types, API hooks, base components
2. Create feature layer: mutations, interactive UI
3. Create widget layer: composed sections
4. Create page layer: route component with layout

### Legacy Migration
1. Identify files in `features-legacy/`
2. Map to correct FSD layers
3. Move with import path updates
4. Verify no circular dependencies

## Rules

- Entities cannot import from features or widgets
- Features can import from entities and shared only
- Widgets can import from features and entities
- Pages can import from all layers
- Use TDS (@thakicloud/shared) components — see 03-tds-essentials.mdc
