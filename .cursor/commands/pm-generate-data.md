---
description: Generate realistic dummy datasets for testing — CSV, JSON, SQL, or Python script
argument-hint: "[csv|json|sql|python] <schema or column list>"
---

# PM Generate Data

Generate realistic dummy datasets for testing. Support CSV, JSON, SQL insert statements, or a Python script. Custom columns, constraints, and distributions (e.g., skewed, random). Uses pm-execution skill, dummy-dataset sub-skill.

## Usage
```
/pm-generate-data csv 100 rows: id, email, name, created_at
/pm-generate-data CSV 100행 생성 id, email, name
/pm-generate-data json Users with nested addresses, 50 records
/pm-generate-data 더미 데이터 JSON 50개
/pm-generate-data sql orders table, 200 rows, date range 2024-01 to 2024-06
/pm-generate-data SQL insert문 200행 생성
```

## Workflow

### Step 1: Choose Output Format
- **csv**: Comma-separated, header row, UTF-8
- **json**: Array of objects or NDJSON
- **sql**: INSERT statements for given schema
- **python**: Script (e.g., Faker) to reproduce dataset
- Default to csv if omitted

### Step 2: Parse Schema
- Accept column names and optional types (string, int, float, date, email, uuid, etc.)
- Support constraints: unique, not-null, range, enum
- Nested structures for JSON (e.g., address: {street, city, zip})

### Step 3: Apply Distributions
- Random: uniform where appropriate
- Skewed: 80/20, geographic clustering, time-of-day patterns
- Correlated: e.g., order amount vs customer segment
- Realistic formats: valid emails, plausible names, consistent dates

### Step 4: Generate and Export
- Output to file or inline
- For SQL: include CREATE TABLE if schema unknown; batch inserts (e.g., 100 per statement)
- For Python: self-contained script with dependency note (e.g., Faker)

## Notes
- No PII in dummy data — use obviously fake values (e.g., test@example.com)
- For SQL, specify table name and DB dialect (Postgres, MySQL) if known
- Python script: add seed for reproducibility
