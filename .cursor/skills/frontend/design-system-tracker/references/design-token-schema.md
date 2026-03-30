# Design Token Schema

Structured format for representing design tokens extracted from Figma or code.

## Token Entry Format

```yaml
- name: color-primary
  category: color
  value: "#1A73E8"
  previous_value: null
  source: figma | code | manual
  component_usage:
    - Button/Primary
    - Link/Default
  change_type: added | modified | removed | unchanged
  breaking: true | false
  notes: ""
```

## Category Definitions

| Category | Token Name Pattern | Value Type |
|----------|-------------------|------------|
| color | `color-*` | hex, rgba, hsl |
| typography | `font-*`, `text-*` | px, rem, string |
| spacing | `spacing-*`, `gap-*` | px, rem |
| shadow | `shadow-*`, `elevation-*` | CSS shadow syntax |
| border | `border-*`, `radius-*` | px, rem |
| breakpoint | `breakpoint-*` | px |
| opacity | `opacity-*` | 0-1 |
| z-index | `z-*` | integer |

## Snapshot Format

A complete snapshot captures all tokens at a point in time:

```yaml
snapshot:
  date: "YYYY-MM-DD"
  source: "figma-file-url or git-commit-hash"
  tokens:
    - name: ...
      category: ...
      value: ...
```

## Diff Format

A diff compares two snapshots:

```yaml
diff:
  from: "snapshot-date-1"
  to: "snapshot-date-2"
  changes:
    added:
      - { name: ..., category: ..., value: ... }
    modified:
      - { name: ..., category: ..., old_value: ..., new_value: ..., breaking: true|false }
    removed:
      - { name: ..., category: ..., last_value: ... }
  summary:
    total_changes: N
    breaking_changes: N
    categories_affected: [list]
```
