#!/usr/bin/env bash
# KIS Secret Scan — standalone hook script
# Scans text (piped via stdin or passed as $1) for KIS secret patterns.
# Can be invoked from session-end.js, CI, or manually.
#
# Usage:
#   echo "some text" | bash .cursor/hooks/scripts/kis-secret-scan.sh
#   bash .cursor/hooks/scripts/kis-secret-scan.sh "some text to scan"
#
# Exit codes: 0 = clean or no input, 1 = secret pattern detected

set -euo pipefail

PROJECT_DIR="${CURSOR_PROJECT_DIR:-$(cd "$(dirname "$0")/../../.." && pwd)}"
LOG_DIR="$PROJECT_DIR/.cursor/logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
TODAY="${TIMESTAMP:0:10}"
LOG_FILE="$LOG_DIR/kis-hooks-${TODAY}.log"

if [[ -n "${1:-}" ]]; then
  TEXT="$1"
elif [[ ! -t 0 ]]; then
  TEXT=$(cat)
else
  echo "[$TIMESTAMP] kis-secret-scan | no input | skip" >> "$LOG_FILE"
  exit 0
fi

if [[ -z "$TEXT" ]]; then
  echo "[$TIMESTAMP] kis-secret-scan | empty input | skip" >> "$LOG_FILE"
  exit 0
fi

SECRET_PATTERNS=(
  'appkey\s*=\s*["'"'"'][A-Za-z0-9]{8,}'
  'appsecret\s*=\s*["'"'"'][A-Za-z0-9]{8,}'
  'app_key\s*=\s*["'"'"'][A-Za-z0-9]{8,}'
  'app_secret\s*=\s*["'"'"'][A-Za-z0-9]{8,}'
  'APP_KEY\s*=\s*["'"'"'][A-Za-z0-9]{8,}'
  'APP_SECRET\s*=\s*["'"'"'][A-Za-z0-9]{8,}'
  'authorization:\s*Bearer\s+[A-Za-z0-9._-]{20,}'
  'approval_key\s*=\s*["'"'"'][A-Za-z0-9]{8,}'
)

FOUND=0
for pattern in "${SECRET_PATTERNS[@]}"; do
  MATCH=$(python3 -c "
import sys, re
text = sys.stdin.read()
m = re.search(r'$pattern', text, re.IGNORECASE)
if m:
    print(m.group(0)[:60])
    sys.exit(0)
sys.exit(1)
" <<< "$TEXT" 2>/dev/null) && {
    echo "[$TIMESTAMP] kis-secret-scan | DETECTED: ${MATCH}" >> "$LOG_FILE"
    echo "[KIS SECURITY] Secret pattern detected: ${MATCH}" >&2
    FOUND=1
  }
done

if [[ $FOUND -eq 0 ]]; then
  echo "[$TIMESTAMP] kis-secret-scan | clean" >> "$LOG_FILE"
  exit 0
else
  exit 1
fi
