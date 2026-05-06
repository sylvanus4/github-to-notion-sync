# Competitive Analysis — Industry & Company Positioning

Produce a structured competitive landscape analysis with market positioning maps, capability matrices, and strategic implications.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `financial-analysis` vertical plugin.

## Triggers

Use when the user asks to "analyze competitors", "competitive landscape", "competitive positioning", "industry analysis", "competitor comparison", "market positioning", "경쟁사 분석", "경쟁 구도", "시장 포지셔닝", "산업 분석", or needs to understand a company's position relative to peers in a financial services context.

Do NOT use for trading comps with multiples (use comps-analysis). Do NOT use for internal ThakiCloud product competitive intelligence (use kwp-product-management-competitive-analysis). Do NOT use for GTM battlecards (use pm-go-to-market or kwp-sales-competitive-intelligence).

## Workflow

### Step 1: Define the Competitive Arena

- Identify the target company and its primary industry/segment
- Define the relevant market (geographic, product, customer segment)
- Determine direct competitors (5-8) and adjacent competitors (2-3)

### Step 2: Gather Intelligence

For each competitor, collect:

**Quantitative:**
- Revenue, revenue growth (3-year CAGR)
- Market share (if available)
- Profitability metrics (gross margin, EBITDA margin, net margin)
- R&D spend as % of revenue
- Employee count and revenue per employee

**Qualitative:**
- Product/service portfolio
- Key customers and partnerships
- Recent strategic moves (M&A, partnerships, product launches)
- Management commentary from earnings calls
- Technology differentiation

### Step 3: Framework Analysis

Apply one or more frameworks:

**Porter's Five Forces:**
1. Threat of new entrants
2. Bargaining power of suppliers
3. Bargaining power of buyers
4. Threat of substitutes
5. Competitive rivalry intensity

**Positioning Matrix:**
- X-axis: relevant strategic dimension (e.g., price, breadth)
- Y-axis: relevant strategic dimension (e.g., quality, specialization)
- Plot each competitor as a bubble (size = market share or revenue)

**Capability Heat Map:**

| Capability | Company A | Company B | Company C | Target |
|------------|-----------|-----------|-----------|--------|
| Technology | Strong | Medium | Weak | Strong |
| Distribution | Medium | Strong | Strong | Weak |
| Brand | Strong | Strong | Medium | Medium |

Score: Strong (3), Medium (2), Weak (1)

### Step 4: SWOT Synthesis

For the target company relative to identified competitors:
- **Strengths**: What the target does better
- **Weaknesses**: Where competitors have clear advantage
- **Opportunities**: Market gaps or shifts favoring the target
- **Threats**: Competitive moves or market trends that threaten position

### Step 5: Strategic Implications

- Identify the 2-3 most important competitive dynamics
- Assess sustainability of competitive advantages (moats)
- Highlight potential disruption vectors
- Recommend strategic priorities based on competitive position

## Output Format

1. Executive summary (1 paragraph)
2. Market overview and size
3. Competitor profiles (1 page each, key metrics + strategy summary)
4. Framework analysis (Five Forces, positioning matrix, capability heat map)
5. SWOT matrix
6. Strategic implications and recommendations

## Composed Skills

| Skill | Purpose |
|-------|---------|
| `comps-analysis` | Pull financial multiples for competitor comparison |
| `parallel-web-search` | Research competitor news and strategy |
| `visual-explainer` | Generate positioning maps and heat maps |
| `anthropic-docx` | Format final competitive report |
