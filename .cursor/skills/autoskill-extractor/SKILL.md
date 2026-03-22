---
name: autoskill-extractor
description: >-
  Extract reusable skill candidates from Cursor agent transcripts by analyzing
  user interaction patterns, corrections, and durable preferences. Use when the
  user asks to "extract skills from sessions", "mine transcripts for skills",
  "autoskill extract", "find reusable patterns", "스킬 추출", "세션에서 스킬 추출",
  "트랜스크립트 마이닝", or when invoked by autoskill-evolve. Do NOT use for
  creating skills from scratch (use create-skill), optimizing existing skills
  (use skill-optimizer), or general transcript reading (use recall).
metadata:
  author: thaki
  version: "0.1.0"
  category: self-improvement
---

# AutoSkill Extractor

Extract reusable skill candidates from Cursor agent transcripts by analyzing user interaction patterns, corrections, and durable preferences. Adapts AutoSkill's P_ext methodology for the Cursor SKILL.md ecosystem.

## Instructions

### Input

The extractor accepts one of:
- A transcript JSONL file path from `~/.cursor/projects/*/agent-transcripts/*.jsonl`
- A session ID (UUID) to locate the transcript automatically
- `--scope recent` to process the 5 most recent transcripts
- An optional `--hint "focus area"` to guide extraction

### Extraction Process

1. **Load Transcript**: Read the JSONL file. Each line is a structured JSON event containing user messages, assistant responses, and tool calls.

2. **Identify User Evidence**: Extract only from USER turns. Assistant turns provide context but are never source-of-truth for skill requirements. Focus on:
   - Explicit reusable constraints (style, format, audience, conventions)
   - User corrections that encode durable preferences
   - Multi-step workflow specifications
   - Schema/template requirements
   - Implementation policies and rules

3. **Apply Extraction Criteria**:

   **DO Extract**:
   - Repeated corrections across sessions → durable preference
   - Explicit "always do X" / "never do Y" instructions
   - Multi-step workflows the user specified
   - Format/style constraints that apply beyond one task
   - Tool usage patterns with specific configurations

   **DO NOT Extract**:
   - One-shot generic tasks ("write a function", "fix this bug")
   - Requirements that appear only in assistant output
   - Case-specific facts, entities, or domain claims
   - Stale constraints from early in a long session
   - Assistant-invented patterns not confirmed by user

4. **De-identify**: Remove case-specific entities. Replace with placeholders: `<project>`, `<file>`, `<endpoint>`, `<model>`. Focus on HOW (portable rules), not WHAT (instance facts).

5. **Generate Skill Candidate**: Output a structured candidate with:

```json
{
  "name": "kebab-case-descriptive-name",
  "description": "1-2 sentences: WHAT the skill does and WHEN to use it",
  "prompt": "# Goal\n...\n# Constraints & Style\n...\n# Workflow (optional)\n...",
  "triggers": ["trigger phrase 1", "trigger phrase 2", "trigger phrase 3"],
  "tags": ["tag1", "tag2"],
  "examples": ["example usage scenario"],
  "confidence": 0.85,
  "source_transcript": "uuid",
  "source_turns": [12, 15, 23]
}
```

6. **Quality Gate**: Only output candidates with confidence >= 0.6. Maximum 2 candidates per transcript to avoid skill spam.

### Output

Write each candidate to `outputs/autoskill-candidates/<date>-<name>.json`. Return a summary listing all candidates with their confidence scores and source transcripts.

### Reference Prompts

See `references/extraction-prompt.md` for the full adapted extraction prompt template.

### Integration

- Uses `scripts/memory/extract-sessions.py` for transcript preprocessing
- Feeds candidates to `autoskill-judge` for add/merge/discard decisions
- Invoked by `autoskill-evolve` orchestrator or manually via `/autoskill-extract`

### SEFO Integration (RSD-HSG)

After extracting candidates from transcripts, POST the raw trace data to the SEFO backend for Recursive Skill Distillation:

1. **Ingest traces**: POST each processed transcript to `POST /api/v1/sefo/traces/ingest` with `session_id` and `raw_trace` fields. This stores the trace for grammar induction.
2. **Trigger grammar induction**: After ingesting a batch, call `POST /api/v1/sefo/traces/rsd/induce` with `d_max=3, epsilon=0.1`. This runs Inside-Outside + MDL compression to extract meta-skills with formal grammar rules.
3. **Compare results**: The SEFO-extracted meta-skills (returned as `skill_ids`) provide formally structured skills with composition DAGs. Compare these with the heuristic candidates from the existing extraction pipeline to identify higher-quality abstractions.
4. **Enrich candidates**: For each heuristic candidate, check if a corresponding SEFO meta-skill exists via `GET /api/v1/sefo/skills?search=<name>`. If found, enrich the candidate JSON with the SEFO skill's `grammar_rule` and `composition_dag`.

This dual-path approach preserves backward compatibility while enabling the formal RSD-HSG pipeline.
