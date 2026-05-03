---
name: code-review-all
description: Full-project adversarial code review with 3 parallel agents — crash/bug checklist, abnormal behavior scenarios, and hacker-perspective security review.
disable-model-invocation: true
---

Run a comprehensive adversarial code review across the entire project or specified scope.

## Three Parallel Review Agents

### Agent 1: Crash & Bug Checklist (7 items)
- Nil/null pointer dereference
- Unclosed resources (files, connections, channels)
- Race conditions and data races
- Integer overflow / underflow
- Unhandled error returns
- Infinite loops / recursion without bounds
- Panic in goroutines without recovery

### Agent 2: Abnormal Behavior Scenarios (30 scenarios)
- Edge cases in input validation
- Concurrent access patterns
- Network failure handling
- Timeout and retry behavior
- State corruption scenarios

### Agent 3: Hacker Perspective Security Review
- Injection vectors (SQL, command, template)
- Authentication bypass paths
- Authorization escalation
- Data exfiltration routes
- Cryptographic weaknesses

## Output

Each agent produces a 10-point severity-scored report. All output in Korean.

## Scoring

- 9-10: Critical — must fix before merge
- 7-8: High — should fix before release
- 5-6: Medium — fix in next sprint
- 1-4: Low — backlog
