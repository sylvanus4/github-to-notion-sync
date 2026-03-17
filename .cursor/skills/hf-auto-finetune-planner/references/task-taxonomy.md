# Task Taxonomy — HF Model Tags and Dataset Filters

Maps natural language task descriptions to Hugging Face Hub search parameters.

## Text Tasks

| Task Description | Model Tags | Dataset Tags | Training Method |
|-----------------|------------|-------------|-----------------|
| Sentiment analysis | `text-classification` | `sentiment`, `text-classification` | SFT |
| Named entity recognition | `token-classification` | `ner`, `token-classification` | SFT |
| Text summarization | `summarization` | `summarization` | SFT |
| Machine translation | `translation` | `translation` | SFT |
| Question answering | `question-answering` | `question-answering` | SFT |
| Text generation / Chat | `text-generation` | `conversational`, `instruction` | SFT / DPO |
| Code generation | `text-generation` | `code` | SFT |
| Instruction following | `text-generation` | `instruction-tuning` | SFT / DPO |
| Preference alignment | `text-generation` | `preference`, `dpo` | DPO |
| Math/reasoning | `text-generation` | `math`, `reasoning` | GRPO |

## Vision Tasks

| Task Description | Model Tags | Dataset Tags | Training Method |
|-----------------|------------|-------------|-----------------|
| Image classification | `image-classification` | `image-classification` | SFT |
| Object detection | `object-detection` | `object-detection` | SFT |
| Image captioning | `image-to-text` | `image-captioning` | SFT |

## Audio Tasks

| Task Description | Model Tags | Dataset Tags | Training Method |
|-----------------|------------|-------------|-----------------|
| Speech recognition | `automatic-speech-recognition` | `asr` | SFT |
| Audio classification | `audio-classification` | `audio-classification` | SFT |

## Language-Specific Keywords

| Language | Search Terms |
|----------|-------------|
| Korean | `korean`, `ko`, `한국어` |
| Japanese | `japanese`, `ja`, `日本語` |
| Chinese | `chinese`, `zh`, `中文` |
| Multilingual | `multilingual`, `multi` |
