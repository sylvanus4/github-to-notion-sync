---
name: gpt-5.5-prompt-guide
description: >-
  ALWAYS invoke when writing, reviewing, migrating, or optimizing prompts for
  OpenAI GPT-5.5 or GPT-5.4 models. Covers outcome-first design, personality,
  preambles, phase parameter, retrieval budgets, verification loops, formatting,
  creative guardrails, and 8-section prompt structure. Use when the user asks to
  "write a GPT-5.5 prompt", "optimize prompt for GPT-5.5", "GPT-5.5 best
  practices", "review my OpenAI prompt", "migrate prompt to GPT-5.5", "GPT-5.5
  system prompt", "OpenAI prompt guide", "GPT-5.4 prompt", "Responses API
  prompt", "gpt-5.5-prompt-guide", "GPT-5.5 프롬프트", "GPT-5.5 가이드",
  "GPT-5.5 최적화", "OpenAI 프롬프트 가이드", "GPT-5.5 시스템 프롬프트",
  "GPT-5.5로 마이그레이션", "OpenAI 프롬프트 작성". Do NOT use for
  Claude/Anthropic prompt optimization (use prompt-architect or
  prompt-transformer). Do NOT use for general prompt framework selection without
  GPT-5.5 context (use prompt-architect). Do NOT use for Cursor skill creation
  (use create-skill).
metadata:
  author: "thaki"
  version: "1.1.0"
  source: "https://developers.openai.com/api/docs/guides/prompt-guidance?model=gpt-5.5"
  category: "execution"
---

# GPT-5.5 Prompt Guide — Outcome-First Prompting for OpenAI Models

## Core Principle

GPT-5.5 is smarter but needs **shorter, outcome-first prompts**. Over-specifying
step-by-step instructions that worked for GPT-4o often degrades GPT-5.5 output.
Tell the model **what you want**, not **how to think**.

## Constraints

- **Freedom level: Medium** — structured output format, flexible content
- Do not apply Claude-specific patterns (XML tags, "think step by step") to GPT-5.5 prompts
- Do not add prompt sections beyond what the task requires (anti-gold-plating)
- Do not generate placeholder sections like "[TBD]" or "[Insert personality here]"
- When reviewing prompts, report issues faithfully; do not soften anti-pattern findings

## When to Use This Skill

- Writing system prompts or user prompts for GPT-5.5 or GPT-5.4
- Reviewing existing prompts for GPT-5.5 compatibility
- Migrating prompts from GPT-4o/4.1 to GPT-5.5
- Building Responses API or Chat Completions workflows with GPT-5.5
- Optimizing cost/latency for GPT-5.5 deployments

## Workflow

### Mode A: Write a New GPT-5.5 Prompt

1. Clarify the task outcome (what the model should produce)
2. Apply the 8-section prompt structure (Prompt Structure section)
3. Add personality if user-facing (Personality section)
4. Set formatting rules (Formatting section)
5. Add grounding/retrieval budget if search is involved (Grounding section)
6. Add verification loop (Verification Loop section)
7. Present the draft prompt with section annotations

### Mode B: Review/Optimize an Existing Prompt for GPT-5.5

1. Read the existing prompt
2. Score against the 8-section checklist
3. Identify anti-patterns (Anti-Patterns section)
4. Propose a rewritten version with change rationale
5. Output a before/after comparison

### Mode C: Migrate a GPT-4o/4.1 Prompt to GPT-5.5

1. Read the existing prompt
2. Remove excessive chain-of-thought scaffolding
3. Convert step-by-step instructions to outcome statements
4. Add personality and preamble sections
5. Validate against the anti-pattern list

## Anti-Example — Do NOT produce output like this

> "You are a helpful assistant. Please think step by step about the user's
> question. First, analyze the context. Then, consider multiple perspectives.
> Next, weigh the pros and cons. Finally, provide a well-reasoned answer.
> Be thorough and comprehensive in your response."

This fails because: (1) no explicit personality beyond "helpful", (2) procedural
chain-of-thought that GPT-5.5 handles internally, (3) no output format, (4) no
stopping condition, (5) no verification step. Every sentence could be removed
without losing information.

---

## Prompt Structure

Order the system prompt in this sequence:

```
1. Identity         — who the model is (1-2 sentences)
2. Personality      — tone, style, behavior constraints
3. Preamble         — opening message template (if streaming)
4. Instructions     — WHAT to do, not HOW to think
5. Output format    — structure, length, language
6. Grounding rules  — citation format, retrieval budget
7. Guardrails       — what NOT to do, safety boundaries
8. Verification     — self-check before responding
```

**Key rule**: Instructions section should describe the desired *outcome*.
Bad: "First analyze X, then consider Y, then weigh Z, then..."
Good: "Produce a risk assessment covering X, Y, Z with severity ratings."

## Personality and Behavior

GPT-5.5 does not infer personality from context alone. State it explicitly.

**Pattern:**
```
You are [role]. You speak in [tone]. You [behavioral constraint].
When uncertain, you [uncertainty behavior].
```

**Example:**
```
You are a senior cloud architect. You speak in concise, technical language.
You default to AWS services unless the user specifies otherwise.
When uncertain, you state your assumption before proceeding.
```

**Anti-pattern:** Omitting personality and expecting the model to "figure it out."

## Preamble (Streaming Optimization)

For streaming use cases, add a preamble instruction so the user sees output
immediately instead of waiting for the model to reason silently.

**Pattern:**
```
Begin your response with a brief 1-sentence summary of what you will do,
then proceed with the full answer.
```

This reduces perceived latency (time to first visible token) without
affecting output quality.

## Outcome-First Instructions

Replace procedural chains with outcome declarations + stopping conditions.

| Bad (procedural) | Good (outcome-first) |
|---|---|
| "Step 1: Read the doc. Step 2: Extract entities. Step 3: Classify..." | "Extract all named entities from the document. Classify each as PERSON, ORG, or LOC. Stop when you've processed all paragraphs." |
| "Think carefully about pros and cons, weigh each factor..." | "Provide a recommendation with the top 3 pros and top 3 cons." |

**Stopping conditions** prevent the model from over-generating:
- "Stop after 5 items"
- "Limit your response to 200 words"
- "If no relevant results, say so instead of speculating"

## Formatting

Explicit formatting instructions produce dramatically better results.

**Rules:**
- Specify output structure: "Return JSON", "Use markdown table", "Bullet list"
- Set length bounds: "2-3 paragraphs", "Under 500 words"
- Define field names if structured: `{"severity": "high|medium|low", "explanation": "..."}`
- For code: specify language, style, and whether to include comments

**Anti-pattern:** Leaving format implicit and hoping the model matches your
mental model.

## Grounding, Citations, and Retrieval Budgets

When the model uses tools (web search, file search, code interpreter):

**Retrieval budget pattern:**
```
Search for up to 3 authoritative sources. Stop searching when you have
at least 2 sources that directly answer the question.
If no authoritative source is found after 3 searches, state that
the information could not be verified.
```

**Citation pattern:**
```
Cite sources inline using [Source Title](URL) format.
Do not cite sources you haven't actually retrieved.
```

The retrieval budget prevents infinite search loops and controls API costs.

## Creative Drafting Guardrails

For creative or subjective tasks, add explicit constraints:

```
Write in active voice. Avoid jargon. Target a 10th-grade reading level.
Do not use the words "delve", "tapestry", or "landscape".
Each paragraph should be 2-4 sentences maximum.
```

Without these, GPT-5.5 tends toward verbose, generic prose.

## Frontend Engineering and Visual Taste

When generating UI code or design recommendations:

```
Use modern, minimal design. Prefer whitespace over decoration.
Follow [design system name] conventions.
Use semantic HTML elements. Prefer CSS Grid for layouts.
```

GPT-5.5 produces better visual output when given explicit design taste
signals rather than generic "make it look good" instructions.

## Verification Loop (Self-Check)

Add a verification step before the model finalizes its response:

**Pattern:**
```
Before responding, verify:
1. Does my answer directly address the user's question?
2. Are all claims grounded in retrieved sources or stated as opinions?
3. Does the format match what was requested?
4. Have I stayed within the specified length/scope?
If any check fails, revise before outputting.
```

This catches hallucinations and format drift at generation time.

## Phase Parameter (Responses API)

For long-running or tool-heavy Responses API workflows:

- `phase: "thinking"` — model is reasoning/searching (intermediate)
- `phase: "responding"` — model is producing the final answer

**Usage:**
```
When using tools, emit intermediate status updates with phase="thinking".
Only emit the final answer with phase="responding".
```

This lets the frontend show progress indicators during tool use.

## GPT-5.5 Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| Long chain-of-thought scaffolding | GPT-5.5 reasons well internally; explicit CoT wastes tokens | State the outcome, let the model reason |
| "Think step by step" | Marginal benefit on GPT-5.5, increases latency | Remove or replace with verification loop |
| Excessive examples (>3) | Overfits to example format, misses edge cases | Use 1-2 examples + clear rules |
| Negative-only instructions | "Don't do X, don't do Y" without positive guidance | State what TO do, then add boundaries |
| Implicit format expectations | Model guesses wrong format | Explicitly specify output structure |
| No personality statement | Generic, inconsistent tone | Add explicit personality section |
| No stopping condition | Over-generation, wandering output | Add explicit limits and stop criteria |
| Retrieval without budget | Infinite search loops, high cost | Set source count and stop rules |

## GPT-5.4 Compatibility Patterns

These patterns work for both GPT-5.4 and GPT-5.5:

### Compact Outputs
```
Respond concisely. Use bullet points for lists. Omit preamble unless asked.
```

### Clear Defaults
```
Default to [X] unless the user specifies otherwise.
```

### Tool Persistence
```
When a tool call fails, retry once with adjusted parameters.
If it fails again, explain the failure and suggest alternatives.
```

### Missing Context Gating
```
If the user's request is ambiguous or missing critical information,
ask a clarifying question instead of guessing.
```

### Action Safety
```
For destructive actions (delete, overwrite, send), confirm with the user
before executing. Preview the action and wait for approval.
```

## Image Tasks

For vision/image analysis tasks, specify detail level:

```
Analyze this image at [high|original|low] detail.
- high: examine fine details, text, small elements
- original: full resolution analysis
- low: quick overview, general composition
```

Default to `high` for document/text extraction, `low` for general description.

---

## Quick Reference: Prompt Template

```
[IDENTITY]
You are [role] specializing in [domain].

[PERSONALITY]
You speak in [tone]. You [behavioral rules]. When uncertain, you [behavior].

[PREAMBLE]
Begin each response with a one-line summary of your approach.

[INSTRUCTIONS]
[Outcome statement 1]
[Outcome statement 2]
[Stopping condition]

[FORMAT]
Return your answer as [format]. Limit to [length].

[GROUNDING]
Cite sources as [citation format]. Search up to [N] sources.
Stop searching when [stopping rule].

[GUARDRAILS]
Do not [prohibited behavior 1].
Do not [prohibited behavior 2].

[VERIFICATION]
Before responding, verify: [checklist items].
```

---

## Gotchas

1. **GPT-5.5 is NOT Claude**: Do not apply Claude-specific patterns (XML tags
   for context, "think step by step" emphasis). Use this skill for OpenAI models
   only.
2. **Preamble is for streaming**: Skip the preamble section if using
   non-streaming batch processing.
3. **Phase parameter is Responses API only**: Does not apply to Chat Completions.
4. **Retrieval budgets require tool access**: Only relevant when the model has
   web_search or file_search tools enabled.
5. **Over-constraining kills creativity**: For open-ended creative tasks, use
   fewer guardrails. The anti-pattern list is for precision tasks.
