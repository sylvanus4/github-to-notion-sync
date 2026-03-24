---
name: design-qa-checklist
description: >-
  Automated design QA against design system rules: component usage, token compliance,
  WCAG AA checks, spacing and typography, responsive behavior, and interaction patterns.
  Produces a pass/fail checklist with screenshots where browser or Figma MCP allows.
  Korean triggers: "디자인 QA", "design qa", "디자인 품질 점검", "디자인 체크리스트",
  "design quality check", "QA checklist", "디자인 검수", "DS 준수". Do NOT use for
  Figma-to-code implementation (use figma-dev-pipeline), DS changelog tracking only
  (use design-system-tracker), or product-level UX critique without DS rules
  (use uiux-expert).
metadata:
  author: thaki
  version: "1.0.0"
  category: review
---

# Design QA Checklist

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

Validate that screens and prototypes comply with the design system and accessibility baseline before handoff or release. Converts rules into a repeatable checklist with evidence.

## Prerequisites

- Access to the artifact under test (URL, Figma, or images).
- Design system reference: Notion rules and/or Figma library; latest token table if available.
- Known product themes (light/dark/high-contrast) if applicable.

## Success criteria

- Each **Fail** references evidence (screenshot, token diff, or WCAG measurement rationale).
- Checklist categories map to **actionable** fixes (design vs engineering vs content).
- **Needs manual review** is used honestly when automation cannot decide.

## Inputs

1. **Artifact** — Staging URL, Storybook URL, Figma frame(s), or exported screenshots path.
2. **Design system source** — Notion DS rules and/or Figma library name; token naming conventions.
3. **Viewport matrix** — e.g., 360, 768, 1280 widths; default mobile + desktop.
4. **Scope** — Whole page, single flow, or component set.

## Procedure

1. **Capture baseline** — Snapshot target states (default, hover, focus, disabled, error) via browser or Figma MCP; store references for the report.
2. **Component usage** — Verify buttons, inputs, modals, tables, and navigation match approved variants; flag custom styling that bypasses tokens.
3. **Token compliance** — Check color roles, spacing scale, typography scale, radius, elevation; list any raw hex or px outliers vs token map.
4. **Accessibility (WCAG AA)** — Contrast for text and icons; focus order visibility; keyboard operability for interactive controls; heading hierarchy; touch target size.
5. **Responsive** — Overflow, truncation rules, grid collapse, sticky regions, and safe areas at each viewport.
6. **Interaction** — Loading states, empty states, error recovery, destructive confirmations, and disabled vs hidden affordances.
7. **Verdict** — Per category: Pass | Fail | Needs manual review; cite screenshot or URL for each Fail.
8. **Handoff** — Prioritized fix list for design and engineering owners.

### Workflow notes

- Run **keyboard-only** pass on interactive pages when browser access exists (Tab, Enter, Escape).
- Capture **focus rings** in screenshots; missing focus styles default to Fail for primary actions.
- For data-dense tables, verify **horizontal scroll** and header stickiness on small viewports.

## Integrations

- **Notion MCP** — Create `[Design] QA Checklist — Feature — YYYY-MM-DD` with embedded links to evidence.
- **Slack MCP** — Post Pass/Fail summary; thread for Fail screenshots.
- **Figma MCP** — Read component properties and inspect frames when available.
- **Browser MCP** — Capture screenshots and verify focus/contrast on live builds.

### Publishing checklist

1. Upload evidence images to Notion or link to Figma frames.
2. Slack summary with Pass/Fail counts; pin for the release train when requested.
3. Optional `gws` Calendar hold for design–dev bugbash if multiple Fails.

## Output Structure

- Context (artifact, viewports, DS version if known).
- Summary table: category × status × count of issues.
- Detailed checklist with evidence links.
- Blockers vs nice-to-have.

## Examples

- **Input:** "QA the billing settings page on staging URL." **Output:** Korean checklist with 8 fails (contrast, spacing) and screenshots.
- **Input:** "Check Figma handoff frame `Invoice-Desktop`." **Output:** Token and component usage verdicts with frame references.
- **Input:** "Mobile QA for settings — WCAG AA." **Output:** Contrast and touch-target section with annotated screenshots.

## Boundaries

- Does **not** judge product-market fit or copy strategy beyond DS and a11y baselines.
- Cannot certify **legal** compliance; only WCAG-oriented design/engineering signals.

## Error Handling

- **No live URL** — Rely on Figma or static images; mark motion/responsive items as manual.
- **Incomplete token map** — Flag unknowns explicitly; do not guess token names.
- **Dynamic theming** — Test both default and dark if product supports both; else document single-theme limitation.
- **Third-party embeds** — Exclude from DS compliance table or tag as `external`.
- **Animated or video UI** — Mark motion-related checks as manual; capture first frame only.
- **Auth-gated pages** — Request test credentials or a recorded walkthrough; otherwise scope to public shells.
