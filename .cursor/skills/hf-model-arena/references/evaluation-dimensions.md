# Evaluation Dimensions

## Scoring Dimensions and Weights

| Dimension | Weight | Metric | Higher is Better |
|-----------|--------|--------|-----------------|
| Accuracy / Quality | 0.40 | Task-specific (see below) | Yes |
| Latency (p50) | 0.20 | Milliseconds per sample | No (invert) |
| Memory Usage | 0.15 | Peak GPU MB | No (invert) |
| Throughput | 0.15 | Samples/second | Yes |
| Cost Efficiency | 0.10 | Quality / $/1K-inferences | Yes |

## Task-Specific Quality Metrics

| Task | Primary Metric | Secondary Metric |
|------|---------------|-----------------|
| Text Classification | Accuracy, Macro-F1 | Per-class F1 |
| Token Classification (NER) | Span-level F1 | Precision, Recall |
| Text Generation | BLEU, ROUGE-L | BERTScore |
| Summarization | ROUGE-1/2/L | Factual consistency |
| Question Answering | Exact Match, F1 | Answer quality |
| Code Generation | pass@1, pass@10 | Compilation rate |
| Translation | BLEU, chrF | TER |

## Normalization

### For "higher is better" metrics:
```
normalized = (value - min_value) / (max_value - min_value)
```

### For "lower is better" metrics (latency, memory):
```
normalized = 1 - (value - min_value) / (max_value - min_value)
```

Applied across the candidate pool for each dimension.

## Benchmarks by Domain

| Domain | Recommended Benchmarks | Dataset |
|--------|----------------------|---------|
| General LLM | MMLU, ARC, HellaSwag | Open LLM Leaderboard suite |
| Code | HumanEval, MBPP | openai/humaneval |
| Math | GSM8K, MATH | gsm8k |
| Korean | KoBEST, KLUE | KLUE benchmark |
| Multilingual | XNLI, XQuAD | facebook/xnli |
