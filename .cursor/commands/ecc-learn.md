---
description: "Extract learned patterns from the current session — observe corrections, errors, and workflows to create instincts"
---

# ECC Learn — Session Pattern Extraction

## Skill Reference

Read and follow the skill at `.cursor/skills/ecc-continuous-learning/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Determine Mode

- **No arguments / status**: Run `/instinct-status` — show all learned instincts with confidence scores
- **observe**: Analyze the current session for patterns (user corrections, error resolutions, repeated workflows)
- **review**: List instincts sorted by confidence, flag low-confidence ones for review
- **import <file>**: Import instincts from an exported file
- **export**: Export current project instincts to a shareable file

### Step 2: Execute

For **observe** mode:
1. Review recent conversation for user corrections and repeated patterns
2. Create atomic instincts with confidence scoring (0.3-0.9)
3. Tag each with domain (code-style, testing, git, debugging, workflow)
4. Save to project-scoped storage

For **status/review** mode:
1. List all instincts (project-scoped + global)
2. Show confidence, domain, and evidence count
3. Highlight candidates for promotion to global scope

### Step 3: Report

Summarize instincts found/updated with confidence scores and domain tags.

## Constraints

- Always scope instincts to the current project by default
- Do not create instincts for one-off corrections — use tasks/lessons.md instead
- Minimum 2 observations before creating an instinct (confidence >= 0.3)
