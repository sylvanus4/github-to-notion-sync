---
name: ai-status
description: >-
  System health dashboard for the personal knowledge infrastructure. Reports
  MemKraft freshness scores, Wiki coverage, unresolved item count, Dream Cycle
  last run, and overall system readiness. Identifies knowledge gaps and
  maintenance needs. Use when the user asks "ai status", "knowledge health",
  "memory status", "system check", "ai-status", "AI 상태", "지식 건강", "메모리 상태",
  "시스템 점검", "MemKraft 상태", "위키 상태", "Dream Cycle 상태", or wants to check the
  health of their personal knowledge system. Do NOT use for application
  service health (use service-health-doctor). Do NOT use for KB topic-level
  lint (use kb-lint). Do NOT use for full KB coverage dashboard (use
  kb-coverage-dashboard). Do NOT use for Dream Cycle execution (use
  memkraft-dream-cycle).
---

# ai-status — Knowledge System Health Dashboard

Reports the health of the entire personal knowledge infrastructure across
MemKraft and LLM Wiki layers, identifying freshness issues, coverage gaps,
and maintenance needs.

## Output Language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Architecture

```
ai-status
  │
  ├─→ MemKraft Health
  │     ├─ Tier distribution (HOT/WARM/COLD counts)
  │     ├─ Freshness scores per topic
  │     ├─ Unresolved items count and age
  │     ├─ Preferences coverage
  │     └─ Dream Cycle last run + next scheduled
  │
  ├─→ Wiki Health
  │     ├─ Company Wiki: topic count, freshness
  │     ├─ Team Wiki: topic count per domain
  │     └─ Registry coverage (_wiki-registry.json)
  │
  └─→ System Readiness Score (0-100)
```

## Workflow

### Step 1: MemKraft Health Check

Scan `memory/` directory:

1. **Tier distribution**: Count `.md` files by tier (from frontmatter or `memkraft.json` thresholds)
2. **Freshness**: Check last-modified dates of `memory/topics/*.md`
3. **Unresolved**: Count items in `memory/unresolved/`, flag items older than 7 days
4. **Preferences**: Check `memory/preferences/` for coverage across domains
5. **Dream Cycle**: Read `memory/dream-cycle/` for last execution log

### Step 2: Wiki Health Check

Scan `knowledge-bases/` directory:

1. Read `_wiki-registry.json` for registered topics
2. Count topics with compiled wiki content
3. Check freshness of recent compilations
4. Identify topics with no raw sources or stale wiki content

### Step 3: System Readiness Score

Calculate a composite score (0-100):

| Component | Weight | Scoring |
|-----------|--------|---------|
| MemKraft freshness (avg) | 25% | 100 if all HOT, decay by tier |
| Unresolved item age | 15% | 100 if none >7d, penalty per stale item |
| Preferences coverage | 10% | 100 if all domains covered |
| Dream Cycle recency | 15% | 100 if <24h, 50 if <72h, 0 if >72h |
| Wiki topic coverage | 20% | % of registry topics with compiled content |
| Wiki freshness | 15% | Avg freshness across compiled topics |

### Step 4: Dashboard Output

```markdown
## 📊 지식 시스템 상태 — {YYYY-MM-DD HH:MM}

### 시스템 준비도: {score}/100 {🟢|🟡|🔴}

### MemKraft 상태
| 항목 | 값 | 상태 |
|------|-----|------|
| HOT 항목 | {N} | {🟢|🟡|🔴} |
| WARM 항목 | {N} | {🟢|🟡|🔴} |
| COLD 항목 | {N} | — |
| 미해결 항목 | {N} ({M}개 >7일) | {🟢|🟡|🔴} |
| 선호도 도메인 | {N}/{total} | {🟢|🟡|🔴} |
| Dream Cycle | {last run timestamp} | {🟢|🟡|🔴} |

### LLM Wiki 상태
| 항목 | 값 | 상태 |
|------|-----|------|
| 회사 위키 토픽 | {N} | — |
| 팀 위키 토픽 | {N} (도메인 {M}개) | — |
| 컴파일 완료율 | {X}% | {🟢|🟡|🔴} |
| 평균 신선도 | {score}/100 | {🟢|🟡|🔴} |

### 권장 조치
1. {highest priority maintenance action}
2. {second priority}
3. {third priority}
```

## Readiness Thresholds

| Score | Status | Meaning |
|-------|--------|---------|
| 80-100 | 🟢 Healthy | System ready for reliable AI assistance |
| 50-79 | 🟡 Attention | Some maintenance needed, results may be stale |
| 0-49 | 🔴 Critical | Run Dream Cycle and Wiki compilation immediately |

## Integration

- **Upstream**: User invocation or `daily-am-orchestrator`
- **Reads**: `memory/memkraft.json`, `memory/topics/`, `memory/preferences/`,
  `memory/unresolved/`, `memory/dream-cycle/`, `knowledge-bases/_wiki-registry.json`
- **Suggests**: `memkraft-dream-cycle` (when Dream Cycle overdue),
  `kb-compile` (when wiki stale), `kb-lint` (for detailed wiki health)
- **Output**: Structured Korean dashboard with readiness score
