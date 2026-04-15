# vllm-lmcache-integration

Reference architecture for integrating vLLM (inference engine) and LMCache (KV-cache persistence layer) with the LLM Wiki + MemKraft knowledge system. This is a **documentation-only** skill — the current system uses Cursor/Claude API for inference, not self-hosted vLLM. When self-hosted inference becomes viable, this document maps the integration points.

## Triggers

Use when the user asks to "plan vLLM deployment", "vLLM + LMCache architecture", "self-hosted inference", "KV cache reuse strategy", "vLLM 배포 계획", "LMCache 통합", "자체 호스팅 추론", "KV 캐시 재사용", "vllm-lmcache-integration", or wants to understand how self-hosted inference would integrate with the Wiki/MemKraft knowledge layers.

Do NOT use for current Cursor/Claude API optimization (use `ecc-token-strategy` rule).
Do NOT use for prompt cache preservation in the current system (use `ecc-token-strategy` rule).
Do NOT use for Kubernetes deployment review (use `sre-devops-expert`).
Do NOT use for model training (use `hf-model-trainer`).

## Status

**DEFERRED** — Document-only. No runtime components exist.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Request                           │
│                    (ai-brief, ai-recall, etc.)                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ai-context-router                           │
│         Assembles context from MemKraft + LLM Wiki              │
│         Tags with provenance ([COMPANY], [PERSONAL], etc.)      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      vLLM Inference                             │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    LMCache Layer                          │  │
│  │                                                           │  │
│  │  ┌─────────────────┐  ┌──────────────────────────────┐   │  │
│  │  │  Wiki KV Cache   │  │    MemKraft Session Cache    │   │  │
│  │  │  (long-lived)    │  │    (per-user, recency)       │   │  │
│  │  │                  │  │                              │   │  │
│  │  │  Company policy  │  │  HOT-tier entries            │   │  │
│  │  │  Team runbooks   │  │  Active preferences          │   │  │
│  │  │  Product docs    │  │  Unresolved items            │   │  │
│  │  │  API references  │  │  Recent session context      │   │  │
│  │  └─────────────────┘  └──────────────────────────────┘   │  │
│  │                                                           │  │
│  │  Cache Hierarchy: GPU VRAM → CPU RAM → SSD → Evict       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Model: Qwen-3 72B / Llama-4 or equivalent                     │
│  Serving: vLLM with PagedAttention + chunked prefill            │
└─────────────────────────────────────────────────────────────────┘
```

## KV Cache Attachment Points

### 1. Wiki System Prompt Cache (Long-lived)

LLM Wiki content is **stable and shared across users/sessions**. This makes it ideal for LMCache's prefix-sharing KV reuse.

| Cache Segment | Content Source | TTL | Invalidation |
|---|---|---|---|
| Company Wiki prefix | `_wiki-registry.json` → company-tier articles | 24h | On `wiki-promote` or `kb-compile` |
| Team Wiki prefix | `_wiki-registry.json` → team-tier articles | 12h | On team article update |
| System instructions | Static skill instructions + provenance rules | 7d | On skill file change |

**Mapping to `ecc-token-strategy`**: This parallels the "Content Ordering (cache-friendly)" section — Wiki content occupies positions 1-2 (static system prompt, project-level rules), which are the most cache-reusable positions.

```
vLLM request structure (cache-friendly ordering):
  1. System prompt + tool definitions     ← globally cached (LMCache L1)
  2. Wiki context (company + team)        ← shared across sessions (LMCache L2)
  3. MemKraft personal context            ← per-user cached (LMCache L3)
  4. Conversation messages                ← per-turn, not cached
```

### 2. MemKraft Session Cache (Per-user, Recency-weighted)

MemKraft HOT-tier entries are **user-specific but reused across turns** within a session. LMCache can cache the KV states for these prefixes per user.

| Cache Segment | Content Source | TTL | Invalidation |
|---|---|---|---|
| HOT preferences | `memory/preferences/*.md` | Session lifetime | On preference update |
| HOT recent context | `memory/topics/*.md` (HOT entries) | 4h | On topic file change |
| Unresolved items | `memory/unresolved/*.md` | Session lifetime | On resolution |

**Mapping to `ecc-token-strategy`**: This parallels position 3 (session context) — user-specific but stable within a session window.

### 3. Dream Cycle Cache Warmup

After the nightly Dream Cycle completes (tier transitions, preference promotions), the system can **pre-warm** LMCache with the updated HOT-tier MemKraft entries:

```
Dream Cycle completes
  → New HOT-tier entries identified
  → Pre-compute KV states for top-N HOT entries
  → Store in LMCache SSD tier for next-morning ai-brief
```

## LMCache Configuration Reference

```yaml
lmcache:
  backend: "ssd"    # GPU VRAM → CPU RAM → SSD hierarchy
  max_cache_size: "50GB"
  eviction_policy: "lru"

  prefix_groups:
    wiki_company:
      prefix_hash_key: "wiki-company-v{version}"
      ttl_hours: 24
      shared: true    # shared across all users

    wiki_team:
      prefix_hash_key: "wiki-team-{domain}-v{version}"
      ttl_hours: 12
      shared: true

    memkraft_hot:
      prefix_hash_key: "memkraft-{user_id}-hot"
      ttl_hours: 4
      shared: false   # per-user

    memkraft_preferences:
      prefix_hash_key: "memkraft-{user_id}-pref"
      ttl_hours: 24
      shared: false
```

## vLLM Serving Configuration Reference

```yaml
vllm:
  model: "Qwen/Qwen3-72B"    # or latest equivalent
  tensor_parallel_size: 4      # 4x A100/H100
  max_model_len: 65536
  enable_chunked_prefill: true
  enable_prefix_caching: true  # native vLLM prefix caching
  gpu_memory_utilization: 0.92

  lmcache_integration:
    enabled: true
    cache_dir: "/data/lmcache"
    preload_wiki_on_startup: true
```

## Cost-Benefit Analysis

### Current System (Cursor/Claude API)

| Dimension | Current State |
|---|---|
| Prompt caching | API-level prefix caching (Anthropic manages) |
| Wiki context | Loaded per-turn via rules/AGENTS.md (~20K tokens) |
| MemKraft context | Loaded per-turn via file reads (~5-10K tokens) |
| Cache control | Limited — `cache_control: ephemeral` markers only |
| Cost model | Pay per input/output token |

### Future System (vLLM + LMCache)

| Dimension | Future State |
|---|---|
| Prompt caching | Full KV-cache persistence (GPU → CPU → SSD) |
| Wiki context | Pre-computed, shared KV states across sessions |
| MemKraft context | Per-user KV cache with session-level reuse |
| Cache control | Fine-grained TTL, invalidation, and warmup |
| Cost model | Fixed GPU cost, amortized across requests |

### Migration Trigger Criteria

Move to self-hosted when ANY of these hold:

1. **Token volume**: >500K input tokens/day sustained → self-hosted is cheaper
2. **Latency**: TTFT >2s on API calls due to long Wiki context → KV cache eliminates re-prefill
3. **Privacy**: Sensitive company data cannot leave the network → on-prem required
4. **Customization**: Need fine-tuned model with domain-specific knowledge → vLLM serves custom checkpoints

## Relationship to Existing Rules

| Rule / Skill | Relationship |
|---|---|
| `ecc-token-strategy` | Cache ordering principles transfer directly; vLLM prefix caching replaces API-level caching |
| `ai-context-router` | Becomes the request builder for vLLM — assembles context in cache-friendly order |
| `unified-knowledge-search` | RRF results feed the context assembly; no changes needed |
| `memkraft-dream-cycle` | Dream Cycle output triggers cache warmup for next day |
| `wiki-company` / `wiki-team` | Wiki compile output triggers cache invalidation + rebuild |

## Implementation Checklist (Future)

When migration criteria are met:

- [ ] Deploy vLLM with LMCache on K8s (Helm chart in `charts/vllm-inference/`)
- [ ] Configure prefix groups for Wiki and MemKraft tiers
- [ ] Update `ai-context-router` to format requests for vLLM API instead of Anthropic API
- [ ] Implement cache invalidation webhooks (on `kb-compile` and `wiki-promote` events)
- [ ] Implement Dream Cycle → cache warmup pipeline
- [ ] Set up monitoring: cache hit rate, TTFT, KV cache utilization
- [ ] Run A/B test: API vs self-hosted latency and cost comparison
- [ ] Document rollback procedure to API-based inference
