# Execution Steps Reference

## Prerequisites

| Tool | Check | Required For |
|------|-------|-------------|
| Python 3.11+ | `python3 --version` | Python checks |
| ruff | `ruff --version` | Python lint |
| black | `black --version` | Python format |
| mypy | `mypy --version` | Python type check |
| Go 1.22+ | `go version` | Go checks |
| Node 20+ | `node --version` | Frontend checks |
| npm | `npm --version` | Frontend checks |
| gitleaks | `gitleaks version` | Secret scan |

If a tool is missing, skip that gate and note it as `SKIPPED` in the report.

## Step 1: Secret Scan

```bash
gitleaks detect --source . --verbose 2>&1 || true
```

Record: pass / fail / skipped (if gitleaks not installed).

## Step 2: Python Lint & Type Check

Run sequentially; stop on first failure within each tool:

```bash
ruff check shared/ services/ --output-format=concise
black --check shared/ services/
mypy shared/python/common/ --ignore-missing-imports
```

## Step 3: Python Security Scan

```bash
pip-audit --strict --desc on 2>&1 || true
bandit -r shared/python/common/ -ll -ii 2>&1 || true
```

These are soft gates — record findings but do not block.

## Step 4: Python Tests

```bash
pytest shared/python/tests/ -x --tb=short
```

For per-service tests, iterate only services that have test files:

```bash
for svc in stt-pipeline nlp-state rag-engine llm-inference knowledge-manager \
           summary-crm feedback admin memory-service orchestration pii-redaction \
           analytics ingress-telephony vad-diarization tts-service chat-channel \
           email-channel sms-channel routing-engine; do
  if ls services/$svc/tests/*.py &>/dev/null; then
    cd services/$svc && pytest -x --tb=short && cd ../..
  fi
done
```

## Step 5: Go Build & Test

```bash
cd services/call-manager
go build ./...
go test -v ./...
```

If `golangci-lint` is installed:

```bash
golangci-lint run ./...
```

## Step 6: Frontend Lint, Type Check & Test

```bash
cd frontend
npm ci --prefer-offline 2>/dev/null || npm install
npm run lint
npm run type-check
npm test
npm run build
```

## Step 7: Schema Consistency

```bash
bash scripts/validate-schema.sh
```
