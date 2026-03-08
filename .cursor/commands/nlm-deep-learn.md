## NLM Deep Learn

Accelerated learning pipeline: mass-upload source materials to NotebookLM, extract mental models experts share, map expert disagreements and consensus, run deep-understanding quiz sessions with gap analysis, and generate study artifacts.

### Usage

```
/nlm-deep-learn "<subject>"                                                  # interactive — gather sources and run full pipeline
/nlm-deep-learn "<subject>" --sources file1.pdf file2.pdf                    # upload local files
/nlm-deep-learn "<subject>" --urls "https://..." "https://..."               # upload URLs
/nlm-deep-learn "<subject>" --rounds 5 --questions 10                        # 5 quiz rounds, 10 questions each
/nlm-deep-learn "<subject>" --sources-only                                   # stop after source ingestion
/nlm-deep-learn "<subject>" --skip-artifacts --lang en                       # quiz only, English
/nlm-deep-learn "<subject>" --artifacts "audio,quiz"                         # generate only debate podcast and quiz
/nlm-deep-learn "<subject>" --share "colleague@company.com"                  # share notebook after creation
```

### Pipeline

1. **Gather** — Collect subject, learning goal, and source materials from the user
2. **Ingest** — Create NotebookLM notebook, upload all sources, optionally run web research
3. **Extract** — Query for 5 core mental models every expert shares
4. **Map** — Query for expert disagreements, consensus, and open questions; compile intellectual landscape document
5. **Quiz** — Generate deep-understanding questions, present via interactive quiz, explain wrong answers
6. **Analyze** — Compile gap analysis and targeted study plan
7. **Generate** — Create 5 study artifacts: debate podcast, flashcards, quiz, mind map, study guide

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--sources` | Local files to upload (PDF, DOCX, TXT) | Interactive |
| `--urls` | URLs to add as sources | Interactive |
| `--lang en/ko` | Language for content generation | Both EN + KO |
| `--rounds N` | Number of quiz rounds | 3 |
| `--questions N` | Questions per quiz round | 5 |
| `--skip-artifacts` | Skip studio artifact generation | Artifacts enabled |
| `--artifacts "types"` | Generate only specified artifact types | All 5 |
| `--sources-only` | Stop after source ingestion | Full pipeline |
| `--skip-research` | Skip web research enrichment | Research enabled |
| `--share "emails"` | Share notebook with collaborators | No sharing |

### Execution

1. Read and follow `.cursor/skills/nlm-deep-learn/SKILL.md`
2. Read the system prompt at `.cursor/skills/nlm-deep-learn/references/system-prompt.md`
3. Read the question rules at `.cursor/skills/nlm-deep-learn/references/question-rules.md`
4. Execute the 7-phase pipeline using `notebooklm-mcp` MCP tools

MCP tools used: `notebook_create`, `source_add`, `notebook_query`, `note`, `research_start`, `research_status`, `research_import`, `studio_create`, `studio_status`, `download_artifact`.

### Examples

Learn Transformer architectures from papers:
```
/nlm-deep-learn "Transformer Architectures" --sources ~/papers/attention.pdf ~/papers/bert.pdf --urls "https://jalammar.github.io/illustrated-transformer/"
```

Quick mental model extraction without quizzing:
```
/nlm-deep-learn "Quantum Computing" --sources textbook.pdf --sources-only
```

Intensive study session with many rounds:
```
/nlm-deep-learn "Microeconomics" --rounds 6 --questions 8 --skip-artifacts
```

Generate only debate podcast and study guide:
```
/nlm-deep-learn "Climate Science" --sources report.pdf --artifacts "audio,report"
```
