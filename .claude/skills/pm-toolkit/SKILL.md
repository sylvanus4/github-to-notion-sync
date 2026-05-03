---
name: pm-toolkit
description: >-
  PM utility skills: resume review against PM best practices, NDA drafting,
  privacy policy generation, and grammar/flow checking. Based on
  phuryn/pm-skills. Use when the user asks for "review resume", "draft NDA",
  "privacy policy", "grammar check", "proofread", or "PM resume review". Do
  NOT use for legal contract review (use kwp-legal-contract-review), general
  documentation (use technical-writer), or marketing content (use
  kwp-marketing-content-creation). Korean triggers: "이력서 검토", "PM 이력서", "NDA
  초안", "개인정보처리방침", "문법 교정", "교정", "이력서 맞춤화", "컴플라이언스".
---

# PM Toolkit

PM utility skills for resume review, NDA drafting, privacy policy generation, and grammar/flow checking. Each sub-skill has a reference file with full instructions.

## Sub-Skill Index

| Sub-Skill        | Reference              | Triggers                                                                 |
|------------------|------------------------|--------------------------------------------------------------------------|
| draft-nda        | [references/draft-nda.md](references/draft-nda.md) | draft NDA, confidentiality agreement, NDA template                       |
| grammar-check    | [references/grammar-check.md](references/grammar-check.md) | grammar check, proofread, fix typos, writing review                      |
| privacy-policy   | [references/privacy-policy.md](references/privacy-policy.md) | privacy policy, data protection policy, GDPR policy, CCPA                 |
| review-resume    | [references/review-resume.md](references/review-resume.md) | review PM resume, resume feedback, PM job application, tailor resume     |

## Workflow

1. **Identify sub-skill**: Match user intent to one of the four sub-skills above.
2. **Read reference**: Load the corresponding `references/<name>.md` for full instructions, input arguments, and output format.
3. **Execute**: Follow the reference process; produce output in the format specified. Add disclaimers where required (NDA, privacy policy).

## Examples

**Example 1 – NDA draft**
> "Draft an NDA between Acme Corp and Beta Inc for sharing technical specs. California jurisdiction."

→ Use `references/draft-nda.md`. Collect party names, addresses, representatives, information types. Output: Summary, full NDA, customization notes. Include legal disclaimer.

**Example 2 – Grammar check**
> "Proofread this investor pitch deck intro"

→ Use `references/grammar-check.md`. Set objective (e.g., persuade investors). Output: Error summary, fixes by category, priority fixes, tone alignment. Do not rewrite the full text.

**Example 3 – PM resume review**
> "Review my resume for this PM job [paste posting]"

→ Use `references/review-resume.md`. Evaluate against 10 best practices. Output: Intro, detailed feedback per practice (with quotes), conclusion. Tailor feedback to the job posting if provided.

## Error Handling

- **Missing inputs**: If required arguments (e.g., party names, text to review) are missing, ask the user for them before continuing.
- **Legal disclaimers**: For `draft-nda` and `privacy-policy`, always state that the output is informational and that a qualified attorney must review before use.
- **Ambiguous scope**: If the request spans multiple sub-skills (e.g., "review my resume and proofread my cover letter"), handle them sequentially: resume first, then grammar-check on the cover letter.
- **Out-of-scope**: Decline and route to other skills when the user needs contract review (kwp-legal-contract-review), general docs (technical-writer), or marketing copy (kwp-marketing-content-creation).
