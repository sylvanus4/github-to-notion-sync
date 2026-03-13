---
description: Analyze and prioritize a batch of feature requests — theme clustering, strategic alignment, priority ranking
argument-hint: "<feature requests as text, file, or paste>"
---

# Feature Request Triage

Transform accumulated feature requests from support tickets, sales calls, surveys, or Slack into a prioritized, actionable backlog.

## Usage
```
/pm-triage-requests [paste a list of requests]
/pm-triage-requests [upload a CSV/spreadsheet]
/pm-triage-requests 기능 요청 목록 분석해줘
```

## Workflow

### Step 1: Receive Feature Requests
Accept any format: pasted text, CSV, Excel, or text files. Parse each request to extract core need, context, and frequency signals.

### Step 2: Collect Prioritization Context
Ask about: product and stage, strategic goals/OKRs, constraints, weighted segments.

### Step 3: Classify and Analyze
Read and apply pm-product-discovery skill, invoking **analyze-feature-requests** sub-skill:
- Theme clustering, request count per theme, strategic alignment, segment analysis, sentiment signals.

### Step 4: Prioritize
Invoke **prioritize-features** sub-skill: Score each theme on Impact, Strategic Alignment, Effort (S/M/L/XL), Risk, and Revenue Signal.

### Step 5: Generate Triage Report
Output prioritized themes as: Immediate (P1), Next Planning (P2), Gather More Signal (P3), Decline/Defer (P4). Save as markdown.

### Step 6: Suggest Next Steps
- "Shall I **write user stories** for the top items?"
- "Shall I **brainstorm solutions** for these themes?"
- "Shall I **design experiments** to validate demand before building?"
