# MiroFish Use Case Templates

## Template 1: Financial Market Scenario Prediction

**Seed Document:** Fed minutes, earnings reports, economic indicators, financial news articles

**Prediction Requirement Example:**
```
Predict how individual investors, institutional investors, and market analysts will react
over the next 30 days if the Federal Reserve announces a surprise 50bp rate cut during
the upcoming FOMC meeting. Focus on equity markets, bond markets, and cryptocurrency.
```

**Recommended Settings:**
- `num_rounds`: 25-30
- `platform_type`: "twitter" (captures real-time market sentiment)
- God's Eye injection at round 10: "Breaking: Fed announces emergency 50bp rate cut"

**Post-Simulation Analysis:**
1. Check agent posts for sentiment shifts
2. Interview "institutional investor" agents about portfolio adjustments
3. Ask ReportAgent to summarize consensus and contrarian views
4. Compare with alphaear-sentiment scores

---

## Template 2: Public Opinion Crisis Simulation

**Seed Document:** Company background, product information, past PR incidents, social media history

**Prediction Requirement Example:**
```
Simulate public reaction if a safety incident involving our flagship product goes viral
on social media. Predict the 7-day trajectory of public sentiment, media coverage,
and potential regulatory response. Include consumer boycott probability.
```

**Recommended Settings:**
- `num_rounds`: 20-25
- `platform_type`: "twitter" + "reddit" (parallel)
- God's Eye injection at round 5: "Viral video surfaces showing product failure"
- God's Eye injection at round 15: "Company CEO issues public apology statement"

**Post-Simulation Analysis:**
1. Review timeline for sentiment turning points
2. Identify most influential agent voices (amplifiers vs dampeners)
3. Interview "journalist" and "regulator" agents for their perspectives
4. Generate crisis response recommendations via ReportAgent

---

## Template 3: Narrative / Novel Ending Prediction

**Seed Document:** Full text of incomplete novel or story (e.g., first 80 chapters of Dream of the Red Chamber)

**Prediction Requirement Example:**
```
Based on the character relationships, plot threads, and thematic patterns established
in the first 80 chapters, predict how the remaining story would unfold. Focus on
the fates of Jia Baoyu, Lin Daiyu, and Xue Baochai. Generate 3 possible endings.
```

**Recommended Settings:**
- `num_rounds`: 30-40 (complex character interactions need more rounds)
- `platform_type`: "reddit" (longer-form discussion suits narrative analysis)

**Post-Simulation Analysis:**
1. Interview key character agents about their motivations and decisions
2. Ask ReportAgent to compare predicted endings with literary analysis traditions
3. Generate a structured narrative summary of each predicted ending path

---

## Template 4: Policy Impact Assessment

**Seed Document:** Draft policy text, economic data, stakeholder position papers, historical policy outcomes

**Prediction Requirement Example:**
```
Simulate the economic and social impact of implementing a universal basic income (UBI)
of $1,000/month in a city of 500,000 people. Predict effects on employment, local
businesses, housing prices, and social services over a 12-month period.
```

**Recommended Settings:**
- `num_rounds`: 30
- `platform_type`: "twitter" (captures diverse stakeholder reactions)
- God's Eye injection at round 15: "Neighboring city announces competing tax reduction program"

**Post-Simulation Analysis:**
1. Review agent-stats for behavioral pattern changes
2. Interview "small business owner", "unemployed worker", "landlord" agents
3. Request statistical analysis via Report tools API
4. Generate policy recommendation brief via ReportAgent

---

## Template 5: Competitive Intelligence

**Seed Document:** Competitor product specs, market reports, customer reviews, industry news

**Prediction Requirement Example:**
```
Predict how the market will respond if competitor X launches a product with 50% better
performance at 30% lower price. Simulate reactions of existing customers, potential
switchers, industry analysts, and our sales team. Estimate 90-day market share impact.
```

**Recommended Settings:**
- `num_rounds`: 20
- `platform_type`: "twitter"
- God's Eye injection at round 10: "Independent reviewer publishes detailed benchmark comparison"

**Post-Simulation Analysis:**
1. Quantify sentiment shift among "customer" agents
2. Interview "sales representative" agents for competitive positioning insights
3. Generate competitive response strategy via ReportAgent
