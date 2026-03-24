# Normalization Schema (Cross-Artifact Comparison)

Use when comparing PRD, design (Figma), code, and policy sources. Convert each
extracted fact into this structure before building the sync matrix.

## Element record

| Field | Description |
|-------|-------------|
| `element_id` | Stable id, e.g. `state:payment:loading`, `rule:password:length` |
| `category` | `state` / `edge_case` / `business_rule` / `policy` / `ui_flow` / `copy` / `component` |
| `description` | Human-readable summary |
| `source` | `prd` / `design` / `code` / `policy` |
| `detail` | Source-specific payload (quotes, file paths, node ids) |

## Ingestion hints

- **PRD (Notion)**: features, state definitions, edge cases, flows, business rules
- **Design (Figma)**: screens, variants, error/empty/loading presence, text layers
- **Code**: enums, conditionals, API calls, validation, error handling, i18n keys
- **Policy**: mandatory rules, prohibitions, legal/consent, data handling

Minimum **two** sources required for a comparison run (any combination).
