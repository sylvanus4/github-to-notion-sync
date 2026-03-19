# Skill Audit Checklist

Derived from Anthropic's "Complete Guide to Building Skills for Claude" (January 2026).

## 1. Frontmatter (7 checks)

- [ ] `name` field is present
- [ ] `name` is kebab-case (no spaces, no capitals, no underscores)
- [ ] `name` matches the folder name
- [ ] `name` does not contain reserved words ("claude", "anthropic")
- [ ] `description` is present and under 1024 characters
- [ ] `description` contains no XML angle brackets (`<` or `>`)
- [ ] `metadata` field present with `author` and `version` (recommended)

### Description Quality (4 sub-checks)

- [ ] Description explains WHAT the skill does
- [ ] Description explains WHEN to use it (specific trigger phrases users would say)
- [ ] Description includes negative triggers ("Do NOT use for...")
- [ ] Description mentions relevant file types or domains if applicable

**Good description formula**: `[WHAT it does] + [WHEN to use — trigger phrases] + [Do NOT use for — negative triggers]`

## 2. Progressive Disclosure (5 checks)

- [ ] SKILL.md body is under 500 lines
- [ ] JSON schemas, large code blocks (10+ lines), and detailed tables are extracted to `references/`
- [ ] All `references/` files are linked from SKILL.md with clear "when to read" guidance
- [ ] References are at most 1 level deep from SKILL.md (no nested references)
- [ ] Reference files over 100 lines include a table of contents at the top

### Token Efficiency Principle

Claude is already very smart. Only include context Claude doesn't already have. Challenge each section: "Does this justify its token cost?" Prefer concise examples over verbose explanations.

## 3. Structure (5 checks)

- [ ] `## Examples` section exists with at least 1 example in format: User says → Actions → Result
- [ ] `## Error Handling` or `## Troubleshooting` section is present
- [ ] No `README.md` file exists inside the skill folder
- [ ] Instructions are specific and actionable (not vague like "validate things properly")
- [ ] Critical validation steps are marked with `**CRITICAL**` or use `## Important` headers

### Recommended SKILL.md Structure

```
# Skill Name
[1-2 sentence summary]

## Input
[What the user provides]

## Workflow
### Step 1: ...
### Step 2: ...

## Examples
### Example 1: [scenario]

## Error Handling
[Error table or bullet list]
```

## 4. Composability (3 checks)

- [ ] Skill does not assume it is the only skill loaded
- [ ] No conflicting global variable names or tool invocations that could clash with other skills
- [ ] Skill is self-contained: does not require reading other SKILL.md files to function (orchestrator skills excluded)

## 5. Accuracy (4 checks)

- [ ] All files referenced in SKILL.md (`references/`, `scripts/`, `assets/`) actually exist on disk
- [ ] All skills referenced (in orchestrator/registry skills) actually exist as SKILL.md files
- [ ] MCP tool names and server identifiers match what is actually available
- [ ] No outdated information (deprecated APIs, renamed paths, wrong URLs)

### How to Check Phantom References

```bash
# Find all referenced files in SKILL.md
grep -oP '\[.*?\]\((.*?)\)' SKILL.md | grep -oP '\(.*?\)' | tr -d '()'

# Verify each exists
for ref in $(above); do ls "$ref" 2>/dev/null || echo "MISSING: $ref"; done
```

For orchestrator skills that list a skill registry:
```bash
# Check each skill path exists
find .cursor/skills -name "SKILL.md" -type f | sort
```

## 6. Redundancy (3 checks)

- [ ] No content duplicated between SKILL.md body and `references/` files
- [ ] No "When to Use" section in body (trigger info belongs in frontmatter `description` only)
- [ ] No redundant external fetches (e.g., curl for data already embedded in the skill)

### Common Redundancy Patterns

| Pattern | Fix |
|---------|-----|
| "When to Use" section in body + description | Remove body section; keep only in description |
| Same table in SKILL.md and references/ | Keep in one place, link from the other |
| curl/fetch step for rules already in the skill | Remove the fetch step |
| Inline code blocks duplicating a script file | Link to the script instead |

## 7. Content Design Pattern (5 checks)

Classify the skill into one or more of the 5 content design patterns (derived from Google ADK / agentskills.io ecosystem analysis, March 2026). A skill may combine multiple patterns.

- [ ] **Pattern classification**: Skill's primary pattern(s) identifiable as one or more of: Tool Wrapper, Generator, Reviewer, Inversion, Pipeline
- [ ] **If Tool Wrapper**: Domain/API context loaded on-demand from `references/` rather than hardcoded inline. Context files are focused on a single library or API surface.
- [ ] **If Generator**: Output templates separated into `assets/templates/` and style guides / formatting rules in `references/`. Template and style concerns are not mixed in SKILL.md body.
- [ ] **If Reviewer**: Review criteria externalized to a swappable checklist file in `references/` (e.g., `review-checklist.md`). Replacing the checklist file changes the review domain without modifying the skill infrastructure.
- [ ] **If Inversion**: Explicit gate condition documented (`HARD-GATE`, `AskQuestion`, or equivalent) that prevents output generation until all required context is gathered from the user.
- [ ] **If Pipeline**: Phases have diamond gate conditions (checkpoint verification before proceeding). Phase-specific reference files are loaded only during their respective phase to conserve context window.

### Pattern Identification Guide

| Pattern | Signal in SKILL.md | Exemplar Skills |
|---------|-------------------|-----------------|
| Tool Wrapper | `references/` with API docs, coding guidelines, or library rules loaded on trigger | `backend-expert`, `security-expert`, `frontend-expert` |
| Generator | `assets/templates/` for output structure, `references/` for style/formatting rules | `docx-template-engine`, `ppt-template-engine`, `alphaear-reporter` |
| Reviewer | Swappable checklist in `references/`, audit infrastructure in SKILL.md body | `deep-review`, `simplify`, `skill-optimizer` |
| Inversion | `HARD-GATE`, `AskQuestion`, or "do NOT proceed until" blocks before any output | `sp-brainstorming`, `create-skill`, `anthropic-skill-creator` |
| Pipeline | Numbered phases with "verify before proceeding" checkpoints, phase-specific reference loading | `today`, `paper-review`, `release-commander` |

### Common Pattern Combinations

| Combination | Use Case | Example |
|-------------|----------|---------|
| Pipeline + Reviewer | Complex workflows with built-in quality gates | `release-commander` + quality checkpoint |
| Generator + Inversion | Interview for requirements before generating artifacts | `anthropic-pptx` + audience/purpose interview |
| Tool Wrapper + Reviewer | Load domain rules, then review against them | `security-expert` loads OWASP, reviews code |
| Pipeline + Inversion | Interview at pipeline start, checkpoints throughout | `paper-review` with scope confirmation |

---

## Severity Classification

| Severity | Definition | Examples |
|----------|-----------|----------|
| Critical | Skill will malfunction or fail to trigger | Missing frontmatter, phantom references causing errors |
| High | Violates core guide principles | Over 500 lines, no negative triggers (over-triggering risk) |
| Medium | Missing recommended sections | No Examples, no Error Handling |
| Low | Missing optional fields, style issues | No metadata, minor formatting |
