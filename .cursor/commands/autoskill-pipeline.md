## AutoSkill Pipeline

End-to-end meta-pipeline that orchestrates research paper analysis, multi-role strategy assessment, skill/rule/command creation, and quality assurance for adapting external AI agent learning methodologies to the Cursor skill ecosystem.

### Usage

```bash
/autoskill-pipeline --paper <url> --repo <url> --topic <name>
/autoskill-pipeline --phase analyze --paper <url>
/autoskill-pipeline --phase strategy
/autoskill-pipeline --phase implement
/autoskill-pipeline --phase optimize
```

### What it does

**Phase 1 — Research Analysis**:
1. Downloads and extracts paper content (anthropic-pdf, alphaxiv-paper-lookup)
2. Analyzes implementation repository (GitHub MCP, defuddle)
3. Runs paper-review pipeline (Korean review + PM analysis + DOCX)
4. Creates technical documentation with architecture diagrams and gap analysis

**Phase 2 — Strategy Assessment**:
1. Runs 6-role analysis in 2 parallel batches (CTO, PM, Developer, Security, UX, CSO)
2. Synthesizes into executive briefing
3. Applies PM frameworks (Lean Canvas, SWOT, PRD)
4. Produces strategy document with decision matrix

**Phase 3 — Implementation**:
1. Creates new skills (SKILL.md + references)
2. Creates rules (.mdc) and commands (.md)
3. Extends existing infrastructure (scripts, hooks, rules)

**Phase 4 — Quality Assurance**:
1. Runs skill-optimizer audit on all new skills
2. Fixes CRITICAL/HIGH findings
3. Runs integration test with sample data

### Skill

Read and follow `.cursor/skills/autoskill-pipeline/SKILL.md`
