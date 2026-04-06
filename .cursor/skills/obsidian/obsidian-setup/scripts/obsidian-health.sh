#!/usr/bin/env bash
set -euo pipefail

PASS=0
FAIL=0
WARN=0

check() {
  local label="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "  ✅ $label"
    ((PASS++))
  else
    echo "  ❌ $label"
    ((FAIL++))
  fi
}

warn() {
  local label="$1"
  echo "  ⚠️  $label"
  ((WARN++))
}

echo "=== Obsidian CLI Health Check ==="
echo ""

# 1. Binary in PATH
echo "[1/4] CLI binary"
if command -v obsidian >/dev/null 2>&1; then
  echo "  ✅ obsidian found at $(command -v obsidian)"
  ((PASS++))
else
  echo "  ❌ obsidian not found in PATH"
  ((FAIL++))
  echo ""
  echo "Add to ~/.zprofile (macOS):"
  echo '  export PATH="/Applications/Obsidian.app/Contents/MacOS:$PATH"'
  echo ""
  echo "Result: $PASS passed, $FAIL failed, $WARN warnings"
  exit 1
fi

# 2. App running
echo "[2/4] Obsidian app"
if pgrep -x "Obsidian" >/dev/null 2>&1 || pgrep -f "obsidian" >/dev/null 2>&1; then
  echo "  ✅ Obsidian app is running"
  ((PASS++))
else
  echo "  ❌ Obsidian app is not running (CLI requires the app)"
  ((FAIL++))
fi

# 3. Version check
echo "[3/4] Version"
VERSION=$(obsidian version 2>/dev/null || echo "unknown")
if [[ "$VERSION" == "unknown" ]]; then
  echo "  ❌ Could not determine version"
  ((FAIL++))
else
  echo "  ✅ Version: $VERSION"
  MAJOR=$(echo "$VERSION" | cut -d. -f1)
  MINOR=$(echo "$VERSION" | cut -d. -f2)
  if [[ "$MAJOR" -gt 1 ]] || { [[ "$MAJOR" -eq 1 ]] && [[ "$MINOR" -ge 12 ]]; }; then
    echo "  ✅ Version >= 1.12 (CLI supported)"
    ((PASS++))
  else
    echo "  ❌ Version < 1.12 (CLI requires 1.12+)"
    ((FAIL++))
  fi
fi

# 4. Vault access
echo "[4/4] Vault access"
VAULTS=$(obsidian vaults 2>/dev/null || echo "")
if [[ -n "$VAULTS" ]]; then
  VAULT_COUNT=$(echo "$VAULTS" | wc -l | tr -d ' ')
  echo "  ✅ $VAULT_COUNT vault(s) accessible"
  ((PASS++))
else
  warn "No vaults found or command failed"
fi

echo ""
echo "Result: $PASS passed, $FAIL failed, $WARN warnings"

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
