---
name: demo-analyzer
description: >-
  Analyze development demos (local or staging URLs) using browser automation: navigate
  flows, capture screenshots, enumerate UI states and edge cases, and produce a
  planner-friendly specification-oriented guide bridging dev demos to planning docs.
  Korean triggers: "데모 분석", "데모에서 기획서", "개발 데모 분석", "데모 상태 추출".
  English triggers: "demo analyzer", "analyze demo", "staging walkthrough",
  "UI state extraction from demo".
  Do NOT use for production security testing, load testing, or code review; not a
  replacement for formal code-to-spec on private repos without a runnable demo.
metadata:
  version: "1.0.0"
  category: analysis
  author: thaki
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

## Examples

- **Onboarding demo** — 6 screens, 2 error states, 1 empty state → matrix + flow + copy gaps.

- **Admin console demo** — Permission-denied states for multiple roles; document separate matrices per role if time permits.

## Quality checklist

- Every **error state** includes repro steps at a high level (non-destructive).
- Empty vs loading is distinguished; if unclear, mark indeterminate **in Korean** in the output.
- Open questions are **specific** (what decision is needed), not vague.

## Error handling

- **Auth wall**: Document repro steps needed; do not guess credentials.
- **Flaky UI**: Retry once; then label unstable **in Korean** in the output.
- **iframe-only content**: Note inaccessible regions per browser tool limits.
- **Scope creep**: Strictly refuse destructive actions; list them as manual verification required **in Korean** in the output.
