## XLSX

Work with spreadsheets — create, read, edit, format, chart, and clean data in .xlsx, .csv, and .tsv files.

### Usage

```
/xlsx read data.xlsx                   # read and summarize
/xlsx create "monthly budget"          # create from description
/xlsx chart data.xlsx --type bar       # generate chart
/xlsx clean data.csv                   # clean and validate data
```

### Workflow

1. **Read** — Parse spreadsheet structure, formulas, and data types
2. **Process** — Create, edit, format, add formulas, pivot tables, or charts
3. **Validate** — Check data integrity, formula correctness, and formatting
4. **Export** — Save as .xlsx, .csv, or .tsv

### Execution

Read and follow the `anthropic-xlsx` skill (`.cursor/skills/anthropic/anthropic-xlsx/SKILL.md`) for comprehensive spreadsheet operations including formulas, pivot tables, charts, and data cleaning.

### Examples

Create a budget spreadsheet:
```
/xlsx create "monthly cloud infrastructure cost tracker with formulas"
```

Generate a chart:
```
/xlsx chart revenue-data.xlsx --type line --title "MRR Growth"
```
