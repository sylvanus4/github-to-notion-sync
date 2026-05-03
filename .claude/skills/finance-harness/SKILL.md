---
name: finance-harness
description: >-
  Finance domain harness orchestrator — sequential month-end close pipeline
  covering journal entries, reconciliation, close management, financial
  statements, variance analysis, audit support, financial report analysis, and
  SaaS metrics. Use when the user asks to "run finance pipeline", "month-end
  close", "financial harness", "재무 하네스", "월말 결산", "finance-harness", or wants
  end-to-end financial operations. Do NOT use for individual finance
  operations (invoke specific kwp-finance-* skill directly). Do NOT use for
  stock market financial analysis (use trading-us-stock-analysis). Do NOT use
  for SaaS narrative only (use saas-metrics-narrator directly).
---

# Finance Harness Orchestrator

Sequential pipeline for end-to-end financial operations, anchored on the month-end close cycle. Each phase depends strictly on the prior phase's output.

## When to Use

- Month-end or quarter-end close cycle requiring full journal → statements → audit flow
- Financial reporting that chains multiple finance skills in dependency order
- Audit preparation requiring traceable artifacts from every close phase
- Any "run the full finance pipeline" or "월말 결산" request

## Architecture

```
User Request (mode selection)
       │
       ▼
┌──────────────┐
│ Phase 1      │ ← Journal Entry Prep (accruals, prepaid, depreciation)
│ JOURNAL      │   kwp-finance-journal-entry-prep
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 2      │ ← Account Reconciliation (GL vs subledger/bank)
│ RECONCILE    │   kwp-finance-reconciliation
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 3      │ ← Close Management (calendar, dependencies, status)
│ CLOSE        │   kwp-finance-close-management
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 4      │ ← Financial Statements (P&L, B/S, Cash Flow)
│ STATEMENTS   │   kwp-finance-financial-statements
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 5      │ ← Variance Analysis (budget vs actual, waterfall)
│ VARIANCE     │   kwp-finance-variance-analysis
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 6      │ ← Audit Support (SOX 404, sampling, workpapers)
│ AUDIT        │   kwp-finance-audit-support
└──────┬───────┘
       ▼
┌──────────────┐
│ Phase 7      │ ← Optional: PDF report analysis or SaaS metrics
│ ENRICH       │   financial-report-analyzer / saas-metrics-narrator
└──────────────┘
```

## Modes

| Mode | Phases | Use Case |
|------|--------|----------|
| `close` | 1→2→3→4→5 | Standard month-end close |
| `statements` | 4 only | Generate financial statements from existing data |
| `variance` | 5 only | Variance analysis on existing statements |
| `audit` | 6 only | Audit prep and SOX 404 support |
| `saas` | 7 (saas-metrics-narrator) | SaaS metrics narrative from KB data |
| `report` | 7 (financial-report-analyzer) | Analyze an uploaded PDF financial report |
| `full` | 1→2→3→4→5→6→7 | Complete pipeline including enrichment |

Default mode: `close`

## Pipeline

### Phase 1: Journal Entry Prep

Prepare journal entries with proper debits, credits, and supporting documentation.

**Skill**: `kwp-finance-journal-entry-prep`
**Input**: Accounting period, transaction data
**Output**: `outputs/finance-harness/{date}/phase1-journal-entries.md`

Covers: accruals, prepaid amortization, fixed asset depreciation, payroll entries, revenue recognition, manual journal entries.

### Phase 2: Account Reconciliation

Reconcile accounts by comparing GL balances to subledgers, bank statements, or third-party data.

**Skill**: `kwp-finance-reconciliation`
**Input**: Phase 1 output + GL data
**Output**: `outputs/finance-harness/{date}/phase2-reconciliation.md`

Covers: bank reconciliations, GL-to-subledger recs, intercompany reconciliations, reconciling item classification.

### Phase 3: Close Management

Track close calendar, manage task sequencing and dependencies, update status.

**Skill**: `kwp-finance-close-management`
**Input**: Phase 2 output + close calendar
**Output**: `outputs/finance-harness/{date}/phase3-close-status.md`

Covers: close calendar management, progress tracking, blocker identification, activity sequencing by day.

### Phase 3.5: Variance Investigation (Optional)

When reconciliation reveals unexplained variances, close management identifies anomalies, or financial data shows unexpected deviations, invoke `hypothesis-finance` for structured hypothesis-driven variance investigation before generating financial statements. Triggered automatically when:

- Reconciliation items exceed materiality threshold without clear classification
- Month-over-month variances exceed 10% without documented drivers
- Intercompany reconciliation discrepancies persist after standard resolution
- User requests variance investigation or asks "why doesn't this balance"

**Skill**: `hypothesis-finance`
**Input**: Phase 2-3 outputs + variance details
**Output**: `outputs/finance-harness/{date}/phase3.5-variance-investigation.md`
**Skip Flag**: `skip-hypothesis`

### Phase 4: Financial Statements

Generate income statements, balance sheets, and cash flow statements.

**Skill**: `kwp-finance-financial-statements`
**Input**: Phase 3 confirmation + reconciled data
**Output**: `outputs/finance-harness/{date}/phase4-financial-statements.md`

Covers: GAAP-compliant presentation, period-over-period comparison, flux analysis, P&L with variance commentary.

### Phase 5: Variance Analysis

Decompose financial variances into drivers with narrative explanations.

**Skill**: `kwp-finance-variance-analysis`
**Input**: Phase 4 statements
**Output**: `outputs/finance-harness/{date}/phase5-variance-analysis.md`

Covers: budget vs actual, period-over-period changes, revenue/expense variances, waterfall analysis, leadership commentary.

### Phase 6: Audit Support

Support SOX 404 compliance with control testing methodology.

**Skill**: `kwp-finance-audit-support`
**Input**: Phase 1-5 outputs (full audit trail)
**Output**: `outputs/finance-harness/{date}/phase6-audit-package.md`

Covers: testing workpapers, sample selection, control deficiency classification, audit preparation.

### Phase 7: Enrichment (Optional)

Additional analysis from PDF reports or SaaS-specific metrics.

**Skills**: `financial-report-analyzer` or `saas-metrics-narrator`
**Input**: PDF financial reports or KB wiki data
**Output**: `outputs/finance-harness/{date}/phase7-enrichment.md`

## Skill Routing Table

| User Intent | Routed Skill | Phase |
|-------------|-------------|-------|
| "Prepare journal entries" | `kwp-finance-journal-entry-prep` | 1 |
| "Reconcile accounts" | `kwp-finance-reconciliation` | 2 |
| "Track close progress" | `kwp-finance-close-management` | 3 |
| "Generate P&L" | `kwp-finance-financial-statements` | 4 |
| "Explain variance" | `kwp-finance-variance-analysis` | 5 |
| "Prepare for audit" | `kwp-finance-audit-support` | 6 |
| "Analyze this PDF report" | `financial-report-analyzer` | 7 |
| "SaaS metrics narrative" | `saas-metrics-narrator` | 7 |

## Subagent Contracts

Each phase runs as a subagent via the Task tool with file-based data transfer:

```
Task: Phase {N} - {Phase Name}
Input file: outputs/finance-harness/{date}/phase{N-1}-*.md
Output file: outputs/finance-harness/{date}/phase{N}-{name}.md

Instructions:
- Read the input file for prior phase context
- Execute the {skill-name} workflow
- Write results to the output file using absolute paths
- Report: phase status, key findings, any blockers
```

## Error Handling

| Error | Recovery |
|-------|----------|
| Phase N fails | Prior phase outputs at `outputs/finance-harness/{date}/phase{N-1}-*.md` remain valid. Fix the issue and re-run from Phase N. |
| Data inconsistency detected in reconciliation | Flag as YELLOW, continue pipeline, include in audit package as open item |
| Missing input data for a phase | Skip phase with WARNING status, document gap in close status report |

## Output Artifacts

| Phase | Stage Name | Output File | Skip Flag |
|-------|-----------|-------------|-----------|
| 1 | Journal Entry Prep | `outputs/finance-harness/{date}/phase1-journal-entries.md` | `skip-journal` |
| 2 | Reconciliation | `outputs/finance-harness/{date}/phase2-reconciliation.md` | `skip-recon` |
| 3 | Close Management | `outputs/finance-harness/{date}/phase3-close-status.md` | `skip-close` |
| 4 | Financial Statements | `outputs/finance-harness/{date}/phase4-financial-statements.md` | `skip-statements` |
| 5 | Variance Analysis | `outputs/finance-harness/{date}/phase5-variance-analysis.md` | `skip-variance` |
| 6 | Audit Support | `outputs/finance-harness/{date}/phase6-audit-package.md` | `skip-audit` |
| 7 | Enrichment | `outputs/finance-harness/{date}/phase7-enrichment.md` | `skip-enrich` |

## Workspace Convention

- Intermediate files: `_workspace/finance-harness/`
- Final deliverables: `outputs/finance-harness/{date}/`
- Close calendar state: `_workspace/finance-harness/close-calendar.json`

## Constraints

- Strict sequential ordering: each phase depends on the prior phase's output
- Never modify source financial data — work on copies
- All monetary values must include currency denomination
- Audit trail: every phase must reference its input source and timestamp
- Human review gate: final statements and audit package require explicit user confirmation before distribution
