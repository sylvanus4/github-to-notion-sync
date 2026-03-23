# Leaderboard Sources

## Open LLM Leaderboard

- **Primary Source:** HF Dataset `open-llm-leaderboard/results`
- **Extraction:** Use `hf-dataset-viewer` skill to query rows sorted by average score
- **Fallback URL:** `https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard`
- **Fallback Strategy:** If dataset not available, use `defuddle` on the Space URL; if Gradio blocks extraction, use `parallel-web-search` for cached results
- **Key Fields:** model name, average score, ARC, HellaSwag, MMLU, TruthfulQA, Winogrande, GSM8K
- **Categories:** pretrained, fine-tuned, chat, instruction-tuned, merged

## Chatbot Arena (LMSYS)

- **Primary URL:** `https://lmarena.ai/`
- **Extraction:** Use `defuddle` to extract the ranking table
- **Fallback:** `parallel-web-search` query `"chatbot arena leaderboard rankings 2026"`
- **Key Fields:** model name, Elo rating, 95% CI, votes, organization, license
- **Categories:** overall, coding, hard prompts, math, creative writing

## Video Generation Benchmarks

### VBench
- **Primary:** Search HF datasets for `vbench` via `hf datasets ls --search vbench`
- **Fallback URL:** `https://vchitect.github.io/VBench-project/`
- **Key Fields:** model name, overall score, subject consistency, motion smoothness, aesthetic quality

### EvalCrafter
- **Primary:** Search HF datasets for `evalcrafter`
- **Fallback URL:** `https://evalcrafter.github.io/`
- **Key Fields:** model name, overall score, visual quality, text alignment, motion quality

## Snapshot Storage

All snapshots use this JSON schema:

```json
{
  "date": "YYYY-MM-DD",
  "leaderboard": "source-name",
  "fetch_method": "dataset-viewer | defuddle | web-search",
  "rankings": [
    {
      "rank": 1,
      "model": "model-name",
      "score": 0.85,
      "params": "70B",
      "org": "organization",
      "details": {}
    }
  ]
}
```

## Update Frequency

- Open LLM Leaderboard: updates daily (new submissions evaluated)
- Chatbot Arena: updates weekly (Elo recalculation)
- Video benchmarks: updates irregularly (project-driven)
