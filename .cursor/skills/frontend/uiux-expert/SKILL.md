---
name: uiux-expert
description: >-
  Thaki Cloud 제품군의 UI/UX 품질 관리, 제품 간 일관성 점검, 정책/패턴 기반 리뷰,
  진행 상황 정리, 정기 공유 자료 생성을 지원합니다. 5개 모듈을 선택적으로 실행하여
  기획/디자인팀의 주간 공유 및 크로스 프로덕트 UI/UX 통일성을 유지합니다.
  Use when the user asks to "UI/UX 리뷰", "디자인 품질 점검", "제품 간 일관성 확인",
  "정기 공유 준비", "UX 피드백", "디자인 정책 점검", "UI 통일성 검토",
  "uiux review", "design consistency check", "cross-product UX audit",
  "weekly design share", "UX quality feedback", or "design policy review".
  Do NOT use for Figma-to-code 구현 (use implement-screen or fsd-development),
  새 UI 컴포넌트 빌드 (use frontend-design), 디자인 시스템 토큰 생성 (use figma-to-tds),
  기획서/PRD 작성 (use pm-execution or kwp-product-management-feature-spec),
  or visual HTML 산출물 생성 (use visual-explainer).
  Korean triggers: "UI/UX 리뷰", "디자인 품질", "제품 일관성", "정기 공유",
  "UX 피드백", "디자인 정책", "UI 통일성", "크로스 프로덕트", "디자인 리뷰 공유".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "review"
---

# UI/UX Expert

Manage UI/UX quality across products and keep cross-product consistency. Automates weekly progress sharing and alignment rituals for planning and design teams.

> **Single-product mode**: When only one product is specified (or the project is a standalone app rather than a multi-product suite), the skill automatically adapts:
> - **Module 3 (cross-product consistency)** is skipped — there is nothing to compare.
> - **Module 1 (progress rollup)** focuses on internal screens/components instead of cross-product tracking.
> - **Module 4 (policy review)** uses project-local design rules (e.g. `.cursor/rules/design-system.mdc`, Tailwind config, Radix patterns) when TDS (`@thakicloud/shared`) is not present.
> - **"Thaki Cloud 제품군"** framing is replaced with the actual product name in all outputs.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Input

| Input | Description | Required |
|------|-------------|----------|
| **Module** | Which module(s) to run (default: all) | Optional |
| **Product name(s)** | Product(s) to cover (single product or multi-product; Module 3 auto-skips for single) | **Yes** |
| **Figma URL** | Design file link | Optional |
| **Notion page/DB** | Progress source | Optional |
| **Policy path** | Design policy / guidelines file | Optional |

### Module flags

- `--all` (default): run the full pipeline
- `--progress`: Module 1 only (progress rollup)
- `--quality`: Module 2 only (UX quality feedback)
- `--consistency`: Module 3 only (cross-product consistency)
- `--policy`: Module 4 only (policy/pattern review)
- `--share`: Module 5 only (share-ready packaging)

---

## Workflow

### Module 1: Progress rollup

Collect structured UI/UX status per product.

**1-1: Sources (parallel)**

- Notion DB: tasks In Progress / In Review
- Figma: recently changed pages (`get_metadata`)
- Slack: summarize recent design threads

**1-2: Structure per product**

- In-flight screens/components
- Completed since last share
- Blockers / dependencies
- Next-week plan

### Module 2: UX quality feedback

Evaluate screen-level quality.

**2-1: Context (parallel)**

- Figma: `get_design_context` + `get_screenshot`
- Implementation code when available
- Browser screenshots when shipped

**2-2: Assessment**

Use [references/review-checklist.md](references/review-checklist.md):

| Area | Critical examples |
|------|-------------------|
| Visual hierarchy | Primary action not discoverable |
| Spacing/rhythm | Tokens ignored / inconsistent |
| Typography | Unclear hierarchy (Major) |
| Components | Same job, different components |
| States | Missing loading/error/empty |
| Accessibility | WCAG 2.1 AA gaps (Major) |
| Responsive | Broken layouts (Major) |
| Interaction | Nonstandard patterns (Major) |

**2-3: Nielsen heuristics (1–10)**

Score each screen against the ten heuristics (visibility, match to world, user control, consistency, error prevention, recognition, flexibility, minimal design, error recovery, help).

### Module 3: Cross-product consistency

Map equivalent flows across products (login, dashboard, list, detail, settings) and shared components (nav, table, form, modal, toast).

Verify with [references/consistency-criteria.md](references/consistency-criteria.md):

| Check | Intent |
|-------|--------|
| Tokens | Color/spacing/type tokens align |
| Components | Same job → same TDS component |
| Interactions | Same action → same pattern |
| Labels | Same concept → same term |
| Layout | Similar screens share structure |
| Errors/empty states | Unified patterns |

### Module 4: Policy / pattern review

Load design policies (e.g. `.cursor/rules/design-*.mdc`), TDS guidelines, and any user-supplied policy doc.

| Violation | Severity |
|-----------|----------|
| TDS component bypass when alternative exists | Critical |
| Hard-coded color/spacing vs tokens | Critical |
| Nonstandard interaction | Major |
| Accessibility gaps | Major |
| Naming drift | Minor |
| Undocumented exceptions | Minor |

### Module 5: Share packaging

**5-1: Notion**

Create sub-page via Notion MCP:

- Title format: Korean title per output rule and team naming (category + product + date)
- Structure from [references/sharing-templates.md](references/sharing-templates.md)

**5-2: Slack**

Post to the planning automation channel: main summary + thread with details (counts, top Critical issues, week-over-week delta).

---

## Output format

Deliver the full report in Korean. Include: title with product name, review date, modules run, severity counts, PASS/FAIL (PASS when Critical = 0), per-module sections (progress, quality issues, consistency table, policy violations), and share links.

---

## Examples

### Example 1: Weekly full run

User: "Summarize Console + Monitor design progress this week and publish the review share"

Actions: gather Notion + Figma + cross-product consistency + policy check → Notion page + Slack summary (Korean).

### Example 2: Single-screen feedback

User: "UX feedback on Console dashboard — Figma: https://figma.com/..."

Actions: pull Figma context, run checklist + heuristics → Korean report with PASS/FAIL.

---

## Error handling

| Situation | Response |
|-----------|----------|
| Quality review without Figma | Use code/screenshots only; note visual parity limits |
| Notion unavailable | Write local markdown; instruct manual upload |
| No policy doc | Use heuristics + general TDS principles; invite policy for stricter review |
| Only one product | Skip Module 3; adapt Module 1/4 per single-product mode |
| Slack unavailable | Notion-only share |
| Truncated Figma MCP | Split nodes; use `get_metadata` to traverse |
