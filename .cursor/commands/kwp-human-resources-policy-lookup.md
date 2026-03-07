## KWP Human Resources: Policy Lookup

Find and explain company policies.

# /policy-lookup


Look up and explain company policies in plain language. See the **employee-handbook** skill for guidance on policy topics, answer structure, and compliance caveats.

## Usage

```
/policy-lookup $ARGUMENTS
```

Search for policies matching: $ARGUMENTS

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    POLICY LOOKUP                                   │
├─────────────────────────────────────────────────────────────────┤
│  STANDALONE (always works)                                       │
│  ✓ Ask any policy question in plain language                    │
│  ✓ Paste your employee handbook and I'll search it              │
│  ✓ Get clear, jargon-free answers                               │
├─────────────────────────────────────────────────────────────────┤
│  SUPERCHARGED (when you connect your tools)                      │
│  + Knowledge base: Search handbook and policy docs automatically │
│  + HRIS: Pull employee-specific details (PTO balance, benefits) │
└─────────────────────────────────────────────────────────────────┘
```

## Output

```markdown
## Policy: [Topic]

### Quick Answer
[1-2 sentence direct answer to their question]

### Details
[Relevant policy details, explained in plain language]

### Exceptions / Special Cases
[Any relevant exceptions or edge cases]

### Who to Contact
[Person or team for questions beyond what's documented]

### Source
[Where this information came from — document name, page, or section]
```

## If Connectors Available

If **Notion** is connected:
- Search employee handbook and policy documents automatically
- Cite the specific document, section, and page number

If **BambooHR** is connected:
- Pull employee-specific details like PTO balance, benefits elections, and enrollment status

## Tips

1. **Ask in plain language** — "Can I work from Europe for a month?" is better than "international remote work policy."
2. **Be specific** — "PTO for part-time employees in California" gets a better answer than "PTO policy."