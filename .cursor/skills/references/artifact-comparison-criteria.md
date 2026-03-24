# Artifact comparison criteria

Detailed match rules for each artifact pair. Use when scoring gaps between
design, code, spec (PRD), and policy.

## Design ↔ Code

| Dimension | Design source | Code source | Match criteria |
|-----------|---------------|-------------|----------------|
| Component presence | Figma components | Component files | 1:1 mapping exists |
| State variants | Figma variants | Conditional branches | Every variant has implementation |
| Copy | Text layers | Hard-coded / i18n strings | Same meaning (allow minor wording) |
| Color | Fill/stroke | CSS / tokens | Same hex/token |
| Spacing | Auto layout | margin/padding | Comparable values |
| Responsive | Resize modes | Breakpoints | Coverage for main breakpoints |

## Code ↔ Spec (PRD)

| Dimension | Spec source | Code source | Match criteria |
|-----------|-------------|-------------|----------------|
| Feature coverage | Stories / requirements | Implemented feature | Requirement traceable to code |
| States | State tables | State variables / UI | All defined states implemented |
| Exceptions | Exception tables | try/catch, error UI | Each defined case handled |
| Validation | Field rules | Schema / validators | Same constraints |
| API | Documented endpoints | Client calls | Method + path align |

## Code ↔ Policy

| Dimension | Policy source | Code source | Match criteria |
|-----------|---------------|-------------|----------------|
| Privacy | Retention/deletion clauses | Storage/delete logic | Same retention behavior |
| Access control | Access policy | Auth middleware | Rules enforced |
| Consent | Terms sections | Consent UI + persistence | Required vs optional matches |
| Masking | Masking rules | Masking utilities | Same fields masked |

## Spec ↔ Policy

| Dimension | Spec source | Policy source | Match criteria |
|-----------|-------------|-------------|----------------|
| Consent flows | Planned UX | Legal requirements | All mandatory consents present |
| Error copy | Planned messages | Mandatory phrases | Required legal text included |
| Data collection | Fields in spec | Privacy policy inventory | Same data categories |

## Design ↔ Spec

| Dimension | Design source | Spec source | Match criteria |
|-----------|---------------|-------------|----------------|
| Screens | Frames | User flows / screen list | Coverage |
| States | Variants | State definitions | No orphan variants / missing states |

## Design ↔ Policy

| Dimension | Design source | Policy source | Match criteria |
|-----------|---------------|-------------|----------------|
| Disclaimers | Footer / modals | Legal text | Required disclosures visible |
| PII display | Visible fields | Display rules | No prohibited exposure |

## Six-axis coverage (when sources allow)

When Design, Code, Spec, and Policy are all available, evaluate these axes:

```
Design ↔ Code
Design ↔ Spec
Code   ↔ Spec
Code   ↔ Policy
Spec   ↔ Policy
Design ↔ Policy
```

Only score axes for which **both** endpoints were provided.
