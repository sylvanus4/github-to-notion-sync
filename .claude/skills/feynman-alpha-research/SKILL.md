---
name: feynman-alpha-research
description: >-
  Advanced paper research operations via the alpha CLI (AlphaXiv-backed):
  semantic/keyword/agentic search, full-text reading, Q&A against PDFs, code
  repository inspection, and persistent annotation management. Use when the
  user asks to 'search papers with alpha', 'alpha search', 'alpha ask', 'read
  paper with alpha', 'alpha annotate', 'paper Q&A', 'inspect paper code',
  'alpha code', 'alpha research', '알파 리서치', '알파 검색', '논문 질의', '논문 코드 검사',
  'feynman-alpha-research', 'alpha CLI', 'alphaXiv search'. Do NOT use for
  quick paper overview without alpha CLI (use alphaxiv-paper-lookup). Do NOT
  use for full paper review with PM analysis (use paper-review). Do NOT use
  for general web search (use parallel-web-search or WebSearch). Do NOT use
  for HuggingFace paper discovery (use hf-papers).
---

# Alpha Research CLI

Extended paper research operations powered by the `alpha` CLI (AlphaXiv-backed). Provides semantic search, full-text reading, interactive Q&A, code repository inspection, and persistent annotation management.

## Prerequisites

- The `alpha` CLI must be installed: `npm install -g alpha-hub`
- Authentication: run `alpha login` to authenticate with AlphaXiv
- Check status: `alpha status`

If `alpha` is not installed, fall back to the alphaxiv-paper-lookup skill and WebSearch for equivalent functionality.

## Commands Reference

| Command | Description | When to Use |
|---------|-------------|-------------|
| `alpha search "<query>"` | Search papers | Finding papers on a topic |
| `alpha search --mode semantic "<query>"` | Semantic search (default) | Natural language queries |
| `alpha search --mode keyword "<query>"` | Exact keyword search | Specific terms, model names |
| `alpha search --mode agentic "<query>"` | Broad retrieval | Exploratory, cross-domain |
| `alpha get <arxiv-id-or-url>` | Fetch paper + annotations | Reading a specific paper |
| `alpha get --full-text <arxiv-id>` | Raw full text | When AI report is insufficient |
| `alpha ask <arxiv-id> "<question>"` | Q&A against PDF | Specific questions about a paper |
| `alpha code <github-url> [path]` | Read repo files | Inspecting paper's codebase |
| `alpha code <github-url> /` | Repo overview | Getting repository structure |
| `alpha annotate <paper-id> "<note>"` | Save annotation | Persistent notes on papers |
| `alpha annotate --clear <paper-id>` | Remove annotation | Cleaning up notes |
| `alpha annotate --list` | List all annotations | Reviewing saved notes |

## Workflow Patterns

### Pattern 1: Topic Discovery

When the user wants to explore a research area:

```bash
# Start broad with semantic search
alpha search --mode semantic "efficient attention mechanisms for long context"

# Narrow with keyword search for specific approaches
alpha search --mode keyword "ring attention"

# Get the most relevant paper
alpha get <top-result-arxiv-id>

# Ask specific questions
alpha ask <arxiv-id> "What is the computational complexity compared to standard attention?"
alpha ask <arxiv-id> "What datasets were used for evaluation?"
```

### Pattern 2: Paper Deep-Dive

When the user wants to thoroughly understand a specific paper:

```bash
# Get the AI-generated overview
alpha get <arxiv-id>

# Ask targeted questions about methodology
alpha ask <arxiv-id> "What optimizer and learning rate schedule were used?"
alpha ask <arxiv-id> "How does the proposed method handle edge cases?"

# Inspect the code implementation
alpha code <github-url> /
alpha code <github-url> src/model.py

# Save key insights
alpha annotate <arxiv-id> "Key insight: uses rotary embeddings with dynamic scaling"
```

### Pattern 3: Literature Comparison

When comparing multiple papers (feeds into feynman-source-comparison):

```bash
# Search for papers in the area
alpha search --mode agentic "comparison of efficient transformer architectures 2025"

# Read top candidates
alpha get <id-1>
alpha get <id-2>
alpha get <id-3>

# Ask the same questions across papers
alpha ask <id-1> "What is the main limitation?"
alpha ask <id-2> "What is the main limitation?"
```

### Pattern 3: Annotation Management

```bash
# Review all annotations
alpha annotate --list

# Add structured annotations
alpha annotate <id> "RELEVANCE: High for ThakiCloud GPU allocation research"
alpha annotate <id> "STATUS: Needs replication — see feynman-replication"

# Clear outdated annotations
alpha annotate --clear <old-id>
```

## Search Strategy Guide

| Goal | Mode | Example |
|------|------|---------|
| Broad exploration | `--mode agentic` | "efficient training methods for large language models" |
| Specific topic | `--mode semantic` | "how LoRA adapters affect fine-tuning stability" |
| Exact term lookup | `--mode keyword` | "FlashAttention-3" |

## Combining with Other Skills

| Need | Alpha CLI Role | Complementary Skill |
|------|---------------|-------------------|
| Quick paper overview | Not needed | alphaxiv-paper-lookup |
| Full review + PM analysis | Evidence gathering | paper-review |
| Paper-code consistency | Code inspection via `alpha code` | feynman-paper-audit |
| Source comparison | Multi-paper reading | feynman-source-comparison |
| Experiment replication | Extract implementation details | feynman-replication |
| Paper archiving | Annotation for tracking | paper-archive |
| Current news + papers | Academic papers only | alphaear-news (for news) |

## Fallback Behavior

If the `alpha` CLI is unavailable:

1. **Search**: Use `WebSearch` with `site:arxiv.org` or alphaxiv-paper-lookup
2. **Read**: Use `WebFetch` on the arXiv abstract page or alphaxiv-paper-lookup
3. **Q&A**: Download PDF via `WebFetch`, read with anthropic-pdf skill
4. **Code**: Use `Shell` with `git clone` and `Read` tool
5. **Annotate**: Save notes to `outputs/feynman/annotations.md` locally

## Output

Alpha CLI results are used inline — they feed into other workflows rather than producing standalone output files. When used standalone:

- Save search results to `outputs/feynman/alpha-search-<slug>.md`
- Save Q&A transcripts to `outputs/feynman/alpha-qa-<slug>.md`

## Verification Before Completion

- [ ] alpha CLI is installed and authenticated (or fallback used)
- [ ] Search mode matches the query intent
- [ ] All cited papers have verified arXiv IDs
- [ ] Code inspection references valid file paths
- [ ] Annotations are saved for future reference
