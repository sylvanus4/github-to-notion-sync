#!/usr/bin/env bash
set -euo pipefail

# start-server.sh — Platform-aware launcher for the tutor companion server.
# Starts tutor-server.js, either foregrounded or backgrounded, and outputs
# the server-info JSON on success.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_JS="$SCRIPT_DIR/tutor-server.js"

PROJECT_DIR=""
HOST="127.0.0.1"
FOREGROUND=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-dir)
      PROJECT_DIR="$2"
      shift 2
      ;;
    --host)
      HOST="$2"
      shift 2
      ;;
    --foreground)
      FOREGROUND=true
      shift
      ;;
    *)
      echo '{"type":"error","message":"Unknown argument: '"$1"'"}' >&2
      exit 1
      ;;
  esac
done

if ! command -v node &>/dev/null; then
  echo '{"type":"error","message":"Node.js is not installed or not in PATH"}' >&2
  exit 1
fi

TIMESTAMP="$(date +%s)"

if [[ -n "$PROJECT_DIR" ]]; then
  SESSION_DIR="$PROJECT_DIR/.tutor/sessions/$TIMESTAMP"
else
  SESSION_DIR="/tmp/tutor-session-$TIMESTAMP"
fi

mkdir -p "$SESSION_DIR"

if [[ "$FOREGROUND" == true ]]; then
  RUN_FOREGROUND=true
else
  RUN_FOREGROUND=false
fi

MAX_ATTEMPTS=3

for attempt in $(seq 1 $MAX_ATTEMPTS); do
  PORT=$(( (RANDOM % 10000) + 50000 ))

  if [[ "$RUN_FOREGROUND" == true ]]; then
    exec node "$SERVER_JS" "$SESSION_DIR" "$HOST" "$PORT"
  fi

  node "$SERVER_JS" "$SESSION_DIR" "$HOST" "$PORT" &
  SERVER_PID=$!

  sleep 0.5

  if kill -0 "$SERVER_PID" 2>/dev/null; then
    SERVER_INFO="$SESSION_DIR/.server-info"
    if [[ -f "$SERVER_INFO" ]]; then
      cat "$SERVER_INFO"
      exit 0
    fi
  fi

  kill "$SERVER_PID" 2>/dev/null || true
  wait "$SERVER_PID" 2>/dev/null || true
done

echo '{"type":"error","message":"Failed to start server after '"$MAX_ATTEMPTS"' attempts"}' >&2
exit 1
