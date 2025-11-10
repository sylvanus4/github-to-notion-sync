#!/bin/bash
# GitHub Actions를 로컬에서 테스트하는 스크립트

set -e

echo "🔍 로컬 GitHub Actions 테스트 시작..."
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Pre-commit hooks
echo "📝 Step 1: Pre-commit hooks 테스트..."
if make pre-commit; then
    echo -e "${GREEN}✅ Pre-commit hooks 통과${NC}"
else
    echo -e "${RED}❌ Pre-commit hooks 실패${NC}"
    exit 1
fi
echo ""

# Step 2: Lint
echo "🔍 Step 2: Ruff lint 테스트..."
if make lint; then
    echo -e "${GREEN}✅ Lint 통과${NC}"
else
    echo -e "${RED}❌ Lint 실패${NC}"
    exit 1
fi
echo ""

# Step 3: Format check
echo "🎨 Step 3: Format 체크..."
if black --check src/ tests/ 2>/dev/null; then
    echo -e "${GREEN}✅ Format 통과${NC}"
else
    echo -e "${YELLOW}⚠️  Format 필요 (make format 실행)${NC}"
fi
echo ""

# Step 4: Type check
echo "🔎 Step 4: Type check (mypy)..."
if make type-check 2>&1 | head -20; then
    echo -e "${YELLOW}⚠️  Type check warnings (허용됨)${NC}"
else
    echo -e "${YELLOW}⚠️  Type check warnings (허용됨)${NC}"
fi
echo ""

# Step 5: Security scan
echo "🔒 Step 5: Security scan (bandit)..."
if make security 2>&1 | tail -10; then
    echo -e "${GREEN}✅ Security scan 완료${NC}"
else
    echo -e "${YELLOW}⚠️  Security warnings (검토 필요)${NC}"
fi
echo ""

echo "================================================================"
echo -e "${GREEN}✅ 모든 필수 체크 완료!${NC}"
echo ""
echo "📌 다음 단계:"
echo "   1. git add -A"
echo "   2. git commit -m \"your message\""
echo "   3. git push origin main"
echo ""
echo "💡 팁: Act로 전체 워크플로우 테스트:"
echo "   act -j code-quality --container-architecture linux/amd64"
echo "================================================================"

