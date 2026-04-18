# Knowledge assembly for marketing-autoreason

## Goal

Produce `knowledge-pack.md` that is:

1. **Auditable** — each bullet cites a source path or user paste id.
2. **Compact** — distill tables to the few numbers the tournament actually needs.
3. **Safe** — no PII, no secrets, no full customer lists.

## Sections (use these H2 headings in order)

### 1. Campaign performance snapshot

- Time window, channel, segment (if any).
- 3–7 metrics max (e.g. open %, CTR, CVR, CPA) with source file path or "user message excerpt".

### 2. Copy exemplars

- **Winners** — short quotes + why labeled winner (metric or qualitative outcome).
- **Losers** — short quotes + failure mode tag (generic, too long, wrong audience).

### 3. Audience language

- Verbatim phrases from reviews, tickets, Reddit, interviews (anonymized). Each line ends with `[source]`.

### 4. Competitor positioning

- 3–5 competitors max: their headline claim, overlap risk, our contrast angle. `[source]` each.

### 5. Brand voice

- Must-use / avoid terms, tonal notes, proof style. Prefer pointers to internal docs if large.

## KB integration

When pulling from the repo wiki:

1. Run `kb-search` or `kb-query` with narrow queries (topic + keyword).
2. Copy only excerpts into `knowledge-pack.md`; add `kb:` line with article title + path.

## Empty evidence

If the user supplies nothing, write:

```markdown
## Evidence status
EVIDENCE: none — qualitative rubric-only judging.
```

Proceed; do not block the tournament.
