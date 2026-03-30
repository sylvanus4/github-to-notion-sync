# Impact criteria (calibration)

Use these thresholds when classifying **risk**, **effort**, and **cascade probability** in change-impact outputs. Labels are relative to the change unit and org context; when uncertain, state assumptions **in Korean** in the report.

## Risk: Low / Med / High

| Level | Concrete signals (any strong signal can justify the level) |
|-------|------------------------------------------------------------|
| **Low** | No auth/billing/compliance path touched; ≤3 direct dependents; change is additive or behind a flag; rollback is trivial; no customer-visible behavior change without opt-in. |
| **Med** | Touches shared types/config or 4–12 dependents; cross-team coordination likely; behavior change is user-visible but reversible; partial data or UX inconsistency possible if wrong. |
| **High** | Touches auth, payments, PII, retention, or legal/compliance text; breaking API or schema; fan-out >12 nodes or unknown frontier; irreversible or hard-to-roll-back data migration; revenue- or safety-critical path. |

If signals conflict, use the **highest** applicable level and note the tension in one line.

## Effort: S / M / L

| Size | Calibration |
|------|----------------|
| **S** | Single team, ≤3 days equivalent, one repo area, no cross-team sequencing; validation is spot-check or unit-level. |
| **M** | Multiple modules or 2 teams, ~3–10 days, requires coordinated release or feature flag; includes integration or design QA. |
| **L** | Org-wide or multi-squad, >10 days or multiple releases; migrations, policy rollouts, or broad comms; needs program-level tracking. |

## Cascade probability

- **High probability of cascade**: Renames of domain concepts, shared enums/tokens, public API contracts, global policy clauses, or root layout/navigation — expect hidden consumers.
- **Medium**: New optional fields, localized copy, additive endpoints — often contained but check clients and analytics.
- **Low**: Isolated component with no shared imports, internal-only docs — still verify one hop.

When depth is capped, label downstream as **unknown** rather than Low.
