## Domain Name Brainstormer

Generate product names and check domain availability for new apps, services, and micro-brands.

### Usage

```
/domain-name "AI-powered cloud cost optimizer"
/domain-name --tone enterprise "multi-cloud management platform"
/domain-name --tld .ai,.dev "open-source LLM gateway"
```

### Workflow

1. **Generate** — Produce 20-30 candidate names using 5 strategies: portmanteau, metaphor, truncation, invented word, descriptive compound
2. **Check** — Verify domain availability (.com, .io, .dev, .ai) and social handles for top 10
3. **Score** — Rank finalists on memorability, spellability, domain availability, relevance, and uniqueness
4. **Recommend** — Present top 5 with availability matrix and scoring breakdown

### Execution

Read and follow the `domain-name-brainstormer` skill (`.cursor/skills/standalone/domain-name-brainstormer/SKILL.md`) for the full naming and availability workflow.

### Examples

Name a new product:
```
/domain-name "developer tool for automating Kubernetes deployments"
```

Enterprise-tone naming:
```
/domain-name --tone enterprise "B2B SaaS for compliance automation"
```
