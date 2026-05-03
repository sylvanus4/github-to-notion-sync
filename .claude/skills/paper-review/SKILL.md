---
name: paper-review
description: End-to-end academic paper review — deep analysis, venue-quality peer review, dual-audience NLM slides, DOCX report, and Slack distribution.
disable-model-invocation: true
arguments: [paper_source]
---

Review academic paper from `$paper_source` (arXiv URL, PDF path, or markdown).

## Pipeline

1. **Paper Ingestion**: Download/read paper, extract to structured markdown
2. **Deep Analysis**: Section-by-section Korean analysis (3000-5000 words)
   - Core contribution, methodology, experimental design
   - Strengths, weaknesses, reproducibility assessment
3. **Peer Review**: Venue-quality review with severity grading
   - FATAL / MAJOR / MINOR classifications
   - Inline annotations with specific citations
   - Concrete revision suggestions
4. **NLM Slides**: Dual-audience decks (elementary + expert, Korean)
5. **DOCX Report**: Detailed analysis uploaded to Google Drive
6. **Distribution**: Slack thread to #deep-research-trending

## Output Format

```markdown
## 논문 분석: [Title]

### 핵심 기여
### 방법론 평가
### 실험 설계 및 결과
### 강점
### 약점 (심각도별)
### 재현 가능성
### 실용적 시사점
### 총평 및 점수
```

## Rules

- Skip papers older than 9 months for NLM uploads
- Always include reproducibility assessment
- Korean output for analysis, English preserved for technical terms
