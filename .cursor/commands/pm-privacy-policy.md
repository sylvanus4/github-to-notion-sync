---
description: Draft a comprehensive privacy policy covering data types, jurisdictions, and GDPR/CCPA compliance.
argument-hint: "<product/service> | <data collected> | <jurisdictions>"
---

# PM Privacy Policy

Draft a comprehensive privacy policy covering data types, jurisdictions, and GDPR/CCPA compliance. References pm-toolkit skill, privacy-policy sub-skill. Includes compliance checklist and implementation checklist.

## Usage

```
/pm-privacy-policy Privacy policy for our SaaS app collecting user analytics and account data
/pm-privacy-policy 우리 앱의 개인정보처리방침 초안 — 유저 분석, 계정 데이터 수집
```

## Workflow

### Step 1: Load skill and reference

Read the `pm-toolkit` skill (`.cursor/skills/pm-toolkit/SKILL.md`) and `references/privacy-policy.md`.

### Step 2: Gather context

Request or use provided:

- Product/service description
- Data collected (personal, usage, cookies, third-party)
- Data subjects (users, visitors, B2B contacts)
- Jurisdictions (EU/GDPR, California/CCPA, other)
- Data sharing (subprocessors, analytics, advertising)
- Retention periods and storage locations

### Step 3: Draft policy sections

Produce a structured privacy policy with:

1. **Introduction** — Who we are, scope
2. **Data we collect** — Categories, sources, purposes
3. **Legal basis** — Consent, contract, legitimate interest (GDPR)
4. **How we use data** — Specific purposes
5. **Data sharing** — Third parties, subprocessors, categories
6. **International transfers** — Safeguards (SCCs, adequacy)
7. **Retention** — How long we keep data
8. **Rights** — Access, rectification, deletion, portability, objection, withdrawal of consent
9. **Cookies and tracking** — Types, purposes, opt-out
10. **Children** — Age restrictions if applicable
11. **Updates** — How we notify of changes
12. **Contact** — DPO or privacy contact

### Step 4: Compliance and implementation checklists

- **Compliance checklist**: GDPR (Art. 13/14), CCPA, cookie consent, etc.
- **Implementation checklist**: Consent banners, data request process, retention automation, DPA templates

### Step 5: Output

Deliver:

1. Full privacy policy draft
2. Compliance checklist (jurisdiction-specific)
3. Implementation checklist
4. Legal disclaimer: *This is informational only; legal counsel must review before publication.*

## Notes

- GDPR and CCPA have different requirements; address both if in scope.
- List subprocessors; keep a separate subprocessor list for DPAs.
- Cookie policy may be separate or integrated; clarify with legal.
