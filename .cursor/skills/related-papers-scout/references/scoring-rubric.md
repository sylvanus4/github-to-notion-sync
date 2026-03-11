# Phase 3: Scoring Rubric & Selection Rules

## Scoring Rubric

| Criterion | Weight | Scoring |
|-----------|--------|---------|
| **Institution match** | 30% | 1.0 if any author from Google/DeepMind, MIT/CSAIL, Stanford, or NVIDIA; 0.5 if from Meta FAIR, Microsoft Research, CMU, Berkeley, or other top-tier lab; 0.0 otherwise |
| **Citation count** | 20% | Normalize: 100+ citations = 1.0, 50-99 = 0.7, 10-49 = 0.4, <10 = 0.1 (for recent papers <6mo, halve threshold) |
| **GitHub traction** | 20% | 1.0 if repo with 500+ stars; 0.7 if 100-499 stars or listed on Papers With Code; 0.3 if has repo but <100 stars; 0.0 if no repo |
| **Twitter/community buzz** | 15% | 1.0 if multiple Twitter threads or blog posts; 0.5 if at least one mention; 0.0 if none found |
| **Recency** | 15% | 1.0 if published within 6 months; 0.7 if 6-12 months; 0.4 if 12-18 months; 0.1 if older |

Calculate `total_score = sum(weight * score)` for each candidate.

## Selection Rules

1. Sort candidates by `total_score` descending
2. Must have at least 3 of the 4 target institutions (Google, MIT, Stanford,
   NVIDIA) represented in the final selection
3. At least 1 paper must have strong GitHub/Twitter traction (GitHub >= 0.7
   OR Twitter >= 0.5), even if from a non-target institution
4. Prefer subtopic diversity — if 2+ papers address the exact same
   sub-problem, keep only the highest-scored one
5. If fewer than 5 papers meet the strict institution filter, relax to
   include papers scoring >= 0.5 on institution from any top-tier lab
   (Meta FAIR, Microsoft Research, CMU, Berkeley, Allen AI, etc.)

Select the top 5 (or `--top N`) papers after applying these rules.

## Deep Dive Summary Template (Phase 4)

Each subagent produces this structure for its assigned paper:

```markdown
## {rank}. {Paper Title}

- **저자**: {authors} ({institution})
- **발표**: {venue}, {year}
- **arXiv**: https://arxiv.org/abs/{arxiv_id}
- **인용수**: {citation_count} | **GitHub Stars**: {stars or "N/A"} | **관련도 점수**: {total_score}/1.0

### 왜 이 논문을 봐야 하는가

- **입력 논문과의 관계**: {extends/complements/challenges/builds-on — specific connection}
- **핵심 기여**: {specific technical contribution with 1-2 sentence detail}
- **커뮤니티 반응**: {Twitter mentions, GitHub adoption, blog coverage — cite URLs}
- **실용적 가치**: {benchmarks, code availability, reproducibility}
- **기관 신뢰도**: {why this institution's work matters for this topic}

### 핵심 내용 요약

{5-8 sentence summary of the paper's main contributions, methods, and key
results. Include specific numbers from benchmarks if available.}

### 참고 링크

- arXiv: {url}
- GitHub: {repo_url or "N/A"}
- Blog/Explainer: {blog_url or "N/A"}
```
