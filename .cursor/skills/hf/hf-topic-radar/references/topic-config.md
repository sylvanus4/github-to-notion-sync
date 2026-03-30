# Topic Configuration

Defines the AI topics to scan on HuggingFace Hub. Each topic has a display name,
HF filter tags (for `hf models ls --filter`), and free-text keywords (for space
search and paper filtering).

## Active Topics

### LLM (Large Language Models)
- **HF Tags:** `text-generation`, `text2text-generation`
- **Keywords:** `LLM`, `language model`, `GPT`, `Llama`, `Mistral`, `Qwen`, `Gemma`, `instruction tuning`, `chat model`, `reasoning`
- **Leaderboard:** Open LLM Leaderboard

### Multi-LLM / Multi-Modal
- **HF Tags:** `multimodal`, `image-text-to-text`, `visual-question-answering`, `any-to-any`
- **Keywords:** `multimodal`, `multi-modal`, `vision language`, `VLM`, `image understanding`, `audio language`, `omni`, `unified model`
- **Leaderboard:** Open VLM Leaderboard

### Video Generation
- **HF Tags:** `text-to-video`, `image-to-video`
- **Keywords:** `video generation`, `text-to-video`, `video synthesis`, `video diffusion`, `video model`, `motion generation`, `video editing`
- **Leaderboard:** VBench

## How to Add a Topic

Add a new H3 section following this format:

```markdown
### Topic Display Name
- **HF Tags:** `tag1`, `tag2`
- **Keywords:** `keyword1`, `keyword2`, `keyword3`
- **Leaderboard:** (optional) relevant benchmark name
```

HF Tags are used with `hf models ls --filter {tag}`.
Keywords are used for `hf spaces ls --search` and paper title matching.

## Notes

- Tags use the HuggingFace pipeline tag taxonomy
- Keywords are case-insensitive during matching
- A model/paper can match multiple topics; assign to the one with the most keyword hits
- Keep the topic list focused (3-5 topics) to avoid Slack noise
