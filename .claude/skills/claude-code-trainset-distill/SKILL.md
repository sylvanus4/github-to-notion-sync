---
name: claude-code-trainset-distill
description: >-
  Convert Claude Code session transcripts (~/.claude/projects/<repo>/*.jsonl)
  into LLM training data: SFT JSONL (multi-turn agentic, Anthropic native
  format with tool calls preserved) and GRPO/DPO preference pairs (weak
  labels from user feedback signals like /rewind, "그게 아니라", correction
  prompts). Includes secret redaction (HF_TOKEN, RUNPOD_API_KEY, ssh keys,
  emails). Use when the user wants to fine-tune a model on their own Claude
  Code interaction patterns. Do NOT use for persona distillation (use
  auto-distill / nuwa). Korean triggers: "학습 데이터", "SFT 데이터",
  "GRPO 데이터", "트랜스크립트 학습용".
---

# Claude Code → SFT/GRPO Trainset Distillation

Convert Claude Code raw transcripts into LLM training-ready JSONL.

## Archetype: Mechanical-Only Extraction

This skill is a reference example of the **mechanical extraction archetype** — a class of skills that:

- **No LLM API calls**: pure regex + JSON walking; cost = $0 per run regardless of input size
- **Idempotent**: re-running on the same input produces the same output (modulo timestamps)
- **Stateless**: only reads filesystem, writes to `outputs/`; no external services
- **Fast**: ~50ms per MB of input; suitable for nightly batch via Stop hook
- **Auditable**: every transformation is a regex pattern in version control (see `redact.py`)

When to use this archetype for new skills:
- Source data already structured (JSONL, CSV, JSON, YAML)
- Transformation rules are deterministic and inspectable
- You want zero-cost batch processing as part of `/jarvis 밤새 동작` consolidation
- Quality bar is "schema-correct + secrets redacted", not "LLM-judged"

When NOT to use this archetype (escalate to LLM-augmented extraction):
- Source is unstructured prose requiring semantic understanding
- Transformation needs synthesis/summarization
- Output quality matters more than cost (use `auto-distill-v2` or `nuwa` instead)

Existing examples in this repo:
- `claude-code-trainset-distill` (this skill) — Claude Code JSONL → SFT/preference pairs
- `scripts/intelligence/intel_registry.py` — URL deduplication via SHA hashing

## Why this skill exists

Claude Code already saves every session transcript as JSONL at:
```
~/.claude/projects/<encoded-repo-path>/<session-uuid>.jsonl
```

These transcripts contain:
- Full user prompts (with context tags like `<command-name>`, `<system-reminder>`)
- Assistant responses with tool calls (Bash, Edit, Read, Agent, etc.) and reasoning
- Tool results (the ground-truth outputs that informed the next action)
- File-history snapshots (state-machine evidence for behavior diffs)
- Queue operations (multi-turn intent / interruption signals)

This is **gold for fine-tuning** because it's:
- Real (not synthetic)
- Multi-turn agentic (tool-use chains, not just chat)
- Domain-grounded (this repo's actual workflows)
- Annotated by the user via natural follow-ups (corrections = preference signal)

But raw JSONL is unusable for training as-is — needs schema normalization, secret redaction, and conversion to standard formats (OpenAI chat, Anthropic native, or DPO pairs).

## When to Use

- Building an SFT dataset from your own Claude Code sessions to fine-tune a smaller model
- Generating DPO/GRPO preference pairs from user-feedback signals
- Bootstrapping a domain-specific assistant from real interaction logs
- Routine call from `/jarvis 밤새 동작` (Consolidation Mode, distill step)

## Do NOT Use For

- Persona/style distillation from text → use `auto-distill`, `nuwa`, `self-distillation`
- Generating synthetic data from scratch → use a generation pipeline, not transcript replay
- Fine-tuning Claude itself — Anthropic doesn't expose tunable weights; this is for OSS targets (Qwen, Llama, Mistral, etc.)

## Outputs

```
outputs/training-data/
├── sft/
│   ├── <session-uuid>.jsonl           # one example per (system + msgs) chunk
│   └── _index.json                    # {file, n_examples, n_tokens_est, last_modified}
├── preference/
│   ├── <session-uuid>.jsonl           # {prompt, chosen, rejected, signal}
│   └── _index.json
├── raw-redacted/                      # redacted full transcripts (audit trail)
│   └── <session-uuid>.jsonl
└── REPORT.md                          # summary: counts, token estimates, redaction stats
```

### SFT format (Anthropic-native, tool calls preserved)

```json
{
  "id": "<session-uuid>:<window-N>",
  "system": "<system prompt + CLAUDE.md, redacted>",
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": [
      {"type": "text", "text": "..."},
      {"type": "tool_use", "id": "...", "name": "Bash", "input": {"command": "...", "description": "..."}}
    ]},
    {"role": "user", "content": [
      {"type": "tool_result", "tool_use_id": "...", "content": "..."}
    ]},
    ...
  ],
  "metadata": {
    "source_session": "<uuid>",
    "model": "claude-opus-4-7",
    "n_turns": 12,
    "n_tool_calls": 7,
    "n_tokens_est": 8400,
    "captured_at": "ISO-8601"
  }
}
```

Convertible to:
- **OpenAI chat completions** (drop `tool_use` / use `function_call`) — `--format openai`
- **ShareGPT** — `--format sharegpt`
- **Llama-Factory** — `--format llama-factory`

### Preference format (DPO/GRPO compatible)

```json
{
  "id": "<session-uuid>:<turn-N>",
  "prompt": "<full conversation up to point of divergence>",
  "chosen": "<assistant response that was accepted (no correction in next turn)>",
  "rejected": "<assistant response that triggered a correction signal>",
  "signal": "user_correction|rewind|repeat_request|explicit_negative",
  "confidence": 0.6,
  "metadata": {...}
}
```

**Weak label heuristics** (signal types):
| Signal | Detection |
|--------|-----------|
| `rewind` | next user turn contains `/rewind` or `/redo` |
| `user_correction` | next user turn matches `^(아니|그게 아니|wrong|no, |no.|정정|다시 해|undo)` |
| `repeat_request` | next user turn restates previous request with explicit modification |
| `explicit_negative` | next user turn contains `잘못`, `이상하다`, `bug`, `실패` |

Pairs require a **counterfactual** for `chosen`. Two strategies:
- (A) Use the *re-attempted* assistant response after correction as `chosen`
- (B) Synthesize `chosen` from the user's correction text (LLM-as-judge, costly)

Default: strategy A (free, faithful). B is opt-in via `--synthesize-chosen`.

## Redaction

Always-redacted patterns (`scripts/redact.py`):
- HuggingFace tokens: `hf_[a-zA-Z0-9]{30,}` → `[REDACTED_HF_TOKEN]`
- RunPod API keys: `rpa_[a-zA-Z0-9]{40,}` → `[REDACTED_RUNPOD_KEY]`
- Generic API keys: `sk-[a-zA-Z0-9]{30,}`, `pk_[a-zA-Z0-9]{30,}` → `[REDACTED_API_KEY]`
- SSH private keys: `-----BEGIN ... PRIVATE KEY-----` blocks → `[REDACTED_SSH_KEY]`
- Email addresses: → `[REDACTED_EMAIL]`
- AWS keys: `AKIA[A-Z0-9]{16}` → `[REDACTED_AWS_KEY]`

Add custom patterns via `scripts/redact.py` `EXTRA_PATTERNS` list (not via SKILL.md edit).

**Audit trail**: `outputs/training-data/raw-redacted/` keeps the redacted full transcripts so you can see what training data was generated from. The original `~/.claude/projects/.../*.jsonl` is never modified.

## Workflow

### Stage 1: Discover sessions

```bash
python3 .claude/skills/claude-code-trainset-distill/scripts/extract_sft.py \
    --discover \
    --since 7d                  # or YYYY-MM-DD, or "last-session"
```

Lists candidate `.jsonl` files with size/turn counts.

### Stage 2: Distill SFT

```bash
python3 .claude/skills/claude-code-trainset-distill/scripts/extract_sft.py \
    --since 7d \
    --output outputs/training-data/sft \
    --max-turns-per-example 20 \
    --redact \
    --format anthropic           # or openai|sharegpt|llama-factory
```

Default chunking: ~20 turns per example (≈8k tokens). Larger windows preserve agentic context but may exceed target model context. Tune per fine-tune target.

### Stage 3: Distill preference pairs

```bash
python3 .claude/skills/claude-code-trainset-distill/scripts/extract_preference.py \
    --since 7d \
    --output outputs/training-data/preference \
    --strategy A                 # A=use re-attempt, B=LLM synthesize
    --redact
```

### Stage 4: Report

```bash
python3 .claude/skills/claude-code-trainset-distill/scripts/build_report.py
```

Writes `outputs/training-data/REPORT.md`:
- Per-session: turns, tool calls, examples extracted, redactions hit
- Aggregate: total examples, est. tokens, est. fine-tune cost (target model dependent)
- Quality flags: short-turn warnings, dedup hits, suspicious prompt-injection patterns

## Integration with `/jarvis 밤새 동작`

When Consolidation Mode runs overnight, append a distill step:
```
iter N: trainset-distill (mechanical, ~30s)
  - extract_sft.py --since 1d --output outputs/training-data/sft
  - extract_preference.py --since 1d --output outputs/training-data/preference
  - build_report.py
```

Set `--since 1d` for daily incremental runs (cheap, no LLM calls). For full retrospective rebuild use `--since 30d --rebuild`.

## Cost & Volume

Mechanical scripts (no LLM API):
- ~50ms per MB of jsonl
- Zero token cost
- Disk: SFT JSONL ≈ 0.7× source jsonl size; preference ≈ 0.1×

Optional LLM-augmented preference (`--synthesize-chosen`):
- Per pair: ~1500 prompt + 800 output tokens
- Sonnet $0.011/pair · Haiku $0.0025/pair
- Use only when re-attempt signal is weak

## Safety Gates

- **Redaction is mandatory** — no flag to disable; only adjust patterns
- **Audit trail required** — `raw-redacted/` always written
- **No upload helpers** — this skill writes JSONL only; uploading to HF Hub or training services is a separate step (use `hf-datasets` for HF Hub, manual for others)
- **Source untouched** — original `~/.claude/projects/.../*.jsonl` never modified

## Known Limitations

- Tool-call schemas evolve across Claude versions; current parser targets Claude Code 2.x format. If transcripts contain unknown `type` values, they're logged to `_unknown_records.json` for inspection.
- The `<system-reminder>` and `<command-name>` injected blocks are kept in user content (they're part of the actual interaction); future option `--strip-system-reminders` may be added.
- Multi-session conversations (continued via `/resume`) are not stitched; each jsonl is a separate example pool.
- Subagent (Task) prompts/responses are nested inside the parent — currently kept as-is in the parent example. Future option `--extract-subagents` may add them as separate top-level examples.
