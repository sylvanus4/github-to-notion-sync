---
name: dev-planning-bridge
description: >-
  개발 결과물에서 기획서 생성, 품질 점검, 문구 보강, 디자인 변경 연동까지
  End-to-End 역기획 파이프라인을 오케스트레이션합니다. code-to-spec,
  spec-quality-gate, policy-text-generator, design-system-tracker,
  md-to-notion 스킬을 자동 조합합니다. Use when the user asks to "역기획
  파이프라인", "전체 역기획", "코드에서 기획서 전체 프로세스", "dev planning
  bridge", "full reverse spec pipeline", "개발 기획 브릿지", "end-to-end
  역기획", "코드 분석부터 노션까지", or wants the complete pipeline from code
  analysis to Notion publishing with quality gates. Do NOT use for code
  analysis only (use code-to-spec). Do NOT use for spec review only (use
  spec-quality-gate). Do NOT use for text generation only (use
  policy-text-generator). Do NOT use for design tracking only (use
  design-system-tracker). Korean triggers: "역기획 파이프라인", "전체 역기획",
  "개발 기획 브릿지", "노션까지", "End-to-End".
metadata:
  author: "thaki"
  version: "1.0.1"
  category: "orchestrator"
---
# Dev-Planning Bridge — Reverse-spec orchestrator

Run the full reverse-spec pipeline from code analysis through optional Notion publish in one flow.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Input

| Input | Required | Notes |
|------|----------|------|
| **Code path** | **Yes** | Directory, file, or glob |
| Scope mode | Optional | `full` (default), `diff`, `today` |
| Policy doc path | Optional | For copy pass |
| API spec path | Optional | For quality cross-check |
| Figma URL | Optional | For design linkage |
| Flags | Optional | `--notion`, `--slack`, `--skip-design`, `--skip-text` |

## Pipeline architecture

```
Phase 1: code-to-spec           → Reverse spec (required)
Phase 2: spec-quality-gate      → Quality + auto-fix (required)
Phase 3: policy-text-generator  → Policy copy pass (optional)
Phase 4: design-system-tracker  → Design change linkage (optional)
Phase 5: md-to-notion           → Notion publish (--notion)
Phase 6: Slack notification     → Channel post (--slack)
```

---

## Workflow

### Phase 1: Reverse spec (`code-to-spec`)

1. Pass target path and scope mode to `code-to-spec`
2. Run three parallel analysis tracks (feature, state, flow) per that skill
3. Write structured spec → `docs/specs/{domain}/`

**Output**: Markdown spec file(s)

**Progress report** (example):
```
[Phase 1/6] code-to-spec complete
- Files analyzed: {N}
- Features: {N}
- State mappings: {N}
- User flows: {N}
- Saved: docs/specs/{domain}/{file}.md
```

### Phase 2: Quality gate (`spec-quality-gate`)

1. Feed Phase 1 output to `spec-quality-gate` with `--fix` where appropriate
2. Run all seven checks
3. If Critical/High issues exist, attempt auto-fix per skill
4. Re-validate after fixes

**Gate**: Proceed only if Critical = 0  
If Critical > 0 → retry `--fix` → if still blocked, stop and ask for manual fixes

**Progress report**:
```
[Phase 2/6] spec-quality-gate complete
- Verdict: PASS/FAIL
- Critical: {N} (fixed {N})
- High: {N}
- Medium: {N}
```

### Phase 3: Policy copy (optional)

Run only if `--skip-text` is **not** set and a policy document is available:

1. Run `policy-text-generator` on error/empty-state strings, etc.
2. Replace user-visible messages in the “exceptions” section with policy-aligned copy
3. Emit i18n key/value pairs when applicable

**Skip**: `--skip-text` or no policy input

### Phase 4: Design linkage (optional)

Run only if `--skip-design` is **not** set and mode is `diff` or `today`:

1. Use `design-system-tracker` in git/code diff mode
2. Append impact summary to the spec “changelog” section
3. Emit checklist of follow-ups for design alignment

**Skip**: `--skip-design`, `full` mode, or no design changes detected

### Phase 5: Notion (`--notion`)

1. Publish final spec via `md-to-notion` patterns
2. If multiple files, create sub-pages under the parent

### Phase 6: Slack (`--slack`)

1. Post summary to the planning automation channel (team default)
2. Thread with feature list, open states, and changes

**Message shape**: post a Korean summary per output rule, including domain name, counts (features, screen states, exceptions), quality verdict, optional Notion URL, and a pointer to the thread for details.

---

## Final report

After the pipeline:

```markdown
## Dev-Planning Bridge Report

### Pipeline summary
| Phase | Status | Duration |
|-------|--------|----------|
| 1. code-to-spec | Done | ~{N}s |
| 2. spec-quality-gate | PASS | ~{N}s |
| 3. policy-text-generator | Done/Skipped | ~{N}s |
| 4. design-system-tracker | Done/Skipped | ~{N}s |
| 5. md-to-notion | Done/Skipped | ~{N}s |
| 6. Slack | Done/Skipped | ~{N}s |

### Artifacts
- Spec: `docs/specs/{domain}/{file}.md`
- i18n: `{path}` (if Phase 3 ran)
- Notion: {URL} (if Phase 5 ran)
- Slack: {channel} (if Phase 6 ran)

### Manual follow-ups
- [ ] Spec review and approval
- [ ] Define {N} open states
- [ ] Address {N} design deltas
```

---

## Examples

### Example 1: Minimal (code → spec only)

User: "Reverse-spec `src/pages/orders/`"

Phases 1–2 run; 3–6 skipped without flags.

### Example 2: Full publish

User: "Reverse-spec today’s code to Notion and Slack" `--notion` `--slack`

Runs Phases 1–6 as applicable (policy skip if no doc).

### Example 3: With policy

User: "Reverse-spec payments code with policy doc"

Phase 3 runs copy alignment; others as configured.

---

## Error handling

| Error | Action |
|-------|--------|
| Phase 1 fails | Report error; verify paths/structure; stop |
| Phase 2 Critical unresolved | Explain auto-fix failure; stop for manual edit |
| Phase 3/4 fails | Skip non-required phase; continue |
| Phase 5 fails | Keep local files; report Notion error |
| Phase 6 fails | Keep local + Notion; report Slack error |

## Troubleshooting

- **Stuck at Phase 2**: Manually fix Critical items, rerun `spec-quality-gate` alone
- **Unwanted Phase 3/4**: Pass `--skip-text` / `--skip-design`
- **Notion failures**: Check MCP auth and page permissions
