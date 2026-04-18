---
name: marketing-autoreason
description: >-
  Marketing Autoreason: knowledge-pack then core autoreason. Triggers: marketing
  autoreason, email subject tournament, blind panel, 마케팅 오토리즌. Not metric-only tuning
  (hypothesis-marketing); needs task_spec (kwp-marketing-content-creation).
metadata:
  author: thaki
  version: 1.0.0
  category: marketing
references:
  core_skill: ../../automation/autoreason/SKILL.md
---

# Marketing Autoreason

Orchestrates the **autoreason** tournament (`../../automation/autoreason/SKILL.md`) for marketing outputs (positioning, hooks, email subjects, ad briefs, landing sections, brand voice excerpts) with a **knowledge layer** assembled from durable evidence.

## Knowledge layer (assemble before pass 1)

Follow `references/knowledge-assembly.md`. Typical sources:

- Pasted metrics tables or GA/ESP exports (user-provided paths only).
- `kb-query` / `kb-search` on `knowledge-bases/` marketing or sales topics (read skill instructions first).
- `kwp-marketing-brand-voice` or internal voice markdown the user points to.
- Competitor positioning bullets from `kwp-marketing-competitive-analysis` outputs or user paste.

Concatenate into a single `knowledge_context` block (max ~4000 words; summarize with citations to file paths if longer).

If no evidence exists, set `knowledge_context` to a single line: `EVIDENCE: none` and proceed; judges use rubric only.

## Rubric override

Set judge rubric from `references/marketing-rubric.md` (five weighted dimensions). Pass the rubric text into each judge prompt as `{rubric_bullets}`.

## Prompt overrides

Use `references/marketing-prompts.md` appendices when filling critic / author / synthesizer templates from the core skill (marketing-specific bans on unsubstantiated metrics, competitor naming discipline, CTA clarity).

## Execution

1. Create run directory `outputs/autoreason/{date}/{run_id}/` (same as core skill).
2. Write `knowledge-pack.md` containing the assembled `knowledge_context` (audit trail).
3. Set `task_spec` to include channel, character limits, locale (default EN UI copy unless user requests Korean deliverable), and compliance notes.
4. Run the full **autoreason** pass loop from the core skill, reading/writing only under that directory.
5. On completion, optionally invoke `kwp-brand-voice-brand-voice-enforcement` on `final_output.md` if the user asked for a voice compliance check (separate pass, not inside blind judges).

## Outputs

In addition to core artifacts, always write:

| File | Purpose |
| ---- | ------- |
| `knowledge-pack.md` | Sources + excerpted evidence |
| `marketing-manifest.json` | Channel, locale, rubric version, pointers to KB queries used |

## Do NOT

- Fabricate open rates, CTR, or revenue; only cite user or KB-sourced numbers.
- Let judges see raw analytics spreadsheets; only the distilled `knowledge_context`.
- Skip blind labeling or merge judge steps into one chat turn.

## Verification

Confirm `final_output.md`, `history.json`, `knowledge-pack.md`, and `marketing-manifest.json` exist. Cross-check that every numeric claim in `final_output.md` appears in `knowledge-pack.md` or remove it.

**VERDICT:** PASS only after numeric claim trace check when stats were supplied.
