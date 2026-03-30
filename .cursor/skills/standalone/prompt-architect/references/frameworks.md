# Prompt Architect — Framework Reference

Consolidated reference for all 8 prompting frameworks. Each section contains: components, when to use, when to avoid, clarifying questions, and one complete before/after example.

---

## 1. CO-STAR (Context, Objective, Style, Tone, Audience, Response)

### Components

| Component | Purpose | Key Question |
|-----------|---------|--------------|
| **Context** | Background, situation, constraints | "What's the situation?" |
| **Objective** | Clear, specific goal | "What do you want achieved?" |
| **Style** | Writing style, format, structure | "How should it be written?" |
| **Tone** | Emotional quality, formality | "What feeling should it convey?" |
| **Audience** | Reader characteristics, expertise | "Who is this for?" |
| **Response** | Output structure, length, format | "What should the output look like?" |

### When to Use
- Content creation, blog posts, emails, marketing copy
- Tasks where audience, tone, and style significantly impact quality
- Communications to specific stakeholder groups
- Brand voice consistency matters

### When to Avoid
- Purely analytical/technical tasks
- Simple format conversions
- Tasks where audience is irrelevant

### Clarifying Questions
1. What's the background context or situation?
2. Who is your target audience? (expertise level, role, characteristics)
3. What specific objective do you want to achieve?
4. What tone is appropriate? (professional, casual, urgent, friendly)
5. What style or format should the output follow?
6. How should the response be structured? (length, sections, format)

### Example

**Before**: "Write about the benefits of exercise."

**After**:
```
CONTEXT:
Creating content for a health blog aimed at busy professionals who struggle
to find time for fitness. Part of a lifestyle improvements series.

OBJECTIVE:
Create an engaging article that convinces time-pressed professionals that
exercise is worth prioritizing, focusing on benefits beyond physical health.

STYLE:
Conversational blog style with short paragraphs (2-3 sentences), subheadings
every 150-200 words, and bullet points for key takeaways. Avoid medical jargon.

TONE:
Encouraging and motivating without being preachy. Acknowledge time constraints.
Be practical and realistic rather than idealistic.

AUDIENCE:
Professionals aged 30-50 working 50+ hours/week with limited free time.
Skeptical of unrealistic fitness advice.

RESPONSE FORMAT:
800-word article with engaging headline, brief introduction, 4-5 sections
with subheadings, bullet points highlighting key benefits, practical
conclusion with next steps.
```

---

## 2. RISEN (Role, Instructions, Steps, End goal, Narrowing)

### Components

| Component | Purpose | Key Question |
|-----------|---------|--------------|
| **Role** | Expertise, persona, perspective | "What perspective is needed?" |
| **Instructions** | High-level principles, methodology | "What approach should guide this?" |
| **Steps** | Detailed sequential actions | "What's the exact sequence?" |
| **End goal** | Success criteria, acceptance criteria | "What defines completion?" |
| **Narrowing** | Constraints, boundaries, what NOT to do | "What should be avoided?" |

### When to Use
- Complex multi-step processes with sequential dependencies
- Tasks requiring specific methodology
- When defining what NOT to do is critical
- Audits, reviews, workflows, SOPs

### When to Avoid
- Simple one-step tasks
- Tasks where any approach is acceptable
- Quick requests without process requirements

### Clarifying Questions
1. What role or expertise level should be demonstrated?
2. What principles or guidelines should guide the approach?
3. What are the specific steps or sequence of actions?
4. What defines success? What are the acceptance criteria?
5. What should be avoided? What constraints exist?

### Example

**Before**: "Help me review this codebase."

**After**:
```
ROLE:
Senior code reviewer with expertise in Python and system security,
10+ years identifying vulnerabilities and architectural issues.

INSTRUCTIONS:
Conduct a security-focused code review following OWASP guidelines.
Prioritize security vulnerabilities over style issues.

STEPS:
1. Scan for common security vulnerabilities (SQL injection, XSS, auth issues)
2. Review authentication and authorization logic
3. Examine data validation and sanitization
4. Check for sensitive data exposure
5. Analyze third-party dependencies for known vulnerabilities
6. Assess error handling and logging practices
7. Document findings with severity ratings
8. Provide remediation recommendations

END GOAL:
Comprehensive security assessment categorizing vulnerabilities by severity
(Critical/High/Medium/Low) with specific code references and concrete
remediation steps prioritized by risk and effort.

NARROWING:
- Do NOT focus on code style or formatting issues
- Do NOT suggest complete rewrites; focus on targeted fixes
- Avoid generic security advice; be specific to this codebase
- Stay within Python ecosystem; don't suggest language changes
```

---

## 3. RISE-IE (Role, Input, Steps, Expectation)

Data-focused variant for input-to-output transformations.

### Components

| Component | Purpose | Key Question |
|-----------|---------|--------------|
| **Role** | Analytical expertise needed | "What perspective is needed?" |
| **Input** | Data format, structure, characteristics | "What am I working with?" |
| **Steps** | Processing/transformation methodology | "How do I transform it?" |
| **Expectation** | Output format and requirements | "What should I produce?" |

### When to Use
- Data analysis and transformation tasks
- Working with specific data formats (CSV, JSON, logs)
- Input-to-output processing workflows
- Report generation from structured data

### When to Avoid
- Creative content creation (use RISE-IX or CO-STAR)
- Tasks without defined input data
- Simple tasks with no processing steps (use RTF)

### Clarifying Questions
1. What role or perspective is needed for this analytical task?
2. What input are you providing? (format, structure, characteristics)
3. What processing or transformation steps are needed?
4. What should the output look like? (format, required elements)
5. Are there any data quirks or edge cases to handle?

### Example

**Before**: "Analyze these customer reviews."

**After**:
```
ROLE:
Customer insights analyst with expertise in sentiment analysis.

INPUT:
50 customer reviews from our mobile app, each containing:
- Star rating (1-5), written feedback, date, user segment (free/premium)

STEPS:
1. Categorize reviews by sentiment (positive, neutral, negative)
2. Extract common themes and topics mentioned
3. Identify feature requests vs. complaints vs. praise
4. Segment findings by user type (free vs. premium)
5. Highlight urgent issues mentioned multiple times

EXPECTATION:
- Summary table showing sentiment distribution
- Top 5 themes with frequency counts
- Feature requests ranked by mentions
- Critical issues requiring immediate attention
- Comparison of free vs. premium feedback
- 2-3 actionable recommendations
```

---

## 4. RISE-IX (Role, Instructions, Steps, Examples)

Instruction-focused variant for content creation with style references.

### Components

| Component | Purpose | Key Question |
|-----------|---------|--------------|
| **Role** | Creative persona or expertise | "Who should I be?" |
| **Instructions** | Task directive and requirements | "What should I create?" |
| **Steps** | Workflow methodology | "How should I approach it?" |
| **Examples** | Reference outputs showing desired style | "What does good look like?" |

### When to Use
- Content creation where examples clarify the desired style
- Replicating existing formats or tones
- Creative work requiring reference points
- Writing with specific style requirements

### When to Avoid
- Data processing tasks (use RISE-IE)
- Tasks without available style references
- Simple tasks with clear format specs (use RTF)

### Clarifying Questions
1. What role or persona is most appropriate?
2. What are the main instructions or task requirements?
3. What workflow or steps should be followed?
4. Can you provide 2-3 examples of desired output or style?
5. What format or style should be replicated?

### Example

**Before**: "Write product descriptions for our sustainable clothing line."

**After**:
```
ROLE:
Senior copywriter specializing in sustainable fashion and eco-conscious brands.

INSTRUCTIONS:
Create compelling product descriptions that:
- Highlight eco-friendly materials and production methods
- Appeal to environmentally conscious millennials
- Emphasize both style and sustainability
- Drive purchase intent through emotional connection

STEPS:
1. Open with the product's unique appeal
2. Describe sustainable materials and ethical production
3. Highlight style, fit, and versatility
4. Include technical details (materials, care, sizing)
5. Close with a CTA emphasizing purchase impact

EXAMPLES:
"The Ocean Breeze Tee — Crafted from 100% recycled ocean plastics, this
impossibly soft tee proves sustainability never has to sacrifice style.
Each purchase removes 5 plastic bottles from our oceans..."

"Evergreen Denim Jacket — Timeless style meets zero-waste innovation.
Woven from organic cotton with natural indigo dye, this jacket gets
better with every wear while treading lightly on the planet..."
```

---

## 5. TIDD-EC (Task type, Instructions, Do, Don't, Examples, Context)

Precision-focused framework with explicit positive and negative guidance.

### Components

| Component | Purpose | Key Question |
|-----------|---------|--------------|
| **Task type** | Activity category | "What kind of task is this?" |
| **Instructions** | Steps and guidelines | "What are the exact steps?" |
| **Do** | Required actions and elements | "What MUST be included?" |
| **Don't** | Errors and approaches to avoid | "What must be AVOIDED?" |
| **Examples** | Concrete desired outcomes | "What does good look like?" |
| **Context** | Background and constraints | "What information is relevant?" |

### When to Use
- High-precision tasks requiring clear boundaries
- Customer support, compliance, technical documentation
- When common errors need explicit prevention
- Quality consistency is critical

### When to Avoid
- Open-ended creative exploration
- Simple tasks where dos/don'ts add no value
- Tasks without clear right/wrong approaches

### Clarifying Questions
1. What type of task is this? (support, analysis, documentation, etc.)
2. What are the exact steps or instructions to follow?
3. What MUST be included in the output? (dos)
4. What must be AVOIDED? (don'ts)
5. Can you provide examples of good output?
6. What context or background information is relevant?

### Example

**Before**: "Help with customer complaint response."

**After**:
```
TASK TYPE:
Customer Support Response — Complaint Resolution

INSTRUCTIONS:
1. Acknowledge the customer's frustration
2. Apologize for the inconvenience
3. Explain what happened in simple terms
4. Provide a concrete solution with timeline
5. Offer additional support contact information

DO:
- Use empathetic, professional language
- Personalize the response with customer name
- Provide specific action items with timeframes
- Keep response between 150-250 words

DON'T:
- Make excuses or deflect blame
- Use template language that sounds robotic
- Make promises you can't keep
- Use passive voice ("mistakes were made")
- Include technical jargon or system error codes

EXAMPLES:
Good: "Dear Sarah, I'm truly sorry that your order arrived damaged.
I'm sending a replacement via overnight shipping at no charge — you'll
have it by Friday 2 PM. You'll also receive a full refund within 24 hours."

Bad: "We apologize for any inconvenience. Please contact our support team
for further assistance. Ticket #12345."

CONTEXT:
- E-commerce retailer specializing in home goods
- Customer is a premium member who shops regularly
- Company policy: full refunds + replacement for damaged items
```

---

## 6. RTF (Role, Task, Format)

Simplest framework for well-defined, straightforward tasks.

### Components

| Component | Purpose | Key Question |
|-----------|---------|--------------|
| **Role** | Expertise required | "Who should do this?" |
| **Task** | What needs to be done | "What needs to be done?" |
| **Format** | Output structure | "How should it look?" |

### When to Use
- Simple, well-defined tasks
- Format is the primary concern
- Quick, focused execution needed
- One-off standalone requests

### When to Avoid
- Complex multi-step processes (upgrade to RISEN)
- Rich context needed (upgrade to CO-STAR)
- Audience/tone matters (upgrade to CO-STAR)
- Input transformation needed (upgrade to RISE-IE)

### Clarifying Questions
1. What expertise or perspective is needed?
2. What exactly needs to be done? (be specific)
3. How should the output be formatted? (structure, length, style)

### Example

**Before**: "Write a sorting function."

**After**:
```
ROLE: Python developer who writes clean, efficient code.

TASK: Write a function that sorts a list of dictionaries by a specified key,
with support for ascending/descending order.

FORMAT:
1. Function signature with type hints
2. Docstring with examples
3. Implementation
4. 2-3 usage examples
```

---

## 7. Chain of Thought (CoT)

Step-by-step reasoning technique for complex problem-solving.

### Approaches

| Approach | Method |
|----------|--------|
| **Explicit** | Provide numbered reasoning steps |
| **Zero-shot** | Add "Let's think step by step" |
| **Few-shot** | Show worked examples with reasoning |
| **Structured** | Provide a labeled reasoning template |

### When to Use
- Mathematical problem-solving
- Logical reasoning and analysis
- Debugging and troubleshooting
- Decision-making with trade-offs

### When to Avoid
- Simple lookups or facts
- Straightforward transformations
- Tasks with obvious single steps

### Clarifying Questions
1. What problem needs to be solved?
2. What reasoning steps should be shown?
3. Should intermediate work be displayed?
4. What verification or validation is needed?

### Example

**Before**: "Should we use MongoDB or PostgreSQL?"

**After**:
```
Decide between MongoDB and PostgreSQL by reasoning through:

STEP 1 — USE CASE ANALYSIS:
What data patterns will we have? (structured/unstructured, relationships, queries)

STEP 2 — MONGODB EVALUATION:
Pros and cons specifically for our use case.

STEP 3 — POSTGRESQL EVALUATION:
Pros and cons specifically for our use case.

STEP 4 — CRITICAL REQUIREMENTS:
What are our non-negotiables and why?

STEP 5 — SCORING:
Rate each database against our requirements.

STEP 6 — DECISION:
Choose one with reasoning.

STEP 7 — VALIDATE:
Does this decision make sense? Any red flags?
```

---

## 8. Chain of Density (CoD)

Iterative refinement technique for progressive improvement.

### Approaches

| Approach | Method |
|----------|--------|
| **Multi-pass** | Request N iterations with decreasing word counts |
| **Recursive** | Use output of one pass as input to next |
| **Targeted** | Focus each iteration on a different quality dimension |
| **Constraint-based** | Add tighter constraints per iteration |

### When to Use
- Summarization and content compression
- Iterative improvement of writing
- Optimizing explanations for clarity
- Refining complex outputs

### When to Avoid
- Simple one-shot tasks
- Fixed-format outputs that can't improve
- Time-critical quick tasks

### Clarifying Questions
1. What content needs to be improved/refined?
2. How many iterations of refinement?
3. What should each iteration optimize for? (clarity, brevity, density)
4. What constraints apply? (length limits, information to preserve)

### Example

**Before**: "Summarize this research paper."

**After**:
```
Summarize this research paper using Chain of Density:

ITERATION 1 (200 words):
Comprehensive summary covering all major points. Prioritize completeness.

ITERATION 2 (150 words):
Remove redundancy, combine related points, increase information density.

ITERATION 3 (100 words):
Keep only essential information. Every sentence must count.

ITERATION 4 (75 words):
Distill to core findings. Remove all fluff. Preserve critical details.

For each iteration, highlight what you removed and why.
```

---

## Combining Frameworks

When a single framework doesn't cover all needs, combine components:

| Combination | Use Case |
|-------------|----------|
| CO-STAR + CoT | Complex content requiring reasoning |
| RISEN + CO-STAR | Procedural tasks with audience considerations |
| RISE-IE + CoT | Data analysis requiring step-by-step reasoning |
| TIDD-EC + CoT | High-precision analytical tasks |
| Any framework + CoD | When iterative refinement improves the result |

Use the Hybrid template from [templates.md](templates.md) as a starting point for combinations.
