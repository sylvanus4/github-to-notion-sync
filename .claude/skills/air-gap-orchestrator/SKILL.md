---
name: air-gap-orchestrator
description: >-
  Air-gap compatible pipeline orchestrator that routes LLM calls to
  on-premises endpoints, manages approval gates, provides audit logging, and
  supports model fallback chains. Use when the user asks to "run in air-gap
  mode", "on-prem pipeline", "에어갭 모드", "온프레미스 파이프라인", "air-gap-orchestrator",
  or needs pipeline execution in secure/isolated environments. Do NOT use for
  standard cloud pipeline execution (use mission-control), general
  orchestration without air-gap requirements (use mission-control), or LLM API
  configuration (configure directly).
disable-model-invocation: true
---

# Air-Gap Orchestrator

Pipeline orchestration middleware for air-gapped and on-premises environments. Ensures all LLM calls route through approved on-prem endpoints with audit logging and approval gates.

## When to Use

- When deploying the "One Person, Six Teams" pipeline in enterprise environments
- When running pipelines in air-gapped networks (no internet access)
- When compliance requires all AI processing to stay on-premises
- For Samsung and similar enterprise deployments with strict data governance

## Configuration

### Environment Variables

```bash
# LLM routing
AIRGAP_MODE=true                          # Enable air-gap mode
LLM_PROVIDER=on-prem                      # on-prem | cloud | hybrid
LLM_BASE_URL=https://llm.internal:8443    # On-prem LLM endpoint
LLM_MODEL=thaki-32b                       # Default on-prem model
LLM_FALLBACK_MODEL=thaki-8b              # Fallback if primary unavailable

# Approval gates
APPROVAL_REQUIRED=true                    # Require human approval for actions
APPROVAL_CHANNEL=#approvals               # Slack channel for approval requests
APPROVAL_TIMEOUT=300                      # Seconds to wait for approval

# Audit
AUDIT_LOG_PATH=/var/log/ai-pipeline/      # Audit log directory
AUDIT_LEVEL=full                          # full | summary | minimal
```

### Model Routing Table

| Task Type | Cloud Model | On-Prem Model | Fallback |
|-----------|-------------|---------------|----------|
| Code review | claude-4 | thaki-32b | thaki-14b |
| Email drafting | claude-4 | thaki-32b | thaki-14b |
| Classification | claude-haiku | thaki-8b | thaki-8b |
| Strategy analysis | claude-4 | thaki-32b | thaki-14b |
| Summarization | claude-haiku | thaki-8b | thaki-8b |

## Workflow

### Step 1: Pre-Flight Check

Before executing any pipeline:

1. **Verify LLM endpoint**: Health check on `LLM_BASE_URL`
2. **Check model availability**: Confirm `LLM_MODEL` is loaded and responding
3. **Validate credentials**: Test authentication with on-prem endpoint
4. **Check storage**: Ensure audit log directory is writable
5. **Network isolation**: Verify no outbound internet access (if strict air-gap)

```
Air-Gap Pre-Flight Check
========================
LLM Endpoint: https://llm.internal:8443 ✅ (latency: 45ms)
Model: thaki-32b ✅ (loaded, GPU memory: 78%)
Fallback: thaki-8b ✅ (loaded)
Audit Log: /var/log/ai-pipeline/ ✅ (writable, 120GB free)
Network: Air-gap confirmed ✅ (no outbound connectivity)
```

### Step 2: LLM Request Interception

Wrap all skill LLM calls through the orchestrator:

```python
def route_llm_request(prompt, task_type, sensitivity):
    if os.getenv("AIRGAP_MODE") == "true":
        model = MODEL_ROUTING_TABLE[task_type]["on_prem"]
        base_url = os.getenv("LLM_BASE_URL")
    else:
        model = MODEL_ROUTING_TABLE[task_type]["cloud"]
        base_url = "https://api.anthropic.com"

    # Audit logging
    log_request(prompt_hash, task_type, model, sensitivity)

    response = call_llm(base_url, model, prompt)

    # Audit response
    log_response(response_hash, token_count, latency)

    return response
```

### Step 3: Approval Gates

For sensitive actions, require human approval before execution:

**Actions requiring approval**:
- Sending emails (`gws-email-reply`)
- Creating calendar events (`gws-calendar`)
- Posting to external Slack channels
- Creating GitHub PRs
- Modifying production infrastructure

**Approval flow**:
1. Post approval request to `APPROVAL_CHANNEL` with context
2. Wait for ✅ reaction (up to `APPROVAL_TIMEOUT` seconds)
3. If approved: proceed with action
4. If declined or timeout: skip action, log as "declined"

### Step 4: Audit Logging

Every pipeline action is logged:

```json
{
  "timestamp": "2026-03-19T14:30:00Z",
  "pipeline": "morning-ship",
  "skill": "deep-review",
  "action": "llm_call",
  "model": "thaki-32b",
  "prompt_hash": "sha256:abc123...",
  "response_hash": "sha256:def456...",
  "tokens_in": 2500,
  "tokens_out": 800,
  "latency_ms": 3200,
  "sensitivity": "internal",
  "approval": "auto",
  "user": "hyojung.han"
}
```

### Step 5: Data Residency Enforcement

Ensure no data leaves the air-gapped environment:
- Block outbound HTTP calls to external APIs
- Redirect web search to internal search index
- Use local document store instead of cloud services
- Cache all external tool outputs for offline use

## Integration

### With existing pipelines

Add `--air-gap` flag to any pipeline command:

```bash
/morning-ship --air-gap
/deep-review --air-gap
/eod-ship --air-gap
```

The orchestrator wraps the pipeline execution with all air-gap controls.

### With mission-control

When `mission-control` orchestrates multi-skill workflows, the air-gap orchestrator sits as middleware, intercepting and routing all LLM calls.

## Output

```
Air-Gap Pipeline Report
=======================
Pipeline: morning-ship
Mode: Air-gap (strict)
Duration: 12 minutes

LLM Calls: 34
  Model: thaki-32b (28 calls)
  Model: thaki-8b (6 calls, classification tasks)
  Total tokens: 125,000 in / 45,000 out
  Avg latency: 2.8s

Approval Gates: 3
  Approved: 2 (email reply, PR creation)
  Declined: 1 (external Slack post)

Audit Entries: 47 (written to /var/log/ai-pipeline/)
Data Residency: ✅ No external data transfer detected
```

## Error Handling

| Error | Action |
|-------|--------|
| On-prem LLM endpoint unreachable | Retry health check 3× with 5s delay; if still failing, abort pipeline and report endpoint status |
| All endpoints fail health check | Abort pipeline; log all endpoint URLs and errors; suggest checking network/firewall |
| Approval gate timeout | Skip the action; log as "approval_timeout"; do not proceed without explicit approval |
| Config file not found | Use environment variables as fallback; if both missing, abort with setup instructions |
| Model capability mismatch | Fall back to next model in chain (e.g., thaki-32b → thaki-14b); log capability downgrade |

## Examples

### Example 1: Air-gap morning pipeline
User says: "/morning-ship --air-gap"
Actions:
1. Pre-flight check on-prem LLM
2. Execute pipeline with LLM routing to on-prem
3. Approval gates for external actions
4. Full audit logging
Result: Morning pipeline completed entirely on-premises

### Example 2: Hybrid mode
User says: "Run review with on-prem LLM but cloud tools"
Actions:
1. Route LLM calls to on-prem
2. Allow non-LLM tool access (GitHub, Slack)
3. Audit all data flows
Result: Hybrid execution with LLM isolation
