---
name: wiki-connection-discoverer
description: >-
  Systematically scan KB wiki articles across all topics to discover implicit
  connections that lack explicit connection documents. Uses co-occurrence
  analysis, shared entity detection, temporal proximity, and causal pattern
  matching to identify article pairs that should be linked. Suggests
  connection types (causal, temporal, contradictory, complementary,
  hierarchical) and generates stub connection documents ready for human review
  or auto-filing. Use when the user asks to "discover connections", "find
  missing links", "wiki connection scan", "suggest connections",
  "co-occurrence analysis", "위키 연결 발견", "누락 커넥션 찾기", "연결 자동 발견", "코어커런스 분석",
  "wiki-connection-discoverer", "missing connection report", "implicit link
  detection", "auto-discover wiki links", "커넥션 발견", "위키 링크 자동 생성", or wants to
  find and create missing connection documents in the KB wiki. Do NOT use for
  compiling wiki from raw sources (use kb-compile). Do NOT use for cross-topic
  synthesis documents (use kb-cross-topic-synthesizer). Do NOT use for linting
  existing connections (use kb-lint). Do NOT use for full KB health dashboard
  (use kb-coverage-dashboard).
---

# Wiki Connection Discoverer

Systematically discover implicit connections between KB wiki articles and suggest
or auto-create connection documents with typed relationships.

## When to Use

- Periodic scan to find articles that should be linked but aren't
- After a large batch ingest or compile, to discover new connection opportunities
- Auditing connection coverage across all KB topics
- Suggesting connection types for article pairs
- User says "find missing connections", "커넥션 발견", "누락 링크"

## Do NOT Use

- Compiling wiki from raw sources → `kb-compile`
- Cross-topic concept synthesis → `kb-cross-topic-synthesizer`
- Linting existing connections for broken links → `kb-lint`
- Full KB health dashboard → `kb-coverage-dashboard`

## Architecture

```
Wiki Connection Discoverer
├── Scan all wiki articles across all topics
│   ├── Parse frontmatter (title, aliases, related, tags)
│   ├── Extract inline entity mentions
│   └── Map existing [[wikilinks]] and connections/ docs
├── Build co-occurrence matrix
│   ├── Entity co-occurrence across articles
│   ├── Tag overlap scoring
│   ├── Temporal proximity (articles ingested close in time)
│   └── Shared source references
├── Detect implicit connections
│   ├── High co-occurrence, no existing link → candidate
│   ├── Shared entities across topics, no cross-reference → candidate
│   ├── Causal language patterns ("because of", "leads to", "caused by")
│   ├── Contradictory claims on same entity → contradiction connection
│   └── Hierarchical relationships (part-of, instance-of)
├── Score and rank candidates
│   ├── Co-occurrence strength (normalized frequency)
│   ├── Topic distance (same topic vs. cross-topic)
│   ├── Entity specificity (named entity vs. generic term)
│   └── Existing link density (fewer links → higher discovery value)
├── Classify connection type
│   ├── causal: A influences or causes B
│   ├── temporal: A and B occurred in related timeframes
│   ├── contradictory: A and B present conflicting claims
│   ├── complementary: A and B cover different aspects of same concept
│   ├── hierarchical: A is a parent/child of B
│   └── associative: A and B frequently co-occur without clear relationship
├── Generate output
│   ├── Discovery report with ranked candidates
│   ├── Optional: stub connection documents for top candidates
│   └── Optional: update frontmatter `related` arrays
└── Save report to knowledge-bases/_connection-discovery/report-{date}.md
```

## Connection Types

| Type | Description | Detection Signal | Example |
|---|---|---|---|
| `causal` | A influences or causes B | "because of", "leads to", "results in" | GPU shortage → pricing increase |
| `temporal` | Related timeframe events | Ingested within 48h, same date references | Q1 earnings + Q1 market shift |
| `contradictory` | Conflicting claims | Opposite assertions on same entity | "market growing" vs "market shrinking" |
| `complementary` | Different angles on same topic | Shared entity, different tags/topic | Sales view vs Engineering view of pricing |
| `hierarchical` | Parent-child relationship | "part of", "includes", "type of" | Cloud platform → GPU instance type |
| `associative` | Frequent co-occurrence | High co-occurrence, no causal language | Kubernetes + GPU scheduling |

## Execution Flow

### Step 1: Inventory Existing State

1. List all topics under `knowledge-bases/`
2. For each topic, enumerate all `wiki/concepts/`, `wiki/references/`, and `wiki/connections/` files
3. Parse existing connections to build a "connected pairs" set
4. Parse all `[[wikilinks]]` to build a "linked articles" set

### Step 2: Build Entity Index

For each article:
1. Extract entities from title, aliases, and body text
2. Normalize entity names (lowercase, strip suffixes)
3. Build an inverted index: `entity → [(article_path, frequency, topic)]`

### Step 3: Compute Co-occurrence Matrix

For each entity pair that appears in 2+ articles:

```yaml
co_occurrences:
  - entity_a: "GPU pricing"
    entity_b: "cloud cost optimization"
    articles_a: ["competitive-intel/wiki/concepts/gpu-pricing.md"]
    articles_b: ["finance-policies/wiki/concepts/cloud-costs.md"]
    shared_articles: []  # none — they don't appear together
    co_occurrence_score: 0.72
    already_connected: false
    topic_distance: "cross-topic"
```

Score formula:
```
co_occurrence_score = (shared_entity_count / max_entity_count) × topic_distance_weight
topic_distance_weight = 1.5 for cross-topic, 1.0 for same-topic
```

### Step 4: Detect Implicit Connections

Filter co-occurrence candidates:
1. `co_occurrence_score >= 0.5` AND `already_connected == false`
2. Scan article pairs for causal language patterns
3. Check for contradictory claims (opposite sentiment on shared entities)
4. Check temporal proximity of `ingested` dates
5. Check hierarchical language ("part of", "instance of", "type of")

### Step 5: Score and Rank

For each candidate connection:

```yaml
candidates:
  - article_a: "competitive-intel/wiki/concepts/aws-pricing.md"
    article_b: "finance-policies/wiki/concepts/cloud-budget-planning.md"
    connection_type: "complementary"
    score: 0.85
    reasoning: "Both discuss cloud pricing from different perspectives (external market vs internal budget)"
    shared_entities: ["GPU pricing", "cloud compute", "reserved instances"]
    topic_distance: "cross-topic"
    existing_links: 0
```

Rank by score descending. Top N candidates (default: 20) are reported.

### Step 6: Generate Connection Stubs (Optional)

For candidates with score >= 0.7, generate stub `connections/` documents:

```markdown
---
title: "{Article A title} ↔ {Article B title}"
connection_type: "{type}"
articles:
  - "{article_a_path}"
  - "{article_b_path}"
discovered_by: "wiki-connection-discoverer"
discovery_date: "{YYYY-MM-DD}"
confidence: {score}
status: "pending_review"
---

# {Article A title} ↔ {Article B title}

**Connection type:** {type}
**Confidence:** {score}

## Relationship

{Auto-generated description of why these articles are connected,
citing shared entities and co-occurrence evidence}

## Shared Entities

{List of entities appearing in both articles}

## Evidence

- From {article_a}: "{relevant excerpt}"
- From {article_b}: "{relevant excerpt}"
```

File in: `{topic_of_article_a}/wiki/connections/{slug}.md`
If cross-topic, file in both topics.

### Step 7: Generate Discovery Report

```markdown
---
title: "Connection Discovery Report — {date}"
topics_scanned: {N}
articles_analyzed: {N}
candidates_found: {N}
stubs_generated: {N}
report_date: {YYYY-MM-DD}
---

# Connection Discovery Report — {date}

## Summary

- **Topics scanned:** {N}
- **Articles analyzed:** {N}
- **Existing connections:** {N}
- **New candidates found:** {N}
- **Stubs auto-generated:** {N} (score ≥ 0.7)

## Top Candidates

| Rank | Article A | Article B | Type | Score | Shared Entities |
|---|---|---|---|---|---|
| 1 | {path} | {path} | {type} | {score} | {entities} |
| 2 | {path} | {path} | {type} | {score} | {entities} |

## By Connection Type

### Causal ({N})
{List of causal connections discovered}

### Complementary ({N})
{List of complementary connections discovered}

### Contradictory ({N})
{List of contradictory connections — these need human attention}

### Temporal ({N})
{List of temporal connections}

### Hierarchical ({N})
{List of hierarchical connections}

### Associative ({N})
{List of associative connections}

## Disconnected Islands

Articles with zero connections (incoming or outgoing):
{List of isolated articles that may need linking}

## Under-Connected Topics

Topics with connection density below the median:
{Table of topic → connection count → density score}

## Source Data

{Summary statistics of the co-occurrence analysis}
```

### Step 8: Save Output

1. Create `knowledge-bases/_connection-discovery/` directory if it doesn't exist
2. Save report to `knowledge-bases/_connection-discovery/report-{YYYY-MM-DD}.md`
3. If stubs were generated, they are filed in the respective topic `wiki/connections/` directories

## Output Format

| Artifact | Location | Description |
|---|---|---|
| Discovery report | `_connection-discovery/report-{date}.md` | Full report with ranked candidates |
| Connection stubs | `{topic}/wiki/connections/` | Auto-generated stub documents (score ≥ 0.7) |
| Isolated articles | In report | List of articles with zero connections |

## Composability

- **kb-compile**: Connection auto-suggestion (added in v3.0) produces initial candidates; this skill does deeper co-occurrence analysis
- **kb-lint**: Check 8 (orphan connections) and Check 9 (cross-topic gaps) feed candidate signals
- **kb-daily-report**: Connection delta section references newly created connection documents
- **kb-cross-topic-synthesizer**: Shares entity overlap methodology; synthesizer operates at concept level, this skill at article-pair level
- **kb-coverage-dashboard**: Connection density metrics feed into the dashboard

## Constraints

- Minimum corpus size: 10 articles across 2+ topics for meaningful co-occurrence
- Connection stubs are marked `status: "pending_review"` — they are not finalized until human/agent review
- Prior discovery reports are preserved for trend tracking
- Co-occurrence scoring is deterministic given the same corpus — re-runs produce consistent results
- The `_connection-discovery/` directory is shared across all topics
- Cross-topic connection stubs are filed in BOTH topics to maintain bidirectional visibility

## Examples

### Example 1: Full discovery run

**Trigger:** User says: "Find missing connections across all KB topics"

**Actions:** (1) Scan all topic `wiki/` directories for article pairs. (2) Analyze co-occurrence, shared entities, temporal proximity. (3) Score connection strength for each pair. (4) Generate discovery report with suggested connection types. (5) Create stub connection documents for high-confidence pairs.

**Result:** Dated report under `_connection-discovery/` plus optional stubs in topic `wiki/connections/`.

### Example 2: Single topic discovery

**Trigger:** User says: "engineering-standards에서 빠진 연결 찾아줘"

**Actions:** (1) Focus scan on `engineering-standards/wiki/` only. (2) Identify article pairs with shared concepts but no connection document. (3) Report findings with connection type suggestions.

**Result:** Scoped discovery report without cross-topic stub fan-out unless pairs warrant it.

## Error Handling

| Error | Action |
|-------|--------|
| Topic has fewer than 3 articles | Skip topic — insufficient content for meaningful connection discovery |
| Connection stubs directory doesn't exist | Create `wiki/connections/` automatically |
| All article pairs already have connections | Report "full coverage" — no new connections needed |
| Co-occurrence analysis produces 100+ candidates | Apply threshold filter (score > 0.6) and report top 20 only |

## Gotchas

- **Symptom:** Huge low-signal candidate lists. **Root cause:** High-frequency terms ("data", "system", "service") co-occur by chance. **Correct approach:** Use stopword filtering; extend with domain-specific stop terms when noise persists.
- **Symptom:** False links from "same day" ingestion. **Root cause:** Temporal proximity without semantic relevance. **Correct approach:** Require semantic check beyond ingest date before promoting a pair.
- **Symptom:** Stubs read like placeholders. **Root cause:** Generic stub template before human review. **Correct approach:** Treat stubs as `pending_review` only; do not treat as authoritative wiki until reviewed.

## Output Discipline

- Do not generate connection stubs for pairs scoring below the confidence threshold (default: 0.5).
- Do not create duplicate connection documents — check existing `connections/` before generating stubs.
- Discovery reports should rank by confidence score, highest first.

## Honest Reporting

- Report the total pairs analyzed, not just the connections found — e.g. "analyzed 450 pairs, found 12 potential connections".
- When the discovery yields zero results, state it clearly rather than lowering the threshold to force results.
- Report false positive rate from previous runs if available to calibrate expectations.
