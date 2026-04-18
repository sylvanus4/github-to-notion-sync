## API Docs

Generate OpenAPI/Swagger documentation from your API routes with examples, error codes, and auth requirements.

### Usage

```
/api-docs                              # generate docs for all API routes
/api-docs src/api/                     # specific directory
/api-docs --format openapi             # OpenAPI 3.0 YAML output
/api-docs --format markdown            # markdown reference output
```

### Workflow

1. **Discover** — Scan for API routes, handlers, and endpoint definitions
2. **Extract** — Parse request/response schemas, parameters, and auth requirements
3. **Document** — Generate endpoint documentation with examples and error codes
4. **Validate** — Check for undocumented endpoints and missing schemas
5. **Output** — Formatted API reference as markdown or OpenAPI spec

### Execution

Read and follow the `swagger-api-doc-generator` skill (`.cursor/skills/frontend/swagger-api-doc-generator/SKILL.md`) for Swagger URL-based doc generation. For broader technical documentation, use `technical-writer` (`.cursor/skills/standalone/technical-writer/SKILL.md`).

### Examples

Generate all API docs:
```
/api-docs
```

Generate from Swagger URL:
```
/api-docs https://api.example.com/swagger.json
```
