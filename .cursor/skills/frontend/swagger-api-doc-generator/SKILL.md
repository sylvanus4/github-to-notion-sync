---
name: swagger-api-doc-generator
description: Swagger/OpenAPI URL에서 API 명세 문서를 Markdown으로 생성합니다. Swagger URL 제공 시, API 문서화 요청 시, 특정 API 그룹의 명세가 필요할 때 사용합니다. Do NOT use for 코드 생성(fsd-development), 화면 구현(implement-screen), 또는 화면 기획서 작성(screen-description).
metadata:
  version: 1.1.1
  category: generation
---

# Swagger API Documentation Generator

Produce clean Markdown API reference documents from Swagger/OpenAPI JSON.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Workflow

### Step 1: Fetch Swagger JSON

```bash
curl -s {SWAGGER_URL} > /tmp/swagger-latest.json
wc -l /tmp/swagger-latest.json
```

### Step 2: List API groups

If the user did not specify a group, show available tags:

```bash
cat /tmp/swagger-latest.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
tags = data.get('tags', [])
for t in tags:
    print(f\"- {t.get('name')}: {t.get('description', '')}\")"
```

### Step 3: Extract paths

```bash
cat /tmp/swagger-latest.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
paths = data.get('paths', {})
keyword = '{KEYWORD}'
filtered = {k: v for k, v in paths.items() if keyword in k}
for path in sorted(filtered.keys()):
    for method in filtered[path].keys():
        summary = filtered[path][method].get('summary', '')
        print(f'{method.upper():7} {path}')
        print(f'        Summary: {summary}')"
```

### Step 4: Extract schema definitions

```bash
cat /tmp/swagger-latest.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
definitions = data.get('definitions', {})
keyword = '{KEYWORD}'
filtered = {k: v for k, v in definitions.items() if keyword in k.lower()}
for name in sorted(filtered.keys()):
    print(f'\n=== {name} ===')
    print(json.dumps(filtered[name], indent=2, ensure_ascii=False))"
```

### Step 5: Generate Markdown

Default save path pattern: `ai-platform/frontend/docs/api/{api-name}/{api-name}-api-spec.md` (adjust to the active repo layout).

Templates: [templates.md](templates.md).

## Document structure

Final Markdown MUST use Korean section titles per output rule. Suggested outline (translate headings appropriately): Authentication → API overview → Endpoint index → Endpoint details (request/response) → Error responses → Appendix (schemas).

## Checklist

- [ ] Swagger JSON downloaded successfully
- [ ] Target paths confirmed
- [ ] Request schemas (path, query, body)
- [ ] Response schemas
- [ ] Enum values documented
- [ ] Example values included
- [ ] HTTP status codes listed

## Examples

### Example 1: Document one API group

User: "Build docs from http://localhost:3000/swagger/doc.json for MyTemplates"

Actions: download → filter by MyTemplates tag → write `docs/api/my-templates/my-templates-api-spec.md`.

### Example 2: Let user pick a group

User: "Generate API docs from http://localhost:3000/swagger/index.html"

Actions: resolve JSON URL (often `/swagger/doc.json`) → list tags → generate for the chosen tag.

## Troubleshooting

### Download fails

Cause: bad URL, server down, or auth required.
Fix: normalize to `/swagger/doc.json`, verify server, add auth headers if needed.

### Empty `definitions`

Cause: OpenAPI 3 uses `components.schemas`.
Fix: also read `data.get('components', {}).get('schemas', {})` and branch by spec version.
