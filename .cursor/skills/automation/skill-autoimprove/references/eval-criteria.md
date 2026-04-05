# Project eval criteria (ai-model-event-stock-analytics)

Use these **binary** checks when auto-improving **project-specific** skills under `.cursor/skills/` for this repository. Do not use this file as the default eval pack for skills copied from other products or generic cloud platforms.

## Scope

- **In scope**: Skills maintained for this repo (stock analytics, trading pipelines, local frontend/backend patterns).
- **Out of scope**: Skills that are pure upstream templates with no project customization — run `skill-optimizer` audit only unless the user explicitly scopes autoimprove to them.

## Required domain dimensions (add 1+ binary eval per dimension)

Each dimension below should map to at least one `EVAL N:` block in the skill’s eval suite (see [eval-guide.md](eval-guide.md)).

### 1. Financial terminology accuracy (POL-001)

- Pass: Output uses terms consistent with `docs/policies/01-product-identity.md` and [project-terminology-glossary.md](../../references/project-overrides/project-terminology-glossary.md) (e.g. ticker, OHLCV, P&L, signal, screener) and does not invent conflicting definitions.
- Fail: Misused finance terms, wrong market labels, or contradictions to the glossary.

### 2. Signal / analytics expression compliance

- Pass: Trading or screening language matches how this repo expresses signals (e.g. daily pipeline, technical indicators, event study) without fabricating data sources.
- Fail: Generic “buy now” advice without the skill’s stated methodology, or claims that imply live execution when the skill is read-only.

### 3. Design system adherence (Tailwind + Radix)

- Pass: Any UI guidance references **Tailwind CSS + Radix UI** and local tokens/conventions per [project-design-conventions.md](../../references/project-overrides/project-design-conventions.md); does not instruct use of Thaki Cloud TDS (`@thakicloud/shared`) or Figma handoff as the source of truth.
- Fail: TDS/Figma-mandatory wording, or `@thakicloud/shared` component mandates for this project’s UI.

### 4. Document quality alignment (POL-004)

- Pass: For skills that produce PRDs/specs/reports, outputs respect structure and quality expectations in `docs/policies/04-document-quality-standards.md` (e.g. required sections, traceability where applicable).
- Fail: Skeleton-only docs, missing mandatory sections defined in POL-004 for that artifact type.

### 5. Forbidden terms / product identity (POL-001)

- Pass: No **new** forbidden or deprecated product terms introduced by the mutated skill (per POL-001 and glossary); cloud-platform product framing is not added unless the skill explicitly targets cross-repo sync.
- Fail: Introduces disallowed naming, wrong product name, or upstream cloud UI stack as required for this app.

### 6. Output token discipline

- Pass: Skill output contains no sycophantic openers/closers ("Great question!", "Let me know if..."), no speculative suggestions beyond scope ("You might also want..."), no narration of internal steps ("Now I will..."), and leads with data/code before explanation.
- Fail: Output starts with pleasantries, ends with padding, includes unrequested suggestions, or buries findings after verbose methodology.

### 7. Token efficiency (quantitative — optional)

When `--measure-tokens` flag is passed to autoimprove, additionally track:

- **Output token count** per run (approximate via word count × 1.3)
- **Output-to-signal ratio**: actionable content lines / total output lines
- Log both metrics in `results.json` under each experiment's entry as `output_tokens_approx` and `signal_ratio`
- A mutation that maintains eval pass rate while reducing output tokens by ≥ 10% counts as an improvement even if the binary score is unchanged

## Combining with user evals

User-provided 3–6 binary evals **replace or extend** this list. If the target skill is not finance-facing, still keep eval **#3** and **#5** when the skill touches frontend or identity; drop **#1–2** only when clearly irrelevant (e.g. pure infra script with no domain copy).
