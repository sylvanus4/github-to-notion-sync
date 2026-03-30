# vLLM Evaluation Details

## lighteval Task Format

Tasks use the format `suite|task|num_fewshot`:
- `leaderboard|mmlu|5` - MMLU with 5-shot
- `leaderboard|gsm8k|5` - GSM8K with 5-shot
- `lighteval|hellaswag|0` - HellaSwag zero-shot
- `leaderboard|arc_challenge|25` - ARC-Challenge with 25-shot

**Finding Available Tasks:**
https://github.com/huggingface/lighteval/blob/main/examples/tasks/all_tasks.txt

Extract the `suite|task|num_fewshot` portion (without trailing `0` version flag).

## inspect-ai Available Tasks

- `mmlu` - Massive Multitask Language Understanding
- `gsm8k` - Grade School Math
- `hellaswag` - Common sense reasoning
- `arc_challenge` - AI2 Reasoning Challenge
- `truthfulqa` - TruthfulQA benchmark
- `winogrande` - Winograd Schema Challenge
- `humaneval` - Code generation

## Hardware Recommendations

| Model Size | Recommended Hardware |
|------------|---------------------|
| < 3B params | `t4-small` |
| 3B - 13B | `a10g-small` |
| 13B - 34B | `a10g-large` |
| 34B+ | `a100-large` |

## Model-Index Format

```yaml
model-index:
  - name: Model Name
    results:
      - task:
          type: text-generation
        dataset:
          name: Benchmark Dataset
          type: benchmark_type
        metrics:
          - name: MMLU
            type: mmlu
            value: 85.2
          - name: HumanEval
            type: humaneval
            value: 72.5
        source:
          name: Source Name
          url: https://source-url.com
```

WARNING: Do not use markdown formatting in the model name. Use exact name from the table. Only use urls in the source.url field.
