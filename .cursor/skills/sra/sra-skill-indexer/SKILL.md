---
name: sra-skill-indexer
description: Build a BM25-searchable index of all installed Cursor skills by scanning SKILL.md files, extracting frontmatter and body text, computing TF-IDF statistics, and writing a JSON index to outputs/sra/skill_index.json. Prerequisite for sra-retriever.
metadata:
  version: "1.0"
  category: automation
  tags: [sra, indexing, bm25, skill-retrieval]
---

# SRA Skill Indexer

Implements **Stage 0 (Skill Corpus Construction)** of the SRA paradigm (arXiv:2604.24594).

## Role

You are a skill corpus builder. You scan all installed Cursor skill directories, extract
structured metadata (YAML frontmatter: name, description) and unstructured body text from
each SKILL.md file, tokenize the content, compute term frequencies, and produce a single
BM25-ready JSON index file.

## When to Use

Use when the user asks to "build skill index", "index skills", "SRA index", "sra-skill-indexer",
"스킬 인덱스 빌드", "스킬 인덱싱", "SRA 인덱스", or when sra-retriever reports a missing/stale index.

Do NOT use for skill search/retrieval (use sra-retriever).
Do NOT use for skill creation (use create-skill).
Do NOT use for skill quality auditing (use skill-optimizer).

## Constraints

- Read-only scan: never modify SKILL.md files
- Truncate body text to 2000 chars per skill for index efficiency
- Deduplicate by absolute file path
- IDF dictionary capped at 10,000 terms to limit index size
- Output MUST be valid JSON at `outputs/sra/skill_index.json`

## Workflow

1. Run the indexer script:
   ```bash
   python scripts/sra/build_index.py
   ```
2. Verify output exists and report skill count:
   ```bash
   python -c "import json; d=json.load(open('outputs/sra/skill_index.json')); print(f'{d[\"N\"]} skills indexed')"
   ```
3. Report: total skills found, index size in KB, top-5 highest-IDF terms

## Custom Directories

Pass `--skill-dirs` to scan additional paths:
```bash
python scripts/sra/build_index.py --skill-dirs "/path/to/extra/skills,/another/path"
```

## Output Schema

```json
{
  "skills": [
    {
      "id": "skill-name",
      "path": "/absolute/path/to/SKILL.md",
      "name": "skill-name",
      "description": "...",
      "body_preview": "first 300 chars...",
      "tf": {"token": count},
      "dl": 150
    }
  ],
  "idf": {"token": 3.14},
  "avgdl": 120.5,
  "N": 500,
  "version": "1.0"
}
```

## Verification

- `outputs/sra/skill_index.json` exists and is valid JSON
- `N > 0` (at least one skill indexed)
- All indexed skills have non-empty `id` and `path`
