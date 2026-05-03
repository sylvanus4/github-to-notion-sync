---
name: ce-hosted-agents
description: >-
  Hosted agent infrastructure patterns — sandbox lifecycle, pre-built images,
  warm pool strategies, self-spawning agents, multiplayer support, and
  multi-client architectures. Use when the user asks to "build background
  agent", "create hosted coding agent", "set up sandboxed execution",
  "implement multiplayer agent", or mentions background agents, sandboxed VMs,
  agent infrastructure, self-spawning agents, or remote coding environments.
  Do NOT use for local dev stack setup (use local-dev-runner or
  local-dev-setup). Do NOT use for Kubernetes deployment review (use
  sre-devops-expert). Do NOT use for general CI/CD pipeline design (use
  sre-devops-expert). Korean triggers: "호스팅 에이전트", "샌드박스 실행", "백그라운드 에이전트",
  "멀티플레이어 에이전트", "웜풀 전략".
disable-model-invocation: true
---

# Hosted Agent Infrastructure

Hosted agents run in remote sandboxed environments rather than on local machines. When designed well, they provide unlimited concurrency, consistent execution environments, and multiplayer collaboration. Session speed should be limited only by model provider time-to-first-token — all infrastructure setup must complete before the user starts their session.

## Core Concepts

### Sandbox Infrastructure

**Image Registry Pattern**: Pre-build environment images on a regular cadence (every 30 minutes) so synchronization is a fast delta, not a full clone.

**Snapshot and Restore**: Take filesystem snapshots at key points — after initial build, when agent finishes changes, before sandbox exit.

**Warm Pool Strategy**: Maintain pre-warmed sandboxes for high-volume repositories. Start warming as users begin typing (predictive warm-up).

### Speed Optimizations

- **Parallel file reading**: Allow reads before git sync completes; block only writes
- **Predictive warm-up**: Begin sandbox setup when user starts typing
- **Maximize build-time work**: Move dependency installation, DB setup, initial runs to image build

### Self-Spawning Agents

Build tools allowing agents to spawn new sessions for research, parallel subtask execution, and generating smaller PRs from large tasks. Expose three primitives: start session, read status, continue main work.

### Multiplayer Support

Design for multiplayer from day one — it is nearly free with proper synchronization architecture. Data models must not be tied to single authors. Pass authorship info per prompt, attribute code changes to the prompting user.

### Metrics That Matter

- Sessions resulting in merged PRs (primary success metric)
- Time from session start to first model response
- PR approval rate and revision count

## Examples

### Example 1: Warm pool sizing for burst traffic
Traffic spikes at market open; you size the warm pool from p95 concurrent sessions plus headroom so new users rarely wait on cold boots. Predictive warm-up when a user opens the IDE further hides latency without keeping idle sandboxes for every user.

### Example 2: Sandboxing untrusted agent code
User-submitted agents run in isolated VMs with no host credentials, network egress allowlists, and per-session filesystems. Snapshots before risky commands let you roll back if generated code tries to exfiltrate data or modify the image.

## Troubleshooting

1. **Cold start latency**: Use warm pools and predictive warm-up to eliminate perceived wait time.
2. **Image staleness**: Set a 30-minute rebuild cadence; monitor build failures.
3. **Sandbox cost runaway**: Set hard timeout limits and per-session cost ceilings.
4. **Auth token expiration mid-session**: Implement token refresh before sensitive operations.
5. **Git config in sandboxes**: Always set git identity explicitly; never assume carryover from images.
6. **State loss on sandbox recycle**: Snapshot before termination; extract artifacts before letting sandbox die.

## References

- [Infrastructure Patterns Reference](./references/infrastructure-patterns.md)
- Related CE skills: ce-multi-agent-patterns, ce-tool-design, ce-context-optimization, ce-filesystem-context
- External: Ramp background agent, Modal Sandboxes, OpenCode framework
