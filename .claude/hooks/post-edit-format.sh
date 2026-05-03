#!/bin/bash
# Auto-format after file edits
FILE="$CLAUDE_FILE_PATH"
if [ -z "$FILE" ]; then
  exit 0
fi

case "$FILE" in
  *.go)
    gofmt -w "$FILE" 2>/dev/null || true
    ;;
  *.ts|*.tsx|*.js|*.jsx|*.json|*.css|*.scss)
    npx prettier --write "$FILE" 2>/dev/null || true
    ;;
esac
