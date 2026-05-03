---
name: policy-text-generator
description: >-
  정책 문서/규정을 기반으로 UI 문구, 에러 메시지, 약관, 안내문을 생성하고 정책 위반 여부를 자동 검증한다. Use when the
  user asks to "generate policy text", "create UI copy from policy", "정책 기반 문구
  생성", "정책 문구", "UI 문구 생성", "에러 메시지 생성", "약관 작성", "안내문 작성", "정책 준수 문구",
  "policy copy", or needs text that must comply with internal policies or
  regulations. Do NOT use for general copywriting without policy constraints
  (use marketing skills). Do NOT use for legal contract drafting (use
  pm-toolkit NDA). Do NOT use for technical documentation (use
  technical-writer). Do NOT use for UX writing without policy constraints.
---

# Policy Text Generator

Generate UI strings, errors, terms, and notices from policy sources, then validate compliance automatically.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Content pattern

**Generator + reviewer**: generate copy from policy (generator), then validate against a checklist (reviewer).

## Input

1. **Policy source** (required) — Notion URL, file path, or pasted text
2. **Copy type** (required) — `ui-copy` | `error-message` | `terms` | `notice` | `tooltip` | `guide`
3. **Context** (optional) — Screen/feature, user scenario
4. **Tone** (optional) — formal | friendly | concise (default: formal)

## Workflow

### Step 1: Parse policy

Extract:
- Must-include clauses (disclaimers, legal notices)
- Forbidden phrases (absolute claims, unapproved promises)
- Terminology rules (approved/banned terms)
- Audience constraints (age, region, eligibility)

Use Notion MCP to fetch Notion-backed policies when needed.

### Step 2: Generate copy

- Apply type-specific templates
- Respect tone
- Insert required disclosures
- Avoid forbidden wording

Offer 2–3 variants per string when useful.

### Step 3: Validate

Check output against [references/policy-checklist.md](references/policy-checklist.md):
- Pass/fail per item
- For failures: violation detail + rewrite suggestion
- Overall compliance score (%)

### Step 4: Traceability table

| Copy | Policy | Clause | How applied |
|------|--------|--------|-------------|
| … | … | … | … |

### Step 5: Publish (optional)

- **Notion**: via `md-to-notion`
- **Slack**: review request if configured

## Examples

### Example 1: Payment error copy

User: "Create payment-failure copy aligned with e-payment rules"

Actions: parse policy → three error variants → checklist validation → mapping table.

### Example 2: Privacy consent

User: "Signup privacy consent text per our policy"

Actions: parse PIPA/telecom rules as provided → consent copy → verify mandatory disclosures → mapping table.

## Error handling

| Error | Action |
|-------|--------|
| Policy missing | Ask for URL or paste |
| Policy ambiguous | Flag ambiguous clauses; ask for interpretation |
| Unsupported copy type | List supported types |
| Validation failures | Show failures + suggested fixes |
| Notion MCP down | Fall back to local/paste |

## Project-Specific Overrides (AI Stock Analytics)

This skill operates under project-specific policies:
- [project-tone-matrix.md](../references/project-overrides/project-tone-matrix.md) (POL-003 — tone by context, signal rules, formatting)
- [project-copy-patterns.md](../references/project-overrides/project-copy-patterns.md) (POL-003 — UI copy, errors, empty states, Slack)

Key constraints:
- All trading or signal-related generated text must include the project’s mandatory disclaimer and must not read as personalized investment advice.
- Follow POL-003 signal-expression rules: informational framing only; no promises of returns or imperative buy/sell language unless policy explicitly allows a fixed legal phrase.
- Use financial-domain number formatting for moves and metrics (e.g. `±#0.00%`) as defined in project copy and tone standards.
