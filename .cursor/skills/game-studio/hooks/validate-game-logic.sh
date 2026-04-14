#!/usr/bin/env bash
# validate-game-logic.sh — Pre-commit hook for game state consistency
# Install: copy to .cursor/hooks/ or symlink into .git/hooks/pre-commit
set -euo pipefail

SRC_DIR="alibi-network/src"
ERRORS=0

if [ ! -d "$SRC_DIR" ]; then
  echo "⚠ Source directory not found at $SRC_DIR — skipping game logic validation"
  exit 0
fi

echo "🔍 Validating game logic consistency..."

# 1. Puzzle bank integrity
if [ -f "$SRC_DIR/data/puzzleBank.ts" ]; then
  PUZZLE_COUNTS=$(grep -c "innocentIndex:" "$SRC_DIR/data/puzzleBank.ts" 2>/dev/null || echo "0")
  if [ "$PUZZLE_COUNTS" -lt 30 ]; then
    echo "❌ Puzzle bank has $PUZZLE_COUNTS puzzles — minimum 30 required"
    ERRORS=$((ERRORS + 1))
  else
    echo "✅ Puzzle bank: $PUZZLE_COUNTS puzzles found"
  fi
fi

# 2. Core interfaces must exist
for IFACE in "Puzzle" "Suspect" "Clue" "GameState"; do
  if ! grep -rq "interface $IFACE" "$SRC_DIR/types/" 2>/dev/null && \
     ! grep -rq "type $IFACE" "$SRC_DIR/types/" 2>/dev/null; then
    echo "❌ Missing core type: $IFACE"
    ERRORS=$((ERRORS + 1))
  fi
done

# 3. No console.log in engine files
ENGINE_LOGS=$(grep -rn "console\.log" "$SRC_DIR/lib/" 2>/dev/null | grep -v "// debug" | wc -l | tr -d ' ')
if [ "$ENGINE_LOGS" -gt 0 ]; then
  echo "⚠ $ENGINE_LOGS console.log statements in lib/ — remove before release"
fi

# 4. innocentIndex bounds check
if [ -f "$SRC_DIR/data/puzzleBank.ts" ]; then
  OUT_OF_BOUNDS=$(grep -n "innocentIndex:" "$SRC_DIR/data/puzzleBank.ts" 2>/dev/null | \
    grep -v "innocentIndex: [0-8]" | wc -l | tr -d ' ')
  if [ "$OUT_OF_BOUNDS" -gt 0 ]; then
    echo "❌ Found innocentIndex outside valid range [0-8]"
    ERRORS=$((ERRORS + 1))
  fi
fi

# 5. Zustand store exports
if [ -f "$SRC_DIR/hooks/useGameState.ts" ]; then
  if ! grep -q "export" "$SRC_DIR/hooks/useGameState.ts" 2>/dev/null; then
    echo "❌ useGameState.ts has no exports"
    ERRORS=$((ERRORS + 1))
  fi
fi

if [ "$ERRORS" -gt 0 ]; then
  echo ""
  echo "🚫 Game logic validation FAILED with $ERRORS error(s)"
  exit 1
fi

echo "✅ Game logic validation passed"
exit 0
