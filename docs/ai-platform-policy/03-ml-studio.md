# 3. ML Studio

> ML Studio is composed of single training execution **Run** units based on training configurations, so there is **no edit page**.

## 3-1. Text Generation

### 3-1-1. Text Generation Status

| Status | Glance Code | Available Actions |
|--------|-------------|-------------------|
| Running | `Running` | Detail, View Metrics in MLflow, Delete |
| Completed | `Completed` | Detail, View Metrics in MLflow, Delete |
| Failed | `Failed` | Detail, View Metrics in MLflow, Delete |

### 3-1-2. Text Generation Create

| Field Name | Category | Required | Editable | Applied | Description |
|-----------|----------|----------|----------|---------|-------------|
| Experiment Name | 기본정보 | Yes | Yes | Yes | |
| Description | 기본정보 | Yes | Yes | Yes | |
| Model Setting | Model | Yes | Yes | Yes | Same card display as AI Hub Model |
| Training Mode | Model | Yes | Yes | Yes | Options: Full Fine-Tuning, LoRA, QLoRA |
| Method | Model | Yes | Yes | Yes | Options: SFT, DPO, GRPO, CPT, GKD |
| Dataset | Model | Yes | Yes | Yes | Same card display as AI Hub Dataset |
| Select Model (Training Steps Setting) | Model | No | Yes | Yes | Same card display as AI Hub Model, but only models compatible with GKD method |
| Training Mode (Training Steps Setting) | Model | Yes | Yes | Yes | Same card display as AI Hub Dataset |
| Total GPUs | Instance | Yes | Yes | Yes | |

---

## 3-2. Tabular

### 3-2-1. Tabular Status

| Status | Glance Code | Available Actions | Description |
|--------|-------------|-------------------|-------------|
| Running | `Running` | - | |
| Completed | `Completed` | - | |
| Failed | `Failed` | - | System failure |
| Pending | `pending` | - | |
| Cancelled | `Cancelled` | - | Intentionally stopped by user |

### 3-2-2. Tabular Create

| Field Name | Category | Required | Editable | Applied | Description |
|-----------|----------|----------|----------|---------|-------------|
| Select Domain | 기본정보 | Yes | Yes | Yes | Domains: Financial Services, Marketing, E-commerce, Insurance, Telecom/Subscription, Manufacturing, Security/Risk, Healthcare, Real Estate/Energy, General |
| Use Case | 기본정보 | Yes | Yes | Yes | Use cases filtered by selected domain |
| Dataset | Instance | Yes | Yes | Yes | |
| Column Set | Model | Yes | Yes | Yes | Target Variable, Exclude Columns |
| Validation Strategy | Model | Yes | Yes | Yes | See details below |
| Experiment Configuration | Model | Yes | Yes | Yes | See details below |

#### Validation Strategy Details

- **Split Method:** Holdout, Stratified K-Fold, Cross Validation, Time Series
- **Train Data Ratio:** Train / Validation / Test
- **Evaluation Metric:** AUC, F1, Accuracy, Logloss, MCC

> **OPEN QUESTION:** "Train Data Ratio 표현 방식 논의 필요" -- Should this just use a simple percentage split instead of the current format?

#### Experiment Configuration Details

- **Fields:** Name, Optimization Metric, Experiment Description
- **Training Mode:** Basic, Auto ML, FLAML AutoML, AutoGluon
- **Select Training Models** (model-specific)
- **Time Budget**
