# Goose Launch Positioning Builder

Craft launch positioning for a new product or feature using the April Dunford "Obviously Awesome" framework. Identifies competitive alternatives, unique attributes, value these enable, and the best-fit customer — then synthesizes into a positioning statement, headline options, and elevator pitch variants.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/launch-positioning-builder.

## When to Use

- "Help me position our product for launch"
- "Build positioning using the April Dunford framework"
- "출시 포지셔닝 작성", "April Dunford 프레임워크"
- "What's our product's competitive positioning?"

## Do NOT Use

- For full product strategy and Lean Canvas (use pm-product-strategy)
- For brand voice and messaging guidelines (use kwp-marketing-brand-voice)
- For GTM launch checklist (use goose-feature-launch-playbook)

## Methodology

### Step 1: Competitive Alternatives
What would customers do if your product didn't exist?
- Direct competitors
- Adjacent tools they'd cobble together
- Hiring someone to do it
- Doing nothing / status quo

### Step 2: Unique Attributes
What do you have that alternatives don't?
- Features, architecture, approach, pricing model
- Technical differentiators
- Business model differentiators
- Team/expertise differentiators

### Step 3: Value These Enable
Translate each attribute into customer value:
- Attribute → "Which means that..." → customer outcome
- Quantify where possible (saves X hours, reduces Y by Z%)

### Step 4: Best-Fit Customer
Who cares the most about the value you deliver?
- Characteristics that make them a perfect fit
- Context/situation that makes them ready to buy
- Anti-personas: who this is NOT for

### Step 5: Market Category
What frame of reference helps customers understand what you are?
- Existing category (best if customers already search for it)
- New subcategory (when existing categories are too broad)
- New category (high risk, high reward — only if truly novel)

## Output

```markdown
# Positioning: [Product Name]

## Competitive Alternatives
[List with brief description of each]

## Unique Attributes
[Your differentiators vs each alternative]

## Value Map
| Attribute | Enables | Customer Outcome |
|-----------|---------|-----------------|

## Best-Fit Customer
[Profile with characteristics and buying context]

## Market Category
[Category choice with rationale]

## Positioning Statement
For [target customer] who [situation/need], [product] is a [market category] that [key benefit]. Unlike [alternative], we [key differentiator].

## Headline Options
1. [Benefit-led]
2. [Outcome-led]
3. [Contrast-led]

## Elevator Pitch (30-second)
[Conversational version of positioning]
```
