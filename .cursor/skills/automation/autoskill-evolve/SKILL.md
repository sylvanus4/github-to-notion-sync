---
name: autoskill-evolve
description: >-
  E2E 스킬 진화 파이프라인: 에이전트 세션 트랜스크립트에서 스킬 후보를 추출하고,
  기존 스킬과 비교 판정(add/merge/discard)하여 스킬 생태계를 자동 진화시킴.
  autoskill-extractor를 오케스트레이션하여 완전한 진화 사이클을 수행.
  Use when the user asks to "스킬 진화", "autoskill evolve", "세션 기반 스킬 진화",
  "transcripts to skills", "run autoskill evolution", "mine sessions for skills",
  "스킬 자동 업데이트", or when triggered by /autoskill-evolve.
  Do NOT use for creating skills manually (use create-skill).
  Do NOT use for auditing existing skills (use skill-optimizer).
  Do NOT use for session context recall (use recall or continual-learning).
  Do NOT use for autonomous skill prompt optimization (use skill-autoimprove).
metadata:
  author: "thaki"
  version: "1.0.2"
  category: "self-improvement"
---
# AutoSkill Evolve

End-to-end pipeline: extract reusable skill candidates from agent session transcripts, compare them against the existing skill ecosystem, and decide add / merge / discard.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Pipeline Overview

```
Transcripts → Extract → Judge → Add/Merge/Discard → Policy compliance → Guard → Report
```

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--scope <scope>` | No | `recent` (default, last 5) / `all` / `session <uuid>` |
| `--dry-run` | No | Preview only; no file changes |
| `--auto-optimize` | No | Run `skill-optimizer` audit on created/merged skills |
| `--slack` | No | Post summary to Slack |
| `--hint <text>` | No | Pass extraction hint to `autoskill-extractor` |

## State Tracking

Evolution state is tracked in `.cursor/hooks/state/autoskill-evolution.json`:

```json
{
  "last_processed": "2026-03-24T10:00:00Z",
  "processed_transcripts": ["uuid1", "uuid2"],
  "evolution_count": 0,
  "skills_created": 0,
  "skills_merged": 0,
  "skills_discarded": 0
}
```

---

## Step 1: Scope Selection

Choose transcripts to process from the `--scope` flag:

- `recent` (default): up to 5 most recent transcripts not yet indexed/processed
- `all`: all unprocessed transcripts (use with care)
- `session <uuid>`: a specific session transcript

Use `processed_transcripts` in the state file to avoid duplicate processing.

### 운영 권장 케이던스

- 이 저장소(**주식·금융 데이터 분석 / 이벤트 스터디**)에서는 트랜스크립트가 쌓인 뒤 **`recent` 스코프로 주 1회**
  실행하는 것을 권장한다. 과도한 빈도는 중복 후보와 노이즈를 늘린다.
- `continual-learning`(AGENTS.md 선호·작업공간 사실)과 **역할을 분리**한다:
  autoskill-evolve는 **SKILL.md**의 트리거·제약·워크플로우 보강에 집중하고,
  사용자 취향·메타 지침은 continual-learning 쪽에 둔다.

---

## Step 2: Extract (autoskill-extractor)

**Each transcript MUST be processed in an isolated subagent via the Task tool** to prevent earlier transcript patterns from contaminating detection in later transcripts. Aggregate extracted candidates after all transcripts complete independently.

For each transcript in scope:

1. **Dispatch a subagent** with the transcript content and the autoskill-extractor instructions
2. The subagent reads `.cursor/skills/automation/autoskill-extractor/SKILL.md` and runs extraction per that skill’s instructions
3. The subagent returns candidates with confidence >= 0.6 (at most 2 per transcript)
4. Collect all subagent results and merge candidate lists

---

## Step 3: Judge

**Each candidate MUST be judged in an isolated subagent via the Task tool** to prevent earlier add/merge/discard decisions from biasing later ones. Pass the candidate JSON and the list of existing skill descriptions as context.

For each extracted candidate, judge its relationship to existing skills.

### Decision criteria

| Decision | Condition |
|----------|-----------|
| **add** | No overlap with existing skills; confidence >= 0.7 |
| **merge** | Overlaps an existing skill but the candidate adds new value |
| **discard** | Fully redundant with an existing skill, or insufficient confidence/value |

### Finding similar skills

Compare the candidate’s triggers, tags, and description to each existing `.cursor/skills/*/SKILL.md` description:

1. Trigger phrase overlap (3+ overlapping phrases → merge candidate)
2. Functional overlap (same input → same output pattern)
3. Tag/category similarity

---

## Step 4: Apply Decisions

### add

1. Create `.cursor/skills/<name>/`
2. Convert the candidate prompt into SKILL.md format and save
3. Include name, description, and metadata in frontmatter
4. **Append or preserve** the **Project-Specific Overrides** block (see end of this SKILL.md) in new skills so agents load [.cursor/skills/references/project-overrides/](../references/project-overrides/README.md) context
5. If `--auto-optimize`, run `skill-optimizer` audit

### merge

1. Read the target skill’s SKILL.md
2. Integrate new elements from the candidate (triggers, workflow steps, examples) into the target
3. Bump the target skill’s version
4. Record what changed in the merge
5. **Preserve** any existing **Project-Specific Overrides** section on the target skill; do not strip project-overrides links when merging

### discard

1. Log the discard reason
2. No file changes

---

## Step 4b: Policy compliance check (mandatory before commit)

After **add** or **merge**, validate the resulting `SKILL.md` against project policies (canonical: `docs/policies/`). **Reject or revise** the change if any check fails.

| Policy | Check |
|--------|--------|
| **POL-001** (product identity / terminology) | No forbidden product terms; finance/stock domain wording consistent with glossary |
| **POL-002** (UI/UX design) | UI guidance uses **Tailwind + Radix** for this app; does not **require** Thaki Cloud TDS (`@thakicloud/shared`) or Figma as the design SSOT |
| **POL-003** (tone and voice) | User-facing output rules match tone policy when the skill defines customer copy |
| **POL-006** (skill governance) | Frontmatter, triggers, and “Do NOT use” clauses are present; skill does not encode **cloud-platform-only** assumptions (e.g. mandatory internal cloud product) for this self-hosted stock analytics repo |

**Reject** skills that assume a different product (generic cloud control plane, unrelated SaaS) as the default runtime. **Inject** references to [.cursor/skills/references/project-overrides/](../references/project-overrides/README.md) in the skill body or overrides table when the skill touches terminology, UI, or document standards.

---

## Step 5: Generate Evolution Report

Write a report to `outputs/autoskill-reports/<date>-evolution.md`:

```markdown
# Skill Evolution Report — YYYY-MM-DD

## Summary
- Transcripts processed: N
- Candidates extracted: M
- Skills added: A
- Skills merged (updated): U
- Skills discarded: D

## Added Skills
| Name | Description | Confidence | Source |
|------|-------------|------------|--------|

## Merged Skills
| Target Skill | Version Change | Changes | Source |
|-------------|----------------|---------|--------|

## Discarded Candidates
| Name | Reason | Confidence |
|------|--------|------------|
```

---

## Step 6 (Optional): Post to Slack

If `--slack` is set, post an evolution summary to Slack.

```
Shell: python3 scripts/slack_post_message.py --channel "<channel>" --message "*[AutoSkill Evolution] {date}*\n\nProcessed: {N} transcripts\nAdded: {A} skills | Merged: {U} | Discarded: {D}"
```

---

## Safety Guards

- Do not process the same transcript twice (state file tracking)
- At most 2 candidates per transcript (avoid skill spam)
- Minimum confidence 0.6
- Flag for human review on merge conflicts
- Use `--dry-run` to preview changes
- **Policy gate**: Do not finalize add/merge until **Step 4b** passes

---

## Examples

### Example 1: Weekly evolution run

User says: "/autoskill-evolve"

Actions:
1. Select up to 5 recent unprocessed transcripts
2. Extract 3 candidates (confidence 0.72, 0.85, 0.61)
3. Judge: 1 add, 1 merge, 1 discard
4. Create one new skill; update one existing skill; run **Step 4b** policy compliance on both
5. Write evolution report

### Example 2: Dry-run preview

User says: "autoskill evolve --dry-run --scope all"

Actions:
1. Scan all unprocessed transcripts
2. Simulate extraction and decisions
3. Present “these changes would apply” preview
4. No file changes

### Example 3: Specific session + auto-optimize

User says: "autoskill evolve --scope session abc123 --auto-optimize"

Actions:
1. Analyze that session’s transcript
2. Judge one add
3. Create the new skill, then run skill-optimizer audit
4. Refine skill structure per audit

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Missing state file | Create initial state file |
| Transcript directory not found | Verify project paths |
| All transcripts already processed | Report “no new sessions” |
| No candidates | Report “no reusable patterns found” |
| Skill directory creation failed | Report error; continue other decisions |
| Merge target SKILL.md parse error | Fall back to add as a separate skill |
| Policy compliance failure (Step 4b) | Revert or edit candidate; log reason; do not ship skill |

---

## Project-Specific Overrides

Applies only in **ai-model-event-stock-analytics**.

| Override | Path |
|----------|------|
| Terminology (POL-001) | [.cursor/skills/references/project-overrides/project-terminology-glossary.md](../references/project-overrides/project-terminology-glossary.md) |
| Design / UI stack (POL-002) | [.cursor/skills/references/project-overrides/project-design-conventions.md](../references/project-overrides/project-design-conventions.md) |
| Tone (POL-003) | [.cursor/skills/references/project-overrides/project-tone-matrix.md](../references/project-overrides/project-tone-matrix.md) |

**Constraints:** Evolved skills must remain aligned with **financial analytics** domain defaults; validate against **POL-001–POL-006**; **reject** skills that embed **cloud-platform** or **Thaki Cloud product** assumptions as mandatory for this repo; keep **project-overrides** pointers in SKILL.md where applicable.
