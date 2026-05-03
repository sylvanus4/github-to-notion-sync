---
name: demo-analyzer
description: >-
  Analyze development demos (local or staging URLs) using browser automation:
  navigate flows, capture screenshots, enumerate UI states and edge cases, and
  produce a planner-friendly specification-oriented guide bridging dev demos
  to planning docs. Korean triggers: "데모 분석", "데모에서 기획서", "개발 데모 분석", "데모 상태
  추출". English triggers: "demo analyzer", "analyze demo", "staging
  walkthrough", "UI state extraction from demo". Do NOT use for production
  security testing, load testing, or code review; not a replacement for formal
  code-to-spec on private repos without a runnable demo.
---

# Demo Analyzer

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

Systematically **walk a demo** (local server or staging URL), **capture evidence**, and produce a **structured planner document**: screens, states, interactions, edge cases, open questions.

## Prerequisites

- Runnable **URL** and test account (if any); list **out-of-scope** actions (payments, destructive ops).
- **Browser MCP** (e.g. cursor-ide-browser / Playwright MCP): snapshot + screenshot support.

## Procedure

1. **Intake** — Record base URL, auth method, primary user journeys to cover, browsers viewport, and **stop conditions** (max N screens, no PII entry).

2. **Environment check** — Open URL; if blocked (login, VPN), stop and report **blocker** with screenshot.

3. **Exploration plan** — Ordered journey list (happy path first). For each step: action → expected result hypothesis → verify via snapshot.

4. **Capture** — For each materially different view:
   - Save **screenshot** (name: `flow-step-NN-state-slug.png` conceptually in the report)
   - Record **DOM snapshot summary**: landmarks, primary CTAs, errors, empty states
   - Tag **state type**: default / loading / success / error / empty / permission-denied (infer conservatively)

5. **Edge probing** (non-destructive) — Where safe: invalid input, required field empty, navigation back, refresh mid-flow, slow network simulation **only if** tool supports it; otherwise document as **not verified** **in Korean** in the output.

6. **Synthesize document** — Write the full artifact **in Korean** with sections covering:
   - Overview (demo purpose, scope, limitations)
   - Screen inventory (table: screen id, description, entry path, screenshot reference)
   - State matrix (screen × state)
   - User flows (step-by-step)
   - Edge and error scenarios
   - Spec alignment checklist (fields, policy, copy, permissions)
   - Open questions

7. **Publish (optional)** — User may request **Notion MCP** page creation under a parent, or **Slack MCP** summary with thread for attachments note.

8. **Traceability** — Map each major UI state to a **flow step id** (F1, F2, …) used consistently in screenshots and tables.

## Browser tool protocol

- Start from a **fresh navigation** to the base URL; take a **snapshot** before each interaction batch.
- After actions that change layout (navigation, modal open, toast), take a **new snapshot** before the next click.
- Store screenshots with readable names in the user’s chosen artifact location; reference them in the Korean report.
- If login is required, stop and request **test credentials** or a **pre-authenticated** environment.

## Notion MCP handoff

- Create a child page under the user-provided parent with a Korean title following team convention (example pattern: category + “demo analysis” + date).
- Paste the Korean report as structured blocks; attach links to screenshot files if uploaded to Drive/Notion by separate steps.

## Slack MCP handoff

- Main message: goal, URL, pass/fail on access, count of states found.
- Thread: top risks, open questions, and links to Notion page if created.

## Output structure (sections must be written in Korean)

Follow **Procedure step 6**; include an evidence index (screenshot paths or MCP log references).

## Skill chain

- **demo-analyzer** — Runnable demos (local/staging URL): dynamic navigation, live UI states, screenshots.
- **code-to-spec** — No runnable demo: static code/PR analysis for contracts, flows, and implementation truth.
- Use **demo-analyzer** when a URL is available; use **code-to-spec** when only repository or diffs are available.

## Examples

- **Onboarding demo** — 6 screens, 2 error states, 1 empty state → matrix + flow + copy gaps.

- **Admin console demo** — Permission-denied states for multiple roles; document separate matrices per role if time permits.

## Quality checklist

- Every **error state** includes repro steps at a high level (non-destructive).
- Empty vs loading is distinguished; if unclear, mark indeterminate **in Korean** in the output.
- Open questions are **specific** (what decision is needed), not vague.

## Error Handling

- **CRITICAL — Scope confirmation**: Before expanding beyond agreed journeys, stop conditions, or non-destructive rules, obtain explicit user confirmation; refuse destructive or out-of-scope execution and list required manual verification **in Korean** in the output.
- **CRITICAL — Auth wall**: Document repro steps needed; do not guess credentials; stop until test credentials or a pre-authenticated environment is provided.
- **Flaky UI**: Retry once; then label unstable **in Korean** in the output.
- **iframe-only content**: Note inaccessible regions per browser tool limits.
- **Scope creep**: Strictly refuse destructive actions; list them as manual verification required **in Korean** in the output.

## Evolution

Binary eval hooks (pass/fail per run; aligned with `autoimprove-demo-analyzer/eval-criteria.md`):

- **E1 — Screen inventory completeness**: Numbered list/table of all navigable screens/states; descriptive names and entry paths; **fail** if screens only appear ad-hoc in prose.
- **E2 — State matrix coverage**: Structured matrix/table with **≥3 state types per major screen** (e.g. normal, error, plus loading or empty or permission); **fail** if only happy-path or prose-only.
- **E3 — Edge case identification**: **≥3** specific edge/boundary items per major feature with trigger and observed behavior; **fail** if generic error-handling only.
- **E4 — Screenshot evidence**: Findings backed by **visual reference** (screenshot name and/or URL-at-capture + snapshot summary); **fail** if UI assertions lack evidence.
- **E5 — Open question specificity**: Each question ties to a **specific screen/state** and **concrete behavior**; owner domain + next step; **fail** for vague “needs clarification” only.

## Project-Specific Overrides (AI Stock Analytics)

This skill operates under project-specific policies:

- `.cursor/skills/references/project-overrides/project-design-conventions.md` (POL-002 — Tailwind+Radix, Refined Swiss design system)
- `.cursor/skills/references/project-overrides/project-tech-stack.md` (POL-001 — frontend/backend libraries)

Key constraints:

- Frame UI state extraction around Tailwind + Radix patterns (this repo does not use TDS); expect financial data views with loading, empty, error, data, and partial states.
- Treat the frontend as React 19 + Vite 7 when inferring component patterns and build/runtime behavior.
