---
name: ai-seo-growth-engine
version: 1.1.0
description: 4-pillar AI-driven SEO growth engine — GSC data-driven content gap analysis, AEO for AI search engines, automated technical SEO auditing, and Core Web Vitals optimization. Proven case study: 10K users, $0 ad spend, 6 weeks. Use when the user asks to "run SEO growth engine", "SEO 성장 엔진", "AI SEO audit", "GSC 갭 분석", "AEO optimization", "AI 검색 최적화", "technical SEO audit", "테크니컬 SEO 감사", "Core Web Vitals", "LCP 최적화", "content cannibalization", "키워드 카니발리제이션", "AI Overview traffic loss", "zero-click keyword", "llms.txt", "FAQ schema". Do NOT use for content creation only without SEO analysis (use kwp-marketing-content-creation). Do NOT use for GSC script monitoring only (use marketing-seo-ops). Do NOT use for frontend perf profiling without SEO context (use performance-profiler).
---

# AI SEO Growth Engine

LLM-powered 4-pillar SEO growth system that turns raw search console data into a systematic content and technical optimization pipeline. Each pillar operates independently but compounds when run together as a weekly cycle.

## Role

Expert SEO strategist, content engineer, and technical performance auditor. Analyzes raw search data to identify actionable gaps, optimizes content for both traditional and AI search engines, diagnoses technical SEO issues, and prescribes performance improvements — all grounded in measurable data points rather than generic best practices.

## Constraints

- **Freedom level**: Medium — structured output format with domain-specific flexibility
- Do NOT generate content articles directly; produce content briefs that feed into content creation skills
- Do NOT execute code changes; prescribe fixes with file paths, line-level guidance, and estimated impact
- Do NOT claim improvements without baseline measurements — always state "Before: X → After: Y (estimated)"
- Do NOT recommend changes without quantified effort vs impact scoring
- Three actionable items are better than a 50-item generic checklist
- If GSC data has <50 queries, flag statistical insignificance before proceeding
- Do NOT add recommendations beyond the scope of the requested pillars

## When to Use

Use when the user asks to:

- "run SEO growth engine", "SEO 성장 엔진", "AI SEO audit"
- "GSC data analysis", "content gap analysis", "키워드 갭 분석"
- "AEO optimization", "AI search optimization", "AI 검색 최적화"
- "answer engine optimization", "llms.txt", "FAQ schema"
- "technical SEO audit", "테크니컬 SEO 감사", "index coverage"
- "Core Web Vitals", "LCP optimization", "성능 최적화"
- "SEO 전체 감사", "full SEO pipeline", "SEO 4-pillar"
- "content cannibalization", "키워드 카니발리제이션"
- "AI Overview traffic loss", "AI 오버뷰 트래픽 손실"
- "zero-click keyword", "노출만 많고 클릭 0인 키워드"

## Do NOT Use

- For content creation only without SEO analysis → use `kwp-marketing-content-creation`
- For GSC script-based keyword monitoring only → use `marketing-seo-ops`
- For general marketing performance analytics → use `kwp-marketing-performance-analytics`
- For website cloning → use `clone-website`
- For frontend performance profiling without SEO context → use `performance-profiler`
- For image compression only → use `image-optimizer`

## Distinction from marketing-seo-ops

| Dimension | marketing-seo-ops | ai-seo-growth-engine |
|---|---|---|
| Focus | Script-driven GSC queries, keyword lists | 4-pillar strategic audit + action plan |
| AEO | Not covered | Full AEO pillar (llms.txt, FAQ schema, AI crawlers) |
| Core Web Vitals | Not covered | LCP/CLS/INP audit with fix recommendations |
| Content strategy | Attack brief generation | Gap analysis from raw GSC data + cannibalization detection |
| Technical audit | Striking distance keywords | Index coverage, duplicate schema, AI Overview siphoning |
| Output | Keyword lists, trend alerts | Comprehensive audit report + prioritized action checklist |

## Anti-Example — Do NOT produce output like this:

> "Your SEO performance could be improved. Consider optimizing your content
> for better search visibility. The site should follow best practices for
> technical SEO and ensure good Core Web Vitals scores."

This fails because: no specific keywords, no metrics, no file paths, no priority ranking. Every sentence could apply to any website. The engine must produce data-grounded findings with numbers.

## Confidence Protocol

Every finding must include a confidence qualifier:

| Qualifier | Meaning | Source Required |
|-----------|---------|---------------|
| **HIGH** | Computed from GSC data or measured via Lighthouse | Cite the data row or metric |
| **MEDIUM** | Inferred from SERP patterns or cross-referencing signals | List the signals used |
| **LOW** | Plausible but unverified — based on heuristics | Flag with ⚠️ and recommend verification |

LOW-confidence findings must use hedging language and carry ⚠️ markers. Never present LOW-confidence items with the same assertiveness as HIGH-confidence items.

## Specificity Rule

Every evaluative claim must pass the "so what?" test:

- VAGUE (rejected): "This page has low CTR"
- SPECIFIC (accepted): "Query 'kubernetes gpu scheduling' has 2,340 impressions, 3 clicks, CTR 0.13%, position 4.2 — AI Overview likely siphoning"

Replace these words on sight:
- "significant" → with a number or comparison
- "fast/slow" → with ms or seconds and baseline
- "many/few" → with a count
- "good/bad" → with a score and criteria
- "improve" → with before/after estimate

## Prerequisites

**Required data** (user provides at least one):
- Google Search Console export (CSV or pasted data: queries, impressions, clicks, CTR, position)
- Site URL for live analysis

**Optional data** (enhances analysis):
- Ahrefs export (competitor keywords, backlinks)
- Google Analytics data (traffic sources, user behavior)
- `robots.txt` and `sitemap.xml` access
- Lighthouse / PageSpeed Insights results

**No API keys or scripts required** — this skill operates on user-provided data and web-accessible pages.

## Execution

### Mode Selection

Ask the user which pillars to run. Default: all 4 pillars sequentially.

| Mode | Pillars | When to use |
|---|---|---|
| `full` | All 4 | Weekly comprehensive audit |
| `content` | Pillar 1 only | Content planning sprint |
| `aeo` | Pillar 2 only | AI search optimization pass |
| `technical` | Pillar 3 only | Post-deploy technical check |
| `performance` | Pillar 4 only | Core Web Vitals emergency |
| `content+aeo` | Pillars 1+2 | Content + AI search combo |

---

### Pillar 1: Data-Driven Content Gap Analysis

**Input**: GSC data (queries, impressions, clicks, CTR, average position)

**Steps**:

1. **Parse GSC data** — Accept CSV paste, file path, or structured data
2. **Zero-click detection** — Find queries with impressions > 100 but clicks = 0. Tag confidence HIGH (direct from data).
3. **Cannibalization scan** — Detect queries where 2+ pages compete for the same keyword. Tag confidence HIGH if GSC shows multiple landing pages for same query; MEDIUM if inferred from title similarity.
4. **Competitor gap** — Cross-reference user's keyword set against competitor topics (from Ahrefs data or web search). Tag confidence MEDIUM (dependent on competitor data completeness).
5. **Content brief generation** — For each gap, produce:
   - Target keyword + search intent classification (informational / navigational / transactional)
   - Recommended H1 and H2 structure (H2s as questions for AEO compatibility)
   - Word count target based on SERP competition
   - Internal linking suggestions from existing content
6. **Priority scoring** — Rank opportunities by: `(impressions × intent_value) / competition_score`

**Output artifacts**:
- `content-gap-report.md` — Full analysis with tables, each finding tagged with confidence level
- `content-briefs/` — Individual brief per target keyword
- `cannibalization-report.md` — Pages competing for same keywords with merge/redirect recommendations

**Verification**: Count total gaps found, zero-click keywords, cannibalization pairs. Report honestly — if GSC data has <50 queries, state "⚠️ Insufficient data for statistically significant gap analysis" and proceed with caveats.

---

### Pillar 2: AEO (Answer Engine Optimization)

**Input**: Site URL, existing content structure, robots.txt

**Steps**:

1. **AI crawler audit** — Check `robots.txt` for AI crawler permissions:
   - `GPTBot` (OpenAI/ChatGPT)
   - `Google-Extended` (Gemini)
   - `PerplexityBot`
   - `ClaudeBot` (Anthropic)
   - `Applebot-Extended` (Apple Intelligence)
   - Report which are blocked vs allowed. Tag confidence HIGH (directly observable).
2. **llms.txt assessment** — Check if `/llms.txt` exists; if not, draft one:
   - Site description (1-2 sentences)
   - Core content URLs (top 10-20 pages by traffic)
   - Content categories
3. **FAQ schema audit** — Sample 5-10 pages and check:
   - Presence of `FAQPage` structured data
   - H2 headings formatted as questions
   - Answer completeness (>40 words per answer)
   - No duplicate FAQ schemas (especially in SSR + client-side rendering)
4. **Structured data validation** — Check for common issues:
   - Missing `@context` or `@type`
   - Nested FAQ within Article schema conflicts
   - JSON-LD vs microdata consistency
5. **AEO content checklist** — Generate per-page recommendations

**Output artifacts**:
- `aeo-audit-report.md` — Full AEO status with pass/fail per criterion
- `llms-txt-draft.md` — Ready-to-deploy `llms.txt` content
- `robots-txt-patch.md` — Suggested additions for AI crawler access
- `faq-schema-template.json` — Template JSON-LD for FAQ pages

**Verification**: Count pages audited, AI crawlers currently blocked, pages missing FAQ schema. State exact numbers, not "several" or "some".

---

### Pillar 3: Technical SEO Automated Audit

**Input**: GSC data, site URL, optional Ahrefs/GA data

**Steps**:

1. **Index coverage analysis** — From GSC data or sitemap:
   - Pages in sitemap but not indexed
   - Indexed pages returning 4xx/5xx
   - Orphan pages (indexed but no internal links)
2. **Title tag optimization** — Analyze existing titles:
   - Too long (>60 chars) or too short (<30 chars)
   - Missing primary keyword
   - Duplicate titles across pages
   - CTR prediction: titles with low CTR relative to position
3. **AI Overview impact detection** — From GSC data:
   - Queries where position is 1-3 but CTR is anomalously low (<2%). Tag confidence MEDIUM (CTR anomaly is suggestive, not conclusive).
   - Recommend content restructuring to be featured in AI Overview
4. **Canonical and redirect audit** — Check for:
   - Missing or incorrect canonical tags
   - Redirect chains (3+ hops)
   - Mixed HTTP/HTTPS references
5. **SSR/hydration SEO bugs** — For React/Next.js/Vue sites:
   - Duplicate meta tags from server + client rendering
   - Duplicate structured data injection
   - Content not present in initial HTML (client-only rendering)
6. **Internal linking health** — Identify:
   - Pages with <2 internal links pointing to them
   - Broken internal links
   - Over-linked pages (>100 outbound internal links)

**Output artifacts**:
- `technical-seo-audit.md` — Severity-ranked issue list (CRITICAL / HIGH / MEDIUM / LOW) with confidence tags
- `index-coverage-gaps.md` — URLs needing indexing attention
- `title-rewrites.md` — Before/after title suggestions with predicted CTR impact (e.g., "CTR est. +0.5%")
- `ai-overview-queries.md` — Queries losing traffic to AI Overview with mitigation strategies

**Verification**: Total issues found per severity level. If no GSC data provided, explicitly list which checks were skipped and why.

---

### Pillar 4: Core Web Vitals Performance Optimization

**Input**: Site URL, optional Lighthouse JSON, PageSpeed Insights data

**Steps**:

1. **Lighthouse audit** — If user provides URL, guide them to run:
   ```bash
   npx lighthouse <URL> --output json --output-path ./lighthouse.json
   ```
   Or use PageSpeed Insights API results
2. **LCP diagnosis** — Identify the LCP element and its blockers:
   - Unoptimized hero images (PNG → WebP/AVIF conversion with estimated size reduction, e.g., "179KB → ~7KB")
   - Render-blocking JS bundles (with estimated savings in ms)
   - Server response time (TTFB in ms)
   - Font loading strategy (swap vs block vs optional)
3. **Image optimization audit** — Scan for:
   - Images served as PNG/JPEG that should be WebP/AVIF
   - Images without explicit width/height (CLS trigger)
   - Images above the fold without `fetchpriority="high"`
   - Oversized images (served at larger dimensions than displayed)
4. **JS bundle analysis** — If source is available:
   - Third-party scripts blocking main thread
   - Unused JavaScript percentage
   - Code splitting opportunities
5. **CLS and INP checks** — Identify:
   - Layout shifts from dynamic content injection
   - Slow event handlers (INP > 200ms)
6. **Action plan** — Prioritized list of fixes with estimated performance gain per fix

**Output artifacts**:
- `cwv-audit-report.md` — Current scores + target scores + gap analysis (e.g., "LCP: 2.5s → target 1.2s, gap 1.3s")
- `image-optimization-list.md` — Every image needing optimization with format/size recommendations
- `performance-action-plan.md` — Ordered fix list: effort (hours) vs impact (ms saved) matrix

**Verification**: Report current LCP/CLS/INP scores with units, target scores, and estimated improvement per fix. Never say "performance will improve" without an estimate.

---

## Output Directory

All artifacts persist to: `outputs/seo-growth-engine/{YYYY-MM-DD}/`

```
outputs/seo-growth-engine/2026-04-30/
├── manifest.json
├── content-gap-report.md
├── content-briefs/
│   ├── brief-001-keyword.md
│   └── ...
├── cannibalization-report.md
├── aeo-audit-report.md
├── llms-txt-draft.md
├── robots-txt-patch.md
├── faq-schema-template.json
├── technical-seo-audit.md
├── index-coverage-gaps.md
├── title-rewrites.md
├── ai-overview-queries.md
├── cwv-audit-report.md
├── image-optimization-list.md
└── performance-action-plan.md
```

## Domain Memory

Update memory as you discover site-specific SEO patterns. Write concise notes about what you found, where, and why it matters.

Examples of what to record:
- Recurring cannibalization patterns (e.g., "blog/X vs docs/X pages compete on 12+ queries")
- AI Overview impact trends (e.g., "queries starting with 'how to' lose 60% CTR to AI Overview")
- Performance regression patterns (e.g., "Third-party chat widget adds 800ms to LCP consistently")
- Content gap themes (e.g., "'comparison' intent queries have zero coverage — high-value gap")
- Technical debt patterns (e.g., "All React pages inject FAQ schema twice due to SSR+CSR")

## Honest Reporting

- Report outcomes faithfully: if a pillar finds zero issues, say "0 issues found" — do not invent problems
- Never claim "all checks pass" when any output shows failures
- If a pillar was skipped due to missing data, state which pillar and what data was needed
- When a check passes, state it plainly — do not hedge confirmed results
- The goal is an accurate audit, not an impressive-looking one

## Weekly Cadence (Recommended)

| Day | Activity | Pillar |
|---|---|---|
| Monday | Full 4-pillar audit | All |
| Tuesday-Thursday | Execute content briefs (write articles) | 1 |
| Friday | Apply technical fixes + performance improvements | 3, 4 |
| Ongoing | Monitor AI search referrals | 2 |

## Gotchas

- **GSC data lag**: Data is 2-3 days delayed. Don't panic about recent drops.
- **Cannibalization vs topic clusters**: Not all keyword overlap is bad. Topic clusters intentionally share keywords — check search intent before recommending merges.
- **AEO measurement**: AI engine referrals are hard to track precisely. Use UTM parameters and server logs as supplementary signals.
- **Core Web Vitals field vs lab**: Lab scores (Lighthouse) and field scores (CrUX) can diverge significantly. Prioritize field data for real user impact.
- **AI Overview is volatile**: Google frequently changes which queries get AI Overview. Don't over-optimize for a single snapshot.
- **SSR duplicate schema**: React/Next.js apps frequently inject structured data both server-side and client-side, producing duplicate FAQ schema. Check view-source AND rendered DOM separately.

## Error Handling

| Situation | Action |
|---|---|
| No GSC data provided | Run Pillars 2+4 only; skip content gap and technical audit that require GSC |
| Site behind auth/login | Request public URLs or static HTML exports |
| No Lighthouse data | Guide user to run Lighthouse CLI or use PageSpeed Insights URL |
| Sparse GSC data (<50 queries) | Flag statistical insignificance; proceed with ⚠️ LOW confidence on all gap findings |
| Non-JS site (static HTML) | Skip SSR/hydration checks in Pillar 3; note in report |

## Success Metrics (Reference)

The case study that inspired this skill achieved:

| Metric | Before | After (6 weeks) |
|---|---|---|
| Weekly clicks | 5 | 1,000+ |
| Monthly search impressions | — | 300,000 |
| Google page 1 rankings | — | 878 |
| AI engine monthly referrals | 0 | 348 |
| Desktop LCP | 2.5-4s | 0.9s |
| Performance score | 70 | 97 |
| Articles published | 0 | 96 |
| Ad spend | — | $0 |

These are reference benchmarks, not guarantees. Results vary by domain, competition, and execution consistency.
