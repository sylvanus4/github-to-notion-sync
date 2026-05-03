---
name: policy-as-skill-manager
description: >-
  Convert canonical policy documents into enforceable SKILL.md assets: fetch
  policy text from Notion, structure constraints/triggers/checklists as a
  skill, version skills, and flag when source policy changes require
  regeneration. Korean triggers: "정책 스킬 변환", "정책 자동화", "정책 SKILL.md", "정책을
  스킬로". English triggers: "policy to skill", "policy-as-skill", "convert
  policy", "policy skill file", "Notion policy to SKILL.md". Do NOT use for
  generating end-user UI copy from policy (use policy-text-generator), generic
  skill authoring without a policy source (use create-skill), or legal review.
---

# Policy-as-Skill Manager

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

Turn **authoritative policy pages** in Notion into **versioned** `SKILL.md` files under `.cursor/skills/` so agents enforce rules consistently, with an **update-detection** loop tied to Notion revisions.

## Prerequisites

- **Notion MCP** access to the policy parent page or database.
- Write access to `.cursor/skills/<policy-skill-slug>/SKILL.md` in this repo.

## Procedure

1. **Identify source** — Notion URL or database entry for the policy. Record: title, `last_edited_time` (if exposed), owner team, scope (product-wide vs domain).

2. **Fetch content** — Use **Notion MCP** to pull page blocks / properties. Normalize to plain structured sections: purpose, rules, exceptions, definitions, enforcement checklist.

3. **Design skill shape** — Map policy to skill anatomy:
   - `description`: triggers + “Do NOT use for …” boundaries (mirror policy scope).
   - Body: mandatory **procedure** (how to verify compliance), **checklists**, **severity model** if applicable.
   - **No external repo paths**; reference only Notion URLs and in-repo paths.

4. **Versioning** — In YAML `metadata`, set `version: "1.0.0"` on first publish; for updates use semver patch for wording, minor for new obligations, major for breaking rule changes. Add a **Change log** subsection in the body (date + Notion snapshot id or edited time).

5. **Write SKILL.md** — Create or update `.cursor/skills/<slug>/SKILL.md`. Keep body **English** per project convention for skills; operational outputs the agent produces stay **Korean**.

6. **Alert on drift** — Compare newly fetched `last_edited_time` (or content hash) to the value embedded in the skill’s Change log. If newer: output a **Korean alert** listing diff summary (high level) and recommend **regenerate** or **merge**; optionally post to **Slack MCP** on the team’s agreed planning-automation channel with Notion link.

7. **Notify stakeholders** — Optional: Slack thread with skill path + Notion canonical link + version bump rationale.

8. **Post-publish hygiene** — Remind the user that new skills may need registry updates **inside this repository** only (no paths outside the workspace). Suggest running the project’s skill quality audit workflow when available.

## Skill content standards (policy-derived)

- **Triggers**: Include both Korean and English trigger phrases copied or paraphrased from policy keywords.
- **Must / Must not**: Use imperative language for enforceable rules; keep examples generic (no customer PII).
- **Evidence**: Each critical rule should cite the Notion section title or block id in the Korean report (not necessarily inside SKILL.md body if redundancy is high — prefer a compact “Source map” table in the report).
- **Separation of concerns**: Operational outputs (emails, Slack posts, Notion pages) remain Korean; the SKILL.md instructional body stays English per repository convention.

## Notion MCP usage

- Fetch the canonical page and, if policies are split, follow **linked** child pages up to a user-defined depth cap (default: 2).
- If the policy is a **database row**, pull key properties (owner, status, effective date) and embed them in the skill’s **Scope** section in the Korean handoff summary.

## Slack MCP usage

- Post a concise “policy skill updated” message with: version, Notion link, skill slug, and whether breaking changes occurred.
- Put long diffs in a **thread**, not the main message.

## Output structure (sections must be written in Korean)

1. Source policy (Notion link, scope)
2. Created/updated skill path and version
3. Rule → skill section mapping summary
4. Drift detection result (or state “in sync”)
5. Follow-ups (PR, skill audit, in-repo registry update guidance)

## Examples

- **HR data-handling policy** → Skill with “Must NOT” data clauses + verification checklist before any customer-facing copy.

- **Design token governance** → Skill referencing Notion policy + internal checklist; triggers for “token”, “component rename”.

- **Security response policy** → Skill emphasizing severity routing, evidence capture, and comms gates; pair with incident workflows if present in the library.

## Quality checklist

- YAML `name` matches directory slug conventions (lowercase, hyphenated).
- `description` includes boundaries (“Do NOT use for …”) aligned with policy scope.
- Version bump rationale is understandable to non-authors.
- Drift detection records **what** changed at a high level, not full unredacted policy text in Slack.

## Error handling

- **Notion fetch fails**: Retry once; then output error class (auth, page deleted, rate limit) and stop without writing files.
- **Ambiguous policy scope**: Produce **two** skill drafts (narrow vs broad) only if user explicitly asked; otherwise ask one clarifying question.
- **Slug collision**: Append `-policy` or domain prefix; document rename in the report.
