# Changelog — daiso-nearby-stock autoimprove

## Eval Suite

```
EVAL 1: Product Filtering
Question: Did the agent correctly exclude non-product accessories (pouches, massagers, markers, towels, cases) from the final output?
Pass: Only actual target products appear in the output; no accessories unless the user asked for them
Fail: An accessory or unrelated item appears in the results table

EVAL 2: Korean Output Format
Question: Is the entire final output written in Korean with the three required sections (Nearby Stores Table, Product Inventory Matrix, Visit Recommendation)?
Pass: All three sections present, all labels and prose in Korean
Fail: Any section missing, or significant portions in English

EVAL 3: Visit Recommendation Quality
Question: Does the visit recommendation name a specific store and give at least one concrete reason (distance, stock variety, or parking)?
Pass: A specific store name with at least one supporting reason
Fail: Generic advice ("visit the closest store") or no recommendation at all

EVAL 4: Per-Unit Price Calculation
Question: Does the output include a per-unit price or value comparison for at least one product (e.g., "개당 500원")?
Pass: At least one per-unit calculation or value comparison present
Fail: Only total package prices shown with no per-unit breakdown

EVAL 5: Zero-Stock Honesty
Question: When a product has zero inventory at all nearby stores, does the output explicitly say so instead of omitting the product?
Pass: Zero-stock products shown with "재고 없음" or equivalent honest label
Fail: Zero-stock products silently omitted from the output
```

## Test Inputs

1. "잠실 아시아선수촌 근처 다이소에 골프공 재고 확인해줘"
2. "강남역 다이소에 건전지 있어?"
3. "홍대 다이소에 USB 허브 재고 확인해줘"

---

## Experiment 1 — KEEP (80% → 100%)

**Hypothesis:** EVAL 4 failed all 3 runs because per-unit price calculation was only shown in an example, not mandated.

**Mutation:** Added "**MUST** include per-unit price calculations for multi-pack products" with explicit examples for both multi-pack and single items to the Visit Recommendation section.

**Result:** 15/15 (100%) — all 3 runs now pass EVAL 4. No regression on other evals.

---

## Experiment 2 — KEEP (100% maintained)

**Hypothesis:** "건전지" search returns 267 results, causing agents to process excessive items or pick random ones.

**Mutation:** Added "If more than 5 candidates remain after filtering, keep only the top 5 by relevance" to Step 1.

**Result:** 15/15 (100%) — efficiency improvement, no eval regression.

---

## Experiment 3 — KEEP (100% maintained)

**Hypothesis:** Inventory results included stores 26km+ away, making "nearby" misleading.

**Mutation:** Added distance filtering: "keep only stores within 5km; expand to 10km if none found; discard beyond 10km" after Step 2 inventory call.

**Result:** 15/15 (100%) — strengthens EVAL 3 (visit rec quality). No regression.

---

## Experiment 4 — KEEP (100% maintained)

**Hypothesis:** Error handling for "no stores found" was vague ("use sido/gugun").

**Mutation:** Replaced with concrete example: `daiso_find_stores({ "storeQuery": "송파" })` instead of "잠실".

**Result:** 15/15 (100%) — error path improvement. No eval regression.

---

## Experiment 5 — KEEP (100% maintained)

**Hypothesis:** Zero-stock honesty (EVAL 5) was passing but lacked defensive reinforcement.

**Mutation:** Added "Never silently omit zero-stock products" explicit instruction to inventory matrix formatting.

**Result:** 15/15 (100%) — defensive hardening. No regression.

---

## Summary

| Metric | Value |
|--------|-------|
| Baseline | 80% (12/15) |
| Final | 100% (15/15) |
| Improvement | +20pp |
| Experiments | 5 |
| Kept | 5/5 |
| Discarded | 0/5 |
| Key fix | Experiment 1 (per-unit price MUST instruction) |
