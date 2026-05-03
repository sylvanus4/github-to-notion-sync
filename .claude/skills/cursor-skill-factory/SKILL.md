---
name: cursor-skill-factory
description: >-
  Passive workflow observer that detects repeated multi-step patterns in agent
  sessions, proposes reusable skill candidates when a pattern recurs 3+ times,
  and generates production-ready SKILL.md files following Cursor conventions.
  Integrates with autoskill-extractor for transcript mining and
  autoskill-judge for add/merge/discard decisions. Use when the user asks to
  "observe my workflow", "detect skill patterns", "factory mode", "watch and
  learn", "auto-generate skills from sessions", "skill factory",
  "cursor-skill-factory", "워크플로우 관찰", "스킬 팩토리", "패턴 감지 모드", "세션에서 스킬 자동 생성",
  "워크플로우 학습", "관찰 모드", or wants passive skill generation from repeated agent
  interaction patterns. Do NOT use for creating skills from scratch without
  observation context (use create-skill). Do NOT use for optimizing existing
  skill prompts (use skill-autoimprove or hermes-skill-evolver). Do NOT use
  for transcript extraction without generation intent (use
  autoskill-extractor). Do NOT use for auditing skill quality without
  generation (use skill-optimizer). Do NOT use for one-off skill learning from
  a single session (use omc-learner).
disable-model-invocation: true
---

# Cursor Skill Factory

Passive workflow observer → pattern detector → skill generator pipeline adapted
from [hermes-skill-factory](https://github.com/Romanescu11/hermes-skill-factory)
for Cursor IDE.

## Core Principle

**Observe first, propose second, generate last.** Never interrupt the user's
workflow. Skills emerge from evidence of repeated patterns, not from guessing.

## When This Skill Activates

- User explicitly requests observation mode or skill factory
- A pipeline or orchestrator invokes factory mode after a session batch
- The user asks "what patterns have you seen?" or "any skills worth creating?"

## Phase 1: Observe

Passively monitor the current session or a batch of recent transcripts for:

| Signal | What to Watch |
|--------|--------------|
| **Repeated sequences** | Same 3+ tool calls in the same order across sessions |
| **Multi-step workflows** | 4+ steps that always execute together to achieve one goal |
| **User corrections** | User overrides agent behavior with the same instruction 2+ times |
| **Tool combinations** | Specific tool pairings that produce better results than individual calls |
| **Domain patterns** | Recurring domain-specific procedures (deploy, review, report) |
| **Error recovery** | Same fix applied to the same class of errors repeatedly |

### Observation Sources

1. **Live session**: Current conversation context (tool calls, user messages)
2. **Transcript archive**: `agent-transcripts/*.jsonl` files via autoskill-extractor
3. **Git history**: Repeated commit patterns via `git log --oneline -50`
4. **Hook logs**: PreToolUse/PostToolUse hook events if ecc-continuous-learning is active

### Session Separation for Transcript Analysis

When analyzing multiple transcripts from the archive, **dispatch each transcript to an isolated subagent via the Task tool**. This prevents earlier transcript patterns from biasing pattern detection in later transcripts. Aggregate pattern evidence from subagent results after all transcripts are processed independently.

### Evidence Collection Format

For each detected pattern, record:

```yaml
pattern_id: "kebab-case-descriptive"
occurrences: 3
sessions:
  - transcript_id: "uuid-1"
    turns: [12, 15, 23]
  - transcript_id: "uuid-2"
    turns: [8, 11, 14]
signal_type: "repeated-sequence"  # or multi-step, correction, combination, domain, recovery
tool_sequence:
  - WebSearch
  - Read
  - StrReplace
  - Shell (git commit)
user_goal: "Research a topic then commit findings"
confidence: 0.85
```

## Phase 2: Detect

Apply the **3-gate quality filter** before proposing any skill:

| Gate | Question | Required |
|------|----------|----------|
| **Non-Googleable** | Could someone find this workflow in documentation? | NO |
| **Project/Domain-Specific** | Is this specific to this codebase or domain? | YES |
| **Hard-Won** | Did this pattern emerge from real iteration, not obvious first attempts? | YES |

### Detection Thresholds

- **Minimum occurrences**: 3 (across 2+ distinct sessions)
- **Minimum steps**: 3 tool calls or actions in sequence
- **Confidence floor**: 0.7 (skip patterns below this)
- **Uniqueness check**: Must not duplicate an existing skill's capability

### Collision Detection

Before proposing, search for overlap with installed skills:

1. Grep all `SKILL.md` descriptions for semantic overlap with the detected pattern
2. Check trigger phrases for collision using exact and fuzzy matching
3. If overlap > 70% with an existing skill → route to `autoskill-merger` instead of creating new

## Phase 3: Propose

Present detected patterns to the user as structured proposals. Never auto-generate
without approval.

### Proposal Format

```markdown
## Skill Proposal: {pattern_name}

**Signal**: {signal_type} detected across {occurrences} sessions
**Confidence**: {confidence}

### What I Observed
{2-3 sentence summary of the repeated pattern}

### Proposed Workflow
1. Step 1 description
2. Step 2 description
3. ...

### Why This Should Be a Skill
- {reason_1: saves time, reduces errors, captures tribal knowledge}
- {reason_2}

### Overlap Assessment
- Nearest existing skill: {skill_name} ({overlap_percentage}%)
- Recommendation: CREATE NEW / MERGE INTO {existing} / SKIP

### Estimated Triggers
- English: "trigger 1", "trigger 2", "trigger 3"
- Korean: "트리거 1", "트리거 2"
```

### User Decision Gate

Wait for explicit user approval before proceeding to Phase 4:
- **approve** → Generate the skill (Phase 4)
- **merge** → Route to autoskill-merger with the target skill
- **skip** → Discard and continue observing
- **refine** → User provides adjustments, re-propose

## Phase 4: Generate

Create a production-ready `SKILL.md` following Cursor conventions.

### SKILL.md Structure Requirements

1. **YAML Frontmatter** (mandatory):
   ```yaml
   ---
   name: kebab-case-name
   description: >-
     Single paragraph with: what it does, when to use (5+ trigger phrases
     in English and Korean), Do NOT use for (3+ boundaries with alternative
     skill names).
   metadata:
     author: cursor-skill-factory
     version: "1.0.0"
     category: "{appropriate-category}"
   ---
   ```

2. **Body Sections**:
   - `# {Skill Name}` — one-line purpose
   - `## When to Use` — activation conditions
   - `## Workflow` — numbered steps with tool calls
   - `## Constraints` — guardrails and limits
   - `## Output Format` — expected deliverables
   - `## Examples` — 2+ concrete usage scenarios

3. **Quality Checklist** (all must pass):
   - [ ] Description < 500 chars
   - [ ] 5+ distinct trigger phrases (English + Korean)
   - [ ] 3+ "Do NOT use for" boundaries with alternative skill names
   - [ ] Workflow has numbered steps
   - [ ] No duplicate capability with existing skills
   - [ ] File size < 600 lines
   - [ ] If skill processes multiple items (batch loops, list iteration, multi-file scans), includes explicit per-item subagent dispatch via Task tool to prevent context contamination

### File Creation

Write to: `.cursor/skills/{category}/{skill-name}/SKILL.md`

## Phase 5: Validate

After generating, run quality checks:

1. **Format validation**: Verify YAML frontmatter parses correctly
2. **Trigger quality**: Ensure 5+ distinct trigger phrases with Korean translations
3. **Boundary check**: Verify "Do NOT use for" clauses reference real alternative skills
4. **Size check**: Confirm < 600 lines
5. **Collision re-check**: Final grep against all installed skills for trigger overlap
6. **skill-upgrade-validator**: If available, run the 12-pattern compliance check

Report validation results to the user with pass/fail per criterion.

## Integration Points

| Skill | When to Compose |
|-------|----------------|
| `autoskill-extractor` | Phase 1 — mine transcripts for patterns |
| `autoskill-judge` | Phase 3 — evaluate add/merge/discard decisions |
| `autoskill-merger` | Phase 3 — when proposal overlaps an existing skill |
| `create-skill` | Phase 4 — if the user prefers manual skill creation guidance |
| `skill-upgrade-validator` | Phase 5 — validate against 12 prompt engineering patterns |
| `omc-learner` | Complementary — captures single-session insights; factory captures cross-session patterns |
| `ecc-continuous-learning` | Complementary — provides instinct-level observations that can feed Phase 1 |

## Domain Memory

Update observation memory as you discover recurring patterns:

- Record newly detected tool sequences with session IDs and confidence scores
- Track which proposals the user approved, merged, or skipped — adjust detection thresholds accordingly
- Note trigger phrase collisions discovered during validation — maintain a collision blocklist
- Log generated skill names to prevent duplicate proposals in future sessions

Store observations in the session transcript for cross-session retrieval via `recall` or `autoskill-extractor`.

## Constraints

- **Never auto-generate skills without user approval** — always pause at Phase 3
- **Minimum 3 occurrences** before proposing — avoid over-fitting to noise
- **One proposal at a time** — present the highest-confidence pattern first
- **Respect scope** — project-scoped patterns stay project-scoped; global patterns are rare
- **No code snippets in skills** — capture decision heuristics and workflows, not code

## Freedom Level

**RIGID** — Follow the 5-phase workflow exactly. Do not skip the Propose phase (Phase 3) or auto-generate without user approval.

## Rationalization Red Flags

If you catch yourself thinking any of these, STOP — you are inflating pattern significance:

| Thought | Reality |
|---------|---------|
| "This pattern is probably common even with only 2 occurrences" | 3 is the minimum. No exceptions. |
| "The user would benefit from this skill even if they haven't repeated it" | Observation-based, not prediction-based. Wait for evidence. |
| "It's basically the same sequence with minor variations" | Minor variations mean it's NOT a stable pattern yet. |
| "I should propose this before I forget it" | Log it in Domain Memory and wait for the 3rd occurrence. |
| "This is clearly a skill even though it only appeared in one session" | Route to `omc-learner` for single-session insights, not here. |

## Gotchas

- Patterns that look repeated may be coincidental. Require 2+ distinct sessions.
- High-frequency tool calls (Read, Grep) are not patterns by themselves — look for the *sequence*.
- User corrections are the strongest signal. A single correction repeated twice is worth more than 5 uncorrected repetitions.
- When the user says "skip", truly skip — do not re-propose the same pattern.

## Example: Factory Detecting a PR Review Pattern

**Observed**: Across 4 sessions, the agent runs `git diff`, then `ReadLints`,
then `Shell (npm test)`, then formats a review comment and posts to GitHub.

**Proposal**:
> Skill Proposal: pr-lint-test-review
>
> Signal: repeated-sequence across 4 sessions (confidence: 0.92)
>
> What I Observed: Every PR review follows the same 4-step sequence —
> diff check, lint verification, test run, formatted review comment.
>
> Overlap: deep-review (35%) — different scope (deep-review is multi-domain;
> this is a lightweight single-pass lint+test check)
>
> Recommendation: CREATE NEW

**After approval**: Generates `SKILL.md` with proper frontmatter, triggers, and workflow.

## Anti-Example: Factory Rejecting a False Pattern

**Observed**: In 2 sessions, the agent ran `Read` → `Grep` → `Read` on different files.

**Analysis**:
- Occurrences: 2 (below minimum of 3)
- Sessions: 2 (meets session threshold, but occurrence count fails)
- Tool sequence: `Read → Grep → Read` is a generic exploration pattern, not a
  domain-specific workflow
- Gate check: FAILS Non-Googleable — this is standard codebase navigation

**Decision**: **DO NOT PROPOSE**. Generic tool usage patterns like read-search-read are
not skills. They are basic agent behavior. Log the observation silently and move on.
Only propose when the *goal* and *sequence* are both specific and repeated.
