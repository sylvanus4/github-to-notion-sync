## SCQA Writing Framework

Apply the SCQA (Situation-Complication-Question-Answer) framework to structure any topic into a persuasive narrative for articles, threads, presentations, memos, and reports.

### Usage

```
# Structure a blog post
/scqa-writing "AI 에이전트가 SaaS를 대체한다는 주제로 블로그 글"

# Create a memo
/scqa-writing "Recommend switching from Jira to Linear" --format memo

# Twitter thread
/scqa-writing "Why most A/B tests fail" --format thread
```

### Workflow

1. **Gather Context** — Collect topic, audience, format, and tone
2. **SCQA Decomposition** — Break into Situation (shared context), Complication (tension), Question (inevitable), Answer (resolution)
3. **Format Adaptation** — Adapt SCQA structure to target format (article, thread, memo, presentation, report)
4. **Write and Polish** — Draft each section and verify narrative flow
5. **Nested SCQA** — For long-form documents, apply document-level and section-level SCQA

### Output

SCQA blueprint (reference) + full content in the target format with narrative tension from S→C→Q→A arc.

### Execution

Read and follow the `scqa-writing-framework` skill (`.cursor/skills/standalone/scqa-writing-framework/SKILL.md`).
