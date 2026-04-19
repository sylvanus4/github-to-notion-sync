---
name: marketing-autoreason
description: >-
  Marketing Autoreason: knowledge-pack then core autoreason. Triggers: marketing
  autoreason, email subject tournament, blind panel, 마케팅 오토리즌. Not metric-only tuning
  (hypothesis-marketing); needs task_spec (kwp-marketing-content-creation).
metadata:
  author: thaki
  version: 1.1.0
  category: marketing
references:
  core_skill: ../../automation/autoreason/SKILL.md
  knowledge_feedback: references/knowledge-feedback.md
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
6. Run the **Post-Execution Knowledge Feedback** phase (see below).

## Post-Execution: Knowledge Feedback

After the tournament concludes, feed results back into the knowledge layer so future runs benefit from accumulated evidence. Follow `references/knowledge-feedback.md` for full design.

### 6a. Tournament Result Ingestion

Extract the winning copy and its judge scores from `final_output.md` and `history.json`. Append a structured entry to the KB marketing topic via `kb-ingest`:

1. Build a markdown snippet with heading `## Autoreason Winner — {date} — {channel}`.
2. Include: winning text (verbatim), composite Borda score, per-dimension rubric scores, task_spec summary (channel, locale, character limit), and the convergence round number.
3. Tag losers with one-line failure-mode labels (generic, off-brand, unsupported claim, etc.).
4. Ingest into `knowledge-bases/marketing-playbook/raw/` with filename `autoreason-winner-{run_id}.md`.
5. Write `feedback-receipt.json` in the run directory confirming ingestion path and timestamp.

### 6b. Campaign Performance Feedback (when available)

When the user supplies post-launch metrics (open rate, CTR, CVR, revenue lift) for a previously generated copy:

1. Locate the original run directory via `run_id` or date+channel match.
2. Create `campaign-results.md` in that run directory with actual vs. predicted performance.
3. Classify the outcome: `VALIDATED` (metrics met or exceeded expectations), `UNDERPERFORMED` (below baseline), or `INCONCLUSIVE` (insufficient data).
4. Ingest the classified result into `knowledge-bases/marketing-playbook/raw/` as `campaign-feedback-{run_id}.md`.
5. If `UNDERPERFORMED`, extract the failure hypothesis and append to the Copy exemplars > Losers section pattern in `knowledge-assembly.md` format.

### 6c. Knowledge Recompilation Signal

After ingesting new feedback artifacts (6a or 6b), emit a recompilation hint:

- Log a one-liner to `outputs/autoreason/kb-recompile-queue.txt`: `{date} {run_id} {type: winner|campaign}`.
- The next `kb-compile` or `kb-daily-build-orchestrator` run picks up queued items automatically.
- Do NOT run `kb-compile` inline during the tournament to avoid latency.

## Outputs

In addition to core artifacts, always write:

| File | Purpose |
| ---- | ------- |
| `knowledge-pack.md` | Sources + excerpted evidence |
| `marketing-manifest.json` | Channel, locale, rubric version, pointers to KB queries used |
| `feedback-receipt.json` | KB ingestion confirmation (path, timestamp, run_id) |

## Do NOT

- Fabricate open rates, CTR, or revenue; only cite user or KB-sourced numbers.
- Let judges see raw analytics spreadsheets; only the distilled `knowledge_context`.
- Skip blind labeling or merge judge steps into one chat turn.

## Verification

Confirm `final_output.md`, `history.json`, `knowledge-pack.md`, and `marketing-manifest.json` exist. Cross-check that every numeric claim in `final_output.md` appears in `knowledge-pack.md` or remove it.

**VERDICT:** PASS only after numeric claim trace check when stats were supplied.
