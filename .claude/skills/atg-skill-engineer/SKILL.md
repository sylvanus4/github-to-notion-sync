---
name: atg-skill-engineer
description: >-
  Analyze and optimize Cursor skills for Agent Tool Gateway (ATG) integration.
  Audits tool calls, applies Amdahl's Law to calculate sequential bottlenecks,
  recommends ATG routing and optimization patterns (cache, dedup, batch,
  compress, parallel sandbox, schema filtering). Use when the user asks to
  "optimize skill for ATG", "reduce tool latency", "skill tool audit", "Amdahl
  analysis", "tool bottleneck", "skill performance", "gateway routing", "ATG
  skill optimization", "ATG 스킬 최적화", "도구 지연 최적화", "도구 병목 분석", "스킬 도구 감사",
  "게이트웨이 라우팅", "암달 분석". Do NOT use for ATG server development or editing
  gateway Go code (edit directly), general code review without
  tool-optimization intent (use deep-review), prompt-only optimization without
  tool-call analysis (use skill-autoimprove), tool schema design theory
  without ATG context (use ce-tool-design), or new skill creation from scratch
  (use create-skill, then invoke this skill afterward).
disable-model-invocation: true
---

# ATG Skill Engineer

Optimize any Cursor skill for the Agent Tool Gateway by auditing its tool calls, quantifying sequential bottlenecks via Amdahl's Law, and recommending concrete ATG patterns that reduce tool latency.

**Core insight (Jeff Dean, GTC 2026)**: AI agents reason 50x faster than humans, but the tools they call — Notion API, Slack API, GitHub API — were designed for human speed. Real-world agent speedup is capped at 2-3x because 60-75% of pipeline time is tool wait. The ATG attacks this bottleneck directly.

## Composability

This skill augments (does not replace) existing skill lifecycle skills:

| Workflow | Invocation Order |
|----------|-----------------|
| New skill creation | `create-skill` -> `atg-skill-engineer` (add tool optimizations) |
| Skill quality audit | `skill-optimizer audit` -> `atg-skill-engineer` (add latency dimension) |
| Prompt mutation loop | `skill-autoimprove` -> `atg-skill-engineer` (inform mutation hypotheses with tool data) |
| Tool schema design | `ce-tool-design` (theory) -> `atg-skill-engineer` (concrete ATG patterns) |

## Input

The user provides one of:
1. **Skill name** — a specific skill to analyze (e.g., `meeting-digest`, `paper-review`)
2. **Skill path** — a SKILL.md file path
3. **Skill category** — a directory under `.cursor/skills/` to scan in batch

If no input is provided, ask the user which skill to analyze.

## Execution: 5-Phase Pipeline

### Phase 1: Tool Call Audit

Scan the target SKILL.md and all files it references (other skills it composes, referenced scripts, workflow descriptions) to enumerate every external tool interaction.

**What to look for:**

- Notion MCP calls: `notion_search`, `notion_create_page`, `notion_get_page`, `notion_query_database`, etc.
- Slack MCP calls: `slack_send_message`, `slack_post_thread`, `slack_search_messages`, etc.
- GitHub MCP/CLI calls: `gh pr create`, `gh issue list`, `github_create_issue`, etc.
- Google Workspace CLI: `gws calendar`, `gws gmail`, `gws drive`, `gws sheets`, etc.
- Shell-based tool invocations: `WebFetch`, `defuddle`, `WebSearch`, etc.
- MCP tool calls via `CallMcpTool`: any server/tool combination
- HuggingFace CLI: `hf models`, `hf papers`, `hf datasets`, etc.
- NotebookLM MCP: `notebook_create`, `studio_create`, `source_add`, etc.
- Figma MCP: `get_design_context`, `get_screenshot`, `search_design_system`, etc.
- Toss Securities CLI: `tossctl` commands
- Browser automation: `browser_navigate`, `browser_snapshot`, etc.

**Output a tool-call inventory table:**

```markdown
| # | Tool Call | Type | Est. Latency | Cacheable | ATG Connector | ATG Status |
|---|-----------|------|-------------|-----------|---------------|------------|
| 1 | notion_search | read | 2-3s | yes | notion | Implemented |
| 2 | slack_post_thread | write | 1-2s | no | slack | Implemented |
| 3 | gws gmail list | read | 1-2s | yes | gws | Planned P1 |
| ... | ... | ... | ... | ... | ... | ... |
```

### Phase 2: Amdahl's Law Analysis

Calculate the sequential fraction (S) and theoretical speedup ceiling for the skill.

**Formula:**

```
Speedup = 1 / (S + (1 - S) / N)

Where:
  S = sequential fraction = sum(tool_wait_time) / total_skill_time
  N = agent speedup factor = 50 (model speed relative to human)
  1 - S = parallelizable fraction (model reasoning, code generation)
```

**Reference latencies for estimation:**

| Operation | MCP (current) | ATG Phase 1 | ATG Phase 2 (cache hit) |
|-----------|--------------|-------------|------------------------|
| Notion page read | 2-3s | 200-400ms | <100ms |
| Notion search | 2-3s | 200-400ms | <100ms |
| Slack channel search | 1-2s | 300-500ms | <200ms |
| Slack post message | 1-2s | 300-500ms | N/A (write) |
| GitHub issue read | 1-2s | 300-500ms | <200ms |
| GitHub PR create | 1-2s | 500ms-1s | N/A (write) |
| GWS CLI invocation | 1-2s | 200-400ms (planned) | <100ms (planned) |
| NLM studio create | 30-120s | 30-120s (no speedup) | cached on retry |
| WebFetch | 1-5s | N/A (not ATG) | N/A |
| Shell command | 0.2-1s | N/A (local) | N/A |

**Calculate and present:**

```
Before ATG:
  Tool calls: N calls x avg_latency = total_tool_wait
  Model reasoning: estimated_reasoning_time
  S_before = total_tool_wait / (total_tool_wait + reasoning_time)
  Speedup_before = 1 / (S_before + (1-S_before)/50)

After ATG:
  Cached reads: X calls x <100ms = reduced_read_time
  Gateway writes: Y calls x 300-500ms = reduced_write_time
  Batch savings: Z independent calls batched = further_reduction
  S_after = reduced_total / (reduced_total + reasoning_time)
  Speedup_after = 1 / (S_after + (1-S_after)/50)

Net improvement: Speedup_after / Speedup_before
```

### Phase 3: ATG Optimization Recommendations

For each tool call identified in Phase 1, apply the applicable optimization patterns:

**7 ATG Optimization Patterns:**

| # | Pattern | When to Apply | Mechanism | Expected Gain |
|---|---------|--------------|-----------|---------------|
| 1 | Response Cache | Repeated read of the same resource across agents or within a pipeline | Valkey cache with TTL; `cacheable: true` in tool definition | 20-30x per cache hit (2s to <100ms) |
| 2 | Request Dedup | Multiple agents or subagents call the same tool with identical args simultaneously | Singleflight pattern collapses N concurrent identical requests to 1 API call | N-1 redundant calls eliminated |
| 3 | Tool Consolidation | Multi-step chain: search -> read -> extract -> format | Use agent-native tools (e.g., `notion_get_page_incremental` instead of `notion_get_page` + `notion_get_block_children`) | 2-3 calls reduced to 1 |
| 4 | Batch Execute | Multiple independent tool calls that do not depend on each other | Submit as DAG to `POST /api/v1/sandbox/execute`; gateway parallelizes internally | Sequential chain time / parallel branches |
| 5 | Schema Filtering | Skill loads all 179 tool schemas but uses only 5-15 tools | Request filtered schemas: `GET /api/v1/tools/schema?connector=notion` | 60-90% token savings (10K+ -> 1-2K tokens) |
| 6 | Response Compression | API response contains verbose metadata the agent does not need | Request compressed response: `compress: true` in tool call request | 85-96% response size reduction |
| 7 | Parallel Sandbox | Skill makes sequential tool calls that are actually independent | Declare as DAG with dependency edges; independent steps run concurrently | Proportional to parallelizable fraction |

**For each tool call, output:**

```markdown
| Tool Call | Applicable Patterns | Specific Recommendation |
|-----------|--------------------|-----------------------|
| notion_search (step 1) | Cache, Schema Filter | Route through ATG; 5min TTL; request only notion schemas |
| slack_post_thread (step 3) | Batch, Dedup | Batch with other Slack writes in step 4-5 |
| gws_gmail_list (step 2) | Cache (future P1) | Flag for ATG routing when GWS connector ships |
```

### Phase 4: Routing Decision Matrix

Classify every tool call into the correct routing path:

| Category | Prefix | Routing | Status |
|----------|--------|---------|--------|
| **ATG Native** | `notion_*`, `slack_*`, `github_*` | Route through ATG (`POST /api/v1/tools/call`) | Implemented (40 tools) |
| **ATG Planned P1** | `gws_*`, `nlm_*` | Use MCP/CLI now; flag `[ATG-P1]` in skill docs | Planned (weeks 3-5) |
| **ATG Planned P2** | `hf_*`, `figma_*` | Use MCP/CLI now; flag `[ATG-P2]` in skill docs | Planned (weeks 6-8) |
| **Direct MCP** | Browser tools, Daiso, Context7 | Use MCP server directly; no caching benefit | Not planned |
| **Direct CLI** | `tossctl`, `gws` (current), `hf` (current) | Use Shell tool; authentication-bound or local | Varies |
| **Local** | File generation (DOCX, PPTX, PDF) | No API call; runs locally | N/A |

**ATG call format** (for implemented connectors):

```json
{
  "tool": "notion_search",
  "connector": "notion",
  "arguments": {"query": "PRD-042", "filter": {"property": "status", "value": "In Progress"}},
  "agent_id": "pipeline-daily-am",
  "compress": true
}
```

**Endpoint reference:**

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/tools/call` | Execute a tool call (cache + dedup + audit applied automatically) |
| GET | `/api/v1/tools/schema` | Retrieve filtered tool schemas |
| GET | `/api/v1/health` | Check connector health |
| POST | `/api/v1/sandbox/execute` | Submit multi-step DAG for parallel execution |

### Phase 5: Optimization Report

Generate a structured report containing:

1. **Tool Call Inventory** — the Phase 1 table
2. **Amdahl's Law Analysis** — before/after S calculation with projected speedup
3. **Optimization Recommendations** — specific changes to the SKILL.md:
   - Which tool calls to route through ATG
   - Which calls to batch together
   - Which calls benefit from caching (and suggested TTL)
   - Which call chains to consolidate into single agent-native tools
   - Schema filtering recommendations
4. **Routing Map** — per-call routing decision (ATG / MCP / CLI / Local)
5. **Future Opportunities** — tool calls flagged `[ATG-P1]` or `[ATG-P2]` that will benefit when new connectors ship, with estimated additional speedup

**Summary format:**

```
Skill: <skill-name>
Tool calls audited: N
ATG-routable (now): X / N
ATG-routable (future): Y / N
S_before: 0.XX (speedup ceiling: X.Xx)
S_after:  0.XX (speedup ceiling: X.Xx)
Net improvement: X.Xx
Top recommendation: <single most impactful change>
```

## Reference: Implemented ATG Tools (40 Total)

### Notion Connector (14 tools)

| Tool | Cacheable | ReadOnly | Agent-Native |
|------|-----------|----------|-------------|
| `notion_search` | yes | yes | standard |
| `notion_get_page` | yes | yes | standard |
| `notion_get_database` | yes | yes | standard |
| `notion_query_database` | yes | yes | standard |
| `notion_get_block_children` | yes | yes | standard |
| `notion_create_page` | no | no | standard |
| `notion_update_page` | no | no | standard |
| `notion_get_page_incremental` | no | yes | agent-native |
| `notion_structured_search` | yes | yes | agent-native |
| `notion_batch_append_blocks` | no | no | agent-native |
| `notion_batch_flush` | no | no | agent-native |
| `notion_batch_status` | no | yes | agent-native |
| `notion_recent_changes` | no | yes | agent-native |
| `notion_invalidate_cache` | no | no | agent-native |

### Slack Connector (17 tools)

| Tool | Cacheable | ReadOnly | Agent-Native |
|------|-----------|----------|-------------|
| `slack_send_message` | no | no | standard |
| `slack_list_channels` | yes | yes | standard |
| `slack_get_channel_info` | yes | yes | standard |
| `slack_get_history` | yes | yes | standard |
| `slack_get_replies` | yes | yes | standard |
| `slack_search_messages` | yes | yes | standard |
| `slack_list_users` | yes | yes | standard |
| `slack_get_user_info` | yes | yes | standard |
| `slack_add_reaction` | no | no | standard |
| `slack_create_canvas` | no | no | standard |
| `slack_post_thread` | no | no | agent-native |
| `slack_render_template` | no | yes | agent-native |
| `slack_list_templates` | yes | yes | agent-native |
| `slack_queued_send` | no | no | agent-native |
| `slack_queue_status` | no | yes | agent-native |
| `slack_recent_events` | no | yes | agent-native |
| `slack_channel_activity` | no | yes | agent-native |

### GitHub Connector (9 tools)

| Tool | Cacheable | ReadOnly |
|------|-----------|----------|
| `github_list_repos` | yes | yes |
| `github_get_repo` | yes | yes |
| `github_list_issues` | yes | yes |
| `github_get_issue` | yes | yes |
| `github_create_issue` | no | no |
| `github_list_pulls` | yes | yes |
| `github_search_code` | yes | yes |
| `github_search_issues` | yes | yes |
| `github_graphql` | no | no |

## Reference: Priority Connector Roadmap

| Priority | Connector | Tool Count | Status | Top Skills |
|----------|-----------|-----------|--------|-----------|
| P0 | Notion, Slack, GitHub | 40 | Implemented | All pipeline skills |
| P1 | Google Workspace | ~11 | Planned (weeks 3-5) | `google-daily`, `gmail-daily-triage`, `morning-ship` |
| P1 | NotebookLM | ~10 | Planned (weeks 3-5) | `nlm-slides`, `nlm-video`, `paper-review` |
| P2 | HuggingFace Hub | ~8 | Planned (weeks 6-8) | `hf-trending-intelligence`, `hf-topic-radar` |
| P2 | Figma | ~5 | Planned (weeks 6-8) | `figma-dev-pipeline`, `figma-to-tds` |

## Reference: Production Baselines

| Pipeline | Current Time | Tool Fraction (S) | Speedup Ceiling |
|----------|-------------|-------------------|----------------|
| `/daily-am` (8 phases) | 15-20 min | 0.65-0.70 | 1.42-1.52x |
| `meeting-digest` | 3-5 min | 0.60-0.70 | 1.42-1.64x |
| `paper-review` | 10-15 min | 0.70-0.75 | 1.33-1.42x |
| `x-to-slack` (per URL) | 30-60 sec | 0.65-0.75 | 1.33-1.52x |
