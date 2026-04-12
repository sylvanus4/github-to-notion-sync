---
name: structured-extractor
version: 1.0.0
description: >
  Extract structured JSON data from documents (PDF, web pages, images) using a
  user-provided or LLM-inferred JSON Schema. Validates output, scores field
  confidence, and supports batch processing with cross-document entity resolution.
tags: [extraction, schema, JSON, document, OCR, structured-data, validation]
triggers:
  - "extract structured data"
  - "document to JSON"
  - "schema extraction"
  - "parse document"
  - "extract fields from PDF"
  - "structured extraction"
  - "data extraction"
  - "invoice extraction"
  - "resume parsing"
  - "form extraction"
  - "table extraction"
  - "entity extraction"
  - "structured-extractor"
  - "구조화 데이터 추출"
  - "문서에서 JSON"
  - "스키마 추출"
  - "PDF 데이터 추출"
  - "테이블 추출"
  - "양식 추출"
  - "엔티티 추출"
  - "구조화 추출"
do_not_use:
  - "For clean markdown extraction without schema (use defuddle)"
  - "For PDF to markdown conversion without structured output (use opendataloader)"
  - "For web scraping with CSS selectors (use scrapling)"
  - "For multi-strategy portal scanning without schema (use portal-scanner)"
  - "For financial data queries from APIs (use kwp-data-sql-queries)"
  - "For general data exploration (use kwp-data-data-exploration)"
composes:
  - defuddle
  - opendataloader
  - batch-agent-runner
---

# Structured Extractor

Schema-driven document-to-JSON extraction with validation and confidence scoring.

## When to Use

- Given a document and a target schema, extract structured data
- Process a batch of invoices, resumes, receipts, or forms into a database-ready format
- Normalize unstructured text into typed records with confidence metrics
- Cross-document entity resolution (dedup names, orgs, addresses)

## Pipeline

```
Schema → Ingest → Extract → Validate → Output
```

### Phase 1: Schema Definition

The schema defines the extraction target. Accept via three modes:

**Mode A — User provides JSON Schema**:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "company_name": { "type": "string" },
    "invoice_number": { "type": "string" },
    "line_items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "description": { "type": "string" },
          "quantity": { "type": "number" },
          "unit_price": { "type": "number" }
        }
      }
    },
    "total": { "type": "number" }
  },
  "required": ["company_name", "invoice_number", "total"]
}
```

**Mode B — Infer from examples**:
User provides 2-3 example documents + expected output pairs. The agent infers a JSON Schema from the examples, presents it for confirmation, then proceeds.

**Mode C — Infer from description**:
User describes what to extract in natural language ("Extract company name, date, all line items with descriptions and amounts"). Agent generates a schema, confirms, then proceeds.

### Phase 2: Document Ingestion

Route each source to the appropriate extractor based on type detection.

| File Type | Extractor | Output |
|---|---|---|
| PDF | `opendataloader` | Layout-preserving markdown with tables |
| Web URL | `defuddle` | Clean markdown with YAML frontmatter |
| Image (PNG/JPG) | Vision model | Structured description; OCR for text-heavy images |
| CSV/TSV | Direct parse | Tabular data (each row = one record) |
| DOCX/TXT | Direct read | Raw text content |
| JSON | Direct parse | Nested data traversal |

For images with dense text (scanned documents, receipts), prefer vision model for layout understanding. Fall back to Tesseract OCR only if vision model cannot resolve text.

### Phase 3: Extraction

LLM extracts fields per schema from the ingested content.

**Extraction prompt structure**:
1. Present the JSON Schema with field descriptions
2. Present the document content (markdown from Phase 2)
3. Request extraction with confidence scoring

**Per-field confidence scoring** (0.0 to 1.0):
- **1.0**: Value explicitly stated in document, exact match
- **0.8-0.9**: Value clearly present but required minor interpretation (date format conversion, unit normalization)
- **0.5-0.7**: Value inferred from context (not explicitly stated but logically derivable)
- **0.1-0.4**: Value is a guess based on partial or ambiguous information
- **0.0**: Value could not be determined, `null` returned

**Output format per record**:
```json
{
  "data": {
    "company_name": "Acme Corp",
    "invoice_number": "INV-2024-001",
    "total": 1500.00
  },
  "confidence": {
    "company_name": 1.0,
    "invoice_number": 0.95,
    "total": 1.0
  },
  "source_references": {
    "company_name": "Header, line 1",
    "invoice_number": "Top-right corner, below logo",
    "total": "Bottom of line items table"
  }
}
```

**Multi-record extraction**: When a single document contains multiple records (e.g., a CSV with 100 rows, a PDF with multiple invoices), extract all records into an array.

### Phase 4: Validation

Validate extracted data against the schema and flag issues.

**Validation layers**:
1. **Schema validation**: Type checks, required field presence, enum value validity
2. **Confidence gate**: Fields below `--confidence-threshold` (default 0.6) flagged for human review
3. **Cross-field consistency**: Check logical relationships (e.g., line_items sum ≈ total)
4. **Cross-document entity resolution** (batch mode only):
   - Normalize company names ("Acme Corp" = "ACME Corporation" = "Acme")
   - Normalize addresses (abbreviation expansion, format standardization)
   - Assign canonical entity IDs for deduplication

**Validation report**:
```json
{
  "total_records": 50,
  "valid": 42,
  "needs_review": 6,
  "failed": 2,
  "review_items": [
    {
      "record_id": "rec_007",
      "field": "invoice_number",
      "confidence": 0.4,
      "reason": "Partially obscured in scan",
      "extracted_value": "INV-2024-0??",
      "source_reference": "Top-right, page 1"
    }
  ]
}
```

### Phase 5: Output

**File outputs** (all under `outputs/extraction/{date}/` or user-specified path):
- `extracted.json` — Array of extracted records with confidence scores
- `validation-report.json` — Validation summary with flagged items
- `schema-used.json` — The JSON Schema used (whether provided or inferred)
- `extracted.csv` — Flattened CSV (for tabular schemas only)

**Batch mode** (via `batch-agent-runner`):
For document sets of 10+, use `batch-agent-runner` TSV state tracking:
1. Write file list to `batch-state.tsv` with columns: `file_path | status | record_count | errors`
2. Process in parallel subagent batches (4 concurrent)
3. Merge results into a single `extracted.json` after all batches complete
4. Run entity resolution across merged dataset

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `--source` | required | File path, URL, or glob pattern for input documents |
| `--schema` | infer | Path to JSON Schema file, or "infer" to auto-detect |
| `--examples` | none | Path to example input/output pairs for schema inference |
| `--confidence-threshold` | 0.6 | Minimum confidence for auto-accept (below = flagged for review) |
| `--entity-resolution` | false | Enable cross-document entity normalization |
| `--output-format` | json | Output format: json, csv, or both |
| `--output-dir` | auto | Output directory (default: `outputs/extraction/{date}/`) |
| `--batch-size` | 4 | Concurrent documents in batch mode |

## Constraints

- Never fabricate data — if a field cannot be extracted, return `null` with confidence 0.0
- Preserve original values — do not "correct" data unless schema specifies a normalization rule
- Source references are mandatory for every extracted field
- PII handling: if schema contains PII fields (email, phone, SSN), log a warning and require explicit `--allow-pii` flag
- Image extraction: always present the image to the vision model first; fall back to OCR only if vision fails
- Large PDFs (>50 pages): split into sections, extract per-section, merge with page references
