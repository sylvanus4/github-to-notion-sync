# Execute PRD

Implement a feature based on the PRD file.

## PRD File: $ARGUMENTS

> ⚠️ **Pre-condition**: Read `my-specs/CONTEXT.md` first.

---

## 🔑 Principles (Strict Rules)

1.  **PRD = Contract**: The PRD is a contract. If the implementation needs to differ from the PRD, **you MUST modify the PRD first**.
2.  **Must-have First**: Do not stop until all Must-have items in the PRD are completed.
3.  **Production Ready**: **No Mocking**. Actual DB/API integration is required.
4.  **Full-Stack Verification**: "Sent from Frontend" is not proof. You must verify **"Backend received and processed it (SQL)"**.
5.  **Config Sync**: When modifying Helm values in `tkai-deploy`, you MUST also update the local `.env`.

---

## 🚀 Execution Process (Step-by-Step)

### Step 0. Proof of Work: Context & Logic Check (CRITICAL)

Before starting implementation, verify the following and **output "Evidence Code"**. You cannot proceed without evidence.

1.  **Check PRD**: Load the `$ARGUMENTS` file.
2.  **Check Existing Implementation**: Read `_codebase/go/handler/{feature}.md` or actual code.
3.  **Architecture Compliance** (`my-specs/CONTEXT.md` §6.1 A1~A6 확인):
    *   Gap 발견 시 → PRD에 수정 태스크 추가 (Must-have).
4.  **Impact Analysis**:
    *   Check all references of target functions/components using `grep`.
    *   Provide analysis: **"This change affects files A and B, so they must be updated together."**
5.  **Logic Evidence (Required)**:
    *   For Frontend work: Read the connected **Backend Handler and Repository (SQL)** code.
    *   **Prove** by quoting 3+ lines: **"This parameter is processed at line X of this backend file."**
    *   *Example: "The `cluster` parameter is processed at line 150 of `text_generation_repository.go` in the clause `WHERE cluster_id = $1`."*
    *   **If no processing logic exists?** → Immediately add a backend implementation task to the PRD.

### Step 1. Plan
- Analyze Must-have items in the PRD.
- Use `todo_write` to create a detailed implementation plan.
- Include a plan for updating Helm and local `.env` if environment variables are needed.

### Step 2. Execute (No Legacy)
- **Do not reference Python code**. Follow Go/React standards only.
- Do not use `sharedApi` in `api.ts`.
- **Implementation Order**: DB (Migration) → Repository → Service → Handler → Frontend

### Step 3. Validate Build
- **Go Backend**: `cd ai-platform/backend/go && make build-all && make test-short && make lint`
- **Frontend**: `cd ai-platform/frontend && pnpm type-check && pnpm lint`

### Step 4. Update Status
- Update the Must-have checklist in the PRD (mark `[x]` with brief completion notes).
- Update the Revision History table with the current date and changes.

### Step 5. Archive PRD
- Keep the `번호-{요약}.md` format and move from `active/` to `archived/completed/`.
- Numbering is separated:
  - `active/` uses implementation order.
  - `archived/completed/` uses archive order.
- When archiving, compute next number from `archived/completed/*.md` in the same feature, then rename during move:
  ```
  mv <prd-dir>/active/{ACTIVE_NN}-{summary}.md <prd-dir>/archived/completed/{ARCHIVE_NN}-{summary}.md
  ```
  Example: `active/01-feature.md` → `archived/completed/11-feature.md`
- Filename must always be `번호-{요약}.md` with lowercase `{summary}` only (no uppercase letters).
- Do not re-number remaining active PRDs after archiving unless explicitly requested.
- Update cross-references in other active PRDs that pointed to the old filename.
- Verify the move succeeded (`ls` the destination) and that `active/` no longer contains the file.
- If the PRD has remaining Should-have or P2 items that are deferred (not blocking), note them in the Revision History before archiving. These can be tracked as separate follow-up PRDs if needed.
