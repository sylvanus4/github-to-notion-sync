---
name: trading-trade-hypothesis-ideator
description: >-
  Generate falsifiable trade strategy hypotheses from market data, trade logs,
  and journal snippets. Use when the user asks to "generate trade hypotheses",
  "rank hypothesis cards", "strategy experiment design", "kill criteria for trades",
  "가설 카드 생성", "트레이드 가설", "실험 설계", or has structured input and wants ranked hypothesis cards with experiment designs and optional strategy.yaml export.
  Do NOT use for strategy backtesting (use trading-backtest-expert). Do NOT use for daily signals (use daily-stock-check).
metadata:
  author: tradermonty
  version: "1.0.0"
  category: research
  source: claude-trading-skills
  api_required: none
---

# Trade Hypothesis Ideator

Generate 1-5 structured hypothesis cards from a normalized input bundle, critique and rank them, then optionally export `pursue` cards into `strategy.yaml` + `metadata.json` artifacts.

## Mandatory Hypothesis-Card Output Shape (User-Facing)

Every ranked hypothesis response (including “오늘의 트레이딩 가설 카드”) **must** use this structure:

1. **Input Bundle Summary** — Source path or paste; list **≥3 numeric fields** copied from evidence (e.g., `win_rate`, `R`, `sample_n`, `drawdown %`) or state `insufficient numeric evidence` and ask for data.
2. **Ranked Cards** — For each card: `### H1 …` (or H2…) with subsections: **Claim**, **Falsification / Kill Criteria** (explicit), **Experiment** (holdout, sample size, metrics), **Evidence Quality** (per `evidence_quality_guide.md`).
3. **Scores** — Integer rank + qualitative tier; include at least one **probability or threshold number** from methodology (e.g., `min_trades=30`) not invented market stats.
4. **Pursue / Park / Kill** — Table: `Card | Decision | One-line rationale`.
5. **Risk Factors** — Data snooping, overfitting, regime change — at least one bullet.
6. **Provenance** — Numbers tied to `example_input.json` / user JSON / script output only.

**Closing:** One sentence: which card to **pursue first** and why (actionable).

If the user provides only free text, normalize into the JSON schema from `examples/example_input.json` before generating cards, or request the missing fields.

## Workflow

1. Receive input JSON bundle.
2. Run pass 1 normalization + evidence extraction.
3. Generate hypotheses with prompts:
   - `prompts/system_prompt.md`
   - `prompts/developer_prompt_template.md` (inject `{{evidence_summary}}`)
4. Critique hypotheses with `prompts/critique_prompt_template.md`.
5. Run pass 2 ranking + output formatting + guardrails.
6. Optionally export `pursue` hypotheses via Step H strategy exporter.

## Scripts

- Pass 1 (evidence summary):

```bash
python3 .cursor/skills/trading-trade-hypothesis-ideator/scripts/run_hypothesis_ideator.py \
  --input .cursor/skills/trading-trade-hypothesis-ideator/examples/example_input.json \
  --output-dir outputs/reports/trading/
```

- Pass 2 (rank + output + optional export):

```bash
python3 .cursor/skills/trading-trade-hypothesis-ideator/scripts/run_hypothesis_ideator.py \
  --input .cursor/skills/trading-trade-hypothesis-ideator/examples/example_input.json \
  --hypotheses outputs/reports/trading/raw_hypotheses.json \
  --output-dir outputs/reports/trading/ \
  --export-strategies
```

## References

- `references/hypothesis_types.md`
- `references/evidence_quality_guide.md`

## Examples

### Example 1: Pass 1 evidence extraction
**User:** "I have market data and trade logs. Run the hypothesis ideator to extract evidence."
**Action:** Runs `run_hypothesis_ideator.py --input example_input.json` for pass 1 normalization and evidence summary.
**Output:** Evidence summary and raw hypotheses in `outputs/reports/trading/`.

### Example 2: Full pipeline with export
**User:** "Generate hypotheses, rank them, and export pursue cards to strategy.yaml."
**Action:** Runs pass 1, then pass 2 with `--hypotheses`, `--export-strategies` to produce ranked cards and strategy artifacts.
**Output:** Ranked hypothesis cards, strategy.yaml and metadata.json for pursue hypotheses.

### Example 3: Strategy experiment design
**User:** "Design kill criteria and experiment structure for this trade hypothesis."
**Action:** Uses critique and ranking prompts to produce falsifiable criteria, sample size guidance, and experiment design.
**Output:** Hypothesis cards with kill criteria, evidence quality assessment, and experiment parameters.

## Error Handling

| Error | Action |
|-------|--------|
| Input JSON invalid or missing | Validate schema; use `examples/example_input.json` as reference |
| Hypotheses file not found for pass 2 | Run pass 1 first; pass 1 output becomes `--hypotheses` input |
| Export fails (strategy.yaml) | Check references/research_ticket_schema.md; ensure hypothesis matches exportable format |
| Guardrails reject hypothesis | Review hypothesis_types.md and evidence_quality_guide.md; refine input evidence |
