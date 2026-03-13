---
description: Draft a non-disclosure agreement with jurisdiction-appropriate clauses and legal review flags.
argument-hint: "<party A> | <party B> | <jurisdiction> | <information types>"
---

# PM Draft NDA

Draft a non-disclosure agreement with jurisdiction-appropriate clauses and legal review flags. References pm-toolkit skill, draft-nda sub-skill. Includes parties, confidential info definition, obligations, exclusions, term, remedies, governing law.

## Usage

```
/pm-draft-nda NDA between Acme Corp and Beta Inc, California, technical specs sharing
/pm-draft-nda Acme와 Beta 간 NDA 초안, 캘리포니아 관할, 기술 스펙 공유
```

## Workflow

### Step 1: Load skill and reference

Read the `pm-toolkit` skill (`.cursor/skills/pm-toolkit/SKILL.md`) and `references/draft-nda.md`.

### Step 2: Collect required inputs

Request or use provided:

- **Parties**: Full legal names, addresses, representative titles
- **Confidential information**: Types (technical specs, business plans, customer data, etc.)
- **Purpose**: Purpose of disclosure (e.g., evaluation, partnership)
- **Jurisdiction**: Governing law (e.g., California, Delaware, UK)
- **Term**: Duration of confidentiality (e.g., 2 years, 5 years, perpetual)
- **Mutual vs one-way**: Both parties disclosing or one-way only

### Step 3: Draft NDA sections

Produce a structured NDA with:

1. **Parties** — Names, addresses, roles
2. **Definitions** — Confidential Information, Receiving Party, Disclosing Party
3. **Obligations** — Use, non-disclosure, care, no copying
4. **Exclusions** — Public domain, independently developed, lawfully received, etc.
5. **Term** — Duration of obligations
6. **Return/destruction** — Upon request or termination
7. **Remedies** — Injunctive relief, damages (as appropriate)
8. **Governing law and dispute resolution**
9. **Miscellaneous** — Assignment, entire agreement, amendments

### Step 4: Add legal review flags

Flag clauses that commonly require attorney review:

- Jurisdiction-specific enforceability
- Limitation of liability
- Indemnification
- Non-compete or non-solicit (if included)

### Step 5: Output

Deliver:

1. Summary of key terms
2. Full NDA draft (formatted)
3. Customization notes
4. Legal disclaimer: *This is informational only; a qualified attorney must review before use.*

## Notes

- Always include a legal disclaimer in the output.
- Jurisdiction affects enforceability; specify clearly.
- Mutual NDAs are common for biz dev; one-way for vendor evaluations.
