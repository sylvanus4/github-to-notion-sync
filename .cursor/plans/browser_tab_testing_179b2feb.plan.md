---
name: Browser Tab Testing
overview: Define 5 key browser test scenarios for each of the 15 main pages/tabs, execute them via browser automation, document all failures or unexpected behaviors, and fix every issue found.
todos:
  - id: test-group-a
    content: "Browser test: Dashboard, Technical Analysis, Events, Stocks (20 scenarios)"
    status: in_progress
  - id: test-group-b
    content: "Browser test: Stock Prices, Stock Price Detail, Analysis, Reports (20 scenarios)"
    status: pending
  - id: test-group-c
    content: "Browser test: Turtle, DualMA, Strategy Comparison, GenAI Features (20 scenarios)"
    status: pending
  - id: test-group-d
    content: "Browser test: LLM Agents, Settings, NotFound (15 scenarios)"
    status: pending
  - id: consolidate-issues
    content: Consolidate all failures into a categorized issue list
    status: pending
  - id: fix-issues
    content: Fix all identified issues by severity (critical > major > minor)
    status: pending
  - id: verify-fixes
    content: Re-test all fixed scenarios to confirm resolution
    status: pending
  - id: update-todo
    content: Update tasks/todo.md with completed work
    status: pending
isProject: false
---

# Browser-Based Functional Testing & Bug Fixing Plan

## Environment

- **Frontend**: [http://localhost:4501](http://localhost:4501) (Vite dev server, running)
- **Backend**: [http://localhost:4567](http://localhost:4567) (FastAPI + uvicorn, running)

---

## Test Scenarios by Tab (5 per tab)

### 1. Dashboard (`/`)

1. **Page load & data rendering** -- Verify summary cards (analyzed events, analysis results, avg CAR, top mover) render with data or graceful empty states
2. **Market toggle** -- Switch between domestic/international and confirm data updates accordingly
3. **Refresh button** -- Click refresh and verify data re-fetches (loading spinner appears, data updates)
4. **Top impact events list** -- Confirm list renders, items are clickable and navigate to event detail
5. **Top movers section** -- Verify ticker-based top movers render with correct price/change values

### 2. Technical Analysis (`/technical-analysis`)

1. **Symbol selector** -- Open symbol dropdown, select a ticker, verify analysis data loads
2. **Timeframe tabs** -- Switch between Daily/Weekly/Monthly tabs, confirm data updates per timeframe
3. **Summary gauges** -- Verify overall/MA/oscillator gauges render with correct labels and values
4. **Moving averages table** -- Confirm MA table renders with all expected columns (name, value, action)
5. **Pivot points table** -- Verify pivot points data renders in a structured table

### 3. Events (`/events`)

1. **Page load & list rendering** -- Verify event list loads with pagination controls
2. **Search filter** -- Type in search box and verify list filters in real-time
3. **Organization/Type filters** -- Apply org and type dropdown filters, confirm filtered results
4. **Create event dialog** -- Open create dialog, verify form fields render, test form validation
5. **List/Grid view toggle** -- Switch between list and grid views, verify layout changes

### 4. Stocks (`/stocks`)

1. **Stock cards rendering** -- Verify all stock cards load with ticker, price, change, and record count
2. **Category filter** -- Select different categories and verify cards filter correctly
3. **Refresh All button** -- Click refresh and verify data reload with loading indicators
4. **Fetch Latest (Yahoo Finance)** -- Trigger fetch latest, verify progress indicator and completion
5. **Navigate to stock detail** -- Click a stock card and verify navigation to `/stock-prices/:symbol`

### 5. Stock Prices (`/stock-prices`)

1. **Overview tab rendering** -- Verify ticker grid loads with category filter and search
2. **Search functionality** -- Type ticker name in search box, verify filtered results
3. **Compare tab** -- Switch to Compare tab, select tickers, verify comparison chart renders
4. **Date range picker** -- Select a date range in Compare mode, verify chart updates
5. **CSV upload modal** -- Open CSV upload modal, verify file input and validation UI

### 6. Stock Price Detail (`/stock-prices/:symbol`)

1. **Chart rendering** -- Navigate to a ticker detail, verify default line chart renders
2. **Chart type switch** -- Toggle between line/candlestick/RSI/volume charts
3. **Date range selection** -- Change date range and verify chart data updates
4. **Price data table** -- Scroll down and verify price data table renders with pagination
5. **Export functionality** -- Click export button and verify download triggers

### 7. Analysis (`/analysis`)

1. **Form rendering** -- Verify analysis form fields (event window, benchmark, tickers, methods) render
2. **Form validation** -- Submit with empty required fields, verify validation error messages
3. **Run analysis** -- Fill form and submit, verify status/progress indicators appear
4. **Analysis history** -- Verify past analysis runs list renders below the form
5. **Navigate to result** -- Click a completed analysis run, verify navigation to `/analysis/:id`

### 8. Reports (`/reports`)

1. **Tab navigation** -- Verify all tabs (Summary, By Org, By Ticker, By Event Type, Charts, All Results) are clickable
2. **Summary tab data** -- Verify summary cards render with aggregate statistics
3. **By Ticker aggregation** -- Switch to By Ticker tab, verify per-ticker breakdown renders
4. **Charts tab** -- Switch to Charts tab, verify chart images or visualizations load
5. **Paginated results** -- Switch to All Results tab, verify pagination controls work

### 9. Turtle Trading (`/turtle`)

1. **Dashboard load** -- Verify instruments table loads with MA and Donchian data
2. **Strategy mode switch** -- Toggle between pure_turtle and modern_cta modes
3. **Sync instruments** -- Click sync button, verify progress and data refresh
4. **Compute indicators** -- Click compute indicators, verify calculation completes
5. **Navigate to backtest** -- Click backtest link, verify `/turtle/backtest` page loads with form

### 10. DualMA (`/dualma`)

1. **Dashboard load** -- Verify DualMA dashboard renders with strategy overview
2. **Backtest navigation** -- Navigate to `/dualma/backtest`, verify form renders
3. **Backtest form** -- Fill backtest parameters and submit, verify results display
4. **Results metrics** -- Verify key metrics (returns, drawdown, Sharpe) display correctly
5. **Chart rendering** -- Verify backtest equity curve or signal chart renders

### 11. Strategy Comparison (`/strategy-comparison`)

1. **Page load** -- Verify strategy comparison page renders with all strategy options
2. **Strategy selection** -- Select strategies to compare, verify comparison data loads
3. **Bollinger Bands backtest** -- Trigger Bollinger Bands backtest, verify results
4. **Comparison chart** -- Verify side-by-side or overlay comparison chart renders
5. **Metrics table** -- Verify strategy metrics comparison table renders

### 12. GenAI Features (`/genai-features`)

1. **Tab navigation** -- Verify all tabs (Dashboard, Features, Prediction, Portfolio) render
2. **Feature Explorer** -- Open Features tab, verify feature list loads
3. **Generate features** -- Trigger feature generation, verify progress/status
4. **Prediction view** -- Switch to Prediction tab, verify prediction UI renders
5. **Portfolio view** -- Switch to Portfolio tab, verify portfolio display

### 13. LLM Agents (`/llm-agents`)

1. **Dashboard load** -- Verify recent runs table and macro indicators panel load
2. **Quick Run** -- Trigger a quick run, verify run starts and appears in table
3. **Macro refresh** -- Click refresh macro, verify macro data updates
4. **Run detail navigation** -- Click a run row, verify navigation to `/llm-agents/runs/:runId`
5. **Backtest page** -- Navigate to `/llm-agents/backtest`, verify config form renders

### 14. Settings (`/settings`)

1. **Theme toggle** -- Switch between light/dark themes, verify UI updates
2. **Language switch** -- Change language (en/ko), verify all labels translate
3. **Database connection test** -- Click test connection, verify success/failure feedback
4. **Clear cache** -- Click clear cache, verify confirmation and completion toast
5. **Analysis defaults** -- Modify analysis default settings, verify they persist after page reload

### 15. NotFound (`/`*)

1. **404 rendering** -- Navigate to `/nonexistent-route`, verify 404 page renders
2. **Home button** -- Click "Go Home" button, verify navigation to `/`
3. **Go Back button** -- Click "Go Back" button, verify browser history navigation
4. **Layout consistency** -- Verify header/navigation still renders on 404 page
5. **Deep invalid paths** -- Navigate to `/stocks/invalid/deep/path`, verify 404 page

---

## Execution Strategy

### Phase 1: Browser Testing (Parallel by Groups)

Launch 4 parallel browser-use subagents, each covering ~4 tabs:

- **Agent A**: Dashboard, Technical Analysis, Events, Stocks
- **Agent B**: Stock Prices, Stock Price Detail, Analysis, Reports
- **Agent C**: Turtle, DualMA, Strategy Comparison, GenAI Features
- **Agent D**: LLM Agents, Settings, NotFound

Each agent will:

1. Navigate to each page
2. Execute all 5 scenarios
3. Take snapshots to verify rendering
4. Document pass/fail for each scenario with details on any failures

### Phase 2: Issue Consolidation

Aggregate all failures from the 4 agents into a single issue list, categorized by severity:

- **Critical**: Page crash, blank screen, JS error
- **Major**: Feature not working, wrong data displayed
- **Minor**: Layout glitch, missing translation, cosmetic issue

### Phase 3: Bug Fixing

Fix all issues found, prioritized by severity. Verify each fix with a re-test.

### Phase 4: Verification

Re-run failed scenarios to confirm all fixes work correctly.

---

## Key Files Likely to Be Modified

- Page components: [frontend/src/pages/](frontend/src/pages/) (Dashboard.tsx, Stocks.tsx, StockPrices.tsx, Settings.tsx, etc.)
- Layout components: [frontend/src/components/layout/](frontend/src/components/layout/) (BottomNavigation.tsx, Sidebar.tsx)
- Error boundary: [frontend/src/components/ErrorBoundary.tsx](frontend/src/components/ErrorBoundary.tsx)
- API layer: [frontend/src/lib/api.ts](frontend/src/lib/api.ts) or service files
- Translations: [frontend/src/locales/](frontend/src/locales/) (en/translation.json, ko/translation.json)
- Backend routes (if API issues found): [backend/app/api/v1/](backend/app/api/v1/)
