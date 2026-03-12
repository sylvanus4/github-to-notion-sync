# HF Datasets Template Examples

## Chat Template (`--template chat`)

```json
{
  "messages": [
    {"role": "user", "content": "Natural user request"},
    {"role": "assistant", "content": "Response with tool usage"},
    {"role": "tool", "content": "Tool response", "tool_call_id": "call_123"}
  ],
  "scenario": "Description of use case",
  "complexity": "simple|intermediate|advanced"
}
```

## Classification Template (`--template classification`)

```json
{
  "text": "Input text to be classified",
  "label": "classification_label",
  "confidence": 0.95,
  "metadata": {"domain": "technology", "language": "en"}
}
```

## QA Template (`--template qa`)

```json
{
  "question": "What is the question being asked?",
  "answer": "The complete answer",
  "context": "Additional context if needed",
  "answer_type": "factual|explanatory|opinion",
  "difficulty": "easy|medium|hard"
}
```

## Completion Template (`--template completion`)

```json
{
  "prompt": "The beginning text or context",
  "completion": "The expected continuation",
  "domain": "code|creative|technical|conversational",
  "style": "description of writing style"
}
```

## Tabular Template (`--template tabular`)

```json
{
  "columns": [
    {"name": "feature1", "type": "numeric", "description": "First feature"},
    {"name": "target", "type": "categorical", "description": "Target variable"}
  ],
  "data": [
    {"feature1": 123, "target": "class_a"},
    {"feature1": 456, "target": "class_b"}
  ]
}
```
