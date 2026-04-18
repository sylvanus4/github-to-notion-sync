## Lead Research

Find target companies and decision-makers based on your ICP. Enrich with contact details, company intel, and outreach-ready data.

### Usage

```
/lead-research "Series B AI startups in Korea"       # ICP-based discovery
/lead-research --enrich "John Kim, Acme Corp"        # enrich a known contact
/lead-research --company "thakicloud.com"             # company research
```

### Workflow

1. **Define ICP** — Clarify ideal customer profile: industry, size, tech stack, role
2. **Discover** — Search for matching companies and decision-makers
3. **Enrich** — Get emails, phone numbers, titles, funding data, tech stack
4. **Score** — Rank leads by ICP fit and engagement signals
5. **Output** — Prioritized lead list with contact cards and outreach angles

### Execution

Read and follow the `kwp-apollo-prospect` skill (`.cursor/skills/kwp/kwp-apollo-prospect/SKILL.md`) for full ICP-to-leads pipeline. For single contact enrichment, use `kwp-apollo-enrich-lead` (`.cursor/skills/kwp/kwp-apollo-enrich-lead/SKILL.md`). For Common Room signals, use `kwp-common-room-prospect` (`.cursor/skills/kwp/kwp-common-room-prospect/SKILL.md`).

### Examples

Find leads by ICP:
```
/lead-research "CTOs at mid-size cloud companies using Kubernetes"
```

Enrich a specific person:
```
/lead-research --enrich "Jane Doe, NVIDIA"
```
