# Knowledge Feedback for marketing-autoreason

## Goal

Close the learning loop: tournament outputs and real campaign results flow back into
`knowledge-bases/marketing-playbook/` so every subsequent autoreason run draws on
accumulated, evidence-graded copy intelligence.

## Feedback mechanisms

### 1. Tournament Result Ingestion (automatic — runs after every tournament)

Triggered by Step 6a in `SKILL.md`. Extracts from the run directory:

| Source file | Extracted data |
| --- | --- |
| `final_output.md` | Winning copy (verbatim), channel, locale |
| `history.json` | Borda scores per round, per-dimension rubric scores, convergence round, loser labels |
| `knowledge-pack.md` | Evidence sources used (for provenance chain) |
| `marketing-manifest.json` | Channel, locale, rubric version |

#### Output artifact: `autoreason-winner-{run_id}.md`

```markdown
---
type: autoreason-winner
run_id: {run_id}
date: {YYYY-MM-DD}
channel: {email_subject | ad_headline | landing_hero | ...}
locale: {EN | KO}
borda_score: {float}
convergence_round: {int}
rubric_version: {semver from marketing-rubric.md}
evidence_sources: [{list of kb: paths from knowledge-pack.md}]
---

## Autoreason Winner — {date} — {channel}

### Winning copy

> {verbatim winning text}

### Rubric scores

| Dimension | Score (1-10) |
| --- | --- |
| Clarity & specificity | {n} |
| Evidence grounding | {n} |
| Brand voice fit | {n} |
| Audience resonance | {n} |
| Competitive differentiation | {n} |

### Task spec

- Channel: {channel}
- Locale: {locale}
- Character limit: {n}
- Compliance notes: {if any}

### Loser failure modes

| Variant | Failure tag |
| --- | --- |
| B (round N) | {generic / off-brand / unsupported-claim / too-long / wrong-audience} |
| A (round M) | {tag} |
```

#### Ingestion path

`knowledge-bases/marketing-playbook/raw/autoreason-winner-{run_id}.md`

Use `kb-ingest` with topic `marketing-playbook`. The file lands in `raw/` and
becomes available to `kb-compile` on the next recompilation cycle.

### 2. Campaign Performance Feedback (user-triggered)

Triggered when the user supplies post-launch metrics for a previously generated copy.
Step 6b in `SKILL.md`.

#### Matching logic

1. User provides `run_id` directly, OR
2. Agent searches `outputs/autoreason/` for a directory matching date + channel.
3. If no match found, ask the user for clarification before proceeding.

#### Output artifact: `campaign-feedback-{run_id}.md`

```markdown
---
type: campaign-feedback
run_id: {run_id}
date_launched: {YYYY-MM-DD}
date_measured: {YYYY-MM-DD}
channel: {email_subject | ad_headline | ...}
outcome: {VALIDATED | UNDERPERFORMED | INCONCLUSIVE}
---

## Campaign Feedback — {run_id}

### Copy tested

> {verbatim copy from the original final_output.md}

### Metrics

| Metric | Predicted / baseline | Actual | Delta |
| --- | --- | --- | --- |
| Open rate | {n}% | {n}% | {+/-n}pp |
| CTR | {n}% | {n}% | {+/-n}pp |
| CVR | {n}% | {n}% | {+/-n}pp |
| Revenue lift | {n}% | {n}% | {+/-n}pp |

### Outcome classification

**{VALIDATED | UNDERPERFORMED | INCONCLUSIVE}**

{1-2 sentence rationale citing which metrics drove the classification.}

### Failure hypothesis (UNDERPERFORMED only)

- Primary cause: {e.g. "subject line promised discount not present in body"}
- Contributing factors: {e.g. "sent on holiday weekend — lower baseline engagement"}
- Recommended rubric adjustment: {e.g. "increase weight of 'CTA-body coherence' dimension"}
```

#### Ingestion path

`knowledge-bases/marketing-playbook/raw/campaign-feedback-{run_id}.md`

#### Classification rules

| Outcome | Condition |
| --- | --- |
| `VALIDATED` | Primary metric >= baseline AND no metric dropped > 20% |
| `UNDERPERFORMED` | Primary metric < baseline by > 10% OR any metric dropped > 30% |
| `INCONCLUSIVE` | Sample size < 1000, OR measurement window < 48h, OR metrics within noise margin |

The "primary metric" is determined by channel:

- Email: open rate
- Ad: CTR
- Landing page: CVR
- Social: engagement rate

#### Loser pattern propagation

When outcome is `UNDERPERFORMED`, the failure hypothesis feeds into future
`knowledge-pack.md` assembly. During the Knowledge Layer step, the agent queries
`kb-search` for `campaign-feedback` entries with `UNDERPERFORMED` status and includes
them in the **Copy exemplars > Losers** section (see `knowledge-assembly.md` section 2).

### 3. Knowledge Recompilation Signal

Both mechanisms (1 and 2) append to a shared queue file so that the next KB build
cycle picks up new artifacts without requiring an immediate inline recompilation.

#### Queue file

`outputs/autoreason/kb-recompile-queue.txt`

Format (one line per entry, append-only):

```
{YYYY-MM-DD} {run_id} {type}
```

Where `type` is `winner` (from mechanism 1) or `campaign` (from mechanism 2).

#### Consumption

- `kb-daily-build-orchestrator` reads the queue at the start of the marketing-playbook
  collection phase and includes queued `run_id` artifacts in its compile scope.
- After successful compilation, processed lines are moved to
  `outputs/autoreason/kb-recompile-queue.done.txt` (archive, not deleted).
- Manual `kb-compile --topic marketing-playbook` also processes the queue.

### 4. `feedback-receipt.json` schema

Written to the run directory after successful KB ingestion (Step 6a, line 5).

```json
{
  "run_id": "string",
  "ingested_at": "ISO-8601 timestamp",
  "ingested_path": "knowledge-bases/marketing-playbook/raw/autoreason-winner-{run_id}.md",
  "queue_entry": "{date} {run_id} winner",
  "knowledge_pack_hash": "sha256 of knowledge-pack.md at time of run"
}
```

For campaign feedback (Step 6b), the receipt is appended or a second receipt file
`feedback-receipt-campaign.json` is written:

```json
{
  "run_id": "string",
  "feedback_type": "campaign",
  "ingested_at": "ISO-8601 timestamp",
  "ingested_path": "knowledge-bases/marketing-playbook/raw/campaign-feedback-{run_id}.md",
  "outcome": "VALIDATED | UNDERPERFORMED | INCONCLUSIVE",
  "queue_entry": "{date} {run_id} campaign"
}
```

## Integration with existing KB pipeline

```
Tournament run
  |
  v
final_output.md + history.json
  |
  v
[6a] autoreason-winner-{run_id}.md --> kb-ingest --> marketing-playbook/raw/
  |
  v
kb-recompile-queue.txt <-- append
  |
  v
[next kb-daily-build or kb-compile] --> marketing-playbook/wiki/ updated
  |
  v
[next marketing-autoreason run] --> knowledge-pack.md includes past winners + losers
```

Campaign feedback loop:

```
User supplies metrics
  |
  v
[6b] campaign-feedback-{run_id}.md --> kb-ingest --> marketing-playbook/raw/
  |
  v
kb-recompile-queue.txt <-- append
  |
  v
[next kb-compile] --> wiki articles updated with VALIDATED/UNDERPERFORMED tags
  |
  v
[next marketing-autoreason run] --> knowledge-pack.md cites validated winners,
                                    flags underperforming patterns as losers
```

## Guardrails

- Never run `kb-compile` inline during a tournament — latency risk.
- Never fabricate campaign metrics; only ingest user-supplied or KB-sourced numbers.
- Failure hypotheses are hypotheses, not verdicts; label them accordingly.
- Queue file is append-only during runs; only the KB build pipeline archives entries.
- If `kb-ingest` fails, log the error in `feedback-receipt.json` with
  `"status": "failed"` and `"error": "..."` — do not silently drop feedback.
