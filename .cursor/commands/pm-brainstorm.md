---
description: Multi-perspective ideation from PM, Designer, and Engineer viewpoints for existing or new products
argument-hint: "[ideas|experiments] [existing|new] <product or feature>"
---

# Multi-Perspective Brainstorming

Generate creative product ideas or experiment designs from three perspectives (PM, Designer, Engineer). Works for both existing and new products.

## Usage
```
/pm-brainstorm ideas existing Mobile banking app engagement
/pm-brainstorm experiments new Marketplace for freelance designers
/pm-brainstorm 기존 모바일 뱅킹 앱 참여도 아이디어
```

## Workflow

### Step 1: Determine Mode
Parse arguments for two dimensions:
1. **What to generate**: `ideas` (feature concepts) or `experiments` (validation tests)
2. **Product stage**: `existing` (continuous discovery) or `new` (early-stage)

If either is missing, ask the user.

### Step 2: Gather Context
For existing products: current users, opportunity area, constraints, prior attempts.
For new products: concept, target users, current alternatives, riskiest assumptions.

### Step 3: Generate Output
Read and apply the pm-product-discovery skill:
- **For ideas**: invoke brainstorm-ideas-existing or brainstorm-ideas-new. Generate ideas from PM (business value), Designer (UX/delight), Engineer (technical innovation). Rank top 5 with rationale.
- **For experiments**: invoke brainstorm-experiments-existing or brainstorm-experiments-new. Design validation tests with hypotheses, methods, success criteria, and effort estimates.

### Step 4: Suggest Follow-ups
- "Shall I **identify assumptions** behind the top ideas?"
- "Shall I **prioritize** these against the current backlog?"
- "Shall I **design experiments** to validate the top ideas?"
