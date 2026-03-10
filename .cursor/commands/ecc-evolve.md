---
description: "Evolve high-confidence instincts into reusable skills, commands, or Cursor rules"
---

# ECC Evolve — Promote Instincts to Skills/Commands

## Skill Reference

Read and follow the skill at `.cursor/skills/ecc-continuous-learning/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Identify Candidates

1. List all instincts with confidence >= 0.8
2. Group by domain (code-style, testing, git, debugging, workflow)
3. Identify clusters of related instincts that form a coherent pattern

### Step 2: Choose Evolution Target

For each candidate cluster, determine the best target:

- **Rule** (`.cursor/rules/*.mdc`): For coding conventions, style preferences, git patterns
- **Skill** (`.cursor/skills/*/SKILL.md`): For complex multi-step workflows
- **Command** (`.cursor/commands/*.md`): For frequently invoked single-purpose actions
- **Lesson** (`tasks/lessons.md`): For error-prevention patterns

### Step 3: Generate

Create the target file following project conventions:
- Skills: YAML frontmatter with name, description (<500 chars), "Do NOT use for..." boundaries
- Commands: YAML frontmatter with description, step-by-step instructions
- Rules: MDC format with activation guard if needed

### Step 4: Report

List what was evolved, from which instincts, and where the new file lives.

## Constraints

- Only evolve instincts with confidence >= 0.8 and evidence count >= 3
- Always check for conflicts with existing skills/commands before creating
- Update skill-orchestration.mdc if a new skill is created
