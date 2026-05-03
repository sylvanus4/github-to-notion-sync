---
name: design-qa-checklist
description: >-
  Automated design QA against Refined Swiss rules: Radix UI patterns, Tailwind
  CSS v4 semantic token compliance (CSS custom properties), WCAG AA checks,
  spacing and typography, responsive behavior, and interaction patterns.
  Verifies tokens and components by referencing
  .cursor/rules/design-system.mdc. Produces a pass/fail checklist with
  screenshots where browser access allows. Korean triggers: "디자인 QA", "design
  qa", "디자인 품질 점검", "디자인 체크리스트", "design quality check", "QA checklist", "디자인
  검수", "DS 준수", "토큰 준수". Do NOT use for policy-document-only authoring (use
  policy-text-generator), DS changelog tracking only (use
  design-system-tracker), or product-level UX critique without DS rules (use
  uiux-expert).
---

# Design QA Checklist

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

Validate that screens and prototypes comply with **Refined Swiss** (Tailwind CSS v4 + Radix UI) and accessibility baseline before handoff or release. Converts rules into a repeatable checklist with evidence.

## Prerequisites

- Access to the artifact under test (URL or images).
- **Design system reference**: `.cursor/rules/design-system.mdc` — use it as the authoritative token and pattern list (semantic colors, spacing, typography, component recipes). Do **not** rely on `search_design_system` MCP or external published Figma libraries.
- Known themes (light/dark) if applicable.

## Success criteria

- Each **Fail** references evidence (screenshot, token diff, or WCAG measurement rationale).
- Checklist categories map to **actionable** fixes (design vs engineering vs content).
- **Needs manual review** is used honestly when automation cannot decide.

## Inputs

1. **Artifact** — Staging URL, Storybook URL, or exported screenshots path.
2. **Design system source** — `.cursor/rules/design-system.mdc` plus optional `docs/policies/` (e.g. POL-002).
3. **Viewport matrix** — e.g., 360, 768, 1280 widths; default mobile + desktop.
4. **Scope** — Whole page, single flow, or component set.

## Procedure

1. **Capture baseline** — Snapshot target states (default, hover, focus, disabled, error) via browser; store references for the report.
2. **Component usage** — Verify buttons, inputs, dialogs, tables, and navigation use **Radix UI** primitives and compositional patterns consistent with `design-system.mdc`; flag ad-hoc markup that bypasses semantic tokens.
3. **Token compliance** — Check color roles, spacing scale, typography scale, radius, elevation against **Tailwind semantic classes / CSS custom properties** from `design-system.mdc`. List raw `bg-blue-500`-style utilities or hardcoded hex/px outliers. **Do not** use Code Connect or Figma MCP for token authority.
4. **Radix patterns** — Verify focus management, `aria-*`, keyboard operability, and portal layering for dialogs, dropdowns, and tabs per Radix docs + project conventions.
5. **Accessibility (WCAG AA)** — Contrast for text and icons; focus order visibility; keyboard operability; heading hierarchy; touch target size (`min-h-[44px]` where applicable).
6. **Responsive** — Overflow, truncation rules, grid collapse, sticky regions, and safe areas at each viewport; **data tables** and **charts** get extra scrutiny.
7. **Interaction** — Loading states, empty states, error recovery, destructive confirmations, disabled vs hidden affordances.
8. **Verdict** — Per category: Pass | Fail | N/A | Needs manual review; cite screenshot or URL for each Fail.
9. **Handoff** — Prioritized fix list for design and engineering owners.

### Workflow notes

- Run **keyboard-only** pass on interactive pages when browser access exists (Tab, Enter, Escape).
- Capture **focus rings** in screenshots; missing focus styles default to Fail for primary actions.
- For data-dense tables, verify **horizontal scroll** and header stickiness on small viewports.

## Integrations

- **Notion MCP** — Create `[Design] QA Checklist — Feature — YYYY-MM-DD` with embedded links to evidence.
- **Slack MCP** — Post Pass/Fail summary; thread for Fail screenshots.
- **Browser MCP** — Capture screenshots and verify focus/contrast on live builds.

### Publishing checklist

1. Upload evidence images to Notion or link to the tested URL.
2. Slack summary with Pass/Fail counts; pin for the release train when requested.
3. Optional `gws` Calendar hold for design–dev bugbash if multiple Fails.

## Output Structure

- Context (artifact, viewports, reference: `design-system.mdc` revision note if known).
- Summary table: category × status × count of issues (token compliance + Radix/a11y).
- Detailed checklist with evidence links.
- Blockers vs nice-to-have.

## Examples

- **Input:** "QA the stock detail page on staging URL." **Output:** Korean checklist with fails (contrast, table scroll) and screenshots.
- **Input:** "Desktop QA for trading-quality dashboard — WCAG AA." **Output:** Contrast and touch-target section with annotated screenshots.

## Boundaries

- Does **not** judge product-market fit or copy strategy beyond DS and a11y baselines.
- Cannot certify **legal** compliance; only WCAG-oriented design/engineering signals.

## Error Handling

- **No live URL** — Rely on static images; mark motion/responsive items as manual.
- **Ambiguous tokens** — Flag unknowns explicitly; re-read `design-system.mdc` before guessing names.
- **Dynamic theming** — Test both default and dark if the app supports both; else document single-theme limitation.
- **Third-party embeds** — Exclude from DS compliance table or tag as `external`.
- **Animated or video UI** — Mark motion-related checks as manual; capture first frame only.
- **Auth-gated pages** — Request test credentials or a recorded walkthrough; otherwise scope to public shells.
