---
description: "Generate a structured data model, outline, or schema from a natural language description"
argument-hint: "<entity or system to model>"
---

# Structured Schema Generator

Generate a formal data model or schema from a plain-language description. Supports multiple output formats for immediate use in code.

## Usage

```
/schema User entity with profile, roles, and subscription history
/schema --typescript E-commerce order with items, shipping, and payment
/schema --json-schema API request body for creating a deployment
/schema --zod Form validation for a registration page
/schema --sql Blog platform with posts, comments, and tags
/schema --prisma Multi-tenant SaaS with organizations and members
/schema --openapi REST API for a task management service
/schema 주문 시스템의 데이터 모델을 설계해줘
```

## Your Task

User input: $ARGUMENTS

### Mode Selection

Parse `$ARGUMENTS` for format flags:

- **No flags / `--typescript`** — TypeScript interfaces (default)
- `--json-schema` — JSON Schema draft-07
- `--zod` — Zod validation schema
- `--sql` — PostgreSQL DDL with constraints and indexes
- `--prisma` — Prisma schema file
- `--yaml` — YAML data model definition
- `--openapi` — OpenAPI 3.0 components/schemas
- `--python` — Python dataclass or Pydantic model

### Workflow

1. **Parse entity description** — Extract entities, fields, relationships, and constraints from natural language
2. **Identify fields** — For each entity, determine field names, types, optionality, and defaults
3. **Define relationships** — Map 1:1, 1:N, N:M relationships between entities
4. **Add constraints** — Required fields, unique constraints, enums, value ranges, string patterns
5. **Add indexes** (for SQL/Prisma) — Primary keys, unique indexes, foreign keys
6. **Format output** — Generate in the selected format with proper syntax
7. **Add usage notes** — Brief comments explaining non-obvious design decisions

### Output Format

```
## Schema: [Entity/System Name]

### Entities
[List of entities and their relationships]

### [Format-specific output in code block]

### Design Notes
- [Non-obvious decision 1]
- [Non-obvious decision 2]
```

### Constraints

- All field names use camelCase (TypeScript/Zod/JSON Schema) or snake_case (SQL/Prisma/Python) per convention
- Every entity must have an `id` field
- Timestamps (`createdAt`, `updatedAt`) included by default unless explicitly excluded
- Enums must be explicitly typed, not raw strings
- Output must be syntactically valid and copy-paste ready
