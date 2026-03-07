# Generate PRD

Create PRD based on topic/meeting.

## Topic: $ARGUMENTS

> Pre-condition: Read `my-specs/CONTEXT.md` first.

## Principles
1. **Context First**: Read `my-specs/CONTEXT.md`, existing `PRDs/`, and backend source code.
2. **Why-Driven**: Record "Why needed?" and "Decisions".
3. **No Mock**: Design for Production.
4. **Full-Stack**: Analyze Backend (API, DB, SQL) impact.
5. **Architecture Compliance**: Must follow the defined architecture and guides.

## Architecture Compliance (MANDATORY)
Read `my-specs/CONTEXT.md` §6.1 and ensure design complies with A1~A6.
Especially **A1 Multi-tenancy**: `org_id`/`project_id` 격리, `AuthorizeProjectAccess`, 404 은닉.

## Path & Numbering
`my-specs/PRDs/{feature}/active/{NN}-{summary}.md`
*(See `my-specs/CONTEXT.md` for feature mapping)*

- `{NN}` is zero-padded two-digit order (`01`, `02`, ...), computed from `active/*.md` only.
- Ignore `archived/` and `archived/completed/` when generating a new PRD.
- If `active/` is empty, start at `01`.
- `{summary}` must be lowercase only. Do not use uppercase letters in the filename.

---

## Process

### 1. Context & Path
- Analyze `$ARGUMENTS` & Determine path.
- Check existing `PRDs/` and read relevant source code directly.
- **Review Architecture Standards**: Check if the feature touches Event-Driven, Storage, or NATS components.
- **Determine implementation order number**: Scan `my-specs/PRDs/{feature}/active/*.md` for the highest `{NN}-` prefix. Assign the next number within that feature.
- **Do not use archived numbering**: `archived/` is tracked separately for completion history.
- **Filename format**: Use `번호-{요약}.md` (`{NN}-{summary}.md`) and keep `{summary}` lowercase.

### 2. Information Gathering
- **With Minutes**: Draft PRD immediately.
- **Without Minutes**: Interview User.
  - Use **Multiple Choice (1a, 1b)** questions.
  - **Required**: Background, Goal, Must-haves, Backend Impact.

### 3. Write PRD
- Use the **Template** below.
- **Backend Impact Analysis** is MANDATORY.

---

## Template

```markdown
# [Feature] PRD

## 1. Overview
### 1.1 Background
- Why needed? Current problems?
### 1.2 Goals
- What to achieve?

## 2. Planning Intent
### 2.1 Must-have (Crucial)
- [ ] Core Feature 1
### 2.2 Should-have
- [ ] Nice-to-have 1

## 3. Decisions
### 3.1 [Decision Topic]
**Problem**: ...
**Options**:
| Option | Pros | Cons |
|---|---|---|
| A | ... | ... |
**Decision**: ...
**Reason**: ...

## 4. Spec
### 4.1 Functional
...
### 4.2 Technical
...
#### 4.2.1 Backend Impact (Mandatory)
- [ ] API Changes (Request/Response)
- [ ] DB Schema Changes (Follow `database_migrations_guide.md`)
- [ ] Repository/Query Modifications
- [ ] Legacy Compatibility
- [ ] Multi-tenancy (A1): `organization_id`/`project_id` 격리, `AuthorizeProjectAccess` 호출, 404 은닉
- [ ] Event-Driven/NATS Impact (Follow `event_driven_design.md`, `nats_jetstream_guide.md`)
- [ ] Storage/NFS Impact (Follow `storage_architecture_guide.md`)
- [ ] Logging/Monitoring (Follow `victoria_logs_guide.md`)

### 4.3 UI/UX
...

## 5. Constraints & Future
...

## Appendix
### References
- [Doc Name](./path)
### Minutes
- [YYYY-MM-DD] Draft
```

## Checklist
- [ ] **Why & Decision**: Clear reasons?
- [ ] **Backend Impact**: Analyzed DB/API?
- [ ] **Architecture Compliance**: `CONTEXT.md` §6.1 (A1~A6) 준수? 특히 A1 Multi-tenancy 격리/인가?
- [ ] **Must-have**: Listed correctly?
- [ ] **Cross-Check**: No conflict with existing code?
- [ ] **Numbering**: Filename follows `{NN}-{summary}.md` in per-feature implementation order?
- [ ] **Lowercase**: `{summary}` uses lowercase only (no uppercase letters)?
