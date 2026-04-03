---
description: "SEO operations — content attack briefs, GSC optimization, keyword gap analysis, trend scouting"
argument-hint: "[brief|gsc|trends|auth] [domain or keyword]"
---

# Marketing SEO Ops

Read and follow the skill at `.cursor/skills/marketing/marketing-seo-ops/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Run the requested SEO operation:

| Command | Script | Purpose |
|---------|--------|---------|
| `brief` | `scripts/content_attack_brief.py` | Generate content attack brief |
| `gsc` | `scripts/gsc_client.py` | GSC analysis (--striking, --queries, --trend) |
| `trends` | `scripts/trend_scout.py` | Discover emerging search trends |
| `auth` | `scripts/gsc_auth.py` | Authenticate with Google Search Console |

Requires: `GSC_SITE_URL`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` environment variables.
