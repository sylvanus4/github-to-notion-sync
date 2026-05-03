---
name: seo-aeo-growth-engine
description: Use Claude as SEO strategist + content engine + CTO to grow organic-only traffic. Pipeline covers GSC-driven content gap analysis, AEO (Answer Engine Optimization) for ChatGPT/Gemini/Perplexity citation, weekly technical SEO audit (GSC + Ahrefs + GA), and Core Web Vitals tuning (LCP/CLS/INP). Trigger when user asks for organic growth, SEO audit, AEO setup, GSC analysis, content calendar from search data, llms.txt setup, FAQ schema, or LCP optimization. Do NOT use for paid search/SEM, Google Ads, social-only growth, sites with < 28 days of GSC data, or ecommerce category-page optimization.
---

# SEO + AEO Growth Engine

A 4-pillar playbook to ship organic growth without paid acquisition. Reproduces the case where a founder hit 10K MAU in 6 weeks using Claude as strategist, writer, and engineer.

**Benchmark (one founder, 6w):** 96 articles · 5→1K+ weekly clicks · 300K impressions/mo · 878 page-1 rankings · 348 AEO refs/mo · LCP 2.5–4s→0.9s · perf 70→97.

## Scope

**Use when:** site has ≥ 28 days of GSC data; goal is editorial / docs / blog organic growth; team can ship code (Pillar 4 needs deploys).

**Do NOT use for:**
- Paid search / SEM strategy, Google Ads, bid management → use a dedicated SEM skill
- Social-only growth (TikTok, IG, X) — none of the 4 pillars apply
- Sites with < 28 days of GSC data — Pillar 1 needs ≥ 200 impressions per query to mine gaps
- Ecommerce category-page / faceted-navigation optimization → different mechanics (canonical groups, parameter handling)
- Local SEO / Google Business Profile — Pillar 2 AEO ≠ map-pack ranking
- Programmatic SEO at template scale → use `goose-programmatic-seo-planner` instead

---

## Pillar 1 — Data-Driven Content Strategy

Goal: stop writing blind. Feed Claude raw search data, mine the gap, write into the gap.

### Inputs to gather
- GSC `Performance` export (last 90d): `query`, `page`, `clicks`, `impressions`, `ctr`, `position`
- GSC `Pages` export: indexed URL list
- (Optional) Ahrefs `Top pages` + `Content gap` for 2–3 competitors
- Sitemap URL or list of existing posts

### Claude prompt template
```
You are an SEO content strategist. Analyze this GSC export and find:

1. HIGH-IMPRESSION ZERO-CLICK queries (impressions ≥ 200, CTR < 1%) — title/snippet rewrite candidates
2. POSITION 11–20 queries — one-edit-away-from-page-1 wins
3. KEYWORD CANNIBALIZATION — same query, multiple URLs, none winning. Pick the canonical, redirect/merge the rest
4. CONTENT GAPS — competitor topics absent from my sitemap
5. INTERNAL-LINK ORPHANS — pages with impressions but ≤ 1 inbound internal link

Output a prioritized table: [opportunity, query, current_pos, est_lift, action, owner]

GSC data:
<paste CSV>

Sitemap:
<paste URLs or sitemap.xml>
```

### Output cadence
- Weekly: top-20 opportunity table → 5 commits to content backlog
- Monthly: cannibalization sweep + redirect plan
- Per article: brief = target query + cluster + intent + 5 H2 questions + FAQ pairs

---

## Pillar 2 — AEO (Answer Engine Optimization)

Goal: not "rank #1 on Google" — get *cited* by ChatGPT, Gemini, Perplexity, Claude.

### Inputs to gather
- Current `robots.txt` (raw text)
- Current `sitemap.xml` (URL list)
- Sample article HTML (DOM dump — to verify rendered FAQ JSON-LD, not just source)
- Existing FAQ block inventory: `[url, h2_count, faq_jsonld_present, faq_visible_qa_count]`

### Quantitative bar
- TL;DR paragraph: **≤ 50 words**, ≤ 2 sentences, opens with the answer noun
- FAQ schema: visible Q&A count on page **must equal** `mainEntity[]` length (1:1 — schema-only Q&A is a Google penalty)
- `llms.txt`: **≤ 200 lines**, each URL one-line summary ≤ 120 chars
- Allowlist crawler set: **≥ 4** of {GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Bingbot} explicitly named
- `Article` schema fields required: author, datePublished, dateModified, headline, image (≥ 1200×630)

### Claude prompt
```
Run an AEO setup audit. Inputs: current robots.txt, sitemap.xml URL list, FAQ inventory CSV (columns: url, h2_count, faq_jsonld_present, faq_visible_qa_count), sample article HTML (rendered DOM, not source).

Produce 4 outputs:

1. robots.txt diff — append explicit Allow rules for ≥ 4 of {GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Bingbot}. Flag any existing Disallow that blocks them.
2. /llms.txt content — site description (≤ 1 line), then Core pages + Docs sections. ≤ 200 lines total, each URL summary ≤ 120 chars.
3. FAQ schema audit table — [url, faq_jsonld_present, visible_qa_count, mainEntity_count, mismatch_flag, fix_action]. Flag any url where visible_qa_count != mainEntity_count (penalty risk).
4. Article schema gaps — list articles missing any of: author, datePublished, dateModified, headline, image (≥ 1200×630).

Output as one markdown file with each section as H2.
```

### On-page checklist
- [ ] All `H2` tags rewritten as **direct questions** ("How does X work?" not "About X")
- [ ] First paragraph after each H2 = ≤ 50-word direct answer (TL;DR style)
- [ ] FAQ schema (`FAQPage` JSON-LD) on every article — visible Q&A 1:1 matched
- [ ] `Article` schema with `author`, `datePublished`, `dateModified`
- [ ] Tables and bullet lists for comparisons (LLMs lift these into citations)

### Crawler & discovery files
- `robots.txt` — explicitly **allow** AI crawlers (do not block by default):
  ```
  User-agent: GPTBot
  Allow: /
  User-agent: ClaudeBot
  Allow: /
  User-agent: PerplexityBot
  Allow: /
  User-agent: Google-Extended
  Allow: /
  ```
- `/llms.txt` at root — site description + curated URL index for LLM ingestion. Format:
  ```
  # <Site Name>
  > One-line value prop.
  ## Core pages
  - [Title](url): one-line summary
  ## Docs
  - [Title](url): one-line summary
  ```
- `/llms-full.txt` (optional) — full markdown of key articles concatenated

### Validation
- Search target query in ChatGPT / Perplexity / Gemini weekly. Log citations in a `aeo-citations.md` ledger
- Track `Referer` from `chat.openai.com`, `perplexity.ai`, `gemini.google.com` in GA4

---

## Pillar 3 — Weekly Technical SEO Audit

Feed three datasets to Claude every Monday. Get a punch list by Tuesday.

**When to use this vs `goose-seo-content-audit`:** this pillar runs alongside Pillars 1/2/4 as part of the integrated growth loop and ingests live GSC/Ahrefs/GA datasets. For a content-only deep audit (no AEO/CWV scope, no live datasets — just sitemap + content inventory), use `goose-seo-content-audit` directly.

### Datasets
1. GSC `Performance` (last 7d, full export — columns: `query, page, clicks, impressions, ctr, position, date`)
2. Ahrefs `Site audit` JSON or CSV (issue table — columns: `url, issue_type, severity, http_status, redirect_hops`)
3. GA4 `Pages and screens` (last 7d — columns: `page_path, sessions, engaged_sessions, bounce_rate, avg_session_duration`)

### Thresholds (used by the audit prompt below)
- Index gap: sitemap URL absent from GSC indexed set for **≥ 14 days** → flag
- AI Overview hijack: `clicks WoW change ≤ -50%` while `impressions WoW change ≥ -10%` → confirmed hijack
- Title/meta rewrite: position in `[5, 15]` AND CTR `< (median CTR for that position band × 0.6)` → rewrite candidate
- Schema error: same `@type` JSON-LD block appearing **> 1 times** in rendered DOM → duplicate
- Redirect chain: `redirect_hops ≥ 3` → crawl-budget waste
- Orphan page: top-quartile traffic AND inbound internal links **≤ 2** → orphan

### Claude prompt
```
Run a technical SEO audit. Identify:

A. INDEXATION GAPS — URLs in sitemap but not in GSC `Indexed` set
B. AI OVERVIEW HIJACKS — queries where impressions > 100 but CTR collapsed (≥ 50% drop WoW). These are AI Overview cannibalizing clicks
C. TITLE/META REWRITES — pages with position 5–15 and CTR below median for that position band
D. SCHEMA ERRORS — duplicate / malformed JSON-LD (esp. React+SSR double-mount FAQ schema)
E. CRAWL WASTE — Ahrefs flagged 4xx/5xx/redirect chains affecting crawl budget
F. ORPHANED HIGH-VALUE PAGES — top-quartile traffic, ≤ 2 internal links

For each, output: [issue, affected_urls (sample 5), severity, fix_diff_or_action]
```

### Common findings (this case study)
- 18 URLs missing from index → fix `<meta robots>` or submit via URL Inspection API
- 121 queries hijacked by AI Overview → pivot to long-tail / how-to angles
- React + SSR double-mounting `FAQPage` JSON-LD (client + server both injected) → render server-side only, gate client with `typeof window`

---

## Pillar 4 — Core Web Vitals (LCP / CLS / INP)

Content alone won't save a 4-second LCP. Hand Claude the bundle + Lighthouse trace, ship the diff.

### Inputs
- `npx lighthouse <url> --output=json --form-factor=desktop` (and mobile)
- `next build` / `vite build` output (bundle stats)
- DevTools `Performance` trace (export as `.json`)

### Claude prompt
```
Optimize Core Web Vitals. Target: desktop LCP < 1.0s, mobile LCP < 2.5s, CLS < 0.05, INP < 200ms.

From the Lighthouse JSON + bundle stats, produce:

1. LCP path — what is the LCP element, what blocks it (render-blocking JS/CSS, late-loaded image, font swap)
2. JS bundle hit list — top 10 chunks > 30KB gzipped, with code-split / lazy-load recommendation
3. Image plan — every above-the-fold image: format (WebP/AVIF), dimensions, `loading`, `fetchpriority`
4. Font plan — `preload` + `font-display: swap` + subset
5. Third-party audit — every `<script>` tag: defer-able, async-able, or removable

For each item, output a concrete diff (file path + before/after).
```

### Quick wins (case study)
- 179KB PNG logo → 7KB WebP; hero `fetchpriority="high"` + `<link rel="preload">`
- Defer analytics + chat widget to `requestIdleCallback`; self-host fonts; PurgeCSS unused Tailwind

---

## Execution Cadence (6-Week Sprint)

| Week | Focus | Deliverable |
|---|---|---|
| 1 | Pillar 1 setup | GSC export pipeline + first opportunity table |
| 1–2 | Pillar 2 setup | `robots.txt`, `llms.txt`, FAQ schema across all posts |
| 2 | Pillar 4 baseline | Lighthouse audit + LCP/JS/image fix PRs |
| 1–6 | Pillar 1 publish | 12–16 articles/week from gap analysis |
| 3,5 | Pillar 3 audit | Mid-sprint + late-sprint technical sweeps |
| 6 | Measure | GSC/GA4/AEO ledger review, decide next sprint |

---

**Required files at repo root:** `robots.txt`, `/llms.txt`, `sitemap.xml` (auto), `aeo-citations.md` (LLM citation ledger), `seo-backlog.md` (opportunity queue, owner + due-date).

---

## Anti-Patterns (do not do)

**Pillar 1 — Content**
- "Write a blog post about X" prompt with no GSC data attached → generic copy, won't rank
- Publishing into a cluster without first deduping cannibalized URLs → splits ranking signal across self-competing pages

**Pillar 2 — AEO**
- Blocking AI crawlers in `robots.txt` (or default-deny) → kills AEO referrals permanently — no rollback
- FAQ schema without matching visible Q&A 1:1 → Google structured-data penalty risk

**Pillar 3 — Audit**
- Running audit but not enqueuing fixes into `seo-backlog.md` with owner + due-date → findings evaporate
- Treating AI Overview hijacks as recoverable rankings → they almost never come back; pivot intent or write a different long-tail angle

**Pillar 4 — Core Web Vitals**
- Optimizing CLS by removing animations users actually expect → UX regression masquerading as a perf win
- Publishing 96 articles before fixing LCP → wasted crawl budget on slow pages, hurts the cohort

---

## Success Metrics

Track weekly in a single dashboard:
- GSC: clicks, impressions, avg position, page-1 rankings count
- GA4: organic sessions, AEO referrals (`chat.openai.com`, `perplexity.ai`, `gemini.google.com`)
- Lighthouse: LCP, CLS, INP, perf score (per top-10 page)
- Content velocity: articles shipped/week, opportunity-to-published lead time

Stop the sprint and re-plan if after week 3:
- Indexed page count not growing
- Avg position worsening across the cohort
- Mobile LCP still > 2.5s
