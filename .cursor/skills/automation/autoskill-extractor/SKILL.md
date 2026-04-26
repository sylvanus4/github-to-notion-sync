---
name: autoskill-extractor
description: >-
  Cursor 에이전트 트랜스크립트에서 재사용 가능한 스킬 후보를 추출. 사용자 교정
  패턴, 반복 지시, 지속적 선호를 분석하여 구조화된 스킬 후보 JSON을 생성.
  Use when the user asks to "extract skills from sessions", "트랜스크립트에서
  스킬 추출", "autoskill extract", "세션에서 패턴 추출", "스킬 후보 추출",
  "mine transcripts", "세션 마이닝". Do NOT use for creating skills from
  scratch (use create-skill), optimizing existing skills (use skill-optimizer
  or skill-autoimprove), or reading transcripts without extraction (read
  transcript files directly).
metadata:
  author: thaki
  version: "1.0.1"
  category: self-improvement
---

# AutoSkill Extractor

Extract reusable skill candidates from Cursor agent transcripts (JSONL). Analyze repeated corrections, explicit instructions, and workflow patterns to produce structured skill candidates.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Input

- Transcript JSONL path: `~/.cursor/projects/*/agent-transcripts/*.jsonl`
- Session ID (UUID): auto-locate transcript
- `--scope recent`: process the 5 most recent transcripts
- `--hint "focus area"` (optional): guide extraction emphasis

## Workflow

### Session Separation Rule

When processing multiple transcripts (e.g., `--scope recent` with 5 transcripts), **each transcript MUST be processed in an isolated subagent via the Task tool**. Never load multiple transcripts into the same session context — earlier transcript patterns contaminate detection for later ones, producing false positive "repeated across sessions" signals.

### Step 1: Load transcripts

Read JSONL and parse structured events. Each line is a JSON event (user message, assistant response, tool calls).

### Step 2: Identify user evidence

Extract **from user turns only**. Use assistant turns as context only.

Targets:
- Explicit reusable constraints (style, format, audience, rules)
- User corrections that imply lasting preferences
- Multi-step workflow specifications
- Schema/template requirements
- Implementation policies and rules

### Step 3: Apply extraction criteria

**DO extract**:
- Corrections repeated across 2+ sessions → durable preference
- Explicit directives like “always do X” / “never do Y”
- User-specified multi-step workflows
- Format/style constraints that apply beyond one task
- Tool-usage patterns with specific settings

**DO NOT extract**:
- One-off generic tasks (“write one function”)
- Requirements that appear only in assistant output
- Case-specific facts, entities, domain claims
- Stale constraints from early in a long session
- Assistant-invented patterns the user never confirmed

### Step 4: De-identify

Replace case-specific entities with placeholders: `<project>`, `<file>`, `<endpoint>`, `<model>`. Focus on HOW (portable rules), remove WHAT (instance facts).

### Step 5: Build skill candidates

```json
{
  "name": "kebab-case-descriptive-name",
  "description": "1–2 sentences on role and when to use",
  "prompt": "# Goal\n...\n# Constraints\n...\n# Workflow\n...",
  "triggers": ["trigger phrase 1", "trigger phrase 2"],
  "tags": ["tag1", "tag2"],
  "examples": ["usage scenario example"],
  "confidence": 0.85,
  "source_transcript": "uuid",
  "source_turns": [12, 15, 23]
}
```

### Step 6: Quality gate

- Output only candidates with confidence >= 0.6
- At most 2 candidates per transcript (anti-spam)

## Output

Save each candidate to `outputs/autoskill-candidates/<date>-<name>.json`. Return confidence scores and a source summary report for all candidates.

## Integration

- Pass candidates to `autoskill-judge` → add/merge/discard
- Invoke via `autoskill-evolve` orchestrator or manually

## Examples

### Example 1: Extract from recent sessions

User: "Extract skills from recent sessions"

Actions:
1. Load 5 most recent transcripts
2. Analyze user turns → find 3 recurring patterns
3. De-identify and structure
4. Emit 2 candidates (confidence 0.78, 0.65)

### Example 2: Extract from one session with hint

User: "Extract patterns from this session --hint 'document writing'"

Actions:
1. Load the specified transcript
2. Focus analysis on document-writing corrections
3. Emit 1 candidate (confidence 0.82)

## Error Handling

| Error | Response |
|-------|----------|
| No transcripts | Verify path; list recent sessions |
| Fewer than 5 user turns | Warn short session; skip extraction |
| No patterns | Report “no reusable patterns to extract” |
| Confidence below 0.6 | Drop candidate; explain why |
