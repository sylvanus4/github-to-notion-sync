---
description: Prepare a customer interview script or summarize an interview transcript into structured insights
argument-hint: "[prep|summarize] <topic or transcript>"
---

# Customer Interview Prep & Summary

Two modes: **prep** creates a structured interview script before talking to customers, **summarize** extracts insights after the interview.

## Usage
```
/pm-interview prep Onboarding experience for enterprise users
/pm-interview summarize [paste transcript or upload file]
/pm-interview 기업 사용자 온보딩 인터뷰 준비
```

## Workflow

### Prep Mode
1. Understand research goals: what to learn, who to interview, time available, decision impact.
2. Read and apply pm-product-discovery skill, invoking **interview-script** sub-skill.
3. Generate script with: warmup questions, core exploration (JTBD probes), specific topic questions, closing, note-taking template, and warning signals.
4. Follow "The Mom Test" principles — no leading questions, focus on past behavior.

### Summarize Mode
1. Accept transcript in any format (text, file, audio summary).
2. Read and apply pm-product-discovery skill, invoking **summarize-interview** sub-skill.
3. Extract: participant profile, JTBDs, current workflow, pain points, satisfaction signals, key quotes, surprising findings.
4. Generate structured summary with action items.

### Follow-up Suggestions
- Prep: "Shall I **summarize** the interview after you conduct it?"
- Summarize: "Shall I **update assumptions** based on this interview?" / "Shall I **build personas** from multiple interviews?"
