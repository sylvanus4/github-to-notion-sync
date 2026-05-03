---
name: domain-name-brainstormer
description: >-
  Generate creative product names using 5 naming strategies and check
  domain/social handle availability across TLDs (.com, .io, .dev, .ai, .co).
  Use when the user asks to "brainstorm names", "find a domain", "name my
  product", "product name ideas", "check domain availability", "name this
  app", "브랜드 이름", "도메인 찾기", "이름 짓기", "프로젝트 네이밍", "도메인 사용 가능 확인", or needs
  creative naming with availability verification. Do NOT use for renaming code
  identifiers (just rename them), trademark search (consult a lawyer), or full
  brand identity design (use brand-guidelines).
---

# Domain Name Brainstormer

Generate creative product names and check domain availability (.com, .io, .dev, .ai, .co) for new apps, services, and micro-brands.

## When to Use

- Launching a new product, app, or service and need a name
- Exploring brand name options before committing
- Checking if a name idea has available domains and social handles
- Brainstorming alternative names when the first choice is taken
- Naming internal tools, open-source projects, or side projects

## When NOT to Use

- Renaming variables or code identifiers (just rename them)
- Trademark or legal name validation (consult a lawyer)
- Full brand identity design (use `brand-guidelines` or `kwp-brand-voice-guideline-generation`)
- SEO domain migration (needs redirect and ranking analysis first)

## Inputs

| Field | Required | Description |
|-------|----------|-------------|
| concept | Yes | What the product/service does (1-2 sentences) |
| tone | No | e.g. "playful", "enterprise", "technical", "minimalist" |
| constraints | No | Max length, must include a word, avoid certain words |
| tld_priority | No | Preferred TLDs in order, default: `.com, .io, .dev, .ai` |

## Workflow

### Phase 1: Name Generation (5 strategies)

Generate 20-30 candidate names using these strategies:

1. **Portmanteau**: Blend two relevant words (Spotify = spot + identify, Pinterest = pin + interest)
2. **Metaphor**: Use a concept from another domain (Slack, Notion, Figma)
3. **Truncation**: Shorten a descriptive word (Kubernetes → Kube, Application → App)
4. **Invented word**: Create a new word that sounds right (Zillow, Twilio, Vercel)
5. **Descriptive compound**: Two simple words combined (GitHub, Airflow, Datadog)

For each candidate, provide:
- Name
- Strategy used
- Why it fits the concept
- Pronunciation guide if non-obvious

### Phase 2: Domain Availability Check

For the top 10 candidates:

1. Check availability via WebSearch for `"{name}.com" domain available`
2. Check alternative TLDs: `.io`, `.dev`, `.ai`, `.co`, `.app`
3. Check social handle availability: Twitter/X, GitHub
4. Flag any that are existing well-known brands or products

### Phase 3: Shortlist & Scoring

Score each finalist (1-10) on:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Memorability | 25% | Easy to remember after hearing once |
| Spellability | 20% | Can be spelled correctly from hearing it |
| Domain availability | 20% | .com or preferred TLD available |
| Relevance | 20% | Conveys what the product does |
| Uniqueness | 15% | Not easily confused with existing brands |

## Output Format

```markdown
## Domain Name Brainstorm: [Concept]

### Top 5 Recommendations

| Rank | Name | Score | .com | .io | .dev | Strategy |
|------|------|-------|------|-----|------|----------|
| 1 | ... | 8.5 | ✅ | ✅ | ✅ | Portmanteau |
| 2 | ... | 8.2 | ❌ | ✅ | ✅ | Metaphor |
| ... | ... | ... | ... | ... | ... | ... |

### Full Candidate List
(all 20-30 names with strategy tags)

### Availability Details
(per-name TLD and social handle check results)
```

## Gotchas

1. **WebSearch availability checks are approximate.** Domain registrar results may differ — always advise the user to verify on their preferred registrar before purchasing.
2. **"Available" != legally safe.** A domain being unregistered doesn't mean the name is free of trademark claims. Always flag this.
3. **Cultural blindspots.** A name that sounds great in English may have unfortunate meanings in Korean or other languages. Run a quick check.

## Verification

After completing all phases:
1. Confirm the shortlist contains names from at least 3 different naming strategies
2. Verify every recommended name has at least one available TLD checked
3. Ensure no recommended name matches an existing well-known product without a flag
4. Confirm pronunciation guide is provided for any non-obvious name

## Anti-Example

```markdown
# BAD: Recommending taken names without checking
- "I recommend 'Notion' for your note-taking app" → Already a $10B company
- Listing 30 names with zero availability checks → Useless output

# BAD: All names from one strategy
- All 10 recommendations are portmanteaus → No diversity, harder for user to choose
```

## Constraints

- Never recommend a name that is an existing well-known product without flagging it
- Always check at least .com and one alternative TLD
- Include at least 3 different naming strategies in the shortlist
- Keep names under 12 characters when possible
- Avoid names that are difficult to pronounce in English and Korean
- Do NOT generate more than 30 candidates — quality over quantity
