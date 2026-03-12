---
name: prompt-architect
description: >-
  Analyze prompts and restructure them using 8 research-backed frameworks
  (CO-STAR, RISEN, RISE-IE, RISE-IX, TIDD-EC, RTF, Chain of Thought, Chain of
  Density). Provides framework recommendations, quality scoring, targeted
  clarifying questions, and iterative refinement. Use when the user asks to
  "architect a prompt", "structure my prompt", "which framework for this
  prompt", "improve prompt with CO-STAR", "RISEN framework", "프롬프트 설계", "프레임워크
  추천", or any framework-specific prompt design request. Do NOT use for general
  prompt polishing without framework selection (use prompt-transformer),
  creating new skills (use skill-creator), or writing documentation (use
  technical-writer).
metadata:
  author: "thaki"
  version: "1.0.0"
  source: "https://github.com/ckelsoe/claude-skill-prompt-architect"
  category: "execution"
---
# Prompt Architect — Framework-Based Prompt Design

Transform vague or incomplete prompts into well-structured, effective prompts by selecting and applying the right prompting framework.

## Workflow

Execute these 6 steps for every prompt architecture request.

### Step 1: Analyze the Original Prompt

Score the prompt across 5 dimensions (1-10 each):

| Dimension | Score 1-3 | Score 4-6 | Score 7-10 |
|-----------|-----------|-----------|------------|
| **Clarity** | Vague goal, ambiguous pronouns | Basic goal stated, some ambiguity | Clear, unambiguous, single interpretation |
| **Specificity** | Under 5 words, no details | Some details, missing specs | Quantified, named entities, format specs |
| **Context** | No background at all | Some situational info | Rich background, constraints, history |
| **Completeness** | Missing what/why/how/format | Has 1-2 of the four elements | All four elements present |
| **Structure** | Single sentence, no organization | Multi-sentence, basic flow | Sections, bullets, logical hierarchy |

Calculate overall = average of all 5. Present the scorecard to the user.

### Step 2: Recommend a Framework

Follow this decision tree top-to-bottom — first match wins:

```
Is it content/writing where audience and tone matter?
  YES → CO-STAR

Is it a multi-step process with methodology and constraints?
  YES → RISEN

Is it a data transformation with defined input → output?
  YES → RISE-IE

Is it content creation where examples clarify the desired style?
  YES → RISE-IX

Does it require explicit dos/don'ts for error prevention?
  YES → TIDD-EC

Is it a simple, well-defined task where format is the main concern?
  YES → RTF

Does it require step-by-step reasoning or problem-solving?
  YES → Chain of Thought

Does it benefit from iterative compression or refinement?
  YES → Chain of Density
```

Present 1-2 recommendations with reasoning. If the user requests a specific framework, use that instead.

### Step 3: Ask Clarifying Questions

Ask 3-5 targeted questions based on the selected framework's gaps. Load the question bank from [references/frameworks.md](references/frameworks.md) for the chosen framework. Never ask more than 5 questions at a time.

### Step 4: Apply the Framework Template

1. Load the appropriate template from [references/templates.md](references/templates.md)
2. Map the user's answers to framework components
3. Fill gaps with reasonable defaults (flag these as assumptions)
4. Structure according to framework format

### Step 5: Present the Improved Prompt

Show the result with:
- **Before**: original prompt with quality score
- **After**: structured prompt with new quality score
- **Changes**: bullet list of what was added/improved and why

### Step 6: Iterate

- Confirm the improved prompt matches the user's intent
- Refine based on feedback
- Switch or combine frameworks if the current one doesn't fit
- Continue until the user is satisfied

## Framework Quick Reference

| Framework | Components | Best For | Complexity |
|-----------|-----------|----------|------------|
| **CO-STAR** | Context, Objective, Style, Tone, Audience, Response | Content creation, writing, communications | High |
| **RISEN** | Role, Instructions, Steps, End goal, Narrowing | Multi-step processes, audits, workflows | High |
| **RISE-IE** | Role, Input, Steps, Expectation | Data analysis, transformations, processing | Medium |
| **RISE-IX** | Role, Instructions, Steps, Examples | Content creation with style references | Medium |
| **TIDD-EC** | Task type, Instructions, Do, Don't, Examples, Context | High-precision tasks, compliance, support | Medium |
| **RTF** | Role, Task, Format | Simple focused tasks, quick requests | Low |
| **Chain of Thought** | Step-by-step reasoning, verification | Problem-solving, debugging, decisions | Medium |
| **Chain of Density** | Iterative passes, progressive refinement | Summarization, compression, polishing | Medium |

For detailed component definitions, selection criteria, and complete examples, see [references/frameworks.md](references/frameworks.md).

For fill-in templates, see [references/templates.md](references/templates.md).

## Example Interaction

**User**: "Write about machine learning"

**Analysis**:
- Clarity: 2/10 — vague goal
- Specificity: 1/10 — no details
- Context: 0/10 — no background
- Completeness: 2/10 — missing most elements
- Structure: 3/10 — single sentence
- **Overall: 1.6/10**

**Recommendation**: CO-STAR (content/writing where audience and tone matter)

**Questions**:
1. What's the context? (blog, docs, presentation?)
2. Who's your audience? (beginners, experts, executives?)
3. What's your objective? (explain concepts, compare approaches, tutorial?)
4. What tone? (academic, casual, professional?)
5. What format/length?

**User**: "Blog post for executives, not technical, 800 words, professional but approachable"

**Improved Prompt** (CO-STAR):
```
CONTEXT:
Creating content for a business blog aimed at C-level executives exploring
AI/ML for their organizations. Readers understand strategy but have limited
technical ML knowledge.

OBJECTIVE:
Create an engaging article helping executives understand practical ML
applications relevant to their companies, focusing on tangible business value.

STYLE:
Professional blog combining narrative with bullet points. Include 2-3
real-world case studies. Subheadings every 150-200 words. Avoid jargon.

TONE:
Professional yet approachable. Confident without being condescending.
Practical and business-focused rather than theoretical.

AUDIENCE:
C-suite executives and senior managers who make technology investment
decisions, understand ROI, but have limited technical ML knowledge.

RESPONSE FORMAT:
800-word article with compelling headline, 2-3 sentence hook, 3-4 sections
with subheadings, mix of paragraphs and bullets, call-to-action conclusion.
```

**Score After: 8.8/10** — all dimensions improved significantly.

## Error Handling

| Problem | Cause | Solution |
|---------|-------|----------|
| User's prompt matches multiple frameworks | Ambiguous use case | Present top 2 with trade-offs, let user choose |
| User wants a framework not suited for their task | Mismatch between task and framework | Explain why another fits better, offer both |
| Quality score doesn't improve | Template applied mechanically | Re-read user's answers, ask follow-up questions |
| User provides minimal answers | Insufficient information | Reduce to 2-3 most critical questions, offer defaults |

## Key Principles

1. **Ask before assuming** — never guess intent; clarify ambiguities
2. **Explain reasoning** — why this framework? why these changes?
3. **Show your work** — display analysis and scoring, not just the result
4. **Be iterative** — start with analysis, refine progressively
5. **Respect user choices** — adapt if user prefers a different framework
