# Changelog v2 — audit-driven mutation run

Date: 2026-04-30 (continued)
Trigger: `/skill-optimizer` audit returned composite 7.6/10 (B+) with 3 weak dimensions
Mode: audit-rubric driven (not synthetic-eval) · gate: 1.20× growth from v2 baseline (10142 chars)

Audit dimensions targeted:
- Boundary Clarity: 6 → 9
- Output Quality: 7 → 9
- Overlap Detection: 6 → 9

---

## v2-1 — keep · audit composite 7.6 → 7.7

**Change:** Added a Claude prompt block to Pillar 2 (AEO). Symmetric with Pillars 1/3/4 — input list (4 items), 4-output spec (robots.txt diff, llms.txt content, FAQ schema audit table, Article schema gaps), output as one markdown file.
**Reasoning:** Audit flagged Pillar 2 as the only pillar without a copy-paste Claude prompt — output was checklist + snippets only, asymmetric with siblings.
**Audit dim affected:** Output Quality 7 → 9.
**Result:** char +725 (10142 → 10867). Pillar 2 now invocable with same workflow as 1/3/4.

## v2-2 — keep · audit composite 7.7 → 7.9

**Change:** Added a "When to use this vs `goose-seo-content-audit`" sentence at the top of Pillar 3.
**Reasoning:** Audit flagged direct overlap with `goose-seo-content-audit`. Disambiguation rule: this skill = integrated 4-pillar growth loop (live GSC/Ahrefs/GA); goose-seo-content-audit = standalone content-only deep audit. The reference also mentions `goose-programmatic-seo-planner` later in the Scope block.
**Audit dim affected:** Overlap Detection 6 → 9 (now resolves the conflict explicitly).
**Result:** char +414. No score regression on Pillar 3 prompt or thresholds.

## v2-3 — keep · audit composite 7.9 → 8.4

**Change:** Two coordinated edits:
- Frontmatter description: "$0 ad spend" → "organic-only"; appended explicit "Do NOT use for: paid search/SEM, Google Ads, social-only growth, sites with < 28 days of GSC data, ecommerce category-page optimization."
- New body section `## Scope` (before Pillar 1): "Use when" prerequisites (≥ 28d GSC data, editorial/docs/blog goal, deploy capability) + 6-item "Do NOT use for" list with redirect notes (e.g., programmatic SEO → `goose-programmatic-seo-planner`, local SEO → out of scope).
**Reasoning:** Audit flagged the strongest weakness — no explicit "Do NOT use" boundary. Anti-patterns covered execution mistakes, not skill-applicability mistakes (different concern). The "$0 ad spend" was also flagged as marketing-y noise in the trigger.
**Audit dim affected:** Boundary Clarity 6 → 9; Trigger Accuracy clarified (cleaner organic-only signal). Overlap further reinforced via planner cross-ref.
**Result:** char +958 (11281 → 12239). Growth ratio 1.207 — initially overshot the 1.20 cap by 25 chars. Fixed in v2-4.

## v2-4 — keep · audit composite 8.4 → 8.5

**Change:** Two compressions to fit the growth gate:
- Required Files section (5 bullets, ~280 chars) → single inline line.
- Anti-Patterns intro (75 chars) → removed.
**Reasoning:** Audit recommendation #6 already said Required Files was redundant with Pillar 2 / anti-patterns / sprint table. The intro line was decorative. Both removable without affecting any audit dimension.
**Audit dim affected:** Conciseness 9 → 8 (still well under 500 lines, but body grew 19% net). Other dims unchanged.
**Result:** char -160 (12239 → 12079). Growth ratio 1.191 — gate PASS (cap 12170).

---

## v2 final score

| Dimension | v1 | v2 | Δ |
|---|---|---|---|
| Trigger Accuracy (2x) | 9 | 9 | 0 |
| Boundary Clarity | 6 | **9** | +3 |
| Structure | 8 | 8 | 0 |
| Conciseness | 9 | 8 | -1 |
| Overlap Detection | 6 | **9** | +3 |
| Output Quality | 7 | **9** | +2 |
| Testability | 7 | 7 | 0 |

**Composite:** v1 7.6 (B+) → v2 **8.5 (A)**
Calc: (9×2 + 9 + 8 + 8 + 9 + 9 + 7) / 8 = 68/8 = 8.5

## Stop reason

Audit ceiling — top 3 weak dimensions (6→9, 7→9, 6→9) all closed. Remaining dimensions are either at-cap or flat (Trigger 9, Structure 8, Testability 7). Pushing Conciseness back to 9 would require removing case-study color (Quick wins, Common findings) which has reader-attractor value beyond eval scope. Diminishing returns.

## Gates (v2 cumulative)

- max_chars 15000: PASS (12079)
- growth_rate 1.20× from v2 baseline (10142): PASS (1.191×, cap 12170)
- non_empty_body / trigger_preservation / boundary_preservation / section_structure: PASS

## Cross-cumulative size

v1 baseline 7956 → v2 final 12079 = 1.518× over both runs. Outside default per-run 1.20× but within absolute 15K cap and signal_ratio improved monotonically (0.62 → 0.80).
