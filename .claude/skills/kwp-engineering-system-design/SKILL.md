---
name: kwp-engineering-system-design
description: >-
  Design systems, services, and architectures. Trigger with "design a system
  for", "how should we architect", "system design for", "what's the right
  architecture for", or when the user needs help with API design, data
  modeling, or service boundaries. Do NOT use for this project's microservice
  architecture review — prefer backend-expert skill. Korean triggers: "시스템
  설계", "아키텍처".
---

# System Design

Help design systems and evaluate architectural decisions.

## Before You Start

Before designing, ask the user to clarify (use AskQuestion):

1. **Problem scope** — What system or service needs to be designed? What problem does it solve?
2. **Scale requirements** — Expected users, requests/sec, data volume, growth rate?
3. **Constraints** — Team size, timeline, existing tech stack, budget limits?
4. **Non-functional priorities** — Rank: latency, availability, consistency, cost, simplicity?

DO NOT start designing until aligned on these inputs. A system designed for 100 users looks fundamentally different from one designed for 10 million.

## Framework

### 1. Requirements Gathering
- Functional requirements (what it does)
- Non-functional requirements (scale, latency, availability, cost)
- Constraints (team size, timeline, existing tech stack)

### 2. High-Level Design
- Component diagram
- Data flow
- API contracts
- Storage choices

### 3. Deep Dive
- Data model design
- API endpoint design (REST, GraphQL, gRPC)
- Caching strategy
- Queue/event design
- Error handling and retry logic

### 4. Scale and Reliability
- Load estimation
- Horizontal vs. vertical scaling
- Failover and redundancy
- Monitoring and alerting

### 5. Trade-off Analysis
- Every decision has trade-offs. Make them explicit.
- Consider: complexity, cost, team familiarity, time to market, maintainability

## Output

Produce clear, structured design documents with diagrams (ASCII or described), explicit assumptions, and trade-off analysis. Always identify what you'd revisit as the system grows.

## Examples

### Example 1: Typical request

**User says:** "I need help with engineering system design"

**Actions:**
1. Ask clarifying questions to understand context and constraints
2. Apply the domain methodology step by step
3. Deliver structured output with actionable recommendations

### Example 2: Follow-up refinement

**User says:** "Can you go deeper on the second point?"

**Actions:**
1. Re-read the relevant section of the methodology
2. Provide detailed analysis with supporting rationale
3. Suggest concrete next steps
## Error Handling

| Issue | Resolution |
|-------|-----------|
| Missing required context | Ask user for specific inputs before proceeding |
| Skill output doesn't match expectations | Re-read the workflow section; verify inputs are correct |
| Conflict with another skill's scope | Check the "Do NOT use" clauses and redirect to the appropriate skill |
