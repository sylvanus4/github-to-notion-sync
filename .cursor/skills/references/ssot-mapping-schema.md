# SSoT Mapping Schema

Schema for the cross-domain artifact mapping table used by `cross-domain-sync-checker`.

## Mapping table format

Each row links a single concept across up to three domains (Policy, Design, Code). Not all domains are required — a concept may exist in only two domains.

```markdown
| Concept | Category | Policy (Notion) | Design (Figma) | Code (GitHub) | SSoT Owner | Last Synced | Sync Status |
|---------|----------|------------------|----------------|---------------|------------|-------------|-------------|
```

### Column definitions

| Column | Required | Description |
|--------|----------|-------------|
| Concept | Yes | Human-readable name (e.g., "Primary Color", "Error Message Tone") |
| Category | Yes | One of: `color`, `typography`, `spacing`, `component`, `pattern`, `copy`, `policy`, `layout`, `icon` |
| Policy (Notion) | No | Notion page ID or title + section reference |
| Design (Figma) | No | Figma component/token path |
| Code (GitHub) | No | File path + symbol |
| SSoT Owner | Yes | Authoritative domain: `policy`, `design`, or `code` |
| Last Synced | Yes | ISO date (YYYY-MM-DD) |
| Sync Status | Auto | `synced`, `stale`, `drifted`, `orphan` |

### SSoT owner rules

| Category | Default owner | Rationale |
|----------|---------------|-----------|
| color, typography, spacing, component, layout, icon | design | Design defines visual system |
| pattern, copy, policy | policy | PM/UX/legal own rules and copy |
| Pure implementation detail | code | No visual/policy aspect |

Overrides: legal/regulatory → `policy` wins; user may set owner explicitly.

## Drift detection rules

- **Value mismatch**: same concept, different values across domains (High)
- **Missing artifact**: exists in one domain only (Medium)
- **Stale sync**: last verified > 30 days (Low) — see thresholds in example below
- **Unidirectional update**: one domain changed, others not (High)
- **Orphan**: in mapping but missing in live domain (Medium)

### Staleness thresholds

| Age | Status | Action |
|-----|--------|--------|
| < 7 days | Fresh | None |
| 7–30 days | OK | Monitor |
| 30–90 days | Stale | Review recommended |
| > 90 days | Critical | Mandatory review |

## Discovery heuristics

When no mapping exists: search Notion for policy pages; scan Figma library; scan code for tokens/components; propose rows by name similarity; confirm with user before treating as authoritative.

Confidence: exact name 0.95; normalized 0.80; semantic 0.60; below 0.50 → manual review only.

## Example mapping

```markdown
| Concept | Category | Policy (Notion) | Design (Figma) | Code (GitHub) | SSoT Owner | Last Synced | Sync Status |
|---------|----------|------------------|----------------|---------------|------------|-------------|-------------|
| Primary Color | color | Brand Guide s.2 | color/primary | theme.ts:colors.primary | design | 2026-03-15 | synced |
| Error Tone | copy | UX Writing s.3 | — | i18n/errors.ts | policy | 2026-03-10 | synced |
| Button Sizes | component | Component Policy | Button/{sm,md,lg} | Button.tsx:sizes | design | 2026-03-01 | stale |
| Legal Disclaimer | policy | Legal Terms v2.1 | — | Footer.tsx:disclaimer | policy | 2026-02-15 | drifted |
| Heading Scale | typography | — | typography/heading-* | typography.ts | design | 2026-03-20 | synced |
| Grid System | layout | Layout Guide s.1 | layout/grid-12 | grid.css:container | design | 2026-03-18 | synced |
```
