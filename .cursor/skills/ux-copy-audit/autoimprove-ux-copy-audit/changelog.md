# Changelog: ux-copy-audit skill-autoimprove cycle

## 2025-03-24 — v1.1.0 → v1.2.0

### Summary

Targeted hardening of the skill so audit outputs satisfy binary evals E1–E4 without expanding scope beyond UX copy auditing.

### Changes

1. **E1 (file/line/key references)** — New **Finding requirements** block: every finding MUST include `file:line` or an agreed key path (`namespace:key`, `ComponentName.i18nKey`); screen-only labels without a locatable reference are disallowed.

2. **E2 (severity)** — Inline **severity classification table** for Critical / High / Medium / Low (policy + user impact, multi-screen inconsistency, single-instance issues, minor polish).

3. **E3 (policy linkage)** — Policy-related findings MUST name the specific section, rule ID, or clause; vague “정책 위반” wording is explicitly a fail for E3.

4. **E4 (actionable fixes)** — Each finding row MUST include concrete remediation; problem-only descriptions fail E4.

5. **Finding template** — Required markdown table columns: Severity, Location, Issue, Policy Rule, Suggested Fix; minimal example row; `N/A (i18n/structure only)` for non-policy findings.

6. **Output Structure** — Findings section now defers to the template (optional ID/category columns allowed).

### Artifacts

- Baseline: `autoimprove-ux-copy-audit/SKILL.md.baseline` (v1.1.0 snapshot before mutations).
- Eval rubric: `autoimprove-ux-copy-audit/eval-criteria.md`.

### Line budget

Post-mutation `SKILL.md`: 140 lines (under 500).
