---
description: "Re-render any content in a specified format: table, JSON, YAML, CSV, Mermaid, markdown, HTML, XML, or bullets"
argument-hint: "<format> <content or topic>"
---

# Format As

Force any content into a specific output format. Useful for data transformation, documentation, and structured exports.

## Usage

```
/format-as table Compare React, Vue, and Angular features
/format-as json List of top 10 tech companies with revenue and employees
/format-as yaml Kubernetes deployment config for a Python app
/format-as mermaid User authentication flow
/format-as csv 2024 quarterly revenue data for AAPL
/format-as markdown [paste raw text here]
/format-as html Simple pricing comparison card
/format-as bullets 이 보고서의 핵심 내용을 불릿으로 정리해줘
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Parse format** — Extract the target format from the first token of `$ARGUMENTS`
2. **Parse content** — Everything after the format token is the content or generation instruction
3. **Generate or transform** — If content is provided, transform it; if a topic is given, generate content in that format
4. **Validate structure** — Ensure the output is syntactically valid for the chosen format
5. **Deliver** — Output in a fenced code block with the appropriate language tag

### Supported Formats

| Format | Output | Language Tag |
|--------|--------|-------------|
| `table` | Markdown pipe table | (none) |
| `json` | Pretty-printed JSON | `json` |
| `yaml` | YAML document | `yaml` |
| `csv` | Comma-separated values | `csv` |
| `mermaid` | Mermaid diagram syntax | `mermaid` |
| `markdown` | Structured markdown | `markdown` |
| `html` | Semantic HTML | `html` |
| `xml` | Well-formed XML | `xml` |
| `bullets` | Bullet point list | (none) |
| `numbered` | Numbered list | (none) |
| `typescript` | TypeScript type/interface | `typescript` |
| `sql` | SQL DDL or query | `sql` |

### Constraints

- Output must be copy-paste ready — no truncation, no placeholders like "..."
- JSON must be valid (parseable by `JSON.parse`)
- YAML must be valid (parseable by any YAML parser)
- Mermaid must render without errors
- Tables must have consistent column counts across all rows
- If the content is too large for a single code block, split into labeled sections
