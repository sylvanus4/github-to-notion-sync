---
name: skill-upgrade-validator
description: >-
  Validate SKILL.md files against the 12 prompt engineering patterns defined in
  skill-prompt-patterns.mdc. Scores compliance (0-12), generates upgrade
  suggestions, and produces a summary report. Patterns 11-12 cover YAML trigger
  quality (Anthropic 5-component guide) and failure mode prevention (5 failure modes).
  Use when the user asks to "validate skill patterns", "check skill compliance",
  "score skill patterns", "pattern coverage check", "skill pattern audit",
  "upgrade validator", "skill-upgrade-validator", "trigger quality check",
  "failure mode check", "스킬 패턴 검증", "스킬 패턴 점수", "패턴 커버리지",
  "스킬 업그레이드 검증", "패턴 준수 확인", "트리거 품질 검증", "실패 모드 검증".
  Do NOT use for general skill quality auditing without pattern focus (use
  skill-optimizer). Do NOT use for autonomous prompt mutation (use
  skill-autoimprove). Do NOT use for creating new skills (use create-skill).
  Do NOT use for skill trigger accuracy testing (use skill-optimizer eval mode).
metadata:
  author: "thaki"
  version: "2.0.0"
  category: "automation"
---

# Skill Upgrade Validator

Validate SKILL.md files against the 12 prompt engineering patterns from `skill-prompt-patterns.mdc`. Produces a compliance score (0-12) per skill and actionable upgrade suggestions. Patterns 11-12 cover YAML trigger quality engineering and Anthropic's 5 failure mode prevention.

## Input

The user provides:
1. **Scope** — a single skill path, a skill category directory, or "all" (default: "all")
2. **Threshold** (optional) — minimum passing score (default: 4)
3. **Tier filter** (optional) — "tier-1", "tier-2", "tier-3", or "all" (default: "all")

## Pattern Detection Rules

Each pattern maps to specific text markers in a SKILL.md file.

| # | Pattern | Detection Markers |
|---|---------|-------------------|
| 1 | Sectioned Prompt Structure | Has at least 4 of: `## Role`, `## Constraints`, `## Domain Behavior`, `## Tools`, `## Output Format`, `## Verification`, `## Input`, `## Workflow`, `## Steps` (alternative section names count — any `##` heading that separates role/constraints/behavior/tools/output/verification into distinct blocks) |
| 2 | Anti-Gold-Plating | Contains phrases: "do not add features", "simplest approach", "do not pad", "match.*length to content", "anti-gold-plating", "Output Discipline", or a section titled `## Output Discipline` |
| 3 | Verification-Before-Completion | Contains: `VERDICT:`, `PASS.*FAIL`, "verification", "verify.*before.*complet", or a section titled `## Verification` or `## Verification Protocol` with command-run instructions |
| 4 | Coordinator Synthesis | Contains: "lazy delegation", "purpose statement", "coordinator.*synthe", "specific specs", "file paths.*line numbers", or a section titled `## Coordinator Synthesis` |
| 5 | Honest Reporting | Contains: "report outcomes faithfully", "never claim.*all checks pass", "never suppress", "honest reporting", or a section titled `## Honest Reporting` |
| 6 | Subagent Contract | Contains: "absolute file paths", "load-bearing", "subagent.*return", "purpose statement.*subagent", or a section titled `## Subagent Contract` |
| 7 | Rationalization Detection | Contains: "rationalization", "reading is not verification", "probably is not verified", "adversarial probe", or a section titled `## Rationalization Detection` |
| 8 | Domain Memory | Contains: "update memory", "domain.*memory", "what you found.*where.*why", or a section titled `## Domain Memory` |
| 9 | Gotchas Section | Contains a section titled `## Gotchas` or `## Known Issues` or `## Common Pitfalls`, with at least 2 bullet items documenting failure patterns |
| 10 | Progressive Disclosure via Filesystem | Skill directory contains `references/`, `scripts/`, `assets/`, or `config.json`; OR SKILL.md references reading from companion files (e.g., "read references/", "see scripts/", "load config.json") |
| 11 | Trigger Quality Engineering | YAML `description` contains: (a) 5+ distinct trigger phrases (count comma/quote-separated phrases in description), (b) at least one `Do NOT use for` clause, (c) directive language ("ALWAYS invoke", "Use when the user asks to", "Use when") — must satisfy all 3. Partial credit (0.5) if only 2 of 3 are met. |
| 12 | Failure Mode Prevention | Contains at least 2 of: (a) `## Gotchas` or `## Known Issues` section (reuse Pattern 9 signal), (b) `## Constraints` with freedom level mention ("high freedom", "medium freedom", "low freedom") or explicit scope boundaries, (c) output format specification (`## Output Format` or inline format examples), (d) `disable-model-invocation: true` for side-effect skills, (e) explicit `## Edge Cases` or edge case handling section. Partial credit (0.5) if only 1 of the above is met. |

## Tier Classification

Skills are classified into tiers based on their category and function:

| Tier | Expected Minimum | Skill Types |
|------|-----------------|-------------|
| Tier-1 | 5/12 (Patterns 1, 2, 3, 5, 11) | Document generation: anthropic-docx, anthropic-pptx, anthropic-pdf, anthropic-canvas-design, anthropic-frontend-design, docx-template-engine, ppt-template-engine, office-template-enforcer |
| Tier-2 | 6/12 (Patterns 1, 4, 5, 6, 9, 11) | Pipeline orchestrators: today, morning-ship, daily-am-orchestrator, daily-pm-orchestrator, eod-ship, google-daily, deep-review, simplify, ship, release-commander, mission-control |
| Tier-3 | 6/12 (Patterns 1, 3, 5, 7, 9, 11) | Review/quality: quality-gate-orchestrator, code-review-all, test-suite, security-expert, ai-quality-evaluator, ecc-verification-loop, ecc-eval-harness, skill-autoimprove |
| Tier-API | 5/12 (Patterns 1, 9, 10, 11) | Library/API reference: anthropic-claude-api, anthropic-mcp-builder, hf-cli, tossinvest-cli, gws-*, context7-mcp |
| Tier-SideEffect | 6/12 (Patterns 1, 3, 11, 12) | Side-effect skills: tossinvest-trading, release-deployer, eod-ship, domain-commit, deploy-related skills |
| General | 3/12 (Patterns 1, 11 + any other) | All other skills |

## Workflow

### Step 1: Discover Skills

```
If scope == "all":
  Glob .cursor/skills/**/SKILL.md
If scope is a directory:
  Glob {scope}/**/SKILL.md
If scope is a single file:
  Use that file directly
```

### Step 2: Scan Each Skill

For each SKILL.md file:

1. Read the file content
2. Apply all 12 pattern detection rules (case-insensitive matching)
3. Record which patterns are present (1), partial (0.5), or absent (0)
4. Calculate score: sum of present/partial patterns (0-12)
5. Determine the skill's tier from the classification table
6. Check if the score meets the tier's expected minimum

### Step 3: Generate Upgrade Suggestions

For each absent pattern in a skill, generate a specific suggestion:

| Missing Pattern | Suggestion |
|----------------|------------|
| 1 (Sectioned Structure) | "Add distinct `## Role`, `## Constraints`, `## Domain Behavior`, `## Output Format` sections to separate concerns" |
| 2 (Anti-Gold-Plating) | "Add `## Output Discipline` section with rules against unnecessary embellishment and placeholder content" |
| 3 (Verification) | "Add `## Verification Protocol` with command-run blocks and VERDICT: PASS/FAIL format" |
| 4 (Coordinator Synthesis) | "Add `## Coordinator Synthesis` section forbidding lazy delegation and requiring purpose statements for subagents" |
| 5 (Honest Reporting) | "Add `## Honest Reporting` section requiring faithful outcome reporting without suppression" |
| 6 (Subagent Contract) | "Add `## Subagent Contract` section requiring absolute paths, load-bearing snippets, and concise returns" |
| 7 (Rationalization Detection) | "Add `## Rationalization Detection` section with the rationalization table and adversarial probe requirement" |
| 8 (Domain Memory) | "Add domain-specific memory update instructions for knowledge that accumulates across runs" |
| 9 (Gotchas Section) | "Add `## Gotchas` section documenting 2-3 common failure patterns (symptom → root cause → correct approach)" |
| 10 (Progressive Disclosure) | "Move large reference material to `references/*.md`, add executable helpers to `scripts/`, and create `config.json` for user settings" |
| 11 (Trigger Quality) | "Ensure YAML `description` includes 5-7+ trigger phrases with directive language ('ALWAYS invoke', 'Use when'), at least one `Do NOT use for...` negative boundary naming alternative skills, and third-person narration" |
| 12 (Failure Mode Prevention) | "Add `## Constraints` with freedom level (High/Medium/Low), `## Output Format` with explicit structure, `## Gotchas` with edge case handling. Side-effect skills MUST use `disable-model-invocation: true` equivalent and Low freedom" |

Only suggest patterns that are marked as Required or Optional for the skill's tier in the Application Guide.

### Step 4: Output Report

Produce a structured markdown report:

```markdown
# Skill Upgrade Validation Report

**Date:** YYYY-MM-DD
**Scope:** [what was scanned]
**Skills scanned:** N
**Average score:** X.X / 12
**Skills below threshold:** N

## Summary by Tier

| Tier | Skills | Avg Score | Passing | Failing |
|------|--------|-----------|---------|---------|
| Tier-1 | N | X.X | N | N |
| Tier-2 | N | X.X | N | N |
| Tier-3 | N | X.X | N | N |
| Tier-API | N | X.X | N | N |
| General | N | X.X | N | N |

## Detailed Results

### [skill-name] — Score: X/12 [PASS/FAIL]

| Pattern | Status |
|---------|--------|
| 1. Sectioned Structure | ✓ / ✗ |
| 2. Anti-Gold-Plating | ✓ / ✗ |
| 3. Verification | ✓ / ✗ |
| 4. Coordinator Synthesis | ✓ / ✗ |
| 5. Honest Reporting | ✓ / ✗ |
| 6. Subagent Contract | ✓ / ✗ |
| 7. Rationalization Detection | ✓ / ✗ |
| 8. Domain Memory | ✓ / ✗ |
| 9. Gotchas Section | ✓ / ✗ |
| 10. Progressive Disclosure | ✓ / ✗ |
| 11. Trigger Quality | ✓ / △ / ✗ |
| 12. Failure Mode Prevention | ✓ / △ / ✗ |

**Suggestions:**
- [specific suggestion for each missing required/optional pattern]

[... repeat for each skill ...]

## Top Upgrade Opportunities

[List the 10 skills with the lowest scores that would benefit most from upgrades,
 prioritized by: (1) tier importance, (2) gap from tier minimum, (3) usage frequency]
```

Write the report to `outputs/skill-validation/validation-{date}.md`.

### Step 5: Slack Summary (Optional)

If the user requests Slack posting, send a summary to `#효정-할일` with:
- Total skills scanned and average score
- Number passing/failing by tier
- Top 5 skills needing attention

## Constraints

- Do NOT modify any SKILL.md files — this skill is read-only validation
- Do NOT count the same pattern twice if detected by multiple markers
- Do NOT penalize skills for missing patterns that are neither Required nor Optional for their tier
- Pattern detection is heuristic — explicit section headings (`## Honest Reporting`) are definitive; inline text matches are probabilistic and require at least 2 distinct marker matches to confirm
- Score thresholds are advisory — FAIL does not block anything, it highlights upgrade opportunities
- For large scopes (100+ skills), use parallel subagents in batches of 20

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected

## Honest Reporting

- Report outcomes faithfully: if most skills fail the threshold, say so
- Never inflate scores to avoid alarming results
- Present data as-is — the user decides what action to take
- When a pattern detection is ambiguous (inline text match but no explicit section), report as "partial" with an explanation
