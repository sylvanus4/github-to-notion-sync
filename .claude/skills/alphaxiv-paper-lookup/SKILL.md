---
name: alphaxiv-paper-lookup
description: >-
  Look up any arXiv paper on alphaxiv.org to get a structured AI-generated
  overview (machine-readable report) without reading raw PDFs. Extracts paper
  ID from arXiv or AlphaXiv URLs, fetches the structured report, and
  optionally retrieves the full paper text as a fallback. Use when the user
  shares an arXiv link, paper ID, or asks to "explain this paper", "summarize
  arxiv paper", "look up paper", "alphaxiv", "논문 조회", "arXiv 논문 요약", "논문 설명",
  "paper overview", or references an arXiv paper ID like "2401.12345". Do NOT
  use for full academic paper review with PM analysis and PPTX (use
  paper-review), arXiv-to-NotebookLM slide pipeline (use nlm-arxiv-slides), or
  general web page extraction (use defuddle). Korean triggers: "논문 조회", "arXiv
  요약", "논문 설명", "논문 개요".
---

# AlphaXiv Paper Lookup

Fetch a structured AI-generated overview of any arXiv paper from alphaxiv.org. Faster and
more reliable than reading raw PDFs — one `curl` call returns a comprehensive markdown report.

## Input

The user provides one of:
- An arXiv URL (e.g., `https://arxiv.org/abs/2401.12345`)
- An AlphaXiv URL (e.g., `https://alphaxiv.org/overview/2401.12345`)
- A bare paper ID (e.g., `2401.12345` or `2401.12345v2`)

## Workflow

### Step 1: Extract Paper ID

Parse the paper ID from the user's input:

| Input Format | Extracted ID |
|-------------|-------------|
| `https://arxiv.org/abs/2401.12345` | `2401.12345` |
| `https://arxiv.org/pdf/2401.12345` | `2401.12345` |
| `https://alphaxiv.org/overview/2401.12345` | `2401.12345` |
| `2401.12345v2` | `2401.12345v2` |
| `2401.12345` | `2401.12345` |

### Step 2: Fetch Machine-Readable Report

```bash
curl -sL --max-time 30 "https://alphaxiv.org/overview/{PAPER_ID}.md"
```

**CRITICAL**: The `-L` flag is required to follow 301 redirects from the AlphaXiv server.

This returns a structured, detailed analysis optimized for LLM consumption — one call,
plain markdown, no JSON parsing needed.

**Check for errors**: If the response is empty or contains a 404 message, the report
has not been generated for this paper yet. Proceed to Step 3.

### Step 3: Fallback — Fetch Full Paper Text (if needed)

Use this only when:
- Step 2 returned a 404 (report not yet generated)
- The user asks about a specific equation, table, or section not in the report

```bash
curl -sL --max-time 30 "https://alphaxiv.org/abs/{PAPER_ID}.md"
```

Returns the full extracted text of the paper as markdown.

If this also returns 404, inform the user and provide the direct PDF link:
`https://arxiv.org/pdf/{PAPER_ID}`

### Step 4: Present Results

Based on the user's intent:

- **Summarize**: Present key findings, contributions, and methodology in Korean
- **Explain**: Walk through the paper's approach with technical detail
- **Save**: Write the report to a local file (e.g., `outputs/papers/{PAPER_ID}-overview.md`)
- **Compare**: Fetch multiple papers and compare approaches
- **Deep dive**: If the overview is insufficient, hand off to `paper-review` for full pipeline

## Combining with Other Skills

| Scenario | Workflow |
|----------|----------|
| Quick paper lookup | This skill alone |
| Full review + PPTX + Notion | Use `paper-review` instead |
| arXiv paper to NotebookLM slides | Use `nlm-arxiv-slides` instead |
| Find related papers after lookup | Follow up with `related-papers-scout` |
| Share findings to Slack | Post summary to `#deep-research-trending` via Slack MCP |

## Error Handling

| Error | Symptom | Action |
|-------|---------|--------|
| Report not generated | 404 on overview endpoint | Try full text endpoint; if also 404, provide PDF link |
| Timeout | `curl` hangs beyond 30s | Retry once; if persistent, suggest direct PDF download |
| Invalid paper ID | No matches from URL parsing | Ask user to verify the arXiv ID format (YYMM.NNNNN) |
| Empty response | `curl` returns empty string | Endpoint may be temporarily down; try `WebFetch` on the AlphaXiv URL as fallback |
| Paper too recent | Report not yet indexed | Inform user and provide `https://arxiv.org/abs/{PAPER_ID}` for manual reading |

## Example

### Example 1: Quick paper summary

**User**: "이 논문 요약해줘: https://arxiv.org/abs/2401.12345"

**Actions**:
1. Extract paper ID: `2401.12345`
2. Run `curl -s "https://alphaxiv.org/overview/2401.12345.md"`
3. Parse the structured report
4. Present a Korean summary covering: 핵심 기여, 방법론, 주요 결과, 한계점

### Example 2: Paper comparison

**User**: "Compare 2405.04434 and 2406.11717"

**Actions**:
1. Fetch both reports in parallel:
   - `curl -s "https://alphaxiv.org/overview/2405.04434.md"`
   - `curl -s "https://alphaxiv.org/overview/2406.11717.md"`
2. Compare: research questions, methodologies, key results, limitations
3. Present structured comparison table in Korean

### Example 3: Fallback to full text

**User**: "What's the loss function in equation 3 of 2401.12345?"

**Actions**:
1. Fetch overview: `curl -s "https://alphaxiv.org/overview/2401.12345.md"`
2. If equation detail missing, fetch full text: `curl -s "https://alphaxiv.org/abs/2401.12345.md"`
3. Locate and explain the specific equation
