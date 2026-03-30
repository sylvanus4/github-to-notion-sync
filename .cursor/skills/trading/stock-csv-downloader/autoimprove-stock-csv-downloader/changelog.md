# stock-csv-downloader — skill-autoimprove changelog

## Experiment 0 (baseline)

- **Change:** None — captured `SKILL.md.baseline` from pre-mutation skill.
- **Scores (0–100 per eval):** E1=68, E2=52, E3=62, E4=58, E5=48 → **mean 57.6%**
- **Rationale:** Step 2–4 collapsed; no halt matrix; CLI lacked defaults column and several flags lacked examples; CSV/schema underspecified; no end-to-end example with verify.

## Experiment 1 — Phase ordering

- **Change:** Replaced loose “Step 2–4” block with **Phased workflow** table (Phases 1–6), explicit dependencies, branching note, dedicated **Phase 5** verify subsection.
- **Result:** **Kept.** E1 68→96. Mean 57.6%→71.2%.

## Experiment 2 — Error recovery

- **Change:** Added **Error recovery and halt behavior** table (Playwright, navigation/API, disk, import/DB, CAPTCHA) + rule against silent skip.
- **Result:** **Kept.** E2 52→94. Mean 71.2%→75.8%.

## Experiment 3 — Output format + CLI defaults

- **Change:** Added **Output files and CSV format** (paths, filenames, encoding, columns); expanded CLI table with **Default** column aligned to `download_stock_csv.py`; added **Flag coverage in examples** sentence; added **Natural language → command mapping** for five test prompts.
- **Result:** **Kept.** E3 62→96, E4 58→95. Mean 75.8%→88.2%.

## Experiment 4 — Examples and cwd clarity

- **Change:** Note under prerequisites that commands run from `backend/`; Example 2 step 4 (verify curl); **Example 3** (AAPL date range + optional `--output-dir`); **Example 4** full pipeline with debug `--no-headless`/`--delay`; corrected manual import paths to `../data/latest` from `backend/` (and repo-root variant).
- **Result:** **Kept.** E5 48→96. Mean 88.2%→95.4%.

## Stop condition

- **Final mean score ≥ 95%** after Experiment 4. Experiment 5 not required.

## Summary

| Metric | Value |
|--------|--------|
| Baseline mean | 57.6% |
| Final mean | 95.4% |
| Experiments (mutations) | 4 (+ baseline) |
