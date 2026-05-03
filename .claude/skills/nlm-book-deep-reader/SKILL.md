---
name: nlm-book-deep-reader
description: >-
  6-prompt deep reading pipeline for books and long documents via Google
  NotebookLM. Follows the Stanford NotebookLM Workflow — sequentially executes
  Core Argument Extractor, Assumption Auditor, Personal Relevance Filter,
  Steelman Challenger, Action Extractor, and Permanent Note Builder. Produces
  Bloom's-taxonomy-aligned analysis that extracts deeper insights than reading
  a book twice, in ~20 minutes. Use when the user asks to "deep read a book",
  "analyze this book", "book deep reader", "Stanford NotebookLM workflow",
  "6-prompt book analysis", "deep reading pipeline", "book analysis with
  NotebookLM", "nlm-book-deep-reader", "책 심층 분석", "책 딥리딩", "북 딥리더",
  "NotebookLM 북 분석", "6단계 프롬프트 분석", "책 분석 파이프라인", "영구 노트 만들기", "Zettelkasten
  분석", or wants to extract structured insights from a book/document using
  NotebookLM. Do NOT use for ad-hoc studio_create on existing notebooks — use
  notebooklm-studio. Do NOT use for accelerated learning with quizzes and
  study artifacts — use nlm-deep-learn. Do NOT use for academic paper review
  with PM analysis — use paper-review. Do NOT use for slides-only from local
  docs — use nlm-slides. Do NOT use for notebook CRUD without the 6-prompt
  pipeline — use notebooklm.
---

# NLM Book Deep Reader

6-prompt deep reading pipeline for books and long documents via Google NotebookLM.

Based on the **Stanford Students' Secret NotebookLM Workflow** — a sequence of 6 prompts
aligned to Bloom's Cognitive Hierarchy (Understand → Analyze → Apply → Evaluate → Create)
that extracts deeper insights than reading a book twice, in approximately 20 minutes.

## Prerequisites

- NotebookLM MCP server (`user-notebooklm-mcp`) connected and authenticated
- Source material: PDF file path, URL, or pasted text
- For Prompt 3 (Personal Relevance Filter): user's context (role, challenges, goals, decisions)

## Pipeline Overview

```
Source Upload ──► P1: Core Argument ──► P2: Assumption Audit ──► P3: Personal Relevance
                                                                         │
P6: Permanent Notes ◄── P5: Action Extractor ◄── P4: Steelman Challenge ◄┘
```

| Phase | Prompt | Bloom Level | Output |
|-------|--------|-------------|--------|
| 1 | Core Argument Extractor | Understanding | Core thesis + 3-5 sub-arguments with evidence strength |
| 2 | Assumption Auditor | Analysis | Unstated assumptions + vulnerability assessment |
| 3 | Personal Relevance Filter | Application | Applicable vs. non-applicable ideas for user's context |
| 4 | Steelman & Challenger | Evaluation | Strengthened argument + strongest counter-argument + verdict |
| 5 | Action Extractor | Synthesis | 5 actionable changes ranked by impact/friction |
| 6 | Permanent Note Builder | Creation | 5 Zettelkasten-style permanent notes |

## Execution

### Phase 0: Setup — Create Notebook & Ingest Source

```
notebook_create(title="Deep Read: <Book Title>")
```

Add the source material. Supported source types:

```
source_add(notebook_id, source_type="file", file_path="<absolute_path_to_pdf>", wait=True)
source_add(notebook_id, source_type="url", url="<url>", wait=True)
source_add(notebook_id, source_type="text", text="<pasted_content>", title="<title>", wait=True)
```

Wait for source processing to complete before proceeding.

If the user has additional context documents (reviews, interviews, related articles), add them
as supplementary sources. The primary book/document should be ingested first.

### Phase 1: Core Argument Extractor

**Goal**: Identify the single core argument (not topic) the author is making, plus sub-arguments.

```
notebook_query(notebook_id, query="""
Read the entire document and identify the single core argument the author is trying to
make. Not the topic — the argument. The specific claim the author is trying to persuade
the reader of. State it in 2 sentences or fewer.

Then identify 3-5 sub-arguments that support this core argument. For each sub-argument:
1. State the claim clearly
2. Identify the evidence the author provides
3. Rate the evidence strength on a scale from Anecdote → Case Study → Survey Data →
   Meta-Analysis → Empirical Proof

Format the output as:
## Core Argument
[2 sentences max]

## Sub-Arguments
### 1. [Sub-argument title]
- **Claim**: ...
- **Evidence**: ...
- **Evidence Strength**: [rating] — [brief justification]

[repeat for each sub-argument]
""")
```

Save response as a note:
```
note(notebook_id, action="create", title="P1: Core Argument Analysis", content=<response>)
```

### Phase 2: Assumption Auditor

**Goal**: Surface unstated assumptions and assess vulnerability of the core argument.

```
notebook_query(notebook_id, query="""
Identify all significant assumptions the author makes but does not explicitly state or
defend. Consider assumptions about:
- Human nature and behavior
- How organizations work
- How change happens
- Market dynamics or social systems
- What the reader already believes

For each assumption:
1. State the assumption clearly
2. Assess: Is it supported by external evidence? Challenged by field experts?
   Or is it the author's worldview presented as universal truth?
3. Rate vulnerability: If this assumption is wrong, how much does it undermine the
   core argument? (Low / Medium / High / Critical)

Then answer: Which single assumption, if proven incorrect, would most undermine the
entire core argument? Why?

Format as:
## Identified Assumptions
### 1. [Assumption]
- **Category**: [human nature / organizational / change / market / reader belief]
- **Assessment**: [supported / challenged / worldview-as-truth]
- **Vulnerability**: [Low/Medium/High/Critical]
- **If wrong**: [impact on core argument]

[repeat for each]

## Most Critical Assumption
[Which one and why]

## Overall Robustness Assessment
[Does the book's argument survive assumption scrutiny?]
""")
```

Save response:
```
note(notebook_id, action="create", title="P2: Assumption Audit", content=<response>)
```

### Phase 3: Personal Relevance Filter

**Goal**: Filter the book through the user's specific context to find directly applicable ideas.

Before running this prompt, **ask the user** for their context if not already provided:
- Current role and work
- Key challenges they face
- Goals they're pursuing
- Decisions they're facing

```
notebook_query(notebook_id, query="""
My specific context: <USER_CONTEXT>

Filter the entire document through my context above. Categorize every major idea,
framework, and recommendation into:

## Directly Applicable
Ideas and frameworks I can apply to my specific situation right now.
For each:
- **Idea**: [what it is]
- **How it applies**: [specific application to my context]
- **Implementation sketch**: [what it would look like in my real situation]

## Interesting but Not Applicable
Ideas that are intellectually valuable but don't map to my current situation.
For each:
- **Idea**: [what it is]
- **Why not applicable**: [specific reason it doesn't fit my context]
- **When it might become relevant**: [future scenario where it applies]

## Relevance Summary
- Total applicable ideas: [count]
- Highest-impact applicable idea: [which one and why]
- Surprising connection: [an unexpected way the book relates to my work]
""")
```

Save response:
```
note(notebook_id, action="create", title="P3: Personal Relevance Filter", content=<response>)
```

### Phase 4: Steelman & Challenger

**Goal**: Stress-test the argument by making it stronger AND building the best counter-argument.

```
notebook_query(notebook_id, query="""
Perform a rigorous intellectual stress test of this book's core argument in three parts:

## Part 1: Steelman — Make the Argument Stronger
Take the author's core argument and make it STRONGER than the author did.
- Add the best supporting evidence the author didn't cite
- Identify the strongest version of this argument that could be made
- What real-world examples or data would make this argument even more compelling?

## Part 2: Steel-man Challenge — Build the Strongest Counter-Argument
Now construct the most powerful counter-argument possible:
- Who are the most credible opposing thinkers? What would they say?
- What real-world evidence contradicts the author's premise?
- What historical examples show the opposite conclusion?
- Where does the author's logic break down under edge cases?

## Part 3: Verdict Under Scrutiny
After performing both exercises:
- How well does the book's argument hold up under serious examination?
- What parts survive the challenge? What parts don't?
- Rate overall argument resilience: [Fragile / Moderate / Robust / Antifragile]
- What is the most important caveat a reader should keep in mind?
""")
```

Save response:
```
note(notebook_id, action="create", title="P4: Steelman & Challenge", content=<response>)
```

### Phase 5: Action Extractor

**Goal**: Convert insights into specific, immediately actionable behavioral changes.

```
notebook_query(notebook_id, query="""
Based on the book's core ideas AND my personal context (<USER_CONTEXT_BRIEF>),
generate exactly 5 changes I can implement within the next 30 days.

Requirements — each change must be:
- A specific behavioral change, not a vague direction like "be more strategic"
- Have a clear TRIGGER (when/where it activates)
- Have a clear ACTION (exactly what to do)
- Have a clear MEASUREMENT (how I know it's working)

Format each as:
### Change [N]: [Title]
- **Trigger**: [specific situation or cue]
- **Action**: [exactly what to do]
- **Measurement**: [how to track success]
- **Impact**: [High/Medium/Low]
- **Friction**: [High/Medium/Low]

Then:
## Ranking by Impact ÷ Friction
[Ordered list from best to worst ratio]

## Start Tomorrow
Pick the #1 ranked change and describe:
- **What exactly to do tomorrow morning**
- **What the first week looks like**
- **First checkpoint at Day 7: what to evaluate**
""")
```

Save response:
```
note(notebook_id, action="create", title="P5: Action Plan", content=<response>)
```

### Phase 6: Permanent Note Builder

**Goal**: Synthesize into 5 Zettelkasten-style permanent notes that remain useful independently.

```
notebook_query(notebook_id, query="""
Synthesize the entire book into exactly 5 permanent notes following the Zettelkasten method.

Each note must be:
1. **Core Idea in My Own Words** — Explain the idea as if to someone who hasn't read the
   book. No jargon, no references to "the author says." Pure concept.
2. **Cross-Domain Connection** — Connect this idea to a concept from a completely different
   field (science, philosophy, engineering, psychology, economics, art, etc.). Show how
   the same pattern appears elsewhere.
3. **Best Supporting Evidence** — One compelling piece of evidence that makes this idea
   credible. Specific data point, study, or real-world example.
4. **Open Question** — One important question this idea raises but doesn't fully answer.
   Something worth continued thinking.

Format each note as:
---
## Note [N]: [Concept Title]

### Idea
[2-3 sentences, own words, standalone]

### Connection
[Link to concept from another domain + why the connection matters]

### Evidence
[One specific, compelling piece of supporting evidence]

### Open Question
[One question worth continued investigation]
---

Design these notes so they are independently useful — someone who never reads this book
should still gain valuable insight from any single note.
""")
```

Save response:
```
note(notebook_id, action="create", title="P6: Permanent Notes", content=<response>)
```

### Phase 7: Synthesis & Output

After all 6 prompts complete:

1. **Compile a summary** of all 6 phases into a single Korean markdown document
2. **Save to disk** at `outputs/book-deep-reader/{date}/{slug}/analysis.md`
3. **Post to Slack** #효정-할일 with a 3-message thread:
   - Message 1: Book title + core argument (2 sentences) + overall verdict
   - Message 2: Top 3 applicable ideas + #1 action for tomorrow
   - Message 3: 5 permanent note titles as a quick reference index

**Optional outputs** (if user requests):
- Upload to Notion via `md-to-notion`
- Generate NotebookLM studio artifacts (audio overview, slides) via `notebooklm-studio`
- Generate NLM slide decks via `nlm-dual-slides`

## User Context Collection

For Phase 3, if the user hasn't provided context, ask with this template:

> 📝 개인 맥락을 입력해주세요 (Personal Relevance Filter용):
> - **현재 역할/업무**: (예: AI 플랫폼 PM, 스타트업 CTO...)
> - **주요 도전과제**: (예: 팀 스케일링, 제품 시장 적합성...)
> - **현재 목표**: (예: 시리즈 A 펀딩, MAU 10만...)
> - **직면한 의사결정**: (예: 빌드 vs 바이, 시장 피벗...)

## Flags & Options

| Flag | Default | Description |
|------|---------|-------------|
| `--skip-personal` | false | Skip Phase 3 (no personal context needed) |
| `--skip-actions` | false | Skip Phase 5 (analysis-only mode) |
| `--with-studio` | false | Generate NLM audio overview after analysis |
| `--with-slides` | false | Generate dual-audience NLM slide decks |
| `--with-notion` | false | Publish analysis to Notion |
| `--lang` | ko | Output language: ko (Korean) or en (English) |

## Error Handling

- If `source_add` fails: check file path is absolute; retry once; if still fails, try alternative source_type
- If `notebook_query` returns thin response: append "Please be more detailed and specific. Reference actual content from the source document." and re-query
- If user context is missing for Phase 3: pause and collect before proceeding
- If NotebookLM MCP is unavailable: fall back to direct LLM analysis (degraded mode without source grounding)

## Design Principles

- **Sequential, not parallel**: Each prompt builds on cumulative context in the notebook
- **Save every response as a note**: The notebook becomes a persistent artifact
- **Korean output by default**: Summary, Slack posts, and compiled document in Korean
- **Bloom's alignment preserved**: The 6 prompts follow Understanding → Analysis → Application → Evaluation → Synthesis → Creation
- **Zettelkasten fidelity**: Phase 6 produces genuinely reusable, connection-rich permanent notes
