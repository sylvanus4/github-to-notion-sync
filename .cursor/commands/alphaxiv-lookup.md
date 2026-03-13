## AlphaXiv Paper Lookup

Look up any arXiv paper on alphaxiv.org and get a structured AI-generated overview without reading raw PDFs.

### Usage

```
/alphaxiv-lookup {arxiv_url_or_paper_id}
/alphaxiv-lookup {paper_id_1} {paper_id_2}       # compare two papers
/alphaxiv-lookup {arxiv_url} --save               # save report to outputs/papers/
/alphaxiv-lookup {arxiv_url} --deep               # hand off to paper-review for full analysis
```

### Workflow

1. **Parse** — Extract paper ID(s) from arXiv URL, AlphaXiv URL, or bare ID
2. **Fetch** — Get structured AI overview from `alphaxiv.org/overview/{id}.md`
3. **Fallback** — If overview unavailable, try full text from `alphaxiv.org/abs/{id}.md`
4. **Present** — Summarize key findings in Korean (핵심 기여, 방법론, 결과, 한계점)
5. **Optional** — Save to file, compare papers, or escalate to full `paper-review` pipeline

### Execution

Read and follow the `alphaxiv-paper-lookup` skill (`.cursor/skills/alphaxiv-paper-lookup/SKILL.md`).

### Examples

Quick lookup:
```
/alphaxiv-lookup https://arxiv.org/abs/2401.12345
```

Bare paper ID:
```
/alphaxiv-lookup 2405.04434
```

Compare two papers:
```
/alphaxiv-lookup 2405.04434 2406.11717
```

Save report locally:
```
/alphaxiv-lookup 2401.12345 --save
```

Full review pipeline:
```
/alphaxiv-lookup 2401.12345 --deep
```

User input:

$ARGUMENTS
