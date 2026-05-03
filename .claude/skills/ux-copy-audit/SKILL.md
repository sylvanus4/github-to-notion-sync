---
name: ux-copy-audit
description: >-
  Scan codebase for UI text strings; detect policy violations, inconsistent
  copy, missing translations, hardcoded strings, and tone misalignment.
  Cross-reference UX writing policy and design system guidance; produce an
  audit report with fixes. Korean triggers: "UX 카피 감사", "ux copy audit", "문구
  감사", "UI 텍스트 스캔", "copy audit", "문구 일관성 스캔", "UI 문자열", "하드코딩 문구". Do NOT use
  for generating new UX copy from scratch only (use ux-writing-agent),
  policy-to-UI batch generation (use policy-text-generator), or WCAG-only
  audits without copy scope (use accessibility-focused skills).
---

# UX Copy Audit

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Purpose

Systematically surface UI string debt: inconsistency, policy risk, i18n gaps, and tone drift before release. Bridges engineering artifacts and planning-owned UX standards.

## Prerequisites

- Repository paths that contain user-facing UI (web, mobile, desktop) agreed with the user.
- If policy-driven: Notion UX writing page URL or export.
- Optional: list of supported locales and the i18n library in use (`react-i18next`, `formatjs`, etc.).

## Success criteria

- Every **Critical** finding ties to an explicit policy clause or accessibility/legal risk.
- Hardcoded strings are listed with **file:line** or build-time key path.
- Recommendations are **implementable** (suggested key name, Korean rewrite, or removal of duplicate).

## Finding requirements (binary eval compliance)

**Location (E1)** — Every finding MUST include a traceable reference: repository **`path/to/file.tsx:42`** (file:line) **or** a build-time / i18n locator such as **`namespace:key`** or **`ComponentName.i18nKey`**. Screen-only labels (“설정 화면”) without file, line, or key path are **not** acceptable.

**Severity (E2)** — Assign exactly one level per finding using this rubric:

| Severity | When to use |
|----------|-------------|
| **Critical** | Policy violation with direct user impact (misleading copy, PII/legal wording risk, or accessibility copy failure **as defined in policy**). |
| **High** | Same user intent expressed inconsistently **across multiple screens or flows**; systemic term or tone drift. |
| **Medium** | Single-instance tone mismatch, clarity issue, or isolated inconsistency. |
| **Low** | Minor phrasing polish; optional consistency improvement with low risk if deferred. |

**Policy linkage (E3)** — Any policy- or guideline-related finding MUST cite the **specific** breached rule: section title, rule ID, or quotable clause from the UX writing / brand / error-message source. Generic phrases like “정책 위반” or “가이드 미준수” without naming the rule **fail** E3.

**Actionable fix (E4)** — Each row MUST include a **concrete** remediation: exact replacement string (Korean where applicable), i18n key name / extraction step, or “remove duplicate; keep canonical key X.” Problem-only descriptions **fail** E4.

### Finding table template (required shape)

Reports MUST use a markdown table with exactly these columns (row cells in Korean except paths/keys):

| Severity | Location | Issue | Policy Rule | Suggested Fix |
|----------|----------|-------|-------------|---------------|
| Medium | `src/ui/Toast.tsx:88` | … | … | … |

- **Policy Rule** — Use `N/A (i18n/structure only)` when the finding is not policy-backed but still needs a fix.
- **Location** — Always the file:line or key path from E1.

## Inputs

1. **Repository paths** (required) — Frontend roots, shared `packages/ui`, localization folders.
2. **Policy source** — Notion UX writing guidelines, brand voice, error-message rules.
3. **Design references** — Optional Figma links or Notion design specs for label intent.
4. **Locales** — Expected languages; default assumption: user-facing Korean with English technical terms where defined.

## Procedure

1. **Discover strings** — Search for patterns: JSX/TSX text nodes, `t('…')` / i18n keys, `aria-label`, `title`, `placeholder`, toast and error constructors, enum labels exposed to users.
2. **Bucket strings** — Categorize: navigation, forms, errors, empty states, confirmations, marketing-in-product.
3. **Policy cross-check** — Compare against Notion rules: forbidden phrases, required honorifics, max length, error structure (cause + next step), PII wording.
4. **Consistency pass** — Cluster near-duplicates (same intent, different wording or languages); flag mixed languages in one flow.
5. **i18n hygiene** — Flag hardcoded user-visible literals outside resource files; missing keys for declared locales; fallback exposure.
6. **Tone** — Check imperative vs polite consistency, product voice, and severity-appropriate error tone.
7. **Prioritize** — Rank by user exposure (primary flows first) and compliance risk.
8. **Deliver** — Spreadsheet-style markdown table + narrative recommendations; optional key-by-key suggested rewrites (Korean).

### Workflow notes

- De-duplicate identical strings across files before reporting counts to avoid noise.
- Treat **developer-only** logs and Sentry messages as out of scope unless the user asks otherwise.
- For design-system components, distinguish **library default strings** from product overrides.

## Integrations

- **Notion MCP** — Fetch policy pages; publish audit summary page with title per team convention (Korean) and date stamp.
- **Slack MCP** — Notify channel with Critical policy violations in thread.
- **Google Workspace CLI (`gws`)** — Share audit Doc or Drive link if reviewers prefer Docs comments.

### Publishing checklist

1. Attach or link evidence snippets in Notion (avoid pasting secrets).
2. Slack: main post = counts + link; thread = Critical policy rows only.
3. Optional: export table TSV for Sheets via paste in chat.

## Output Structure

- Scan scope and file counts.
- Summary: total strings, hardcoded count, policy hits, i18n gaps.
- Findings: ID, severity, category, string or key, location, rule violated, recommendation.
- Backlog suggestions grouped by sprint-sized batches.

## Examples

- **Input:** "Audit `apps/web` against our UX writing Notion page." **Output:** Korean report listing 30 findings with file:line and suggested replacements.
- **Input:** "Are checkout errors compliant?" **Output:** Focused table on checkout error strings only with policy citations.
- **Input:** "Find mixed KO/EN in onboarding modals." **Output:** Clustered findings by screen with tone and i18n recommendations.

## Boundaries

- Not a substitute for **legal** review of regulated claims or financial disclaimers.
- Does **not** automatically change code; produces a report and suggested patches for humans or a follow-up coding task.

## Error Handling

- **Policy doc missing** — Run structural consistency and i18n scan only; mark policy section N/A.
- **Obfuscated bundles** — If only build output is available, note imprecision and request source paths.
- **Dynamic composition** — Flag patterns where safe verification needs runtime review; do not guess final user-visible text.
- **Third-party components** — Exclude vendor-owned copy unless product overrides; document exclusions.
- **Encrypted or minified assets** — Skip with explicit note; request source maps or dev builds.
- **Plural/gender grammar** — If i18n ICU messages are required, flag as implementation follow-up, not a single static string fix.

## Evolution

Binary eval hooks (skill-autoimprove / audits). Each: **PASS** if true, **FAIL** otherwise.

| Hook | Criterion |
|------|-----------|
| **E1** | Audit report includes file:line (or agreed key-path) references for findings. |
| **E2** | Severity properly classified (Critical/High/Medium/Low per report rubric). |
| **E3** | Policy violations link to source policy clause or section. |
| **E4** | Actionable fix suggestions provided (rewrite, key name, or removal path). |
