## PM Toolkit

PM utility workflows: resume review, NDA drafting, privacy policy generation, and grammar/flow checking.

### Usage

```
<sub-skill> [context]
```

### Sub-Skills

| Sub-Skill | Shorthand | What it does |
|-----------|-----------|--------------|
| review-resume | `resume` | PM resume review against 10 best practices |
| draft-nda | `nda` | Draft NDA with jurisdiction-appropriate clauses |
| privacy-policy | `privacy` | Draft privacy policy (data types, jurisdiction, compliance) |
| grammar-check | `proofread` | Grammar, logic, and flow check with targeted fixes |

### Execution

Read and follow the `pm-toolkit` skill (`.cursor/skills/pm-toolkit/SKILL.md`) for the full workflow, sub-skill selection, and error handling.

### Examples

```bash
# Review PM resume
/pm-toolkit resume -- review my resume for this Senior PM role

# Tailor resume to job posting
/pm-toolkit resume -- tailor my resume to this job description [paste]

# Draft NDA
/pm-toolkit nda -- NDA between Acme Corp and Beta Inc, California jurisdiction

# Privacy policy
/pm-toolkit privacy -- privacy policy for our SaaS app collecting user analytics

# Proofread document
/pm-toolkit proofread -- check grammar and flow in this investor pitch deck intro
```
