# NVIDIA Data Designer

Build high-quality synthetic datasets using NVIDIA's Data Designer orchestration framework. Supports generation from scratch or from seed data, with LLM-powered text/code/structured/judge columns, statistical samplers, validators, and custom generators. Orchestrates workflows through a CLI that provides curated API context to minimize token usage and errors.

Use when the user asks to "generate synthetic data", "create a dataset with LLM", "build a data generation pipeline", "synthetic QA pairs", "generate training data", "data-designer", "create fake data", "build synthetic dataset", or wants to design and produce structured datasets using LLM inference and statistical sampling.

Do NOT use for daily stock data sync (use `weekly-stock-update`). Do NOT use for HuggingFace dataset CRUD without generation (use `hf-datasets`). Do NOT use for general CSV/Excel operations (use `anthropic-xlsx`). Do NOT use for model training (use `hf-model-trainer`). Do NOT use for web scraping to collect data (use `scrapling`).

Korean triggers: "합성 데이터 생성", "데이터셋 빌드", "시뮬레이션 데이터", "데이터 파이프라인", "데이터 디자이너", "합성 데이터", "학습 데이터 생성", "가짜 데이터 생성", "LLM 데이터 생성".

## Setup

### 1. Install Data Designer

```bash
pip install data-designer
```

Or in a virtual environment:

```bash
python -m venv .venv && source .venv/bin/activate && pip install data-designer
```

### 2. Configure API Keys

Set at least one LLM provider's API key:

```bash
export NVIDIA_API_KEY="nvapi-..."      # NVIDIA NIM endpoints
export OPENAI_API_KEY="sk-..."         # OpenAI endpoints
export OPENROUTER_API_KEY="sk-or-..."  # OpenRouter endpoints
```

### 3. Verify Installation

```bash
data-designer config list
```

### 4. Telemetry (Optional)

Disable usage telemetry:

```bash
export NEMO_TELEMETRY_ENABLED=false
```

## Before You Start

Do not explore the workspace or source code first. The workflow's Learn step gives you everything you need via a single CLI command.

Locate the `data-designer` CLI:

```bash
command -v data-designer 2>/dev/null || (test -x .venv/bin/data-designer && realpath .venv/bin/data-designer)
```

Use this resolved path for all `data-designer` commands throughout the skill. If blank, see Troubleshooting.

## Goal

Build a synthetic dataset using the Data Designer library that matches the user's description.

## Workflow

Use **Autopilot** mode if the user implies they don't want to answer questions — e.g., "be opinionated", "you decide", "make reasonable assumptions", "just build it", "surprise me". Otherwise, use **Interactive** mode (default).

Read **only** the workflow file that matches the selected mode, then follow it:

- **Interactive** → read `workflows/interactive.md`
- **Autopilot** → read `workflows/autopilot.md`

## Rules

- Keep all columns in the output by default. Drop a column only if: (1) the user explicitly asks, or (2) it is a helper column that exists solely to derive other columns (e.g., a sampled person object used to extract name, city, etc.). When in doubt, keep the column.
- Do not suggest or ask about seed datasets. Only use one when the user explicitly provides seed data or asks to build from existing records. When using a seed, read `references/seed-datasets.md`.
- When the dataset requires person data (names, demographics, addresses), read `references/person-sampling.md`.
- If a dataset script matching the description already exists, ask the user whether to edit it or create a new one.

## Gotchas

- `SamplerColumnConfig` param is `params=`, not `sampler_params=` → `TypeError` at build time
- Sampler/validation columns need both a type AND params: `sampler_type="category"` + `params=dd.CategorySamplerParams(...)`
- `LLMJudgeColumnConfig` scores are nested dicts (`{reasoning, score}`). Use `{{ quality.correctness.score }}` for the numeric value — `{{ quality.correctness }}` returns the full dict
- Jinja2 templates in `prompt`/`system_prompt`/`expr`: reference columns with `{{ col }}`, nested with `{{ col.field }}`
- `data-designer validate` must pass before `preview` — skipping it produces cryptic runtime errors

## Cross-Skill Composition

After generating a dataset, compose with these project skills:

- **`hf-datasets`** — Upload the generated dataset to HuggingFace Hub
- **`hf-model-trainer`** — Use the generated data for fine-tuning via TRL
- **`cognee`** — Ingest generated datasets into the knowledge graph
- **`anthropic-xlsx`** — Export generated data to spreadsheets

## Troubleshooting

- **`data-designer` command not found:** If no virtual environment exists, create one first (`python -m venv .venv && source .venv/bin/activate`), then install (`pip install data-designer`). If a virtual environment already exists, activate it and verify the package is installed.
- **API key errors:** Run `data-designer config list` to verify which providers are configured. At least one of `NVIDIA_API_KEY`, `OPENAI_API_KEY`, or `OPENROUTER_API_KEY` must be set.
- **Network errors during preview:** A sandbox environment may be blocking outbound requests. Ask the user for permission to retry the command with the sandbox disabled. Only as a last resort, if retrying outside the sandbox also fails, tell the user to run the command themselves.

## Output Template

Write a Python file to the current directory with a `load_config_builder()` function returning a `DataDesignerConfigBuilder`. Name the file descriptively (e.g., `customer_reviews.py`). Use PEP 723 inline metadata for dependencies.

```python
# /// script
# dependencies = [
#   "data-designer", # always required
#   "pydantic", # only if this script imports from pydantic
#   # add additional dependencies here
# ]
# ///
import data_designer.config as dd
from pydantic import BaseModel, Field


class MyStructuredOutput(BaseModel):
    field_one: str = Field(description="...")
    field_two: int = Field(description="...")


@dd.custom_column_generator(
    required_columns=["col_a"],
    side_effect_columns=["extra_col"],
)
def generator_function(row: dict) -> dict:
    row["name_in_custom_column_config"] = "custom value"
    row["extra_col"] = "extra value"
    return row


def load_config_builder() -> dd.DataDesignerConfigBuilder:
    config_builder = dd.DataDesignerConfigBuilder()

    # Seed dataset (only if the user explicitly mentions a seed dataset path)
    # config_builder.with_seed_dataset(dd.LocalFileSeedSource(path="path/to/seed.parquet"))

    # config_builder.add_column(...)
    # config_builder.add_processor(...)

    return config_builder
```

Only include Pydantic models, custom generators, seed datasets, and extra dependencies when the task requires them.
