# HF Datasets Python API and Workflow Examples

## Python API Usage (sql_manager)

```python
from sql_manager import HFDatasetSQL

sql = HFDatasetSQL()

# Query
results = sql.query("cais/mmlu", "SELECT * FROM data WHERE subject='nutrition' LIMIT 10")

# Get schema
schema = sql.describe("cais/mmlu")

# Sample
samples = sql.sample("cais/mmlu", n=5, seed=42)

# Count
count = sql.count("cais/mmlu", where="subject='nutrition'")

# Histogram
dist = sql.histogram("cais/mmlu", "subject")

# Filter and transform
results = sql.filter_and_transform(
    "cais/mmlu",
    select="subject, COUNT(*) as cnt",
    group_by="subject",
    order_by="cnt DESC",
    limit=10
)

# Push to Hub
url = sql.push_to_hub(
    "cais/mmlu",
    "username/nutrition-subset",
    sql="SELECT * FROM data WHERE subject='nutrition'",
    private=True
)

# Export locally
sql.export_to_parquet("cais/mmlu", "output.parquet", sql="SELECT * FROM data LIMIT 100")

sql.close()
```

## Combined Workflow Examples

**Example 1: Create Training Subset**
```bash
uv run scripts/sql_manager.py describe --dataset "cais/mmlu"
uv run scripts/sql_manager.py query --dataset "cais/mmlu" \
  --sql "SELECT * FROM data WHERE subject IN ('nutrition', 'anatomy', 'clinical_knowledge')" \
  --push-to "username/mmlu-medical-subset" --private
```

**Example 2: Transform and Reshape**
```bash
uv run scripts/sql_manager.py query --dataset "cais/mmlu" \
  --sql "SELECT question, choices[answer] as correct_answer, subject FROM data" \
  --push-to "username/mmlu-qa-format"
```

**Example 3: Quality Filtering**
```bash
uv run scripts/sql_manager.py query --dataset "squad" \
  --sql "SELECT * FROM data WHERE LENGTH(context) > 500 AND LENGTH(question) > 20" \
  --push-to "username/squad-filtered"
```

**Example 4: Create Custom Training Dataset**
```bash
uv run scripts/sql_manager.py export --dataset "cais/mmlu" \
  --sql "SELECT question, subject FROM data WHERE subject='nutrition'" \
  --output "nutrition_source.jsonl" --format jsonl
# Process with your pipeline, then:
uv run scripts/dataset_manager.py init --repo_id "username/nutrition-training"
uv run scripts/dataset_manager.py add_rows --repo_id "username/nutrition-training" \
  --template qa --rows_json "$(cat processed_data.json)"
```
