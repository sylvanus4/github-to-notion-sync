---
name: role-data-scientist
description: >
  Analyze a given topic from the Data Scientist perspective — data pipeline impact, ML model
  implications, statistical methodology, data quality requirements, and visualization needs.
  Scores topic relevance (1-10) and produces a structured Korean analysis document when relevant (>= 5).
  Composes kwp-data-data-exploration, kwp-data-statistical-analysis, kwp-data-data-visualization,
  kwp-data-data-validation, kwp-data-sql-queries, hf-model-trainer, hf-evaluation, hf-datasets,
  workflow-miner, skill-composer, semantic-guard, and intent-alignment-tracker.
  Use when the role-dispatcher invokes this skill with a topic, or when the user asks for
  "data scientist perspective", "데이터 사이언티스트 관점", "DS 분석", "data impact analysis".
  Do NOT use for running data exploration directly (use kwp-data-data-exploration),
  model training execution (use hf-model-trainer), or dashboard building (use kwp-data-interactive-dashboard-builder).
  Korean triggers: "데이터 사이언티스트 관점", "DS 분석", "데이터 영향 분석".
metadata:
  author: "thaki"
  version: "1.0.1"
  category: "role-analysis"
---

# Data Scientist Perspective Analyzer

Analyzes any business topic from the Data Scientist's viewpoint, covering data pipeline impact,
ML model requirements, statistical methodology, data quality, feature engineering, and
visualization needs.

## Relevance Criteria

Score the topic 1-10 based on overlap with data science concerns:

| Domain | Weight | Keywords |
|--------|--------|----------|
| Data analysis & exploration | High | dataset, EDA, profiling, distribution, outlier, correlation |
| ML model development | High | model, training, fine-tuning, inference, prediction, classification |
| Data pipeline & ETL | High | pipeline, ETL, ingestion, transformation, batch, streaming |
| Statistical methods | High | hypothesis, regression, significance, confidence, A/B test |
| Data visualization | High | chart, dashboard, plot, visualization, Plotly, matplotlib |
| Data quality & validation | High | quality, missing data, drift, validation, schema, anomaly |
| ML evaluation & benchmarking | Medium | accuracy, F1, AUC, benchmark, eval, leaderboard |
| Feature engineering | Medium | feature, embedding, encoding, normalization, selection |
| Research & papers | Medium | paper, arXiv, SOTA, experiment, ablation |
| Product & UX | Low | UI, user flow, design, wireframe |
| HR & organization | Low | hiring, culture, retention |

Score >= 5 → produce full analysis. Score < 5 → return brief relevance note only.

## Analysis Pipeline

When relevant, execute sequentially:

1. **Data Exploration** (via `kwp-data-data-exploration`):
   - Dataset profiling and shape assessment
   - Column distributions, null analysis, outlier detection
   - Data source identification and availability

2. **Statistical Analysis** (via `kwp-data-statistical-analysis`):
   - Applicable statistical methods
   - Hypothesis formulation and testing approach
   - Confidence intervals and significance thresholds

3. **ML Model Assessment** (via `hf-evaluation` + `hf-model-trainer`):
   - Model architecture recommendations
   - Training data requirements and availability
   - Evaluation metrics and benchmark targets
   - Fine-tuning vs training-from-scratch assessment

4. **Data Quality Validation** (via `kwp-data-data-validation`):
   - Methodology soundness check
   - Bias and survivorship bias detection
   - Reproducibility requirements

5. **Visualization Recommendations** (via `kwp-data-data-visualization`):
   - Chart type selection for key insights
   - Dashboard design recommendations
   - Publication-quality figure requirements

6. **SQL & Pipeline Assessment** (via `kwp-data-sql-queries`):
   - Query complexity and performance
   - Data warehouse schema implications
   - ETL pipeline changes needed

7. **Pipeline Pattern Discovery** (via `workflow-miner`):
   - Discover data analysis workflow patterns from interaction history
   - Identify recurring data pipeline sequences
   - Recommend automation opportunities for repetitive analysis tasks

8. **Pipeline Composition** (via `skill-composer`):
   - Recommend skill chain compositions for data pipeline optimization
   - Suggest reusable analysis workflow definitions
   - Map natural language data requirements to executable skill chains

9. **Data Privacy Validation** (via `semantic-guard`):
   - Scan datasets and outputs for PII exposure
   - Validate data flow source-to-destination for sensitive data
   - Check model inputs/outputs for data leakage risks

10. **Analysis Quality Tracking** (via `intent-alignment-tracker`):
    - Measure alignment between analysis goals and delivered insights
    - Track per-skill IA scores for data pipeline steps
    - Identify analysis quality trends and improvement areas

## Output Format

```markdown
# 데이터 사이언티스트 관점 분석: {Topic}

## 관련도: {N}/10
## 분석 일자: {YYYY-MM-DD}

## DS 요약 (3-5 bullets)
- ...

## 데이터 탐색 & 품질
### 필요 데이터셋
### 데이터 품질 평가
### 결측치 & 이상치 전략

## 통계 분석
### 적용 통계 방법론
### 가설 설정
### 유의성 기준

## ML 모델 평가
### 모델 아키텍처 권고
### 학습 데이터 요구사항
### 평가 메트릭 & 벤치마크 목표
### Fine-tuning vs 신규 학습

## 피처 엔지니어링
### 핵심 피처
### 인코딩/정규화 전략
### 피처 선택 기준

## 데이터 파이프라인
### ETL 변경 필요사항
### 스키마 영향
### 배치 vs 스트리밍

## 시각화 권고
### 차트 유형 선택
### 대시보드 설계
### 주요 인사이트 시각화

## 워크플로우 패턴 분석
### 발견된 분석 패턴
### 파이프라인 자동화 기회
### 스킬 체인 구성 권고

## 데이터 보안 & 프라이버시
### PII 노출 리스크
### 데이터 흐름 검증
### 모델 데이터 누출 점검

## 의도 정렬 평가
### IA 점수 (0-100)
### 분석 품질 추적
### 개선 필요 영역

## DS 권고
### 즉시 분석 작업
### 모델 개발 로드맵
### 데이터 인프라 개선
### 실험 설계 제안
```

## Agent Response Contract (Binary Eval Gate)

When relevance score is **≥ 5**, every end-user analysis MUST satisfy:

1. **EVAL 1 — Relevance first:** Before any other analysis sections, output `## 관련도 선행 평가` containing `**점수:** N/10` and `**선행 근거:**` (2–4 Korean sentences explicitly mapping the topic to the **Relevance Criteria** table). If N < 5, output only a short Korean relevance note—do not fill the full template.

2. **EVAL 2 — Composed sub-skills (≥3):** Include `## 위임된 서브스킬` as a markdown table with **at least three rows** chosen from this skill's **Analysis Pipeline** only. Columns: 서브스킬 (backtick name, e.g. `kwp-data-data-exploration`), 위임 범위 (Korean), 기대 산출물 (Korean).

3. **EVAL 3 — Korean narrative structure:** After the sections above, all substantive analysis MUST be **Korean** (proper nouns and skill identifiers may appear in English inside backticks). Use H2/H3 headings, bullet lists, and **at least one** additional markdown table in the body (excluding the delegation table).

4. **EVAL 4 — Actionable recommendations:** End with `## 실행 액션 플랜` containing **at least three** numbered items (`1.`, `2.`, `3.`). Each item MUST explicitly include **담당:** (role or team) and **기한:** (concrete horizon, e.g. 2주 내, 30일 내, 분기 내).

## Error Handling

- If a composed skill is unavailable, skip that pipeline step and note the gap in the output
- If the topic is ambiguous, request clarification before scoring relevance
- If relevance score is borderline (4-5), include the score rationale in the output
- Always produce output in Korean regardless of the input language

## Example

**Input**: "New GPU inference service launch for enterprise customers"

**Relevance Score**: 8/10 (model inference + data pipeline + evaluation metrics + monitoring)

**Analysis highlights**:
- Data: Inference request/response logging schema needed, expected 10K requests/day
- ML: Model serving optimization (quantization, batching), latency-accuracy tradeoff
- Pipeline: Real-time inference pipeline with batch fallback, model versioning
- Quality: A/B testing framework for model versions, drift detection on inference inputs
- Visualization: Inference latency dashboard, model accuracy tracking over time
- Workflow: Discovered pattern "model-train → evaluate → deploy → monitor" (frequency: 8)
- Privacy: Enterprise inference inputs may contain PII — semantic-guard scan required
- Recommendation: Start with offline evaluation pipeline, add real-time monitoring in sprint 2
