# Design Audit Output Template

Use this template for the Step 3 Design Plan output.

---

## Report Structure

```
DESIGN AUDIT RESULTS

Overall Assessment: [1-2 sentences on the current state of the design]

PHASE 1 — Critical
Issues that actively hurt usability, responsiveness, or visual hierarchy.
- [Issue/Component]: What is wrong -> What it should be -> Why this matters
- [Issue/Component]: What is wrong -> What it should be -> Why this matters
Review: [Reasoning for why Phase 1 items are highest-priority]

PHASE 2 — Refinement
Spacing, typography, color, alignment, and consistency adjustments that elevate the experience.
- [Issue/Component]: What is wrong -> What it should be -> Why this matters
- [Issue/Component]: What is wrong -> What it should be -> Why this matters
Review: [Reasoning for Phase 2 sequencing]

PHASE 3 — Polish
Micro-interactions, transitions, empty states, loading states, error states, dark mode,
and subtle details that make it feel world-class.
- [Issue/Component]: What is wrong -> What it should be -> Why this matters
- [Issue/Component]: What is wrong -> What it should be -> Why this matters
Review: [Reasoning for Phase 3 items and expected cumulative impact]

DESIGN_SYSTEM.md / LESSONS.md UPDATES:
- (New tokens, colors, spacing values, typography changes, or component additions)
- These must be approved and posted before implementation begins.
```

## Implementation Notes for the Build Agent

These rules govern how approved phases are executed:

- Each property and value is a visual choice — never add arbitrary values.
- No defaults: specify exact token references from DESIGN_SYSTEM.md.
- Written so the build agent can execute without design interpretation.
- Once a phase is approved, change only what was approved.
- Do not touch anything outside the approved phase — save it for the next phase.
- If the result does not feel right after implementation, propose a refinement pass before moving to the next phase. Keep refining until it feels absolutely right.

## Phase Approval Checklist

Before presenting each phase to the user:

- [ ] Every issue includes: what is wrong, what it should be, why it matters.
- [ ] All recommended values reference design system tokens, not arbitrary values.
- [ ] No issue requires application logic changes (flag separately if so).
- [ ] Before/after comparisons included where visual differences are non-obvious.
- [ ] Phase is self-contained — can be implemented independently of other phases.
