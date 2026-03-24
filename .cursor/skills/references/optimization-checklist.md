# Skill Optimization Checklist

Per-skill scoring rubric — 100 points total. Use this to audit each SKILL.md file.

## Scoring Categories

### 1. Description Quality (30 points)

| Check | Points | Pass Criteria |
|-------|--------|--------------|
| What it does | 6 | First sentence clearly states the skill's purpose |
| Trigger phrases | 8 | Contains "Use when..." with 3+ specific trigger phrases |
| Negative triggers | 8 | Contains "Do NOT use for..." with at least 1 alternative skill reference |
| Character limit | 4 | Description is under 1024 characters |
| No angle brackets | 4 | Zero `<` or `>` in the entire YAML frontmatter block |

### 2. Progressive Disclosure (20 points)

| Check | Points | Pass Criteria |
|-------|--------|--------------|
| Body line count | 8 | SKILL.md body is under 150 lines (200 line hard limit) |
| Heavy content extracted | 6 | Tables 10+ rows, large bash blocks, templates are in `references/` |
| Links resolve | 6 | Every `(references/...)` link points to an existing file |

### 3. Examples (15 points)

| Check | Points | Pass Criteria |
|-------|--------|--------------|
| Has examples section | 5 | An `## Examples` or `### Example` heading exists |
| At least 1 example | 5 | Contains "User says:" with a realistic trigger phrase |
| Proper format | 5 | Example follows `User says / Actions / Result` structure |

### 4. Troubleshooting (10 points)

| Check | Points | Pass Criteria |
|-------|--------|--------------|
| Has troubleshooting section | 4 | A `## Troubleshooting` heading exists |
| At least 1 entry | 3 | Contains a problem description with Cause and Solution |
| Actionable solutions | 3 | Solutions describe concrete steps, not vague advice |

### 5. Metadata (10 points)

| Check | Points | Pass Criteria |
|-------|--------|--------------|
| Version present | 5 | `metadata.version` exists in frontmatter (e.g., `"1.0.0"`) |
| Category present | 5 | `metadata.category` is meaningful for this repo (e.g. `review`, `execution`, `generation`, `orchestrator`, `self-improvement`) |

### 6. Structure (15 points)

| Check | Points | Pass Criteria |
|-------|--------|--------------|
| Clear headings | 3 | Uses H2 (`##`) for major sections, H3 for subsections |
| Output format section | 4 | Has an `## Output Format` section describing expected output |
| No scattered instructions | 4 | Instructions are grouped under workflow/steps, not scattered |
| Folder naming | 2 | Skill folder is kebab-case, no spaces/underscores/capitals |
| File naming | 2 | Main file is exactly `SKILL.md` (case-sensitive) |

## Score Interpretation

| Range | Rating | Action |
|-------|--------|--------|
| 90-100 | Excellent | No changes needed |
| 70-89 | Good | Minor improvements recommended |
| 50-69 | Needs Work | Multiple sections need attention |
| Below 50 | Poor | Major rewrite recommended |

## Audit Table Template

Copy this table to record audit results:

```
| Skill | Desc (/30) | Disclosure (/20) | Examples (/15) | Troubleshoot (/10) | Metadata (/10) | Structure (/15) | Total (/100) |
|-------|-----------|-----------------|----------------|-------------------|----------------|-----------------|-------------|
```

## Quick-Check Commands

Use these to rapidly assess a skill:

1. **Line count**: Count lines in SKILL.md body (after second `---`)
2. **Description length**: Count characters in the `description:` field
3. **Angle bracket scan**: Search for `<` or `>` in YAML frontmatter
4. **Link resolution**: Extract all `(references/...)` paths and verify files exist
5. **Section presence**: Search for `## Examples`, `## Troubleshooting`, `## Output Format` headings
6. **Metadata presence**: Check for `version:` and `category:` in frontmatter
