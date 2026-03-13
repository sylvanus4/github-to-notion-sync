---
description: Convert feature-list roadmaps to outcome-driven roadmaps
argument-hint: "<paste current roadmap or feature list>"
---

# PM Transform Roadmap

Transform a feature-centric roadmap into an outcome-driven roadmap that emphasizes user and business outcomes rather than deliverables. Uses pm-execution skill and outcome-roadmap sub-skill.

## Usage
```
/pm-transform-roadmap Convert this feature list to outcome-driven format
/pm-transform-roadmap 현재 로드맵을 아웃컴 기반으로 변환해줘
```

## Workflow

### Step 1: Accept Current Roadmap
- Read the user's current roadmap, feature list, or backlog
- If none provided, ask for the roadmap source (Notion, doc, inline paste)
- Document each existing item as-is before transformation

### Step 2: Gather Strategic Context
- Request or infer: product vision, OKRs, target user segment, success metrics
- Note any constraints (timeline, resources, dependencies)
- Clarify prioritization criteria if ambiguous

### Step 3: Transform Each Item
For each roadmap item:
- **Identify user/business outcome**: What change in user behavior or business result does this enable?
- **Rewrite as outcome statement**: "Users can…" or "Business achieves…"
- **Group by initiative**: Cluster related outcomes into strategic initiatives
- **Add success metrics**: How will we measure success? (usage, conversion, retention, revenue)

### Step 4: Generate Now/Next/Later Format
- Organize transformed items into Now / Next / Later buckets
- Add a "Transformation Notes" section documenting mapping from original features to outcomes
- Highlight any features dropped or merged during transformation

## Notes
- Outcome statements should be observable and measurable, not implementation details
- When grouping, balance initiative size — avoid one giant initiative vs many tiny ones
- Keep the original feature names in transformation notes for traceability
