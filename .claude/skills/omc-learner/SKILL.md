---
name: omc-learner
description: >-
  Extract reusable skills from the current conversation or debugging session
  using a 3-gate quality filter: (1) not Googleable, (2) codebase-specific,
  (3) required real debugging effort. Captures decision-making heuristics and
  principles — not code snippets. Classifies learned insights as Expertise
  (domain knowledge, patterns, gotchas) or Workflow (operational procedures).
  Use when the user asks to "learn from this", "extract a skill", "save this
  as a skill", "capture this pattern", "remember this gotcha", "learner", "이걸
  스킬로 만들어", "이 패턴 저장", "이 교훈 기록", "스킬 추출", "이거 기억해둬", or after solving a
  tricky bug, discovering a non-obvious workaround, or uncovering undocumented
  behavior. Do NOT use for saving generic programming patterns (use
  documentation). Do NOT use for creating skills from external docs or repos
  (use skill-seekers). Do NOT use for creating skills from scratch without
  conversation context (use create-skill). Do NOT use for optimizing existing
  skills (use skill-optimizer or skill-autoimprove).
---

# Learner: Quality-Gated Skill Extraction

Adapted from [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) learner skill. Extracts reusable skills from conversation context using strict quality gates.

## Instructions

### Core Principle

Reusable skills are **principles and decision-making heuristics** that teach HOW TO THINK about a class of problems — not code snippets to copy-paste.

**The difference:**
- BAD (mimicking): "When you see ConnectionResetError, add this try/except block"
- GOOD (reusable): "In async network code, any I/O operation can fail independently due to client/server lifecycle mismatches. The principle: wrap each I/O operation separately, because failure between operations is the common case."

### Step 1: Recognition — Should We Extract?

Extract ONLY after one of these signals:
- Solving a tricky bug that required deep investigation
- Discovering a non-obvious workaround specific to this codebase
- Finding a hidden gotcha that wastes time when forgotten
- Uncovering undocumented behavior that affects this project
- User explicitly asks to save the current learning

### Step 2: Quality Gate (ALL Three Must Pass)

| Gate | Question | Required Answer |
|------|----------|----------------|
| **Non-Googleable** | "Could someone Google this in 5 minutes?" | NO |
| **Codebase-Specific** | "Is this specific to THIS codebase?" | YES |
| **Hard-Won** | "Did this take real debugging effort to discover?" | YES |

If ANY gate fails, do NOT extract. Explain which gate failed and why.

### Step 3: Gather Required Information

- **Problem Statement**: The SPECIFIC error, symptom, or confusion that occurred.
  - Include actual error messages, file paths, line numbers.
  - Example: "TypeError in `src/hooks/session.ts:45` when sessionId is undefined after restart"

- **Solution**: The EXACT fix, not general advice.
  - Include code snippets, file paths, configuration changes.
  - Example: "Add null check before accessing `session.user`, regenerate session on 401"

- **Triggers**: Keywords that would appear when hitting this problem again.
  - Use error message fragments, file names, symptom descriptions.
  - Example: `["sessionId undefined", "session.ts TypeError", "401 session"]`

### Step 4: Classify as Expertise or Workflow

| Classification | Description | Save As |
|----------------|-------------|---------|
| **Expertise** | Domain knowledge, pattern, gotcha, architectural insight | `{topic}-expertise` |
| **Workflow** | Operational procedure, step sequence, debugging protocol | `{topic}-workflow` |

### Step 5: Write the Skill

Use this template:

```markdown
# {Skill Name}

## The Insight
What is the underlying PRINCIPLE you discovered? Not the code, but the mental model.

## Why This Matters
What goes wrong if you don't know this? What symptom led you here?

## Recognition Pattern
How do you know when this skill applies? What are the signs?

## The Approach
The decision-making heuristic, not just code. How should the agent THINK about this?

## Example
[If code helps, show it as illustration of the principle, not copy-paste material.]
```

**Key**: A skill is REUSABLE if the agent can apply it to NEW situations, not just identical ones.

### Step 6: Save Location

- **Default**: `.cursor/skills/learned/{topic}-{expertise|workflow}/SKILL.md` — version-controlled with the repo.
- Create the directory if it doesn't exist.
- Update the skill's frontmatter with proper `name`, `description`, and trigger keywords.

### Step 7: Report

After saving, report:
- What was extracted and why it passed the quality gates
- Where it was saved
- The trigger keywords that would activate it

### Anti-Patterns (DO NOT EXTRACT)

- Generic programming patterns (use documentation instead)
- Refactoring techniques (these are universal)
- Library usage examples (use library docs)
- Type definitions or boilerplate
- Anything a junior developer could Google in 5 minutes

## Error Handling

- **Quality gate fails**: Report which gate failed and why — do NOT extract the skill.
- **Insufficient conversation context**: Ask the user to describe the problem, solution, and why it was hard to find.
- **Cannot determine if insight is Googleable**: Default to NOT extracting; suggest the user verify.
- **Output directory creation fails**: Fall back to outputting the skill content in the response for manual saving.
- **Duplicate skill topic detected**: Check `.cursor/skills/learned/` for existing skills with similar topics; suggest merging rather than creating a new one.

## When to Use

- After solving a tricky bug with deep investigation
- After discovering a non-obvious codebase-specific workaround
- After finding a hidden gotcha that wastes time when forgotten
- After uncovering undocumented behavior affecting the project
- User explicitly asks to capture the current learning

## When NOT to Use

- Saving generic programming patterns — use documentation
- Creating skills from external docs or repositories — use skill-seekers
- Creating skills from scratch without conversation context — use create-skill
- Optimizing existing skills — use skill-optimizer or skill-autoimprove
- Session-level memory capture — use ecc-continuous-learning

## Examples

<example>
After debugging a session management issue:

**Quality Gate Check:**
- Googleable? NO — specific to this project's session/JWT interaction
- Codebase-specific? YES — references src/auth/session.ts and .env config
- Hard-won? YES — took 45 minutes to trace through 3 middleware layers

**Extracted Skill:**

# JWT Session Race Condition

## The Insight
When JWT tokens are refreshed while a session is being validated, the old session
reference becomes stale. The principle: session validation and token refresh must
be atomic, or the intermediate state must be handled explicitly.

## Why This Matters
Users get randomly logged out during active sessions. The symptom appears intermittent
because it depends on the timing of the token refresh relative to the session check.

## Recognition Pattern
- "Session expired" errors during active use
- 401 responses that resolve on retry
- `session.user` is undefined despite valid JWT

## The Approach
Check for a stale session reference AFTER token refresh, not before. If the session
was created before the current token's `iat`, regenerate it.
</example>

<example>
Gate failure — correctly rejected:

User: "Save that we should use try/catch for async operations"

**Quality Gate Check:**
- Googleable? **YES** — standard async error handling
- Gate FAILED. Not extracting.

This is a universal programming pattern documented in every async/await guide.
No codebase-specific insight to capture.
</example>

<example>
After discovering a database migration gotcha:

**Quality Gate Check:**
- Googleable? NO — specific interaction between Alembic and this project's enum types
- Codebase-specific? YES — references backend/app/models/ enum patterns
- Hard-won? YES — migration silently succeeded but data was corrupted

**Extracted Skill: alembic-enum-migration-expertise**

Saved to: .cursor/skills/learned/alembic-enum-migration-expertise/SKILL.md
Triggers: ["enum migration", "Alembic enum", "migration data corruption", "MarketType"]
</example>
