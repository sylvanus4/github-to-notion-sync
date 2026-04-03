---
description: "KIS environment diagnostics — check prerequisites, dependencies, and configuration with step-by-step remediation"
---

# KIS Setup

## Skill Reference

Read and follow the skill at `.cursor/skills/trading/kis-cs/SKILL.md` for customer-service tone guidance.

## Your Task

User input: $ARGUMENTS

Run KIS environment diagnostics and guide remediation. Parse `$ARGUMENTS`:

| Input | Action |
|---|---|
| (no args) | Full diagnostics + fix failed items in order |
| `check`, `status`, `상태` | Diagnostics only, no fixes |

## Execution Steps

### 1. Run diagnostics

Run `uv run scripts/kis/setup_check.py $(pwd)` and capture the JSON result.

Display as a status table:

| 항목 | 상태 | 비고 |
|---|---|---|
| Python 3.11+ | ✅ | 3.13.3 |
| uv | ✅ | |
| Node.js 18+ | ✅ | 20.10.0 |
| Docker | ✅ | Running |
| KIS 설정파일 | ✅ | VPS+prod |
| 인증 | ✅ | 모의투자 |

If `all_ok` is `true`, report "모든 설정이 완료되었습니다!" and stop.
If `check`/`status` arg, show table only and stop.

### 2. Fix prerequisites (if failed)

For each failed prerequisite, provide installation guidance:

| Item | Guidance |
|---|---|
| Python | `brew install python@3.11` or official site |
| uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Node.js | `brew install node` or nvm |
| Docker not installed | https://www.docker.com/products/docker-desktop |
| Docker not running | "Docker Desktop을 시작해주세요" — wait for user |

Do NOT proceed past prerequisites until all are resolved.

### 3. Fix KIS config (if failed)

If `~/KIS/config/kis_devlp.yaml` is missing or incomplete:
1. Create directory: `mkdir -p ~/KIS/config`
2. Show the YAML template and direct user to fill it manually
3. Credentials are obtained from [KIS OpenAPI Portal](https://apiportal.koreainvestment.com/)
4. Wait for user confirmation before proceeding

### 4. Fix auth (if failed)

If authentication is not active:
- Guide: "모의투자로 시작하려면 `/kis-auth vps`를 실행하세요"
- Do NOT auto-authenticate — user must choose the mode

### 5. Final verification

Re-run `uv run scripts/kis/setup_check.py $(pwd)` and display updated status.

If all pass: "Setup 완료! `/kis-my-status`로 계좌를 확인하거나, `/kis-help`로 사용법을 알아보세요."
If partial: show remaining failures and suggest `/kis-setup check` later.

## Constraints

- NEVER read or write `kis_devlp.yaml` directly (security policy)
- NEVER output tokens, appkey, appsecret, or any credentials
- Each step is idempotent — skip already-completed steps
- Only reference `setup_check.py` JSON output for state assessment
- Warn user about time-consuming operations (e.g., Docker image pulls)
- Present all guidance in Korean
