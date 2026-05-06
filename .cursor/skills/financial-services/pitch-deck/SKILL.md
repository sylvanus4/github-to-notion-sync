# Pitch Deck — Investment Banking Presentation Builder

Populate investment banking pitch deck templates with data-driven content: situation overview, strategic alternatives, valuation summary, transaction comparables, and management presentation slides.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `investment-banking` vertical plugin.

## Triggers

Use when the user asks to "build a pitch deck", "pitch book", "IB presentation", "sell-side pitch", "buy-side pitch", "management presentation", "strategic alternatives presentation", "피치 덱 작성", "투자은행 프레젠테이션", "M&A 피치", "전략적 대안 발표자료", or needs to create client-facing investment banking presentations.

Do NOT use for general marketing presentations (use presentation-strategist). Do NOT use for startup pitch decks without financial depth (use presentation-strategist). Do NOT use for deck quality review after creation (use deck-qc).

## Rendering Limitations

AI cannot directly produce formatted PPTX files with precise layouts. This skill produces structured content that maps to standard pitch book templates.

**Output format**: Slide-by-slide markdown with content blocks, data tables, and chart specifications that a human or template engine fills into the actual deck.

## Standard Pitch Book Sections

### 1. Cover Page
- Client name and logo placement
- Bank/advisor name
- Date and classification (Confidential, Draft, Preliminary)
- Project code name (if applicable)

### 2. Table of Contents
- Section list with slide numbers

### 3. Situation Overview
- Company description (2-3 sentences)
- Key financial metrics snapshot
- Strategic context (why this engagement, why now)
- Industry backdrop (1-2 slides)

### 4. Company Profile
- Business segment breakdown
- Revenue and EBITDA history (5 years)
- Key products/services
- Geographic revenue mix
- Management team overview
- Shareholder structure

### 5. Financial Summary
- Income statement summary (3-5 years historical + 2-3 projected)
- Key ratios and margins
- Balance sheet highlights
- Cash flow summary

### 6. Valuation Analysis
- Trading comps summary table (from comps-analysis)
- Transaction comps summary (precedent transactions)
- DCF summary (from dcf-model)
- Valuation football field (range comparison chart)

### 7. Strategic Alternatives
- Status quo analysis
- Sale process (potential buyers list)
- Merger/partnership options
- Recapitalization alternatives
- Each with pros/cons matrix

### 8. Buyer Universe
- Strategic buyers (categorized by rationale)
- Financial sponsors (PE firms with relevant experience)
- For each: name, description, rationale, estimated capacity

### 9. Process Recommendations
- Recommended transaction structure
- Timeline (milestone-based)
- Key considerations and risks
- Next steps

### 10. Appendix
- Detailed financial projections
- Comparable company detail sheets
- Industry data
- Disclaimers and disclosures

## Formatting Standards

- Use consistent number formats throughout ($XM, $XB)
- All tables must include source footnotes
- Valuation ranges shown as low-mid-high
- Charts specify: type, axes, data series, colors
- Every slide has a clear headline (action title, not descriptive)

### Action Titles (Required)
Each slide headline should state the key takeaway:
- WRONG: "Revenue Summary"
- RIGHT: "Revenue Has Grown 15% CAGR Driven by North American Expansion"

## Anti-Patterns (Do NOT Do)

- Do NOT invent financial data; use placeholders `[DATA NEEDED]` if unavailable
- Do NOT include unverified projections without "management estimate" label
- Do NOT create misleading charts (e.g., truncated axes, cherry-picked periods)
- Do NOT use informal language; maintain professional IB tone
- Do NOT include internal advisor notes in client-facing sections

## Workflow

1. Gather all required data (company filings, market data, precedent transactions)
2. Run comps-analysis and dcf-model for valuation sections
3. Populate each section with structured content
4. Flag data gaps as `[DATA NEEDED: {description}]`
5. Generate slide-by-slide output in markdown
6. Run deck-qc on the output

## Composed Skills

| Skill | Purpose |
|-------|---------|
| `comps-analysis` | Trading comparables for valuation section |
| `dcf-model` | DCF valuation for football field |
| `competitive-analysis` | Industry positioning for situation overview |
| `deck-qc` | Post-creation quality review |
| `anthropic-pptx` | Template population if PPTX output needed |
| `parallel-web-search` | Industry data and recent news |
