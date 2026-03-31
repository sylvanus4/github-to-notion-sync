# Audience profiles

Use during **Transform** and **Enrich** phases of `tech-doc-translator`. Map CLI flags: `planner`/`pm` → Planner; `designer` → Designer; `ops` → Ops; `executive` → Executive; `all` → produce Planner + Designer + Executive (and Ops where relevant).

---

## Planner (PM / 기획자)

| Dimension | Guidance |
|-----------|----------|
| Technical level | Mid — knows APIs conceptually, not implementation |
| Focus | Scope, UX impact, schedule, constraints, data in/out |
| Depth | WHAT + WHY (minimal HOW) |
| Analogies | Daily life + product examples |
| Metrics | Concurrent users, perceived latency, storage from user POV |
| Omit | Implementation stack, infra topology, folder structure |

### Explanation template (Korean output)

```
[기능명]은 [일상 비유]와 비슷합니다.

가능한 것:
- …

불가능한 것 / 제약:
- …

숫자로 보면:
- …

기획에서 고려할 점:
- …
```

### Translation rules (technical → planner language)

| Technical | Planner framing |
|-----------|-----------------|
| API endpoint | "When the user [action], this capability runs" |
| DB schema | "Stored fields (name → Korean label)" |
| 4xx errors | User-caused → needs user-facing message |
| 5xx errors | Server issue → retry / contact guidance |
| Caching | "Faster repeat views; freshness tradeoff" |
| Rate limit | "Burst limit → queue or wait UX" |
| Async job | "Result not immediate; notify when done" |
| Pagination | "Paged loading, not all rows at once" |
| AuthN / AuthZ | Logged-in only / role-gated features |

---

## Designer

| Dimension | Guidance |
|-----------|----------|
| Technical level | Low–mid — UI patterns; weak on backend |
| Focus | UI states, interaction bounds, latency perception, field limits |
| Depth | WHAT + visible outcome (no server internals) |
| Analogies | Visual / familiar-product examples |
| Metrics | Loading time, row counts, image size caps |
| Omit | Server architecture, DB tuning, deploy mechanics |

### Extra checklist (Korean output)

- States to design: normal / loading / error / empty / disabled
- Heavy data: pagination vs infinite scroll vs "load more"
- Real-time: auto vs manual vs periodic refresh
- Offline: cache indicator vs error vs partial features

### Translation rules

| Technical | Designer framing |
|-----------|------------------|
| WebSocket | Real-time updates without full refresh |
| Max upload 5 MB | Upload UI cap + error state for oversize |
| HTTP 200 / 404 / 500 | Success / not-found / server-error screens |
| VARCHAR(N) | Max N chars + counter UX |
| ENUM | Select / radio options |
| Nullable | Empty state when allowed |
| ~200 ms latency | Feels instant; often no spinner |
| 2 s+ | Visible loading pattern |
| 10 s+ | Progress + cancel |

---

## Ops (운영 / CS)

| Dimension | Guidance |
|-----------|----------|
| Technical level | System flow; no code |
| Focus | Incidents, monitoring, CS scripts, where to verify data |
| Depth | Symptom → customer impact → comms |
| Omit | Code structure, algorithms |

### Translation rules

| Technical | Ops framing |
|-----------|-------------|
| Outage / error | Customer-visible impact + what to say |
| Deploy / maintenance | When users see downtime or readonly |
| Data location | Where to look up records / logs for tickets |

---

## Executive (경영진)

| Dimension | Guidance |
|-----------|----------|
| Technical level | Conceptual only |
| Focus | Cost, timeline, risk, competitiveness |
| Depth | WHAT + SO WHAT (business) |
| Analogies | Investment, runway, market |
| Omit | Terminology-heavy diagrams, code, deep architecture |

### Summary template (Korean output)

```
한 줄 요약: …

비즈니스 영향:
- 비용 / 일정 / 리스크

선택지:
| 옵션 | 비용 | 일정 | 리스크 | 권장 |
|------|------|------|--------|------|
| …    | …    | …    | …      | ★   |

결론: …
```

### Translation rules

| Technical | Executive framing |
|-----------|-------------------|
| Microservices | Faster isolated releases; smaller blast radius |
| Horizontal scaling | Traffic spikes; cost scales with usage |
| Technical debt | Higher future cost / incident risk |
| CI/CD | Faster, safer releases |
| SLA 99.9% | ~8.76 h downtime/year budget |
| Migration | Data move risk + schedule |

---

## Planning-implications frame (all audiences)

| Lens | Questions |
|------|-----------|
| Scope | What becomes possible or must be dropped? |
| UX | Speed limits, errors, empty states? |
| Business model | Usage-based cost impact? |
| Schedule | Complexity vs milestones? |
| Risk | What fails badly for users? |

## Decision-point format

For each open decision:

- **Decision** — what must be chosen
- **Options** — A/B with pros/cons
- **Technical hint** — neutral recommendation
- **Planning note** — extra PM considerations
