---
name: paper-auto-classifier
description: >-
  Automatically discover, classify, and route academic papers from arXiv RSS
  feeds and HuggingFace daily papers. Scores relevance to tracked research
  topics, routes high-relevance papers to Slack with summaries, and queues top
  papers for full review. Use when the user asks to "monitor papers",
  "auto-classify papers", "paper radar", "논문 자동 분류", "논문 레이더",
  "paper-auto-classifier", or wants automated paper discovery and routing. Do
  NOT use for reviewing a specific paper (use paper-review), looking up a
  known paper (use alphaxiv-paper-lookup), or general web research (use
  parallel-web-search).
---

# Paper Auto-Classifier

Automated paper discovery pipeline: poll sources, classify by relevance, summarize, and route to appropriate channels.

## When to Use

- As part of the daily Intel track (runs automatically)
- When setting up monitoring for a new research area
- To discover papers from overnight arXiv submissions

## Tracked Research Topics

Configurable topic registry with relevance keywords:

| Topic | Keywords | Weight |
|-------|----------|--------|
| LLM Infrastructure | inference, serving, vLLM, SGLang, TensorRT | 1.0 |
| GPU/Accelerator | CUDA, H100, B200, GPU cluster, NVLink | 0.9 |
| Kubernetes/Cloud | K8s, orchestration, scheduling, Kueue | 0.8 |
| Fine-tuning | LoRA, QLoRA, RLHF, DPO, SFT, distillation | 0.8 |
| AI Agents | agentic, tool use, MCP, agent framework | 0.9 |
| MLOps | model serving, monitoring, A/B testing | 0.7 |
| Security/Safety | alignment, guardrails, red-teaming, jailbreak | 0.7 |

## Workflow

### Step 1: Poll Sources

**arXiv RSS Feeds** (configurable categories):
- `cs.CL` — Computation and Language
- `cs.AI` — Artificial Intelligence
- `cs.DC` — Distributed Computing
- `cs.CR` — Cryptography and Security

**HuggingFace Daily Papers**:
```
hf papers list --date today
```

**Semantic Scholar Alerts** (if configured):
- Keyword-based alerts for tracked topics

### Step 2: Deduplicate

Check against `paper-archive` index to skip already-processed papers:
```
paper-archive check <arxiv-id>
```

### Step 3: Quick Classification

For each new paper, use LLM to classify:
- **Topic match**: Score 1-10 against tracked topics
- **Institution signal**: Bonus for Google, Meta, NVIDIA, OpenAI, Anthropic, MIT, Stanford
- **Community signal**: GitHub stars (if linked), Twitter mentions, HF trending rank
- **Recency**: Preference for papers < 7 days old

Composite relevance score = topic_match * 0.5 + institution * 0.2 + community * 0.2 + recency * 0.1

### Step 4: Tier and Route

| Tier | Score | Action |
|------|-------|--------|
| **A (Must Read)** | >= 8.0 | Full `paper-review` pipeline → `#deep-research-trending` |
| **B (Interesting)** | 5.0 - 7.9 | `alphaxiv-paper-lookup` quick summary → `#deep-research-trending` |
| **C (Archive)** | 3.0 - 4.9 | Archive in `paper-archive` with metadata, no Slack |
| **D (Skip)** | < 3.0 | Log and skip |

### Step 5: Post Summaries

For Tier A and B papers, post to Slack with structured format:

```
📄 [Tier A] Efficient LLM Serving with Dynamic Batching
Authors: Smith et al. (Google DeepMind)
Score: 8.7/10 | Topics: LLM Infrastructure, GPU

Key insight: Novel batching algorithm reduces P99 latency by 40%
while maintaining throughput on H100 clusters.

🔗 arxiv.org/abs/2403.12345
📊 Full review queued → estimated in 30 min
```

### Step 6: Daily Summary

End-of-day summary of paper radar activity:

```
Paper Radar — Daily Summary
============================
Papers Scanned: 156
Tier A (Full Review): 2
Tier B (Quick Summary): 8
Tier C (Archived): 23
Tier D (Skipped): 123

Top Papers:
1. [8.7] Efficient LLM Serving — Google DeepMind
2. [8.2] Agent Memory Architecture — Anthropic
```

## Error Handling

| Error | Action |
|-------|--------|
| arXiv RSS feed timeout | Retry after 5 min; if still fails, use HF papers only; note "arXiv unavailable" in daily summary |
| HF papers API unavailable | Retry with backoff; fall back to arXiv-only; report partial source in summary |
| Paper PDF download fails | Skip full review; post quick summary from alphaxiv-paper-lookup if available; log for manual review |
| Relevance scoring model error | Use fallback heuristic (keyword match only); flag papers for manual review; log model error |
| Slack channel not found | Fall back to default `#deep-research-trending`; log channel config error; continue pipeline |

## Examples

### Example 1: Daily paper scan
Automated trigger: Morning pipeline
Actions:
1. Poll arXiv and HF for new papers
2. Classify and score each paper
3. Route Tier A/B to Slack, archive Tier C
4. Queue Tier A for full review
Result: Team receives curated paper digest

### Example 2: Add new research topic
User says: "Start monitoring papers about mixture of experts"
Actions:
1. Add "MoE" topic to registry with keywords
2. Backfill: scan last 30 days for matching papers
3. Set up ongoing monitoring
Result: New topic tracked with initial paper backfill
