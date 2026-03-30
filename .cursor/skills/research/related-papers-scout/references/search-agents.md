# Phase 2: Search Agent Details

Detailed search queries and instructions for each of the 4 parallel
discovery agents.

## Table of Contents

1. [Agent 1: Semantic Scholar API](#agent-1-semantic-scholar-api)
2. [Agent 2: Google Scholar + arXiv Search](#agent-2-google-scholar--arxiv-search-via-websearch)
3. [Agent 3: Papers With Code + GitHub](#agent-3-papers-with-code--github-implementation-traction)
4. [Agent 4: Twitter/X + Community Buzz](#agent-4-twitterx--community-buzz-social-traction)

## Agent 1: Semantic Scholar API

The primary structured source. No API key required for low-volume usage.

### Step A — Get Recommendations

```bash
curl -s "https://api.semanticscholar.org/recommendations/v1/papers/forpaper/ARXIV:{arxiv_id}?fields=title,url,venue,year,citationCount,influentialCitationCount,authors,externalIds,openAccessPdf,abstract&limit=30"
```

If the input paper has no arXiv ID, search by title first:

```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query={url_encoded_title}&fields=paperId,title,externalIds&limit=1"
```

Then use the returned `paperId` in place of `ARXIV:{arxiv_id}`.

### Step B — Get Citing Papers

```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/ARXIV:{arxiv_id}/citations?fields=title,url,citationCount,authors,year,venue,abstract,externalIds&limit=30"
```

### Step C — Filter by Institution

For each candidate paper, check `authors[].affiliations[]` for matches
against the target institutions list. Keep papers where ANY author is
affiliated with: `Google`, `DeepMind`, `MIT`, `CSAIL`, `Stanford`,
`NVIDIA`.

Return all candidates with metadata and a boolean `institution_match` flag.

---

## Agent 2: Google Scholar + arXiv Search (via WebSearch)

Run 2-3 WebSearch queries tailored to the input paper:

```
WebSearch: "{title}" related work site:arxiv.org Google Research OR DeepMind OR MIT OR Stanford OR NVIDIA 2024 2025 2026
```

```
WebSearch: "{key_term_1}" "{key_term_2}" site:arxiv.org {arxiv_category} Google OR MIT OR Stanford OR NVIDIA
```

```
WebSearch: "{key_term_3}" "{key_term_4}" arxiv paper {year} Google Research OR Stanford AI OR NVIDIA Research
```

For each result:
- Extract arXiv ID from URL if present
- Record title, URL, snippet information
- Note institution mentioned in snippet

---

## Agent 3: Papers With Code + GitHub (Implementation Traction)

```
WebSearch: "{title}" OR "{key_term_1} {key_term_2}" site:paperswithcode.com
```

```
WebSearch: "{key_term_1}" "{key_term_2}" github implementation stars paper 2024 2025 2026
```

```
WebSearch: "{title}" github repository code release
```

For each candidate:
- Check if it has a GitHub repo linked
- Note star count if visible in search snippets
- Papers With Code listing itself is a positive signal
- Record arXiv IDs found in paperswithcode.com URLs

---

## Agent 4: Twitter/X + Community Buzz (Social Traction)

```
WebSearch: "{title}" site:x.com OR site:twitter.com paper
```

```
WebSearch: "{key_term_1}" "{key_term_2}" trending paper AI research 2025 2026
```

```
WebSearch: "{key_term_1}" "{key_term_2}" Google OR MIT OR Stanford OR NVIDIA new paper arxiv hot
```

```
WebSearch: "{title}" discussion thread blog review
```

For each result:
- Note papers appearing in Twitter/X discussions
- Track blog posts, YouTube explainers, newsletter mentions
- Record source and engagement signals (likes, retweets if visible)
