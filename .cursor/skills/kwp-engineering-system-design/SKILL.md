---
name: kwp-engineering-system-design
description: Design systems, services, and architectures. Trigger with "design a system for", "how should we architect", "system design for", "what's the right architecture for", or when the user needs
  help with API design, data modeling, or service boundaries. Do NOT use for this project's microservice architecture review — prefer backend-expert skill.
metadata:
  author: anthropic-kwp
  version: 1.0.0
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
