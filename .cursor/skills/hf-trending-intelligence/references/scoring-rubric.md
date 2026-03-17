# Trend Scoring Rubric

## Composite Score Formula

```
trend_score = w1*S_paper + w2*S_models + w3*S_datasets + w4*S_discussions + w5*S_web
```

| Dimension | Weight | Source | Normalization |
|-----------|--------|--------|---------------|
| Paper upvotes | 0.30 | `hf papers ls` | min-max over day's papers |
| Model downloads | 0.20 | `hf models ls` | log10 scale, capped at 6 (1M downloads) |
| Dataset activity | 0.20 | `hf datasets ls` | count of associated datasets, capped at 10 |
| Discussion count | 0.15 | `hf discussions list` | count, capped at 20 |
| Web mentions | 0.15 | `parallel-web-search` | count, capped at 50 |

## Normalization Rules

### Min-Max (Paper Upvotes)
```
S = (value - min_value) / (max_value - min_value)
```
Applied across all papers in the daily batch.

### Log10 Capped (Model Downloads)
```
S = min(log10(total_downloads + 1) / 6, 1.0)
```
1M+ downloads = 1.0, 100K = ~0.83, 10K = ~0.67

### Count Capped
```
S = min(count / cap, 1.0)
```
Simple count normalized against a reasonable maximum.

## Classification Thresholds

| Score Range | Label | Meaning |
|-------------|-------|---------|
| >= 0.70 | **HOT** | High ecosystem activity, likely mainstream soon |
| 0.40 - 0.69 | **WARM** | Growing interest, worth monitoring |
| < 0.40 | **COOL** | Early stage, limited ecosystem presence |

## Tiebreakers

When scores are equal:
1. Higher paper upvotes wins
2. Higher model download count wins
3. More recent publication date wins
