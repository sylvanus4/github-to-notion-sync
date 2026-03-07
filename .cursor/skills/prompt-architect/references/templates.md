# Prompt Architect — Framework Templates

Fill-in-the-blank templates for all 8 frameworks. Copy the appropriate template, replace bracketed placeholders with user-provided information, and remove any sections that don't apply.

---

## CO-STAR Template

```
CONTEXT:
[Background information, situation, constraints. What's the setting? What limitations exist?]

OBJECTIVE:
[Clear, specific goal. What exactly should be accomplished? What does success look like?]

STYLE:
[Writing style, format preferences, structural approach. Style guide? Format requirements?]

TONE:
[Emotional quality and attitude. Professional, casual, urgent, friendly, authoritative, empathetic?]

AUDIENCE:
[Who consumes this output. Expertise level? What do they care about? Characteristics?]

RESPONSE FORMAT:
[Expected output structure. How long? What sections? What level of detail?]
```

---

## RISEN Template

```
ROLE:
[Expertise level, persona, or perspective to adopt. What knowledge should be demonstrated?]

INSTRUCTIONS:
[High-level guidance, principles, overarching direction. What methodology or approach?]

STEPS:
1. [First specific action or stage]
2. [Second specific action or stage]
3. [Third specific action or stage]
[Continue with detailed, sequential steps...]

END GOAL:
[Success criteria and final desired outcome. What should be true when complete?]

NARROWING:
- Do NOT: [Specific thing to avoid]
- Avoid: [Approach or pattern to avoid]
- Out of scope: [What's not included]
- Stay within: [Boundaries and constraints]
```

---

## RISE-IE Template (Input-Expectation)

```
ROLE:
[Perspective or expertise needed for this analytical task]

INPUT:
[Description of provided data/content:
- Format and structure (CSV, JSON, text, etc.)
- Key characteristics and fields
- Any quirks or special considerations]

STEPS:
1. [Processing action 1]
2. [Processing action 2]
3. [Processing action 3]
[Continue with transformation/analysis steps...]

EXPECTATION:
[Output format and content requirements:
- Format and structure
- Required elements and sections
- Level of detail needed
- Length or size constraints]
```

---

## RISE-IX Template (Instructions-Examples)

```
ROLE:
[Persona or expertise level for this creative task]

INSTRUCTIONS:
[Main task or directive:
- What to create or accomplish
- Core requirements
- Key guidelines to follow]

STEPS:
1. [Approach or methodology step 1]
2. [Step 2]
3. [Step 3]
[Continue with workflow/process steps...]

EXAMPLES:
[Positive examples showing desired output:]

Example 1: [Reference example demonstrating desired output]

Example 2: [Second example showing format/style to match]
```

---

## TIDD-EC Template

```
TASK TYPE:
[Activity type — e.g., Data Analysis, Customer Support, Technical Documentation]

INSTRUCTIONS:
1. [First step or action]
2. [Second step or action]
3. [Continue with methodology and sequence...]

DO:
- [Required action or element]
- [Language or tone to use]
- [Structure or format to follow]
- [Information that must be present]

DON'T:
- [Error or mistake to prevent]
- [Inappropriate language or approach to avoid]
- [Common pitfall to prevent]
- [Boundary not to cross]

EXAMPLES:
Example 1 (Good):
[Detailed example showing desired output]

Example 2 (What to Avoid):
[Counter-example showing what NOT to do]

CONTEXT:
[Background information affecting the task:
- Business or domain constraints
- User-provided data to reference
- Standards or guidelines that apply]
```

---

## RTF Template

```
ROLE:
[Expertise or perspective needed]

TASK:
[Clearly and specifically what needs to be done. Explicit about the deliverable.]

FORMAT:
[How the output should be structured:
- Overall format (document, code, list, table, etc.)
- Required sections or components
- Length constraints
- Specific formatting rules]
```

---

## Chain of Thought Template

```
[Problem statement]

Think through this step-by-step:

STEP 1 — [LABEL]:
[What to analyze or calculate]

STEP 2 — [LABEL]:
[Next reasoning step]

STEP 3 — [LABEL]:
[Continue reasoning...]

STEP N — VERIFY:
[Check the answer. Does it make sense? Any errors?]
```

---

## Chain of Density Template

```
[Task description]

ITERATION 1 ([word count]):
[Comprehensive first version. Prioritize completeness over brevity.]

ITERATION 2 ([smaller word count]):
[Refine: remove redundancy, combine related points, increase density.]

ITERATION 3 ([smaller word count]):
[Further compress: keep only essentials. Every sentence must count.]

ITERATION 4 ([smallest word count]):
[Maximum density: distill to core. Remove all fluff. Preserve critical details.]

For each iteration, note what changed and why.
```

---

## Hybrid Template

Combine elements from multiple frameworks when no single one covers all needs. Include only components that add value; remove sections that don't apply.

```
CONTEXT (from CO-STAR):
[Background, situation, constraints]

ROLE (from RISEN/RISE/RTF):
[Expertise or perspective needed]

OBJECTIVE (from CO-STAR):
[Specific goal to achieve]

INPUT (from RISE-IE — if applicable):
[What's being provided, format, characteristics]

INSTRUCTIONS (from RISEN — if needed):
[Guiding principles, methodology]

STEPS (from RISEN/RISE):
1. [Detailed action 1]
2. [Detailed action 2]
3. [Continue...]

AUDIENCE (from CO-STAR — if relevant):
[Who this is for, their characteristics]

TONE & STYLE (from CO-STAR — if relevant):
[Emotional quality and writing style]

END GOAL / EXPECTATION (from RISEN/RISE):
[Success criteria, output format]

NARROWING (from RISEN — if needed):
- Avoid: [Constraints]
- Out of scope: [Boundaries]

RESPONSE FORMAT (from CO-STAR/RTF):
[Detailed output structure requirements]
```
